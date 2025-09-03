# Adding New Model Providers to Cynetics CLI

Cynetics CLI supports a wide variety of model providers out of the box, but you can also easily add your own custom providers.

## Supported Providers

Cynetics CLI comes with built-in support for the following providers:

1. **OpenAI** - GPT models
2. **Ollama** - Local models
3. **Anthropic** - Claude models
4. **OpenRouter** - Various models through a unified API
5. **Qwen** - Alibaba's Qwen models
6. **DeepSeek** - DeepSeek models
7. **Cohere** - Cohere models
8. **Google** - Gemini models

## Adding a New Provider

To add a new model provider, follow these steps:

### 1. Create the Provider Class

Create a new Python file in the `cynetics/models/` directory:

```python
# cynetics/models/myprovider.py
import requests
from typing import Dict, Any
from cynetics.models.provider import ModelProvider

class MyProvider(ModelProvider):
    """Description of your provider."""
    
    def __init__(self):
        self.api_key = None
        self.model = "default-model"
        # Add other provider-specific attributes
    
    def configure(self, config: Dict[str, Any]):
        """Configure the provider with settings from config.yaml."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "default-model")
        # Configure other settings
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        # Implement the API call to your provider
        # Return the generated text
        pass
```

### 2. Register the Provider

Add your provider to the `MODEL_PROVIDERS` dictionary in `cynetics/cli.py`:

```python
# In cynetics/cli.py
from cynetics.models.myprovider import MyProvider

MODEL_PROVIDERS = {
    # ... existing providers ...
    "myprovider": MyProvider
}
```

### 3. Configure in config.yaml

Add your provider configuration to your `config.yaml`:

```yaml
model_providers:
  myprovider:
    api_key: "your-api-key"
    model: "your-model-name"
    # Add other provider-specific settings
```

### 4. Test Your Provider

Test your new provider with the CLI:

```bash
python -m cynetics.cli model-manager --list
```

## Example Provider Implementation

Here's a complete example of a simple provider:

```python
# cynetics/models/example_provider.py
import requests
from typing import Dict, Any
from cynetics.models.provider import ModelProvider

class ExampleProvider(ModelProvider):
    """Example model provider."""
    
    def __init__(self):
        self.api_key = None
        self.model = "example-model"
        self.base_url = "https://api.example.com/v1"
    
    def configure(self, config: Dict[str, Any]):
        """Configure the provider."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "example-model")
        self.base_url = config.get("base_url", "https://api.example.com/v1")
        
        if not self.api_key:
            raise ValueError("Example API key is required")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 1024)
        }
        
        response = requests.post(
            f"{self.base_url}/completions",
            headers=headers,
            json=data,
            timeout=kwargs.get("timeout", 30)
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract and return the generated text
        return response_data.get("text", "")
```

## Using the Model Manager CLI

You can manage model providers using the built-in CLI command:

```bash
# List all available providers
python -m cynetics.cli model-manager --list

# View current configuration
python -m cynetics.cli model-manager

# Add a new provider (requires a JSON config file)
python -m cynetics.cli model-manager --add myprovider /path/to/config.json

# Remove a provider
python -m cynetics.cli model-manager --remove myprovider
```

## Best Practices

1. **Error Handling**: Always implement proper error handling for API calls
2. **Timeouts**: Use reasonable timeouts to prevent hanging
3. **Security**: Never log or expose API keys
4. **Documentation**: Document your provider's configuration options
5. **Testing**: Test your provider with various inputs and edge cases

By following these guidelines, you can easily extend Cynetics CLI to support any model provider you need.