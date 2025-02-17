import pytest
from unittest.mock import patch, Mock, mock_open
from autotools.autospell.core import SpellChecker
import spacy
from langdetect import DetectorFactory
import pyperclip
import io
import sys

# MOCK DATA
MOCK_MATCHES = [
    Mock(
        message="Spelling mistake",
        context="This is a speling mistake",
        offset=10,
        errorLength=7,
        category="SPELLING",
        ruleId="SPELLING_ERROR",
        replacements=["spelling"],
    ),
    Mock(
        message="Grammar error",
        context="They is going",
        offset=0,
        errorLength=7,
        category="GRAMMAR",
        ruleId="GRAMMAR_ERROR",
        replacements=["They are"],
    )
]

MOCK_LANGUAGES = [
    {
        "longCode": "en-US",
        "name": "English (US)",
        "variants": [{"name": "English (UK)"}]
    },
    {
        "longCode": "fr-FR",
        "name": "French",
        "variants": []
    }
]

# UNIT TESTS

# TEST INITIALIZATION
def test_init():
    """TEST SPELLCHECKER INITIALIZATION"""
    with patch('language_tool_python.LanguageTool') as mock_tool:
        checker = SpellChecker()
        assert checker.nlp_models == {}
        mock_tool.assert_called_once_with('auto')

# TEST LOADING SPACY MODEL
def test_load_spacy_model():
    """TEST LOADING SPACY MODEL"""
    with patch('spacy.util.get_installed_models') as mock_get_models, \
         patch('spacy.load') as mock_load:
        mock_get_models.return_value = ['en_core_web_lg', 'en_core_web_sm']
        mock_load.return_value = Mock()
        
        checker = SpellChecker()
        model = checker._load_spacy_model('en')
        
        assert model is not None
        mock_load.assert_called_once_with('en_core_web_lg')

# TEST TEXT CHECKING
def test_check_text_basic():
    """TEST BASIC TEXT CHECKING"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class, \
         patch('langdetect.detect_langs') as mock_detect:
        mock_tool = Mock()
        mock_tool.check.return_value = MOCK_MATCHES
        mock_tool_class.return_value = mock_tool
        mock_detect.return_value = [Mock(lang='en', prob=0.9)]
        
        checker = SpellChecker()
        result = checker.check_text("This is a test")
        
        assert 'corrections' in result
        assert 'statistics' in result
        assert 'language' in result
        assert len(result['corrections']) == 2
        assert result['language']['code'] == 'en'
        assert abs(result['language']['confidence'] - 0.9) < 0.1  # ALLOW SMALL FLOATING POINT DIFFERENCE

# TEST TEXT CHECKING WITH SPECIFIED LANGUAGE
def test_check_text_with_language():
    """TEST TEXT CHECKING WITH SPECIFIED LANGUAGE"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class:
        mock_tool = Mock()
        mock_tool.check.return_value = MOCK_MATCHES
        mock_tool_class.return_value = mock_tool
        
        checker = SpellChecker()
        result = checker.check_text("This is a test", lang='en')
        
        assert result['language']['code'] == 'en'
        assert result['language']['confidence'] == 1.0

# TEST ERROR SEVERITY CLASSIFICATION
def test_error_severity():
    """TEST ERROR SEVERITY CLASSIFICATION"""
    with patch('language_tool_python.LanguageTool'):
        checker = SpellChecker()
        
        spelling_match = Mock(ruleId="SPELLING_ERROR")
        grammar_match = Mock(ruleId="GRAMMAR_ERROR")
        style_match = Mock(ruleId="STYLE_ERROR")
        
        assert checker._get_error_severity(spelling_match) == 'high'
        assert checker._get_error_severity(grammar_match) == 'medium'
        assert checker._get_error_severity(style_match) == 'low'

