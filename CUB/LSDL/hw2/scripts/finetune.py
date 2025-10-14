#!/usr/bin/env python3
"""
Fine-tuning Script for Classification Task
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, models, datasets
from tqdm.notebook import tqdm
import copy
import argparse

from configs.config import Config


def finetune_model(backbone_path, output_model_path, method_name="unknown"):
    """
    Fine-tune a model using a pre-trained backbone.
    
    Args:
        backbone_path (str): Path to the pre-trained backbone weights
        output_model_path (str): Path to save the best fine-tuned model
        method_name (str): Name of the pretext method (for logging)
    """
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Transformations for the downstream classification task
    finetune_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create dataset using ImageFolder
    full_labeled_dataset = datasets.ImageFolder(Config.LABELED_PATH, transform=finetune_transforms)
    
    # Split labeled data into train and validation sets
    train_size = int(Config.TRAIN_VAL_SPLIT * len(full_labeled_dataset))
    val_size = len(full_labeled_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_labeled_dataset, [train_size, val_size])
    
    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE, shuffle=False, num_workers=2)
    
    # Get class names for later use
    class_names = full_labeled_dataset.classes
    print(f"Found {len(full_labeled_dataset)} labeled images in {len(class_names)} classes.")
    print("Classes:", class_names)
    
    # Initialize the final classification model
    finetune_model = models.resnet18(num_classes=Config.NUM_CLASSES)
    
    # Load the pre-trained backbone weights
    print(f"Loading pre-trained backbone weights from {backbone_path}...")
    try:
        finetune_model.load_state_dict(torch.load(backbone_path), strict=False)
        print("Successfully loaded backbone weights.")
    except Exception as e:
        print(f"Warning: Could not load backbone weights: {e}")
        print("Training from scratch...")
    
    finetune_model = finetune_model.to(device)
    
    # Define loss and optimizer for fine-tuning
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(finetune_model.parameters(), lr=Config.LEARNING_RATE_FINETUNE)
    
    best_val_acc = 0.0
    best_model_wts = copy.deepcopy(finetune_model.state_dict())
    
    print(f"Starting supervised fine-tuning ({method_name})...")
    
    for epoch in range(Config.FINETUNE_EPOCHS):
        # Training phase
        finetune_model.train()
        running_loss = 0.0
        correct_predictions = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{Config.FINETUNE_EPOCHS} (Train)")
        
        for images, labels in progress_bar:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = finetune_model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            correct_predictions += (predicted == labels).sum().item()
            progress_bar.set_postfix(loss=loss.item())
        
        train_acc = correct_predictions / len(train_dataset)
        
        # Validation phase
        finetune_model.eval()
        val_correct = 0
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = finetune_model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                _, predicted = torch.max(outputs.data, 1)
                val_correct += (predicted == labels).sum().item()
        
        val_acc = val_correct / len(val_dataset)
        print(f"Epoch {epoch+1}/{Config.FINETUNE_EPOCHS} - Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save the best model based on validation accuracy
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_wts = copy.deepcopy(finetune_model.state_dict())
            torch.save(best_model_wts, output_model_path)
            print(f"New best model saved with validation accuracy: {best_val_acc:.4f}")
    
    print(f"Finished fine-tuning ({method_name}). Best Validation Accuracy: {best_val_acc:.4f}")
    return class_names


def main():
    parser = argparse.ArgumentParser(description='Fine-tune a pre-trained backbone')
    parser.add_argument('--method', choices=['rotation', 'jigsaw', 'scratch'], 
                       default='rotation', help='Pretext method used for backbone')
    args = parser.parse_args()
    
    if args.method == 'rotation':
        backbone_path = Config.ROTATION_BACKBONE_PATH
        output_path = Config.BEST_MODEL_ROTATION_PATH
    elif args.method == 'jigsaw':
        backbone_path = Config.JIGSAW_BACKBONE_PATH
        output_path = Config.BEST_MODEL_JIGSAW_PATH
    else:  # scratch
        backbone_path = None
        output_path = Config.BEST_MODEL_PATH
    
    if backbone_path and not os.path.exists(backbone_path):
        print(f"Warning: Backbone weights not found at {backbone_path}")
        print("Training from scratch...")
        backbone_path = None
    
    finetune_model(backbone_path, output_path, args.method)


if __name__ == "__main__":
    main()