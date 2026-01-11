import pytest
from click.testing import CliRunner
from autotools.cli import autolower

# INTEGRATION TESTS

# TEST FOR BASIC CLI FUNCTIONALITY
def test_autolower_cli_basic():
    runner = CliRunner()
    result = runner.invoke(autolower, ["HELLO WORLD"])
    assert result.exit_code == 0
    assert "hello world" in result.output

# TEST FOR EMPTY INPUT
def test_autolower_cli_empty():
    runner = CliRunner()
    result = runner.invoke(autolower, [""])
    assert result.exit_code == 0
    assert "" in result.output

# TEST FOR SPECIAL CHARACTERS
def test_autolower_cli_special_chars():
    runner = CliRunner()
    result = runner.invoke(autolower, ["HELLO@WORLD.COM"])
    assert result.exit_code == 0
    assert "hello@world.com" in result.output

# TEST FOR UNICODE CHARACTERS
def test_autolower_cli_unicode():
    runner = CliRunner()
    result = runner.invoke(autolower, ["HÉLLO WÖRLD"])
    assert result.exit_code == 0
    assert "héllo wörld" in result.output

# TEST FOR MULTIPLE ARGUMENTS
def test_autolower_cli_multiple_args():
    runner = CliRunner()
    result = runner.invoke(autolower, ["HELLO", "WORLD"])
    assert result.exit_code == 0
    assert "hello" in result.output 
