import pytest
import os
import json
from unittest.mock import patch
from click.testing import CliRunner
from autotools.cli import autoconvert

# INTEGRATION TESTS

# FIXTURE FOR CLI RUNNER
@pytest.fixture
def cli_runner():
    return CliRunner()

# TEST BASIC COMMANDS FUNCTIONALITY - TEXT TO JSON
def test_autoconvert_cli_text_to_json(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "hello world", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["text"] == "hello world"

# TEST COMMANDS TEXT TO XML
def test_autoconvert_cli_text_to_xml(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test content", mode="w")
    output_file = os.path.join(temp_dir, "output.xml")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert os.path.exists(output_file)

# TEST COMMANDS JSON TO TEXT
def test_autoconvert_cli_json_to_text(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.json", json.dumps({"text": "hello world"}), mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "hello world" in content

# TEST COMMANDS WITH INPUT TYPE OPTION
def test_autoconvert_cli_with_input_type(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file, "--input-type", "text"])
    assert result.exit_code == 0

# TEST COMMANDS WITH OUTPUT TYPE OPTION
def test_autoconvert_cli_with_output_type(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file, "--output-type", "text"])
    assert result.exit_code == 0

# TEST COMMANDS WITH FORMAT OPTION
def test_autoconvert_cli_with_format(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output")
    expected_output = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file, "--format", "json"])
    assert result.exit_code == 0
    assert os.path.exists(expected_output)

# TEST COMMANDS WITH NONEXISTENT FILE
def test_autoconvert_cli_nonexistent_file(cli_runner, temp_dir):
    input_file = os.path.join(temp_dir, "nonexistent.txt")
    output_file = os.path.join(temp_dir, "output.txt")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code != 0
    assert "FILE NOT FOUND" in result.output.upper() or "NOT FOUND" in result.output.upper()

# TEST COMMANDS HELP
def test_autoconvert_cli_help(cli_runner):
    result = cli_runner.invoke(autoconvert, ["--help"])
    assert result.exit_code == 0
    assert "CONVERTS FILES" in result.output.upper() or "autoconvert" in result.output.lower()

# TEST COMMANDS TEXT TO HTML
def test_autoconvert_cli_text_to_html(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "hello world", mode="w")
    output_file = os.path.join(temp_dir, "output.html")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "<html>" in content
        assert "hello world" in content

# TEST COMMANDS CREATES OUTPUT DIRECTORY
def test_autoconvert_cli_creates_directory(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "subdir", "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert os.path.exists(output_file)

# TEST COMMANDS WITH FORMAT WHEN FILE ALREADY HAS EXTENSION
def test_autoconvert_cli_format_already_has_extension(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file, "--format", "json"])
    assert result.exit_code == 0
    assert os.path.exists(output_file)

# TEST COMMANDS WITH FORMAT AND OUTPUT TYPE
def test_autoconvert_cli_format_with_output_type(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file, "--format", "json", "--output-type", "text"])
    assert result.exit_code == 0

# TEST COMMANDS CONVERSION FAILURE
def test_autoconvert_cli_conversion_failure(cli_runner, temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.jpg")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code != 0

# TEST COMMANDS WITH IMPORT ERROR (MOCK)
def test_autoconvert_cli_import_error(monkeypatch, cli_runner, temp_dir, create_test_file):
    def mock_convert_file(*args, **kwargs): raise ImportError("MOCKED IMPORT ERROR")
    monkeypatch.setattr("autotools.autoconvert.commands.convert_file", mock_convert_file)
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code != 0
    assert "IMPORT ERROR" in result.output.upper() or "ERROR" in result.output.upper()

# TEST COMMANDS WITH GENERAL EXCEPTION
@patch('autotools.autoconvert.commands.convert_file')
def test_autoconvert_cli_general_exception(mock_convert_file, cli_runner, temp_dir, create_test_file):
    mock_convert_file.side_effect = Exception("MOCKED GENERAL ERROR")
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")

    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code != 0
    assert "ERROR" in result.output.upper()

# TEST COMMANDS WITH UPDATE MESSAGE
@patch('autotools.autoconvert.commands.check_for_updates')
@patch('autotools.autoconvert.commands.convert_file')
def test_autoconvert_cli_with_update_message(mock_convert_file, mock_updates, cli_runner, temp_dir, create_test_file):
    mock_convert_file.return_value = (True, "SUCCESS")
    mock_updates.return_value = "Update available: v2.0.0"
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")

    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code == 0
    assert "Update available" in result.output

# TEST COMMANDS CONVERSION FAILURE (SUCCESS=FALSE)
@patch('autotools.autoconvert.commands.convert_file')
def test_autoconvert_cli_conversion_failure_success_false(mock_convert_file, cli_runner, temp_dir, create_test_file):
    mock_convert_file.return_value = (False, "CONVERSION FAILED")
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")

    result = cli_runner.invoke(autoconvert, [input_file, output_file])
    assert result.exit_code != 0
    assert "CONVERSION FAILED" in result.output.upper()
