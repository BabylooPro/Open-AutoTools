import pytest
import os
from unittest.mock import MagicMock

from autotools.autoconvert.conversion.convert_audio import convert_audio
from ..conftest import mock_import_error

# TEST CONVERT AUDIO WITH OUTPUT FORMAT
def test_convert_audio_with_output_format(monkeypatch, mock_pydub, temp_dir, create_test_file):
    mock_segment = MagicMock()
    mock_pydub.from_file.return_value = mock_segment
    
    input_file = create_test_file("input.mp3", b"fake audio data")
    output_file = os.path.join(temp_dir, "output.wav")
    
    result = convert_audio(input_file, output_file, "wav")
    assert result is True
    mock_segment.export.assert_called_once_with(output_file, format="wav")

# TEST CONVERT AUDIO SUCCESS
def test_convert_audio_success(monkeypatch, mock_pydub, temp_dir, create_test_file):
    mock_segment = MagicMock()
    mock_pydub.from_file.return_value = mock_segment
    
    input_file = create_test_file("input.mp3", b"fake audio data")
    output_file = os.path.join(temp_dir, "output.wav")
    
    result = convert_audio(input_file, output_file)
    assert result is True
    mock_segment.export.assert_called_once()

# TEST CONVERT AUDIO FILE NOT FOUND
def test_convert_audio_file_not_found(monkeypatch, mock_pydub, temp_dir):
    input_file = os.path.join(temp_dir, "nonexistent.mp3")
    output_file = os.path.join(temp_dir, "output.wav")
    
    with pytest.raises(Exception) as exc_info: convert_audio(input_file, output_file)
    assert "FILE NOT FOUND" in str(exc_info.value).upper()

# TEST CONVERT AUDIO WITH EXCEPTION
def test_convert_audio_with_exception(monkeypatch, mock_pydub, temp_dir, create_test_file):
    mock_pydub.from_file.side_effect = Exception("Audio processing error")
    
    input_file = create_test_file("input.mp3", b"fake audio data")
    output_file = os.path.join(temp_dir, "output.wav")
    
    with pytest.raises(Exception) as exc_info: convert_audio(input_file, output_file)
    assert "AUDIO CONVERSION FAILED" in str(exc_info.value)

# TEST CONVERT AUDIO IMPORT ERROR
def test_convert_audio_import_error(monkeypatch, temp_dir, create_test_file):
    mock_import_error(monkeypatch, 'pydub')
    
    input_file = create_test_file("input.mp3", b"fake audio data")
    output_file = os.path.join(temp_dir, "output.wav")
    
    with pytest.raises(ImportError) as exc_info: convert_audio(input_file, output_file)
    assert "PYDUB" in str(exc_info.value).upper()
