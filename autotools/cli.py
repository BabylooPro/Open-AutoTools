import os
import click
from autotools.autocaps.core import autocaps_transform
from autotools.autocorrect.core import autocorrect_text
from dotenv import load_dotenv


load_dotenv()  # LOAD ENVIRONMENT VARIABLES


# CLI FUNCTION DEFINITION
@click.group()
def cli():
    # THIS FUNCTION IS NOT USED, BUT IT IS NEEDED TO DEFINE CLI
    pass


# AUTOCAPS COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autocaps(text):
    result = autocaps_transform(text)
    click.echo(result)


# AUTOCORRECT COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autocorrect(text):
    result = autocorrect_text(text)
    click.echo(result)


# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()
