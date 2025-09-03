import yaml
from typing import Dict, Any

class Config:
    """Simple configuration class without pydantic."""
    
    def __init__(self, data: Dict[str, Any]):
        self.model_providers = data.get("model_providers", {})
        self.tools = data.get("tools", {})
        self.tui_enabled = data.get("tui_enabled", True)

def load_config(path: str) -> Config:
    """Load configuration from a YAML file."""
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return Config(data)
    except FileNotFoundError:
        # Return default config if file not found
        return Config({})

# Example config.yaml structure:
# model_providers:
#   openai:
#     api_key: "sk-..."
#   ollama:
#     host: "http://localhost:11434"
# tools:
#   enabled:
#     - "file_manager"
#     - "web_search"
# tui_enabled: true