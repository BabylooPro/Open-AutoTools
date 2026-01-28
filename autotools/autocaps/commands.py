import click
from .core import autocaps_transform
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Text'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'basic', 'args': ['test', 'with', 'multiple', 'words']},
    {'name': 'special', 'args': ['special', 'chars:', '!@#$%^&*()']},
    {'name': 'mixed', 'args': ['123', 'mixed', 'WITH', 'lowercase', '456']},
    {'name': 'unicode', 'args': ['áccênts', 'ànd', 'émojis', '🚀', '⭐']},
]

# CLI COMMAND TO TRANSFORM TEXT TO UPPERCASE
@click.command()
@click.argument('text', nargs=-1)
def autocaps(text):
    """
        TRANSFORMS TEXT TO UPPERCASE.

        \b
        EXAMPLES:
            autocaps hello world
            autocaps "this is a test"
            echo "text" | autocaps
    """

    with LoadingAnimation(): result = autocaps_transform(" ".join(text))
    click.echo(result)
    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg) 
