import pytest
from click.testing import CliRunner
from autotools.cli import autopassword

# INTEGRATION TESTS

# TEST FOR DEFAULT PASSWORD GENERATION
def test_autopassword_cli_default():
    runner = CliRunner()
    result = runner.invoke(autopassword)
    assert result.exit_code == 0
    assert "Generated Password:" in result.output
    assert len(result.output.split("Generated Password:")[1].strip().split()[0]) == 12

# TEST FOR PASSWORD GENERATION WITH CUSTOM LENGTH
def test_autopassword_cli_custom_length():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--length", "16"])
    assert result.exit_code == 0
    assert len(result.output.split("Generated Password:")[1].strip().split()[0]) == 16

# TEST FOR PASSWORD GENERATION WITHOUT SPECIAL CHARACTERS
def test_autopassword_cli_no_special():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--no-special"])
    assert result.exit_code == 0
    password = result.output.split("Generated Password:")[1].strip().split()[0]
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# TEST FOR PASSWORD STRENGTH ANALYSIS
def test_autopassword_cli_analyze():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--analyze"])
    assert result.exit_code == 0
    assert "Strength Analysis:" in result.output
    assert "Score:" in result.output
    assert "Strength:" in result.output

# TEST FOR ENCRYPTION KEY GENERATION
def test_autopassword_cli_gen_key():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--gen-key"])
    assert result.exit_code == 0
    assert "Encryption Key:" in result.output
    key = result.output.split("Encryption Key:")[1].strip()
    assert len(key) == 44

# TEST FOR KEY GENERATION FROM PASSWORD
def test_autopassword_cli_password_key():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--password-key", "testpassword123"])
    assert result.exit_code == 0
    assert "Derived Key:" in result.output
    assert "Salt:" in result.output

# TEST FOR HELP DISPLAY
def test_autopassword_cli_help():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--length" in result.output
    assert "--analyze" in result.output
    assert "--gen-key" in result.output

# TEST FOR PASSWORD KEY WITH ANALYZE AND SUGGESTIONS
def test_autopassword_cli_password_key_with_analyze():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--password-key", "weak", "--analyze"])
    assert result.exit_code == 0
    assert "Derived Key:" in result.output
    assert "Analyzing source password:" in result.output
    assert "Analyzing generated key:" in result.output
    assert "Suggestions for improvement:" in result.output or "Strength Analysis:" in result.output

# TEST FOR PASSWORD GENERATION WITH SUGGESTIONS
def test_autopassword_cli_with_suggestions():
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--length", "6", "--analyze"])
    assert result.exit_code == 0
    assert "Strength Analysis:" in result.output 
