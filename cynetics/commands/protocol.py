import click
import json
from cynetics.protocols.manager import CrossProtocolManager

@click.command()
@click.option('--protocol', required=True, help='Protocol to use (api, ssh, git)')
@click.option('--action', required=True, help='Action to execute')
@click.option('--config', type=click.Path(exists=True), help='Path to protocol configuration JSON file')
@click.option('--param', multiple=True, help='Additional parameters in key=value format')
def protocol(protocol, action, config, param):
    """Execute actions across different protocols (APIs, SSH, Git, etc.)."""
    
    # Create the cross-protocol manager
    manager = CrossProtocolManager()
    
    # Load configuration if provided
    if config:
        try:
            with open(config, 'r') as f:
                config_data = json.load(f)
            if manager.configure_adapter(protocol, config_data):
                click.echo(f"Configured {protocol} protocol successfully")
            else:
                click.echo(f"Failed to configure {protocol} protocol")
                return
        except Exception as e:
            click.echo(f"Error loading configuration: {e}")
            return
    
    # Parse additional parameters
    kwargs = {}
    for p in param:
        if '=' in p:
            key, value = p.split('=', 1)
            # Try to parse as JSON for complex values
            try:
                kwargs[key] = json.loads(value)
            except json.JSONDecodeError:
                kwargs[key] = value
    
    # Execute the action
    click.echo(f"Executing {action} on {protocol} protocol...")
    result = manager.execute_protocol_action(protocol, action, **kwargs)
    
    # Display the result
    if result["status"] == "success":
        click.echo("Action executed successfully:")
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo("Action failed:")
        click.echo(json.dumps(result, indent=2))

if __name__ == "__main__":
    protocol()