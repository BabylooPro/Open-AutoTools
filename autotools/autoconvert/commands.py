import os
import click
from pathlib import Path
from .core import convert_file, detect_file_type
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# CLI COMMAND TO CONVERT FILES BETWEEN DIFFERENT FORMATS
@click.command()
@click.argument('input_file', type=click.Path())
@click.argument('output_file', type=click.Path())
@click.option('--input-type', '-i', help='FORCE INPUT FILE TYPE (text/image/audio/video)')
@click.option('--output-type', '-o', help='FORCE OUTPUT FILE TYPE (text/image/audio/video)')
@click.option('--format', '-f', help='OUTPUT FORMAT (OVERRIDES OUTPUT FILE EXTENSION)')
def autoconvert(input_file, output_file, input_type, output_type, format):
    """
        CONVERTS FILES BETWEEN DIFFERENT FORMATS.

        \b
        SUPPORTS:
            - TEXT: txt, md, markdown, json, xml, html, htm, csv
            - IMAGES: jpg, jpeg, png, gif, webp, bmp, tiff, tif, ico, svg
            - AUDIO: mp3, wav, ogg, flac, aac, m4a, wma, opus
            - VIDEO: mp4, avi, mov, mkv, wmv, flv, webm, m4v

        \b
        EXAMPLES:
            autoconvert input.txt output.json
            autoconvert image.jpg image.png
            autoconvert audio.mp3 audio.wav
            autoconvert video.mp4 video.avi
    """

    # TRY TO CONVERT FILE
    # - CHECK IF INPUT FILE EXISTS, OTHERWISE FAIL
    # - HANDLE --FORMAT: UPDATE OUTPUT NAME/EXT, DETECT OUTPUT TYPE IF UNSET
    # - MAKE OUTPUT DIRECTORY IF IT DOESN'T EXIST, RUN CONVERT WITH LOADING SPINNER
    # - SHOW RESULT, PRINT UPDATE NOTICE
    try:
        if not os.path.exists(input_file): raise FileNotFoundError(f"INPUT FILE NOT FOUND: {input_file}")

        if format:
            output_path = Path(output_file)
            if not output_file.endswith(f'.{format}'): output_file = str(output_path.with_suffix(f'.{format}'))
            if output_type is None: output_type = detect_file_type(output_file)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with LoadingAnimation(): success, message = convert_file(input_file, output_file, input_type, output_type)
        
        if success:
            click.echo(click.style(f"✓ {message}", fg='green'))
            click.echo(click.style(f"OUTPUT: {output_file}", fg='blue'))
        else:
            click.echo(click.style(f"✗ {message}", fg='red'), err=True)
            raise click.Abort()
        
        update_msg = check_for_updates()
        if update_msg: click.echo(update_msg)

    except FileNotFoundError as e:
        click.echo(click.style(f"✗ FILE NOT FOUND: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except ImportError as e:
        click.echo(click.style(f"✗ {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"✗ ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
