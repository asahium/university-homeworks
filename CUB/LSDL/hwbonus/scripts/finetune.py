"""
Fine-tune self-supervised models for digit classification
"""
import sys
sys.path.append('.')

import os
import json
import torch
import torch.nn as nn
from tqdm import tqdm
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split

from config.config import Config
from datasets import get_dataloaders, get_contrastive_dataloaders, get_speaker_splits, AudioMNISTDataset, AudioMNISTSpectrogramDataset
from models import MultiFormatContrastiveModel
from utils import Logger, strip_prefix_from_state_dict


class FineTunedModel1D(nn.Module):
    """Fine-tuned model using 1D encoder from contrastive model"""
    def __init__(self, encoder, num_classes=Config.NUM_CLASSES):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Linear(Config.EMBEDDING_DIM, num_classes)
    
    def forward(self, x):
        embeddings = self.encoder(x)
        return self.classifier(embeddings)
    
    def get_embeddings(self, x):
        return self.encoder(x)


class FineTunedModel2D(nn.Module):
    """Fine-tuned model using 2D encoder from contrastive model"""
    def __init__(self, encoder, num_classes=Config.NUM_CLASSES):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Linear(Config.EMBEDDING_DIM, num_classes)
    
    def forward(self, x):
        embeddings = self.encoder(x)
        return self.classifier(embeddings)
    
    def get_embeddings(self, x):
        return self.encoder(x)


def train_epoch(model, loader, criterion, optimizer, device):
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


