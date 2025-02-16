import pytest
from autotools.autopassword.core import generate_password, generate_encryption_key, analyze_password_strength
import string
import base64
from cryptography.fernet import Fernet

# UNIT TESTS

# TEST FOR DEFAULT PASSWORD GENERATION
def test_generate_password_default():
    """TEST PASSWORD GENERATION WITH DEFAULT PARAMETERS"""
    password = generate_password()
    assert len(password) == 12
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# TEST FOR PASSWORD GENERATION WITH CUSTOM PARAMETERS
def test_generate_password_custom():
    """TEST PASSWORD GENERATION WITH CUSTOM PARAMETERS"""
    password = generate_password(
        length=16,
        use_uppercase=False,
        use_numbers=True,
        use_special=False,
        min_numbers=2
    )
    assert len(password) == 16
    assert not any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert sum(c.isdigit() for c in password) >= 2
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# TEST FOR PASSWORD GENERATION WITH MINIMUM REQUIREMENTS
def test_generate_password_min_requirements():
    """TEST PASSWORD GENERATION WITH MINIMUM REQUIREMENTS"""
    password = generate_password(
        length=10,
        min_special=2,
        min_numbers=2
    )
    assert len(password) == 10
    assert sum(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password) >= 2
    assert sum(c.isdigit() for c in password) >= 2

# TEST FOR RANDOM ENCRYPTION KEY GENERATION
def test_generate_encryption_key_random():
    """TEST RANDOM ENCRYPTION KEY GENERATION"""
    key = generate_encryption_key()
    assert isinstance(key, bytes)
    assert len(key) == 44  # BASE64 ENCODED 32-BYTE KEY
    # VERIFY IT'S A VALID FERNET KEY
    Fernet(key)

# TEST FOR ENCRYPTION KEY GENERATION FROM PASSWORD
def test_generate_encryption_key_from_password():
    """TEST ENCRYPTION KEY GENERATION FROM PASSWORD"""
    password = "testpassword123"
    key, salt = generate_encryption_key(password)
    assert isinstance(key, bytes)
    assert isinstance(salt, bytes)
    assert len(key) == 44  # BASE64 ENCODED 32-BYTE KEY
    assert len(salt) == 16
    # VERIFY KEY GENERATION IS DETERMINISTIC
    key2, _ = generate_encryption_key(password, salt)
    assert key == key2

# TEST FOR PASSWORD STRENGTH ANALYSIS - VERY WEAK
def test_analyze_password_strength_very_weak():
    """TEST PASSWORD STRENGTH ANALYSIS - VERY WEAK"""
    result = analyze_password_strength("abc")
    assert result['score'] == 1
    assert result['strength'] == "Weak"
    assert len(result['suggestions']) > 0

# TEST FOR PASSWORD STRENGTH ANALYSIS - STRONG
def test_analyze_password_strength_strong():
    """TEST PASSWORD STRENGTH ANALYSIS - STRONG"""
    result = analyze_password_strength("Test123!@#")
    assert result['score'] >= 4
    assert result['strength'] in ["Strong", "Very Strong"]
    assert len(result['suggestions']) == 0

# TEST FOR PASSWORD STRENGTH ANALYSIS - ALL CHARACTER TYPES
def test_analyze_password_strength_all_types():
    """TEST PASSWORD STRENGTH ANALYSIS - ALL CHARACTER TYPES"""
    result = analyze_password_strength("TestPass123!@#")
    assert result['score'] == 6
    assert result['strength'] == "Very Strong"
    assert len(result['suggestions']) == 0 
