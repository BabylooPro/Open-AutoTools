import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner
from autotools.cli import autotranslate

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

# INTEGRATION TESTS

# TEST BASIC CLI FUNCTIONALITY
@patch('autotools.autotranslate.core.translate_text')
def test_autotranslate_cli_basic(mock_translate):
    """TEST BASIC CLI FUNCTIONALITY"""
    mock_translate.return_value = MOCK_TRANSLATION['translated']
    
    runner = CliRunner()
    result = runner.invoke(autotranslate, ['Hello world', '--to', 'fr'])
    assert result.exit_code == 0
    assert MOCK_TRANSLATION['translated'] in result.output

# TEST LIST LANGUAGES FUNCTIONALITY
@patch('autotools.autotranslate.core.get_supported_languages')
def test_autotranslate_cli_list_languages(mock_languages):
    """TEST LIST LANGUAGES FUNCTIONALITY"""
    mock_languages.return_value = MOCK_LANGUAGES
    
    runner = CliRunner()
    result = runner.invoke(autotranslate, ['--list-languages'])
    assert result.exit_code == 0
    for lang in MOCK_LANGUAGES.values():
        assert lang.lower() in result.output.lower()

# TEST TRANSLATION WITH SOURCE LANGUAGE
@patch('autotools.autotranslate.core.translate_text')
def test_autotranslate_cli_with_source(mock_translate):
    """TEST TRANSLATION WITH SOURCE LANGUAGE"""
    mock_translate.return_value = MOCK_TRANSLATION['translated']
    
    runner = CliRunner()
    result = runner.invoke(autotranslate, ['Hello world', '--to', 'fr', '--from', 'en'])
    assert result.exit_code == 0
    assert MOCK_TRANSLATION['translated'] in result.output

# TEST TRANSLATION WITH CLIPBOARD COPY
@patch('autotools.autotranslate.core.translate_text')
def test_autotranslate_cli_with_copy(mock_translate):
    """TEST TRANSLATION WITH CLIPBOARD COPY"""
    mock_translate.return_value = MOCK_TRANSLATION['translated']
    
    runner = CliRunner()
    result = runner.invoke(autotranslate, ['Hello world', '--to', 'fr', '--copy'])
    assert result.exit_code == 0
    assert MOCK_TRANSLATION['translated'] in result.output

# TEST TRANSLATION WITH LANGUAGE DETECTION
@patch('autotools.autotranslate.core.translate_text')
def test_autotranslate_cli_with_detect(mock_translate):
    """TEST TRANSLATION WITH LANGUAGE DETECTION"""
    mock_translate.return_value = MOCK_TRANSLATION['translated']
    
    runner = CliRunner()
    result = runner.invoke(autotranslate, ['Hello world', '--to', 'fr', '--detect'])
    assert result.exit_code == 0
    assert MOCK_TRANSLATION['translated'] in result.output

# TEST TRANSLATION WITH FILE OUTPUT
@patch('autotools.autotranslate.core.translate_text')
def test_autotranslate_cli_with_output(mock_translate):
    """TEST TRANSLATION WITH FILE OUTPUT"""
    mock_translate.return_value = MOCK_TRANSLATION['translated']
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(autotranslate, ['Hello world', '--to', 'fr', '--output', 'test.txt'])
        assert result.exit_code == 0
        assert MOCK_TRANSLATION['translated'] in result.output

# TEST CLI WITH NO TEXT PROVIDED
def test_autotranslate_cli_no_text():
    """TEST CLI WITH NO TEXT PROVIDED"""
    runner = CliRunner()
    result = runner.invoke(autotranslate)
    assert result.exit_code == 0
    assert "Error: Please provide text to translate" in result.output 
