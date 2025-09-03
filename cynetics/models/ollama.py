import requests
from cynetics.models.provider import ModelProvider

class OllamaProvider(ModelProvider):
    """Ollama model provider for local models."""
    
    def __init__(self):
        self.host = "http://localhost:11434"
        self.model = "llama3"

    def configure(self, config: dict):
        """Configure the Ollama provider."""
        self.host = config.get("host", "http://localhost:11434")
        self.model = config.get("model", "llama3")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Ollama's API."""
        url = f"{self.host}/api/generate"
        
        data = {
            "model": self.model,
            "prompt": prompt,
            **kwargs
        }
        
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()
        
        # Ollama streams responses, so we need to collect them
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                # Each line is a JSON object
                import json
                try:
                    json_obj = json.loads(decoded_line)
                    full_response += json_obj.get("response", "")
                except json.JSONDecodeError:
                    pass  # Skip invalid lines
        
        return full_response