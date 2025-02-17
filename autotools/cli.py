import os
import click
import base64
import json as json_module
from importlib.metadata import version as get_version, PackageNotFoundError
from packaging.version import parse as parse_version
from autotools.autocaps.core import autocaps_transform
from autotools.autolower.core import autolower_transform
from autotools.autodownload.core import (
    download_youtube_video,
    download_file,
    validate_youtube_url
)
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
from datetime import datetime
import pytest
import sys
import subprocess
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

# VERSION CALLBACK
def print_version(ctx, param, value):
    """PRINT VERSION AND CHECK FOR UPDATES"""
    
    # EXIT IF VERSION IS NOT REQUESTED
    if not value or ctx.resilient_parsing:
        return
    
    try:
        # GET CURRENT VERSION
        pkg_version = get_version('Open-AutoTools')
        click.echo(f"Open-AutoTools version {pkg_version}")

        # GET DISTRIBUTION INFO
        import pkg_resources
        dist = pkg_resources.get_distribution("Open-AutoTools")
        current_version = parse_version(dist.version)

        # GET LATEST VERSION FROM PYPI
        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        response = requests.get(pypi_url)
        
        # CHECK IF RESPONSE IS SUCCESSFUL
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            releases = data["releases"]
            
            # GET RELEASE DATE
            if latest_version in releases and releases[latest_version]:
                try:
                    upload_time = releases[latest_version][0]["upload_time"]
                    for date_format in [
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%d %H:%M:%S"
                    ]:
                        try:
                            published_date = datetime.strptime(upload_time, date_format)
                            formatted_date = published_date.strftime("%d %B %Y at %H:%M:%S")
                            click.echo(f"Released: {formatted_date}")
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass  # SKIP DATE IF PARSING FAILS
            
            # CHECK FOR UPDATES
            latest_parsed = parse_version(latest_version)

            # COMPARE VERSIONS AND PRINT UPDATE MESSAGE IF NEEDED
            if latest_parsed > current_version:
                update_cmd = "pip install --upgrade Open-AutoTools"
                click.echo(click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True))
                click.echo(click.style(f"Run '{update_cmd}' to update", fg='red'))

    except pkg_resources.DistributionNotFound:
        click.echo("Package distribution not found")
    except PackageNotFoundError:
        click.echo("Open-AutoTools version information not available")
    except Exception as e:
        click.echo(f"Error checking updates: {str(e)}")
    
    ctx.exit()

# CLI FUNCTION DEFINITION
@click.group()
@click.option('--version', '--v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version and check for updates')
@click.option('--help', '-h', is_flag=True, callback=lambda ctx, param, value: 
              None if not value else (click.echo(ctx.get_help() + '\n' + 
              (check_for_updates() or '')) or ctx.exit()),
              is_eager=True, expose_value=False, help='Show this message and exit.')
def cli():
    """A suite of automated tools for various tasks.
    
    Run 'autotools COMMAND --help' for more information on each command."""
    pass

# AUTOTOOLS COMMAND LINE INTERFACE FUNCTION DEFINITION FOR SHOW HELP MESSAGE
@cli.command()
def autotools():
    """Display available commands and tool information."""
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
        import pkg_resources
        dist = pkg_resources.get_distribution("Open-AutoTools")
        current_version = parse_version(dist.version)

        # GET LATEST VERSION FROM PYPI
        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        
        # CHECK FOR UPDATES FROM PYPI
        response = requests.get(pypi_url)
        
        # CHECK IF RESPONSE IS SUCCESSFUL
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            
            # PARSE VERSIONS FOR COMPARISON
            latest_parsed = parse_version(latest_version)
            
            # PRINT UPDATE MESSAGE IF NEEDED
            if latest_parsed > current_version:
                update_cmd = "pip install --upgrade Open-AutoTools"
                return (
                    click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True) + "\n" +
                    click.style(f"Run '{update_cmd}' to update", fg='red')
                )
    except Exception as e:
        # FOR DEBUGGING, LOG ERROR
        print(f"Error checking updates: {str(e)}")
    
    return None

# AUTOCAPS COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text', nargs=-1)
def autocaps(text):
    """Convert text to UPPERCASE."""
    result = autocaps_transform(" ".join(text))
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# AUTOLOWER CASE COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('text', nargs=-1)
def autolower(text):
    """Convert text to lowercase."""
    result = autolower_transform(" ".join(text))
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# AUTODOWNLOAD COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.argument('url')
@click.option('--format', '-f', type=click.Choice(['mp4', 'mp3'], case_sensitive=False), 
              default='mp4', help='Output file format')
