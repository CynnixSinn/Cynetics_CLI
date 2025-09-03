import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class AnthropicProvider(ModelProvider):
    """Anthropic model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "claude-3-opus-20240229"
        self.base_url: str = "https://api.anthropic.com/v1"
        self.default_headers: Dict[str, str] = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def configure(self, config: Dict[str, Any]):
        """Configure the Anthropic provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "claude-3-opus-20240229")
        self.base_url = config.get("base_url", "https://api.anthropic.com/v1")
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Anthropic's API."""
        if not self.api_key:
            raise ValueError("Anthropic API key is not set.")
        
        headers = {
            **self.default_headers,
            "x-api-key": self.api_key
        }
        
        # Prepare the messages
        messages = [{"role": "user", "content": prompt}]
        
        # Handle system message if provided
        system_message = kwargs.get("system")
        
        # Prepare the data
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        
        # Add optional parameters
        if system_message:
            data["system"] = system_message
            
        if "temperature" in kwargs:
            data["temperature"] = kwargs["temperature"]
            
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]
            
        if "top_k" in kwargs:
            data["top_k"] = kwargs["top_k"]
        
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text content
        if "content" in response_data and len(response_data["content"]) > 0:
            return response_data["content"][0]["text"]
        else:
            return ""