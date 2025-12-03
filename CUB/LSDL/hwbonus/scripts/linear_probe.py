"""
Linear probing for contrastive models
"""
import sys
sys.path.append('.')

import os
import torch
import torch.nn as nn
from tqdm import tqdm

from config.config import Config
from datasets import get_contrastive_dataloaders
from models import MultiFormatContrastiveModel, LinearProbe, LinearProbeConcatenated
from utils import Logger, strip_prefix_from_state_dict


def train_linear_probe(model, train_loader, val_loader, device, probe_type='1d', model_name=''):
    """
    Train a linear probe on frozen encoder.
    
    Args:
        model: Contrastive model
        train_loader: Training data loader
        val_loader: Validation data loader
        device: Device
        probe_type: '1d', '2d', or 'concat'
        model_name: Name of the contrastive model
    
    Returns:
        Best validation accuracy
    """
    # Get encoder based on probe type
    if probe_type == '1d':
        encoder = model.encoder_1d
        input_dim = Config.EMBEDDING_DIM
    elif probe_type == '2d':
        encoder = model.encoder_2d
        input_dim = Config.EMBEDDING_DIM
    else:  # concat
        input_dim = Config.EMBEDDING_DIM * 2
    
    # Create linear classifier
    if probe_type == 'concat':
        classifier = nn.Linear(input_dim, Config.NUM_CLASSES).to(device)
    else:
        classifier = nn.Linear(input_dim, Config.NUM_CLASSES).to(device)
    
    # Freeze encoder(s)
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    
    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(classifier.parameters(), lr=Config.LINEAR_PROBE_LR)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=Config.LINEAR_PROBE_EPOCHS
    )
    
    best_val_acc = 0
    
    for epoch in range(Config.LINEAR_PROBE_EPOCHS):
        # Training
        classifier.train()
        train_correct = 0
        train_total = 0
        
        for waveform, spectrogram, labels, speakers in tqdm(train_loader, desc=f"Probe {probe_type}", leave=False):
            waveform = waveform.to(device)
            spectrogram = spectrogram.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            with torch.no_grad():
                if probe_type == '1d':
                    embeddings = model.encoder_1d(waveform)
                elif probe_type == '2d':
                    embeddings = model.encoder_2d(spectrogram)
                else:  # concat
                    h1 = model.encoder_1d(waveform)
                    h2 = model.encoder_2d(spectrogram)
                    embeddings = torch.cat([h1, h2], dim=1)
            
            outputs = classifier(embeddings)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        scheduler.step()
        train_acc = 100. * train_correct / train_total
        
        # Validation
        classifier.eval()
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for waveform, spectrogram, labels, speakers in val_loader:
                waveform = waveform.to(device)
                spectrogram = spectrogram.to(device)
                labels = labels.to(device)
                
                if probe_type == '1d':
                    embeddings = model.encoder_1d(waveform)
                elif probe_type == '2d':
                    embeddings = model.encoder_2d(spectrogram)
                else:
                    h1 = model.encoder_1d(waveform)
                    h2 = model.encoder_2d(spectrogram)
                    embeddings = torch.cat([h1, h2], dim=1)
                
                outputs = classifier(embeddings)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_acc = 100. * val_correct / val_total
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}: Train Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%")
    
    return best_val_acc, classifier


def evaluate_linear_probe(model, classifier, test_loader, device, probe_type='1d'):
    """Evaluate linear probe on test set"""
    model.eval()
    classifier.eval()
    
    correct = 0
    total = 0
    
    with torch.no_grad():
        for waveform, spectrogram, labels, speakers in test_loader:
            waveform = waveform.to(device)
            spectrogram = spectrogram.to(device)
            labels = labels.to(device)
            
            if probe_type == '1d':
                embeddings = model.encoder_1d(waveform)
            elif probe_type == '2d':
                embeddings = model.encoder_2d(spectrogram)
            else:
                h1 = model.encoder_1d(waveform)
                h2 = model.encoder_2d(spectrogram)
                embeddings = torch.cat([h1, h2], dim=1)
            
            outputs = classifier(embeddings)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return 100. * correct / total


def run_linear_probing(model_name):
    """
    Run linear probing for a specific contrastive model.
    
    Args:
        model_name: Name of the contrastive model checkpoint
    
    Returns:
        Dict with results for each probe type
    """
    print(f"\n{'='*60}")
    print(f"Linear Probing: {model_name}")
    print("="*60)
    
    device = Config.DEVICE
    
    # Load model
    model = MultiFormatContrastiveModel().to(device)
    checkpoint_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_best.pth')
    
    if os.path.exists(checkpoint_path):
        state_dict = torch.load(checkpoint_path, map_location=device)
        state_dict = strip_prefix_from_state_dict(state_dict)
        model.load_state_dict(state_dict)
    else:
        print(f"Warning: Checkpoint not found: {checkpoint_path}")
        return None
    
    # Get data
    train_loader, val_loader, test_loader = get_contrastive_dataloaders(
        batch_size=Config.LINEAR_PROBE_BATCH_SIZE
    )
    
    results = {}
    
    for probe_type in ['1d', '2d', 'concat']:
        print(f"\nProbe type: {probe_type}")
        val_acc, classifier = train_linear_probe(
            model, train_loader, val_loader, device, probe_type, model_name
        )
        test_acc = evaluate_linear_probe(
            model, classifier, test_loader, device, probe_type
        )
        
        results[probe_type] = {
            'val_acc': val_acc,
            'test_acc': test_acc
        }
        print(f"  Best Val Acc: {val_acc:.2f}%, Test Acc: {test_acc:.2f}%")
    
    return results


def main():
    """Run linear probing for all contrastive models"""
    
    model_names = [
        'contrastive_no_aug',
        'contrastive_wav_aug',
        'contrastive_spec_aug',
        'contrastive_wav_aug_spec_aug'
    ]
    
    all_results = {}
    
    for model_name in model_names:
        results = run_linear_probing(model_name)
        if results:
            all_results[model_name] = results
    
    # Print summary
    print("\n" + "="*60)
    print("Linear Probing Summary")
    print("="*60)
    
    print(f"\n{'Model':<35} {'1D':<12} {'2D':<12} {'Concat':<12}")
    print("-" * 75)
    
    for model_name, results in all_results.items():
        acc_1d = results['1d']['test_acc']
        acc_2d = results['2d']['test_acc']
        acc_concat = results['concat']['test_acc']
        print(f"{model_name:<35} {acc_1d:.2f}%      {acc_2d:.2f}%      {acc_concat:.2f}%")
    
    # Save results
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    import json
    with open(os.path.join(Config.RESULTS_DIR, 'linear_probe_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)


if __name__ == "__main__":
    main()

