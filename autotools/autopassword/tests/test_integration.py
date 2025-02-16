import pytest
from click.testing import CliRunner
from autotools.cli import autopassword

# INTEGRATION TESTS

# TEST FOR DEFAULT PASSWORD GENERATION
def test_autopassword_cli_default():
    """TEST DEFAULT PASSWORD GENERATION"""
    runner = CliRunner()
    result = runner.invoke(autopassword)
    assert result.exit_code == 0
    assert "Generated Password:" in result.output
    assert len(result.output.split("Generated Password:")[1].strip().split()[0]) == 12

# TEST FOR PASSWORD GENERATION WITH CUSTOM LENGTH
def test_autopassword_cli_custom_length():
    """TEST PASSWORD GENERATION WITH CUSTOM LENGTH"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--length", "16"])
    assert result.exit_code == 0
    assert len(result.output.split("Generated Password:")[1].strip().split()[0]) == 16

# TEST FOR PASSWORD GENERATION WITHOUT SPECIAL CHARACTERS
def test_autopassword_cli_no_special():
    """TEST PASSWORD GENERATION WITHOUT SPECIAL CHARACTERS"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--no-special"])
    assert result.exit_code == 0
    password = result.output.split("Generated Password:")[1].strip().split()[0]
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# TEST FOR PASSWORD STRENGTH ANALYSIS
def test_autopassword_cli_analyze():
    """TEST PASSWORD STRENGTH ANALYSIS"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--analyze"])
    assert result.exit_code == 0
    assert "Strength Analysis:" in result.output
    assert "Score:" in result.output
    assert "Strength:" in result.output

# TEST FOR ENCRYPTION KEY GENERATION
def test_autopassword_cli_gen_key():
    """TEST ENCRYPTION KEY GENERATION"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--gen-key"])
    assert result.exit_code == 0
    assert "Encryption Key:" in result.output
    key = result.output.split("Encryption Key:")[1].strip()
    assert len(key) == 44  # BASE64 ENCODED 32-BYTE KEY

# TEST FOR KEY GENERATION FROM PASSWORD
def test_autopassword_cli_password_key():
    """TEST KEY GENERATION FROM PASSWORD"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--password-key", "testpassword123"])
    assert result.exit_code == 0
    assert "Derived Key:" in result.output
    assert "Salt:" in result.output

# TEST FOR HELP DISPLAY
def test_autopassword_cli_help():
    """TEST HELP DISPLAY"""
    runner = CliRunner()
    result = runner.invoke(autopassword, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--length" in result.output
    assert "--analyze" in result.output
    assert "--gen-key" in result.output 
