import yaml
import os

def load_config(path: str) -> dict:
    """Loads YAML config from given path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Optional: validate required fields
    if "detection" not in config or "sanitization" not in config:
        raise ValueError("Invalid config file. Must contain 'detection' and 'sanitization' sections.")
    
    return config