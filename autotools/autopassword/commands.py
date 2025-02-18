import click
import base64
from .core import generate_password, generate_encryption_key, analyze_password_strength
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

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
def autopassword(length, no_uppercase, no_numbers, no_special, 
                 min_special, min_numbers, analyze, gen_key, password_key):
    """Generate secure passwords and encryption keys."""
    
    def show_analysis(text, prefix=""):
        """Helper function to show password/key analysis"""
        if analyze:
            with LoadingAnimation():
                analysis = analyze_password_strength(text)
            click.echo(f"\n{prefix}Strength Analysis:")
            click.echo(f"Strength: {analysis['strength']}")
            click.echo(f"Score: {analysis['score']}/5")
            if analysis['suggestions']:
                click.echo("\nSuggestions for improvement:")
                for suggestion in analysis['suggestions']:
                    click.echo(f"- {suggestion}")
    
    # GENERATE KEY
    if gen_key:
        with LoadingAnimation():
            key = generate_encryption_key()
        key_str = key.decode()
        click.echo(f"Encryption Key: {key_str}")
        if analyze:
            show_analysis(key_str, "Key ")
        return
    
    # GENERATE KEY FROM PASSWORD
    if password_key:
        with LoadingAnimation():
            key, salt = generate_encryption_key(password_key)
        key_str = key.decode()
        click.echo(f"Derived Key: {key_str}")
        click.echo(f"Salt: {base64.b64encode(salt).decode()}")
        if analyze:
            click.echo("\nAnalyzing source password:")
            show_analysis(password_key, "Password ")
            click.echo("\nAnalyzing generated key:")
            show_analysis(key_str, "Key ")
        return
    
    # GENERATE PASSWORD
    with LoadingAnimation():
        password = generate_password(
            length=length,
            use_uppercase=not no_uppercase,
            use_numbers=not no_numbers,
            use_special=not no_special,
            min_special=min_special,
            min_numbers=min_numbers,
        )
    
    # SHOW PASSWORD
    click.echo(f"Generated Password: {password}")
    show_analysis(password, "Password ")
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