# TEST DETAILED STATISTICS GENERATION
def test_detailed_stats():
    """TEST DETAILED STATISTICS GENERATION"""
    with patch('language_tool_python.LanguageTool'):
        checker = SpellChecker()
        corrections = [
            {'category': 'SPELLING', 'severity': 'high'},
            {'category': 'GRAMMAR', 'severity': 'medium'},
            {'category': 'SPELLING', 'severity': 'high'}
        ]
        
        stats = checker._get_detailed_stats(corrections)
        assert stats['total_errors'] == 3
        assert stats['categories']['SPELLING'] == 2
        assert stats['categories']['GRAMMAR'] == 1
        assert stats['severity']['high'] == 2
        assert stats['severity']['medium'] == 1

# TEST AUTOMATIC TEXT FIXING
def test_fix_text_auto():
    """TEST AUTOMATIC TEXT FIXING"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class:
        mock_tool = Mock()
        mock_tool.correct.return_value = "This is a corrected text"
        mock_tool_class.return_value = mock_tool
        
        checker = SpellChecker()
        result = checker.fix_text("This is a test")
        
        assert result == "This is a corrected text"
        mock_tool.correct.assert_called_once_with("This is a test")

# TEST TEXT FIXING WITH CLIPBOARD COPY
def test_fix_text_with_clipboard():
    """TEST TEXT FIXING WITH CLIPBOARD COPY"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class, \
         patch('pyperclip.copy') as mock_copy:
        mock_tool = Mock()
        mock_tool.correct.return_value = "This is a corrected text"
        mock_tool_class.return_value = mock_tool
        
        checker = SpellChecker()
        result = checker.fix_text("This is a test", copy_to_clipboard=True)
        
        assert result == "This is a corrected text"
        mock_copy.assert_called_once_with("This is a corrected text")

# TEST INTERACTIVE TEXT FIXING
def test_fix_text_interactive():
    """TEST INTERACTIVE TEXT FIXING"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class, \
         patch('builtins.input') as mock_input, \
         patch('builtins.print') as mock_print:
        mock_tool = Mock()
        mock_tool.check.return_value = MOCK_MATCHES
        mock_tool_class.return_value = mock_tool
        mock_input.return_value = "1"
        
        checker = SpellChecker()
        result = checker.fix_text("This is a speling mistake", interactive=True)
        
        assert mock_input.called
        assert mock_print.called

# TEST TEXT FIXING WITH IGNORED RULES
def test_fix_text_with_ignore():
    """TEST TEXT FIXING WITH IGNORED RULES"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class:
        mock_tool = Mock()
        mock_tool.check.return_value = MOCK_MATCHES
        mock_tool_class.return_value = mock_tool
        
        checker = SpellChecker()
        checker.fix_text("This is a test", ignore=['spelling'])
        
        mock_tool.correct.assert_called_once_with("This is a test")

# TEST GETTING SUPPORTED LANGUAGES
def test_get_supported_languages():
    """TEST GETTING SUPPORTED LANGUAGES"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class, \
         patch('requests.get') as mock_get:
        mock_tool = Mock()
        mock_tool_class.return_value = mock_tool
        mock_response = Mock()
        mock_response.json.return_value = MOCK_LANGUAGES
        mock_get.return_value = mock_response
        
        checker = SpellChecker()
        languages = checker.get_supported_languages()
        
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert 'code' in languages[0]
        assert 'name' in languages[0]
        assert 'variants' in languages[0]

# TEST GETTING SUPPORTED LANGUAGES WITH API FAILURE
def test_get_supported_languages_fallback():
    """TEST GETTING SUPPORTED LANGUAGES WITH API FAILURE"""
    with patch('language_tool_python.LanguageTool') as mock_tool_class, \
         patch('requests.get') as mock_get:
        mock_tool = Mock()
        mock_tool.language = 'en'
        mock_tool_class.return_value = mock_tool
        mock_get.side_effect = Exception("API Error")
        
        checker = SpellChecker()
        languages = checker.get_supported_languages()
        
        assert isinstance(languages, list)
        assert len(languages) == 1
        assert languages[0]['code'] == 'en' 
