"""
Voice biometrics evaluation using kNN on test speakers
"""
import sys
sys.path.append('.')

import os
import json
import torch
import numpy as np
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split

from config.config import Config
from datasets import get_speaker_splits, AudioMNISTDataset, AudioMNISTSpectrogramDataset
from models import SupervisedModel1D, SupervisedModel2D, MultiFormatContrastiveModel
from utils import knn_cross_validate, evaluate_knn, strip_prefix_from_state_dict


def get_test_speaker_data():
    """Get data for test speakers only"""
    _, _, test_speakers = get_speaker_splits()
    
    # Create datasets for test speakers
    test_waveform = AudioMNISTDataset(
        Config.DATA_ROOT, test_speakers, return_both=False
    )
    
    test_spectrogram = AudioMNISTSpectrogramDataset(
        Config.DATA_ROOT, test_speakers
    )
    
    test_combined = AudioMNISTDataset(
        Config.DATA_ROOT, test_speakers, return_both=True
    )
    
    return test_waveform, test_spectrogram, test_combined


def stratified_split_test_data(dataset):
    """
    Split test data into two equal subsets, stratified by speaker and digit.
    
    Args:
        dataset: AudioMNIST dataset for test speakers
    
    Returns:
        train_indices, test_indices for kNN evaluation
    """
    # Create stratification key
    strat_keys = [f"{s['speaker']}_{s['digit']}" for s in dataset.samples]
    indices = list(range(len(dataset)))
    
    train_idx, test_idx = train_test_split(
        indices,
        test_size=0.5,
        stratify=strat_keys,
        random_state=Config.SEED
    )
    
    return train_idx, test_idx


def extract_embeddings_for_knn(model, loader, device, model_type='1d'):
    """Extract embeddings for kNN evaluation"""
    model.eval()
    all_embeddings = []
    all_speakers = []
    all_digits = []
    
    with torch.no_grad():
        for batch in loader:
            if model_type in ['1d', '2d']:
                if len(batch) == 3:
                    inputs, digits, speakers = batch
                else:
                    inputs, digits = batch
                    speakers = torch.zeros_like(digits)
                
                inputs = inputs.to(device)
                
                # Handle contrastive models (have encoder_1d and encoder_2d)
                if hasattr(model, 'encoder_1d') and hasattr(model, 'encoder_2d'):
                    if model_type == '1d':
                        embeddings = model.encoder_1d(inputs)
                    else:
                        embeddings = model.encoder_2d(inputs)
                # Handle supervised models
                elif hasattr(model, 'encoder'):
                    embeddings = model.encoder(inputs)
                elif hasattr(model, 'get_embeddings'):
                    embeddings = model.get_embeddings(inputs)
                else:
                    embeddings = model(inputs)
            else:  # combined for contrastive
                waveform, spectrogram, digits, speakers = batch
                waveform = waveform.to(device)
                spectrogram = spectrogram.to(device)
                
                h1, h2 = model.get_embeddings(waveform, spectrogram)
                embeddings = torch.cat([h1, h2], dim=1)
            
            all_embeddings.append(embeddings.cpu().numpy())
            all_speakers.append(speakers.numpy() if isinstance(speakers, torch.Tensor) else np.array(speakers))
            all_digits.append(digits.numpy() if isinstance(digits, torch.Tensor) else np.array(digits))
    
    embeddings = np.concatenate(all_embeddings, axis=0)
    speakers = np.concatenate(all_speakers, axis=0)
    digits = np.concatenate(all_digits, axis=0)
    
    return embeddings, speakers, digits


def evaluate_voice_biometrics(model, test_dataset, device, model_type='1d'):
    """
    Evaluate voice biometrics using kNN.
    
    Args:
        model: Trained model
        test_dataset: Dataset for test speakers
        device: Device
        model_type: '1d', '2d', or 'combined'
    
    Returns:
        Dict with results
    """
    # Split test data
    train_idx, test_idx = stratified_split_test_data(test_dataset)
    
    # Create subsets
    train_subset = Subset(test_dataset, train_idx)
    test_subset = Subset(test_dataset, test_idx)
    
    train_loader = DataLoader(
        train_subset, batch_size=64, shuffle=False,
        num_workers=Config.NUM_WORKERS
    )
    test_loader = DataLoader(
        test_subset, batch_size=64, shuffle=False,
        num_workers=Config.NUM_WORKERS
    )
    
    # Extract embeddings
    train_emb, train_speakers, train_digits = extract_embeddings_for_knn(
        model, train_loader, device, model_type
    )
    test_emb, test_speakers, test_digits = extract_embeddings_for_knn(
        model, test_loader, device, model_type
    )
    
    # Cross-validate to find optimal k
    print("  Cross-validating k...")
    best_k, best_cv_score, all_cv_scores = knn_cross_validate(
        train_emb, train_speakers, k_values=Config.KNN_K_VALUES
    )
    
    print(f"  Best k: {best_k}, CV Score: {best_cv_score*100:.2f}%")
    
    # Evaluate on test set
    test_acc = evaluate_knn(train_emb, train_speakers, test_emb, test_speakers, best_k)
    
    return {
        'best_k': best_k,
        'cv_score': best_cv_score * 100,
        'test_accuracy': test_acc,
        'all_cv_scores': {k: v * 100 for k, v in all_cv_scores.items()}
    }


