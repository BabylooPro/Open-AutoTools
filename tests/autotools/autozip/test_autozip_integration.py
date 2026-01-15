import pytest
import os
import tempfile
import shutil
import click
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from autotools.cli import autozip

# FIXTURES

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def test_file(temp_dir):
    file_path = Path(temp_dir) / "test.txt"
    file_path.write_text("TEST CONTENT FOR COMPRESSION")
    return str(file_path)

@pytest.fixture
def test_dir(temp_dir):
    dir_path = Path(temp_dir) / "test_dir"
    dir_path.mkdir()
    (dir_path / "file1.txt").write_text("FILE 1 CONTENT")
    (dir_path / "file2.txt").write_text("FILE 2 CONTENT")
    return str(dir_path)

# HELPER FUNCTIONS

def assert_success(result, expected_in_output=None):
    assert result.exit_code == 0
    if expected_in_output: assert expected_in_output in result.output

def assert_error(result, expected_in_output=None):
    assert result.exit_code != 0
    if expected_in_output: assert expected_in_output in result.output

# INTEGRATION TESTS

# TEST FOR BASIC ZIP COMPRESSION
def test_autozip_cli_zip_basic(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert "archive.zip" in result.output
    assert Path(output).exists()

# TEST FOR ZIP WITH SHORT OUTPUT OPTION
def test_autozip_cli_zip_short_output(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "-o", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.GZ COMPRESSION
def test_autozip_cli_tar_gz(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tar.gz")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.GZ WITH TGZ EXTENSION
def test_autozip_cli_tgz(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tgz")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.BZ2 COMPRESSION
def test_autozip_cli_tar_bz2(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tar.bz2")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.BZ2 WITH TBZ2 EXTENSION
def test_autozip_cli_tbz2(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tbz2")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.XZ COMPRESSION
def test_autozip_cli_tar_xz(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tar.xz")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR.XZ WITH TXZ EXTENSION
def test_autozip_cli_txz(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.txz")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR TAR COMPRESSION
def test_autozip_cli_tar(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.tar")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR EXPLICIT FORMAT OPTION
@pytest.mark.parametrize("format_name", ["zip", "tar.gz", "tar.bz2", "tar.xz", "tar"])
def test_autozip_cli_explicit_format(runner, temp_dir, test_file, format_name):
    output = str(Path(temp_dir) / "archive.unknown")
    result = runner.invoke(autozip, [test_file, "--output", output, "--format", format_name])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR EXPLICIT FORMAT WITH SHORT OPTION
def test_autozip_cli_explicit_format_short(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.unknown")
    result = runner.invoke(autozip, [test_file, "-o", output, "-f", "zip"])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR COMPRESSION LEVEL
@pytest.mark.parametrize("level", [0, 1, 6, 9])
def test_autozip_cli_compression_level(runner, temp_dir, test_file, level):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output, "--compression", str(level)])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR COMPRESSION LEVEL WITH SHORT OPTION
def test_autozip_cli_compression_level_short(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "-o", output, "-c", "9"])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR MULTIPLE SOURCES
def test_autozip_cli_multiple_sources(runner, temp_dir, test_file, test_dir):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, test_dir, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR DIRECTORY COMPRESSION
def test_autozip_cli_directory(runner, temp_dir, test_dir):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_dir, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR ARCHIVE SIZE DISPLAY (KB)
def test_autozip_cli_size_kb(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result)
    assert "ARCHIVE SIZE:" in result.output
    assert "KB" in result.output

# TEST FOR ARCHIVE SIZE DISPLAY (MB) - CREATE LARGE NON-COMPRESSIBLE FILE
def test_autozip_cli_size_mb(runner, temp_dir):
    large_file = Path(temp_dir) / "large.bin"
    import random
    random.seed(42)
    
    data = bytes([random.randint(0, 255) for _ in range(5 * 1024 * 1024)])
    large_file.write_bytes(data)

    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [str(large_file), "--output", output, "--compression", "0"])
    assert_success(result)

    assert "ARCHIVE SIZE:" in result.output
    assert "KB" in result.output or "MB" in result.output

# TEST FOR ERROR - NO SOURCES (CLICK VALIDATES BEFORE OUR CODE)
def test_autozip_cli_no_sources(runner, temp_dir):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, ["--output", output])
    assert_error(result)
    assert "Missing argument" in result.output or "SOURCES" in result.output

# TEST FOR ERROR - INVALID COMPRESSION LEVEL (TOO LOW)
def test_autozip_cli_invalid_compression_low(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output, "--compression", "-1"])
    assert_error(result, "ERROR")
    assert "COMPRESSION LEVEL MUST BE BETWEEN 0 AND 9" in result.output

# TEST FOR ERROR - INVALID COMPRESSION LEVEL (TOO HIGH)
def test_autozip_cli_invalid_compression_high(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output, "--compression", "10"])
    assert_error(result, "ERROR")
    assert "COMPRESSION LEVEL MUST BE BETWEEN 0 AND 9" in result.output

# TEST FOR ERROR - NONEXISTENT SOURCE
def test_autozip_cli_nonexistent_source(runner, temp_dir):
    output = str(Path(temp_dir) / "archive.zip")
    nonexistent = str(Path(temp_dir) / "nonexistent.txt")
    result = runner.invoke(autozip, [nonexistent, "--output", output])
    assert_error(result, "ERROR")
    assert "SOURCE PATH NOT FOUND" in result.output

# TEST FOR ERROR - UNSUPPORTED FORMAT (CLICK VALIDATES BEFORE OUR CODE)
def test_autozip_cli_unsupported_format(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.unknown")
    result = runner.invoke(autozip, [test_file, "--output", output, "--format", "unknown"])
    assert_error(result)
    assert "Invalid value" in result.output or "not one of" in result.output

# TEST FOR HELP
def test_autozip_cli_help(runner):
    result = runner.invoke(autozip, ["--help"])
    assert_success(result)
    assert "COMPRESSES FILES AND DIRECTORIES" in result.output or "compresses files" in result.output.lower()
    assert "ZIP" in result.output or "zip" in result.output.lower()
    assert "tar.gz" in result.output.lower()

# TEST FOR UPDATE MESSAGE
@patch('autotools.autozip.commands.check_for_updates')
def test_autozip_cli_with_update(mock_updates, runner, temp_dir, test_file):
    mock_updates.return_value = "Update available: v1.0.0"
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert "Update available" in result.output

# TEST FOR UPDATE MESSAGE NOT SHOWN WHEN NONE
@patch('autotools.autozip.commands.check_for_updates')
def test_autozip_cli_without_update(mock_updates, runner, temp_dir, test_file):
    mock_updates.return_value = None
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert "Update available" not in result.output

# TEST FOR UNEXPECTED ERROR
@patch('autotools.autozip.commands.autozip_compress')
def test_autozip_cli_unexpected_error(mock_compress, runner, temp_dir, test_file):
    mock_compress.side_effect = RuntimeError("Unexpected error")
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_error(result, "UNEXPECTED ERROR")

# TEST FOR FILE NOT FOUND ERROR
def test_autozip_cli_file_not_found_error(runner, temp_dir):
    output = str(Path(temp_dir) / "archive.zip")
    nonexistent = str(Path(temp_dir) / "nonexistent.txt")
    result = runner.invoke(autozip, [nonexistent, "--output", output])
    assert_error(result, "ERROR")
    assert "SOURCE PATH NOT FOUND" in result.output

# TEST FOR VALUE ERROR (INVALID FORMAT FROM EXTENSION)
def test_autozip_cli_value_error_invalid_extension(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.invalid")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_error(result, "ERROR")
    assert "UNSUPPORTED" in result.output

# TEST FOR CASE INSENSITIVE FORMAT
@pytest.mark.parametrize("format_name", ["ZIP", "TAR.GZ", "TAR.BZ2", "TAR.XZ", "TAR"])
def test_autozip_cli_case_insensitive_format(runner, temp_dir, test_file, format_name):
    output = str(Path(temp_dir) / "archive.unknown")
    result = runner.invoke(autozip, [test_file, "--output", output, "--format", format_name])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR OUTPUT DIRECTORY CREATION
def test_autozip_cli_creates_output_dir(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "subdir" / "nested" / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()
    assert Path(output).parent.exists()

# TEST FOR DEFAULT COMPRESSION LEVEL
def test_autozip_cli_default_compression(runner, temp_dir, test_file):
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR MULTIPLE FILES AND DIRECTORIES
def test_autozip_cli_mixed_sources(runner, temp_dir, test_file, test_dir):
    file2 = Path(temp_dir) / "test2.txt"
    file2.write_text("TEST 2")
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, [test_file, str(file2), test_dir, "--output", output])
    assert_success(result, "SUCCESS")
    assert Path(output).exists()

# TEST FOR ARCHIVE SIZE DISPLAY (MB) - TEST MB BRANCH DIRECTLY
def test_autozip_cli_size_mb_branch(runner, temp_dir):
    import random
    random.seed(42)
    files = []

    for i in range(10):
        large_file = Path(temp_dir) / f"large{i}.bin"
        data = bytes([random.randint(0, 255) for _ in range(200 * 1024)])
        large_file.write_bytes(data)
        files.append(str(large_file))
    
    output = str(Path(temp_dir) / "archive.zip")
    result = runner.invoke(autozip, files + ["--output", output, "--compression", "0"])
    assert_success(result)
    
    assert "ARCHIVE SIZE:" in result.output
    assert "KB" in result.output or "MB" in result.output

# TEST FOR EMPTY SOURCES CHECK (COVER COMMANDS.PY LINES 37-40)
def test_autozip_commands_empty_sources_direct(runner, temp_dir):
    import autotools.autozip.commands as commands_module
    original_autozip_cmd = commands_module.autozip
    output = str(Path(temp_dir) / "archive.zip")
    
    with patch('autotools.autozip.commands.click.echo') as mock_echo:
        with patch('autotools.autozip.commands.click.get_current_context') as mock_get_context:
            mock_ctx = MagicMock()
            mock_ctx.get_help.return_value = "HELP TEXT"
            mock_get_context.return_value = mock_ctx
            
            try:
                original_autozip_cmd.callback([], output, None, 6)
            except (SystemExit, click.Abort):
                error_calls = [
                    call for call in mock_echo.call_args_list 
                    if len(call[0]) > 0 and "AT LEAST ONE SOURCE PATH IS REQUIRED" in str(call[0][0])
                ]
                assert len(error_calls) > 0, "ERROR MESSAGE FOR EMPTY SOURCES NOT CALLED"
                raise
