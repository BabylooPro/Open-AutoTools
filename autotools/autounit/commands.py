import click
from .core import autounit_convert
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Conversion'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'length-meters-feet', 'args': ['100', 'meter', 'feet']},
    {'name': 'volume-liters-gallons', 'args': ['10', 'liter', 'gallon']},
    {'name': 'weight-kg-lb', 'args': ['50', 'kilogram', 'pound']},
    {'name': 'temperature-celsius-fahrenheit', 'args': ['25', 'celsius', 'fahrenheit']},
]

# CLI COMMAND TO CONVERT MEASUREMENT UNITS
@click.command()
@click.argument('value', nargs=1)
@click.argument('from_unit', nargs=1)
@click.argument('to_unit', nargs=1)
def autounit(value, from_unit, to_unit):
    """
        CONVERTS MEASUREMENT UNITS (EXAMPLE: METERS TO FEET, LITERS TO GALLONS).

        \b
        SUPPORTS VARIOUS UNIT CATEGORIES:
            - LENGTH: meter, feet, inch, kilometer, mile, centimeter, millimeter, yard
            - VOLUME: liter, gallon, milliliter, fluid_ounce, cup, pint, quart
            - WEIGHT: kilogram, pound, gram, ounce, ton, stone
            - TEMPERATURE: celsius, fahrenheit, kelvin
            - AND MANY MORE...

        \b
        EXAMPLES:
            autounit 100 meter feet
            autounit 10 liter gallon
            autounit 50 kilogram pound
            autounit 25 celsius fahrenheit
            autounit 5 kilometer mile
    """

    try:
        with LoadingAnimation():
            result = autounit_convert(value, from_unit, to_unit)
        click.echo(result)
        update_msg = check_for_updates()
        if update_msg:
            click.echo(update_msg)
    except ValueError as e:
        click.echo(click.style(f"ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"UNEXPECTED ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
