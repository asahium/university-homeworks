import numpy as np
import itertools
import os


def generate_permutations(n_permutations, grid_size, save_path=None):
    """
    Generate and save a fixed set of permutations for jigsaw puzzle task.
    
    Args:
        n_permutations (int): Number of permutations to generate
        grid_size (int): Size of the grid (e.g., 3 for 3x3)
        save_path (str, optional): Path to save permutations. If None, uses default naming.
        
    Returns:
        np.ndarray: Array of permutations
    """
    if save_path is None:
        save_path = f'permutations_{n_permutations}.npy'
    
    if os.path.exists(save_path):
        print(f"Loading existing permutations from {save_path}...")
        perms = np.load(save_path)
        return perms

    print("Generating new permutations...")
    n_patches = grid_size * grid_size
    
    # Create all possible permutations
    all_perms = list(itertools.permutations(range(n_patches)))
    
    # Select subset with maximum Hamming distance for diversity
    # (simplified version - random selection)
    np.random.shuffle(all_perms)
    selected_perms = all_perms[:n_permutations]
    
    np.save(save_path, selected_perms)
    print(f"Saved {n_permutations} permutations to {save_path}")
    return np.array(selected_perms)