import click
import json
import uuid
from cynetics.team.mode import team_manager

@click.command()
@click.option('--session-id', help='Session ID to join or create')
@click.option('--user-id', required=True, help='User ID')
@click.option('--user-name', required=True, help='User name')
@click.option('--create', is_flag=True, help='Create a new session')
@click.option('--list-sessions', is_flag=True, help='List all active sessions')
@click.option('--send-message', help='Send a message to the session')
@click.option('--get-history', is_flag=True, help='Get chat history')
@click.option('--get-context', is_flag=True, help='Get shared context')
@click.option('--set-context', nargs=2, help='Set a key-value pair in shared context')
def team(session_id, user_id, user_name, create, list_sessions, send_message, get_history, get_context, set_context):
    """Collaborate with other users in a team session."""
    
    # List sessions if requested
    if list_sessions:
        sessions = team_manager.list_sessions()
        if sessions:
            click.echo("Active sessions:")
            for session in sessions:
                click.echo(f"  {session}")
        else:
            click.echo("No active sessions")
        return
    
    # Create a new session if requested
    if create:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        try:
            session = team_manager.create_session(session_id)
            session.add_user(user_id, user_name)
            click.echo(f"Created session: {session_id}")
            click.echo(f"You ({user_name}) have joined the session")
        except ValueError as e:
            click.echo(f"Error: {e}")
        return
    
    # Validate session ID for other operations
    if not session_id:
        click.echo("Error: Session ID is required for this operation")
        return
    
    # Get the session
    session = team_manager.get_session(session_id)
    if not session:
        click.echo(f"Error: Session '{session_id}' not found")
        return
    
    # Add user to session (if not already added)
    if not session.get_users().get(user_id):
        session.add_user(user_id, user_name)
        click.echo(f"You ({user_name}) have joined the session")
    
    # Send a message if provided
    if send_message:
        if session.send_message(user_id, send_message):
            click.echo("Message sent")
        else:
            click.echo("Error: Failed to send message")
    
    # Get chat history if requested
    if get_history:
        history = session.get_chat_history()
        if history:
            click.echo("Chat history:")
            for msg in history:
                click.echo(f"[{msg['timestamp']}] {msg['user_name']}: {msg['message']}")
        else:
            click.echo("No messages in history")
    
    # Get shared context if requested
    if get_context:
        context = session.get_shared_context()
        if context:
            click.echo("Shared context:")
            click.echo(json.dumps(context, indent=2))
        else:
            click.echo("No shared context")
    
    # Set context if provided
    if set_context:
        key, value = set_context
        # Try to parse value as JSON, fallback to string
        try:
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            parsed_value = value
        
        if session.update_context(user_id, key, parsed_value):
            click.echo(f"Context updated: {key} = {value}")
        else:
            click.echo("Error: Failed to update context")

if __name__ == "__main__":
    team()