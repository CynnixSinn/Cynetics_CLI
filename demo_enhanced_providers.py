#!/usr/bin/env python3
"""
Demonstration of Cynetics CLI Enhanced Model Provider Support
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_welcome():
    """Show welcome message."""
    print("Cynetics CLI Enhanced Model Provider Support Demo")
    print("=" * 50)
    print()

def demo_provider_support():
    """Demonstrate provider support."""
    print("1. Supported Model Providers")
    print("-" * 25)
    
    providers = [
        ("OpenAI", "GPT-4, GPT-3.5, etc."),
        ("Ollama", "Llama, Mistral, Mixtral, etc."),
        ("Anthropic", "Claude 3 Opus, Sonnet, Haiku"),
        ("OpenRouter", "100+ models via unified API"),
        ("Qwen", "Alibaba's Qwen models"),
        ("DeepSeek", "Specialized coding models"),
        ("Cohere", "Command R+, Embed models"),
        ("Google", "Gemini Pro, Ultra")
    ]
    
    for name, models in providers:
        print(f"  ✓ {name}: {models}")
    
    print()
    return True

def demo_configuration_example():
    """Show configuration example."""
    print("2. Configuration Example")
    print("-" * 23)
    
    config_example = """
model_providers:
  openai:
    api_key: "sk-..."  # Your OpenAI API key
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
"""
    
    print("Example config.yaml:")
    print(config_example)
    return True

def demo_api_usage():
    """Demonstrate API usage."""
    print("3. API Usage Example")
    print("-" * 18)
    
    print("To add a new provider programmatically:")
    print()
    print("```python")
    print("from cynetics.models.provider import ModelProvider")
    print("from typing import Dict, Any")
    print()
    print("class MyProvider(ModelProvider):")
    print("    def __init__(self):")
    print("        self.api_key = None")
    print("        self.model = \"default-model\"")
    print()
    print("    def configure(self, config: Dict[str, Any]):")
    print("        self.api_key = config.get(\"api_key\")")
    print("        self.model = config.get(\"model\", \"default-model\")")
    print()
    print("    def generate(self, prompt: str, **kwargs) -> str:")
    print("        # Implement API call to your provider")
    print("        pass")
    print()
    print("# Register the provider")
    print("from cynetics.cli.main import MODEL_PROVIDERS")
    print("MODEL_PROVIDERS['myprovider'] = MyProvider")
    print("```")
    print()
    return True

def demo_cli_usage():
    """Demonstrate CLI usage."""
    print("4. CLI Usage")
    print("-" * 12)
    
    print("Once configured, use providers with the CLI:")
    print()
    print("  $ python -m cynetics.cli generate --description \"Write a poem\" --provider openai")
    print("  $ python -m cynetics.cli generate --description \"Explain quantum computing\" --provider anthropic")
    print("  $ python -m cynetics.cli generate --description \"Solve this math problem\" --providers openai,anthropic --voting")
    print()
    return True

def demo_completion():
    """Show completion message."""
    print("Demo completed successfully! 🎉")
    print()
    print("Cynetics CLI now supports 8 major model providers out of the box,")
    print("with an extensible API for adding more providers.")
    print()
    print("For detailed instructions on adding custom providers, see:")
    print("  docs/adding_providers.md")
    print("  docs/enhanced_model_providers.md")
    print()
    return True

def main():
    """Run the demo."""
    demo_welcome()
    
    demos = [
        demo_provider_support,
        demo_configuration_example,
        demo_api_usage,
        demo_cli_usage,
        demo_completion
    ]
    
    for demo in demos:
        if not demo():
            print("Demo failed. Exiting.")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
