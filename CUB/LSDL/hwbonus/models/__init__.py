"""
Model implementations for AudioMNIST self-supervised learning
"""
from .encoder_1d import Encoder1D, Encoder1DWithHead
from .encoder_2d import Encoder2D, Encoder2DWithHead
from .contrastive import MultiFormatContrastiveModel, contrastive_loss, symmetric_contrastive_loss
from .supervised import SupervisedModel1D, SupervisedModel2D, LinearProbe, LinearProbeConcatenated

__all__ = [
    'Encoder1D',
    'Encoder1DWithHead',
    'Encoder2D', 
    'Encoder2DWithHead',
    'MultiFormatContrastiveModel',
    'contrastive_loss',
    'symmetric_contrastive_loss',
    'SupervisedModel1D',
    'SupervisedModel2D',
    'LinearProbe',
    'LinearProbeConcatenated'
]

