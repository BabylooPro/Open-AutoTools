import string
import random
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# GENERATES A SECURE RANDOM PASSWORD WITH SPECIFIED REQUIREMENTS
def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True, min_special=1, min_numbers=1):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ''
    numbers = string.digits if use_numbers else ''
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_special else ''
    all_chars = lowercase + uppercase + numbers + special
    password = []
    password.append(secrets.choice(lowercase))

    if use_uppercase: password.append(secrets.choice(uppercase))
    if use_numbers: password.extend(secrets.choice(numbers) for _ in range(min_numbers))
    if use_special: password.extend(secrets.choice(special) for _ in range(min_special))

    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))
    random.shuffle(password)

    return ''.join(password)

# GENERATES ENCRYPTION KEY FOR FERNET SYMMETRIC ENCRYPTION
def generate_encryption_key(password=None, salt=None):
    if not password: return Fernet.generate_key()
    if not salt: salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

# ANALYZES PASSWORD STRENGTH AND PROVIDES IMPROVEMENT SUGGESTIONS
def analyze_password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: suggestions.append("Password should be at least 8 characters long")

    if any(c.isupper() for c in password): score += 1
    else: suggestions.append("Add uppercase letters")

    if any(c.islower() for c in password): score += 1
    else: suggestions.append("Add lowercase letters")

    if any(c.isdigit() for c in password): score += 1
    else: suggestions.append("Add numbers")

    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
    else: suggestions.append("Add special characters")

    return {
        'score': score,
        'strength': ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'][min(score, 4)],
        'suggestions': suggestions
    }
