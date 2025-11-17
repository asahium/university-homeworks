# Contrastive Learning on STL-10

A comprehensive implementation of contrastive self-supervised learning methods including SimCLR, BYOL, and MoCo v2.

## Project Structure

```
contrastive-learning-project/
├── config/
│   └── config.py                 # Configuration settings
├── data/
│   └── datasets.py               # Dataset loaders and augmentations
├── models/
│   ├── __init__.py
│   ├── supervised.py             # Supervised baseline
│   ├── simclr.py                 # SimCLR implementation
│   ├── byol.py                   # BYOL implementation
│   └── moco.py                   # MoCo v2 implementation
├── utils/
│   ├── __init__.py
│   ├── logger.py                 # Weights & Biases logging
│   └── evaluation.py             # Evaluation utilities
├── scripts/
│   ├── train_supervised.py       # Train supervised baseline
│   ├── train_simclr.py           # Train SimCLR
│   ├── train_byol.py             # Train BYOL
│   ├── train_moco.py             # Train MoCo (bonus)
│   ├── linear_probe.py           # Linear probing for SSL models
│   ├── finetune.py               # Fine-tuning SSL models
│   ├── evaluate_ood.py           # OOD robustness evaluation
│   └── run_all.sh                # Master script to run everything
├── checkpoints/                  # Saved model checkpoints
├── results/                      # Training metrics (JSON)
├── visualization.ipynb           # Visualization notebook
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation

1. Clone the repository or extract the project files

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run All Experiments (Recommended)

Run the master script to train all models sequentially:

```bash
chmod +x scripts/run_all.sh
./scripts/run_all.sh
```

This will:
1. Train supervised baseline (~2-3 hours on GPU)
2. Train SimCLR (~4-6 hours on GPU)
3. Train BYOL (~4-6 hours on GPU)
4. Train MoCo (~4-6 hours on GPU)
5. Perform linear probing for all SSL models
6. Fine-tune all SSL models
7. Evaluate OOD robustness on CIFAR-10

**Total time: ~15-20 hours on GPU, much longer on CPU**

### Option 2: Run Individual Scripts

Train specific models:

```bash
# Train supervised baseline
python scripts/train_supervised.py

# Train self-supervised models
python scripts/train_simclr.py
python scripts/train_byol.py
python scripts/train_moco.py  # Bonus

# Linear probing
python scripts/linear_probe.py

# Fine-tuning
python scripts/finetune.py

# OOD evaluation
python scripts/evaluate_ood.py
```

## Visualization

After running experiments, launch the visualization notebook:

```bash
jupyter notebook visualization.ipynb
```

The notebook includes:
- Training curves for all models
- t-SNE embeddings visualization
- Linear probing vs fine-tuning comparisons
- OOD robustness results
- Summary tables

## Configuration

Modify hyperparameters in `config/config.py`:

```python
# Example: Change SimCLR learning rate
SIMCLR_LR = 3e-4

# Example: Change number of epochs
SIMCLR_EPOCHS = 200
```

## Weights & Biases Integration

The project includes Weights & Biases logging for experiment tracking:

1. Login to wandb:
```bash
wandb login
```

2. (Optional) Set your entity in `config/config.py`:
```python
WANDB_ENTITY = "your-username"
```

All training runs will be logged to wandb automatically with:
- Training/validation losses
- Learning rates
- Accuracies
- Custom metrics (e.g., BYOL projection std)

To disable wandb logging, set `enabled=False` when initializing the logger.

## Models Implemented

### 1. Supervised Baseline
- ResNet-18 trained on labeled STL-10 data
- Standard supervised learning baseline

### 2. SimCLR (Chen et al., 2020)
- Contrastive learning framework
- NT-Xent loss
- Strong data augmentation
- Projection head for contrastive learning

### 3. BYOL (Grill et al., 2020)
- Bootstrap Your Own Latent
- Non-contrastive self-supervised learning
- Online and target networks with momentum
- Predictor network
- Monitors projection standard deviation to detect collapse

### 4. MoCo v2 (He et al., 2019/2020) - Bonus
- Momentum Contrast
- Queue-based contrastive learning
- Momentum encoder
- Memory bank for negative samples

## Evaluation Methods

### Linear Probing
- Freeze pre-trained encoder
- Train only a linear classifier on top
- Tests quality of learned representations

### Fine-tuning
- Initialize with pre-trained weights
- Train the entire model end-to-end
- Typically achieves better performance

### OOD Robustness
- Evaluate on CIFAR-10 (out-of-distribution)
- Tests generalization to different data distribution
- 9 matching classes between STL-10 and CIFAR-10

## Results

All results are saved to:
- **Checkpoints**: `./checkpoints/*.pth`
- **Metrics**: `./results/*.json`
- **Wandb**: Online dashboard

Expected performance (approximate):
- Supervised: ~71-72% on STL-10
- SimCLR + Fine-tuning: ~73-75% on STL-10
- BYOL + Fine-tuning: ~73-75% on STL-10
- MoCo + Fine-tuning: ~73-75% on STL-10

## Dataset

The project uses:
- **STL-10**: 10 classes, 96x96 images
  - Train: 5,000 labeled images
  - Test: 8,000 labeled images
  - Unlabeled: 100,000 unlabeled images (for SSL)
- **CIFAR-10**: For OOD evaluation (9/10 matching classes)

Datasets are downloaded automatically on first run.

## Hardware Requirements

- **GPU**: Highly recommended (CUDA-compatible)
- **RAM**: 16GB+ recommended
- **Storage**: ~10GB for datasets and checkpoints

## Tips

1. **Use GPU**: Training on CPU will be extremely slow
2. **Monitor wandb**: Check training progress in real-time
3. **Adjust batch size**: If you run out of memory, reduce batch size in config
4. **Use mixed precision**: Already enabled for faster training
5. **Checkpoint management**: Models are saved after training completes

## Troubleshooting

### Out of Memory
- Reduce batch size in `config/config.py`
- Reduce image size (not recommended)
- Use gradient accumulation

### Slow Training
- Ensure GPU is being used (`Config.DEVICE`)
- Reduce number of workers if CPU-bound
- Enable mixed precision (already enabled)

### Import Errors
- Ensure you're in the project root directory
- Check that `sys.path.append('.')` is present in scripts

## Citation

If you use this code, please cite the original papers:

```bibtex
@inproceedings{chen2020simple,
  title={A simple framework for contrastive learning of visual representations},
  author={Chen, Ting and Kornblith, Simon and Norouzi, Mohammad and Hinton, Geoffrey},
  booktitle={ICML},
  year={2020}
}

@inproceedings{grill2020bootstrap,
  title={Bootstrap your own latent: A new approach to self-supervised learning},
  author={Grill, Jean-Bastien and Strub, Florian and Altch{\'e}, Florent and others},
  booktitle={NeurIPS},
  year={2020}
}

@inproceedings{he2020momentum,
  title={Momentum contrast for unsupervised visual representation learning},
  author={He, Kaiming and Fan, Haoqi and Wu, Yuxin and Xie, Saining and Girshick, Ross},
  booktitle={CVPR},
  year={2020}
}
```

## License

This project is for educational purposes.

## Contact

For questions or issues, please open an issue in the repository.

