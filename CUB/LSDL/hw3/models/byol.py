"""
BYOL model implementation
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from config.config import Config


class BYOLProjectionHead(nn.Module):
    """Projection head for BYOL"""
    def __init__(self, input_dim=512, hidden_dim=Config.BYOL_HIDDEN_DIM, 
                 output_dim=Config.BYOL_PROJECTION_DIM):
        super().__init__()
        self.projection = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.projection(x)


class BYOLPredictor(nn.Module):
    """Predictor head for BYOL (only in online network)"""
    def __init__(self, input_dim=Config.BYOL_PROJECTION_DIM, 
                 hidden_dim=Config.BYOL_HIDDEN_DIM, 
                 output_dim=Config.BYOL_PROJECTION_DIM):
        super().__init__()
        self.predictor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.predictor(x)


class BYOL(nn.Module):
    """BYOL model with online and target networks"""
    def __init__(self, base_encoder=None, 
                 projection_dim=Config.BYOL_PROJECTION_DIM,
                 hidden_dim=Config.BYOL_HIDDEN_DIM):
        super().__init__()
        
        if base_encoder is None:
            base_encoder = torchvision.models.resnet18(pretrained=False)
        
        # Online network
        self.online_encoder = base_encoder
        self.online_encoder.fc = nn.Identity()
        self.online_projector = BYOLProjectionHead(512, hidden_dim, projection_dim)
        self.predictor = BYOLPredictor(projection_dim, hidden_dim, projection_dim)
        
        # Target network (same architecture, no gradient)
        self.target_encoder = torchvision.models.resnet18(pretrained=False)
        self.target_encoder.fc = nn.Identity()
        self.target_projector = BYOLProjectionHead(512, hidden_dim, projection_dim)
        
        # Initialize target network with online network weights
        self.target_encoder.load_state_dict(self.online_encoder.state_dict())
        self.target_projector.load_state_dict(self.online_projector.state_dict())
        
        # Target network parameters do not require gradients
        for param in self.target_encoder.parameters():
            param.requires_grad = False
        for param in self.target_projector.parameters():
            param.requires_grad = False
    
    def forward(self, x1, x2):
        # Online network predictions
        h1_online = self.online_encoder(x1)
        z1_online = self.online_projector(h1_online)
        p1 = self.predictor(z1_online)
        
        h2_online = self.online_encoder(x2)
        z2_online = self.online_projector(h2_online)
        p2 = self.predictor(z2_online)
        
        # Target network projections (no gradient)
        with torch.no_grad():
            h1_target = self.target_encoder(x1)
            z1_target = self.target_projector(h1_target)
            
            h2_target = self.target_encoder(x2)
            z2_target = self.target_projector(h2_target)
        
        return p1, p2, z1_target, z2_target, z1_online
    
    @torch.no_grad()
    def update_target_network(self, momentum=Config.BYOL_MOMENTUM):
        """Exponential moving average update of target network"""
        for online_params, target_params in zip(self.online_encoder.parameters(), 
                                                  self.target_encoder.parameters()):
            target_params.data = momentum * target_params.data + (1 - momentum) * online_params.data
        
        for online_params, target_params in zip(self.online_projector.parameters(), 
                                                  self.target_projector.parameters()):
            target_params.data = momentum * target_params.data + (1 - momentum) * online_params.data


def byol_loss(p1, p2, z1_target, z2_target):
    """BYOL loss: mean squared error between predictor output and target projection"""
    # Normalize
    p1 = F.normalize(p1, dim=1)
    p2 = F.normalize(p2, dim=1)
    z1_target = F.normalize(z1_target, dim=1)
    z2_target = F.normalize(z2_target, dim=1)
    
    # Loss is symmetric
    loss = (2 - 2 * (p1 * z2_target).sum(dim=1)).mean() + (2 - 2 * (p2 * z1_target).sum(dim=1)).mean()
    return loss / 2

