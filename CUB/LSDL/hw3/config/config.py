"""
Configuration file for contrastive learning experiments
"""
import torch

class Config:
    # General settings
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    SEED = 42
    NUM_WORKERS = 8
    PIN_MEMORY = True
    
    # Data settings
    DATA_ROOT = './data'
    CHECKPOINT_DIR = './checkpoints'
    RESULTS_DIR = './results'
    
    # STL-10 dataset
    IMG_SIZE = 96
    NUM_CLASSES = 10
    STL10_MEAN = (0.4467, 0.4398, 0.4066)
    STL10_STD = (0.2603, 0.2566, 0.2713)
    
    # Supervised training
    SUPERVISED_EPOCHS = 100
    SUPERVISED_BATCH_SIZE = 256
    SUPERVISED_LR = 0.1
    SUPERVISED_MOMENTUM = 0.9
    SUPERVISED_WEIGHT_DECAY = 5e-4
    
    # SimCLR settings
    SIMCLR_EPOCHS = 100
    SIMCLR_BATCH_SIZE = 4096
    SIMCLR_LR = 3e-4
    SIMCLR_TEMPERATURE = 0.5
    SIMCLR_PROJECTION_DIM = 128
    
    # BYOL settings
    BYOL_EPOCHS = 100
    BYOL_BATCH_SIZE = 512
    BYOL_LR = 3e-4
    BYOL_MOMENTUM = 0.996
    BYOL_PROJECTION_DIM = 256
    BYOL_HIDDEN_DIM = 4096
    
    # MoCo settings
    MOCO_EPOCHS = 40
    MOCO_BATCH_SIZE = 256
    MOCO_LR = 0.03
    MOCO_MOMENTUM_ENCODER = 0.999
    MOCO_TEMPERATURE = 0.2
    MOCO_QUEUE_SIZE = 4096
    MOCO_PROJECTION_DIM = 128
    MOCO_WEIGHT_DECAY = 1e-4
    
    # Linear probe settings
    LINEAR_PROBE_EPOCHS = 50
    LINEAR_PROBE_LR = 1e-3
    
    # Fine-tuning settings
    FINETUNE_EPOCHS = 50
    FINETUNE_LR = 0.01
    FINETUNE_MOMENTUM = 0.9
    FINETUNE_WEIGHT_DECAY = 5e-4
    
    # Weights & Biases
    WANDB_PROJECT = "contrastive-learning-stl10"
    WANDB_ENTITY = "asah1um-jetbrains"  # Set your wandb username here if needed
    WANDB_API_KEY = "165a14846024e5e38cebc82334b2306114de0a76"  # Set your wandb API key here (or set WANDB_API_KEY env variable)
    
    # Class names
    CLASS_NAMES = ['airplane', 'bird', 'car', 'cat', 'deer', 'dog', 'horse', 'monkey', 'ship', 'truck']

