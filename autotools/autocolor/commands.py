import click
from .core import autocolor_convert
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'hex-default', 'args': ['#FF5733']},
    {'name': 'hex-rgb', 'args': ['#FF5733', '--format', 'rgb']},
    {'name': 'rgb-hsl', 'args': ['rgb(255,87,51)', '--format', 'hsl']},
    {'name': 'hsl-rgba', 'args': ['hsl(9,100%,60%)', '--format', 'rgba']},
]

# CLI COMMAND TO CONVERT COLOR CODES BETWEEN FORMATS
@click.command()
@click.argument('color', nargs=-1)
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['hex', 'rgb', 'rgba', 'hsl', 'hsla'], case_sensitive=False),
              default='hex', help='OUTPUT FORMAT (hex, rgb, rgba, hsl, hsla)')
def autocolor(color, output_format):
    """
        CONVERTS COLOR CODES BETWEEN DIFFERENT FORMATS.

        \b
        SUPPORTS INPUT FORMATS:
            - HEX: #RRGGBB, #RRGGBBAA, #RGB
            - RGB: rgb(r, g, b)
            - RGBA: rgba(r, g, b, a)
            - HSL: hsl(h, s%, l%)
            - HSLA: hsla(h, s%, l%, a)

        \b
        EXAMPLES:
            autocolor "#FF5733"
            autocolor "rgb(255, 87, 51)" --format hsl
            autocolor "hsl(9, 100%, 60%)" --format hex
            autocolor "#F73" --format rgba
    """

    if not color:
        click.echo(click.style("ERROR: COLOR ARGUMENT IS REQUIRED", fg='red'), err=True)
        click.echo(click.get_current_context().get_help())
        return

    color_input = " ".join(color)
    
    try:
        with LoadingAnimation(): result = autocolor_convert(color_input, output_format)
        click.echo(result)
        update_msg = check_for_updates()
        if update_msg: click.echo(update_msg)
    except ValueError as e:
        click.echo(click.style(f"ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"UNEXPECTED ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
