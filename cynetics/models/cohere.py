import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class CohereProvider(ModelProvider):
    """Cohere model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "command-r-plus"
        self.base_url: str = "https://api.cohere.ai/v1"
        self.default_headers: Dict[str, str] = {
            "content-type": "application/json"
        }

    def configure(self, config: Dict[str, Any]):
        """Configure the Cohere provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "command-r-plus")
        self.base_url = config.get("base_url", "https://api.cohere.ai/v1")
        
        if not self.api_key:
            raise ValueError("Cohere API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Cohere's API."""
        if not self.api_key:
            raise ValueError("Cohere API key is not set.")
        
        headers = {
            **self.default_headers,
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Prepare the data
        data = {
            "model": self.model,
            "message": prompt,
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        
        # Add optional parameters
        if "temperature" in kwargs:
            data["temperature"] = kwargs["temperature"]
            
        if "p" in kwargs:
            data["p"] = kwargs["p"]
            
        if "k" in kwargs:
            data["k"] = kwargs["k"]
            
        if "frequency_penalty" in kwargs:
            data["frequency_penalty"] = kwargs["frequency_penalty"]
            
        if "presence_penalty" in kwargs:
            data["presence_penalty"] = kwargs["presence_penalty"]
            
        # Handle chat history if provided
        if "chat_history" in kwargs:
            data["chat_history"] = kwargs["chat_history"]
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text content
        if "text" in response_data:
            return response_data["text"]
        else:
            return ""