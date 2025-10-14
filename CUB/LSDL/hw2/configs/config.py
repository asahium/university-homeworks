import os


class Config:
    """Configuration class for the self-supervised learning project."""
    
    # Device configuration
    DEVICE = "cuda"  # Will be checked and set to "cpu" if CUDA is not available
    
    # Data paths
    BASE_PATH = 'data/'
    UNLABELED_PATH = os.path.join(BASE_PATH, 'train', 'unlabeled')
    LABELED_PATH = os.path.join(BASE_PATH, 'train', 'labeled')
    TEST_PATH = os.path.join(BASE_PATH, 'test')
    
    # Output paths
    CHECKPOINTS_DIR = 'checkpoints/'
    SUBMISSIONS_DIR = 'submissions/'
    
    # Training hyperparameters
    PRETRAIN_EPOCHS = 30
    FINETUNE_EPOCHS = 30
    BATCH_SIZE = 32
    LEARNING_RATE_PRETRAIN = 1e-3
    LEARNING_RATE_FINETUNE = 1e-4
    
    # Jigsaw puzzle parameters
    GRID_SIZE = 3  # 3x3 grid
    PATCH_SIZE = 64  # Size of each patch
    N_PERMUTATIONS = 100  # Number of permutations for prediction
    
    # Model parameters
    NUM_CLASSES = 10  # Number of classes for fine-tuning
    
    # Data split
    TRAIN_VAL_SPLIT = 0.9  # 90% for training, 10% for validation
    
    # Model checkpoint names
    ROTATION_BACKBONE_PATH = os.path.join(CHECKPOINTS_DIR, 'resnet18_backbone_pretrained_rotations.pth')
    JIGSAW_BACKBONE_PATH = os.path.join(CHECKPOINTS_DIR, 'resnet18_backbone_pretrained_jigsaw.pth')
    BEST_MODEL_ROTATION_PATH = os.path.join(CHECKPOINTS_DIR, 'best_finetuned_model_rotations.pth')
    BEST_MODEL_JIGSAW_PATH = os.path.join(CHECKPOINTS_DIR, 'best_finetuned_model_jigsaw.pth')
    BEST_MODEL_PATH = os.path.join(CHECKPOINTS_DIR, 'best_finetuned_model.pth')
    
    # Submission file names
    SUBMISSION_ROTATION_PATH = os.path.join(SUBMISSIONS_DIR, 'submission_rotations.csv')
    SUBMISSION_JIGSAW_PATH = os.path.join(SUBMISSIONS_DIR, 'submission_jigsaw.csv')
    SUBMISSION_PATH = os.path.join(SUBMISSIONS_DIR, 'submission.csv')
    
    # Permutations file
    PERMUTATIONS_PATH = f'permutations_{N_PERMUTATIONS}.npy'


# Create directories if they don't exist
os.makedirs(Config.CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(Config.SUBMISSIONS_DIR, exist_ok=True)