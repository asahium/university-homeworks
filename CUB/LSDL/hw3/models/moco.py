"""
MoCo v2 model implementation
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from config.config import Config


class MoCo(nn.Module):
    """MoCo v2 implementation with momentum encoder and queue"""
    def __init__(self, base_encoder=None, 
                 dim=Config.MOCO_PROJECTION_DIM,
                 K=Config.MOCO_QUEUE_SIZE,
                 m=Config.MOCO_MOMENTUM_ENCODER,
                 T=Config.MOCO_TEMPERATURE):
        super().__init__()
        
        self.K = K  # Queue size
        self.m = m  # Momentum coefficient
        self.T = T  # Temperature
        
        if base_encoder is None:
            base_encoder = torchvision.models.resnet18(pretrained=False)
        
        # Query encoder
        self.encoder_q = base_encoder
        self.encoder_q.fc = nn.Identity()
        self.projection_q = nn.Sequential(
            nn.Linear(512, 2048),
            nn.ReLU(),
            nn.Linear(2048, dim)
        )
        
        # Key encoder (momentum encoder)
        self.encoder_k = torchvision.models.resnet18(pretrained=False)
        self.encoder_k.fc = nn.Identity()
        self.projection_k = nn.Sequential(
            nn.Linear(512, 2048),
            nn.ReLU(),
            nn.Linear(2048, dim)
        )
        
        # Initialize key encoder with query encoder
        for param_q, param_k in zip(self.encoder_q.parameters(), self.encoder_k.parameters()):
            param_k.data.copy_(param_q.data)
            param_k.requires_grad = False
        
        for param_q, param_k in zip(self.projection_q.parameters(), self.projection_k.parameters()):
            param_k.data.copy_(param_q.data)
            param_k.requires_grad = False
        
        # Create the queue
        self.register_buffer("queue", torch.randn(dim, K))
        self.queue = F.normalize(self.queue, dim=0)
        self.register_buffer("queue_ptr", torch.zeros(1, dtype=torch.long))
    
    @torch.no_grad()
    def _momentum_update_key_encoder(self):
        """Momentum update of the key encoder"""
        for param_q, param_k in zip(self.encoder_q.parameters(), self.encoder_k.parameters()):
            param_k.data = param_k.data * self.m + param_q.data * (1. - self.m)
        
        for param_q, param_k in zip(self.projection_q.parameters(), self.projection_k.parameters()):
            param_k.data = param_k.data * self.m + param_q.data * (1. - self.m)
    
    @torch.no_grad()
    def _dequeue_and_enqueue(self, keys):
        """Update queue"""
        batch_size = keys.shape[0]
        
        ptr = int(self.queue_ptr)
        
        if ptr + batch_size <= self.K:
            self.queue[:, ptr:ptr + batch_size] = keys.T
        else:
            remaining = self.K - ptr
            self.queue[:, ptr:] = keys[:remaining].T
            self.queue[:, :batch_size - remaining] = keys[remaining:].T
        
        ptr = (ptr + batch_size) % self.K
        self.queue_ptr[0] = ptr
    
    def forward(self, im_q, im_k):
        """
        Input:
            im_q: a batch of query images
            im_k: a batch of key images
        Output:
            logits, targets
        """
        
        # Compute query features
        q = self.encoder_q(im_q)
        q = self.projection_q(q)
        q = F.normalize(q, dim=1)
        
        # Compute key features
        with torch.no_grad():
            self._momentum_update_key_encoder()
            
            k = self.encoder_k(im_k)
            k = self.projection_k(k)
            k = F.normalize(k, dim=1)
        
        # Compute logits
        # Positive logits: Nx1
        l_pos = torch.einsum('nc,nc->n', [q, k]).unsqueeze(-1)
        # Negative logits: NxK
        l_neg = torch.einsum('nc,ck->nk', [q, self.queue.clone().detach()])
        
        # Logits: Nx(1+K)
        logits = torch.cat([l_pos, l_neg], dim=1)
        
        # Apply temperature
        logits /= self.T
        
        # Labels: positive key indicators
        labels = torch.zeros(logits.shape[0], dtype=torch.long, device=logits.device)
        
        # Dequeue and enqueue
        self._dequeue_and_enqueue(k)
        
        return logits, labels, q

