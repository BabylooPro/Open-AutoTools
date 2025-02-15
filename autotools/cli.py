import os
import click
from autotools.autocaps.core import autocaps_transform
from autotools.downloader.core import download_youtube_video, download_file

# CLI FUNCTION DEFINITION
@click.group()
def cli():
    """Autotools is a set of tools for text capitalization and file downloading."""
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
