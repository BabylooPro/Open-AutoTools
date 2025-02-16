import os
import click
import base64
import json as json_module
from autotools.autocaps.core import autocaps_transform
from autotools.autolower.core import autolower_transform
from autotools.autodownload.core import download_youtube_video, download_file
from autotools.password.core import (
    generate_password,
    generate_encryption_key,
    analyze_password_strength
)
from translate import Translator
from autotools.autotranslate.core import translate_text, get_supported_languages
import yt_dlp
from autotools import autodownload, autolower, autocaps, autoip
import argparse
from autotools.autospell.core import SpellChecker
from urllib.parse import urlparse

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

# AUTOIP COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.option('--test', '-t', is_flag=True, help='Run connectivity tests')
@click.option('--speed', '-s', is_flag=True, help='Run internet speed test')
@click.option('--monitor', '-m', is_flag=True, help='Monitor network traffic')
@click.option('--ports', '-p', is_flag=True, help='Check common ports status')
@click.option('--dns', '-d', is_flag=True, help='Show DNS servers')
@click.option('--location', '-l', is_flag=True, help='Show IP location info')
@click.option('--no-ip', '-n', is_flag=True, help='Hide IP addresses display')
def autoip(test, speed, monitor, ports, dns, location, no_ip):
    """DISPLAY LOCAL AND PUBLIC IP ADDRESSES"""
    from autotools import autoip
    autoip.run(test, speed, monitor, ports, dns, location, no_ip)

# AUTOSPELL COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('texts', nargs=-1)
@click.option('--lang', '-l', default='auto', help='Language code (auto for detection)')
@click.option('--fix', '-f', is_flag=True, help='Auto-fix text and copy to clipboard')
@click.option('--copy', '-c', is_flag=True, help='Copy result to clipboard')
@click.option('--list-languages', is_flag=True, help='List supported languages')
@click.option('--json', '-j', is_flag=True, help='Output results as JSON')
@click.option('--ignore', '-i', multiple=True, 
    type=click.Choice(['spelling', 'grammar', 'style', 'punctuation']),
    help='Error types to ignore')
@click.option('--interactive', '-n', is_flag=True, 
    help='Interactive mode - confirm each correction')
@click.option('--output', '-o', type=click.Path(), 
    help='Save corrections to file')
def autospell(texts: tuple, lang: str, fix: bool, copy: bool, list_languages: bool, 
              json: bool, ignore: tuple, interactive: bool, output: str):
    """CHECK AND FIX SPELLING/GRAMMAR IN TEXT"""
    checker = SpellChecker()
    
    # LIST ALL SUPPORTED LANGUAGES
    if list_languages:
        languages = checker.get_supported_languages()
        if json:
            result = {'languages': languages}
            click.echo(json_module.dumps(result, indent=2))
        else:
            click.echo("\nSupported Languages:")
            for lang in languages:
                click.echo(f"{lang['code']:<8} {lang['name']}")
        return
        
    # CHECK AND FIX SPELLING/GRAMMAR IN TEXT
    for text in texts:
        if not text:
            click.echo("Error: Please provide text to check")
            continue
        
        # FIX SPELLING/GRAMMAR IN TEXT
        if fix:
            # CORRECT TEXT WITH SPELL CHECKER
            corrected = checker.fix_text(text, lang, copy_to_clipboard=True, 
                                       ignore=ignore, interactive=interactive)
            result = {'corrected_text': corrected} # RESULT TO RETURN
            
            # OUTPUT RESULTS AS JSON
            if json:
                click.echo(json_module.dumps(result, indent=2))
            else:
                # LANGUAGE INFORMATION
                check_result = checker.check_text(text, lang)
                lang_info = check_result['language']
                click.echo(f"\nLanguage detected: {lang_info['name']} ({lang_info['code']})")
                click.echo(f"Confidence: {lang_info['confidence']:.2%}")
                click.echo("\nCorrected text (copied to clipboard):")
                click.echo(corrected)
                
            # SAVE CORRECTIONS TO FILE
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    if json:
                        json_module.dump(result, f, indent=2)
                    else:
                        f.write(corrected)
        else:
            # CHECK SPELLING/GRAMMAR IN TEXT
            check_result = checker.check_text(text, lang)
            
            # OUTPUT RESULTS AS JSON
            if json:
                click.echo(json_module.dumps(check_result, indent=2))
            else:
                lang_info = check_result['language']
                click.echo(f"\nLanguage detected: {lang_info['name']} ({lang_info['code']})")
                click.echo(f"Confidence: {lang_info['confidence']:.2%}")
                click.echo(f"Total errors found: {check_result['statistics']['total_errors']}")
                
                # CORRECTIONS SUGGESTED
                if check_result['corrections']:
                    click.echo("\nCorrections suggested:")
                    for i, corr in enumerate(check_result['corrections'], 1):
                        click.echo(f"\n{i}. [{corr['severity'].upper()}] {corr['message']}")
                        click.echo(f"   Context: {corr['context']}")
                        if corr['replacements']:
                            click.echo(f"   Suggestions: {', '.join(corr['replacements'][:3])}")
            
            # SAVE CHECK RESULT TO FILE
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    if json:
                        json_module.dump(check_result, f, indent=2)
                    else:
                        # WRITE A HUMAN-READABLE REPORT
                        f.write(f"Language: {lang_info['name']} ({lang_info['code']})\n")
                        f.write(f"Confidence: {lang_info['confidence']:.2%}\n")
                        f.write(f"Total errors: {check_result['statistics']['total_errors']}\n\n")
                        
                        # CORRECTIONS SUGGESTED
                        if check_result['corrections']:
                            f.write("Corrections suggested:\n")
                            for i, corr in enumerate(check_result['corrections'], 1):
                                f.write(f"\n{i}. [{corr['severity'].upper()}] {corr['message']}\n")
                                f.write(f"   Context: {corr['context']}\n")
                                if corr['replacements']:
                                    f.write(f"   Suggestions: {', '.join(corr['replacements'][:3])}\n")

# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()

def download_video(url):
    try:
        # CONFIGURE YT-DLP WITH COOKIES AND HEADERS
        yt_opts = {
            'cookiefile': '~/cookies.txt',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

# REMOVE OR COMMENT OUT THE NEW ARGPARSE-BASED MAIN FUNCTION
# def main():
#     parser = argparse.ArgumentParser()
#     ...
