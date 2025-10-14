# HW2 - Self-Supervised Learning Project

This project implements self-supervised learning techniques using rotation and jigsaw puzzle pretext tasks, followed by fine-tuning for image classification.

## Project Structure

```
hw2/
├── src/
│   ├── models/
│   │   └── jigsaw_model.py      # JigsawNet model class
│   ├── datasets/
│   │   └── datasets.py          # Dataset classes (Rotation, Jigsaw, Test)
│   └── utils.py                 # Utility functions (permutation generation)
├── configs/
│   └── config.py                # Configuration and hyperparameters
├── scripts/
│   ├── train_rotation.py        # Rotation pretext task training
│   ├── train_jigsaw.py          # Jigsaw pretext task training
│   ├── finetune.py              # Fine-tuning script
│   └── inference.py             # Test set prediction generation
├── checkpoints/                 # Model weights (.pth files)
├── submissions/                 # Submission CSV files
├── notebooks/
│   ├── hw2.ipynb               # Main organized notebook
│   └── hw2_original.ipynb      # Original notebook backup
└── data/                       # Dataset directory
    ├── train/
    │   ├── labeled/            # Labeled training data
    │   └── unlabeled/          # Unlabeled data for pretext tasks
    └── test/                   # Test data
```

## Quick Start

### 1. Setup Environment

Make sure you have the required dependencies installed:
- PyTorch
- torchvision
- PIL (Pillow)
- pandas
- numpy
- tqdm

### 2. Training Pipeline

Run the training pipeline in order:

```bash
cd scripts/

# Step 1: Train rotation pretext task
python train_rotation.py

# Step 2: Train jigsaw pretext task  
python train_jigsaw.py

# Step 3: Fine-tune with rotation backbone
python finetune.py --method rotation

# Step 4: Fine-tune with jigsaw backbone
python finetune.py --method jigsaw

# Step 5: Train from scratch (baseline)
python finetune.py --method scratch
```

### 3. Generate Predictions

```bash
cd scripts/

# Generate predictions for each method
python inference.py --method rotation
python inference.py --method jigsaw
python inference.py --method scratch
```

## Configuration

All hyperparameters and paths are centralized in `configs/config.py`. Key settings include:

- **Training**: 30 epochs for pretraining and fine-tuning
- **Batch size**: 32
- **Learning rates**: 1e-3 (pretraining), 1e-4 (fine-tuning)
- **Jigsaw parameters**: 3x3 grid, 64px patches, 100 permutations

## Methods Implemented

### 1. Rotation Pretext Task
- Predicts rotation angle (0°, 90°, 180°, 270°)
- Uses standard ResNet-18 backbone
- Self-supervised learning on unlabeled data

### 2. Jigsaw Puzzle Pretext Task
- Predicts correct permutation of image patches
- Custom JigsawNet architecture
- 3x3 grid with 100 different permutations

### 3. Supervised Fine-tuning
- Uses pretrained backbones from pretext tasks
- 10-class classification task
- 90/10 train/validation split

## Output Files

- **Checkpoints**: Saved in `checkpoints/` directory
  - `resnet18_backbone_pretrained_rotations.pth`
  - `resnet18_jigsaw_backbone.pth`
  - `best_finetuned_model_rotations.pth`
  - `best_finetuned_jigsaw_model.pth`
  - `best_finetuned_model.pth`

- **Submissions**: CSV files in `submissions/` directory
  - `submission_rotations.csv`
  - `submission_jigsaw.csv` 
  - `submission.csv`

## Usage Tips

1. **Modular Design**: Each component is in a separate file for easy modification
2. **Configuration**: Change hyperparameters in `configs/config.py`
3. **Experimentation**: Scripts support different methods via command-line arguments
4. **Backup**: Original notebook is preserved in `notebooks/hw2_original.ipynb`

## Benefits of This Organization

- **Maintainability**: Code is separated into logical modules
- **Reusability**: Components can be easily reused or modified
- **Scalability**: Easy to add new pretext tasks or models
- **Reproducibility**: Configuration is centralized and version-controlled
- **Collaboration**: Clear structure makes it easy for others to understand