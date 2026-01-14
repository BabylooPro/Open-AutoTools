import pytest
from unittest.mock import patch
from click.testing import CliRunner
from autotools.cli import autocolor

# FIXTURES

@pytest.fixture
def runner():
    return CliRunner()

# HELPER FUNCTIONS

def invoke_autocolor(runner, args, format_option=None):
    cmd_args = list(args)
    if format_option:
        cmd_args.extend(["--format", format_option])
    return runner.invoke(autocolor, cmd_args)

def assert_success(result, expected_in_output=None):
    assert result.exit_code == 0
    if expected_in_output: assert expected_in_output in result.output

def assert_error(result, expected_in_output=None):
    assert result.exit_code != 0
    if expected_in_output: assert expected_in_output in result.output

# INTEGRATION TESTS

# TEST FOR BASIC CLI FUNCTIONALITY WITH DIFFERENT INPUT FORMATS
@pytest.mark.parametrize("color_input,expected_in_output", [
    ("#FF5733", "#FF5733"),
    ("rgb(255, 87, 51)", "#FF5733"),
    ("hsl(9, 100%, 60%)", "#"),
])
def test_autocolor_cli_basic_formats(runner, color_input, expected_in_output):
    result = invoke_autocolor(runner, [color_input])
    assert_success(result, expected_in_output)
    if expected_in_output == "#": assert result.output.strip().startswith("#")

# TEST FOR CLI WITH FORMAT OPTION
@pytest.mark.parametrize("color_input,format_option,expected_in_output", [
    ("#FF5733", "rgb", "rgb(255, 87, 51)"),
    ("rgb(255, 87, 51)", "hsl", "hsl("),
    ("#FF5733", "rgba", "rgba(255, 87, 51"),
    ("#FF5733", "hsla", "hsla("),
    ("#FF5733", "RGB", "rgb("),
])
def test_autocolor_cli_format_options(runner, color_input, format_option, expected_in_output):
    result = invoke_autocolor(runner, [color_input], format_option)
    assert_success(result, expected_in_output)

# TEST FOR CLI WITH SHORT FORMAT OPTION
def test_autocolor_cli_format_short(runner):
    result = runner.invoke(autocolor, ["#FF5733", "-f", "rgb"])
    assert_success(result, "rgb(255, 87, 51)")

# TEST FOR CLI WITH MULTIPLE ARGUMENTS
def test_autocolor_cli_multiple_args(runner):
    result = runner.invoke(autocolor, ["rgb(255,", "87,", "51)"])
    assert_success(result, "#FF5733")

# TEST FOR CLI WITH QUOTED COLOR (QUOTES ARE PASSED AS PART OF STRING)
def test_autocolor_cli_quoted(runner):
    result = invoke_autocolor(runner, ['"#FF5733"'])
    assert_error(result)

# TEST FOR CLI WITH DIFFERENT HEX/RGBA/HSLA INPUTS
@pytest.mark.parametrize("color_input", [
    "rgba(255, 87, 51, 1.0)",
    "hsla(9, 100%, 60%, 1.0)",
    "#F73",
    "#FF5733FF",
])
def test_autocolor_cli_various_inputs(runner, color_input):
    result = invoke_autocolor(runner, [color_input])
    assert_success(result)
    assert result.output.strip().startswith("#")

# TEST FOR CLI ERROR - NO ARGUMENTS
def test_autocolor_cli_no_args(runner):
    result = invoke_autocolor(runner, [])
    assert result.exit_code == 0
    assert "ERROR" in result.output or "COLOR ARGUMENT IS REQUIRED" in result.output

# TEST FOR CLI ERROR - INVALID COLOR FORMATS
@pytest.mark.parametrize("invalid_color", [
    "invalid",
    "#GGGGGG",
    "rgb(255, 87)",
    "hsl(9, 100%)",
])
def test_autocolor_cli_invalid_formats(runner, invalid_color):
    result = invoke_autocolor(runner, [invalid_color])
    assert_error(result, "ERROR")

# TEST FOR CLI WITH WHITESPACE
def test_autocolor_cli_whitespace(runner):
    result = invoke_autocolor(runner, ["  #FF5733  "])
    assert_success(result, "#FF5733")

# TEST FOR CLI HELP
def test_autocolor_cli_help(runner):
    result = runner.invoke(autocolor, ["--help"])
    assert_success(result)
    assert "CONVERTS COLOR CODES" in result.output or "converts color codes" in result.output.lower()

# TEST FOR CLI WITH EMPTY STRING
def test_autocolor_cli_empty_string(runner):
    result = invoke_autocolor(runner, [""])
    assert_error(result)

# TEST FOR CLI ROUND-TRIP CONVERSION
def test_autocolor_cli_round_trip(runner):
    result1 = invoke_autocolor(runner, ["#FF5733"], "rgb")
    assert_success(result1)
    rgb_output = result1.output.strip()
    result2 = invoke_autocolor(runner, [rgb_output], "hex")
    assert_success(result2, "#FF5733")

# TEST FOR CLI WITH SPECIAL COLORS
@pytest.mark.parametrize("color_input,expected_in_output", [
    ("#000000", "#000000"),
    ("#FFFFFF", "#FFFFFF"),
])
def test_autocolor_cli_special_colors(runner, color_input, expected_in_output):
    result = invoke_autocolor(runner, [color_input])
    assert_success(result, expected_in_output)

# TEST FOR CLI WITH DIFFERENT HEX CASE VARIATIONS
@pytest.mark.parametrize("color_input", [
    "#ff5733",
    "#Ff5733",
])
def test_autocolor_cli_hex_case_variations(runner, color_input):
    result = invoke_autocolor(runner, [color_input])
    assert_success(result)
    assert result.output.strip().startswith("#")

# TEST FOR CLI WITH UPDATE MESSAGE
@patch('autotools.autocolor.commands.check_for_updates')
def test_autocolor_cli_with_update(mock_updates, runner):
    mock_updates.return_value = "Update available: v1.0.0"
    result = invoke_autocolor(runner, ["#FF5733"])
    assert_success(result, "#FF5733")
    assert "Update available" in result.output

# TEST FOR CLI WITH UNEXPECTED EXCEPTION
@patch('autotools.autocolor.commands.autocolor_convert')
def test_autocolor_cli_unexpected_error(mock_convert, runner):
    mock_convert.side_effect = RuntimeError("Unexpected error")
    result = invoke_autocolor(runner, ["#FF5733"])
    assert_error(result, "UNEXPECTED ERROR")
