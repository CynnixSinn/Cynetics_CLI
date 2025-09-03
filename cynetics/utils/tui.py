from rich.console import Console
from rich.panel import Panel

def show_welcome_message():
    """Display a welcome message using Rich."""
    console = Console()
    console.print(Panel.fit("[bold blue]Welcome to Cynetics CLI![/bold blue]\n[green]The next-generation AI-driven command-line tool.[/green]"))