def evaluate_all_models():
    """Evaluate voice biometrics for all models"""
    device = Config.DEVICE
    results = {}
    
    # Get test data
    test_waveform, test_spectrogram, test_combined = get_test_speaker_data()
    
    # Evaluate supervised 1D model
    print("\n" + "="*60)
    print("Evaluating Supervised 1D Model")
    print("="*60)
    
    model_1d = SupervisedModel1D().to(device)
    ckpt_path = os.path.join(Config.CHECKPOINT_DIR, 'supervised_1d_best.pth')
    if os.path.exists(ckpt_path):
        model_1d.load_state_dict(torch.load(ckpt_path, map_location=device))
        results['supervised_1d'] = evaluate_voice_biometrics(
            model_1d, test_waveform, device, '1d'
        )
        print(f"  Test Accuracy: {results['supervised_1d']['test_accuracy']:.2f}%")
    else:
        print(f"  Checkpoint not found: {ckpt_path}")
    
    # Evaluate supervised 2D model
    print("\n" + "="*60)
    print("Evaluating Supervised 2D Model")
    print("="*60)
    
    model_2d = SupervisedModel2D().to(device)
    ckpt_path = os.path.join(Config.CHECKPOINT_DIR, 'supervised_2d_best.pth')
    if os.path.exists(ckpt_path):
        model_2d.load_state_dict(torch.load(ckpt_path, map_location=device))
        results['supervised_2d'] = evaluate_voice_biometrics(
            model_2d, test_spectrogram, device, '2d'
        )
        print(f"  Test Accuracy: {results['supervised_2d']['test_accuracy']:.2f}%")
    else:
        print(f"  Checkpoint not found: {ckpt_path}")
    
    # Evaluate contrastive models
    contrastive_models = [
        'contrastive_no_aug',
        'contrastive_wav_aug',
        'contrastive_spec_aug',
        'contrastive_wav_aug_spec_aug'
    ]
    
    for model_name in contrastive_models:
        print(f"\n{'='*60}")
        print(f"Evaluating {model_name}")
        print("="*60)
        
        model = MultiFormatContrastiveModel().to(device)
        ckpt_path = os.path.join(Config.CHECKPOINT_DIR, f'{model_name}_best.pth')
        
        if os.path.exists(ckpt_path):
            state_dict = torch.load(ckpt_path, map_location=device)
            state_dict = strip_prefix_from_state_dict(state_dict)
            model.load_state_dict(state_dict)
            
            # Evaluate using 1D encoder
            print("  1D Encoder:")
            results[f'{model_name}_1d'] = evaluate_voice_biometrics(
                model, test_waveform, device, '1d'
            )
            print(f"    Test Accuracy: {results[f'{model_name}_1d']['test_accuracy']:.2f}%")
            
            # Evaluate using 2D encoder
            print("  2D Encoder:")
            results[f'{model_name}_2d'] = evaluate_voice_biometrics(
                model, test_spectrogram, device, '2d'
            )
            print(f"    Test Accuracy: {results[f'{model_name}_2d']['test_accuracy']:.2f}%")
            
            # Evaluate using concatenated embeddings
            print("  Concatenated:")
            results[f'{model_name}_concat'] = evaluate_voice_biometrics(
                model, test_combined, device, 'combined'
            )
            print(f"    Test Accuracy: {results[f'{model_name}_concat']['test_accuracy']:.2f}%")
        else:
            print(f"  Checkpoint not found: {ckpt_path}")
    
    return results


def main():
    """Main function for voice biometrics evaluation"""
    print(f"Device: {Config.DEVICE}")
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    results = evaluate_all_models()
    
    # Print summary
    print("\n" + "="*60)
    print("Voice Biometrics Summary (Speaker Classification)")
    print("="*60)
    
    print(f"\n{'Model':<40} {'Best k':<10} {'Test Acc':<12}")
    print("-" * 65)
    
    for model_name, res in results.items():
        print(f"{model_name:<40} {res['best_k']:<10} {res['test_accuracy']:.2f}%")
    
    # Save results
    with open(os.path.join(Config.RESULTS_DIR, 'voice_biometrics_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {Config.RESULTS_DIR}/voice_biometrics_results.json")


if __name__ == "__main__":
    main()

