import click
from .core import autolower_transform
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Text'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'basic', 'args': ['TEST', 'WITH', 'MULTIPLE', 'WORDS']},
    {'name': 'special', 'args': ['SPECIAL', 'CHARS:', '!@#$%^&*()']},
    {'name': 'mixed', 'args': ['123', 'MIXED', 'with', 'UPPERCASE', '456']},
    {'name': 'unicode', 'args': ['ÁCCÊNTS', 'ÀND', 'ÉMOJIS', '🚀', '⭐']},
]

# CLI COMMAND TO TRANSFORM TEXT TO LOWERCASE
@click.command()
@click.argument('text', nargs=-1)
def autolower(text):
    """
        TRANSFORMS TEXT TO LOWERCASE.

        \b
        EXAMPLES:
            autolower HELLO WORLD
            autolower "THIS IS A TEST"
            echo "TEXT" | autolower
    """

    with LoadingAnimation(): result = autolower_transform(" ".join(text))
    click.echo(result)
    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg) 
