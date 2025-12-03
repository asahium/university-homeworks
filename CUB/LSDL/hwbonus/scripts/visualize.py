"""
t-SNE visualization of embeddings for all models
"""
import sys
sys.path.append('.')

import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from config.config import Config
from datasets import get_dataloaders, get_contrastive_dataloaders, get_speaker_splits, AudioMNISTDataset, AudioMNISTSpectrogramDataset
from models import SupervisedModel1D, SupervisedModel2D, MultiFormatContrastiveModel
from utils import extract_embeddings, extract_contrastive_embeddings, compute_tsne, plot_tsne, strip_prefix_from_state_dict


def get_test_dataloaders():
    """Get test data loaders for visualization"""
    train_speakers, val_speakers, test_speakers = get_speaker_splits()
    
    # Waveform dataset
    test_waveform = AudioMNISTDataset(
        Config.DATA_ROOT, test_speakers, return_both=False
    )
    
    # Spectrogram dataset
    test_spectrogram = AudioMNISTSpectrogramDataset(
        Config.DATA_ROOT, test_speakers
    )
    
    # Combined dataset
    test_combined = AudioMNISTDataset(
        Config.DATA_ROOT, test_speakers, return_both=True
    )
    
    from torch.utils.data import DataLoader
    
    loader_wave = DataLoader(
        test_waveform, batch_size=64, shuffle=False,
        num_workers=Config.NUM_WORKERS, pin_memory=Config.PIN_MEMORY
    )
    
    loader_spec = DataLoader(
        test_spectrogram, batch_size=64, shuffle=False,
        num_workers=Config.NUM_WORKERS, pin_memory=Config.PIN_MEMORY
    )
    
    loader_combined = DataLoader(
        test_combined, batch_size=64, shuffle=False,
        num_workers=Config.NUM_WORKERS, pin_memory=Config.PIN_MEMORY
    )
    
    return loader_wave, loader_spec, loader_combined


def visualize_supervised_models():
    """Visualize embeddings from supervised models"""
    device = Config.DEVICE
    loader_wave, loader_spec, _ = get_test_dataloaders()
    
    # Load supervised 1D model
    model_1d = SupervisedModel1D().to(device)
    ckpt_path_1d = os.path.join(Config.CHECKPOINT_DIR, 'supervised_1d_best.pth')
    if os.path.exists(ckpt_path_1d):
        model_1d.load_state_dict(torch.load(ckpt_path_1d, map_location=device))
        print("Loaded supervised 1D model")
    else:
        print(f"Warning: {ckpt_path_1d} not found")
        return None, None
    
    # Load supervised 2D model
    model_2d = SupervisedModel2D().to(device)
    ckpt_path_2d = os.path.join(Config.CHECKPOINT_DIR, 'supervised_2d_best.pth')
    if os.path.exists(ckpt_path_2d):
        model_2d.load_state_dict(torch.load(ckpt_path_2d, map_location=device))
        print("Loaded supervised 2D model")
    else:
        print(f"Warning: {ckpt_path_2d} not found")
        return None, None
    
    # Extract embeddings
    print("Extracting embeddings from supervised 1D model...")
    emb_1d, labels_1d, speakers_1d = extract_embeddings(model_1d, loader_wave, device, model_type='1d')
    
    print("Extracting embeddings from supervised 2D model...")
    emb_2d, labels_2d, speakers_2d = extract_embeddings(model_2d, loader_spec, device, model_type='2d')
    
    return {
        'supervised_1d': (emb_1d, labels_1d, speakers_1d),
        'supervised_2d': (emb_2d, labels_2d, speakers_2d)
    }


