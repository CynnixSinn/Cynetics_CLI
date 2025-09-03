import click

@click.command()
def model_manager():
    """Manage model providers."""
    click.echo("Model manager command is working!")

if __name__ == "__main__":
    model_manager()