import requests
from cynetics.models.provider import ModelProvider

class OpenAIProvider(ModelProvider):
    """OpenAI model provider."""
    
    def __init__(self):
        self.api_key = None
        self.model = "gpt-4"
        self.base_url = "https://api.openai.com/v1"

    def configure(self, config: dict):
        """Configure the OpenAI provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "gpt-4")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI's API."""
        if not self.api_key:
            raise ValueError("OpenAI API key is not set.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]