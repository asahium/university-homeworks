"""
Train multi-format contrastive learning model
"""
import sys
sys.path.append('.')

import os
import torch
from tqdm import tqdm

from config.config import Config
from datasets import get_contrastive_dataloaders
from models import MultiFormatContrastiveModel, symmetric_contrastive_loss
from utils import get_augmentation_transforms, Logger


def train_epoch(model, loader, optimizer, device):
    """Train contrastive model for one epoch"""
    model.train()
    total_loss = 0
    
    for waveform, spectrogram, labels, speakers in tqdm(loader, desc="Training", leave=False):
        waveform = waveform.to(device)
        spectrogram = spectrogram.to(device)
        
        optimizer.zero_grad()
        
        z1, z2, h1, h2 = model(waveform, spectrogram)
        loss = symmetric_contrastive_loss(z1, z2, Config.CONTRASTIVE_TEMPERATURE)
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(loader)


def validate(model, loader, device):
    """Validate contrastive model"""
    model.eval()
    total_loss = 0
    
    with torch.no_grad():
        for waveform, spectrogram, labels, speakers in tqdm(loader, desc="Validating", leave=False):
            waveform = waveform.to(device)
            spectrogram = spectrogram.to(device)
            
            z1, z2, h1, h2 = model(waveform, spectrogram)
            loss = symmetric_contrastive_loss(z1, z2, Config.CONTRASTIVE_TEMPERATURE)
            
            total_loss += loss.item()
    
    return total_loss / len(loader)


def train_contrastive_model(aug_waveform=False, aug_spectrogram=False, name_suffix=""):
    """
    Train a contrastive model with specified augmentations.
    
    Args:
        aug_waveform: Whether to augment waveforms
        aug_spectrogram: Whether to augment spectrograms
        name_suffix: Suffix for model name
    
    Returns:
        Trained model
    """
    # Determine model name
    aug_str = []
    if not aug_waveform and not aug_spectrogram:
        aug_str = ["no_aug"]
    else:
        if aug_waveform:
            aug_str.append("wav_aug")
        if aug_spectrogram:
            aug_str.append("spec_aug")
    model_name = f"contrastive_{'_'.join(aug_str)}{name_suffix}"
    
    print("\n" + "="*60)
    print(f"Training Contrastive Model: {model_name}")
    print(f"Waveform Augmentation: {aug_waveform}")
    print(f"Spectrogram Augmentation: {aug_spectrogram}")
    print("="*60)
    
    # Create directories
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    # Get augmentation transforms
    wave_transform, spec_transform = get_augmentation_transforms(
        aug_waveform=aug_waveform,
        aug_spectrogram=aug_spectrogram
    )
    
    # Get data
    train_loader, val_loader, test_loader = get_contrastive_dataloaders(
        batch_size=Config.CONTRASTIVE_BATCH_SIZE,
        transform_waveform=wave_transform if aug_waveform else None,
        transform_spectrogram=spec_transform if aug_spectrogram else None
    )
    
    # Initialize model
    device = Config.DEVICE
    model = MultiFormatContrastiveModel().to(device)
    
    # Training setup
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=Config.CONTRASTIVE_LR,
        weight_decay=Config.CONTRASTIVE_WEIGHT_DECAY
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=Config.CONTRASTIVE_EPOCHS
    )
    
    # Logger
    logger = Logger(
        model_name,
        config_dict={
            "model": "MultiFormatContrastiveModel",
            "epochs": Config.CONTRASTIVE_EPOCHS,
            "batch_size": Config.CONTRASTIVE_BATCH_SIZE,
            "lr": Config.CONTRASTIVE_LR,
            "temperature": Config.CONTRASTIVE_TEMPERATURE,
            "aug_waveform": aug_waveform,
            "aug_spectrogram": aug_spectrogram
        }
    )
    
    # Training loop
    best_val_loss = float('inf')
    train_losses, val_losses = [], []
    
    for epoch in range(Config.CONTRASTIVE_EPOCHS):
        train_loss = train_epoch(model, train_loader, optimizer, device)
        val_loss = validate(model, val_loader, device)
        scheduler.step()
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        
        if (epoch + 1) % 10 == 0:
            logger.log({
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "val_loss": val_loss
            })
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(),
                      os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_best.pth'))
    
    # Save final model
    torch.save(model.state_dict(),
              os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_final.pth'))
    
    logger.log_summary({
        "best_val_loss": best_val_loss,
        "final_train_loss": train_losses[-1]
    })
    
    logger.save_metrics_to_file({
        "train_losses": train_losses,
        "val_losses": val_losses
    }, os.path.join(Config.RESULTS_DIR, f'{model_name}_metrics.json'))
    
    logger.finish()
    
    print(f"\nBest validation loss: {best_val_loss:.4f}")
    
    return model, model_name


def train_all_contrastive_models():
    """Train all 4 contrastive models with different augmentation combinations"""
    
    augmentation_configs = [
        (False, False),  # No augmentation
        (True, False),   # Waveform augmentation only
        (False, True),   # Spectrogram augmentation only
        (True, True),    # Both augmentations
    ]
    
    models = {}
    
    for aug_wave, aug_spec in augmentation_configs:
        model, name = train_contrastive_model(
            aug_waveform=aug_wave,
            aug_spectrogram=aug_spec
        )
        models[name] = model
    
    return models


def main():
    """Main function"""
    print(f"Device: {Config.DEVICE}")
    
    models = train_all_contrastive_models()
    
    print("\n" + "="*60)
    print("Contrastive Training Complete")
    print("="*60)
    print(f"Trained {len(models)} models:")
    for name in models.keys():
        print(f"  - {name}")


if __name__ == "__main__":
    main()

