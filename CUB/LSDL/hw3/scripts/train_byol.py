"""
Train BYOL model
"""
import sys
sys.path.append('.')

import torch
import numpy as np
from tqdm import tqdm
import os
import glob
import re

from config.config import Config
from data.datasets import get_stl10_dataloaders
from models.byol import BYOL, byol_loss
from utils.logger import WandbLogger


def train_epoch(model, loader, optimizer, scaler, device):
    """Train BYOL for one epoch"""
    model.train()
    total_loss = 0
    z_stds = []
    
    for (x1, x2), _ in tqdm(loader, desc="Training BYOL", leave=False):
        x1, x2 = x1.to(device), x2.to(device)
        
        optimizer.zero_grad()
        
        # Mark step begin for CUDA graphs compatibility with torch.compile
        torch.compiler.cudagraph_mark_step_begin()
        
        with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
            p1, p2, z1_target, z2_target, z_online = model(x1, x2)
            loss = byol_loss(p1, p2, z1_target, z2_target)
        
        if device.type == 'cuda':
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        
        # Update target network with momentum
        model.update_target_network()
        
        total_loss += loss.item()
        
        # Track standard deviation of projections
        with torch.no_grad():
            z_stds.append(z_online.std(dim=0).mean().item())
    
    return total_loss / len(loader), np.mean(z_stds)


def validate(model, loader, device):
    """Validate BYOL"""
    model.eval()
    total_loss = 0
    
    with torch.no_grad():
        for (x1, x2), _ in loader:
            x1, x2 = x1.to(device), x2.to(device)
            
            # Mark step begin for CUDA graphs compatibility with torch.compile
            torch.compiler.cudagraph_mark_step_begin()
            
            with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
                p1, p2, z1_target, z2_target, _ = model(x1, x2)
                loss = byol_loss(p1, p2, z1_target, z2_target)
            
            total_loss += loss.item()
    
    return total_loss / len(loader)


def find_latest_checkpoint(checkpoint_dir, prefix='byol_model_'):
    """Find the latest checkpoint file"""
    pattern = os.path.join(checkpoint_dir, f'{prefix}*.pth')
    checkpoints = glob.glob(pattern)
    
    if not checkpoints:
        return None, 0
    
    # Extract epoch numbers from filenames
    epoch_numbers = []
    for ckpt in checkpoints:
        match = re.search(rf'{prefix}(\d+)\.pth', os.path.basename(ckpt))
        if match:
            epoch_numbers.append((int(match.group(1)), ckpt))
    
    if not epoch_numbers:
        return None, 0
    
    # Return checkpoint with highest epoch number
    latest_epoch, latest_ckpt = max(epoch_numbers, key=lambda x: x[0])
    return latest_ckpt, latest_epoch


def main():
    # Create directories
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    # Initialize logger
    logger = WandbLogger(
        experiment_name="byol",
        config_dict={
            "model": "BYOL-ResNet18",
            "epochs": Config.BYOL_EPOCHS,
            "batch_size": Config.BYOL_BATCH_SIZE,
            "learning_rate": Config.BYOL_LR,
            "optimizer": "Adam",
            "momentum": Config.BYOL_MOMENTUM,
            "projection_dim": Config.BYOL_PROJECTION_DIM
        }
    )
    
    # Load data
    print("Loading data...")
    train_loader = get_stl10_dataloaders('unlabeled', Config.BYOL_BATCH_SIZE, 'byol')
    val_loader = get_stl10_dataloaders('train', Config.BYOL_BATCH_SIZE, 'byol')
    
    # Initialize model
    print(f"Training on device: {Config.DEVICE}")
    
    # Enable TF32 for better performance on Ampere GPUs
    if Config.DEVICE.type == 'cuda':
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    
    model = BYOL().to(Config.DEVICE)
    
    # Training setup
    optimizer = torch.optim.Adam(model.parameters(), lr=Config.BYOL_LR, fused=(Config.DEVICE.type == 'cuda'))
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.BYOL_EPOCHS)
    scaler = torch.amp.GradScaler('cuda', enabled=(Config.DEVICE.type == 'cuda'))
    
    # Check for existing checkpoints
    latest_ckpt, start_epoch = find_latest_checkpoint(Config.CHECKPOINT_DIR, 'byol_model_')
    train_losses, val_losses, z_stds = [], [], []
    
    if latest_ckpt:
        print(f"\nFound checkpoint: {latest_ckpt}")
        print(f"Resuming from epoch {start_epoch}")
        checkpoint = torch.load(latest_ckpt, map_location=Config.DEVICE)
        
        # Load model state
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
            scaler.load_state_dict(checkpoint['scaler_state_dict'])
            train_losses = checkpoint.get('train_losses', [])
            val_losses = checkpoint.get('val_losses', [])
            z_stds = checkpoint.get('z_stds', [])
        else:
            # Old format - only model state dict
            model.load_state_dict(checkpoint)
    else:
        start_epoch = 0
        print("\nNo checkpoint found, starting from scratch")
    
    # Compile model for speedup (PyTorch 2.0+)
    try:
        model = torch.compile(model, mode='max-autotune')
        print("Model compiled with torch.compile()")
    except Exception as e:
        print(f"torch.compile not available: {e}")
    
    # Training loop
    print("\n=== Training BYOL ===")
    
    for epoch in range(start_epoch, Config.BYOL_EPOCHS):
        train_loss, z_std = train_epoch(model, train_loader, optimizer, scaler, Config.DEVICE)
        val_loss = validate(model, val_loader, Config.DEVICE)
        scheduler.step()
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        z_stds.append(z_std)
        
        # Log to wandb (including projection std to monitor collapse)
        logger.log({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "projection_std": z_std,
            "learning_rate": optimizer.param_groups[0]['lr'],
            "epoch": epoch + 1
        })
        
        if (epoch + 1) % 20 == 0:
            checkpoint = {
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'scaler_state_dict': scaler.state_dict(),
                'train_losses': train_losses,
                'val_losses': val_losses,
                'z_stds': z_stds
            }
            model_path = os.path.join(Config.CHECKPOINT_DIR, f'byol_model_{epoch+1}.pth')
            torch.save(checkpoint, model_path)
            print(f"\nCheckpoint saved to {model_path}")
            print(f"Epoch [{epoch+1}/{Config.BYOL_EPOCHS}] "
                  f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, "
                  f"Z Std: {z_std:.4f}")
    
    # Save final model in old format for compatibility
    model_path = os.path.join(Config.CHECKPOINT_DIR, 'byol_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f"\nFinal model saved to {model_path}")
    print("BYOL training completed!")
    
    # Log summary
    logger.log_summary({
        "final_train_loss": train_losses[-1],
        "final_val_loss": val_losses[-1],
        "final_projection_std": z_stds[-1],
        "best_val_loss": min(val_losses)
    })
    
    # Save metrics
    metrics = {
        "train_losses": train_losses,
        "val_losses": val_losses,
        "projection_stds": z_stds
    }
    metrics_path = os.path.join(Config.RESULTS_DIR, 'byol_metrics.json')
    logger.save_metrics_to_file(metrics, metrics_path)
    print(f"Metrics saved to {metrics_path}")
    
    logger.finish()


if __name__ == "__main__":
    main()

