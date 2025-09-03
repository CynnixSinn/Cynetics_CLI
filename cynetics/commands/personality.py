import click
from cynetics.personality.adaptive import AdaptivePersonality, AgentMode

@click.command()
@click.option('--mode', type=click.Choice(['precision', 'creative', 'autonomous']), 
              help='Set the agent mode')
@click.option('--list-modes', is_flag=True, help='List all available modes')
def personality(mode, list_modes):
    """Manage agent personality and modes."""
    
    adaptive_personality = AdaptivePersonality()
    
    if list_modes:
        # List all available modes
        modes = adaptive_personality.list_modes()
        click.echo("Available agent modes:")
        for mode_name, description in modes.items():
            current_indicator = " (current)" if mode_name == adaptive_personality.get_mode().value else ""
            click.echo(f"  {mode_name}: {description}{current_indicator}")
        return
    
    if mode:
        # Set the agent mode
        try:
            mode_enum = AgentMode(mode)
            adaptive_personality.set_mode(mode_enum)
            click.echo(f"Agent mode set to: {mode}")
            click.echo(f"Description: {adaptive_personality.get_mode_description()}")
        except ValueError:
            click.echo(f"Invalid mode: {mode}")
            return
    
    # Show current mode if no options were specified
    if not mode and not list_modes:
        current_mode = adaptive_personality.get_mode()
        click.echo(f"Current agent mode: {current_mode.value}")
        click.echo(f"Description: {adaptive_personality.get_mode_description()}")

if __name__ == "__main__":
    personality()