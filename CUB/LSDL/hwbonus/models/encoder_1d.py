"""
1D Convolutional Encoder for raw audio waveforms
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

import sys
sys.path.append('.')
from config.config import Config


class ConvBlock1D(nn.Module):
    """1D Convolutional block with BatchNorm and ReLU"""
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        dilation=1,
        padding=None
    ):
        super().__init__()
        if padding is None:
            padding = (kernel_size - 1) * dilation // 2
        
        self.conv = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            dilation=dilation,
            padding=padding
        )
        self.bn = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class Encoder1D(nn.Module):
    """
    1D CNN Encoder for raw audio waveforms.
    Uses dilated convolutions with large kernels for capturing temporal patterns.
    
    Args:
        in_channels: Number of input channels (1 for mono audio)
        embedding_dim: Output embedding dimension
        channels: List of channel sizes for conv layers
        kernel_size: Kernel size for conv layers
        stride: Stride for conv layers
        dilation: Dilation factor for conv layers
    """
    def __init__(
        self,
        in_channels=1,
        embedding_dim=Config.EMBEDDING_DIM,
        channels=None,
        kernel_size=Config.ENCODER_1D_KERNEL_SIZE,
        stride=Config.ENCODER_1D_STRIDE,
        dilation=Config.ENCODER_1D_DILATION
    ):
        super().__init__()
        
        if channels is None:
            channels = Config.ENCODER_1D_CHANNELS
        
        layers = []
        prev_channels = in_channels
        
        for i, out_channels in enumerate(channels):
            # Use dilation for first few layers, then reduce
            layer_dilation = dilation if i < 2 else 1
            layers.append(ConvBlock1D(
                prev_channels,
                out_channels,
                kernel_size,
                stride=stride,
                dilation=layer_dilation
            ))
            prev_channels = out_channels
        
        self.encoder = nn.Sequential(*layers)
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(channels[-1], embedding_dim)
    
    def forward(self, x):
        """
        Args:
            x: Input waveform of shape (batch, 1, time) or (batch, time)
        Returns:
            Embedding of shape (batch, embedding_dim)
        """
        if x.dim() == 2:
            x = x.unsqueeze(1)
        
        x = self.encoder(x)
        x = self.global_pool(x).squeeze(-1)
        x = self.fc(x)
        return x


class Encoder1DWithHead(nn.Module):
    """
    1D Encoder with classification head for supervised training.
    """
    def __init__(
        self,
        num_classes=Config.NUM_CLASSES,
        embedding_dim=Config.EMBEDDING_DIM,
        **encoder_kwargs
    ):
        super().__init__()
        self.encoder = Encoder1D(embedding_dim=embedding_dim, **encoder_kwargs)
        self.classifier = nn.Linear(embedding_dim, num_classes)
    
    def forward(self, x):
        embedding = self.encoder(x)
        logits = self.classifier(embedding)
        return logits
    
    def get_embeddings(self, x):
        return self.encoder(x)


if __name__ == "__main__":
    # Test the encoder
    model = Encoder1D()
    x = torch.randn(4, 1, 16000)  # 4 samples, 1 channel, 1 second at 16kHz
    out = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {out.shape}")
    print(f"Number of parameters: {sum(p.numel() for p in model.parameters()):,}")

