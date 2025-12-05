"""
Evaluation utilities for AudioMNIST experiments
"""
import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm
from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

import sys
sys.path.append('.')
from config.config import Config


def evaluate_model(model, loader, criterion, device, return_both=False):
    """
    Evaluate a classification model.
    
    Args:
        model: Model to evaluate
        loader: DataLoader
        criterion: Loss function
        device: Device to use
        return_both: If True, expects loader to return (waveform, spectrogram, label, speaker)
    
    Returns:
        loss: Average loss
        accuracy: Accuracy percentage
    """
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating", leave=False):
            if return_both:
                waveform, spectrogram, labels, speakers = batch
                waveform = waveform.to(device)
                spectrogram = spectrogram.to(device)
                labels = labels.to(device)
                outputs = model(waveform, spectrogram)
            else:
                if len(batch) == 3:
                    inputs, labels, speakers = batch
                else:
                    inputs, labels = batch
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
            
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(loader), 100. * correct / total


def extract_embeddings(model, loader, device, model_type='1d'):
    """
    Extract embeddings from a model.
    
    Args:
        model: Model with get_embeddings method or encoder
        loader: DataLoader
        device: Device to use
        model_type: '1d', '2d', or 'both'
    
    Returns:
        embeddings: numpy array of shape (N, D)
        labels: numpy array of digit labels
        speakers: numpy array of speaker IDs
    """
    model.eval()
    all_embeddings = []
    all_labels = []
    all_speakers = []
    
    with torch.no_grad():
        for batch in tqdm(loader, desc="Extracting embeddings", leave=False):
            if model_type == 'both':
                waveform, spectrogram, labels, speakers = batch
                waveform = waveform.to(device)
                spectrogram = spectrogram.to(device)
                
                if hasattr(model, 'get_embeddings'):
                    h1, h2 = model.get_embeddings(waveform, spectrogram)
                    embeddings = torch.cat([h1, h2], dim=1)
                else:
                    h1 = model.encoder_1d(waveform)
                    h2 = model.encoder_2d(spectrogram)
                    embeddings = torch.cat([h1, h2], dim=1)
            else:
                if len(batch) == 4:
                    waveform, spectrogram, labels, speakers = batch
                    if model_type == '1d':
                        inputs = waveform
                    else:
                        inputs = spectrogram
                elif len(batch) == 3:
                    inputs, labels, speakers = batch
                else:
                    inputs, labels = batch
                    speakers = torch.zeros_like(labels)
                
                inputs = inputs.to(device)
                
                if hasattr(model, 'get_embeddings'):
                    embeddings = model.get_embeddings(inputs)
                elif hasattr(model, 'encoder'):
                    embeddings = model.encoder(inputs)
                else:
                    embeddings = model(inputs)
            
            all_embeddings.append(embeddings.cpu().numpy())
            all_labels.append(labels.numpy() if isinstance(labels, torch.Tensor) else np.array(labels))
            all_speakers.append(speakers.numpy() if isinstance(speakers, torch.Tensor) else np.array(speakers))
    
    embeddings = np.concatenate(all_embeddings, axis=0)
    labels = np.concatenate(all_labels, axis=0)
    speakers = np.concatenate(all_speakers, axis=0)
    
    return embeddings, labels, speakers


def extract_contrastive_embeddings(model, loader, device, return_mode='1d'):
    """
    Extract embeddings from contrastive model.
    
    Args:
        model: MultiFormatContrastiveModel
        loader: DataLoader that returns (waveform, spectrogram, label, speaker)
        device: Device
        return_mode: '1d', '2d', or 'concat'
    
    Returns:
        embeddings, labels, speakers
    """
    model.eval()
    all_embeddings = []
    all_labels = []
    all_speakers = []
    
    with torch.no_grad():
        for waveform, spectrogram, labels, speakers in tqdm(loader, desc="Extracting", leave=False):
            waveform = waveform.to(device)
            spectrogram = spectrogram.to(device)
            
            h1, h2 = model.get_embeddings(waveform, spectrogram)
            
            if return_mode == '1d':
                embeddings = h1
            elif return_mode == '2d':
                embeddings = h2
            else:  # concat
                embeddings = torch.cat([h1, h2], dim=1)
            
            all_embeddings.append(embeddings.cpu().numpy())
            all_labels.append(labels.numpy())
            all_speakers.append(speakers.numpy())
    
    return (
        np.concatenate(all_embeddings, axis=0),
        np.concatenate(all_labels, axis=0),
        np.concatenate(all_speakers, axis=0)
    )


def compute_tsne(embeddings, perplexity=30, max_iter=1000, seed=Config.SEED):
    """
    Compute t-SNE embedding.
    
    Args:
        embeddings: numpy array of shape (N, D)
        perplexity: t-SNE perplexity
        max_iter: Number of iterations
        seed: Random seed
    
    Returns:
        tsne_embeddings: numpy array of shape (N, 2)
    """
    tsne = TSNE(n_components=2, perplexity=perplexity, max_iter=max_iter, random_state=seed)
    return tsne.fit_transform(embeddings)


def plot_tsne(tsne_embeddings, labels, title, save_path=None, figsize=(10, 8)):
    """
    Plot t-SNE visualization.
    
    Args:
        tsne_embeddings: 2D embeddings from t-SNE
        labels: Labels for coloring
        title: Plot title
        save_path: Path to save figure
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    unique_labels = np.unique(labels)
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))
    
    for i, label in enumerate(unique_labels):
        mask = labels == label
        plt.scatter(
            tsne_embeddings[mask, 0],
            tsne_embeddings[mask, 1],
            c=[colors[i]],
            label=str(label),
            alpha=0.6,
            s=20
        )
    
    plt.title(title)
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    
    # Only show legend if not too many labels
    if len(unique_labels) <= 20:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', markerscale=2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.close()


def knn_cross_validate(embeddings, labels, k_values=Config.KNN_K_VALUES, cv=5):
    """
    Cross-validate kNN classifier to find optimal k.
    
    Args:
        embeddings: Feature embeddings
        labels: Labels
        k_values: List of k values to try
        cv: Number of cross-validation folds
    
    Returns:
        best_k: Optimal k value
        best_score: Best cross-validation score
        all_scores: Dict mapping k to scores
    """
    all_scores = {}
    
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, embeddings, labels, cv=cv)
        all_scores[k] = scores.mean()
    
    best_k = max(all_scores, key=all_scores.get)
    best_score = all_scores[best_k]
    
    return best_k, best_score, all_scores


def evaluate_knn(train_embeddings, train_labels, test_embeddings, test_labels, k):
    """
    Evaluate kNN classifier.
    
    Args:
        train_embeddings: Training embeddings
        train_labels: Training labels
        test_embeddings: Test embeddings
        test_labels: Test labels
        k: Number of neighbors
    
    Returns:
        accuracy: Classification accuracy
    """
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(train_embeddings, train_labels)
    predictions = knn.predict(test_embeddings)
    accuracy = (predictions == test_labels).mean() * 100
    return accuracy


def strip_prefix_from_state_dict(state_dict, prefix='_orig_mod.'):
    """
    Strip prefix from state dict keys.
    
    Args:
        state_dict: State dictionary
        prefix: Prefix to remove (str or list of str)
    
    Returns:
        Cleaned state dictionary
    """
    if isinstance(prefix, str):
        prefixes = [prefix]
    else:
        prefixes = prefix
    
    new_state_dict = {}
    for key, value in state_dict.items():
        new_key = key
        for p in prefixes:
            if new_key.startswith(p):
                new_key = new_key[len(p):]
        new_state_dict[new_key] = value
    
    return new_state_dict

