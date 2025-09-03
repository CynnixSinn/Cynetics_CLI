#!/usr/bin/env python3
"""
Simplified Cynetics CLI with configuration wizard.
"""

import os
import sys
import yaml
import click
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cynetics.cli.main import main as cynetics_main

# Allow overriding config file path with environment variable
CONFIG_FILE = os.environ.get('CYNETICS_CONFIG_FILE', os.path.expanduser("~/.cynetics_config.yaml"))

def load_or_create_config():
    """Load existing config or create a new one with wizard."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    # No config exists, run wizard
    print("Welcome to Cynetics CLI!")
    print("Let's set up your configuration.\\n")
    
    config = {"model_providers": {}, "tools": {"enabled": []}, "tui_enabled": True}
    
    # Model providers setup
    print("Model Providers Setup:")
    print("1. OpenAI (requires API key)")
    print("2. Ollama (local models)")
    print("3. Both")
    print("4. Skip for now")
    
    choice = input("Select an option (1-4): ").strip()
    
    if choice == "1":
        api_key = input("Enter your OpenAI API key: ").strip()
        model = input("Enter model name (default: gpt-4): ").strip() or "gpt-4"
        config["model_providers"]["openai"] = {
            "api_key": api_key,
            "model": model
        }
    elif choice == "2":
        host = input("Enter Ollama host (default: http://localhost:11434): ").strip() or "http://localhost:11434"
        model = input("Enter model name (default: llama3): ").strip() or "llama3"
        config["model_providers"]["ollama"] = {
            "host": host,
            "model": model
        }
    elif choice == "3":
        # OpenAI setup
        api_key = input("Enter your OpenAI API key: ").strip()
        model = input("Enter model name (default: gpt-4): ").strip() or "gpt-4"
        config["model_providers"]["openai"] = {
            "api_key": api_key,
            "model": model
        }
        
        # Ollama setup
        host = input("Enter Ollama host (default: http://localhost:11434): ").strip() or "http://localhost:11434"
        ollama_model = input("Enter Ollama model name (default: llama3): ").strip() or "llama3"
        config["model_providers"]["ollama"] = {
            "host": host,
            "model": ollama_model
        }
    
    # Tools setup
    print("\\nTools Setup:")
    enable_file_manager = input("Enable file manager tool? (y/n, default: y): ").strip().lower()
    if enable_file_manager != 'n':
        config["tools"]["enabled"].append("file_manager")
    
    enable_web_search = input("Enable web search tool? (y/n, default: y): ").strip().lower()
    if enable_web_search != 'n':
        config["tools"]["enabled"].append("web_search")
    
    # Save config
    try:
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print(f"\\nConfiguration saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"Warning: Could not save configuration: {e}")
    
    return config

@click.command()
@click.option('--repl', is_flag=True, help='Start in REPL mode.')
@click.option('--setup', is_flag=True, help='Run configuration wizard.')
@click.option('--version', is_flag=True, help='Show version information.')
def simple_cli(repl, setup, version):
    """Simplified Cynetics CLI with easier setup."""
    if version:
        print("Cynetics CLI v0.1.0 (Simplified)")
        return
    
    if setup:
        load_or_create_config()
        return
    
    # Try to load config
    config = load_or_create_config()
    
    # If no model providers configured, run setup
    if not config.get("model_providers"):
        print("No model providers configured. Running setup...")
        config = load_or_create_config()
    
    # Save config to temporary file for the main CLI
    temp_config = "/tmp/cynetics_temp_config.yaml"
    try:
        with open(temp_config, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        print(f"Error creating temporary config: {e}")
        return
    
    # Call the main CLI with our config
    sys.argv = [sys.argv[0], '--config', temp_config]
    if repl:
        sys.argv.append('run')
        sys.argv.append('--repl')
    else:
        sys.argv.append('run')
    
    try:
        cynetics_main()
    finally:
        # Clean up temporary config
        try:
            os.remove(temp_config)
        except:
            pass

if __name__ == "__main__":
    simple_cli()
