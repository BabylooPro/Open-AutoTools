import pytest
from unittest.mock import patch, Mock, mock_open as mock_open_func
from autotools.autotranslate.core import translate_text, get_supported_languages
import io
import sys

# MOCK DATA
MOCK_LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German'
}

MOCK_TRANSLATION = {
    'text': 'Hello world',
    'translated': 'Bonjour le monde',
    'source_lang': 'en',
    'target_lang': 'fr'
}

# UNIT TESTS

# TEST GET SUPPORTED LANGUAGES
def test_get_supported_languages():
    """TEST GET SUPPORTED LANGUAGES"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator:
        mock_instance = Mock()
        mock_instance.get_supported_languages.return_value = MOCK_LANGUAGES
        mock_translator.return_value = mock_instance
        languages = get_supported_languages()
        assert isinstance(languages, dict)
        assert 'en' in languages
        assert languages['en'] == 'English'

# TEST BASIC TEXT TRANSLATION
def test_translate_text_basic():
    """TEST BASIC TEXT TRANSLATION"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr')
        assert result == MOCK_TRANSLATION['translated']

# TEST TRANSLATION WITH SOURCE LANGUAGE
def test_translate_text_with_source():
    """TEST TRANSLATION WITH SOURCE LANGUAGE"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        
        result = translate_text('Hello world', from_lang='en', to_lang='fr')
        assert result == MOCK_TRANSLATION['translated']

# TEST LANGUAGE DETECTION
def test_translate_text_with_detect():
    """TEST TRANSLATION WITH LANGUAGE DETECTION"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr', detect_lang=True)
        expected = f"[Detected: {mock_detect.return_value}] {MOCK_TRANSLATION['translated']}"
        assert result == expected

# TEST CLIPBOARD COPY
def test_translate_text_with_copy():
    """TEST TRANSLATION WITH CLIPBOARD COPY"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('pyperclip.copy') as mock_copy:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr', copy=True)
        assert result == MOCK_TRANSLATION['translated']
        mock_copy.assert_called_once_with(MOCK_TRANSLATION['translated'])

# TEST FILE OUTPUT
def test_translate_text_with_output():
    """TEST TRANSLATION WITH FILE OUTPUT"""
    mock_open = mock_open_func()
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('builtins.open', mock_open):
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr', output='test.txt')
        assert result == MOCK_TRANSLATION['translated']
        mock_open.assert_called_once_with('test.txt', 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with(MOCK_TRANSLATION['translated'])

# TEST FILE OUTPUT WITH DETECTION
def test_translate_text_with_output_and_detect():
    """TEST TRANSLATION WITH FILE OUTPUT AND DETECTION"""
    mock_open = mock_open_func()
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('builtins.open', mock_open):
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr', output='test.txt', detect_lang=True)
        expected = f"[Detected: {mock_detect.return_value}] {MOCK_TRANSLATION['translated']}"
        assert result == expected
        mock_open.assert_called_once_with('test.txt', 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with(expected)

# TEST FILE OUTPUT ERROR
def test_translate_text_with_output_error():
    """TEST TRANSLATION WITH FILE OUTPUT ERROR"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('builtins.open', create=True) as mock_open, \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        error_msg = "Permission denied"
        mock_open.side_effect = IOError(error_msg)
        
        result = translate_text('Hello world', to_lang='fr', output='test.txt', detect_lang=True)
        expected = f"[Detected: {mock_detect.return_value}] {MOCK_TRANSLATION['translated']}"
        assert result == expected
        assert f"\nError saving to file: {error_msg}" in fake_out.getvalue()

# TEST FILE OUTPUT ERROR WITHOUT DETECTION
def test_translate_text_with_output_error_no_detect():
    """TEST TRANSLATION WITH FILE OUTPUT ERROR WITHOUT DETECTION"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('builtins.open', create=True) as mock_open, \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        error_msg = "Permission denied"
        mock_open.side_effect = IOError(error_msg)
        
        result = translate_text('Hello world', to_lang='fr', output='test.txt', detect_lang=False)
        assert result == MOCK_TRANSLATION['translated']
        assert f"\nError saving to file: {error_msg}" in fake_out.getvalue()

# TEST FILE OUTPUT GENERIC ERROR
def test_translate_text_with_output_generic_error():
    """TEST TRANSLATION WITH GENERIC FILE OUTPUT ERROR"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect, \
         patch('builtins.open', create=True) as mock_open, \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        error_msg = "Some unexpected error"
        mock_open.side_effect = Exception(error_msg)
        
        result = translate_text('Hello world', to_lang='fr', output='test.txt')
        assert result == MOCK_TRANSLATION['translated']
        assert f"\nError saving to file: {error_msg}" in fake_out.getvalue()

# TEST AUTO DETECT LANGUAGE
def test_translate_text_auto_detect():
    """TEST TRANSLATION WITH AUTO LANGUAGE DETECTION"""
    with patch('autotools.autotranslate.core.GoogleTranslator') as mock_translator, \
         patch('autotools.autotranslate.core.detect') as mock_detect:
        mock_instance = Mock()
        mock_instance.translate.return_value = MOCK_TRANSLATION['translated']
        mock_translator.return_value = mock_instance
        mock_detect.return_value = 'en'
        
        result = translate_text('Hello world', to_lang='fr', from_lang=None)
        assert result == MOCK_TRANSLATION['translated']
        mock_detect.assert_called_once_with('Hello world') 
