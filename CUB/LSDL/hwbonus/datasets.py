"""
AudioMNIST dataset loading and speaker-based splits
"""
import os
import torch
import torchaudio
import torchaudio.transforms as T

# Use soundfile backend to avoid FFmpeg dependency issues
torchaudio.set_audio_backend("soundfile")
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from collections import defaultdict

from config.config import Config


class LogMelSpectrogram(T.MelSpectrogram):
    """Log mel spectrogram transform"""
    def __init__(self, eps=1e-8, **kwargs):
        super().__init__(**kwargs)
        self.eps = eps

    def forward(self, waveform):
        return (super().forward(waveform) + self.eps).log()


class AudioMNISTDataset(Dataset):
    """
    AudioMNIST dataset for digit classification
    
    Args:
        root: Path to AudioMNIST/data directory
        speaker_ids: List of speaker IDs to include
        sample_indices: Optional list of sample indices to include
        transform_waveform: Optional transform for waveforms
        transform_spectrogram: Optional transform for spectrograms
        return_both: If True, return both waveform and spectrogram
        normalize_spec: If True, normalize spectrogram to zero mean and unit variance
    """
    def __init__(
        self,
        root,
        speaker_ids,
        sample_indices=None,
        transform_waveform=None,
        transform_spectrogram=None,
        return_both=False,
        normalize_spec=True
    ):
        self.root = root
        self.speaker_ids = speaker_ids
        self.transform_waveform = transform_waveform
        self.transform_spectrogram = transform_spectrogram
        self.return_both = return_both
        self.normalize_spec = normalize_spec
        
        # Audio processing
        self.resample = T.Resample(
            orig_freq=Config.ORIG_SAMPLE_RATE,
            new_freq=Config.SAMPLE_RATE
        )
        self.mel_spectrogram = LogMelSpectrogram(
            sample_rate=Config.SAMPLE_RATE,
            n_mels=Config.N_MELS,
            n_fft=Config.N_FFT,
            hop_length=Config.HOP_LENGTH
        )
        
        # Build sample list
        self.samples = []
        for speaker_id in speaker_ids:
            speaker_dir = os.path.join(root, speaker_id)
            if not os.path.isdir(speaker_dir):
                continue
            for audio_file in os.listdir(speaker_dir):
                if audio_file.endswith('.wav'):
                    digit = int(audio_file[0])
                    self.samples.append({
                        'path': os.path.join(speaker_dir, audio_file),
                        'digit': digit,
                        'speaker': int(speaker_id)
                    })
        
        # Filter by sample indices if provided
        if sample_indices is not None:
            self.samples = [self.samples[i] for i in sample_indices]
    
    def __len__(self):
        return len(self.samples)
    
    def _pad_or_truncate(self, waveform, target_length):
        """Pad or truncate waveform to target length"""
        if waveform.shape[1] > target_length:
            waveform = waveform[:, :target_length]
        elif waveform.shape[1] < target_length:
            padding = target_length - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding))
        return waveform
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # Load audio
        waveform, sample_rate = torchaudio.load(sample['path'])
        
        # Resample to target sample rate
        if sample_rate != Config.SAMPLE_RATE:
            waveform = self.resample(waveform)
        
        # Pad or truncate to fixed length
        waveform = self._pad_or_truncate(waveform, Config.MAX_AUDIO_LENGTH)
        
        # Get label
        digit = sample['digit']
        speaker = sample['speaker']
        
        if self.return_both:
            # Return both waveform and spectrogram
            waveform_out = waveform.clone()
            if self.transform_waveform:
                waveform_out = self.transform_waveform(waveform_out)
            
            # Compute spectrogram
            spectrogram = self.mel_spectrogram(waveform.squeeze(0))
            if self.normalize_spec:
                spectrogram = (spectrogram - spectrogram.mean()) / (spectrogram.std() + 1e-8)
            spectrogram = spectrogram.unsqueeze(0)  # Add channel dimension
            
            if self.transform_spectrogram:
                spectrogram = self.transform_spectrogram(spectrogram)
            
            return waveform_out, spectrogram, digit, speaker
        else:
            # Return only waveform (spectrogram can be computed if needed)
            if self.transform_waveform:
                waveform = self.transform_waveform(waveform)
            
            return waveform, digit, speaker


class AudioMNISTSpectrogramDataset(Dataset):
    """
    AudioMNIST dataset returning only spectrograms
    """
    def __init__(
        self,
        root,
        speaker_ids,
        sample_indices=None,
        transform=None,
        normalize=True
    ):
        self.root = root
        self.speaker_ids = speaker_ids
        self.transform = transform
        self.normalize = normalize
        
        # Audio processing
        self.resample = T.Resample(
            orig_freq=Config.ORIG_SAMPLE_RATE,
            new_freq=Config.SAMPLE_RATE
        )
        self.mel_spectrogram = LogMelSpectrogram(
            sample_rate=Config.SAMPLE_RATE,
            n_mels=Config.N_MELS,
            n_fft=Config.N_FFT,
            hop_length=Config.HOP_LENGTH
        )
        
        # Build sample list
        self.samples = []
        for speaker_id in speaker_ids:
            speaker_dir = os.path.join(root, speaker_id)
            if not os.path.isdir(speaker_dir):
                continue
            for audio_file in os.listdir(speaker_dir):
                if audio_file.endswith('.wav'):
                    digit = int(audio_file[0])
                    self.samples.append({
                        'path': os.path.join(speaker_dir, audio_file),
                        'digit': digit,
                        'speaker': int(speaker_id)
                    })
        
        if sample_indices is not None:
            self.samples = [self.samples[i] for i in sample_indices]
    
    def __len__(self):
        return len(self.samples)
    
    def _pad_or_truncate(self, waveform, target_length):
        if waveform.shape[1] > target_length:
            waveform = waveform[:, :target_length]
        elif waveform.shape[1] < target_length:
            padding = target_length - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding))
        return waveform
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # Load and process audio
        waveform, sample_rate = torchaudio.load(sample['path'])
        if sample_rate != Config.SAMPLE_RATE:
            waveform = self.resample(waveform)
        waveform = self._pad_or_truncate(waveform, Config.MAX_AUDIO_LENGTH)
        
        # Compute spectrogram
        spectrogram = self.mel_spectrogram(waveform.squeeze(0))
        if self.normalize:
            spectrogram = (spectrogram - spectrogram.mean()) / (spectrogram.std() + 1e-8)
        spectrogram = spectrogram.unsqueeze(0)  # Add channel dimension
        
        if self.transform:
            spectrogram = self.transform(spectrogram)
        
        return spectrogram, sample['digit'], sample['speaker']


