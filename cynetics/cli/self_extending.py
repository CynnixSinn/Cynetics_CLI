import os
import click
import importlib.util
import sys
from typing import Dict, Any
from cynetics.models.provider import ModelProvider

class SelfExtendingCLI:
    """A system that allows the CLI to generate new subcommands and tools."""
    
    def __init__(self, provider: ModelProvider):
        self.provider = provider
        self.generated_commands = {}
        self.commands_dir = "commands"
        os.makedirs(self.commands_dir, exist_ok=True)
    
    def generate_new_command(self, description: str, name: str = None) -> Dict[str, Any]:
        """Generate a new CLI command based on a description."""
        # Simplified implementation for now
        command_data = {
            "name": name or "generated_command",
            "description": f"Generated command for {description}",
            "implementation": "@click.command()\ndef generated_command():\n    \"\"\"Generated command.\"\"\"\n    click.echo(\"This is a generated command\")",
            "created_at": __import__("datetime").datetime.now().isoformat()
        }
        self.generated_commands[command_data["name"]] = command_data
        return command_data
    
    def save_command(self, name: str, filepath: str = None) -> str:
        """Save a generated command to a Python file."""
        if name not in self.generated_commands:
            raise ValueError(f"Command {name} not found in generated commands")
        command_data = self.generated_commands[name]
        if not filepath:
            filepath = f"{self.commands_dir}/{name}.py"
        content = f"""\"\"\"
Generated CLI command: {command_data["name"]}
Description: {command_data["description"]}
Created at: {command_data["created_at"]}
\"\"\"

{command_data["implementation"]}
"""
        with open(filepath, "w") as f:
            f.write(content)
        return filepath
    
    def load_command(self, name: str) -> click.Command:
        """Load a generated command from a file."""
        filepath = f"{self.commands_dir}/{name}.py"
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Command file {filepath} not found")
        spec = importlib.util.spec_from_file_location(name, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        command_func = getattr(module, name, None)
        if command_func is None:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, click.Command):
                    return attr
            raise ValueError(f"No Click command found in {filepath}")
        return command_func
    
    def list_generated_commands(self) -> Dict[str, str]:
        """List all generated commands with their descriptions."""
        return {name: data["description"] for name, data in self.generated_commands.items()}
    
    def integrate_command(self, name: str, cli_group: click.Group):
        """Integrate a generated command into a Click CLI group."""
        if name not in self.generated_commands:
            raise ValueError(f"Command {name} not found in generated commands")
        try:
            command = self.load_command(name)
            cli_group.add_command(command)
            print(f"Command {name} successfully integrated into the CLI.")
        except Exception as e:
            print(f"Error integrating command {name}: {e}")
            print("Please check the generated command code for issues.")
