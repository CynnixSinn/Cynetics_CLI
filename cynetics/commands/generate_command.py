import click
import os
import sys

# Add the project root to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cynetics.cli.self_extending import SelfExtendingCLI
from cynetics.models.openai import OpenAIProvider
from cynetics.models.ollama import OllamaProvider
from cynetics.models.anthropic import AnthropicProvider
from cynetics.config_module import load_config

@click.command()
@click.option('--description', required=True, help='Description of what the new command should do')
@click.option('--name', help='Name for the new command (will be generated if not provided)')
@click.option('--save', is_flag=True, help='Save the generated command to a file')
@click.option('--integrate', is_flag=True, help='Integrate the command into the current CLI')
@click.option('--provider', default='openai', help='Model provider to use (openai, ollama, anthropic)')
@click.option('--api-key', help='API key for the model provider (if not in config)')
def generate_command(description, name, save, integrate, provider, api_key):
    """Generate a new CLI command based on a description."""
    
    # Load config to get provider settings
    config = load_config('config.yaml')
    
    # Initialize the appropriate provider
    if provider == 'openai':
        provider_instance = OpenAIProvider()
        if api_key:
            provider_config = {"api_key": api_key}
        else:
            provider_config = config.model_providers.get("openai", {})
    elif provider == 'ollama':
        provider_instance = OllamaProvider()
        provider_config = config.model_providers.get("ollama", {})
    elif provider == 'anthropic':
        provider_instance = AnthropicProvider()
        if api_key:
            provider_config = {"api_key": api_key}
        else:
            provider_config = config.model_providers.get("anthropic", {})
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    provider_instance.configure(provider_config)
    
    # Create the self-extending CLI system
    self_extending_cli = SelfExtendingCLI(provider_instance)
    
    # Generate the new command
    click.echo("Generating new command...")
    try:
        command_data = self_extending_cli.generate_new_command(description, name)
        
        click.echo(f"Generated command: {command_data['name']}")
        click.echo(f"Description: {command_data['description']}")
        click.echo(f"Implementation:\n{command_data['implementation']}")
        
        # Save the command if requested
        if save:
            filepath = self_extending_cli.save_command(command_data['name'])
            click.echo(f"Command saved to: {filepath}")
            
            # Integrate the command if requested
            if integrate:
                try:
                    # Import the main CLI to add the command to it
                    from cynetics.cli.main import main
                    self_extending_cli.integrate_command(command_data['name'], main)
                except Exception as e:
                    click.echo(f"Warning: Could not integrate command automatically: {e}")
                    click.echo("You can manually integrate the command by importing it in main.py")
        
    except Exception as e:
        click.echo(f"Error generating command: {e}")

if __name__ == "__main__":
    generate_command()