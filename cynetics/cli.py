import click
import os
import json
from cynetics.config_module import load_config
from cynetics.models.provider import ModelProvider
from cynetics.models.openai import OpenAIProvider
from cynetics.models.ollama import OllamaProvider
from cynetics.models.anthropic import AnthropicProvider
from cynetics.models.openrouter import OpenRouterProvider
from cynetics.models.qwen import QwenProvider
from cynetics.models.deepseek import DeepSeekProvider
from cynetics.models.cohere import CohereProvider
from cynetics.models.google import GoogleProvider
from cynetics.utils.tui import show_welcome_message
from cynetics.tools import load_tool
from cynetics.commands.generate_command import generate_command
from cynetics.commands.agent_mesh import agent_mesh
from cynetics.commands.knowledge_snapshot import knowledge_snapshot
from cynetics.commands.self_healing import self_healing
from cynetics.commands.multimodal import multimodal
from cynetics.commands.task_delegation import task_delegation
from cynetics.commands.cli_tutorial import cli_tutorial
from cynetics.commands.autocomplete import autocomplete
from cynetics.commands.playbooks import playbooks
from cynetics.commands.debugger import debugger
from cynetics.commands.model_manager import model_manager
from cynetics.commands.test_cmd import test_cmd
from cynetics.personality.modes import list_modes, set_mode
from cynetics.team.team_session import TeamSession
from cynetics.context.fusion import ContextFusion
from cynetics.voting.consensus import ModelVoting
from cynetics.cli.advanced_repl import AdvancedREPL

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

class CyneticsCLI:
    """Main CLI class with enhanced REPL features."""
    
    def __init__(self, config):
        self.config = config
        self.tools = {}
        self.model_providers = {}
        self.current_model = None
        self._load_tools()
        self._load_model_providers()
    
    def _load_tools(self):
        """Load enabled tools from config."""
        enabled_tools = self.config.tools.get("enabled", [])
        for tool_name in enabled_tools:
            try:
                self.tools[tool_name] = load_tool(tool_name)
            except ValueError as e:
                click.echo(f"Warning: {e}")
    
    def _load_model_providers(self):
        """Load model providers from config."""
        providers_config = self.config.model_providers
        for provider_name, provider_config in providers_config.items():
            if provider_name in MODEL_PROVIDERS:
                provider = MODEL_PROVIDERS[provider_name]()
                provider.configure(provider_config)
                self.model_providers[provider_name] = provider
                # Set the first provider as current by default
                if self.current_model is None:
                    self.current_model = provider
    
    def start_repl(self):
        """Start the interactive REPL mode with history and autocomplete."""
        repl = AdvancedREPL(self.config, self.tools, self.model_providers)
        repl.start()

@click.group()
@click.option('--config', default='config.yaml', help='Path to the configuration file.')
@click.pass_context
def main(ctx, config):
    """Cynetics CLI - The next-generation AI-driven command-line tool."""
    show_welcome_message()
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config)

@main.command()
@click.option('--repl', is_flag=True, help='Start in REPL mode.')
@click.pass_context
def run(ctx, repl):
    """Run the Cynetics CLI."""
    config = ctx.obj['config']
    if repl:
        cli = CyneticsCLI(config)
        cli.start_repl()
    else:
        # Placeholder for single-command execution
        click.echo("Single-command execution mode. Use --repl for interactive mode.")

@main.command()
@click.option('--list-modes', is_flag=True, help='List available personality modes.')
@click.option('--mode', help='Set the personality mode.')
@click.pass_context
def personality(ctx, list_modes, mode):
    """Manage agent personality and modes."""
    if list_modes:
        modes = list_modes()
        click.echo("Available personality modes:")
        for m in modes:
            click.echo(f"  {m}")
    elif mode:
        try:
            set_mode(mode)
            click.echo(f"Personality mode set to: {mode}")
        except ValueError as e:
            click.echo(f"Error: {e}")
    else:
        click.echo("Current personality mode: default")
        click.echo("Use --list-modes to see available modes or --mode <mode> to set a mode.")

