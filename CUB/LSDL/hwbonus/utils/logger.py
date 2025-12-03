"""
Logging utilities for experiments
"""
import json
import os
from datetime import datetime

import sys
sys.path.append('.')
from config.config import Config


class Logger:
    """Simple logger for tracking experiments"""
    
    def __init__(self, experiment_name, config_dict=None, log_dir=None):
        self.experiment_name = experiment_name
        self.config_dict = config_dict or {}
        self.log_dir = log_dir or Config.RESULTS_DIR
        self.metrics = []
        self.summary = {}
        
        os.makedirs(self.log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(
            self.log_dir, 
            f"{experiment_name}_{timestamp}.json"
        )
    
    def log(self, metrics_dict, step=None):
        """Log metrics for a step"""
        entry = {**metrics_dict}
        if step is not None:
            entry['step'] = step
        entry['timestamp'] = datetime.now().isoformat()
        self.metrics.append(entry)
        
        # Print to console
        metric_str = ", ".join(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}" 
                              for k, v in metrics_dict.items())
        print(f"[{self.experiment_name}] {metric_str}")
    
    def log_summary(self, summary_dict):
        """Log summary metrics"""
        self.summary.update(summary_dict)
    
    def save(self):
        """Save logs to file"""
        data = {
            'experiment_name': self.experiment_name,
            'config': self.config_dict,
            'metrics': self.metrics,
            'summary': self.summary
        }
        
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Logs saved to {self.log_file}")
    
    def save_metrics_to_file(self, metrics, filepath):
        """Save specific metrics to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def finish(self):
        """Finalize logging"""
        self.save()


class WandbLogger:
    """
    Weights & Biases logger wrapper.
    Falls back to simple logging if wandb is not available.
    """
    
    def __init__(self, experiment_name, config_dict=None):
        self.experiment_name = experiment_name
        self.config_dict = config_dict or {}
        self.use_wandb = False
        self.simple_logger = Logger(experiment_name, config_dict)
        
        if Config.WANDB_PROJECT:
            try:
                import wandb
                
                if Config.WANDB_API_KEY:
                    wandb.login(key=Config.WANDB_API_KEY)
                
                wandb.init(
                    project=Config.WANDB_PROJECT,
                    entity=Config.WANDB_ENTITY,
                    name=experiment_name,
                    config=config_dict
                )
                self.use_wandb = True
                print(f"Initialized W&B logging for {experiment_name}")
            except ImportError:
                print("wandb not installed, using simple logging")
            except Exception as e:
                print(f"Failed to initialize wandb: {e}")
    
    def log(self, metrics_dict, step=None):
        """Log metrics"""
        self.simple_logger.log(metrics_dict, step)
        
        if self.use_wandb:
            import wandb
            wandb.log(metrics_dict, step=step)
    
    def log_summary(self, summary_dict):
        """Log summary metrics"""
        self.simple_logger.log_summary(summary_dict)
        
        if self.use_wandb:
            import wandb
            for key, value in summary_dict.items():
                wandb.run.summary[key] = value
    
    def save_metrics_to_file(self, metrics, filepath):
        """Save metrics to file"""
        self.simple_logger.save_metrics_to_file(metrics, filepath)
    
    def finish(self):
        """Finalize logging"""
        self.simple_logger.finish()
        
        if self.use_wandb:
            import wandb
            wandb.finish()