def get_speaker_splits(root=Config.DATA_ROOT, seed=Config.SEED):
    """
    Split speakers into train, validation, and test sets.
    
    Returns:
        train_speakers: List of speaker IDs for training
        val_speakers: List of speaker IDs for validation  
        test_speakers: List of speaker IDs for testing
    """
    np.random.seed(seed)
    
    # Get all speaker IDs
    all_speakers = sorted([d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))])
    
    # Split: 1/3 test, 2/3 train+val
    num_test = len(all_speakers) // 3
    test_speakers = all_speakers[:num_test]
    train_val_speakers = all_speakers[num_test:]
    
    # Split train_val into train and val (80:20)
    num_val = int(len(train_val_speakers) * Config.VAL_RATIO)
    np.random.shuffle(train_val_speakers)
    val_speakers = train_val_speakers[:num_val]
    train_speakers = train_val_speakers[num_val:]
    
    return train_speakers, val_speakers, test_speakers


def get_stratified_split_indices(dataset, test_size=0.5, seed=Config.SEED):
    """
    Get stratified split indices for a dataset, stratifying by both speaker and digit.
    
    Args:
        dataset: AudioMNIST dataset
        test_size: Fraction for test split
        seed: Random seed
        
    Returns:
        train_indices, test_indices
    """
    # Create stratification key combining speaker and digit
    strat_keys = [f"{s['speaker']}_{s['digit']}" for s in dataset.samples]
    indices = list(range(len(dataset)))
    
    train_idx, test_idx = train_test_split(
        indices,
        test_size=test_size,
        stratify=strat_keys,
        random_state=seed
    )
    
    return train_idx, test_idx


def get_train_val_split_indices(dataset, val_size=0.2, seed=Config.SEED):
    """
    Get stratified train/val split indices, stratifying by both speaker and digit.
    
    Args:
        dataset: AudioMNIST dataset
        val_size: Fraction for validation split
        seed: Random seed
        
    Returns:
        train_indices, val_indices
    """
    # Create stratification key combining speaker and digit
    strat_keys = [f"{s['speaker']}_{s['digit']}" for s in dataset.samples]
    indices = list(range(len(dataset)))
    
    train_idx, val_idx = train_test_split(
        indices,
        test_size=val_size,
        stratify=strat_keys,
        random_state=seed
    )
    
    return train_idx, val_idx


def get_dataloaders(
    root=Config.DATA_ROOT,
    batch_size=Config.SUPERVISED_BATCH_SIZE,
    return_both=False,
    transform_waveform=None,
    transform_spectrogram=None,
    use_spectrogram_only=False
):
    """
    Get train, validation, and test dataloaders.
    
    Args:
        root: Path to data
        batch_size: Batch size
        return_both: If True, return both waveform and spectrogram
        transform_waveform: Transform for waveforms
        transform_spectrogram: Transform for spectrograms
        use_spectrogram_only: If True, use spectrogram-only dataset
        
    Returns:
        train_loader, val_loader, test_loader
    """
    train_speakers, val_speakers, test_speakers = get_speaker_splits(root)
    
    if use_spectrogram_only:
        DatasetClass = AudioMNISTSpectrogramDataset
        train_dataset = DatasetClass(root, train_speakers, transform=transform_spectrogram)
        val_dataset = DatasetClass(root, val_speakers, transform=None)
        test_dataset = DatasetClass(root, test_speakers, transform=None)
    else:
        train_dataset = AudioMNISTDataset(
            root, train_speakers,
            transform_waveform=transform_waveform,
            transform_spectrogram=transform_spectrogram,
            return_both=return_both
        )
        val_dataset = AudioMNISTDataset(
            root, val_speakers,
            return_both=return_both
        )
        test_dataset = AudioMNISTDataset(
            root, test_speakers,
            return_both=return_both
        )
    
    # For train/val, we need stratified split within the speakers
    train_indices, val_indices_within_train = get_train_val_split_indices(train_dataset)
    
    # Create subset datasets
    train_subset = torch.utils.data.Subset(train_dataset, train_indices)
    
    train_loader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=Config.NUM_WORKERS,
        pin_memory=Config.PIN_MEMORY,
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=Config.NUM_WORKERS,
        pin_memory=Config.PIN_MEMORY
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=Config.NUM_WORKERS,
        pin_memory=Config.PIN_MEMORY
    )
    
    return train_loader, val_loader, test_loader


def get_contrastive_dataloaders(
    root=Config.DATA_ROOT,
    batch_size=Config.CONTRASTIVE_BATCH_SIZE,
    transform_waveform=None,
    transform_spectrogram=None
):
    """
    Get dataloaders for contrastive learning (returns both waveform and spectrogram).
    """
    return get_dataloaders(
        root=root,
        batch_size=batch_size,
        return_both=True,
        transform_waveform=transform_waveform,
        transform_spectrogram=transform_spectrogram
    )

