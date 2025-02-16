import pytest
from autotools.autolower.core import autolower_transform

# UNIT TESTS

# TEST FOR BASIC STRING TRANSFORMATION
def test_autolower_transform_basic():
    """TEST BASIC STRING TRANSFORMATION"""
    assert autolower_transform("HELLO") == "hello"
    assert autolower_transform("Hello World") == "hello world"
    assert autolower_transform("123") == "123"

# TEST FOR EMPTY STRING
def test_autolower_transform_empty():
    """TEST EMPTY STRING"""
    assert autolower_transform("") == ""

# TEST FOR SPECIAL CHARACTERS
def test_autolower_transform_special_chars():
    """TEST STRING WITH SPECIAL CHARACTERS"""
    assert autolower_transform("HELLO@WORLD.COM") == "hello@world.com"
    assert autolower_transform("HELLO-WORLD!") == "hello-world!"

# TEST FOR MIXED CASE STRING
def test_autolower_transform_mixed_case():
    """TEST MIXED CASE STRING"""
    assert autolower_transform("HeLLo WoRLD") == "hello world"

# TEST FOR WHITESPACE
def test_autolower_transform_whitespace():
    """TEST STRING WITH WHITESPACE"""
    assert autolower_transform("  HELLO  WORLD  ") == "  hello  world  "
    assert autolower_transform("\tHELLO\nWORLD") == "\thello\nworld"

# TEST FOR NUMBERS
def test_autolower_transform_numbers():
    """TEST STRING WITH NUMBERS"""
    assert autolower_transform("HELLO123WORLD") == "hello123world"
    assert autolower_transform("123HELLO456WORLD789") == "123hello456world789"

# TEST FOR UNICODE CHARACTERS
def test_autolower_transform_unicode():
    """TEST UNICODE CHARACTERS"""
    assert autolower_transform("HÉLLO WÖRLD") == "héllo wörld"
    assert autolower_transform("こんにちは") == "こんにちは"  # JAPANESE SHOULD REMAIN UNCHANGED 
