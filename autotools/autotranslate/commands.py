import click
from .core import translate_text, get_supported_languages
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
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
        with LoadingAnimation():
            click.echo("\nSupported Languages:")
            for code, name in get_supported_languages().items():
                click.echo(f"{code:<8} {name}")
        return
    
    # CHECK IF TEXT IS PROVIDED
    if not text:
        click.echo("Error: Please provide text to translate")
        return
        
    with LoadingAnimation():
        result = translate_text(text, to_lang=to, from_lang=from_lang, 
                              copy=copy, detect_lang=detect, output=output)
    click.echo(result)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
