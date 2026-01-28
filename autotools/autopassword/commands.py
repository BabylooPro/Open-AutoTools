import click
import base64
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates
from .core import generate_password, generate_encryption_key, analyze_password_strength

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Security'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'basic', 'args': []},
    {'name': 'length', 'args': ['--length', '32']},
    {'name': 'no-special', 'args': ['--no-special']},
    {'name': 'no-numbers', 'args': ['--no-numbers']},
    {'name': 'no-uppercase', 'args': ['--no-uppercase']},
    {'name': 'min-special', 'args': ['--min-special', '3']},
    {'name': 'min-numbers', 'args': ['--min-numbers', '3']},
    {'name': 'analysis', 'args': ['--analyze']},
    {'name': 'encryption', 'args': ['--gen-key']},
]

# CLI COMMAND TO GENERATE PASSWORDS OR ENCRYPTION KEYS
@click.command()
@click.option('--length', '-l', default=12, help='Password length (default: 12)')
@click.option('--no-uppercase', '-u', is_flag=True, help='Exclude uppercase letters')
@click.option('--no-numbers', '-n', is_flag=True, help='Exclude numbers')
@click.option('--no-special', '-s', is_flag=True, help='Exclude special characters')
@click.option('--min-special', '-m', default=1, help='Minimum number of special characters')
@click.option('--min-numbers', '-d', default=1, help='Minimum number of numbers')
@click.option('--analyze', '-a', is_flag=True, help='Analyze password strength')
@click.option('--gen-key', '-g', is_flag=True, help='Generate encryption key')
@click.option('--password-key', '-p', help='Generate key from password')
def autopassword(length, no_uppercase, no_numbers, no_special, min_special, min_numbers, analyze, gen_key, password_key):
    """
        GENERATES SECURE PASSWORDS OR ENCRYPTION KEYS.

        \b
        FEATURES:
            - Generate random passwords with customizable length
            - Control character sets (uppercase, numbers, special)
            - Set minimum requirements for special characters and numbers
            - Analyze password strength
            - Generate encryption keys
            - Derive keys from passwords

        \b
        EXAMPLES:
            autopassword
            autopassword --length 16
            autopassword --length 20 --analyze
            autopassword --no-special --min-numbers 3
            autopassword --gen-key
            autopassword --password-key "mypassword" --analyze
    """

    # DISPLAYS PASSWORD STRENGTH ANALYSIS RESULTS
    def show_analysis(text, prefix=""):
        if not analyze: return
        with LoadingAnimation(): analysis = analyze_password_strength(text)

        click.echo(f"\n{prefix}Strength Analysis:")
        click.echo(f"Strength: {analysis['strength']}")
        click.echo(f"Score: {analysis['score']}/5")

        if analysis['suggestions']:
            click.echo("\nSuggestions for improvement:")
            for suggestion in analysis['suggestions']: click.echo(f"- {suggestion}")

    # GENERATES ENCRYPTION KEY IF GEN_KEY FLAG IS SET
    if gen_key:
        with LoadingAnimation(): key = generate_encryption_key()
        key_str = key.decode()
        click.echo(f"Encryption Key: {key_str}")
        if analyze: show_analysis(key_str, "Key ")
        return
    
    # GENERATES ENCRYPTION KEY FROM PASSWORD IF PASSWORD_KEY FLAG IS SET
    if password_key:
        with LoadingAnimation(): key, salt = generate_encryption_key(password_key)
        key_str = key.decode()
        click.echo(f"Derived Key: {key_str}")
        click.echo(f"Salt: {base64.b64encode(salt).decode()}")

        if analyze:
            click.echo("\nAnalyzing source password:")
            show_analysis(password_key, "Password ")
            click.echo("\nAnalyzing generated key:")
            show_analysis(key_str, "Key ")

        return

    # GENERATES PASSWORD IF NO OTHER OPTIONS ARE SET
    with LoadingAnimation():
        password = generate_password(
            length=length,
            use_uppercase=not no_uppercase,
            use_numbers=not no_numbers,
            use_special=not no_special,
            min_special=min_special,
            min_numbers=min_numbers,
        )

    click.echo(f"Generated Password: {password}")
    show_analysis(password, "Password ")

    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg)
