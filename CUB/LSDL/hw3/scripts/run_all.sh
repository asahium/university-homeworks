#!/bin/bash

# Master script to run all experiments
# This will run all training, linear probing, fine-tuning, and evaluation scripts

echo "=========================================="
echo "Contrastive Learning Experiments Pipeline"
echo "=========================================="
echo ""

# Create necessary directories
mkdir -p checkpoints
mkdir -p results
mkdir -p data

# Step 1: Train supervised baseline
echo "[Step 1/6] Training Supervised Baseline..."
python scripts/train_supervised.py
if [ $? -ne 0 ]; then
    echo "Error: Supervised training failed"
    exit 1
fi
echo "✓ Supervised baseline completed"
echo ""

# Step 2: Train SimCLR
echo "[Step 2/6] Training SimCLR..."
python scripts/train_simclr.py
if [ $? -ne 0 ]; then
    echo "Error: SimCLR training failed"
    exit 1
fi
echo "✓ SimCLR training completed"
echo ""

# Step 3: Train BYOL
echo "[Step 3/6] Training BYOL..."
python scripts/train_byol.py
if [ $? -ne 0 ]; then
    echo "Error: BYOL training failed"
    exit 1
fi
echo "✓ BYOL training completed"
echo ""

# Step 4: Train MoCo (Bonus)
echo "[Step 4/6] Training MoCo (Bonus)..."
python scripts/train_moco.py
if [ $? -ne 0 ]; then
    echo "Error: MoCo training failed"
    exit 1
fi
echo "✓ MoCo training completed"
echo ""

# Step 5: Linear Probing
echo "[Step 5/6] Running Linear Probing for all SSL models..."
python scripts/linear_probe.py
if [ $? -ne 0 ]; then
    echo "Error: Linear probing failed"
    exit 1
fi
echo "✓ Linear probing completed"
echo ""

# Step 6: Fine-tuning
echo "[Step 6/6] Fine-tuning all SSL models..."
python scripts/finetune.py
if [ $? -ne 0 ]; then
    echo "Error: Fine-tuning failed"
    exit 1
fi
echo "✓ Fine-tuning completed"
echo ""

# Step 7: OOD Evaluation
echo "[Step 7/7] Evaluating OOD robustness..."
python scripts/evaluate_ood.py
if [ $? -ne 0 ]; then
    echo "Error: OOD evaluation failed"
    exit 1
fi
echo "✓ OOD evaluation completed"
echo ""

echo "=========================================="
echo "All experiments completed successfully!"
echo "=========================================="
echo ""
echo "Results saved to:"
echo "  - Checkpoints: ./checkpoints/"
echo "  - Metrics: ./results/"
echo ""
echo "Now run the visualization.ipynb notebook to see the results!"

