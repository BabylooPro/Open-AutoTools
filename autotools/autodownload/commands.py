import click
import sys
from .core import download_youtube_video, download_file, validate_youtube_url
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
@click.argument('url')
@click.option('--format', '-f', type=click.Choice(['mp4', 'mp3'], case_sensitive=False), 
              default='mp4', help='Output file format (mp4 for video, mp3 for audio)')
@click.option('--quality', '-q', type=click.Choice(['best', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p'], 
              case_sensitive=False), default='best', help='Video quality (mp4 only)')
def autodownload(url, format, quality):
    """Download videos from YouTube or files from any URL.
    
    Supports YouTube video download with quality selection and format conversion (mp4/mp3).
    
    For non-YouTube URLs, downloads the file directly."""
    
    loading = LoadingAnimation()

    if "youtube.com" in url or "youtu.be" in url:
        with loading:
            if not validate_youtube_url(url):
                click.echo("Invalid YouTube URL", err=True)
                sys.exit(1)
        
        if not download_youtube_video(url, format, quality):
            sys.exit(1)
    else:
        with loading:
            if not download_file(url):
                sys.exit(1)
        
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