def visualize_contrastive_model(model_name):
    """Visualize embeddings from a contrastive model"""
    device = Config.DEVICE
    _, _, loader_combined = get_test_dataloaders()
    
    # Load model
    model = MultiFormatContrastiveModel().to(device)
    ckpt_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_best.pth')
    
    if os.path.exists(ckpt_path):
        state_dict = torch.load(ckpt_path, map_location=device)
        state_dict = strip_prefix_from_state_dict(state_dict)
        model.load_state_dict(state_dict)
        print(f"Loaded {model_name}")
    else:
        print(f"Warning: {ckpt_path} not found")
        return None
    
    # Extract embeddings for both encoders
    print(f"Extracting embeddings from {model_name}...")
    
    emb_1d, labels, speakers = extract_contrastive_embeddings(
        model, loader_combined, device, return_mode='1d'
    )
    emb_2d, _, _ = extract_contrastive_embeddings(
        model, loader_combined, device, return_mode='2d'
    )
    
    return {
        f'{model_name}_1d': (emb_1d, labels, speakers),
        f'{model_name}_2d': (emb_2d, labels, speakers)
    }


def create_tsne_plots(all_embeddings, save_dir=None):
    """
    Create t-SNE plots for all models.
    
    Args:
        all_embeddings: Dict mapping model_name to (embeddings, labels, speakers)
        save_dir: Directory to save plots
    """
    if save_dir is None:
        save_dir = os.path.join(Config.RESULTS_DIR, 'tsne_plots')
    os.makedirs(save_dir, exist_ok=True)
    
    # Custom colormap for speakers (need many colors)
    n_speakers = 60
    speaker_cmap = plt.cm.get_cmap('hsv', n_speakers)
    
    # Custom colormap for digits (10 classes)
    digit_cmap = plt.cm.get_cmap('tab10', 10)
    
    for model_name, (embeddings, labels, speakers) in all_embeddings.items():
        print(f"\nComputing t-SNE for {model_name}...")
        tsne_emb = compute_tsne(embeddings)
        
        # Plot colored by digit
        fig, ax = plt.subplots(figsize=(10, 8))
        for digit in range(10):
            mask = labels == digit
            ax.scatter(
                tsne_emb[mask, 0], tsne_emb[mask, 1],
                c=[digit_cmap(digit)], label=str(digit),
                alpha=0.6, s=20
            )
        ax.set_title(f'{model_name} - Colored by Digit')
        ax.set_xlabel('t-SNE 1')
        ax.set_ylabel('t-SNE 2')
        ax.legend(title='Digit', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'{model_name}_by_digit.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Plot colored by speaker
        fig, ax = plt.subplots(figsize=(12, 10))
        unique_speakers = np.unique(speakers)
        for i, speaker in enumerate(unique_speakers):
            mask = speakers == speaker
            ax.scatter(
                tsne_emb[mask, 0], tsne_emb[mask, 1],
                c=[speaker_cmap(i % n_speakers)],
                alpha=0.5, s=15
            )
        ax.set_title(f'{model_name} - Colored by Speaker')
        ax.set_xlabel('t-SNE 1')
        ax.set_ylabel('t-SNE 2')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'{model_name}_by_speaker.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    print(f"\nPlots saved to {save_dir}")


def main():
    """Generate t-SNE visualizations for all models"""
    print(f"Device: {Config.DEVICE}")
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    all_embeddings = {}
    
    # Supervised models
    print("\n" + "="*60)
    print("Visualizing Supervised Models")
    print("="*60)
    
    supervised_emb = visualize_supervised_models()
    if supervised_emb:
        all_embeddings.update(supervised_emb)
    
    # Contrastive models
    print("\n" + "="*60)
    print("Visualizing Contrastive Models")
    print("="*60)
    
    contrastive_models = [
        'contrastive_no_aug',
        'contrastive_wav_aug',
        'contrastive_spec_aug',
        'contrastive_wav_aug_spec_aug'
    ]
    
    for model_name in contrastive_models:
        emb = visualize_contrastive_model(model_name)
        if emb:
            all_embeddings.update(emb)
    
    # Create plots
    if all_embeddings:
        print("\n" + "="*60)
        print("Creating t-SNE Plots")
        print("="*60)
        create_tsne_plots(all_embeddings)
    else:
        print("No embeddings to visualize. Train models first.")


if __name__ == "__main__":
    main()

