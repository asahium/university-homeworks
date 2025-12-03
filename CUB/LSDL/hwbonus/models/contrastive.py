"""
Multi-format Contrastive Learning Model
Implements contrastive learning between raw audio (1D) and spectrogram (2D) representations.
Based on: https://arxiv.org/abs/2103.06508
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

import sys
sys.path.append('.')
from config.config import Config
from models.encoder_1d import Encoder1D
from models.encoder_2d import Encoder2D


class ProjectionHead(nn.Module):
    """Projection head for contrastive learning"""
    def __init__(self, input_dim, hidden_dim=512, output_dim=128):
        super().__init__()
        self.projection = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.projection(x)


class MultiFormatContrastiveModel(nn.Module):
    """
    Multi-format contrastive learning model.
    Learns to align representations from raw audio (1D) and spectrograms (2D).
    
    Args:
        embedding_dim: Dimension of encoder embeddings
        projection_dim: Dimension of projection head output
    """
    def __init__(
        self,
        embedding_dim=Config.EMBEDDING_DIM,
        projection_dim=128
    ):
        super().__init__()
        
        # Encoders
        self.encoder_1d = Encoder1D(embedding_dim=embedding_dim)
        self.encoder_2d = Encoder2D(embedding_dim=embedding_dim)
        
        # Projection heads
        self.projection_1d = ProjectionHead(embedding_dim, output_dim=projection_dim)
        self.projection_2d = ProjectionHead(embedding_dim, output_dim=projection_dim)
    
    def forward(self, waveform, spectrogram):
        """
        Args:
            waveform: Raw audio of shape (batch, 1, time)
            spectrogram: Log mel spectrogram of shape (batch, 1, n_mels, time)
        
        Returns:
            z1: Projected embedding from 1D encoder
            z2: Projected embedding from 2D encoder
            h1: Raw embedding from 1D encoder
            h2: Raw embedding from 2D encoder
        """
        # Get embeddings
        h1 = self.encoder_1d(waveform)
        h2 = self.encoder_2d(spectrogram)
        
        # Project
        z1 = self.projection_1d(h1)
        z2 = self.projection_2d(h2)
        
        return z1, z2, h1, h2
    
    def get_embeddings(self, waveform=None, spectrogram=None):
        """Get raw embeddings without projection"""
        h1 = self.encoder_1d(waveform) if waveform is not None else None
        h2 = self.encoder_2d(spectrogram) if spectrogram is not None else None
        return h1, h2


def contrastive_loss(z1, z2, temperature=Config.CONTRASTIVE_TEMPERATURE):
    """
    InfoNCE contrastive loss between two views.
    
    Args:
        z1: Embeddings from view 1 (batch, dim)
        z2: Embeddings from view 2 (batch, dim)
        temperature: Temperature parameter
    
    Returns:
        loss: Scalar loss value
    """
    batch_size = z1.shape[0]
    
    # Normalize embeddings
    z1 = F.normalize(z1, dim=1)
    z2 = F.normalize(z2, dim=1)
    
    # Compute similarity matrix
    # Positive pairs: (z1[i], z2[i]) and (z2[i], z1[i])
    # Negative pairs: all other combinations
    
    # Concatenate for easier computation
    z = torch.cat([z1, z2], dim=0)  # (2N, dim)
    
    # Compute all pairwise similarities
    sim_matrix = torch.mm(z, z.t()) / temperature  # (2N, 2N)
    
    # Mask out self-similarities
    mask = torch.eye(2 * batch_size, dtype=torch.bool, device=z.device)
    sim_matrix = sim_matrix.masked_fill(mask, float('-inf'))
    
    # Positive pair indices
    # For z1[i], positive is z2[i] (at index batch_size + i)
    # For z2[i], positive is z1[i] (at index i)
    pos_indices = torch.cat([
        torch.arange(batch_size, 2 * batch_size, device=z.device),
        torch.arange(0, batch_size, device=z.device)
    ])
    
    # Compute loss using cross-entropy
    labels = pos_indices
    loss = F.cross_entropy(sim_matrix, labels)
    
    return loss


def symmetric_contrastive_loss(z1, z2, temperature=Config.CONTRASTIVE_TEMPERATURE):
    """
    Symmetric contrastive loss (average of both directions).
    
    Args:
        z1: Embeddings from view 1 (batch, dim)
        z2: Embeddings from view 2 (batch, dim)
        temperature: Temperature parameter
    
    Returns:
        loss: Scalar loss value
    """
    batch_size = z1.shape[0]
    
    # Normalize embeddings
    z1 = F.normalize(z1, dim=1)
    z2 = F.normalize(z2, dim=1)
    
    # Compute similarities
    sim_1_to_2 = torch.mm(z1, z2.t()) / temperature  # (N, N)
    sim_2_to_1 = sim_1_to_2.t()
    
    # Labels: diagonal elements are positive pairs
    labels = torch.arange(batch_size, device=z1.device)
    
    # Loss in both directions
    loss_1_to_2 = F.cross_entropy(sim_1_to_2, labels)
    loss_2_to_1 = F.cross_entropy(sim_2_to_1, labels)
    
    return (loss_1_to_2 + loss_2_to_1) / 2


if __name__ == "__main__":
    # Test the model
    model = MultiFormatContrastiveModel()
    
    waveform = torch.randn(8, 1, 16000)
    spectrogram = torch.randn(8, 1, 64, 100)
    
    z1, z2, h1, h2 = model(waveform, spectrogram)
    
    print(f"Waveform input shape: {waveform.shape}")
    print(f"Spectrogram input shape: {spectrogram.shape}")
    print(f"z1 shape: {z1.shape}")
    print(f"z2 shape: {z2.shape}")
    print(f"h1 shape: {h1.shape}")
    print(f"h2 shape: {h2.shape}")
    
    loss = symmetric_contrastive_loss(z1, z2)
    print(f"Contrastive loss: {loss.item():.4f}")
    
    print(f"Number of parameters: {sum(p.numel() for p in model.parameters()):,}")

