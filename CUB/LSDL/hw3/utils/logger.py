"""
Logging utilities with Weights & Biases
"""
import wandb
import json
import os
from config.config import Config


class WandbLogger:
    """Wrapper for Weights & Biases logging"""
    
    def __init__(self, experiment_name, config_dict=None, enabled=True):
        """
        Initialize wandb logger
        
        Args:
            experiment_name: Name of the experiment
            config_dict: Configuration dictionary to log
            enabled: Whether to enable wandb logging
        """
        self.enabled = enabled
        self.experiment_name = experiment_name
        
        if self.enabled:
            if Config.WANDB_API_KEY is not None:
                wandb.login(key=Config.WANDB_API_KEY)
            
            wandb.init(
                project=Config.WANDB_PROJECT,
                entity=Config.WANDB_ENTITY,
                name=experiment_name,
                config=config_dict,
                reinit=True
            )
    
    def log(self, metrics_dict, step=None):
        """Log metrics to wandb"""
        if self.enabled:
            wandb.log(metrics_dict, step=step)
    
    def log_summary(self, summary_dict):
        """Log summary metrics"""
        if self.enabled:
            for key, value in summary_dict.items():
                wandb.run.summary[key] = value
    
    def finish(self):
        """Finish wandb run"""
        if self.enabled:
            wandb.finish()
    
    @staticmethod
    def save_metrics_to_file(metrics, filepath):
        """Save metrics to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=4)
    
    @staticmethod
    def load_metrics_from_file(filepath):
        """Load metrics from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)

