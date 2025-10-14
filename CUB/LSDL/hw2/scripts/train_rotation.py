#!/usr/bin/env python3
"""
Rotation Pretext Task Training Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, models
from tqdm.notebook import tqdm
import copy

from configs.config import Config
from src.datasets.datasets import RotationDataset


def train_rotation_pretext():
    """Train the rotation pretext task."""
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Define transformations for the pretext task
    pretext_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create Dataset and DataLoader
    pretrain_dataset = RotationDataset(Config.UNLABELED_PATH, transform=pretext_transforms)
    pretrain_loader = DataLoader(pretrain_dataset, batch_size=Config.BATCH_SIZE, 
                                shuffle=True, num_workers=2)
    
    print(f"Found {len(pretrain_dataset)} images for pre-training.")
    
    # Load ResNet-18 and modify the classifier for the pretext task
    pretext_model = models.resnet18(weights=None)  # Start from scratch
    num_features = pretext_model.fc.in_features
    pretext_model.fc = nn.Linear(num_features, 4)  # 4 classes for 4 rotation angles
    pretext_model = pretext_model.to(device)
    
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(pretext_model.parameters(), lr=Config.LEARNING_RATE_PRETRAIN)
    
    print("Starting self-supervised pre-training (Rotation)...")
    
    for epoch in range(Config.PRETRAIN_EPOCHS):
        pretext_model.train()
        running_loss = 0.0
        correct_predictions = 0
        total_predictions = 0
        
        progress_bar = tqdm(pretrain_loader, desc=f"Epoch {epoch+1}/{Config.PRETRAIN_EPOCHS}")
        
        for images, labels in progress_bar:
            images, labels = images.to(device), labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = pretext_model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Update statistics
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_predictions += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()
            
            # Update progress bar
            progress_bar.set_postfix(loss=loss.item(), acc=f"{(correct_predictions/total_predictions):.2f}")
        
        epoch_loss = running_loss / len(pretrain_loader.dataset)
        epoch_acc = correct_predictions / total_predictions
        print(f"Pre-training Epoch {epoch+1}/{Config.PRETRAIN_EPOCHS} - Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}")
    
    print("Finished pre-training.")
    
    # Save the backbone (feature extractor) weights
    # Remove the final fully connected layer ('fc') before saving
    backbone_weights = copy.deepcopy(pretext_model.state_dict())
    keys_to_remove = ["fc.weight", "fc.bias"]
    for key in keys_to_remove:
        if key in backbone_weights:
            del backbone_weights[key]
    
    torch.save(backbone_weights, Config.ROTATION_BACKBONE_PATH)
    print(f"Saved pre-trained backbone weights to '{Config.ROTATION_BACKBONE_PATH}'")


if __name__ == "__main__":
    train_rotation_pretext()