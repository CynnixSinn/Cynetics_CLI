import click
import readline
import os
from typing import Dict, Any
from cynetics.models.provider import ModelProvider
from cynetics.tools.base import BaseTool
from cynetics.personality.adaptive import AdaptivePersonality, AgentMode
from cynetics.context.fusion import ContextFusion
from cynetics.voting.consensus import ModelVoting

class AdvancedREPL:
    """An advanced REPL with history, autocomplete, and enhanced features."""
    
    def __init__(self, config, tools: Dict[str, BaseTool], model_providers: Dict[str, ModelProvider]):
        self.config = config
        self.tools = tools
        self.model_providers = model_providers
        self.current_model = next(iter(model_providers.values())) if model_providers else None
        self.personality = AdaptivePersonality()
        self.context_fusion = ContextFusion()
        self.model_voting = ModelVoting()
        
        # Register providers with fusion and voting systems
        for name, provider in model_providers.items():
            self.context_fusion.register_provider(name, provider)
            self.model_voting.register_provider(name, provider)
        
        # Set up history
        self.history_file = os.path.expanduser("~/.cynetics_history")
        self._load_history()
        
        # Set up autocomplete
        self._setup_autocomplete()
    
    def _load_history(self):
        """Load command history from file."""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
    
    def _save_history(self):
        """Save command history to file."""
        readline.write_history_file(self.history_file)
    
    def _setup_autocomplete(self):
        """Set up command autocomplete."""
        # Get all available commands
        commands = list(self.tools.keys()) + [
            'exit', 'quit', 'help', 'model', 'tools', 'personality', 
            'context', 'vote', 'history', 'clear'
        ]
        
        # Set up readline for autocomplete
        readline.set_completer(self._completer)
        readline.parse_and_bind("tab: complete")
        self.commands = commands
    
    def _completer(self, text, state):
        """Command completer function for readline."""
        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None
    
    def start(self):
        """Start the advanced REPL."""
        print("Starting Cynetics CLI Advanced REPL mode...")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                user_input = input("cynetics> ").strip()
                
                # Add to history
                if user_input:
                    readline.add_history(user_input)
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                # Parse and handle command
                self._handle_command(user_input)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit.")
            except EOFError:
                print("\nExiting...")
                break
        
        # Save history on exit
        self._save_history()
    
    def _handle_command(self, user_input: str):
        """Handle a user command."""
        if not user_input:
            return
        
        # Parse command and arguments
        parts = user_input.split()
        command = parts[0]
        args = parts[1:]
        
        # Handle built-in commands
        if command == 'help':
            self._show_help()
        elif command == 'model':
            self._handle_model_command(args)
        elif command == 'tools':
            self._list_tools()
        elif command == 'personality':
            self._handle_personality_command(args)
        elif command == 'context':
            self._handle_context_command(args)
        elif command == 'vote':
            self._handle_voting_command(args)
        elif command == 'history':
            self._show_history()
        elif command == 'clear':
            os.system('clear' if os.name == 'posix' else 'cls')
        elif command in self.tools:
            # Handle tool commands
            self._execute_tool(command, args)
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def _show_help(self):
        """Show available commands."""
        print("Available commands:")
        print("  help - Show this help message")
        print("  tools - List available tools")
        print("  model - Manage model providers")
        print("  personality - Manage agent personality modes")
        print("  context - Context fusion commands")
        print("  vote - Model voting commands")
        print("  history - Show command history")
        print("  clear - Clear the screen")
        print("  exit/quit - Exit the REPL")
        print("\nAvailable tools:")
        for tool_name in self.tools:
            print(f"  {tool_name} - {self.tools[tool_name].description}")
    
    def _handle_model_command(self, args):
        """Handle model-related commands."""
        if not args:
            print(f"Current model provider: {type(self.current_model).__name__ if self.current_model else 'None'}")
            print(f"Available providers: {', '.join(self.model_providers.keys())}")
            return
        
        subcommand = args[0]
        if subcommand == 'list':
            print("Available model providers:")
            for name in self.model_providers:
                current_marker = " (current)" if self.model_providers[name] == self.current_model else ""
                print(f"  {name}{current_marker}")
        elif subcommand == 'switch' and len(args) > 1:
            provider_name = args[1]
            if provider_name in self.model_providers:
                self.current_model = self.model_providers[provider_name]
                print(f"Switched to model provider: {provider_name}")
            else:
                print(f"Unknown model provider: {provider_name}")
        else:
            print("Usage: model [list|switch <provider>]")
    
    def _list_tools(self):
        """List available tools."""
        print("Available tools:")
        for name, tool in self.tools.items():
            print(f"  {name} - {tool.description}")
    
    def _handle_personality_command(self, args):
        """Handle personality mode commands."""
        if not args:
            current_mode = self.personality.get_mode()
            print(f"Current personality mode: {current_mode.value}")
            print("Use 'personality list' to see available modes or 'personality set <mode>' to set a mode.")
            return
        
        subcommand = args[0]
        if subcommand == 'list':
            modes = self.personality.list_modes()
            print("Available personality modes:")
            for mode, description in modes.items():
                current_marker = " (current)" if mode == self.personality.get_mode().value else ""
                print(f"  {mode} - {description}{current_marker}")
        elif subcommand == 'set' and len(args) > 1:
            mode_name = args[1]
            try:
                mode = AgentMode(mode_name.lower())
                self.personality.set_mode(mode)
                print(f"Personality mode set to: {mode.value}")
            except ValueError:
                print(f"Unknown mode: {mode_name}. Use 'personality list' to see available modes.")
        else:
            print("Usage: personality [list|set <mode>]")
    
    def _handle_context_command(self, args):
        """Handle context fusion commands."""
        if not args:
            print("Usage: context [providers|fusion <prompt>]")
            return
        
        subcommand = args[0]
        if subcommand == 'providers':
            print("Registered model providers for context fusion:")
            for name in self.context_fusion.providers:
                print(f"  {name}")
        elif subcommand == 'fusion' and len(args) > 1:
            prompt = " ".join(args[1:])
            providers = list(self.context_fusion.providers.keys())
            
            if not providers:
                print("No providers registered for context fusion.")
                return
            
            print("Generating context fusion...")
            result = self.context_fusion.generate_with_context(prompt, providers)
            
            print("\nResponses:")
            for provider, response in result["responses"].items():
                print(f"  [{provider}]: {response}")
            
            print("\nMerged Context:")
            print(result["merged_context"]["combined_response"])
        else:
            print("Usage: context [providers|fusion <prompt>]")
    
    def _handle_voting_command(self, args):
        """Handle model voting commands."""
        if not args:
            print("Usage: vote [providers|majority <prompt>]")
            return
        
        subcommand = args[0]
        if subcommand == 'providers':
            print("Registered model providers for voting:")
            for name in self.model_voting.providers:
                print(f"  {name}")
        elif subcommand == 'majority' and len(args) > 1:
            prompt = " ".join(args[1:])
            providers = list(self.model_voting.providers.keys())
            
            if not providers:
                print("No providers registered for voting.")
                return
            
            print("Generating responses for majority vote...")
            result = self.model_voting.majority_vote(prompt, providers)
            
            print("\nResponses:")
            for provider, response in result["responses"].items():
                print(f"  [{provider}]: {response}")
            
            print(f"\nMajority Vote: {result['majority_vote']}")
            print(f"Vote Count: {result['majority_count']}/{result['total_responses']}")
        else:
            print("Usage: vote [providers|majority <prompt>]")
    
    def _show_history(self):
        """Show command history."""
        print("Command History:")
        for i in range(readline.get_current_history_length()):
            item = readline.get_history_item(i + 1)
            if item:
                print(f"  {i + 1}: {item}")
    
    def _execute_tool(self, tool_name: str, args):
        """Execute a tool with the given arguments."""
        tool = self.tools[tool_name]
        
        # For now, we'll just show the tool's description
        # In a real implementation, we would parse the args and execute the tool
        print(f"Tool '{tool_name}' loaded. Description: {tool.description}")
        print("Tool execution not yet implemented in this demo.")