import pytest
import json
import os
import builtins
from unittest.mock import patch

from autotools.autoconvert.core import (detect_file_type, convert_file)

# FILE TYPE DETECTION TESTS

# TEST DETECT TEXT FILE TYPE
def test_detect_file_type_text():
    assert detect_file_type("file.txt") == "text"
    assert detect_file_type("file.md") == "text"
    assert detect_file_type("file.json") == "text"
    assert detect_file_type("file.xml") == "text"
    assert detect_file_type("file.html") == "text"

# TEST DETECT IMAGE FILE TYPE
def test_detect_file_type_image():
    assert detect_file_type("file.jpg") == "image"
    assert detect_file_type("file.png") == "image"
    assert detect_file_type("file.gif") == "image"
    assert detect_file_type("file.webp") == "image"

# TEST DETECT AUDIO FILE TYPE
def test_detect_file_type_audio():
    assert detect_file_type("file.mp3") == "audio"
    assert detect_file_type("file.wav") == "audio"
    assert detect_file_type("file.ogg") == "audio"
    assert detect_file_type("file.flac") == "audio"

# TEST DETECT VIDEO FILE TYPE
def test_detect_file_type_video():
    assert detect_file_type("file.mp4") == "video"
    assert detect_file_type("file.avi") == "video"
    assert detect_file_type("file.mov") == "video"
    assert detect_file_type("file.webm") == "video"

# TEST DETECT UNKNOWN FILE TYPE
def test_detect_file_type_unknown():
    assert detect_file_type("file.unknown") == "unknown"
    assert detect_file_type("file") == "unknown"

# FILE CONVERSION TESTS

# TEST TEXT TO TEXT CONVERSION
def test_convert_file_text_to_json(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "hello world", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["text"] == "hello world"

# TEST TEXT TO XML CONVERSION
def test_convert_file_text_to_xml(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test content", mode="w")
    output_file = os.path.join(temp_dir, "output.xml")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)

# TEST JSON TO TEXT CONVERSION
def test_convert_file_json_to_text(temp_dir, create_test_file):
    input_file = create_test_file("input.json", json.dumps({"text": "hello world"}), mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "hello world" in content

# TEST XML TO TEXT CONVERSION
def test_convert_file_xml_to_text(temp_dir, create_test_file):
    input_file = create_test_file("input.xml", "<root><text>hello world</text></root>", mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "hello world" in content

# TEST CONVERT FILE WITH NONEXISTENT INPUT
def test_convert_file_nonexistent(temp_dir):
    input_file = os.path.join(temp_dir, "nonexistent.txt")
    output_file = os.path.join(temp_dir, "output.txt")
    
    with pytest.raises(FileNotFoundError) as exc_info: convert_file(input_file, output_file)
    assert "NOT FOUND" in str(exc_info.value).upper() or "INPUT FILE" in str(exc_info.value).upper()

# TEST CONVERT FILE UNSUPPORTED CONVERSION
def test_convert_file_unsupported(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.jpg")
    
    success, message = convert_file(input_file, output_file)
    assert success is False or "UNSUPPORTED" in message.upper()

# TEST CONVERT FILE HTML TO TEXT
def test_convert_file_html_to_text(temp_dir, create_test_file):
    input_file = create_test_file("input.html", "<html><body><p>Hello World</p></body></html>", mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Hello World" in content

# TEST CONVERT FILE HTML TO JSON
def test_convert_file_html_to_json(temp_dir, create_test_file):
    input_file = create_test_file("input.html", "<html><body><p>Test</p></body></html>", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)

# TEST CONVERT FILE WITH EXCEPTION
def test_convert_file_with_exception(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    invalid_output = os.path.join(temp_dir, "nonexistent_dir", "output.txt")
    
    with patch("autotools.autoconvert.conversion.convert_text.os.makedirs", side_effect=OSError("Cannot create output directory")):
        success, message = convert_file(input_file, invalid_output)
    assert success is False
    assert "FAILED" in message.upper()

# TEST CONVERT FILE WITH WRITE ERROR
def test_convert_file_with_write_error(temp_dir, create_test_file):
    call_count = [0]
    original_open = builtins.open
    
    def mock_open_side_effect(path, mode, *args, **kwargs):
        call_count[0] += 1
        if 'r' in mode: return original_open(path, mode, *args, **kwargs)
        elif 'w' in mode or 'x' in mode or 'a' in mode: raise PermissionError("Permission denied")
        else: return original_open(path, mode, *args, **kwargs)
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    with patch('builtins.open', side_effect=mock_open_side_effect): success, message = convert_file(input_file, output_file)
    
    assert success is False
    assert "FAILED" in message.upper()
    assert "write" in message.lower() or "permission" in message.lower()

# TEST CONVERT FILE WITH GENERAL EXCEPTION
@patch('autotools.autoconvert.core.detect_file_type')
def test_convert_file_with_general_exception(mock_detect, temp_dir, create_test_file):
    mock_detect.side_effect = ValueError("Unexpected error")
    
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.txt")
    
    success, message = convert_file(input_file, output_file)
    assert success is False
    assert "FAILED" in message.upper()

# TEST CONVERT FILE WITH INPUT TYPE PROVIDED
def test_convert_file_with_input_type(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    success, _ = convert_file(input_file, output_file, input_type="text")
    assert success is True

# TEST CONVERT FILE WITH OUTPUT TYPE PROVIDED
def test_convert_file_with_output_type(temp_dir, create_test_file):
    input_file = create_test_file("input.txt", "test", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    success, _ = convert_file(input_file, output_file, output_type="text")
    assert success is True

# TEST CONVERT FILE MARKDOWN TO JSON
def test_convert_file_markdown_to_json(temp_dir, create_test_file):
    input_file = create_test_file("input.md", "# Test\nThis is a test.", mode="w")
    output_file = os.path.join(temp_dir, "output.json")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    assert os.path.exists(output_file)

# TEST CONVERT FILE IMAGE TO IMAGE
@patch('autotools.autoconvert.core.convert_image')
def test_convert_file_image_to_image(mock_convert_image, temp_dir, create_test_file):
    mock_convert_image.return_value = True
    
    input_file = create_test_file("input.jpg", b"fake image")
    output_file = os.path.join(temp_dir, "output.png")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    mock_convert_image.assert_called_once()

# TEST CONVERT FILE AUDIO TO AUDIO
@patch('autotools.autoconvert.core.convert_audio')
def test_convert_file_audio_to_audio(mock_convert_audio, temp_dir, create_test_file):
    mock_convert_audio.return_value = True
    
    input_file = create_test_file("input.mp3", b"fake audio")
    output_file = os.path.join(temp_dir, "output.wav")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    mock_convert_audio.assert_called_once()

# TEST CONVERT FILE VIDEO TO VIDEO
@patch('autotools.autoconvert.core.convert_video')
def test_convert_file_video_to_video(mock_convert_video, temp_dir, create_test_file):
    mock_convert_video.return_value = True
    
    input_file = create_test_file("input.mp4", b"fake video")
    output_file = os.path.join(temp_dir, "output.avi")
    
    success, _ = convert_file(input_file, output_file)
    assert success is True
    mock_convert_video.assert_called_once()