@main.command()
@click.option('--protocol', required=True, help='Protocol to use (api, ssh, git, etc.)')
@click.option('--action', required=True, help='Action to perform')
@click.option('--config', 'config_file', help='Configuration file for the protocol')
@click.option('--param', multiple=True, help='Parameters in key=value format')
@click.pass_context
def protocol(ctx, protocol, action, config_file, param):
    """Execute actions across different protocols."""
    # Parse parameters
    params = {}
    for p in param:
        if '=' in p:
            key, value = p.split('=', 1)
            # Try to parse JSON values
            try:
                params[key] = json.loads(value)
            except json.JSONDecodeError:
                params[key] = value
    
    # Import protocol manager here to avoid circular imports
    from cynetics.protocols.manager import create_protocol_manager
    
    # Create protocol manager
    protocol_manager = create_protocol_manager()
    
    # Load config if provided
    config = {}
    if config_file:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            click.echo(f"Error loading config file: {e}")
            return
    
    # Connect to the protocol
    try:
        if not protocol_manager.connect(protocol, config):
            click.echo(f"Failed to connect to {protocol} protocol")
            return
    except Exception as e:
        click.echo(f"Error connecting to {protocol} protocol: {e}")
        return
    
    # Execute the action
    try:
        result = protocol_manager.execute_action(protocol, action, params)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error executing action: {e}")
    finally:
        # Disconnect from the protocol
        try:
            protocol_manager.disconnect(protocol)
        except:
            pass

@main.command()
@click.option('--create', is_flag=True, help='Create a new team session')
@click.option('--session-id', help='Session ID')
@click.option('--user-id', help='User ID')
@click.option('--user-name', help='User name')
@click.option('--send-message', help='Send a message to the team')
@click.option('--get-history', is_flag=True, help='Get chat history')
@click.option('--set-context', nargs=2, help='Set context key-value pair')
@click.option('--get-context', is_flag=True, help='Get shared context')
@click.pass_context
def team(ctx, create, session_id, user_id, user_name, send_message, get_history, set_context, get_context):
    """Collaborate with other users in a team session."""
    if not session_id:
        click.echo("Error: --session-id is required")
        return
    
    session = TeamSession(session_id)
    
    if create:
        if not user_id or not user_name:
            click.echo("Error: --user-id and --user-name are required to create a session")
            return
        session.add_user(user_id, user_name)
        click.echo(f"Created team session: {session_id}")
    elif send_message:
        if not user_id or not user_name:
            click.echo("Error: --user-id and --user-name are required to send a message")
            return
        session.add_user(user_id, user_name)
        session.send_message(user_id, send_message)
        click.echo("Message sent")
    elif get_history:
        history = session.get_history()
        for msg in history:
            click.echo(f"[{msg['timestamp']}] {msg['user_name']}: {msg['message']}")
    elif set_context:
        key, value = set_context
        session.set_context(key, value)
        click.echo(f"Context set: {key} = {value}")
    elif get_context:
        context = session.get_context()
        for key, value in context.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo("Team session ready. Use subcommands to interact.")

# Add the generate-command subcommand
main.add_command(generate_command)

# Add the agent-mesh subcommand
main.add_command(agent_mesh)

# Add the knowledge-snapshot subcommand
main.add_command(knowledge_snapshot)

# Add the self-healing subcommand
main.add_command(self_healing)

# Add the multimodal subcommand
main.add_command(multimodal)

# Add the task-delegation subcommand
main.add_command(task_delegation)

# Add the cli-tutorial subcommand
main.add_command(cli_tutorial)

# Add the autocomplete subcommand
main.add_command(autocomplete)

# Add the playbooks subcommand
main.add_command(playbooks)

# Add the debugger subcommand
main.add_command(debugger)

# Add the model manager subcommand
main.add_command(model_manager)

# Add test command
main.add_command(test_cmd)

if __name__ == "__main__":
    main()