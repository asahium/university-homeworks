import torch
from torch.utils.data import Dataset
from PIL import Image
import os
import numpy as np
from torchvision import transforms


class RotationDataset(Dataset):
    """Custom Dataset for the rotation pretext task."""
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
                           if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = Image.open(img_path).convert('RGB')

        # Apply the base transformations
        if self.transform:
            image = self.transform(image)

        # Apply a random rotation and create the label
        rotation_angle_idx = torch.randint(0, 4, (1,)).item()  # 0: 0°, 1: 90°, 2: 180°, 3: 270°
        rotated_image = torch.rot90(image, k=rotation_angle_idx, dims=[1, 2])

        return rotated_image, rotation_angle_idx


class JigsawDataset(Dataset):
    """Custom Dataset for the jigsaw puzzle pretext task."""
    def __init__(self, image_dir, permutations, grid_size=3, patch_size=64, transform=None):
        self.image_dir = image_dir
        self.image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
                           if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.permutations = permutations
        self.grid_size = grid_size
        self.patch_size = patch_size
        self.transform = transform

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = Image.open(img_path).convert('RGB')
        
        # 1. Crop center square and divide into grid
        img_size = self.grid_size * self.patch_size
        center_crop = transforms.CenterCrop(img_size)
        image = center_crop(image)
        
        patches = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                box = (j * self.patch_size, i * self.patch_size, 
                      (j + 1) * self.patch_size, (i + 1) * self.patch_size)
                patch = image.crop(box)
                if self.transform:
                    patch = self.transform(patch)
                patches.append(patch)
        
        # 2. Choose random permutation
        perm_index = np.random.randint(0, len(self.permutations))
        perm = self.permutations[perm_index]
        
        # 3. Shuffle patches
        shuffled_patches = [patches[i] for i in perm]
        
        # Stack into tensor
        shuffled_patches_tensor = torch.stack(shuffled_patches)
        
        return shuffled_patches_tensor, torch.tensor(perm_index, dtype=torch.long)


class TestDataset(Dataset):
    """Dataset for test images."""
    def __init__(self, test_dir, transform=None):
        self.test_dir = test_dir
        self.transform = transform
        self.image_files = sorted([f for f in os.listdir(test_dir) 
                                 if f.endswith(('.png', '.jpg', '.jpeg'))])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.test_dir, self.image_files[idx])
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, self.image_files[idx]