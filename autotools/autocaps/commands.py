import click
from .core import autocaps_transform
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# CLI COMMAND TO TRANSFORM TEXT TO UPPERCASE
@click.command()
@click.argument('text', nargs=-1)
def autocaps(text):
    with LoadingAnimation(): result = autocaps_transform(" ".join(text))
    click.echo(result)
    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg) 
