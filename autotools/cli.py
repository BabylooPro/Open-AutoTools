import os
import click
import base64
import json as json_module
import pkg_resources
from autotools.autocaps.core import autocaps_transform
from autotools.autolower.core import autolower_transform
from autotools.autodownload.core import download_youtube_video, download_file
from autotools.autopassword.core import (
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
import requests
from packaging import version
from datetime import datetime

# CLI FUNCTION DEFINITION
@click.group()
@click.version_option(package_name='Open-AutoTools')
def cli():
    """A suite of automated tools for various tasks.
    
    Run 'autotools COMMAND --help' for more information on each command."""
    pass

# AUTOTOOLS COMMAND LINE INTERFACE FUNCTION DEFINITION FOR SHOW HELP MESSAGE
@cli.command()
@click.option('--version', '--v', is_flag=True, help='Show version and check for updates')
def autotools(version):
    """Display available commands and tool information."""
    if version:
        import pkg_resources
        import requests
        from packaging import version
        from datetime import datetime

        # GET CURRENT VERSION
        current_version = pkg_resources.get_distribution('Open-AutoTools').version
        click.echo(f"Open-AutoTools version {current_version}")

        try:
            # CHECK LATEST VERSION FROM GITHUB API
            response = requests.get("https://api.github.com/repos/BabylooPro/Open-AutoTools/releases/latest")
            if response.status_code == 200:
                data = response.json()
                latest_version = data["tag_name"].replace("v", "")
                # PARSE AND FORMAT RELEASE DATE
                published_date = datetime.strptime(data["published_at"], "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = published_date.strftime("%B %d, %Y")
                click.echo(f"Released: {formatted_date}")
                
                if version.parse(latest_version) > version.parse(current_version):
                    click.echo(click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True))
                    click.echo(click.style("Run 'pip install --upgrade Open-AutoTools' to update", fg='red'))
        except Exception:
            pass  # SILENTLY IGNORE UPDATE CHECK FAILURES
        return

    # SHOW COMMANDS LIST WITH BETTER FORMATTING
    ctx = click.get_current_context()
    commands = cli.list_commands(ctx)
    
    click.echo(click.style("\nOpen-AutoTools Commands:", fg='blue', bold=True))
    for cmd in sorted(commands):
        if cmd != 'autotools':
            cmd_obj = cli.get_command(ctx, cmd)
            help_text = cmd_obj.help or cmd_obj.short_help or ''
            click.echo(f"\n{click.style(cmd, fg='green', bold=True)}")
            click.echo(f"  {help_text}")
            
            # GET OPTIONS FOR EACH COMMAND
            if hasattr(cmd_obj, 'params'):
                click.echo(click.style("\n  Options:", fg='yellow'))
                for param in cmd_obj.params:
                    if isinstance(param, click.Option):
                        opts = '/'.join(param.opts)
                        help_text = param.help or ''
                        click.echo(f"    {click.style(opts, fg='yellow')}")
                        click.echo(f"      {help_text}")

    # SHOW USAGE EXAMPLES
    click.echo(click.style("\nUsage Examples:", fg='blue', bold=True))
    click.echo("  autotools --help         Show this help message")
    click.echo("  autotools --version      Show version information")
    click.echo("  autotools COMMAND        Run a specific command")
    click.echo("  autotools COMMAND --help Show help for a specific command")

    # CHECK FOR UPDATES
    update_msg = check_for_updates()
    if update_msg:
        click.echo(click.style("\nUpdate Available:", fg='red', bold=True))
        click.echo(update_msg)

def check_for_updates():
    """CHECK IF AN UPDATE IS AVAILABLE AND RETURN UPDATE MESSAGE IF NEEDED"""
    
    # GET CURRENT VERSION
    try:
        current_version = pkg_resources.get_distribution('Open-AutoTools').version
        
        # CHECK FOR UPDATES FROM GITHUB API RELEASES PAGE
        response = requests.get("https://api.github.com/repos/BabylooPro/Open-AutoTools/releases/latest")
        
        # CHECK IF RESPONSE IS SUCCESSFUL
        if response.status_code == 200:
            latest_version = response.json()["tag_name"].replace("v", "")
            if version.parse(latest_version) > version.parse(current_version):
                return f"\nUpdate available: v{latest_version}\nRun 'pip install --upgrade Open-AutoTools' to update"
    except Exception:
        pass
    return None

# AUTOCAPS COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autocaps(text):
    """Convert text to UPPERCASE."""
    result = autocaps_transform(text)
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# AUTOLOWER CASE COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text')
def autolower(text):
    """Convert text to lowercase."""
    result = autolower_transform(text)
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# AUTODOWNLOAD COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('url')
@click.option('--format', type=click.Choice(['mp4', 'mp3'], case_sensitive=False), 
              default='mp4', help='Output file format')
@click.option('--quality', type=click.Choice(['best', '1440p', '1080p', '720p', '480p', '360p', '240p'], 
              case_sensitive=False), default='best', help='Video quality (mp4 only)')
def autodownload(url, format, quality):
    """Download videos from YouTube or files from any URL.
    
    Supports YouTube video download with quality selection and format conversion (mp4/mp3).
    For non-YouTube URLs, downloads the file directly."""
    if "youtube.com" in url or "youtu.be" in url:
        download_youtube_video(url, format, quality)
    else:
        download_file(url)
        
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

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
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

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
    """Translate text to specified language."""
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
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

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
    """Display network information and diagnostics.
    
    Shows local and public IP addresses, runs network diagnostics,
    performs speed tests, monitors traffic, checks ports,
    displays DNS information and provides geolocation data."""
    from autotools import autoip
    autoip.run(test, speed, monitor, ports, dns, location, no_ip)
    update_msg = check_for_updates()
    
    # UPDATE CHECK AT THE END
    if update_msg:
        click.echo(update_msg)

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
    """Check and fix text for spelling, grammar, style, and punctuation errors.
    
    Provides comprehensive text analysis with support for multiple languages,
    interactive corrections, and various output formats (text/JSON).
    Can ignore specific error types: spelling, grammar, style, or punctuation."""
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

    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()
