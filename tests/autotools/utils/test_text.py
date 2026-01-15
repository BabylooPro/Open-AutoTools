import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from autotools.utils.text import safe_text, is_ci_environment, mask_ipv4, mask_ipv6, mask_ips_in_text, mask_sensitive_info

# TEST FOR SAFE TEXT WITH NON-STRING INPUT
def test_safe_text_non_string():
    assert safe_text(123) == 123
    assert safe_text(None) is None
    assert safe_text([]) == []

# TEST FOR SAFE TEXT WITH ENCODABLE TEXT
def test_safe_text_encodable():
    result = safe_text("Hello World")
    assert result == "Hello World"

# TEST FOR SAFE TEXT WITH UTF8 ENCODING
@patch('sys.stdout')
def test_safe_text_utf8_encoding(mock_stdout):
    mock_stdout.encoding = 'utf-8'
    result = safe_text("Hello [OK] World")
    assert result == "Hello [OK] World"

# TEST FOR SAFE TEXT WITH UNICODE THAT FAILS ENCODING
@patch('sys.stdout')
def test_safe_text_unicode_fails_encoding(mock_stdout):
    mock_stdout.encoding = 'cp1252'
    result = safe_text("Test émojî unicode")
    assert isinstance(result, str)
    assert len(result) > 0

# TEST FOR SAFE TEXT WITH UNICODE CHARACTERS
@patch('sys.stdout')
def test_safe_text_unicode_characters(mock_stdout):
    mock_stdout.encoding = 'cp1252'
    text = "Test with émojî and spécial chars"
    result = safe_text(text)
    assert isinstance(result, str)
    assert len(result) > 0

# TEST FOR SAFE TEXT WITH NO ENCODING ATTRIBUTE
@patch('sys.stdout')
def test_safe_text_no_encoding_attribute(mock_stdout):
    del mock_stdout.encoding
    result = safe_text("Hello World")
    assert result == "Hello World"

# TEST FOR SAFE TEXT WITH ENCODING FAILURE
@patch('sys.stdout')
def test_safe_text_encoding_failure(mock_stdout):
    mock_stdout.encoding = 'cp1252'
    text = "Test émojî unicode"
    result = safe_text(text)
    assert isinstance(result, str)
    assert len(result) > 0

# TEST FOR SAFE TEXT WITH COMPLETE ENCODING FAILURE
@patch('sys.stdout')
def test_safe_text_complete_encoding_failure(mock_stdout):
    mock_stdout.encoding = 'ascii'
    text = "Test with émojî and spécial chars"
    result = safe_text(text)
    assert isinstance(result, str)
    assert isinstance(result, str)
    assert len(result) > 0

# TEST FOR SAFE TEXT WITH ENCODING FAILURE IN BOTH ATTEMPTS
@patch('sys.stdout')
def test_safe_text_encoding_failure_both_attempts(mock_stdout):
    mock_stdout.encoding = 'invalid-encoding-xyz123'
    text = "Test with émojî unicode"
    
    result = safe_text(text)
    assert isinstance(result, str)
    assert len(result) > 0
    assert isinstance(result, str)

# TEST FOR SAFE TEXT WITH NONE ENCODING
@patch('sys.stdout')
def test_safe_text_none_encoding(mock_stdout):
    mock_stdout.encoding = None
    result = safe_text("Hello World")
    assert result == "Hello World"

# TEST FOR SAFE TEXT WITH EMPTY STRING
def test_safe_text_empty_string():
    result = safe_text("")
    assert result == ""

# TEST FOR SAFE TEXT WITH SPECIAL CHARACTERS
def test_safe_text_special_characters():
    result = safe_text("Hello\nWorld\tTest")
    assert result == "Hello\nWorld\tTest"

# TEST FOR CI ENVIRONMENT DETECTION
# FALSE
def test_is_ci_environment_false():
    with patch.dict(os.environ, {}, clear=True):
        assert is_ci_environment() is False

# CI VARIABLE
def test_is_ci_environment_ci_var():
    with patch.dict(os.environ, {'CI': 'true'}, clear=False):
        assert is_ci_environment() is True

# GITHUB ACTIONS
def test_is_ci_environment_github_actions():
    with patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'}, clear=False):
        assert is_ci_environment() is True

# GITLAB CI
def test_is_ci_environment_gitlab_ci():
    with patch.dict(os.environ, {'GITLAB_CI': 'true'}, clear=False):
        assert is_ci_environment() is True

