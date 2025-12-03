"""
Train supervised models (1D and 2D encoders) on AudioMNIST
"""
import sys
sys.path.append('.')

import os
import torch
import torch.nn as nn
from tqdm import tqdm

from config.config import Config
from datasets import get_dataloaders, get_speaker_splits, AudioMNISTDataset, AudioMNISTSpectrogramDataset
from models import SupervisedModel1D, SupervisedModel2D
from utils import evaluate_model, Logger


def train_epoch(model, loader, criterion, optimizer, device, model_type='1d'):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch in tqdm(loader, desc="Training", leave=False):
        if len(batch) == 3:
            inputs, labels, speakers = batch
        else:
            inputs, labels = batch
        
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(loader), 100. * correct / total


def evaluate(model, loader, criterion, device):
    """Evaluate model"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating", leave=False):
            if len(batch) == 3:
                inputs, labels, speakers = batch
            else:
                inputs, labels = batch
            
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(loader), 100. * correct / total


def train_supervised_1d():
    """Train 1D supervised model on raw waveforms"""
    print("\n" + "="*60)
    print("Training Supervised 1D Model (Waveforms)")
    print("="*60)
    
    # Create directories
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    # Get data
    train_loader, val_loader, test_loader = get_dataloaders(
        batch_size=Config.SUPERVISED_BATCH_SIZE,
        return_both=False,
        use_spectrogram_only=False
    )
    
    # Initialize model
    device = Config.DEVICE
    model = SupervisedModel1D().to(device)
    
    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=Config.SUPERVISED_LR,
        weight_decay=Config.SUPERVISED_WEIGHT_DECAY
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=Config.SUPERVISED_EPOCHS
    )
    
    # Logger
    logger = Logger(
        "supervised_1d",
        config_dict={
            "model": "SupervisedModel1D",
            "epochs": Config.SUPERVISED_EPOCHS,
            "batch_size": Config.SUPERVISED_BATCH_SIZE,
            "lr": Config.SUPERVISED_LR
        }
    )
    
    # Training loop
    best_val_acc = 0
    train_losses, train_accs = [], []
    val_losses, val_accs = [], []
    
    for epoch in range(Config.SUPERVISED_EPOCHS):
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, '1d'
        )
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        val_losses.append(val_loss)
        val_accs.append(val_acc)
        
        if (epoch + 1) % 10 == 0:
            logger.log({
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "val_loss": val_loss,
                "val_acc": val_acc
            })
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 
                      os.path.join(Config.CHECKPOINT_DIR, 'supervised_1d_best.pth'))
    
    # Evaluate on test set
    model.load_state_dict(
        torch.load(os.path.join(Config.CHECKPOINT_DIR, 'supervised_1d_best.pth'))
    )
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    
    print(f"\nTest Accuracy (1D): {test_acc:.2f}%")
    
    # Save final model and metrics
    torch.save(model.state_dict(), 
              os.path.join(Config.CHECKPOINT_DIR, 'supervised_1d_final.pth'))
    
    logger.log_summary({
        "best_val_acc": best_val_acc,
        "test_acc": test_acc
    })
    
    logger.save_metrics_to_file({
        "train_losses": train_losses,
        "train_accs": train_accs,
        "val_losses": val_losses,
        "val_accs": val_accs,
        "test_acc": test_acc
    }, os.path.join(Config.RESULTS_DIR, 'supervised_1d_metrics.json'))
    
    logger.finish()
    
    return model, test_acc


def train_supervised_2d():
    """Train 2D supervised model on spectrograms"""
    print("\n" + "="*60)
    print("Training Supervised 2D Model (Spectrograms)")
    print("="*60)
    
    # Create directories
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    # Get data (spectrogram only)
    train_loader, val_loader, test_loader = get_dataloaders(
        batch_size=Config.SUPERVISED_BATCH_SIZE,
        use_spectrogram_only=True
    )
    
    # Initialize model
    device = Config.DEVICE
    model = SupervisedModel2D().to(device)
    
    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=Config.SUPERVISED_LR,
        weight_decay=Config.SUPERVISED_WEIGHT_DECAY
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=Config.SUPERVISED_EPOCHS
    )
    
    # Logger
    logger = Logger(
        "supervised_2d",
        config_dict={
            "model": "SupervisedModel2D",
            "epochs": Config.SUPERVISED_EPOCHS,
            "batch_size": Config.SUPERVISED_BATCH_SIZE,
            "lr": Config.SUPERVISED_LR
        }
    )
    
    # Training loop
    best_val_acc = 0
    train_losses, train_accs = [], []
    val_losses, val_accs = [], []
    
    for epoch in range(Config.SUPERVISED_EPOCHS):
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, '2d'
        )
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        val_losses.append(val_loss)
        val_accs.append(val_acc)
        
        if (epoch + 1) % 10 == 0:
            logger.log({
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "val_loss": val_loss,
                "val_acc": val_acc
            })
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(),
                      os.path.join(Config.CHECKPOINT_DIR, 'supervised_2d_best.pth'))
    
    # Evaluate on test set
    model.load_state_dict(
        torch.load(os.path.join(Config.CHECKPOINT_DIR, 'supervised_2d_best.pth'))
    )
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    
    print(f"\nTest Accuracy (2D): {test_acc:.2f}%")
    
    # Save final model and metrics
    torch.save(model.state_dict(),
              os.path.join(Config.CHECKPOINT_DIR, 'supervised_2d_final.pth'))
    
    logger.log_summary({
        "best_val_acc": best_val_acc,
        "test_acc": test_acc
    })
    
    logger.save_metrics_to_file({
        "train_losses": train_losses,
        "train_accs": train_accs,
        "val_losses": val_losses,
        "val_accs": val_accs,
        "test_acc": test_acc
    }, os.path.join(Config.RESULTS_DIR, 'supervised_2d_metrics.json'))
    
    logger.finish()
    
    return model, test_acc


def main():
    """Train both supervised models"""
    print(f"Device: {Config.DEVICE}")
    
    # Train 1D model
    model_1d, acc_1d = train_supervised_1d()
    
    # Train 2D model
    model_2d, acc_2d = train_supervised_2d()
    
    print("\n" + "="*60)
    print("Supervised Training Complete")
    print("="*60)
    print(f"1D Model (Waveforms) Test Accuracy: {acc_1d:.2f}%")
    print(f"2D Model (Spectrograms) Test Accuracy: {acc_2d:.2f}%")


if __name__ == "__main__":
    main()

