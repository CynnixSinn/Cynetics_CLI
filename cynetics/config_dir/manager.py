import yaml
import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """A simple configuration manager supporting YAML and JSON formats."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = {}
        
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
    
    def load_config(self, file_path: str):
        """Load configuration from a file."""
        self.config_file = file_path
        
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    self.config = yaml.safe_load(f) or {}
                elif file_path.endswith('.json'):
                    self.config = json.load(f)
                else:
                    raise ValueError("Unsupported file format. Use .yaml, .yml, or .json")
        except Exception as e:
            raise ValueError(f"Failed to load config file: {e}")
    
    def save_config(self, file_path: Optional[str] = None):
        """Save configuration to a file."""
        path = file_path or self.config_file
        
        if not path:
            raise ValueError("No file path specified")
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w') as f:
                if path.endswith('.yaml') or path.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False)
                elif path.endswith('.json'):
                    json.dump(self.config, f, indent=2)
                else:
                    raise ValueError("Unsupported file format. Use .yaml, .yml, or .json")
        except Exception as e:
            raise ValueError(f"Failed to save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set a configuration value by key (supports dot notation)."""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def delete(self, key: str) -> bool:
        """Delete a configuration key."""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                return False
            config = config[k]
        
        # Delete the key if it exists
        if keys[-1] in config:
            del config[keys[-1]]
            return True
        return False
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self.config.copy()
    
    def set_all(self, config: Dict[str, Any]):
        """Set all configuration values."""
        self.config = config.copy()
    
    def merge(self, config: Dict[str, Any]):
        """Merge configuration with existing config."""
        def deep_merge(base: Dict[str, Any], update: Dict[str, Any]):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        deep_merge(self.config, config)
    
    def has(self, key: str) -> bool:
        """Check if a configuration key exists."""
        keys = key.split('.')
        config = self.config
        
        try:
            for k in keys:
                config = config[k]
            return True
        except (KeyError, TypeError):
            return False