import numpy as np
import matplotlib.pyplot as plt
import time
import Student as model
import os

# --- Data Generation ---

def generate_test_data(H, W, K, h, w, noise_std, seed=42):
    """
    Generates a test dataset as described in the PDF.
    
    Creates a true background (stripes) and a true face (smiley).
    Places the face at random locations in the background for K images.
    Adds Gaussian noise.
    
    Returns:
        X: array (H, W, K) - Noisy images
        F_true: array (h, w) - True face
        B_true: array (H, W) - True background
    """
    np.random.seed(seed)
    
    # Create true background (e.g., horizontal stripes)
    B_true = np.zeros((H, W))
    for i in range(H):
        B_true[i, :] = i / H
    
    # Create true face (e.g., a simple smiley)
    F_true = np.full((h, w), 0.5) # Grey background
    if h >= 5 and w >= 5:
        F_true[1, 1] = 0.9 # Eye
        F_true[1, w-2] = 0.9 # Eye
        F_true[h-2, 1:w-1] = 0.1 # Mouth
    
    X = np.zeros((H, W, K))
    
    for k in range(K):
        # Choose random displacement
        dh = np.random.randint(0, H - h + 1)
        dw = np.random.randint(0, W - w + 1)
        
        # Create clean image
        clean_img = np.copy(B_true)
        clean_img[dh:dh+h, dw:dw+w] = F_true
        
        # Add noise
        X[:, :, k] = clean_img + np.random.normal(0, noise_std, (H, W))
        
    return X, F_true, B_true

# --- Plotting Utility ---

def plot_F_B(F, B, F_true, B_true, title_prefix, save_path):
    """Helper function to plot and save F and B images."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    
    axes[0, 0].imshow(F, cmap='gray', vmin=0, vmax=1)
    axes[0, 0].set_title(f"{title_prefix} - Recovered Face (F)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(B, cmap='gray', vmin=0, vmax=1)
    axes[0, 1].set_title(f"{title_prefix} - Recovered Background (B)")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(F_true, cmap='gray', vmin=0, vmax=1)
    axes[1, 0].set_title("True Face")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(B_true, cmap='gray', vmin=0, vmax=1)
    axes[1, 1].set_title("True Background")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{save_path}.png")
    plt.close(fig)
    print(f"Saved plot: {save_path}.png")

def plot_LL(LL_dict, title, save_path):
    """Helper function to plot lower bound curves."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, LL in LL_dict.items():
        ax.plot(LL, label=label)
    
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Evidence Lower Bound (L)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(f"{save_path}.png")
    plt.close(fig)
    print(f"Saved plot: {save_path}.png")

# --- Analysis Functions ---

def run_analysis_1(X, h, w, F_true, B_true, n_runs=3):
    """
    Analysis 1: Influence of Initialization.
    Runs EM several times and plots the best result.
    """
    print("\n--- Running Analysis 1: Influence of Initialization ---")
    
    best_L = -np.inf
    best_F, best_B, best_LL = None, None, None
    
    for i in range(n_runs):
        print(f"Restart {i+1}/{n_runs}...")
        F, B, s, A, LL = model.run_EM(X, h, w, max_iter=25, tolerance=1e-3)
        final_L = LL[-1]
        print(f"  ...final L = {final_L:.2f}")
        
        if final_L > best_L:
            best_L = final_L
            best_F, best_B, best_LL = F, B, LL
            
    plot_F_B(best_F, best_B, F_true, B_true, "Analysis 1", "analysis_1_best_FB")
    plot_LL({"Best Run": best_LL}, "Analysis 1: Best Run ELBO", "analysis_1_best_LL")

def run_analysis_2(H, W, h, w, F_true, B_true):
    """
    Analysis 2: Effect of Sample Size (K) and Noise (s).
    """
    print("\n--- Running Analysis 2: Effect of Sample Size & Noise ---")
    
    # Effect of K
    sample_sizes = [10, 50, 200]
    noise_std = 0.5
    LL_K = {}
    for K in sample_sizes:
        print(f"Running for K = {K}...")
        X_k, _, _ = generate_test_data(H, W, K, h, w, noise_std)
        F, B, s, A, LL = model.run_EM(X_k, h, w, max_iter=25, tolerance=1e-3)
        LL_K[f"K = {K}"] = LL / K # Normalize by K
        plot_F_B(F, B, F_true, B_true, f"Analysis 2 (K={K})", f"analysis_2_K_{K}_FB")
        
    plot_LL(LL_K, "Analysis 2: ELBO / K vs. Iteration (Varying K)", "analysis_2_K_LL")

    # Effect of Noise
    noise_levels = [0.1, 0.5, 1.0]
    K = 50
    LL_s = {}
    for noise in noise_levels:
        print(f"Running for noise = {noise}...")
        X_s, _, _ = generate_test_data(H, W, K, h, w, noise)
        F, B, s, A, LL = model.run_EM(X_s, h, w, max_iter=25, tolerance=1e-3)
        LL_s[f"Noise = {noise}"] = LL / K
        plot_F_B(F, B, F_true, B_true, f"Analysis 2 (Noise={noise})", f"analysis_2_noise_{noise}_FB")
        
    plot_LL(LL_s, "Analysis 2: ELBO / K vs. Iteration (Varying Noise)", "analysis_2_noise_LL")

