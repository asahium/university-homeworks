"""
Audio augmentation transforms for waveforms and spectrograms
"""
import torch
import torch.nn as nn
import torchaudio.transforms as T
import random

import sys
sys.path.append('.')
from config.config import Config


class WaveformAugmentation(nn.Module):
    """
    Augmentation transforms for raw audio waveforms.
    
    Includes:
    - Time shifting
    - Adding noise
    - Time masking
    """
    def __init__(
        self,
        time_shift_max=Config.TIME_SHIFT_MAX,
        noise_factor=Config.NOISE_FACTOR,
        p_shift=0.5,
        p_noise=0.5
    ):
        super().__init__()
        self.time_shift_max = time_shift_max
        self.noise_factor = noise_factor
        self.p_shift = p_shift
        self.p_noise = p_noise
    
    def forward(self, waveform):
        """
        Args:
            waveform: Audio tensor of shape (1, time) or (time,)
        Returns:
            Augmented waveform
        """
        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0)
        
        # Time shift
        if random.random() < self.p_shift:
            waveform = self._time_shift(waveform)
        
        # Add noise
        if random.random() < self.p_noise:
            waveform = self._add_noise(waveform)
        
        return waveform
    
    def _time_shift(self, waveform):
        """Randomly shift audio in time"""
        shift_amount = int(waveform.shape[-1] * self.time_shift_max * random.uniform(-1, 1))
        return torch.roll(waveform, shifts=shift_amount, dims=-1)
    
    def _add_noise(self, waveform):
        """Add random Gaussian noise"""
        noise = torch.randn_like(waveform) * self.noise_factor
        return waveform + noise


class TimeMasking(nn.Module):
    """Time masking for waveforms"""
    def __init__(self, max_mask_length=1600, num_masks=2, p=0.5):
        super().__init__()
        self.max_mask_length = max_mask_length
        self.num_masks = num_masks
        self.p = p
    
    def forward(self, waveform):
        if random.random() > self.p:
            return waveform
        
        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0)
        
        waveform = waveform.clone()
        length = waveform.shape[-1]
        
        for _ in range(self.num_masks):
            mask_length = random.randint(1, self.max_mask_length)
            start = random.randint(0, max(0, length - mask_length))
            waveform[..., start:start + mask_length] = 0
        
        return waveform


class SpectrogramAugmentation(nn.Module):
    """
    SpecAugment-style augmentation for spectrograms.
    
    Includes:
    - Frequency masking
    - Time masking
    """
    def __init__(
        self,
        freq_mask_param=Config.FREQ_MASK_PARAM,
        time_mask_param=Config.TIME_MASK_PARAM,
        num_freq_masks=Config.NUM_FREQ_MASKS,
        num_time_masks=Config.NUM_TIME_MASKS,
        p=0.5
    ):
        super().__init__()
        self.freq_mask = T.FrequencyMasking(freq_mask_param)
        self.time_mask = T.TimeMasking(time_mask_param)
        self.num_freq_masks = num_freq_masks
        self.num_time_masks = num_time_masks
        self.p = p
    
    def forward(self, spectrogram):
        """
        Args:
            spectrogram: Tensor of shape (1, n_mels, time) or (n_mels, time)
        Returns:
            Augmented spectrogram
        """
        if random.random() > self.p:
            return spectrogram
        
        # Add batch dimension if needed
        squeeze = False
        if spectrogram.dim() == 2:
            spectrogram = spectrogram.unsqueeze(0)
            squeeze = True
        elif spectrogram.dim() == 3 and spectrogram.shape[0] == 1:
            # Already has channel dim, add batch
            spectrogram = spectrogram.unsqueeze(0)
        
        spectrogram = spectrogram.clone()
        
        # Apply frequency masking
        for _ in range(self.num_freq_masks):
            spectrogram = self.freq_mask(spectrogram)
        
        # Apply time masking
        for _ in range(self.num_time_masks):
            spectrogram = self.time_mask(spectrogram)
        
        # Remove added dimensions
        if squeeze:
            spectrogram = spectrogram.squeeze(0)
        else:
            spectrogram = spectrogram.squeeze(0)
        
        return spectrogram


class CombinedWaveformAugmentation(nn.Module):
    """Combined waveform augmentation pipeline"""
    def __init__(self):
        super().__init__()
        self.augmentations = nn.Sequential(
            WaveformAugmentation(p_shift=0.5, p_noise=0.5),
            TimeMasking(max_mask_length=1600, num_masks=2, p=0.5)
        )
    
    def forward(self, waveform):
        return self.augmentations(waveform)


class IdentityTransform(nn.Module):
    """Identity transform (no augmentation)"""
    def forward(self, x):
        return x


def get_augmentation_transforms(aug_waveform=False, aug_spectrogram=False):
    """
    Get augmentation transforms based on configuration.
    
    Args:
        aug_waveform: Whether to augment waveforms
        aug_spectrogram: Whether to augment spectrograms
    
    Returns:
        waveform_transform, spectrogram_transform
    """
    if aug_waveform:
        waveform_transform = CombinedWaveformAugmentation()
    else:
        waveform_transform = IdentityTransform()
    
    if aug_spectrogram:
        spectrogram_transform = SpectrogramAugmentation(p=0.8)
    else:
        spectrogram_transform = IdentityTransform()
    
    return waveform_transform, spectrogram_transform


if __name__ == "__main__":
    # Test augmentations
    waveform = torch.randn(1, 16000)
    spectrogram = torch.randn(1, 64, 100)
    
    wave_aug = CombinedWaveformAugmentation()
    spec_aug = SpectrogramAugmentation()
    
    aug_wave = wave_aug(waveform)
    aug_spec = spec_aug(spectrogram)
    
    print(f"Original waveform shape: {waveform.shape}")
    print(f"Augmented waveform shape: {aug_wave.shape}")
    print(f"Original spectrogram shape: {spectrogram.shape}")
    print(f"Augmented spectrogram shape: {aug_spec.shape}")

