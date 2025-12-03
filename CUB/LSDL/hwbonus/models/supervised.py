"""
Supervised classification models
"""
import torch
import torch.nn as nn

import sys
sys.path.append('.')
from config.config import Config
from models.encoder_1d import Encoder1D, Encoder1DWithHead
from models.encoder_2d import Encoder2D, Encoder2DWithHead


class SupervisedModel1D(nn.Module):
    """
    Supervised model using 1D encoder for raw waveforms.
    """
    def __init__(
        self,
        num_classes=Config.NUM_CLASSES,
        embedding_dim=Config.EMBEDDING_DIM
    ):
        super().__init__()
        self.encoder = Encoder1D(embedding_dim=embedding_dim)
        self.classifier = nn.Linear(embedding_dim, num_classes)
    
    def forward(self, x):
        embedding = self.encoder(x)
        logits = self.classifier(embedding)
        return logits
    
    def get_embeddings(self, x):
        return self.encoder(x)


class SupervisedModel2D(nn.Module):
    """
    Supervised model using 2D encoder for spectrograms.
    """
    def __init__(
        self,
        num_classes=Config.NUM_CLASSES,
        embedding_dim=Config.EMBEDDING_DIM
    ):
        super().__init__()
        self.encoder = Encoder2D(embedding_dim=embedding_dim)
        self.classifier = nn.Linear(embedding_dim, num_classes)
    
    def forward(self, x):
        embedding = self.encoder(x)
        logits = self.classifier(embedding)
        return logits
    
    def get_embeddings(self, x):
        return self.encoder(x)


class LinearProbe(nn.Module):
    """
    Linear probe for evaluating frozen encoder representations.
    """
    def __init__(self, encoder, embedding_dim=Config.EMBEDDING_DIM, num_classes=Config.NUM_CLASSES):
        super().__init__()
        self.encoder = encoder
        # Freeze encoder
        for param in self.encoder.parameters():
            param.requires_grad = False
        
        self.classifier = nn.Linear(embedding_dim, num_classes)
    
    def forward(self, x):
        with torch.no_grad():
            embedding = self.encoder(x)
        logits = self.classifier(embedding)
        return logits


class LinearProbeConcatenated(nn.Module):
    """
    Linear probe on concatenated embeddings from both encoders.
    """
    def __init__(
        self,
        encoder_1d,
        encoder_2d,
        embedding_dim=Config.EMBEDDING_DIM,
        num_classes=Config.NUM_CLASSES
    ):
        super().__init__()
        self.encoder_1d = encoder_1d
        self.encoder_2d = encoder_2d
        
        # Freeze encoders
        for param in self.encoder_1d.parameters():
            param.requires_grad = False
        for param in self.encoder_2d.parameters():
            param.requires_grad = False
        
        self.classifier = nn.Linear(embedding_dim * 2, num_classes)
    
    def forward(self, waveform, spectrogram):
        with torch.no_grad():
            h1 = self.encoder_1d(waveform)
            h2 = self.encoder_2d(spectrogram)
        
        # Concatenate embeddings
        h = torch.cat([h1, h2], dim=1)
        logits = self.classifier(h)
        return logits


if __name__ == "__main__":
    # Test supervised models
    model_1d = SupervisedModel1D()
    model_2d = SupervisedModel2D()
    
    waveform = torch.randn(4, 1, 16000)
    spectrogram = torch.randn(4, 1, 64, 100)
    
    out_1d = model_1d(waveform)
    out_2d = model_2d(spectrogram)
    
    print(f"1D model output shape: {out_1d.shape}")
    print(f"2D model output shape: {out_2d.shape}")
    print(f"1D model parameters: {sum(p.numel() for p in model_1d.parameters()):,}")
    print(f"2D model parameters: {sum(p.numel() for p in model_2d.parameters()):,}")

