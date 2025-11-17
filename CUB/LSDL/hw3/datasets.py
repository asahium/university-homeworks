"""
Dataset loaders and augmentation transforms
"""
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from config.config import Config


class DataAugmentation:
    """Data augmentation for different methods"""
    
    @staticmethod
    def get_supervised_transforms():
        """Standard augmentation for supervised training"""
        train_transform = transforms.Compose([
            transforms.RandomCrop(Config.IMG_SIZE, padding=12),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4),
            transforms.ToTensor(),
            transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
        ])
        
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
        ])
        
        return train_transform, test_transform
    
    @staticmethod
    def get_simclr_transforms():
        """SimCLR augmentation pipeline"""
        class SimCLRTransform:
            def __init__(self, size=Config.IMG_SIZE):
                self.transform = transforms.Compose([
                    transforms.RandomResizedCrop(size, scale=(0.2, 1.0)),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomApply([transforms.ColorJitter(0.8, 0.8, 0.8, 0.2)], p=0.8),
                    transforms.RandomGrayscale(p=0.2),
                    transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0)),
                    transforms.ToTensor(),
                    transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
                ])
            
            def __call__(self, x):
                return self.transform(x), self.transform(x)
        
        return SimCLRTransform()
    
    @staticmethod
    def get_byol_transforms():
        """BYOL augmentation pipeline with two different augmentations"""
        class BYOLTransform:
            def __init__(self, size=Config.IMG_SIZE):
                self.transform1 = transforms.Compose([
                    transforms.RandomResizedCrop(size, scale=(0.08, 1.0)),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.2, 0.1)], p=0.8),
                    transforms.RandomGrayscale(p=0.2),
                    transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0)),
                    transforms.ToTensor(),
                    transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
                ])
                
                self.transform2 = transforms.Compose([
                    transforms.RandomResizedCrop(size, scale=(0.08, 1.0)),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.2, 0.1)], p=0.8),
                    transforms.RandomGrayscale(p=0.2),
                    transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0)),
                    transforms.RandomSolarize(threshold=128, p=0.2),
                    transforms.ToTensor(),
                    transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
                ])
            
            def __call__(self, x):
                return self.transform1(x), self.transform2(x)
        
        return BYOLTransform()
    
    @staticmethod
    def get_moco_transforms():
        """MoCo augmentation pipeline"""
        class MoCoTransform:
            def __init__(self, size=Config.IMG_SIZE):
                self.transform = transforms.Compose([
                    transforms.RandomResizedCrop(size, scale=(0.2, 1.0)),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.4, 0.1)], p=0.8),
                    transforms.RandomGrayscale(p=0.2),
                    transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0)),
                    transforms.ToTensor(),
                    transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
                ])
            
            def __call__(self, x):
                return self.transform(x), self.transform(x)
        
        return MoCoTransform()


def get_stl10_dataloaders(split='train', batch_size=128, augmentation='supervised'):
    """
    Get STL-10 dataloaders
    
    Args:
        split: 'train', 'test', or 'unlabeled'
        batch_size: batch size
        augmentation: 'supervised', 'simclr', 'byol', or 'moco'
    """
    if augmentation == 'supervised':
        train_transform, test_transform = DataAugmentation.get_supervised_transforms()
        transform = train_transform if split == 'train' else test_transform
    elif augmentation == 'simclr':
        transform = DataAugmentation.get_simclr_transforms()
    elif augmentation == 'byol':
        transform = DataAugmentation.get_byol_transforms()
    elif augmentation == 'moco':
        transform = DataAugmentation.get_moco_transforms()
    else:
        raise ValueError(f"Unknown augmentation: {augmentation}")
    
    dataset = torchvision.datasets.STL10(
        root=Config.DATA_ROOT,
        split=split,
        download=True,
        transform=transform
    )
    
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(split in ['train', 'unlabeled']),
        num_workers=Config.NUM_WORKERS,
        pin_memory=Config.PIN_MEMORY,
        drop_last=(split == 'unlabeled')
    )
    
    return loader


def get_cifar10_ood_loader(batch_size=128):
    """Get CIFAR-10 test loader for OOD evaluation (excluding frog class)"""
    transform = transforms.Compose([
        transforms.Resize(Config.IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(Config.STL10_MEAN, Config.STL10_STD)
    ])
    
    cifar10_test = torchvision.datasets.CIFAR10(
        root=Config.DATA_ROOT,
        train=False,
        download=True,
        transform=transform
    )
    
    # CIFAR-10 to STL-10 class mapping
    cifar_to_stl_mapping = {
        0: 0,   # airplane
        1: 2,   # automobile -> car
        2: 1,   # bird
        3: 3,   # cat
        4: 4,   # deer
        5: 5,   # dog
        6: -1,  # frog (exclude)
        7: 6,   # horse
        8: 8,   # ship
        9: 9    # truck
    }
    
    # Filter out frog class
    filtered_indices = [i for i, (_, label) in enumerate(cifar10_test) if label != 6]
    filtered_dataset = torch.utils.data.Subset(cifar10_test, filtered_indices)
    
    class RemappedDataset(torch.utils.data.Dataset):
        def __init__(self, dataset, mapping):
            self.dataset = dataset
            self.mapping = mapping
        
        def __len__(self):
            return len(self.dataset)
        
        def __getitem__(self, idx):
            img, label = self.dataset[idx]
            return img, self.mapping[label]
    
    filtered_dataset = RemappedDataset(filtered_dataset, cifar_to_stl_mapping)
    
    loader = DataLoader(
        filtered_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=Config.NUM_WORKERS,
        pin_memory=Config.PIN_MEMORY
    )
    
    return loader