def run_analysis_3(X, h, w, F_true, B_true):
    """
    Analysis 3: EM vs. Hard EM.
    """
    print("\n--- Running Analysis 3: EM vs. Hard EM ---")
    
    # Run standard EM
    print("Running Standard EM...")
    start_em = time.time()
    F_em, B_em, s_em, A_em, LL_em = model.run_EM(X, h, w, max_iter=25, tolerance=1e-3, use_MAP=False)
    time_em = time.time() - start_em
    print(f"  ...done in {time_em:.2f}s. Final L = {LL_em[-1]:.2f}")
    
    # Run Hard EM
    print("Running Hard EM...")
    start_hard_em = time.time()
    F_hard, B_hard, s_hard, A_hard, LL_hard = model.run_EM(X, h, w, max_iter=25, tolerance=1e-3, use_MAP=True)
    time_hard_em = time.time() - start_hard_em
    print(f"  ...done in {time_hard_em:.2f}s. Final L = {LL_hard[-1]:.2f}")
    
    # Plot results
    plot_LL({"Standard EM": LL_em, "Hard EM": LL_hard}, "Analysis 3: EM vs. Hard EM", "analysis_3_LL")
    plot_F_B(F_em, B_em, F_true, B_true, "Analysis 3 (Standard EM)", "analysis_3_EM_FB")
    plot_F_B(F_hard, B_hard, F_true, B_true, "Analysis 3 (Hard EM)", "analysis_3_HardEM_FB")
    
    print("\nComparison:")
    print(f"               | Standard EM | Hard EM")
    print(f"Time (s)       | {time_em:11.2f} | {time_hard_em:7.2f}")
    print(f"Final L        | {LL_em[-1]:11.2f} | {LL_hard[-1]:7.2f}")

def run_analysis_4(h, w, data_file='data_50.npy'):
    """
    Analysis 4: Run on criminal data.
    """
    print("\n--- Running Analysis 4: Criminal Data ---")
    if not os.path.exists(data_file):
        print(f"Data file '{data_file}' not found. Skipping Analysis 4.")
        print("Please download the data, name it 'data_50.npy', and place it in the same directory.")
        return

    print(f"Loading data from '{data_file}'...")
    X_criminal = np.load(data_file)
    print(f"Data shape: {X_criminal.shape}")
    
    # We don't have F_true, B_true, so we create placeholders
    F_placeholder = np.zeros((h, w))
    B_placeholder = np.zeros((X_criminal.shape[0], X_criminal.shape[1]))

    print("Running EM with restarts on criminal data...")
    F, B, s, A, L = model.run_EM_with_restarts(X_criminal, h, w, tolerance=1e-3, max_iter=100, n_restarts=10)
    
    print(f"Best L found: {L:.2f}")
    
    # Plot final recovered F and B
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    axes[0].imshow(F, cmap='gray')
    axes[0].set_title("Recovered Face (F)")
    axes[0].axis('off')
    
    axes[1].imshow(B, cmap='gray')
    axes[1].set_title("Recovered Background (B)")
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig("analysis_4_criminal_FB.png")
    plt.close(fig)
    print("Saved plot: analysis_4_criminal_FB.png")


# --- Main execution ---

def main():
    # Create directory for plots
    if not os.path.exists("plots"):
        os.makedirs("plots")
        
    # Parameters for generated data
    H, W = 30, 40
    h, w = 15, 15
    K = 50
    noise_std = 0.5
    
    # Generate main test set
    print("Generating test data...")
    X, F_true, B_true = generate_test_data(H, W, K, h, w, noise_std)
    print(f"Generated X with shape {X.shape}")
    
    # Run all analyses
    run_analysis_1(X, h, w, F_true, B_true, n_runs=5)
    run_analysis_2(H, W, h, w, F_true, B_true)
    run_analysis_3(X, h, w, F_true, B_true)
    
    # Run analysis 4 - Criminal data
    h_real, w_real = 75, 60  # Face size for criminal data
    run_analysis_4(h_real, w_real, data_file='data_50.npy')
    
    print("\n--- Analysis complete. Plots saved to directory. ---")

if __name__ == "__main__":
    main()
