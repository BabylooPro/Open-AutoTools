import pytest
from unittest.mock import patch, Mock, mock_open
from pathlib import Path
import os
import platform
import json
import shutil
from autotools.autodownload.core import (
    get_default_download_dir,
    get_filename_from_url,
    validate_youtube_url,
    download_file,
    get_consent_file_path,
    load_consent_status,
    save_consent_status,
    get_user_consent,
    download_youtube_video
)

# FIXTURES
@pytest.fixture(autouse=True)
def cleanup_downloads():
    """CLEANUP DOWNLOADED FILES AFTER EACH TEST"""
    # SETUP - CREATE TEMP DOWNLOAD DIR
    test_download_dir = Path.home() / 'Downloads' / 'test_downloads'
    test_download_dir.mkdir(parents=True, exist_ok=True)
    
    # PATCH DEFAULT DOWNLOAD DIR TO USE TEST DIR
    with patch('autotools.autodownload.core.get_default_download_dir', return_value=test_download_dir):
        yield test_download_dir
    
    # CLEANUP - REMOVE TEST DIR AND ALL ITS CONTENTS
    if test_download_dir.exists():
        shutil.rmtree(test_download_dir)

# CONSENT FILE FIXTURE
@pytest.fixture(autouse=True)
def cleanup_consent():
    """CLEANUP CONSENT FILE AFTER EACH TEST"""
    # SETUP
    consent_file = get_consent_file_path()
    consent_dir = consent_file.parent
    
    yield
    
    # CLEANUP - USE RMTREE INSTEAD OF UNLINK/RMDIR
    if consent_dir.exists():
        shutil.rmtree(consent_dir)

# UNIT TESTS

# TEST FOR DEFAULT DOWNLOAD DIRECTORY RETRIEVAL
def test_get_default_download_dir():
    """TEST DEFAULT DOWNLOAD DIRECTORY RETRIEVAL"""
    with patch.dict('os.environ', {'USERPROFILE': '/users/test'} if os.name == 'nt' else {}):
        download_dir = get_default_download_dir()
        assert isinstance(download_dir, Path)
        assert download_dir.name == 'Downloads'

# TEST FOR FILENAME EXTRACTION FROM URL
def test_get_filename_from_url():
    """TEST FILENAME EXTRACTION FROM URL"""
    # TEST WITH FILENAME IN URL
    url = 'https://example.com/file.pdf'
    assert get_filename_from_url(url) == 'file.pdf'
    
    # TEST WITHOUT FILENAME
    url = 'https://example.com/'
    assert get_filename_from_url(url) == 'downloaded_file'
    
    # TEST WITHOUT EXTENSION
    url = 'https://example.com/file'
    assert get_filename_from_url(url) == 'file.bin'

# TEST FOR YOUTUBE URL VALIDATION
@patch('yt_dlp.YoutubeDL')
def test_validate_youtube_url_valid(mock_ytdl):
    """TEST YOUTUBE URL VALIDATION - VALID URL"""
    mock_ytdl.return_value.__enter__.return_value.extract_info.return_value = {}
    # TEST STANDARD FORMATS
    assert validate_youtube_url('https://youtube.com/watch?v=valid') is True
    assert validate_youtube_url('https://youtu.be/valid') is True
    # TEST ADDITIONAL FORMATS
    assert validate_youtube_url('https://youtube.com/watch/valid') is True
    assert validate_youtube_url('https://youtube.com/shorts/valid') is True
    assert validate_youtube_url('https://youtube.com/live/valid') is True
    assert validate_youtube_url('https://music.youtube.com/watch?v=valid') is True
    assert validate_youtube_url('https://youtube.com/attribution_link?a=xyz&u=/watch?v=valid') is True

# TEST FOR YOUTUBE URL VALIDATION - NON YOUTUBE URL
def test_validate_youtube_url_non_youtube():
    """TEST YOUTUBE URL VALIDATION - NON YOUTUBE URL"""
    assert validate_youtube_url('https://example.com/video') is False

# TEST FOR YOUTUBE URL VALIDATION - INVALID URL
@patch('yt_dlp.YoutubeDL')
def test_validate_youtube_url_invalid(mock_ytdl):
    """TEST YOUTUBE URL VALIDATION - INVALID URL"""
    mock_ytdl.return_value.__enter__.return_value.extract_info.side_effect = Exception('Invalid URL')
    assert validate_youtube_url('https://youtube.com/invalid') is False

