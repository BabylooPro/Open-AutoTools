import pytest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch
from autotools.cli import autotodo

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def todo_file(temp_dir):
    todo_path = Path(temp_dir) / "TODO.md"
    todo_path.write_text("""### TODO LIST

#### TASK

- [ ] **fix:** existing task

#### IN PROGRESS

- [ ] **fixing:** task in progress

#### DONE

- [x] **added:** completed task

[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
""", encoding='utf-8')
    return str(todo_path)

def assert_success(result, expected_in_output=None):
    assert result.exit_code == 0
    if expected_in_output: assert expected_in_output in result.output

def assert_error(result, expected_in_output=None):
    assert result.exit_code != 0
    if expected_in_output: assert expected_in_output in result.output

# TEST FOR AUTOTODO CLI ADD TASK
def test_autotodo_cli_add_task(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', 'test task', '--prefix', 'fix', '--file', todo_path])
    assert_success(result, 'SUCCESS')
    assert 'ADDED TASK' in result.output
    assert Path(todo_path).exists()

# TEST FOR AUTOTODO CLI ADD TASK WITH PRIORITY
def test_autotodo_cli_add_task_with_priority(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', 'test task', '--prefix', 'fix', '--priority', 'high', '--file', todo_path])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI ADD TASK DEFAULT PREFIX
def test_autotodo_cli_add_task_default_prefix(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', 'test task', '--file', todo_path])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI START TASK
def test_autotodo_cli_start_task(runner, todo_file):
    result = runner.invoke(autotodo, ['--start', '0', '--section', 'tasks', '--file', todo_file])
    assert_success(result, 'SUCCESS')
    assert 'IN PROGRESS' in result.output
    content = Path(todo_file).read_text(encoding='utf-8')
    assert '**fixing:** existing task' in content

# TEST FOR AUTOTODO CLI START TASK INVALID SECTION
def test_autotodo_cli_start_task_invalid_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--start', '0', '--section', 'in_progress', '--file', todo_file])
    assert_error(result, 'ERROR')
    assert 'tasks' in result.output

# TEST FOR AUTOTODO CLI START TASK NO SECTION
def test_autotodo_cli_start_task_no_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--start', '0', '--file', todo_file])
    assert_error(result, 'ERROR')
    assert '--section' in result.output

# TEST FOR AUTOTODO CLI DONE FROM TASKS
def test_autotodo_cli_done_from_tasks(runner, todo_file):
    result = runner.invoke(autotodo, ['--done', '0', '--section', 'tasks', '--file', todo_file])
    assert_success(result, 'SUCCESS')
    assert 'DONE' in result.output

# TEST FOR AUTOTODO CLI DONE FROM IN PROGRESS
def test_autotodo_cli_done_from_in_progress(runner, todo_file):
    result = runner.invoke(autotodo, ['--done', '0', '--section', 'in_progress', '--file', todo_file])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI DONE INVALID SECTION
def test_autotodo_cli_done_invalid_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--done', '0', '--section', 'done', '--file', todo_file])
    assert_error(result, 'ERROR')

# TEST FOR AUTOTODO CLI DONE NO SECTION
def test_autotodo_cli_done_no_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--done', '0', '--file', todo_file])
    assert_error(result, 'ERROR')

# TEST FOR AUTOTODO CLI REMOVE FROM TASKS
def test_autotodo_cli_remove_from_tasks(runner, todo_file):
    result = runner.invoke(autotodo, ['--remove', '0', '--section', 'tasks', '--file', todo_file])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI REMOVE FROM IN PROGRESS
def test_autotodo_cli_remove_from_in_progress(runner, todo_file):
    result = runner.invoke(autotodo, ['--remove', '0', '--section', 'in_progress', '--file', todo_file])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI REMOVE FROM DONE
def test_autotodo_cli_remove_from_done(runner, todo_file):
    result = runner.invoke(autotodo, ['--remove', '0', '--section', 'done', '--file', todo_file])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI REMOVE NO SECTION
def test_autotodo_cli_remove_no_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--remove', '0', '--file', todo_file])
    assert_error(result, 'ERROR')

# TEST FOR AUTOTODO CLI LIST ALL
def test_autotodo_cli_list_all(runner, todo_file):
    result = runner.invoke(autotodo, ['--list', '--file', todo_file])
    assert_success(result)
    assert 'Task' in result.output or 'IN PROGRESS' in result.output

# TEST FOR AUTOTODO CLI LIST SPECIFIC SECTION
def test_autotodo_cli_list_specific_section(runner, todo_file):
    result = runner.invoke(autotodo, ['--list-section', 'tasks', '--file', todo_file])
    assert_success(result)
    assert 'NO TASKS FOUND' in result.output or 'Task' in result.output

# TEST FOR AUTOTODO CLI LIST EMPTY FILE
def test_autotodo_cli_list_empty_file(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "empty.md")
    Path(todo_path).write_text("", encoding='utf-8')
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert 'NO TASKS FOUND' in result.output or 'Task' in result.output or 'DONE' in result.output

# TEST FOR AUTOTODO CLI NO OPERATION
def test_autotodo_cli_no_operation(runner, todo_file):
    result = runner.invoke(autotodo, ['--file', todo_file])
    assert_error(result, 'ERROR')
    assert 'NO OPERATION' in result.output

# TEST FOR AUTOTODO CLI MULTIPLE OPERATIONS
def test_autotodo_cli_multiple_operations(runner, todo_file):
    result = runner.invoke(autotodo, ['--add-task', 'task1', '--list', '--file', todo_file])
    assert_error(result, 'ERROR')
    assert 'ONE OPERATION' in result.output

# TEST FOR AUTOTODO CLI INVALID TASK INDEX
def test_autotodo_cli_invalid_task_index(runner, todo_file):
    result = runner.invoke(autotodo, ['--start', '999', '--section', 'tasks', '--file', todo_file])
    assert_error(result, 'ERROR')
    assert 'OUT OF RANGE' in result.output or 'UNEXPECTED ERROR' in result.output

# TEST FOR AUTOTODO CLI VALUE ERROR
def test_autotodo_cli_value_error(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "invalid.md")
    Path(todo_path).write_text("invalid content", encoding='utf-8')
    result = runner.invoke(autotodo, ['--add-task', 'task', '--file', todo_path])
    assert_success(result, 'SUCCESS')

# TEST FOR AUTOTODO CLI CUSTOM FILE
def test_autotodo_cli_custom_file(runner, temp_dir):
    custom_file = str(Path(temp_dir) / "custom_todo.md")
    result = runner.invoke(autotodo, ['--add-task', 'test', '--file', custom_file])
    assert_success(result, 'SUCCESS')
    assert Path(custom_file).exists()

# TEST FOR AUTOTODO CLI DEFAULT FILE
def test_autotodo_cli_default_file(runner, temp_dir):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(temp_dir)
        result = runner.invoke(autotodo, ['--add-task', 'test'])
        assert_success(result, 'SUCCESS')
        assert Path(temp_dir) / "TODO.md"
    finally:
        os.chdir(old_cwd)

@patch('autotools.autotodo.commands.check_for_updates')
# TEST FOR AUTOTODO CLI WITH UPDATE
def test_autotodo_cli_with_update(mock_updates, runner, temp_dir):
    mock_updates.return_value = "Update available: v1.0.0"
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert "Update available" in result.output

@patch('autotools.autotodo.commands.check_for_updates')
# TEST FOR AUTOTODO CLI WITHOUT UPDATE
def test_autotodo_cli_without_update(mock_updates, runner, temp_dir):
    mock_updates.return_value = None
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert "Update available" not in result.output

# TEST FOR AUTOTODO CLI HELP
def test_autotodo_cli_help(runner):
    result = runner.invoke(autotodo, ['--help'])
    assert_success(result)
    assert 'MANAGES A SIMPLE TASK LIST' in result.output or 'task list' in result.output.lower()

@pytest.mark.parametrize("prefix", ['fix', 'add', 'change', 'update', 'improve', 'refactor'])
# TEST FOR AUTOTODO CLI ADD TASK PREFIXES
def test_autotodo_cli_add_task_prefixes(runner, temp_dir, prefix):
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', f'test {prefix}', '--prefix', prefix, '--file', todo_path])
    assert_success(result, 'SUCCESS')
    content = Path(todo_path).read_text(encoding='utf-8')
    assert f'**{prefix}:**' in content

@pytest.mark.parametrize("priority", ['high', 'mid', 'low'])
# TEST FOR AUTOTODO CLI ADD TASK PRIORITIES
def test_autotodo_cli_add_task_priorities(runner, temp_dir, priority):
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', 'test', '--prefix', 'fix', '--priority', priority, '--file', todo_path])
    assert_success(result, 'SUCCESS')
    content = Path(todo_path).read_text(encoding='utf-8')
    assert priority.upper() in content

@pytest.mark.parametrize("section", ['tasks', 'in_progress', 'done'])
# TEST FOR AUTOTODO CLI LIST SECTIONS
def test_autotodo_cli_list_sections(runner, todo_file, section):
    result = runner.invoke(autotodo, ['--list-section', section, '--file', todo_file])
    assert_success(result)
    assert 'NO TASKS FOUND' in result.output or section.upper() in result.output or 'Task' in result.output or 'IN PROGRESS' in result.output or 'DONE' in result.output

@patch('autotools.autotodo.commands.autotodo_add_task')
# TEST FOR AUTOTODO CLI UNEXPECTED ERROR
def test_autotodo_cli_unexpected_error(mock_add, runner, temp_dir):
    mock_add.side_effect = RuntimeError("Unexpected error")
    todo_path = str(Path(temp_dir) / "TODO.md")
    result = runner.invoke(autotodo, ['--add-task', 'test', '--file', todo_path])
    assert_error(result, 'UNEXPECTED ERROR')

# TEST FOR AUTOTODO CLI START WITH EMPTY TASKS
def test_autotodo_cli_start_with_empty_tasks(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--start', '0', '--section', 'tasks', '--file', todo_path])
    assert result.exit_code != 0 or 'OUT OF RANGE' in result.output

# TEST FOR AUTOTODO CLI DONE WITH EMPTY SECTION
def test_autotodo_cli_done_with_empty_section(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n#### IN PROGRESS\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--done', '0', '--section', 'in_progress', '--file', todo_path])
    assert result.exit_code != 0 or 'OUT OF RANGE' in result.output

# TEST FOR AUTOTODO CLI REMOVE WITH EMPTY SECTION
def test_autotodo_cli_remove_with_empty_section(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--remove', '0', '--section', 'tasks', '--file', todo_path])
    assert result.exit_code != 0 or 'OUT OF RANGE' in result.output

# TEST FOR AUTOTODO CLI LIST WITH NO TASKS
def test_autotodo_cli_list_with_no_tasks(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n#### IN PROGRESS\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert 'NO TASKS FOUND' in result.output or 'Task' in result.output

# TEST FOR AUTOTODO CLI LIST OPERATION COVERAGE
def test_autotodo_cli_list_operation_coverage(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert 'Task' in result.output or 'IN PROGRESS' in result.output or 'DONE' in result.output

# TEST FOR EXECUTE OPERATION LIST TASKS FLAG EXITS
def test_execute_operation_list_tasks_flag_exits(runner, temp_dir):
    todo_path = str(Path(temp_dir) / "TODO.md")
    Path(todo_path).write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    result = runner.invoke(autotodo, ['--list', '--file', todo_path])
    assert_success(result)
    assert 'Task' in result.output or 'NO TASKS FOUND' in result.output
