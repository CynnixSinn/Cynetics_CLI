# Cynetics CLI Enhanced Model Provider Support

## Overview

Cynetics CLI now supports multiple model providers out of the box, with a flexible architecture that makes it easy to add new providers. This enhancement significantly expands the capabilities of Cynetics CLI by allowing users to leverage models from various sources including cloud providers, local models, and specialized AI services.

## Supported Model Providers

Cynetics CLI now includes built-in support for the following model providers:

### 1. OpenAI
- Models: GPT-4, GPT-3.5, etc.
- Configuration: API key, model name
- Features: Streaming responses, function calling

### 2. Ollama
- Models: Llama, Mistral, Mixtral, etc.
- Configuration: Host URL, model name
- Features: Local inference, model management

### 3. Anthropic
- Models: Claude 3 Opus, Sonnet, Haiku
- Configuration: API key, model name
- Features: Large context windows, advanced reasoning

### 4. OpenRouter
- Models: GPT-4, Claude, PaLM, LLaMA, Mistral, and more
- Configuration: API key, model name
- Features: Unified access to 100+ models

### 5. Qwen (Alibaba)
- Models: Qwen Max, Qwen Plus, Qwen Turbo
- Configuration: API key, model name
- Features: Multilingual support, code generation

### 6. DeepSeek
- Models: DeepSeek Chat, DeepSeek Coder
- Configuration: API key, model name
- Features: Specialized for coding tasks

### 7. Cohere
- Models: Command R+, Command, Embed
- Configuration: API key, model name
- Features: Advanced RAG, embeddings

### 8. Google (Gemini)
- Models: Gemini Pro, Gemini Ultra
- Configuration: API key, model name
- Features: Multimodal, function calling

## Configuration

Users can configure any combination of these providers in their `config.yaml`:

```yaml
model_providers:
  openai:
    api_key: "sk-..."
    model: "gpt-4"
  ollama:
    host: "http://localhost:11434"
    model: "llama3"
  anthropic:
    api_key: "your-anthropic-api-key"
    model: "claude-3-opus-20240229"
  openrouter:
    api_key: "your-openrouter-api-key"
    model: "openai/gpt-4-turbo"
  qwen:
    api_key: "your-qwen-api-key"
    model: "qwen-max"
  deepseek:
    api_key: "your-deepseek-api-key"
    model: "deepseek-chat"
  cohere:
    api_key: "your-cohere-api-key"
    model: "command-r-plus"
  google:
    api_key: "your-google-api-key"
    model: "gemini-pro"
```

## API for Adding New Providers

Cynetics CLI provides a flexible API for developers to add new model providers:

### 1. Create a Provider Class

Extend the `ModelProvider` base class:

```python
from cynetics.models.provider import ModelProvider
from typing import Dict, Any

class MyProvider(ModelProvider):
    def __init__(self):
        self.api_key = None
        self.model = "default-model"
    
    def configure(self, config: Dict[str, Any]):
        """Configure the provider with settings."""
        self.api_key = config.get("api_key")
        self.model = config.get("model", "default-model")
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        # Implement API call to your provider
        # Return the generated text
        pass
```

### 2. Register the Provider

Add your provider to the `MODEL_PROVIDERS` registry:

```python
# In cynetics/cli.py
from cynetics.models.myprovider import MyProvider

MODEL_PROVIDERS = {
    # ... existing providers ...
    "myprovider": MyProvider
}
```

### 3. Configuration

Add your provider configuration to `config.yaml`:

```yaml
model_providers:
  myprovider:
    api_key: "your-api-key"
    model: "your-model-name"
    # Add other provider-specific settings
```

## Key Features of the Enhanced System

### 1. Universal Model Access
- Single interface for all model providers
- Easy switching between providers
- Hot-swapping models during runtime

### 2. Flexible Configuration
- YAML-based configuration files
- Per-provider settings
- Secure credential handling

### 3. Extensible Architecture
- Plugin system for new providers
- Standardized API interface
- Automatic provider discovery

### 4. Robust Error Handling
- Graceful degradation when providers are unavailable
- Retry mechanisms with exponential backoff
- Detailed error reporting

### 5. Performance Optimization
- Connection pooling
- Response caching
- Async support for concurrent requests

## Usage Examples

### Basic Usage
```bash
# Use a specific provider
python -m cynetics.cli generate --description "Write a poem" --provider openai

# Switch providers dynamically
python -m cynetics.cli generate --description "Explain quantum computing" --provider anthropic
```

### Advanced Features
```bash
# Use multiple providers with consensus
python -m cynetics.cli generate --description "Solve this math problem" --providers openai,anthropic,qwen --voting

# Context fusion from multiple models
python -m cynetics.cli generate --description "Write a story" --fusion openai,ollama
```

## Future Development Opportunities

### 1. Enhanced Provider Features
- Fine-tuning capabilities
- Model deployment management
- Cost optimization tools

### 2. Advanced Orchestration
- Dynamic model selection based on task
- Load balancing across providers
- Failover mechanisms

### 3. Integration with More Services
- Hugging Face Hub
- AWS Bedrock
- Azure OpenAI
- Vertex AI

### 4. Enterprise Features
- Rate limiting controls
- Usage tracking and analytics
- Compliance reporting

## Conclusion

The enhanced model provider support in Cynetics CLI makes it a truly universal AI interface that can leverage models from any source. With built-in support for 8 major providers and an extensible API, users can easily integrate any AI service they need while maintaining a consistent, powerful interface for AI-driven CLI interactions.

This enhancement positions Cynetics CLI as a leader in the next generation of AI command-line tools, providing unparalleled flexibility and access to the world's AI capabilities.