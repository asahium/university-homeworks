"""
2D Convolutional Encoder for log mel-spectrograms
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

import sys
sys.path.append('.')
from config.config import Config


class ConvBlock2D(nn.Module):
    """2D Convolutional block with BatchNorm and ReLU"""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            padding=padding
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class Encoder2D(nn.Module):
    """
    2D CNN Encoder for log mel-spectrograms.
    
    Args:
        in_channels: Number of input channels (1 for mono spectrogram)
        embedding_dim: Output embedding dimension
        channels: List of channel sizes for conv layers
        kernel_size: Kernel size for conv layers
    """
    def __init__(
        self,
        in_channels=1,
        embedding_dim=Config.EMBEDDING_DIM,
        channels=None,
        kernel_size=Config.ENCODER_2D_KERNEL_SIZE
    ):
        super().__init__()
        
        if channels is None:
            channels = Config.ENCODER_2D_CHANNELS
        
        layers = []
        prev_channels = in_channels
        
        for out_channels in channels:
            layers.append(ConvBlock2D(
                prev_channels,
                out_channels,
                kernel_size,
                stride=1,
                padding=kernel_size // 2
            ))
            layers.append(nn.MaxPool2d(2, 2))
            prev_channels = out_channels
        
        self.encoder = nn.Sequential(*layers)
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(channels[-1], embedding_dim)
    
    def forward(self, x):
        """
        Args:
            x: Input spectrogram of shape (batch, 1, n_mels, time)
        Returns:
            Embedding of shape (batch, embedding_dim)
        """
        if x.dim() == 3:
            x = x.unsqueeze(1)
        
        x = self.encoder(x)
        x = self.global_pool(x).squeeze(-1).squeeze(-1)
        x = self.fc(x)
        return x


class Encoder2DWithHead(nn.Module):
    """
    2D Encoder with classification head for supervised training.
    """
    def __init__(
        self,
        num_classes=Config.NUM_CLASSES,
        embedding_dim=Config.EMBEDDING_DIM,
        **encoder_kwargs
    ):
        super().__init__()
        self.encoder = Encoder2D(embedding_dim=embedding_dim, **encoder_kwargs)
        self.classifier = nn.Linear(embedding_dim, num_classes)
    
    def forward(self, x):
        embedding = self.encoder(x)
        logits = self.classifier(embedding)
        return logits
    
    def get_embeddings(self, x):
        return self.encoder(x)


if __name__ == "__main__":
    # Test the encoder
    model = Encoder2D()
    # Typical spectrogram shape: (batch, 1, n_mels, time_frames)
    # For 1 second audio at 16kHz with hop_length=160: time_frames ≈ 100
    x = torch.randn(4, 1, 64, 100)
    out = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {out.shape}")
    print(f"Number of parameters: {sum(p.numel() for p in model.parameters()):,}")

