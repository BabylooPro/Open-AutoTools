import click
from pathlib import Path
from .core import (autotodo_add_task, autotodo_start, autotodo_done, autotodo_remove, autotodo_list, DEFAULT_TODO_FILE)
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Task'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [{'name': 'autotodo-list', 'args': ['--list']}]

# CLI COMMAND TO MANAGE TODO LIST
@click.command()
@click.option('--file', '-f', 'todo_path', default=DEFAULT_TODO_FILE, help='PATH TO TODO FILE (DEFAULT: TODO.md)')
@click.option('--add-task', 'add_task', metavar='DESCRIPTION', help='ADD A TASK')
@click.option('--prefix', type=str, default='fix', help='PREFIX FOR TASK (DEFAULT: fix, EXAMPLES: fix, add, change, update)')
@click.option('--priority', '-p', type=click.Choice(['high', 'mid', 'low'], case_sensitive=False), help='PRIORITY FOR TASK (OPTIONAL)')
@click.option('--start', 'start_task', type=int, metavar='INDEX', help='MOVE TASK TO IN PROGRESS (REQUIRES --section tasks)')
@click.option('--done', 'done_task', type=int, metavar='INDEX', help='MOVE TASK TO DONE (REQUIRES --section)')
@click.option('--remove', 'remove_task', type=int, metavar='INDEX', help='REMOVE TASK (REQUIRES --section)')
@click.option('--section', '-s', type=click.Choice(['tasks', 'in_progress', 'done'], case_sensitive=False), help='SECTION FOR --start, --done, OR --remove')
@click.option('--list', 'list_tasks', is_flag=True, help='LIST ALL TASKS')
@click.option('--list-section', type=click.Choice(['tasks', 'in_progress', 'done'], case_sensitive=False), help='LIST TASKS IN SPECIFIC SECTION')
def autotodo(todo_path, add_task, prefix, priority, start_task, done_task, remove_task, section, list_tasks, list_section):
    """
        MANAGES A SIMPLE TASK LIST IN A MARKDOWN FILE.

        \b
        OPERATIONS:
            - ADD TASK: --add-task "description" [--prefix fix|add|change|...] [--priority high|mid|low]
            - START TASK: --start INDEX --section tasks
            - COMPLETE TASK: --done INDEX --section tasks|in_progress
            - REMOVE TASK: --remove INDEX --section tasks|in_progress|done
            - LIST TASKS: --list [--list-section SECTION]

        \b
        EXAMPLES:
            autotodo --add-task "fix login issue" --prefix fix --priority high
            autotodo --add-task "add dark mode" --prefix add
            autotodo --add-task "update documentation" --prefix update
            autotodo --start 0 --section tasks
            autotodo --done 0 --section in_progress
            autotodo --list
            autotodo --list-section tasks
    """

    operations = sum([bool(add_task), bool(start_task is not None), bool(done_task is not None), bool(remove_task is not None), bool(list_tasks), bool(list_section)])

    if operations == 0:
        click.echo(click.style("ERROR: NO OPERATION SPECIFIED", fg='red'), err=True)
        click.echo(click.get_current_context().get_help())
        raise click.Abort()

    if operations > 1:
        click.echo(click.style("ERROR: ONLY ONE OPERATION CAN BE PERFORMED AT A TIME", fg='red'), err=True)
        raise click.Abort()

    if (start_task is not None or done_task is not None or remove_task is not None) and not section:
        click.echo(click.style("ERROR: --section IS REQUIRED FOR --start, --done, OR --remove", fg='red'), err=True)
        raise click.Abort()
    
    try:
        with LoadingAnimation():
            _execute_operation(todo_path, add_task, prefix, priority, start_task, done_task, remove_task, section, list_tasks, list_section)
        update_msg = check_for_updates()
        if update_msg: click.echo(update_msg)
    
    except ValueError as e:
        click.echo(click.style(f"ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"UNEXPECTED ERROR: {str(e)}", fg='red'), err=True)
        raise click.Abort()

# HANDLES LIST OPERATION
def _handle_list_operation(todo_path, list_section):
    section_to_list = list_section if list_section else None
    tasks = autotodo_list(todo_path, section_to_list)

    if not tasks:
        click.echo(click.style("NO TASKS FOUND", fg='yellow'))
    else:
        section_names = {'tasks': 'Task', 'in_progress': 'IN PROGRESS', 'done': 'DONE'}
        for sec, task_lines in tasks:
            section_name = section_names.get(sec, sec.upper())
            click.echo(click.style(f"\n{section_name}:", fg='blue', bold=True))
            for i, task_line in enumerate(task_lines): click.echo(f"  [{i}] {task_line}")

# EXECUTES THE REQUESTED OPERATION
def _execute_operation(todo_path, add_task, prefix, priority, start_task, done_task, remove_task, section, list_tasks, list_section):
    if add_task:
        result = autotodo_add_task(todo_path, add_task, prefix, priority)
        click.echo(click.style(f"SUCCESS: ADDED TASK TO {result}", fg='green'))

    elif start_task is not None:
        if section != 'tasks':
            click.echo(click.style("ERROR: --start REQUIRES --section tasks", fg='red'), err=True)
            raise click.Abort()
        result = autotodo_start(todo_path, start_task, section)
        click.echo(click.style(f"SUCCESS: MOVED TASK TO IN PROGRESS IN {result}", fg='green'))

    elif done_task is not None:
        if section not in ['tasks', 'in_progress']:
            click.echo(click.style("ERROR: --done REQUIRES --section tasks OR in_progress", fg='red'), err=True)
            raise click.Abort()
        result = autotodo_done(todo_path, done_task, section)
        click.echo(click.style(f"SUCCESS: MOVED TASK TO DONE IN {result}", fg='green'))

    elif remove_task is not None:
        result = autotodo_remove(todo_path, remove_task, section)
        click.echo(click.style(f"SUCCESS: REMOVED TASK FROM {result}", fg='green'))

    elif list_tasks or list_section:
        _handle_list_operation(todo_path, list_section)
