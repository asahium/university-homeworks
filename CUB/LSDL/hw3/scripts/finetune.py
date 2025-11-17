"""
Fine-tuning SSL models for classification
"""
import sys
sys.path.append('.')

import torch
import torch.nn as nn
from torchvision.models import resnet18
from tqdm import tqdm
import os

from config.config import Config
from data.datasets import get_stl10_dataloaders
from models.simclr import SimCLR
from models.byol import BYOL
from models.moco import MoCo
from utils.logger import WandbLogger
from utils.evaluation import evaluate_model, strip_prefix_from_state_dict


def train_epoch(model, loader, criterion, optimizer, scaler, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for images, labels in tqdm(loader, desc="Fine-tuning", leave=False):
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


def main():
    models_to_finetune = ['moco'] #['simclr', 'byol', 'moco']
    
    for model_name in models_to_finetune:
        print(f"\n{'='*50}")
        print(f"Fine-tuning: {model_name.upper()}")
        print(f"{'='*50}")
        
        # Initialize logger
        logger = WandbLogger(
            experiment_name=f"{model_name}-finetune",
            config_dict={
                "model": f"{model_name}-finetune",
                "epochs": Config.FINETUNE_EPOCHS,
                "batch_size": Config.SUPERVISED_BATCH_SIZE,
                "learning_rate": Config.FINETUNE_LR
            }
        )
        
        # Load data
        train_loader = get_stl10_dataloaders('train', Config.SUPERVISED_BATCH_SIZE, 'supervised')
        test_loader = get_stl10_dataloaders('test', Config.SUPERVISED_BATCH_SIZE, 'supervised')
        
        # Load pretrained SSL model and extract encoder
        if model_name == 'simclr':
            ssl_model = SimCLR().to(Config.DEVICE)
            checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'simclr_model.pth'), map_location=Config.DEVICE)
            # Handle both full checkpoint and state dict formats
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
            else:
                state_dict = checkpoint
            state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
            ssl_model.load_state_dict(state_dict)
            encoder = ssl_model.encoder
        elif model_name == 'byol':
            ssl_model = BYOL().to(Config.DEVICE)
            checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'byol_model.pth'), map_location=Config.DEVICE)
            # Handle both full checkpoint and state dict formats
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
            else:
                state_dict = checkpoint
            state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
            ssl_model.load_state_dict(state_dict)
            encoder = ssl_model.online_encoder
        elif model_name == 'moco':
            ssl_model = MoCo().to(Config.DEVICE)
            checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'moco_model.pth'), map_location=Config.DEVICE)
            # Handle both full checkpoint and state dict formats
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
            else:
                state_dict = checkpoint
            state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
            ssl_model.load_state_dict(state_dict)
            encoder = ssl_model.encoder_q
        
        # Create fine-tuned model
        model = resnet18(num_classes=Config.NUM_CLASSES)
        model.load_state_dict(encoder.state_dict(), strict=False)
        model = model.to(Config.DEVICE)
        
        # Training setup
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=Config.FINETUNE_LR,
            momentum=Config.FINETUNE_MOMENTUM,
            weight_decay=Config.FINETUNE_WEIGHT_DECAY
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.FINETUNE_EPOCHS)
        scaler = torch.amp.GradScaler('cuda', enabled=(Config.DEVICE.type == 'cuda'))
        
        # Training loop
        train_losses, train_accs, test_losses, test_accs = [], [], [], []
        
        for epoch in range(Config.FINETUNE_EPOCHS):
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
                "epoch": epoch + 1
            })
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{Config.FINETUNE_EPOCHS}] "
                      f"Train Acc: {train_acc:.2f}%, Test Acc: {test_acc:.2f}%")
        
        # Save model
        model_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_finetuned.pth')
        torch.save(model.state_dict(), model_path)
        print(f"Model saved to {model_path}")
        print(f"Final Test Accuracy: {test_accs[-1]:.2f}%")
        
        # Log summary
        logger.log_summary({
            "final_test_acc": test_accs[-1],
            "best_test_acc": max(test_accs)
        })
        
        # Save metrics
        metrics = {
            "train_losses": train_losses,
            "train_accs": train_accs,
            "test_losses": test_losses,
            "test_accs": test_accs
        }
        metrics_path = os.path.join(Config.RESULTS_DIR, f'{model_name}_finetune_metrics.json')
        logger.save_metrics_to_file(metrics, metrics_path)
        
        logger.finish()


if __name__ == "__main__":
    main()

