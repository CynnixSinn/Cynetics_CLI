import click
import json
import os
import yaml
from typing import Dict, Any
from cynetics.config_module import load_config, Config
from cynetics.models.provider import ModelProvider
from cynetics.models.openai import OpenAIProvider
from cynetics.models.ollama import OllamaProvider
from cynetics.models.anthropic import AnthropicProvider
from cynetics.models.openrouter import OpenRouterProvider
from cynetics.models.qwen import QwenProvider
from cynetics.models.deepseek import DeepSeekProvider
from cynetics.models.cohere import CohereProvider
from cynetics.models.google import GoogleProvider

# Model provider registry
MODEL_PROVIDERS = {
    "openai": OpenAIProvider,
    "ollama": OllamaProvider,
    "anthropic": AnthropicProvider,
    "openrouter": OpenRouterProvider,
    "qwen": QwenProvider,
    "deepseek": DeepSeekProvider,
    "cohere": CohereProvider,
    "google": GoogleProvider
}

@click.command()
@click.option('--list', 'list_providers', is_flag=True, help='List all available model providers')
@click.option('--add', 'add_provider', nargs=2, help='Add a new model provider (name config_file)')
@click.option('--remove', 'remove_provider', help='Remove a model provider by name')
@click.option('--config', 'config_file', default='config.yaml', help='Path to the configuration file')
@click.pass_context
def model_manager(ctx, list_providers, add_provider, remove_provider, config_file):
    """Manage model providers."""
    
    if list_providers:
        click.echo("Available Model Providers:")
        click.echo("==========================")
        for name, provider_class in MODEL_PROVIDERS.items():
            click.echo(f"  {name}: {provider_class.__name__}")
        click.echo()
        click.echo("To add a provider, create a config file with the required settings and use --add")
        return
    
    if add_provider:
        provider_name, provider_config_file = add_provider
        
        if provider_name not in MODEL_PROVIDERS:
            click.echo(f"Error: Unknown provider '{provider_name}'. Available providers: {', '.join(MODEL_PROVIDERS.keys())}")
            return
        
        try:
            # Load provider configuration
            with open(provider_config_file, 'r') as f:
                provider_config = json.load(f)
            
            # Load existing configuration
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
            else:
                config_data = {}
            
            # Add to configuration
            if 'model_providers' not in config_data:
                config_data['model_providers'] = {}
            
            config_data['model_providers'][provider_name] = provider_config
            
            # Save configuration
            with open(config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            
            click.echo(f"Added provider '{provider_name}' with configuration from '{provider_config_file}'")
            
        except FileNotFoundError:
            click.echo(f"Error: Configuration file '{provider_config_file}' not found")
            return
        except json.JSONDecodeError:
            click.echo(f"Error: Invalid JSON in configuration file '{provider_config_file}'")
            return
        except Exception as e:
            click.echo(f"Error: {e}")
            return
        
        return
    
    if remove_provider:
        try:
            # Load existing configuration
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
            else:
                click.echo(f"Configuration file '{config_file}' not found")
                return
            
            # Remove provider if it exists
            if 'model_providers' in config_data and remove_provider in config_data['model_providers']:
                del config_data['model_providers'][remove_provider]
                
                # Save configuration
                with open(config_file, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)
                
                click.echo(f"Removed provider '{remove_provider}'")
            else:
                click.echo(f"Provider '{remove_provider}' not found in configuration")
        except Exception as e:
            click.echo(f"Error: {e}")
        return
    
    # Show current providers
    try:
        config = load_config(config_file)
        click.echo("Current Model Providers:")
        click.echo("========================")
        
        if hasattr(config, 'model_providers'):
            for name, settings in config.model_providers.items():
                click.echo(f"  {name}:")
                for key, value in settings.items():
                    # Don't show API keys
                    if 'key' in key.lower() or 'secret' in key.lower():
                        click.echo(f"    {key}: ***")
                    else:
                        click.echo(f"    {key}: {value}")
        else:
            click.echo("  No providers configured")
    except Exception as e:
        click.echo(f"Error loading configuration: {e}")

if __name__ == "__main__":
    model_manager()