# TEST FOR MASK IPV4
# VALID
def test_mask_ipv4_valid():
    assert mask_ipv4('192.168.1.1') == 'xxx.xxx.xxx.xxx'
    assert mask_ipv4('10.0.0.1') == 'xxx.xxx.xxx.xxx'
    assert mask_ipv4('172.16.0.1') == 'xxx.xxx.xxx.xxx'

# INVALID
def test_mask_ipv4_invalid():
    assert mask_ipv4('not.an.ip') == 'not.an.ip'
    assert mask_ipv4('192.168.1') == '192.168.1'
    assert mask_ipv4('999.999.999.999') == '999.999.999.999'

# EDGE CASES
def test_mask_ipv4_edge_cases():
    assert mask_ipv4('') == ''
    assert mask_ipv4('192.168.1.256') == '192.168.1.256'

# TEST FOR MASK IPV6
def test_mask_ipv6_valid():
    assert mask_ipv6('2001:0db8::1') == 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx'
    assert mask_ipv6('2001:db8:85a3::8a2e:370:7334') == 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx'
    assert mask_ipv6('::1') == 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx'

def test_mask_ipv6_with_interface():
    assert mask_ipv6('2001:db8::1%eth0') == 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx'

def test_mask_ipv6_invalid():
    assert mask_ipv6('not.an.ipv6') == 'not.an.ipv6'
    assert mask_ipv6('192.168.1.1') == '192.168.1.1'

def test_mask_ipv6_edge_cases():
    assert mask_ipv6('') == ''

# TEST FOR MASK IPS 
# MASK IPV4
def test_mask_ips_in_text_ipv4():
    text = "My IP is 192.168.1.1 and server is 10.0.0.1"
    result = mask_ips_in_text(text)
    assert 'xxx.xxx.xxx.xxx' in result
    assert '192.168.1.1' not in result
    assert '10.0.0.1' not in result

# MASK IPV6
def test_mask_ips_in_text_ipv6():
    text = "My IPv6 is 2001:db8::1"
    result = mask_ips_in_text(text)
    assert 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx' in result
    assert '2001:db8::1' not in result

# MIXED
def test_mask_ips_in_text_mixed():
    text = "IPv4: 192.168.1.1 IPv6: 2001:db8::1"
    result = mask_ips_in_text(text)
    assert 'xxx.xxx.xxx.xxx' in result
    assert 'xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx' in result

# NO IPS
def test_mask_ips_in_text_no_ips():
    text = "This is just regular text"
    result = mask_ips_in_text(text)
    assert result == text

# EDGE CASES
def test_mask_ips_in_text_edge_cases():
    assert mask_ips_in_text('') == ''
    assert mask_ips_in_text('192.168.1.1.extra') != '192.168.1.1.extra'
    assert mask_ips_in_text(None) is None
    assert mask_ips_in_text(123) == 123
    assert mask_ips_in_text([]) == []

# TEST FOR MASK SENSITIVE INFO
# WITH IPS
def test_mask_sensitive_info_with_ips():
    text = "IP: 192.168.1.1"
    result = mask_sensitive_info(text, mask_ips=True)
    assert 'xxx.xxx.xxx.xxx' in result

# WITH COORDINATES
def test_mask_sensitive_info_with_coordinates():
    text = "Location: 37.4056,-122.0775"
    result = mask_sensitive_info(text, mask_ips=True)
    assert '[REDACTED]' in result
    assert '37.4056,-122.0775' not in result

# WITH BOTH IPS AND COORDINATES
def test_mask_sensitive_info_with_both():
    text = "IP: 192.168.1.1 Location: 37.4056,-122.0775"
    result = mask_sensitive_info(text, mask_ips=True)
    assert 'xxx.xxx.xxx.xxx' in result
    assert '[REDACTED]' in result

# NO MASK IPS
def test_mask_sensitive_info_no_mask_ips():
    text = "IP: 192.168.1.1"
    result = mask_sensitive_info(text, mask_ips=False)
    assert '192.168.1.1' in result

# EDGE CASES
def test_mask_sensitive_info_edge_cases():
    assert mask_sensitive_info('') == ''
    assert mask_sensitive_info('no sensitive data') == 'no sensitive data'
    assert mask_sensitive_info(None) is None
    assert mask_sensitive_info(123) == 123
    assert mask_sensitive_info([]) == []
