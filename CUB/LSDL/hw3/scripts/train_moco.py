"""
Train MoCo model
"""
import sys
sys.path.append('.')

import torch
import torch.nn as nn
from tqdm import tqdm
import os
import glob
import re

from config.config import Config
from data.datasets import get_stl10_dataloaders
from models.moco import MoCo
from utils.logger import WandbLogger


def train_epoch(model, loader, optimizer, scaler, device):
    """Train MoCo for one epoch"""
    model.train()
    total_loss = 0
    criterion = nn.CrossEntropyLoss()
    
    for (im_q, im_k), _ in tqdm(loader, desc="Training MoCo", leave=False):
        im_q, im_k = im_q.to(device), im_k.to(device)
        
        optimizer.zero_grad()
        
        # Mark step begin for CUDA graphs compatibility with torch.compile
        torch.compiler.cudagraph_mark_step_begin()
        
        with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
            logits, labels, _ = model(im_q, im_k)
            loss = criterion(logits, labels)
        
        if device.type == 'cuda':
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(loader)


def validate(model, loader, device):
    """Validate MoCo"""
    model.eval()
    total_loss = 0
    criterion = nn.CrossEntropyLoss()
    
    with torch.no_grad():
        for (im_q, im_k), _ in loader:
            im_q, im_k = im_q.to(device), im_k.to(device)
            
            # Mark step begin for CUDA graphs compatibility with torch.compile
            torch.compiler.cudagraph_mark_step_begin()
            
            with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
                logits, labels, _ = model(im_q, im_k)
                loss = criterion(logits, labels)
            
            total_loss += loss.item()
    
    return total_loss / len(loader)


def find_latest_checkpoint(checkpoint_dir, prefix='moco_model_'):
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
        experiment_name="moco",
        config_dict={
            "model": "MoCo-v2-ResNet18",
            "epochs": Config.MOCO_EPOCHS,
            "batch_size": Config.MOCO_BATCH_SIZE,
            "learning_rate": Config.MOCO_LR,
            "optimizer": "SGD",
            "momentum_encoder": Config.MOCO_MOMENTUM_ENCODER,
            "temperature": Config.MOCO_TEMPERATURE,
            "queue_size": Config.MOCO_QUEUE_SIZE
        }
    )
    
    # Load data
    print("Loading data...")
    train_loader = get_stl10_dataloaders('unlabeled', Config.MOCO_BATCH_SIZE, 'moco')
    val_loader = get_stl10_dataloaders('train', Config.MOCO_BATCH_SIZE, 'moco')
    
    # Initialize model
    print(f"Training on device: {Config.DEVICE}")
    
    # Enable TF32 for better performance on Ampere GPUs
    if Config.DEVICE.type == 'cuda':
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    
    model = MoCo().to(Config.DEVICE)
    
    # Training setup
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=Config.MOCO_LR,
        momentum=0.9,
        weight_decay=Config.MOCO_WEIGHT_DECAY,
        fused=(Config.DEVICE.type == 'cuda')
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.MOCO_EPOCHS)
    scaler = torch.amp.GradScaler('cuda', enabled=(Config.DEVICE.type == 'cuda'))
    
    # Check for existing checkpoints
    latest_ckpt, start_epoch = find_latest_checkpoint(Config.CHECKPOINT_DIR, 'moco_model_')
    train_losses, val_losses = [], []
    
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
        else:
            # Old format - only model state dict
            model.load_state_dict(checkpoint)
    else:
        start_epoch = 0
        print("\nNo checkpoint found, starting from scratch")
    
    # Note: torch.compile() disabled for MoCo due to compatibility issues with @torch.no_grad() decorators
    # in the momentum encoder update and queue management methods
    print("Note: torch.compile() disabled for MoCo (incompatible with @torch.no_grad() in forward pass)")
    
    # Training loop
    print("\n=== Training MoCo ===")
    
    for epoch in range(start_epoch, Config.MOCO_EPOCHS):
        train_loss = train_epoch(model, train_loader, optimizer, scaler, Config.DEVICE)
        val_loss = validate(model, val_loader, Config.DEVICE)
        scheduler.step()
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        
        # Log to wandb
        logger.log({
            "train_loss": train_loss,
            "val_loss": val_loss,
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
                'val_losses': val_losses
            }
            model_path = os.path.join(Config.CHECKPOINT_DIR, f'moco_model_{epoch+1}.pth')
            torch.save(checkpoint, model_path)
            print(f"\nCheckpoint saved to {model_path}")
            print(f"Epoch [{epoch+1}/{Config.MOCO_EPOCHS}] "
                  f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    
    # Save final model in old format for compatibility
    model_path = os.path.join(Config.CHECKPOINT_DIR, 'moco_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f"\nFinal model saved to {model_path}")
    print("MoCo training completed!")
    
    # Log summary
    logger.log_summary({
        "final_train_loss": train_losses[-1],
        "final_val_loss": val_losses[-1],
        "best_val_loss": min(val_losses)
    })
    
    # Save metrics
    metrics = {
        "train_losses": train_losses,
        "val_losses": val_losses
    }
    metrics_path = os.path.join(Config.RESULTS_DIR, 'moco_metrics.json')
    logger.save_metrics_to_file(metrics, metrics_path)
    print(f"Metrics saved to {metrics_path}")
    
    logger.finish()


if __name__ == "__main__":
    main()

