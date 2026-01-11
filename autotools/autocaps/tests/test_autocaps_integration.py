import pytest
from click.testing import CliRunner
from autotools.cli import autocaps

# INTEGRATION TESTS

# TEST FOR BASIC CLI FUNCTIONALITY
def test_autocaps_cli_basic():
    runner = CliRunner()
    result = runner.invoke(autocaps, ["hello world"])
    assert result.exit_code == 0
    assert "HELLO WORLD" in result.output

# TEST FOR EMPTY INPUT
def test_autocaps_cli_empty():
    runner = CliRunner()
    result = runner.invoke(autocaps, [""])
    assert result.exit_code == 0
    assert "" in result.output

# TEST FOR SPECIAL CHARACTERS
def test_autocaps_cli_special_chars():
    runner = CliRunner()
    result = runner.invoke(autocaps, ["hello@world.com"])
    assert result.exit_code == 0
    assert "HELLO@WORLD.COM" in result.output

# TEST FOR UNICODE CHARACTERS
def test_autocaps_cli_unicode():
    runner = CliRunner()
    result = runner.invoke(autocaps, ["héllo wörld"])
    assert result.exit_code == 0
    assert "HÉLLO WÖRLD" in result.output

# TEST FOR MULTIPLE ARGUMENTS
def test_autocaps_cli_multiple_args():
    runner = CliRunner()
    result = runner.invoke(autocaps, ["hello", "world"])
    assert result.exit_code == 0
    assert "HELLO" in result.output 
