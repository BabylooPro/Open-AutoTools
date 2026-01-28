import click
from pathlib import Path
from .core import autozip_compress
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Files'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'zip-readme', 'args': ['README.md', '--output', '/tmp/autozip-smoke.zip']},
]

# CLI COMMAND TO COMPRESS FILES AND DIRECTORIES
@click.command()
@click.argument('sources', nargs=-1, required=True)
@click.option('--output', '-o', 'output_path', required=True,
              help='OUTPUT ARCHIVE PATH (EXTENSION DETERMINES FORMAT)')
@click.option('--format', '-f', 'archive_format',
              type=click.Choice(['zip', 'tar.gz', 'tar.bz2', 'tar.xz', 'tar'], case_sensitive=False),
              help='ARCHIVE FORMAT (AUTO-DETECTED FROM OUTPUT EXTENSION IF NOT SPECIFIED)')
@click.option('--compression', '-c', 'compression_level', type=int, default=6,
              help='COMPRESSION LEVEL (0-9, DEFAULT: 6)')
def autozip(sources, output_path, archive_format, compression_level):
    """
        COMPRESSES FILES AND DIRECTORIES INTO VARIOUS ARCHIVE FORMATS.

        \b
        SUPPORTED FORMATS:
            - ZIP: .zip
            - TAR.GZ: .tar.gz, .tgz
            - TAR.BZ2: .tar.bz2, .tbz2
            - TAR.XZ: .tar.xz, .txz
            - TAR: .tar

        \b
        EXAMPLES:
            autozip file.txt dir/ -o archive.zip
            autozip file1.txt file2.txt -o backup.tar.gz --compression 9
            autozip project/ -o release.tar.bz2 --format tar.bz2
            autozip data/ -o archive.tar.xz --compression 7
    """

    # VALIDATE SOURCE PATHS
    if not sources:
        click.echo(click.style("ERROR: AT LEAST ONE SOURCE PATH IS REQUIRED", fg='red'), err=True)
        click.echo(click.get_current_context().get_help())
        return

    # VALIDATE COMPRESSION LEVEL
    if compression_level < 0 or compression_level > 9:
        click.echo(click.style("ERROR: COMPRESSION LEVEL MUST BE BETWEEN 0 AND 9", fg='red'), err=True)
        raise click.Abort()

    # COMPRESS FILES AND DIRECTORIES
    try:
        with LoadingAnimation():
            result = autozip_compress(
                list(sources),
                output_path,
                archive_format=archive_format,
                compression_level=compression_level
            )
        
        click.echo(click.style(f"SUCCESS: CREATED ARCHIVE: {result}", fg='green'))
        
        archive_size = Path(result).stat().st_size
        size_mb = archive_size / (1024 * 1024)

        if size_mb >= 1:
            click.echo(f"ARCHIVE SIZE: {size_mb:.2f} MB")
        else:
            size_kb = archive_size / 1024
            click.echo(f"ARCHIVE SIZE: {size_kb:.2f} KB")
        
        update_msg = check_for_updates()
        if update_msg: click.echo(update_msg)

    except FileNotFoundError as e:
        click.echo(click.style(f"ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except ValueError as e:
        click.echo(click.style(f"ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"UNEXPECTED ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