def finetune_contrastive_model(model_name, encoder_type='1d'):
    """
    Fine-tune a contrastive model for digit classification.
    
    Args:
        model_name: Name of the contrastive model
        encoder_type: '1d' or '2d'
    
    Returns:
        Trained model and test accuracy
    """
    print(f"\nFine-tuning {model_name} ({encoder_type} encoder)")
    
    device = Config.DEVICE
    
    # Load pretrained contrastive model
    contrastive_model = MultiFormatContrastiveModel().to(device)
    ckpt_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_best.pth')
    
    if not os.path.exists(ckpt_path):
        print(f"  Checkpoint not found: {ckpt_path}")
        return None, None
    
    state_dict = torch.load(ckpt_path, map_location=device)
    state_dict = strip_prefix_from_state_dict(state_dict)
    contrastive_model.load_state_dict(state_dict)
    
    # Create fine-tuned model
    if encoder_type == '1d':
        model = FineTunedModel1D(contrastive_model.encoder_1d).to(device)
        train_loader, val_loader, test_loader = get_dataloaders(
            batch_size=Config.SUPERVISED_BATCH_SIZE,
            use_spectrogram_only=False
        )
    else:
        model = FineTunedModel2D(contrastive_model.encoder_2d).to(device)
        train_loader, val_loader, test_loader = get_dataloaders(
            batch_size=Config.SUPERVISED_BATCH_SIZE,
            use_spectrogram_only=True
        )
    
    # Training setup - use lower learning rate for encoder
    encoder_params = list(model.encoder.parameters())
    classifier_params = list(model.classifier.parameters())
    
    optimizer = torch.optim.AdamW([
        {'params': encoder_params, 'lr': Config.FINETUNE_LR * 0.1},
        {'params': classifier_params, 'lr': Config.FINETUNE_LR}
    ], weight_decay=Config.FINETUNE_WEIGHT_DECAY)
    
    criterion = nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=Config.FINETUNE_EPOCHS
    )
    
    # Training loop
    best_val_acc = 0
    train_losses, train_accs = [], []
    val_losses, val_accs = [], []
    
    for epoch in range(Config.FINETUNE_EPOCHS):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        val_losses.append(val_loss)
        val_accs.append(val_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(),
                      os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_{encoder_type}_finetuned_best.pth'))
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}: Train Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%")
    
    # Load best model and evaluate on test set
    model.load_state_dict(
        torch.load(os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_{encoder_type}_finetuned_best.pth'))
    )
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    
    print(f"  Test Accuracy: {test_acc:.2f}%")
    
    return model, {
        'train_losses': train_losses,
        'train_accs': train_accs,
        'val_losses': val_losses,
        'val_accs': val_accs,
        'best_val_acc': best_val_acc,
        'test_acc': test_acc
    }


def evaluate_voice_biometrics_finetuned(model, test_dataset, device, model_type='1d'):
    """Evaluate voice biometrics for fine-tuned model"""
    from scripts.voice_biometrics import evaluate_voice_biometrics
    return evaluate_voice_biometrics(model, test_dataset, device, model_type)


def main():
    """Fine-tune all contrastive models"""
    print(f"Device: {Config.DEVICE}")
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    contrastive_models = [
        'contrastive_no_aug',
        'contrastive_wav_aug',
        'contrastive_spec_aug',
        'contrastive_wav_aug_spec_aug'
    ]
    
    all_results = {}
    
    for model_name in contrastive_models:
        print("\n" + "="*60)
        print(f"Fine-tuning: {model_name}")
        print("="*60)
        
        # Fine-tune 1D encoder
        model_1d, results_1d = finetune_contrastive_model(model_name, '1d')
        if results_1d:
            all_results[f'{model_name}_1d_finetuned'] = results_1d
        
        # Fine-tune 2D encoder
        model_2d, results_2d = finetune_contrastive_model(model_name, '2d')
        if results_2d:
            all_results[f'{model_name}_2d_finetuned'] = results_2d
    
    # Print summary
    print("\n" + "="*60)
    print("Fine-tuning Summary (Digit Classification)")
    print("="*60)
    
    print(f"\n{'Model':<45} {'Val Acc':<12} {'Test Acc':<12}")
    print("-" * 70)
    
    for model_name, results in all_results.items():
        print(f"{model_name:<45} {results['best_val_acc']:.2f}%      {results['test_acc']:.2f}%")
    
    # Save results
    # Convert to JSON-serializable format
    json_results = {}
    for k, v in all_results.items():
        json_results[k] = {
            'best_val_acc': v['best_val_acc'],
            'test_acc': v['test_acc']
        }
    
    with open(os.path.join(Config.RESULTS_DIR, 'finetune_results.json'), 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\nResults saved to {Config.RESULTS_DIR}/finetune_results.json")
    
    # Voice biometrics evaluation for fine-tuned models
    print("\n" + "="*60)
    print("Voice Biometrics Evaluation (Fine-tuned Models)")
    print("="*60)
    
    device = Config.DEVICE
    _, _, test_speakers = get_speaker_splits()
    test_waveform = AudioMNISTDataset(Config.DATA_ROOT, test_speakers, return_both=False)
    test_spectrogram = AudioMNISTSpectrogramDataset(Config.DATA_ROOT, test_speakers)
    
    biometrics_results = {}
    
    for model_name in contrastive_models:
        # 1D encoder
        ckpt_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_1d_finetuned_best.pth')
        if os.path.exists(ckpt_path):
            contrastive_model = MultiFormatContrastiveModel().to(device)
            model = FineTunedModel1D(contrastive_model.encoder_1d).to(device)
            model.load_state_dict(torch.load(ckpt_path, map_location=device))
            
            print(f"\n{model_name}_1d_finetuned:")
            res = evaluate_voice_biometrics_finetuned(model, test_waveform, device, '1d')
            biometrics_results[f'{model_name}_1d_finetuned'] = res
            print(f"  Speaker Classification Accuracy: {res['test_accuracy']:.2f}%")
        
        # 2D encoder
        ckpt_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_2d_finetuned_best.pth')
        if os.path.exists(ckpt_path):
            contrastive_model = MultiFormatContrastiveModel().to(device)
            model = FineTunedModel2D(contrastive_model.encoder_2d).to(device)
            model.load_state_dict(torch.load(ckpt_path, map_location=device))
            
            print(f"\n{model_name}_2d_finetuned:")
            res = evaluate_voice_biometrics_finetuned(model, test_spectrogram, device, '2d')
            biometrics_results[f'{model_name}_2d_finetuned'] = res
            print(f"  Speaker Classification Accuracy: {res['test_accuracy']:.2f}%")
    
    # Save biometrics results
    with open(os.path.join(Config.RESULTS_DIR, 'finetune_biometrics_results.json'), 'w') as f:
        json.dump(biometrics_results, f, indent=2)


if __name__ == "__main__":
    main()

