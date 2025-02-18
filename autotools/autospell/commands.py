import click
import json as json_module
from .core import SpellChecker
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
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
        with LoadingAnimation():
            languages = checker.get_supported_languages()
            if json:
                result = {'languages': languages}
                click.echo(json_module.dumps(result, indent=2))
            else:
                click.echo("\nSupported Languages:")
                for lang in languages:
                    click.echo(f"{lang['code']:<8} {lang['name']}")
        return
        
    # --CHECK AND FIX SPELLING/GRAMMAR IN TEXT
    for text in texts:
        if not text:
            click.echo("Error: Please provide text to check")
            continue
        
        # --FIX OPTION: SPELLING/GRAMMAR IN TEXT
        if fix:
            # CORRECT TEXT WITH SPELL CHECKER
            with LoadingAnimation():
                corrected = checker.fix_text(text, lang, copy_to_clipboard=True, 
                                           ignore=ignore, interactive=interactive)
                result = {'corrected_text': corrected}
            
            # OUTPUT RESULTS AS JSON
            if json:
                click.echo(json_module.dumps(result, indent=2))
            else:
                # LANGUAGE INFORMATION
                with LoadingAnimation():
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
            with LoadingAnimation():
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
