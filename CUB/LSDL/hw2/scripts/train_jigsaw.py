#!/usr/bin/env python3
"""
Jigsaw Pretext Task Training Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.notebook import tqdm

from configs.config import Config
from src.datasets.datasets import JigsawDataset
from src.models.jigsaw_model import JigsawNet
from src.utils import generate_permutations


def train_jigsaw_pretext():
    """Train the jigsaw puzzle pretext task."""
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Generate or load permutations
    permutations = generate_permutations(Config.N_PERMUTATIONS, Config.GRID_SIZE, 
                                       Config.PERMUTATIONS_PATH)
    
    # Transformations for each image patch
    pretext_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create dataset and dataloader
    pretrain_dataset = JigsawDataset(Config.UNLABELED_PATH, permutations, 
                                   grid_size=Config.GRID_SIZE, patch_size=Config.PATCH_SIZE, 
                                   transform=pretext_transforms)
    pretrain_loader = DataLoader(pretrain_dataset, batch_size=Config.BATCH_SIZE, 
                                shuffle=True, num_workers=2)
    
    print(f"Found {len(pretrain_dataset)} images for pre-training.")
    
    # Initialize model
    jigsaw_model = JigsawNet(num_permutations=Config.N_PERMUTATIONS, 
                           grid_size=Config.GRID_SIZE).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(jigsaw_model.parameters(), lr=Config.LEARNING_RATE_PRETRAIN)
    
    print("Starting self-supervised pre-training (Jigsaw)...")
    
    for epoch in range(Config.PRETRAIN_EPOCHS):
        jigsaw_model.train()
        running_loss = 0.0
        correct_predictions = 0
        total_predictions = 0
        
        progress_bar = tqdm(pretrain_loader, desc=f"Epoch {epoch+1}/{Config.PRETRAIN_EPOCHS}")
        
        for patches, labels in progress_bar:
            patches, labels = patches.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = jigsaw_model(patches)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * patches.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_predictions += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()
            
            progress_bar.set_postfix(loss=loss.item(), acc=f"{(correct_predictions/total_predictions):.2f}")
        
        epoch_acc = correct_predictions / total_predictions
        print(f"Pre-training Epoch {epoch+1}/{Config.PRETRAIN_EPOCHS} - Accuracy: {epoch_acc:.4f}")
    
    print("Pre-training completed.")
    
    # Save trained backbone weights
    torch.save(jigsaw_model.backbone.state_dict(), Config.JIGSAW_BACKBONE_PATH)
    print(f"Backbone weights saved to '{Config.JIGSAW_BACKBONE_PATH}'")


if __name__ == "__main__":
    train_jigsaw_pretext()