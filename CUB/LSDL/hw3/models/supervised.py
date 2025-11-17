"""
Supervised baseline model
"""
import torch.nn as nn
from torchvision.models import resnet18
from config.config import Config


class SupervisedModel(nn.Module):
    """ResNet-18 for supervised classification"""
    def __init__(self, num_classes=Config.NUM_CLASSES):
        super().__init__()
        self.model = resnet18(pretrained=False, num_classes=num_classes)
    
    def forward(self, x):
        return self.model(x)
    
    def get_encoder(self):
        """Return encoder without classification head"""
        encoder = resnet18(pretrained=False)
        encoder.fc = nn.Identity()
        encoder.load_state_dict(self.model.state_dict(), strict=False)
        return encoder

