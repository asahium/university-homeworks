"""
Evaluation utilities
"""
import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm
from config.config import Config


def strip_prefix_from_state_dict(state_dict, prefix='_orig_mod.'):
    """
    Strip prefix from state dict keys (e.g., '_orig_mod.' added by torch.compile or 'model.' from wrapper)
    
    Args:
        state_dict: State dictionary to process
        prefix: Prefix to remove (default: '_orig_mod.'). Can also be a list of prefixes.
    
    Returns:
        new_state_dict: State dictionary with prefix removed
    """
    if isinstance(prefix, str):
        prefixes = [prefix]
    else:
        prefixes = prefix
    
    new_state_dict = {}
    for key, value in state_dict.items():
        new_key = key
        changed = True
        while changed:
            changed = False
            for p in prefixes:
                if new_key.startswith(p):
                    new_key = new_key[len(p):]
                    changed = True
                    break
        new_state_dict[new_key] = value
    return new_state_dict


def extract_embeddings(model, loader, device, is_ssl=False):
    """
    Extract embeddings from a model
    
    Args:
        model: The model to extract embeddings from
        loader: DataLoader
        device: torch device
        is_ssl: Whether the model is a self-supervised learning model
    
    Returns:
        embeddings: numpy array of shape (N, D)
        labels: numpy array of shape (N,)
    """
    model.eval()
    embeddings = []
    labels = []
    
    with torch.no_grad():
        for images, targets in tqdm(loader, desc="Extracting embeddings", leave=False):
            images = images.to(device)
            
            if is_ssl:
                if hasattr(model, 'online_encoder'):
                    # BYOL
                    h = model.online_encoder(images)
                elif hasattr(model, 'encoder'):
                    # SimCLR
                    h = model.encoder(images)
                elif hasattr(model, 'encoder_q'):
                    # MoCo
                    h = model.encoder_q(images)
                else:
                    h = model(images)
            else:
                original_fc = model.fc
                model.fc = nn.Identity()
                h = model(images)
                model.fc = original_fc
            
            embeddings.append(h.cpu().numpy())
            labels.append(targets.numpy())
    
    embeddings = np.concatenate(embeddings, axis=0)
    labels = np.concatenate(labels, axis=0)
    
    return embeddings, labels


def evaluate_model(model, loader, criterion, device):
    """
    Evaluate a classification model
    
    Args:
        model: The model to evaluate
        loader: DataLoader
        criterion: Loss function
        device: torch device
    
    Returns:
        loss: Average loss
        accuracy: Accuracy in percentage
    """
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Evaluating", leave=False):
            images, labels = images.to(device), labels.to(device)
            
            # Mark step begin for CUDA graphs compatibility with torch.compile
            torch.compiler.cudagraph_mark_step_begin()
            
            with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
                outputs = model(images)
                loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(loader), 100. * correct / total


def evaluate_ood(model, loader, device):
    """
    Evaluate model on out-of-distribution data
    
    Args:
        model: The model to evaluate
        loader: DataLoader
        device: torch device
    
    Returns:
        accuracy: Accuracy in percentage
    """
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Evaluating OOD", leave=False):
            images, labels = images.to(device), labels.to(device)
            
            torch.compiler.cudagraph_mark_step_begin()
            
            with torch.amp.autocast('cuda', enabled=(device.type == 'cuda')):
                outputs = model(images)
            
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return 100. * correct / total

