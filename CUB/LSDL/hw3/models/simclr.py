"""
SimCLR model implementation
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import resnet18
from config.config import Config


class ProjectionHead(nn.Module):
    """Projection head for SimCLR"""
    def __init__(self, input_dim=512, hidden_dim=2048, output_dim=Config.SIMCLR_PROJECTION_DIM):
        super().__init__()
        self.projection = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.projection(x)


class SimCLR(nn.Module):
    """SimCLR model"""
    def __init__(self, base_encoder=None, projection_dim=Config.SIMCLR_PROJECTION_DIM):
        super().__init__()
        if base_encoder is None:
            base_encoder = resnet18(pretrained=False)
        
        self.encoder = base_encoder
        self.encoder.fc = nn.Identity()
        self.projection_head = ProjectionHead(input_dim=512, output_dim=projection_dim)
    
    def forward(self, x):
        h = self.encoder(x)
        z = self.projection_head(h)
        return h, z


def nt_xent_loss(z_i, z_j, temperature=Config.SIMCLR_TEMPERATURE):
    """NT-Xent loss (Normalized Temperature-scaled Cross Entropy Loss)"""
    batch_size = z_i.shape[0]
    
    # Normalize the features
    z_i = F.normalize(z_i, dim=1)
    z_j = F.normalize(z_j, dim=1)
    
    # Concatenate
    z = torch.cat([z_i, z_j], dim=0)  # 2N x D
    
    # Compute similarity matrix
    sim_matrix = torch.mm(z, z.t()) / temperature  # 2N x 2N
    
    # Create mask to exclude self-similarities
    mask = torch.eye(2 * batch_size, dtype=torch.bool, device=z.device)
    # Use -1e4 for FP16 compatibility (FP16 max ~65k)
    sim_matrix = sim_matrix.masked_fill(mask, float('-inf') if sim_matrix.dtype == torch.float32 else -1e4)
    
    # Positive pairs: (i, j) and (j, i)
    pos_sim = torch.exp(torch.cat([
        torch.diag(sim_matrix, batch_size),
        torch.diag(sim_matrix, -batch_size)
    ]))
    
    # Sum of all similarities (excluding self)
    neg_sim = torch.exp(sim_matrix).sum(dim=1)
    
    # Loss
    loss = -torch.log(pos_sim / neg_sim).mean()
    
    return loss

