import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class OpenRouterProvider(ModelProvider):
    """OpenRouter model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "openai/gpt-3.5-turbo"
        self.base_url: str = "https://openrouter.ai/api/v1"
        self.site_url: Optional[str] = None
        self.site_name: Optional[str] = None

    def configure(self, config: Dict[str, Any]):
        """Configure the OpenRouter provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "openai/gpt-3.5-turbo")
        self.base_url = config.get("base_url", "https://openrouter.ai/api/v1")
        self.site_url = config.get("site_url")
        self.site_name = config.get("site_name")
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenRouter's API."""
        if not self.api_key:
            raise ValueError("OpenRouter API key is not set.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url or "https://github.com/cynetics-ai/cynetics-cli",
            "X-Title": self.site_name or "Cynetics CLI",
            "Content-Type": "application/json"
        }
        
        # Prepare the messages
        messages = [{"role": "user", "content": prompt}]
        
        # Add system message if provided
        if "system" in kwargs:
            messages.insert(0, {"role": "system", "content": kwargs["system"]})
        
        # Prepare the data
        data = {
            "model": self.model,
            "messages": messages,
        }
        
        # Add optional parameters
        if "temperature" in kwargs:
            data["temperature"] = kwargs["temperature"]
            
        if "max_tokens" in kwargs:
            data["max_tokens"] = kwargs["max_tokens"]
            
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text content
        if "choices" in response_data and len(response_data["choices"]) > 0:
            choice = response_data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
        
        return ""