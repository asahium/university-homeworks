#!/usr/bin/env python3
"""
Inference Script for Test Set Predictions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from torch.utils.data import DataLoader
from torchvision import transforms, models, datasets
from tqdm.notebook import tqdm
import pandas as pd
import argparse

from configs.config import Config
from src.datasets.datasets import TestDataset


def generate_predictions(model_path, output_csv_path, method_name="unknown"):
    """
    Generate predictions on test set using a trained model.
    
    Args:
        model_path (str): Path to the trained model weights
        output_csv_path (str): Path to save the submission CSV
        method_name (str): Name of the method (for logging)
    """
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Use validation transforms for the test set (no random augmentations)
    test_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Create test dataset and dataloader
    test_dataset = TestDataset(Config.TEST_PATH, transform=test_transforms)
    test_loader = DataLoader(test_dataset, batch_size=Config.BATCH_SIZE, shuffle=False, num_workers=2)
    
    # Get class names from the labeled dataset
    dummy_labeled_dataset = datasets.ImageFolder(Config.LABELED_PATH)
    class_names = dummy_labeled_dataset.classes
    print(f"Class names: {class_names}")
    
    # Load the best model for inference
    final_model = models.resnet18(num_classes=Config.NUM_CLASSES)
    
    if os.path.exists(model_path):
        final_model.load_state_dict(torch.load(model_path))
        print(f"Loaded model from {model_path}")
    else:
        print(f"Warning: Model not found at {model_path}")
        return
    
    final_model = final_model.to(device)
    final_model.eval()
    
    predictions = []
    image_ids = []
    
    print(f"Generating predictions on the test set using {method_name} model...")
    with torch.no_grad():
        for images, fnames in tqdm(test_loader, desc="Inference"):
            images = images.to(device)
            outputs = final_model(images)
            _, predicted_indices = torch.max(outputs, 1)
            
            predictions.extend([class_names[i] for i in predicted_indices.cpu().numpy()])
            image_ids.extend(fnames)
    
    # Create submission DataFrame
    submission_df = pd.DataFrame({
        'id': image_ids,
        'class': predictions
    })
    
    # Save to CSV
    submission_df.to_csv(output_csv_path, index=False)
    
    print(f"Submission file '{output_csv_path}' created successfully!")
    print(f"Generated {len(submission_df)} predictions")
    print(submission_df.head())
    
    return submission_df


def main():
    parser = argparse.ArgumentParser(description='Generate predictions on test set')
    parser.add_argument('--method', choices=['rotation', 'jigsaw', 'scratch'], 
                       default='rotation', help='Method used for training')
    args = parser.parse_args()
    
    if args.method == 'rotation':
        model_path = Config.BEST_MODEL_ROTATION_PATH
        output_path = Config.SUBMISSION_ROTATION_PATH
    elif args.method == 'jigsaw':
        model_path = Config.BEST_MODEL_JIGSAW_PATH
        output_path = Config.SUBMISSION_JIGSAW_PATH
    else:  # scratch
        model_path = Config.BEST_MODEL_PATH
        output_path = Config.SUBMISSION_PATH
    
    generate_predictions(model_path, output_path, args.method)


if __name__ == "__main__":
    main()