import click

@click.command()
def test_cmd():
    """A simple test command."""
    click.echo("Test command is working!")

if __name__ == "__main__":
    test_cmd()