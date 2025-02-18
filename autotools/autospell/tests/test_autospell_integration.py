import pytest
from unittest.mock import patch, Mock, PropertyMock, call
from click.testing import CliRunner
from autotools.autospell.commands import autospell
from autotools.autospell.core import SpellChecker

# MOCK DATA
MOCK_CORRECTIONS = {
    'corrections': [
        {
            'message': 'Spelling mistake',
            'context': 'This is a speling mistake',
            'offset': 10,
            'length': 7,
            'category': 'SPELLING',
            'rule_id': 'SPELLING_ERROR',
            'replacements': ['spelling'],
            'severity': 'high'
        }
    ],
    'statistics': {
        'total_errors': 1,
        'categories': {'SPELLING': 1},
        'severity': {'high': 1, 'medium': 0, 'low': 0}
    },
    'language': {
        'code': 'en',
        'name': 'ENGLISH',
        'confidence': 0.9
    }
}

MOCK_LANGUAGES = [
    {'code': 'en', 'name': 'English', 'variants': ['US', 'UK']},
    {'code': 'fr', 'name': 'French', 'variants': []}
]

# INTEGRATION TESTS

@pytest.fixture
def runner():
    return CliRunner()

# TEST BASIC CLI FUNCTIONALITY
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_basic(mock_spellchecker, runner):
    """TEST BASIC CLI FUNCTIONALITY"""
    mock_checker = Mock()
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['This is a test'])
    
    assert result.exit_code == 0
    assert mock_checker.check_text.call_args_list[-1] == call('This is a test', 'auto')

# TEST CLI WITH SPECIFIED LANGUAGE
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_with_language(mock_spellchecker, runner):
    """TEST CLI WITH SPECIFIED LANGUAGE"""
    mock_checker = Mock()
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['This is a test', '--lang', 'en'])
    
    assert result.exit_code == 0
    assert mock_checker.check_text.call_args_list[-1] == call('This is a test', 'en')

# TEST CLI FIX COMMAND
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_fix(mock_spellchecker, runner):
    """TEST CLI FIX COMMAND"""
    mock_checker = Mock()
    mock_checker.fix_text.return_value = "This is a corrected text"
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['--fix', 'This is a test'])
    
    assert result.exit_code == 0
    assert mock_checker.fix_text.call_args_list[-1] == call('This is a test', 'auto', copy_to_clipboard=True, ignore=(), interactive=False)

# TEST CLI FIX WITH CLIPBOARD COPY
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_fix_with_copy(mock_spellchecker, runner):
    """TEST CLI FIX WITH CLIPBOARD COPY"""
    mock_checker = Mock()
    mock_checker.fix_text.return_value = "This is a corrected text"
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['--fix', '--copy', 'This is a test'])
    
    assert result.exit_code == 0
    assert mock_checker.fix_text.call_args_list[-1] == call('This is a test', 'auto', copy_to_clipboard=True, ignore=(), interactive=False)

# TEST CLI FIX IN INTERACTIVE MODE
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_fix_interactive(mock_spellchecker, runner):
    """TEST CLI FIX IN INTERACTIVE MODE"""
    mock_checker = Mock()
    mock_checker.fix_text.return_value = "This is a corrected text"
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['--fix', '--interactive', 'This is a test'])
    
    assert result.exit_code == 0
    assert mock_checker.fix_text.call_args_list[-1] == call('This is a test', 'auto', copy_to_clipboard=True, ignore=(), interactive=True)

# TEST CLI FIX WITH IGNORED RULES
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_fix_with_ignore(mock_spellchecker, runner):
    """TEST CLI FIX WITH IGNORED RULES"""
    mock_checker = Mock()
    mock_checker.fix_text.return_value = "This is a corrected text"
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['--fix', '--ignore', 'spelling', 'This is a test'])
    
    assert result.exit_code == 0
    assert mock_checker.fix_text.call_args_list[-1] == call('This is a test', 'auto', copy_to_clipboard=True, ignore=('spelling',), interactive=False)

# TEST CLI LIST LANGUAGES COMMAND
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_languages(mock_spellchecker, runner):
    """TEST CLI LIST LANGUAGES COMMAND"""
    mock_checker = Mock()
    mock_checker.get_supported_languages.return_value = MOCK_LANGUAGES
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, ['--list-languages'])
    
    assert result.exit_code == 0
    assert mock_checker.get_supported_languages.call_count == 1

# TEST CLI WITH NO TEXT PROVIDED
@patch('autotools.autospell.commands.SpellChecker')
def test_autospell_cli_no_text(mock_spellchecker, runner):
    """TEST CLI WITH NO TEXT PROVIDED"""
    mock_checker = Mock()
    mock_checker.check_text.return_value = MOCK_CORRECTIONS
    type(mock_checker).corrections = PropertyMock(return_value=MOCK_CORRECTIONS['corrections'])
    mock_spellchecker.return_value = mock_checker
    
    result = runner.invoke(autospell, [''])
    
    assert result.exit_code == 0
    assert "Error: Please provide text to check" in result.output
