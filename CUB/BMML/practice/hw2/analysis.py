import numpy as np
from PIL import Image
import danila_biktimirov as model
import time

def generate_test_data(H, W, K, h, w, noise_std=0.1, seed=42):
    np.random.seed(seed)
    F_true = np.random.rand(h, w)
    B_true = np.random.rand(H, W)
    
    X = np.zeros((H, W, K))
    coords = []
    for k in range(K):
        dh = np.random.randint(0, H - h + 1)
        dw = np.random.randint(0, W - w + 1)
        coords.append((dh, dw))
        
        img = B_true.copy()
        img[dh:dh+h, dw:dw+w] = F_true
        X[:, :, k] = img + np.random.randn(H, W) * noise_std
    
    return X, F_true, B_true, coords

def mse(a, b):
    return np.mean((a - b) ** 2)

print("=" * 60)
print("ANALYSIS OF EM ALGORITHM FOR FACE RECOVERY")
print("=" * 60)

# =============================================================================
# 1. Test on generated data with different initializations
# =============================================================================
print("\n1. TESTING ON GENERATED DATA")
print("-" * 40)

H, W, K = 20, 30, 50
h, w = 10, 10
noise = 0.1

X, F_true, B_true, _ = generate_test_data(H, W, K, h, w, noise)

print(f"Image size: {H}x{W}, Face size: {h}x{w}, K={K}, noise={noise}")

# Single run
F1, B1, s1, A1, LL1 = model.run_EM(X, h, w, max_iter=50, use_MAP=True)
print(f"Single run: F_MSE={mse(F_true, F1):.6f}, B_MSE={mse(B_true, B1):.6f}, iters={len(LL1)}")

# With restarts
F2, B2, s2, A2, L2 = model.run_EM_with_restarts(X, h, w, max_iter=50, n_restarts=5, use_MAP=True)
print(f"5 restarts: F_MSE={mse(F_true, F2):.6f}, B_MSE={mse(B_true, B2):.6f}")

# =============================================================================
# 2. Effect of sample size
# =============================================================================
print("\n2. EFFECT OF SAMPLE SIZE")
print("-" * 40)

sample_sizes = [20, 50, 100, 200]
H, W, h, w = 20, 30, 10, 10

for K in sample_sizes:
    X, F_true, B_true, _ = generate_test_data(H, W, K, h, w, noise_std=0.1, seed=42)
    F, B, s, A, L = model.run_EM_with_restarts(X, h, w, max_iter=50, n_restarts=3, use_MAP=True)
    print(f"K={K:4d}: F_MSE={mse(F_true, F):.6f}, B_MSE={mse(B_true, B):.6f}, L/K={L/K:.2f}")

# =============================================================================
# 3. Effect of noise level
# =============================================================================
print("\n3. EFFECT OF NOISE LEVEL")
print("-" * 40)

noise_levels = [0.05, 0.1, 0.2, 0.3, 0.5]
H, W, K, h, w = 20, 30, 100, 10, 10

for noise in noise_levels:
    X, F_true, B_true, _ = generate_test_data(H, W, K, h, w, noise_std=noise, seed=42)
    F, B, s, A, L = model.run_EM_with_restarts(X, h, w, max_iter=50, n_restarts=3, use_MAP=True)
    print(f"noise={noise:.2f}: F_MSE={mse(F_true, F):.6f}, B_MSE={mse(B_true, B):.6f}, s_est={s:.4f}")

# =============================================================================
# 4. EM vs Hard EM comparison
# =============================================================================
print("\n4. EM vs HARD EM COMPARISON")
print("-" * 40)

H, W, K, h, w = 15, 20, 30, 6, 6
X, F_true, B_true, _ = generate_test_data(H, W, K, h, w, noise_std=0.15, seed=42)

# Hard EM
t0 = time.perf_counter()
F_hard, B_hard, s_hard, A_hard, LL_hard = model.run_EM(X, h, w, max_iter=50, use_MAP=True)
t_hard = time.perf_counter() - t0

# Soft EM
t0 = time.perf_counter()
F_soft, B_soft, s_soft, A_soft, LL_soft = model.run_EM(X, h, w, max_iter=50, use_MAP=False)
t_soft = time.perf_counter() - t0

print(f"Hard EM: F_MSE={mse(F_true, F_hard):.6f}, time={t_hard:.3f}s, L={LL_hard[-1]:.2f}")
print(f"Soft EM: F_MSE={mse(F_true, F_soft):.6f}, time={t_soft:.3f}s, L={LL_soft[-1]:.2f}")
print(f"Speed ratio: {t_soft/t_hard:.1f}x slower for soft EM")

# =============================================================================
# 5. Criminal data analysis
# =============================================================================
print("\n5. CRIMINAL DATA ANALYSIS")
print("-" * 40)

for data_file in ['data_100.npy', 'data_500.npy', 'data_1000.npy', 'data_2000.npy']:
    try:
        X = np.load(data_file) / 255.0
        K = X.shape[2]
        h, w = 75, 60
        
        t0 = time.perf_counter()
        F, B, s, A, L = model.run_EM_with_restarts(X, h, w, tolerance=1e-3, max_iter=50, n_restarts=3, use_MAP=True)
        elapsed = time.perf_counter() - t0
        
        print(f"{data_file}: K={K:4d}, L={L:.2f}, s={s:.4f}, time={elapsed:.1f}s")
        
        if data_file == 'data_2000.npy':
            F_img = (F * 255).clip(0, 255).astype(np.uint8)
            B_img = (B * 255).clip(0, 255).astype(np.uint8)
            Image.fromarray(F_img).save('criminal_face.png')
            Image.fromarray(B_img).save('background.png')
            print("  -> Saved criminal_face.png and background.png")
    except FileNotFoundError:
        print(f"{data_file}: not found")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

