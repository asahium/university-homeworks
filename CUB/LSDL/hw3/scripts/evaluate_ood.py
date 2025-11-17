"""
Evaluate OOD robustness on CIFAR-10
"""
import sys
sys.path.append('.')

import torch
import torch.nn as nn
from torchvision.models import resnet18
import os
import json

from config.config import Config
from data.datasets import get_cifar10_ood_loader
from models.simclr import SimCLR
from models.byol import BYOL
from models.moco import MoCo
from utils.evaluation import evaluate_ood, strip_prefix_from_state_dict
from utils.logger import WandbLogger


class LinearProbe(nn.Module):
    """Linear probe wrapper for loading"""
    def __init__(self, encoder, num_classes=Config.NUM_CLASSES):
        super().__init__()
        self.encoder = encoder
        for param in self.encoder.parameters():
            param.requires_grad = False
        self.fc = nn.Linear(512, num_classes)
    
    def forward(self, x):
        with torch.no_grad():
            h = self.encoder(x)
        return self.fc(h)


def main():
    print("\n" + "="*60)
    print("OOD Robustness Evaluation on CIFAR-10")
    print("="*60)
    
    # Load OOD data
    ood_loader = get_cifar10_ood_loader(Config.SUPERVISED_BATCH_SIZE)
    print(f"Loaded CIFAR-10 OOD data (excluding frog class)")
    
    results = {}
    
    # 1. Supervised baseline
    print("\n[1/7] Evaluating Supervised Baseline...")
    model = resnet18(num_classes=Config.NUM_CLASSES)
    state_dict = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'supervised_baseline.pth'), map_location=Config.DEVICE)
    # Strip both _orig_mod. and model. prefixes
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.', 'model.'])
    model.load_state_dict(state_dict)
    model = model.to(Config.DEVICE)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['supervised'] = acc
    print(f"Supervised: {acc:.2f}%")
    
    # 2. SimCLR + Linear Probe
    print("\n[2/7] Evaluating SimCLR + Linear Probe...")
    ssl_model = SimCLR().to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'simclr_model_40.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    ssl_model.load_state_dict(state_dict)
    model = LinearProbe(ssl_model.encoder).to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'simclr_linear_probe.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['simclr_linear_probe'] = acc
    print(f"SimCLR + Linear Probe: {acc:.2f}%")
    
    # 3. SimCLR + Fine-tuning
    print("\n[3/7] Evaluating SimCLR + Fine-tuning...")
    model = resnet18(num_classes=Config.NUM_CLASSES)
    state_dict = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'simclr_finetuned.pth'), map_location=Config.DEVICE)
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    model = model.to(Config.DEVICE)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['simclr_finetuned'] = acc
    print(f"SimCLR + Fine-tuning: {acc:.2f}%")
    
    # 4. BYOL + Linear Probe
    print("\n[4/7] Evaluating BYOL + Linear Probe...")
    ssl_model = BYOL().to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'byol_model_40.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    ssl_model.load_state_dict(state_dict)
    model = LinearProbe(ssl_model.online_encoder).to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'byol_linear_probe.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['byol_linear_probe'] = acc
    print(f"BYOL + Linear Probe: {acc:.2f}%")
    
    # 5. BYOL + Fine-tuning
    print("\n[5/7] Evaluating BYOL + Fine-tuning...")
    model = resnet18(num_classes=Config.NUM_CLASSES)
    state_dict = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'byol_finetuned.pth'), map_location=Config.DEVICE)
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    model = model.to(Config.DEVICE)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['byol_finetuned'] = acc
    print(f"BYOL + Fine-tuning: {acc:.2f}%")
    
    # 6. MoCo + Linear Probe
    print("\n[6/7] Evaluating MoCo + Linear Probe...")
    ssl_model = MoCo().to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'moco_model_40.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    ssl_model.load_state_dict(state_dict)
    model = LinearProbe(ssl_model.encoder_q).to(Config.DEVICE)
    checkpoint = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'moco_linear_probe.pth'), map_location=Config.DEVICE)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['moco_linear_probe'] = acc
    print(f"MoCo + Linear Probe: {acc:.2f}%")
    
    # 7. MoCo + Fine-tuning
    print("\n[7/7] Evaluating MoCo + Fine-tuning...")
    model = resnet18(num_classes=Config.NUM_CLASSES)
    state_dict = torch.load(os.path.join(Config.CHECKPOINT_DIR, 'moco_finetuned.pth'), map_location=Config.DEVICE)
    state_dict = strip_prefix_from_state_dict(state_dict, prefix=['_orig_mod.'])
    model.load_state_dict(state_dict)
    model = model.to(Config.DEVICE)
    acc = evaluate_ood(model, ood_loader, Config.DEVICE)
    results['moco_finetuned'] = acc
    print(f"MoCo + Fine-tuning: {acc:.2f}%")
    
    # Save results
    results_path = os.path.join(Config.RESULTS_DIR, 'ood_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print("\n" + "="*60)
    print("OOD Evaluation Results Summary")
    print("="*60)
    for model_name, acc in results.items():
        print(f"{model_name:<30}: {acc:>6.2f}%")
    print("="*60)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()

