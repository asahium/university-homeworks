import numpy as np
from PIL import Image
import danila_biktimirov as model
import sys

def log(msg):
    print(msg, flush=True)

# Use smaller dataset for faster testing
data_file = sys.argv[1] if len(sys.argv) > 1 else 'data_100.npy'

log(f'Loading {data_file}...')
X = np.load(data_file)
log(f'Data shape: {X.shape}')

# Normalize to [0, 1]
X = X / 255.0

# Face size parameters
h, w = 75, 60
log(f'Face size: {h} x {w}')

log('Running Hard EM (n_restarts=3, max_iter=50)...')
F, B, s, A, L = model.run_EM_with_restarts(
    X, h, w, 
    tolerance=1e-3, 
    max_iter=50, 
    n_restarts=3, 
    use_MAP=True
)
log(f'Best L found: {L:.2f}')

# Convert to uint8 for saving
F_img = (F * 255).clip(0, 255).astype(np.uint8)
B_img = (B * 255).clip(0, 255).astype(np.uint8)

# Save images
Image.fromarray(F_img).save('criminal_face.png')
log('Saved: criminal_face.png')

Image.fromarray(B_img).save('background.png')
log('Saved: background.png')

log('\nDONE! Check criminal_face.png')