@click.option('--quality', '-q', type=click.Choice(['best', '1440p', '1080p', '720p', '480p', '360p', '240p'], 
              case_sensitive=False), default='best', help='Video quality (mp4 only)')
def autodownload(url, format, quality):
    """Download videos from YouTube or files from any URL.
    
    Supports YouTube video download with quality selection and format conversion (mp4/mp3).
    For non-YouTube URLs, downloads the file directly."""
    if "youtube.com" in url or "youtu.be" in url:
        # VALIDATE YOUTUBE URL FIRST
        if not validate_youtube_url(url):
            click.echo("Invalid YouTube URL", err=True)
            sys.exit(1)
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
@click.option('--output', '-o', type=click.Path(), help='Save translation to file')
def autotranslate(text: str, to: str, from_lang: str, list_languages: bool, 
                  copy: bool, detect: bool, output: str):
    """Translate text to specified language.
    
    Supports automatic language detection, multiple target languages,
    clipboard operations and file output. Use --list-languages to see
    all supported language codes."""
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
                          copy=copy, detect_lang=detect, output=output)
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
@click.option('--interval', '-i', default=1, help='Monitoring interval in seconds')
@click.option('--ports', '-p', is_flag=True, help='Check common ports status')
@click.option('--dns', '-d', is_flag=True, help='Show DNS servers')
@click.option('--location', '-l', is_flag=True, help='Show IP location info')
@click.option('--no-ip', '-n', is_flag=True, help='Hide IP addresses')
def autoip(test, speed, monitor, interval, ports, dns, location, no_ip):
    """Display network information and diagnostics.
    
    Shows local and public IP addresses, runs network diagnostics,
    performs speed tests, monitors traffic with custom intervals,
    checks ports, displays DNS information and provides geolocation data."""
    from autotools.autoip.core import run
    output = run(test=test, speed=speed, monitor=monitor, interval=interval,
                ports=ports, dns=dns, location=location, no_ip=no_ip)
    click.echo(output)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
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

# TEST COMMAND LINE INTERFACE FUNCTION DEFINITION
@cli.command()
@click.option('--unit', '-u', is_flag=True, help='Run only unit tests')
@click.option('--integration', '-i', is_flag=True, help='Run only integration tests')
@click.option('--no-cov', is_flag=True, help='Disable coverage report')
@click.option('--html', is_flag=True, help='Generate HTML coverage report')
@click.option('--module', '-m', help='Test specific module (e.g., autocaps, autolower)')
def test(unit, integration, no_cov, html, module):
    """Run test suite with various options."""
    # CHECK IF PYTEST IS INSTALLED
    try:
        import pytest
        import pytest_cov
    except ImportError:
        click.echo(click.style("\n❌ pytest and/or pytest-cov not found. Installing...", fg='yellow', bold=True))
        try:
            subprocess.run(['pip', 'install', 'pytest', 'pytest-cov'], check=True)
            click.echo(click.style("✅ Successfully installed pytest and pytest-cov", fg='green', bold=True))
        except subprocess.CalledProcessError as e:
            click.echo(click.style(f"\n❌ Failed to install dependencies: {str(e)}", fg='red', bold=True))
            sys.exit(1)
    
    cmd = ['python', '-m', 'pytest', '-v'] # BASE COMMAND
    
    # COVERAGE OPTIONS
    if not no_cov:
        cmd.extend(['--cov=autotools'])
        if html:
            cmd.extend(['--cov-report=html'])
        else:
            cmd.extend(['--cov-report=term-missing'])
    
    # TEST SELECTION
    test_path = 'autotools'
    if module:
        if unit and not integration:
            cmd.append(f'autotools/{module}/tests/test_{module}_core.py')
        elif integration and not unit:
            cmd.append(f'autotools/{module}/tests/test_{module}_integration.py')
        else:
            cmd.append(f'autotools/{module}/tests')
    
    # SHOW COMMAND BEING RUN
    click.echo(click.style("\nRunning tests with command:", fg='blue', bold=True))
    click.echo(" ".join(cmd))
    click.echo()
    
    # RUN TESTS
    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            click.echo(click.style("\n✅ All tests passed!", fg='green', bold=True))
        else:
            click.echo(click.style("\n❌ Some tests failed!", fg='red', bold=True))
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"\n❌ Tests failed with return code {e.returncode}", fg='red', bold=True))
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"\n❌ Error running tests: {str(e)}", fg='red', bold=True))
        sys.exit(1)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg)

# MAIN FUNCTION TO RUN CLI
if __name__ == '__main__':
    cli()
