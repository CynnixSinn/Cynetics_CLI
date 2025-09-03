import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class DeepSeekProvider(ModelProvider):
    """DeepSeek model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "deepseek-chat"
        self.base_url: str = "https://api.deepseek.com/v1"
        self.default_headers: Dict[str, str] = {
            "content-type": "application/json"
        }

    def configure(self, config: Dict[str, Any]):
        """Configure the DeepSeek provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "deepseek-chat")
        self.base_url = config.get("base_url", "https://api.deepseek.com/v1")
        
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using DeepSeek's API."""
        if not self.api_key:
            raise ValueError("DeepSeek API key is not set.")
        
        headers = {
            **self.default_headers,
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Prepare the messages
        messages = [{"role": "user", "content": prompt}]
        
        # Handle system message if provided
        system_message = kwargs.get("system")
        if system_message:
            messages.insert(0, {"role": "system", "content": system_message})
        
        # Prepare the data
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        
        # Add optional parameters
        if "temperature" in kwargs:
            data["temperature"] = kwargs["temperature"]
            
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]
            
        if "frequency_penalty" in kwargs:
            data["frequency_penalty"] = kwargs["frequency_penalty"]
            
        if "presence_penalty" in kwargs:
            data["presence_penalty"] = kwargs["presence_penalty"]
        
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