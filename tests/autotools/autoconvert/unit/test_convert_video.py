import pytest
import os
import sys
from unittest.mock import MagicMock

from autotools.autoconvert.conversion.convert_video import convert_video
from ..conftest import mock_import_error, cleanup_sys_modules

# TEST CONVERT VIDEO WITH OUTPUT FORMAT
def test_convert_video_with_output_format(monkeypatch, mock_moviepy, temp_dir, create_test_file):
    mock_clip = MagicMock()
    mock_moviepy.VideoFileClip.return_value.__enter__.return_value = mock_clip
    
    input_file = create_test_file("input.mp4", b"fake video data")
    output_file = os.path.join(temp_dir, "output.avi")
    
    result = convert_video(input_file, output_file, "avi")
    assert result is True
    mock_clip.write_videofile.assert_called_once()

# TEST CONVERT VIDEO SUCCESS
def test_convert_video_success(monkeypatch, mock_moviepy, temp_dir, create_test_file):
    mock_clip = MagicMock()
    mock_moviepy.VideoFileClip.return_value.__enter__.return_value = mock_clip
    
    input_file = create_test_file("input.mp4", b"fake video data")
    output_file = os.path.join(temp_dir, "output.avi")
    
    result = convert_video(input_file, output_file)
    assert result is True
    mock_clip.write_videofile.assert_called_once()

# TEST CONVERT VIDEO FILE NOT FOUND
def test_convert_video_file_not_found(monkeypatch, mock_moviepy, temp_dir):
    input_file = os.path.join(temp_dir, "nonexistent.mp4")
    output_file = os.path.join(temp_dir, "output.avi")
    
    with pytest.raises(Exception) as exc_info: convert_video(input_file, output_file)
    assert "FILE NOT FOUND" in str(exc_info.value).upper()

# TEST CONVERT VIDEO WITH EXCEPTION
def test_convert_video_with_exception(monkeypatch, mock_moviepy, temp_dir, create_test_file):
    mock_moviepy.VideoFileClip.side_effect = Exception("Video processing error")
    
    input_file = create_test_file("input.mp4", b"fake video data")
    output_file = os.path.join(temp_dir, "output.avi")
    
    with pytest.raises(Exception) as exc_info: convert_video(input_file, output_file)
    assert "VIDEO CONVERSION FAILED" in str(exc_info.value)

# TEST CONVERT VIDEO IMPORT ERROR
def test_convert_video_import_error(monkeypatch, temp_dir, create_test_file):
    cleanup_sys_modules('moviepy', 'moviepy.editor')
    mock_import_error(monkeypatch, 'moviepy')
    
    input_file = create_test_file("input.mp4", b"fake video data")
    output_file = os.path.join(temp_dir, "output.avi")
    
    with pytest.raises(ImportError) as exc_info: convert_video(input_file, output_file)
    assert "MOVIEPY" in str(exc_info.value).upper()
