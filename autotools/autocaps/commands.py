import click
from .core import autocaps_transform
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
@click.argument('text', nargs=-1)
def autocaps(text):
    """Convert text to UPPERCASE."""
    with LoadingAnimation():
        result = autocaps_transform(" ".join(text))
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
