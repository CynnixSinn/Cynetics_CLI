import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class QwenProvider(ModelProvider):
    """Qwen model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "qwen-max"
        self.base_url: str = "https://dashscope.aliyuncs.com/api/v1"
        self.default_headers: Dict[str, str] = {
            "content-type": "application/json"
        }

    def configure(self, config: Dict[str, Any]):
        """Configure the Qwen provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "qwen-max")
        self.base_url = config.get("base_url", "https://dashscope.aliyuncs.com/api/v1")
        
        if not self.api_key:
            raise ValueError("Qwen API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Qwen's API."""
        if not self.api_key:
            raise ValueError("Qwen API key is not set.")
        
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
            "input": {
                "messages": messages
            },
            "parameters": {
                "max_tokens": kwargs.get("max_tokens", 1024),
            }
        }
        
        # Add optional parameters
        if "temperature" in kwargs:
            data["parameters"]["temperature"] = kwargs["temperature"]
            
        if "top_p" in kwargs:
            data["parameters"]["top_p"] = kwargs["top_p"]
            
        if "top_k" in kwargs:
            data["parameters"]["top_k"] = kwargs["top_k"]
        
        response = requests.post(
            f"{self.base_url}/services/aigc/text-generation/generation",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text content
        if "output" in response_data and "text" in response_data["output"]:
            return response_data["output"]["text"]
        else:
            return ""