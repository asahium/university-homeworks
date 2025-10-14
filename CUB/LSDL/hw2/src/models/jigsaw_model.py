import torch
import torch.nn as nn
from torchvision import models


class JigsawNet(nn.Module):
    def __init__(self, num_permutations, grid_size=3):
        super(JigsawNet, self).__init__()
        # Load ResNet-18 backbone without the last layer
        resnet_backbone = models.resnet18(weights=None)  # weights=None, training from scratch
        self.backbone = nn.Sequential(*list(resnet_backbone.children())[:-1])
        
        # Classifier that takes concatenated features
        # grid_size^2 (patches) * 512 (features from ResNet18)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear((grid_size**2) * 512, 1024),
            nn.ReLU(),
            nn.Linear(1024, num_permutations)
        )

    def forward(self, x):
        # x has shape (batch_size, num_patches, 3, patch_size, patch_size)
        batch_size, num_patches, c, h, w = x.shape
        
        # Combine batch_size and num_patches to process all patches in one pass
        x = x.view(batch_size * num_patches, c, h, w)
        
        # Get features for each patch
        features = self.backbone(x)
        
        # Restore original batch dimension
        features = features.view(batch_size, num_patches, -1)
        
        # Pass through classifier
        output = self.classifier(features)
        return output