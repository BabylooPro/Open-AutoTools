import click
from .core import autonote_add, autonote_list, DEFAULT_NOTES_FILE
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Text'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'add-note', 'args': ['--add', 'Test note']},
    {'name': 'list-notes', 'args': ['--list']},
]

# CLI COMMAND TO MANAGE NOTES
@click.command()
@click.option('--file', '-f', 'notes_path', default=DEFAULT_NOTES_FILE, help='PATH TO NOTES FILE (DEFAULT: NOTES.md)')
@click.option('--add', 'add_note', metavar='NOTE', help='ADD A NOTE')
@click.option('--no-timestamp', 'no_timestamp', is_flag=True, help='ADD NOTE WITHOUT TIMESTAMP')
@click.option('--list', 'list_notes', is_flag=True, help='LIST ALL NOTES')
@click.option('--limit', type=int, metavar='N', help='LIMIT NUMBER OF NOTES WHEN LISTING (SHOWS LAST N NOTES)')
def autonote(notes_path, add_note, no_timestamp, list_notes, limit):
    """
        TAKES QUICK NOTES AND SAVES THEM TO A MARKDOWN FILE.

        \b
        OPERATIONS:
            - ADD NOTE: --add "your note here" [--no-timestamp]
            - LIST NOTES: --list [--limit N]

        \b
        EXAMPLES:
            autonote --add "Meeting with team at 3pm"
            autonote --add "Remember to update docs" --no-timestamp
            autonote --list
            autonote --list --limit 5
    """

    operations = sum([bool(add_note), bool(list_notes)])

    if operations == 0:
        click.echo(click.style("ERROR: NO OPERATION SPECIFIED", fg='red'), err=True)
        click.echo(click.get_current_context().get_help())
        raise click.Abort()

    if operations > 1:
        click.echo(click.style("ERROR: ONLY ONE OPERATION CAN BE PERFORMED AT A TIME", fg='red'), err=True)
        raise click.Abort()

    try:
        with LoadingAnimation():
            if add_note:
                result = autonote_add(notes_path, add_note, timestamp=not no_timestamp)
                click.echo(click.style(f"SUCCESS: ADDED NOTE TO {result}", fg='green'))
            elif list_notes:  # pragma: no branch
                notes = autonote_list(notes_path, limit, format_for_terminal=True)
                if not notes:
                    click.echo(click.style("NO NOTES FOUND", fg='yellow'))
                else:
                    click.echo(click.style(f"\nNOTES ({len(notes)}):", fg='blue', bold=True))
                    for note in notes:
                        click.echo(f"  {note}")
        
        update_msg = check_for_updates()
        if update_msg:
            click.echo(update_msg)
    
    except Exception as e:
        click.echo(click.style(f"UNEXPECTED ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
