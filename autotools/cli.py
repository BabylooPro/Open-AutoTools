import os
import click
import base64
from autotools.autocaps.core import autocaps_transform
from autotools.autolower.core import autolower_transform
from autotools.downloader.core import download_youtube_video, download_file
from autotools.password.core import (
    generate_password,
    generate_encryption_key,
    analyze_password_strength
)
from translate import Translator
from autotools.autotranslate.core import translate_text, get_supported_languages

# CLI FUNCTION DEFINITION
@click.group()
def cli():
    """Autotools is a set of tools for text capitalization and file downloading."""
    pass

# AUTOTOOLS COMMAND LINE INTERFACE FUNCTION DEFINITION FOR SHOW HELP MESSAGE
@cli.command()
def autotools():
    return

# AUTOCAPS COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autocaps(text):
    result = autocaps_transform(text)
    click.echo(result)

# AUTOLOWER CASE COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autolower(text):
    result = autolower_transform(text)
    click.echo(result)

# AUTODOWNLOAD COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('url')
@click.option('--format', type=click.Choice(['mp4', 'mp3'], case_sensitive=False), default='mp4', help='Output file format (mp4 or mp3)')
@click.option('--quality', type=click.Choice(['best', '1440p', '1080p', '720p', '480p', '360p', '240p'], case_sensitive=False), default='best', help='"Video quality (mp4 only)"')
def autodownload(url, format, quality):
    if "youtube.com" in url or "youtu.be" in url:
        download_youtube_video(url, format, quality)
    else:
        download_file(url)

# AUTOPASSWORD COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.option('--length', '-l', default=12, help='Password length (default: 12)')
@click.option('--no-uppercase', is_flag=True, help='Exclude uppercase letters')
@click.option('--no-numbers', is_flag=True, help='Exclude numbers')
@click.option('--no-special', is_flag=True, help='Exclude special characters')
@click.option('--min-special', default=1, help='Minimum number of special characters')
@click.option('--min-numbers', default=1, help='Minimum number of numbers')
@click.option('--analyze', is_flag=True, help='Analyze password strength')
@click.option('--gen-key', is_flag=True, help='Generate encryption key')
@click.option('--password-key', help='Generate key from password')
def autopassword(length, no_uppercase, no_numbers, no_special, 
                 min_special, min_numbers, analyze, gen_key, password_key):
    """Generate secure passwords and encryption keys."""
    
    ## HELPER FUNCTION TO SHOW PASSWORD/KEY ANALYSIS
    def show_analysis(text, prefix=""):
        """Helper function to show password/key analysis"""
        if analyze:
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
        key = generate_encryption_key()
        key_str = key.decode()
        click.echo(f"Encryption Key: {key_str}")
        if analyze:
            show_analysis(key_str, "Key ")
        return
    
    # GENERATE KEY FROM PASSWORD
    if password_key:
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

# TRANSLATE COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text', required=False)
@click.option('--to', default='en', help='Target language (default: en)')
@click.option('--from', 'from_lang', help='Source language (default: auto-detect)')
@click.option('--list-languages', is_flag=True, help='List all supported languages')
@click.option('--copy', is_flag=True, help='Copy translation to clipboard')
@click.option('--detect', is_flag=True, help='Show detected source language')
def autotranslate(text: str, to: str, from_lang: str, list_languages: bool, 
                  copy: bool, detect: bool):
    """TRANSLATE TEXT TO SPECIFIED LANGUAGE (AUTO-DETECTS SOURCE LANGUAGE)"""
    
    # LIST ALL SUPPORTED LANGUAGES
    if list_languages:
        click.echo("\nSupported Languages:")
        for code, name in get_supported_languages().items():
            click.echo(f"{code:<8} {name}")
        return
    
    # CHECK IF TEXT IS PROVIDED
    if not text:
        click.echo("Error: Please provide text to translate")
        return
        
    result = translate_text(text, to_lang=to, from_lang=from_lang, 
                          copy=copy, detect_lang=detect)
    click.echo(result)

# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()
