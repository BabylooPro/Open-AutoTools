import click
from .core import autolower_transform
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
@click.argument('text', nargs=-1)
def autolower(text):
    """Convert text to lowercase."""
    with LoadingAnimation():
        result = autolower_transform(" ".join(text))
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
