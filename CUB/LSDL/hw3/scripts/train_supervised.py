"""
Train supervised baseline model
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
from models.supervised import SupervisedModel
from utils.logger import WandbLogger
from utils.evaluation import evaluate_model


def train_epoch(model, loader, criterion, optimizer, scaler, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for images, labels in tqdm(loader, desc="Training", leave=False):
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        
        # Mark step begin for CUDA graphs compatibility with torch.compile
        torch.compiler.cudagraph_mark_step_begin()
        
        with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
            outputs = model(images)
            loss = criterion(outputs, labels)
        
        if device.type == 'cuda':
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(loader), 100. * correct / total


def find_latest_checkpoint(checkpoint_dir, prefix='supervised_baseline_'):
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
        experiment_name="supervised-baseline",
        config_dict={
            "model": "ResNet-18",
            "epochs": Config.SUPERVISED_EPOCHS,
            "batch_size": Config.SUPERVISED_BATCH_SIZE,
            "learning_rate": Config.SUPERVISED_LR,
            "optimizer": "SGD",
            "momentum": Config.SUPERVISED_MOMENTUM,
            "weight_decay": Config.SUPERVISED_WEIGHT_DECAY
        }
    )
    
    # Load data
    print("Loading data...")
    train_loader = get_stl10_dataloaders('train', Config.SUPERVISED_BATCH_SIZE, 'supervised')
    test_loader = get_stl10_dataloaders('test', Config.SUPERVISED_BATCH_SIZE, 'supervised')
    
    # Initialize model
    print(f"Training on device: {Config.DEVICE}")
    
    # Enable TF32 for better performance on Ampere GPUs
    if Config.DEVICE.type == 'cuda':
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    
    model = SupervisedModel().to(Config.DEVICE)
    
    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=Config.SUPERVISED_LR,
        momentum=Config.SUPERVISED_MOMENTUM,
        weight_decay=Config.SUPERVISED_WEIGHT_DECAY,
        fused=(Config.DEVICE.type == 'cuda')
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.SUPERVISED_EPOCHS)
    scaler = torch.amp.GradScaler('cuda', enabled=(Config.DEVICE.type == 'cuda'))
    
    # Check for existing checkpoints
    latest_ckpt, start_epoch = find_latest_checkpoint(Config.CHECKPOINT_DIR, 'supervised_baseline_')
    train_losses, train_accs, test_losses, test_accs = [], [], [], []
    
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
            train_accs = checkpoint.get('train_accs', [])
            test_losses = checkpoint.get('test_losses', [])
            test_accs = checkpoint.get('test_accs', [])
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
    print("\n=== Training Supervised Baseline ===")
    
    for epoch in range(start_epoch, Config.SUPERVISED_EPOCHS):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, scaler, Config.DEVICE)
        test_loss, test_acc = evaluate_model(model, test_loader, criterion, Config.DEVICE)
        scheduler.step()
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        
        # Log to wandb
        logger.log({
            "train_loss": train_loss,
            "train_acc": train_acc,
            "test_loss": test_loss,
            "test_acc": test_acc,
            "learning_rate": optimizer.param_groups[0]['lr'],
            "epoch": epoch + 1
        })
        
        if (epoch + 1) % 10 == 0:
            checkpoint = {
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'scaler_state_dict': scaler.state_dict(),
                'train_losses': train_losses,
                'train_accs': train_accs,
                'test_losses': test_losses,
                'test_accs': test_accs
            }
            model_path = os.path.join(Config.CHECKPOINT_DIR, f'supervised_baseline_{epoch+1}.pth')
            torch.save(checkpoint, model_path)
            print(f"\nCheckpoint saved to {model_path}")
            print(f"Epoch [{epoch+1}/{Config.SUPERVISED_EPOCHS}] "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
                  f"Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")
    
    # Save final model in old format for compatibility
    model_path = os.path.join(Config.CHECKPOINT_DIR, 'supervised_baseline.pth')
    torch.save(model.state_dict(), model_path)
    print(f"\nFinal model saved to {model_path}")
    print(f"Final Test Accuracy: {test_accs[-1]:.2f}%")
    
    # Log summary
    logger.log_summary({
        "final_test_acc": test_accs[-1],
        "final_train_acc": train_accs[-1],
        "best_test_acc": max(test_accs)
    })
    
    # Save metrics
    metrics = {
        "train_losses": train_losses,
        "train_accs": train_accs,
        "test_losses": test_losses,
        "test_accs": test_accs
    }
    metrics_path = os.path.join(Config.RESULTS_DIR, 'supervised_metrics.json')
    logger.save_metrics_to_file(metrics, metrics_path)
    print(f"Metrics saved to {metrics_path}")
    
    logger.finish()


if __name__ == "__main__":
    main()

