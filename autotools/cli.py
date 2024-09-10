from dotenv import load_dotenv
load_dotenv() # LOAD ENVIRONMENT VARIABLES BEFORE IMPORTING OTHER MODULES BECAUSE CERTAIN MODULES DEPEND ON ENVIRONMENT VARIABLES

import os
import click
from autotools.autotranslate.core import autotranslate_text, autotranslate_supported_languages
from autotools.autocorrect.core import autocorrect_text
from autotools.autocaps.core import autocaps_transform
from autotools.downloader.core import download_youtube_video, download_file

# CLI FUNCTION DEFINITION
@click.group()
def cli():
    """Autotools is a set of tools for text capitalization, correction and translation."""
    pass

# AUTOTOOLS COMMAND LINE INTERFACE FUNCTION DEFINITION FOR SHOW HELP MESSAGE
@cli.command()
def autotools():
    return

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

# AUTOTRANSLATE COMMAND LINE INTERFACE FUNCTION DEFINITION
VALID_LANGUAGES = autotranslate_supported_languages() # VALID LANGUAGES FOR TRANSLATION
@cli.command()
@click.argument('text')
#@click.option('--from', 'language_origin', required=True, help="Language of the source text")
@click.option('--to', 'language_target', required=True, help="Target language for translation")
def autotranslate(text, language_target):
    if language_target not in VALID_LANGUAGES:
        click.secho(f"Language code '{
                    language_target}' is not supported.", fg='red')
        return

    # CALL TO AUTOTRANSLATE FUNCTION
    result = autotranslate_text(
        text, language_target=language_target)
    click.secho(result)

# AUTODOWNLOAD COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('url')
@click.option('--format', type=click.Choice(['mp4', 'mp3'], case_sensitive=False), default='mp4', help='Output file format (mp4 or mp3)')
@click.option('--quality', type=click.Choice(['best', '1440p', '1080p', '720p', '480p', '360p', '240p'], case_sensitive=False), default='best', help='"Video quality (mp4 only)"')
def autodownload(url, format, quality):
    if "youtube.com" in url or "youtu.be" in url:
        download_youtube_video(url, format, quality)
    else:
        download_file(url)

# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()
