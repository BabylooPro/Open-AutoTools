import pytest
from autotools.autocaps.core import autocaps_transform

# UNIT TESTS

# TEST FOR BASIC STRING TRANSFORMATION
def test_autocaps_transform_basic():
    """TEST BASIC STRING TRANSFORMATION"""
    assert autocaps_transform("hello") == "HELLO"
    assert autocaps_transform("Hello World") == "HELLO WORLD"
    assert autocaps_transform("123") == "123"

# TEST FOR EMPTY STRING
def test_autocaps_transform_empty():
    """TEST EMPTY STRING"""
    assert autocaps_transform("") == ""

# TEST FOR SPECIAL CHARACTERS
def test_autocaps_transform_special_chars():
    """TEST STRING WITH SPECIAL CHARACTERS"""
    assert autocaps_transform("hello@world.com") == "HELLO@WORLD.COM"
    assert autocaps_transform("hello-world!") == "HELLO-WORLD!"

# TEST FOR MIXED CASE STRING
def test_autocaps_transform_mixed_case():
    """TEST MIXED CASE STRING"""
    assert autocaps_transform("HeLLo WoRLD") == "HELLO WORLD"

# TEST FOR WHITESPACE
def test_autocaps_transform_whitespace():
    """TEST STRING WITH WHITESPACE"""
    assert autocaps_transform("  hello  world  ") == "  HELLO  WORLD  "
    assert autocaps_transform("\thello\nworld") == "\tHELLO\nWORLD"

# TEST FOR NUMBERS
def test_autocaps_transform_numbers():
    """TEST STRING WITH NUMBERS"""
    assert autocaps_transform("hello123world") == "HELLO123WORLD"
    assert autocaps_transform("123hello456world789") == "123HELLO456WORLD789"

# TEST FOR UNICODE CHARACTERS
def test_autocaps_transform_unicode():
    """TEST UNICODE CHARACTERS"""
    assert autocaps_transform("héllo wörld") == "HÉLLO WÖRLD"
    assert autocaps_transform("こんにちは") == "こんにちは"  # JAPANESE SHOULD REMAIN UNCHANGED 