# TEST FOR FILE DOWNLOAD
@patch('requests.get')
@patch('builtins.open', new_callable=mock_open)
def test_download_file(mock_file, mock_get, cleanup_downloads):
    """TEST FILE DOWNLOAD"""
    # MOCK RESPONSE WITH CONTEXT MANAGER
    mock_response = Mock()
    mock_response.headers.get.return_value = '1024'
    mock_response.iter_content.return_value = [b'data']
    mock_response.raise_for_status.return_value = None
    
    # CONFIGURE CONTEXT MANAGER PROPERLY
    mock_get.return_value = mock_response
    mock_get.return_value.__enter__ = Mock(return_value=mock_response)
    mock_get.return_value.__exit__ = Mock(return_value=None)
    
    download_file('https://example.com/file.pdf')
    mock_file.assert_called()
    mock_response.iter_content.assert_called_once()

# TEST FOR CONSENT FILE PATH RETRIEVAL
def test_get_consent_file_path():
    """TEST CONSENT FILE PATH"""
    with patch('pathlib.Path.home', return_value=Path('/tmp')):
        path = get_consent_file_path()
        assert isinstance(path, Path)
        assert path.name == 'consent.json'
        assert '.autotools' in str(path)

# TEST FOR CONSENT STATUS LOADING - TRUE
@patch('pathlib.Path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='{"youtube_consent": true}')
def test_load_consent_status_true(mock_file, mock_exists):
    """TEST CONSENT STATUS LOADING - TRUE"""
    mock_file.return_value.__enter__.return_value.read.return_value = '{"youtube_consent": true}'
    assert load_consent_status() is True
    mock_file.assert_called_once()

# TEST FOR CONSENT STATUS LOADING - FALSE
@patch('pathlib.Path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='{"youtube_consent": false}')
def test_load_consent_status_false(mock_file, mock_exists):
    """TEST CONSENT STATUS LOADING - FALSE"""
    mock_file.return_value.__enter__.return_value.read.return_value = '{"youtube_consent": false}'
    assert load_consent_status() is False
    mock_file.assert_called_once()

# TEST FOR CONSENT STATUS SAVING
@patch('pathlib.Path.exists', return_value=False)
@patch('pathlib.Path.mkdir')
@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
def test_save_consent_status(mock_json_dump, mock_file, mock_mkdir, mock_exists):
    """TEST CONSENT STATUS SAVING"""
    # CALL THE FUNCTION
    result = save_consent_status(True)
    
    # VERIFY CALLS
    mock_mkdir.assert_called_once_with(exist_ok=True)
    mock_file.assert_called_once()
    mock_json_dump.assert_called_once_with({'youtube_consent': True}, mock_file())
    assert result is True

# TEST FOR USER CONSENT - YES
@patch('builtins.input', return_value='yes')
@patch('autotools.autodownload.core.save_consent_status')
def test_get_user_consent_yes(mock_save, mock_input):
    """TEST USER CONSENT - YES"""
    assert get_user_consent() is True
    mock_save.assert_called_with(True)
    mock_input.assert_called_once()

# TEST FOR USER CONSENT - NO
@patch('builtins.input', return_value='no')
@patch('autotools.autodownload.core.save_consent_status')
def test_get_user_consent_no(mock_save, mock_input):
    """TEST USER CONSENT - NO"""
    assert get_user_consent() is False
    mock_save.assert_called_with(False)
    mock_input.assert_called_once()

# TEST FOR YOUTUBE VIDEO DOWNLOAD   
@patch('yt_dlp.YoutubeDL')
@patch('autotools.autodownload.core.load_consent_status', return_value=True)
def test_download_youtube_video(mock_consent, mock_ytdl):
    """TEST YOUTUBE VIDEO DOWNLOAD"""
    # MOCK VIDEO INFO EXTRACTION
    mock_info = {
        'formats': [
            {'height': 720, 'ext': 'mp4'},
            {'height': 1080, 'ext': 'mp4'}
        ]
    }
    mock_ytdl_instance = Mock()
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    mock_ytdl_instance.extract_info.return_value = mock_info
    mock_ytdl_instance.download.return_value = 0
    
    # MOCK FILE CHECK TO RETURN TRUE (NO EXISTING FILE)
    with patch('autotools.autodownload.core.check_existing_video', return_value=True):
        assert download_youtube_video('https://youtube.com/watch?v=test') is True
        mock_ytdl.assert_called()
        mock_consent.assert_called_once()
        mock_ytdl_instance.download.assert_called_once() 
