"""
Configuration file for AudioMNIST self-supervised learning experiments
"""
import torch


class Config:
    # General settings
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    SEED = 42
    NUM_WORKERS = 4
    PIN_MEMORY = True
    
    # Data settings
    DATA_ROOT = './AudioMNIST/data'
    CHECKPOINT_DIR = './checkpoints'
    RESULTS_DIR = './results'
    
    # Audio settings
    ORIG_SAMPLE_RATE = 48000
    SAMPLE_RATE = 16000
    MAX_AUDIO_LENGTH = 16000  # 1 second at 16kHz
    N_MELS = 64
    N_FFT = 512
    HOP_LENGTH = 160
    
    # Dataset splits
    NUM_SPEAKERS = 60
    TEST_SPEAKERS_RATIO = 1/3  # 20 speakers for test
    VAL_RATIO = 0.2  # 20% of train speakers for validation
    
    # Model settings
    NUM_CLASSES = 10  # digits 0-9
    EMBEDDING_DIM = 256
    
    # 1D Encoder settings (for raw waveforms)
    ENCODER_1D_CHANNELS = [32, 64, 128, 256]
    ENCODER_1D_KERNEL_SIZE = 15
    ENCODER_1D_STRIDE = 4
    ENCODER_1D_DILATION = 2
    
    # 2D Encoder settings (for spectrograms)
    ENCODER_2D_CHANNELS = [32, 64, 128, 256]
    ENCODER_2D_KERNEL_SIZE = 3
    
    # Supervised training
    SUPERVISED_EPOCHS = 50
    SUPERVISED_BATCH_SIZE = 64
    SUPERVISED_LR = 1e-3
    SUPERVISED_WEIGHT_DECAY = 1e-4
    
    # Contrastive learning settings
    CONTRASTIVE_EPOCHS = 100
    CONTRASTIVE_BATCH_SIZE = 64
    CONTRASTIVE_LR = 1e-3
    CONTRASTIVE_TEMPERATURE = 0.07
    CONTRASTIVE_WEIGHT_DECAY = 1e-4
    
    # Linear probe settings
    LINEAR_PROBE_EPOCHS = 50
    LINEAR_PROBE_LR = 1e-3
    LINEAR_PROBE_BATCH_SIZE = 64
    
    # Fine-tuning settings
    FINETUNE_EPOCHS = 30
    FINETUNE_LR = 1e-4
    FINETUNE_WEIGHT_DECAY = 1e-4
    
    # Voice biometrics (kNN)
    KNN_K_VALUES = [1, 3, 5, 7, 9, 11, 15, 21]
    
    # Augmentation settings
    # Waveform augmentations
    TIME_SHIFT_MAX = 0.1  # max shift as fraction of audio length
    NOISE_FACTOR = 0.005
    
    # Spectrogram augmentations (SpecAugment)
    FREQ_MASK_PARAM = 10
    TIME_MASK_PARAM = 10
    NUM_FREQ_MASKS = 2
    NUM_TIME_MASKS = 2
    
    # Logging
    WANDB_PROJECT = None
    WANDB_ENTITY = None

