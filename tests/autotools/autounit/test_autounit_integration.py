import pytest
from unittest.mock import patch
from click.testing import CliRunner
from autotools.cli import autounit

# FIXTURES

@pytest.fixture
def runner():
    return CliRunner()

# HELPER FUNCTIONS

def assert_success(result, expected_in_output=None):
    assert result.exit_code == 0
    if expected_in_output:
        assert expected_in_output in result.output

def assert_error(result, expected_in_output=None):
    assert result.exit_code != 0
    if expected_in_output:
        assert expected_in_output in result.output

# TEST FOR BASIC CLI FUNCTIONALITY - LENGTH
@pytest.mark.parametrize("value,from_unit,to_unit,expected_in_output", [ ("100", "meter", "feet", "feet"), ("1", "kilometer", "mile", "mile"), ("1", "inch", "centimeter", "centimeter")])
def test_autounit_cli_length_conversions(runner, value, from_unit, to_unit, expected_in_output):
    result = runner.invoke(autounit, [value, from_unit, to_unit])
    assert_success(result, expected_in_output)

# TEST FOR BASIC CLI FUNCTIONALITY - VOLUME
@pytest.mark.parametrize("value,from_unit,to_unit,expected_in_output", [("10", "liter", "gallon", "gallon"), ("1", "gallon", "liter", "liter"), ("100", "milliliter", "fluid_ounce", "fluid_ounce")])
def test_autounit_cli_volume_conversions(runner, value, from_unit, to_unit, expected_in_output):
    result = runner.invoke(autounit, [value, from_unit, to_unit])
    assert_success(result, expected_in_output)

# TEST FOR BASIC CLI FUNCTIONALITY - WEIGHT
@pytest.mark.parametrize("value,from_unit,to_unit,expected_in_output", [("50", "kilogram", "pound", "pound"), ("100", "pound", "kilogram", "kilogram"), ("100", "gram", "ounce", "ounce")])
def test_autounit_cli_weight_conversions(runner, value, from_unit, to_unit, expected_in_output):
    result = runner.invoke(autounit, [value, from_unit, to_unit])
    assert_success(result, expected_in_output)

# TEST FOR BASIC CLI FUNCTIONALITY - TEMPERATURE
@pytest.mark.parametrize("value,from_unit,to_unit,expected_in_output", [("25", "celsius", "fahrenheit", "fahrenheit"), ("77", "fahrenheit", "celsius", "celsius"), ("0", "celsius", "kelvin", "kelvin")])
def test_autounit_cli_temperature_conversions(runner, value, from_unit, to_unit, expected_in_output):
    result = runner.invoke(autounit, [value, from_unit, to_unit])
    assert_success(result, expected_in_output)

# TEST FOR CLI WITH NUMERIC VALUES WITH COMMAS
def test_autounit_cli_with_commas(runner):
    result = runner.invoke(autounit, ["1,000", "meter", "feet"])
    assert_success(result, "feet")

# TEST FOR CLI WITH WHITESPACE
def test_autounit_cli_with_whitespace(runner):
    result = runner.invoke(autounit, ["  100  ", "meter", "feet"])
    assert_success(result, "feet")

# TEST FOR CLI ERROR - MISSING ARGUMENTS
def test_autounit_cli_missing_args(runner):
    result = runner.invoke(autounit, ["100", "meter"])
    assert_error(result)

# TEST FOR CLI ERROR - INVALID VALUE
def test_autounit_cli_invalid_value(runner):
    result = runner.invoke(autounit, ["invalid", "meter", "feet"])
    assert_error(result, "ERROR")

# TEST FOR CLI ERROR - INCOMPATIBLE UNITS
def test_autounit_cli_incompatible_units(runner):
    result = runner.invoke(autounit, ["100", "meter", "liter"])
    assert_error(result, "ERROR")

# TEST FOR CLI ERROR - INVALID UNIT
def test_autounit_cli_invalid_unit(runner):
    result = runner.invoke(autounit, ["100", "invalid_unit", "feet"])
    assert_error(result, "ERROR")

# TEST FOR CLI HELP
def test_autounit_cli_help(runner):
    result = runner.invoke(autounit, ["--help"])
    assert_success(result)
    assert "CONVERTS MEASUREMENT UNITS" in result.output or "converts measurement units" in result.output.lower()

# TEST FOR CLI WITH ZERO VALUE
def test_autounit_cli_zero_value(runner):
    result = runner.invoke(autounit, ["0", "meter", "feet"])
    assert_success(result)
    assert "0" in result.output or "feet" in result.output

# TEST FOR CLI WITH NEGATIVE VALUE
def test_autounit_cli_negative_value(runner):
    result = runner.invoke(autounit, ["--", "-10", "celsius", "fahrenheit"])
    assert_success(result)
    assert "fahrenheit" in result.output

# TEST FOR CLI WITH LARGE VALUE
def test_autounit_cli_large_value(runner):
    result = runner.invoke(autounit, ["1000000", "meter", "kilometer"])
    assert_success(result)
    assert "kilometer" in result.output

# TEST FOR CLI WITH SMALL VALUE
def test_autounit_cli_small_value(runner):
    result = runner.invoke(autounit, ["0.001", "meter", "millimeter"])
    assert_success(result)
    assert "millimeter" in result.output

# TEST FOR CLI ROUND-TRIP CONVERSION
def test_autounit_cli_round_trip(runner):
    result1 = runner.invoke(autounit, ["100", "meter", "feet"])
    assert_success(result1)
    feet_value = result1.output.strip().split()[0]
    result2 = runner.invoke(autounit, [feet_value, "feet", "meter"])
    assert_success(result2)
    assert "meter" in result2.output

# TEST FOR CLI WITH UPDATE MESSAGE
@patch('autotools.autounit.commands.check_for_updates')
def test_autounit_cli_with_update(mock_updates, runner):
    mock_updates.return_value = "Update available: v1.0.0"
    result = runner.invoke(autounit, ["100", "meter", "feet"])
    assert_success(result, "feet")
    assert "Update available" in result.output

# TEST FOR CLI WITH UNEXPECTED EXCEPTION
@patch('autotools.autounit.commands.autounit_convert')
def test_autounit_cli_unexpected_error(mock_convert, runner):
    mock_convert.side_effect = RuntimeError("Unexpected error")
    result = runner.invoke(autounit, ["100", "meter", "feet"])
    assert_error(result, "UNEXPECTED ERROR")

# TEST FOR CLI WITH DIFFERENT UNIT FORMATS
@pytest.mark.parametrize("from_unit,to_unit", [("m", "ft"), ("km", "mi"), ("kg", "lb")])
def test_autounit_cli_unit_aliases(runner, from_unit, to_unit):
    result = runner.invoke(autounit, ["1", from_unit, to_unit])
    assert_success(result)
