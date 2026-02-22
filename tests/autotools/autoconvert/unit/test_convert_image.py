import pytest
import os
import sys
import types
from unittest.mock import patch, MagicMock

from autotools.autoconvert.conversion.convert_image import convert_image

# TEST CONVERT IMAGE WITH PIL
@patch('PIL.Image', create=True)
def test_convert_image_success(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'RGB'
    mock_image.open.return_value.__enter__.return_value = mock_img
    
    input_file = create_test_file("input.jpg", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")
    
    result = convert_image(input_file, output_file)
    assert result is True
    mock_img.save.assert_called_once()

# TEST CONVERT IMAGE RGBA TO RGB
@patch('PIL.Image', create=True)
def test_convert_image_rgba_to_rgb(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'RGBA'
    mock_img.size = (100, 100)
    mock_img.split.return_value = [None, None, None, MagicMock()]
    mock_image.open.return_value.__enter__.return_value = mock_img
    mock_rgb_img = MagicMock()
    mock_image.new.return_value = mock_rgb_img
    
    input_file = create_test_file("input.png", b"fake image data")
    output_file = os.path.join(temp_dir, "output.jpg")
    
    result = convert_image(input_file, output_file, "JPG")
    assert result is True
    mock_rgb_img.save.assert_called_once()

# TEST CONVERT IMAGE MODE P TO RGB
@patch('PIL.Image', create=True)
def test_convert_image_mode_p_to_rgb(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'P'
    mock_img.size = (100, 100)
    mock_image.open.return_value.__enter__.return_value = mock_img
    mock_rgb_img = MagicMock()
    mock_image.new.return_value = mock_rgb_img
    
    input_file = create_test_file("input.gif", b"fake image data")
    output_file = os.path.join(temp_dir, "output.jpg")
    
    result = convert_image(input_file, output_file, "JPG")
    assert result is True
    mock_img.convert.assert_called_once_with('RGBA')

# TEST CONVERT IMAGE MODE LA TO RGB
@patch('PIL.Image', create=True)
def test_convert_image_mode_la_to_rgb(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'LA'
    mock_img.size = (100, 100)
    mock_img.split.return_value = [None, MagicMock()]
    mock_image.open.return_value.__enter__.return_value = mock_img
    mock_rgb_img = MagicMock()
    mock_image.new.return_value = mock_rgb_img
    
    input_file = create_test_file("input.png", b"fake image data")
    output_file = os.path.join(temp_dir, "output.jpg")
    
    result = convert_image(input_file, output_file, "JPG")
    assert result is True
    mock_rgb_img.save.assert_called_once()

# TEST CONVERT IMAGE WITH OUTPUT FORMAT
@patch('PIL.Image', create=True)
def test_convert_image_with_output_format(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'RGB'
    mock_image.open.return_value.__enter__.return_value = mock_img
    
    input_file = create_test_file("input.jpg", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")
    
    result = convert_image(input_file, output_file, "PNG")
    assert result is True
    mock_img.save.assert_called_once_with(output_file, format="PNG")

# TEST NORMALIZE JPG TO JPEG FORMAT FOR PIL
@patch('PIL.Image', create=True)
def test_convert_image_normalizes_jpg_to_jpeg(mock_image, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'RGB'
    mock_image.open.return_value.__enter__.return_value = mock_img

    input_file = create_test_file("input.jpg", b"fake image data")
    output_file = os.path.join(temp_dir, "output.jpg")

    result = convert_image(input_file, output_file)
    assert result is True
    mock_img.save.assert_called_once_with(output_file, format="JPEG")

# TEST HEIC INPUT REGISTERS PILLOW-HEIF OPENER WHEN AVAILABLE
@patch('PIL.Image', create=True)
def test_convert_image_heic_registers_heif_opener(mock_image, monkeypatch, temp_dir, create_test_file):
    mock_img = MagicMock()
    mock_img.mode = 'RGB'
    mock_image.open.return_value.__enter__.return_value = mock_img
    register_mock = MagicMock()
    monkeypatch.setitem(sys.modules, 'pillow_heif', types.SimpleNamespace(register_heif_opener=register_mock))

    input_file = create_test_file("input.heic", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")

    result = convert_image(input_file, output_file)
    assert result is True
    register_mock.assert_called_once()
    mock_img.save.assert_called_once_with(output_file, format="PNG")

# TEST HEIC INPUT WITHOUT PILLOW-HEIF FALLS BACK GRACEFULLY
@patch('PIL.Image', create=True)
def test_convert_image_heic_without_heif_dependency(mock_image, monkeypatch, temp_dir, create_test_file):
    from ..conftest import mock_import_error
    mock_img = MagicMock()
    mock_img.mode = 'RGB'
    mock_image.open.return_value.__enter__.return_value = mock_img
    mock_import_error(monkeypatch, 'pillow_heif')

    input_file = create_test_file("input.heic", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")

    result = convert_image(input_file, output_file)
    assert result is True
    mock_img.save.assert_called_once_with(output_file, format="PNG")

# TEST CONVERT IMAGE FILE NOT FOUND
def test_convert_image_file_not_found(temp_dir):
    input_file = os.path.join(temp_dir, "nonexistent.jpg")
    output_file = os.path.join(temp_dir, "output.png")
    
    with pytest.raises(Exception) as exc_info: convert_image(input_file, output_file)
    assert "FILE NOT FOUND" in str(exc_info.value).upper()

# TEST CONVERT IMAGE WITH EXCEPTION
@patch('PIL.Image', create=True)
def test_convert_image_with_exception(mock_image, temp_dir, create_test_file):
    mock_image.open.side_effect = Exception("Image processing error")
    
    input_file = create_test_file("input.jpg", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")
    
    with pytest.raises(Exception) as exc_info: convert_image(input_file, output_file)
    assert "IMAGE CONVERSION FAILED" in str(exc_info.value)

# TEST CONVERT IMAGE IMPORT ERROR
def test_convert_image_import_error(monkeypatch, temp_dir, create_test_file):
    from ..conftest import mock_import_error
    mock_import_error(monkeypatch, 'PIL')
    
    input_file = create_test_file("input.jpg", b"fake image data")
    output_file = os.path.join(temp_dir, "output.png")
    
    with pytest.raises(ImportError) as exc_info: convert_image(input_file, output_file)
    assert "PILLOW" in str(exc_info.value).upper()
