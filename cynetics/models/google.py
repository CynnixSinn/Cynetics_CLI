import requests
import json
from typing import Dict, Any, Optional
from cynetics.models.provider import ModelProvider

class GoogleProvider(ModelProvider):
    """Google Gemini model provider."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "gemini-pro"
        self.base_url: str = "https://generativelanguage.googleapis.com/v1beta"
        self.default_headers: Dict[str, str] = {
            "content-type": "application/json"
        }

    def configure(self, config: Dict[str, Any]):
        """Configure the Google provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "gemini-pro")
        self.base_url = config.get("base_url", "https://generativelanguage.googleapis.com/v1beta")
        
        if not self.api_key:
            raise ValueError("Google API key is required")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Google's Gemini API."""
        if not self.api_key:
            raise ValueError("Google API key is not set.")
        
        headers = {
            **self.default_headers
        }
        
        # Prepare the contents
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        
        # Handle system instructions if provided
        system_instruction = kwargs.get("system")
        
        # Prepare the data
        data = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", 1024),
            }
        }
        
        # Add system instruction if provided
        if system_instruction:
            data["systemInstruction"] = {"parts": [{"text": system_instruction}]}
            
        # Add optional parameters
        if "temperature" in kwargs:
            data["generationConfig"]["temperature"] = kwargs["temperature"]
            
        if "topP" in kwargs:
            data["generationConfig"]["topP"] = kwargs["topP"]
            
        if "topK" in kwargs:
            data["generationConfig"]["topK"] = kwargs["topK"]
        
        response = requests.post(
            f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text content
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if len(parts) > 0 and "text" in parts[0]:
                    return parts[0]["text"]
        
        return ""