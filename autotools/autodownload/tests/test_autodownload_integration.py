import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner
from autotools.autodownload.commands import autodownload
from autotools.autodownload.core import download_youtube_video, download_file, validate_youtube_url

# INTEGRATION TESTS

# TEST FOR YOUTUBE VIDEO DOWNLOAD WITH MP4 FORMAT
@patch('autotools.autodownload.commands.validate_youtube_url', return_value=True)
@patch('autotools.autodownload.core.get_user_consent', return_value=True)
@patch('autotools.autodownload.commands.download_youtube_video')
def test_autodownload_cli_youtube_mp4(mock_download, mock_consent, mock_validate, runner):
    """TEST YOUTUBE VIDEO DOWNLOAD WITH MP4 FORMAT"""
    mock_download.return_value = True
    result = runner.invoke(autodownload, ['https://youtube.com/watch?v=test'])
    assert result.exit_code == 0
    mock_download.assert_called_with('https://youtube.com/watch?v=test', 'mp4', 'best')

# TEST FOR YOUTUBE VIDEO DOWNLOAD WITH MP3 FORMAT
@patch('autotools.autodownload.commands.validate_youtube_url', return_value=True)
@patch('autotools.autodownload.core.get_user_consent', return_value=True)
@patch('autotools.autodownload.commands.download_youtube_video')
def test_autodownload_cli_youtube_mp3(mock_download, mock_consent, mock_validate, runner):
    """TEST YOUTUBE VIDEO DOWNLOAD WITH MP3 FORMAT"""
    mock_download.return_value = True
    result = runner.invoke(autodownload, ['https://youtube.com/watch?v=test', '--format', 'mp3'])
    assert result.exit_code == 0
    mock_download.assert_called_with('https://youtube.com/watch?v=test', 'mp3', 'best')

# TEST FOR YOUTUBE VIDEO DOWNLOAD WITH CUSTOM QUALITY
@patch('autotools.autodownload.commands.validate_youtube_url', return_value=True)
@patch('autotools.autodownload.core.get_user_consent', return_value=True)
@patch('autotools.autodownload.commands.download_youtube_video')
def test_autodownload_cli_youtube_quality(mock_download, mock_consent, mock_validate, runner):
    """TEST YOUTUBE VIDEO DOWNLOAD WITH CUSTOM QUALITY"""
    mock_download.return_value = True
    result = runner.invoke(autodownload, ['https://youtube.com/watch?v=test', '--quality', '720p'])
    assert result.exit_code == 0
    mock_download.assert_called_with('https://youtube.com/watch?v=test', 'mp4', '720p')

# TEST FOR REGULAR FILE DOWNLOAD
@patch('autotools.autodownload.commands.download_file')
def test_autodownload_cli_file(mock_download, runner):
    """TEST REGULAR FILE DOWNLOAD"""
    result = runner.invoke(autodownload, ['https://example.com/file.pdf'])
    assert result.exit_code == 0
    mock_download.assert_called_with('https://example.com/file.pdf')

# TEST FOR INVALID YOUTUBE URL HANDLING
@patch('autotools.autodownload.commands.validate_youtube_url')
def test_autodownload_cli_invalid_youtube(mock_validate, runner):
    """TEST INVALID YOUTUBE URL HANDLING"""
    mock_validate.return_value = False
    
    result = runner.invoke(autodownload, ['https://youtube.com/invalid'], catch_exceptions=False)
    
    # VERIFY THAT THE COMMAND FAILED AND THE ERROR MESSAGE IS CORRECT
    assert result.exit_code == 1
    assert "Invalid YouTube URL" in result.output

# TEST FOR HELP DISPLAY
def test_autodownload_cli_help(runner):
    """TEST HELP DISPLAY"""
    result = runner.invoke(autodownload, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--format" in result.output
    assert "--quality" in result.output 

@pytest.fixture
def runner():
    return CliRunner() 
