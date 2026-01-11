# AutoPassword

## Description

Generates secure random passwords and encryption keys with customizable options. Uses cryptographically secure random number generation (`secrets` module) for password generation. Encryption keys use Fernet symmetric encryption, and password-derived keys use PBKDF2HMAC with 100,000 iterations for key derivation.

## Usage

```bash
autopassword --length 16
autopassword --no-special --length 8
autopassword --gen-key
autopassword --password-key "your-password" --analyze
```

## Options

-   `--length, -l`: Set password length (default: 12)
-   `--no-uppercase, -u`: Exclude uppercase letters
-   `--no-numbers, -n`: Exclude numbers
-   `--no-special, -s`: Exclude special characters
-   `--min-special, -m`: Minimum number of special characters (default: 1)
-   `--min-numbers, -d`: Minimum number of numbers (default: 1)
-   `--analyze, -a`: Show password strength analysis (score 0-5 with improvement suggestions)
-   `--gen-key, -g`: Generate a random encryption key
-   `--password-key, -p`: Generate an encryption key from password

## Examples

```bash
# Generate a default password (12 characters)
autopassword

# Generate a 16-character password
autopassword --length 16

# Generate password without special characters
autopassword --no-special --length 8

# Generate password and analyze strength
autopassword --length 20 --analyze

# Generate a random encryption key
autopassword --gen-key

# Generate encryption key from password
autopassword --password-key "my-secret-password" --analyze
# Note: Also displays the salt in base64 format for key derivation
```
