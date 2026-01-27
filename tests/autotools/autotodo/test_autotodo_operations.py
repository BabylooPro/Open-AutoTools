import pytest
import tempfile
from pathlib import Path
from autotools.autotodo import *  # NOSONAR

# TEST FOR AUTOTODO ADD TASK
def test_autotodo_add_task(todo_file):
    result = autotodo_add_task(str(todo_file), "test task", "fix")
    assert Path(result).exists()
    content = Path(result).read_text(encoding='utf-8')
    assert '**fix:** test task' in content

# TEST FOR AUTOTODO ADD TASK WITH PRIORITY
def test_autotodo_add_task_with_priority(todo_file):
    result = autotodo_add_task(str(todo_file), "test task", "fix", "high")
    content = Path(result).read_text(encoding='utf-8')
    assert '![HIGH][high]' in content

# TEST FOR AUTOTODO START
def test_autotodo_start(todo_file):
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** test task
#### DONE
""", encoding='utf-8')
    result = autotodo_start(str(todo_file), 0, 'tasks')
    content = Path(result).read_text(encoding='utf-8')
    assert '**fixing:** test task' in content

# TEST FOR AUTOTODO DONE FROM TASKS
def test_autotodo_done_from_tasks(todo_file):
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** test task
#### DONE
""", encoding='utf-8')
    result = autotodo_done(str(todo_file), 0, 'tasks')
    content = Path(result).read_text(encoding='utf-8')
    assert '**added:** test task' in content
    assert '- [x]' in content

# TEST FOR AUTOTODO DONE FROM IN PROGRESS
def test_autotodo_done_from_in_progress(todo_file):
    todo_file.write_text("""### HEADER
#### IN PROGRESS
- [ ] **fixing:** test task
#### DONE
""", encoding='utf-8')
    result = autotodo_done(str(todo_file), 0, 'in_progress')
    content = Path(result).read_text(encoding='utf-8')
    assert '**added:** test task' in content

# TEST FOR AUTOTODO REMOVE
def test_autotodo_remove(todo_file):
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
""", encoding='utf-8')
    result = autotodo_remove(str(todo_file), 0, 'tasks')
    content = Path(result).read_text(encoding='utf-8')
    assert '**fix:** task1' not in content
    assert '**add:** task2' in content

# TEST FOR AUTOTODO REMOVE RETURNS PATH
def test_autotodo_remove_returns_path(temp_dir):
    todo_file = Path(temp_dir) / "TODO.md"
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task1
#### DONE
""", encoding='utf-8')
    result = autotodo_remove(str(todo_file), 0, 'tasks')
    assert result == str(todo_file)

# TEST FOR AUTOTODO REMOVE RETURNS FILE PATH
def test_autotodo_remove_returns_file_path(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    result = autotodo_remove(str(todo_file), 0, 'tasks')
    assert result == str(todo_file)

# TEST FOR AUTOTODO LIST ALL
def test_autotodo_list_all(todo_file):
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task1
#### IN PROGRESS
- [ ] **fixing:** task2
#### DONE
- [x] **added:** task3
""", encoding='utf-8')
    result = autotodo_list(str(todo_file))
    assert len(result) == 3
    assert any(sec == 'tasks' for sec, _ in result)
    assert any(sec == 'in_progress' for sec, _ in result)
    assert any(sec == 'done' for sec, _ in result)

# TEST FOR AUTOTODO LIST SPECIFIC SECTION
def test_autotodo_list_specific_section(todo_file):
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task1
#### IN PROGRESS
- [ ] **fixing:** task2
""", encoding='utf-8')
    result = autotodo_list(str(todo_file), 'tasks')
    assert len(result) == 1
    assert result[0][0] == 'tasks'

# TEST FOR AUTOTODO LIST EMPTY
def test_autotodo_list_empty(temp_dir):
    todo_file = Path(temp_dir) / "empty.md"
    todo_file.write_text("### HEADER\n", encoding='utf-8')
    result = autotodo_list(str(todo_file))
    assert isinstance(result, list)

# TEST FOR LIST WITH VERSIONED DONE
def test_list_with_versioned_done(temp_dir):
    test_file = Path(temp_dir) / "test.md"
    test_file.write_text("""### HEADER
#### TASK
#### DONE - v0.0.5
- [x] **added:** task
""", encoding='utf-8')
    result = autotodo_list(str(test_file))
    assert isinstance(result, list)

# TEST FOR LIST WITH MIXED CONTENT
def test_list_with_mixed_content():
    content = """### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
#### IN PROGRESS
- [ ] **fixing:** task3
#### DONE
- [x] **added:** task4
#### DONE - v0.0.5
- [x] **added:** task5
"""
    todo_file = Path(tempfile.mkdtemp()) / "test.md"
    todo_file.write_text(content, encoding='utf-8')
    result = autotodo_list(str(todo_file))
    assert len(result) == 3
    tasks_section = next((sec, lines) for sec, lines in result if sec == 'tasks')
    assert len(tasks_section[1]) == 2

# TEST FOR AUTOTODO LIST HANDLES VERSIONED DONE
def test_autotodo_list_handles_versioned_done():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
- [x] **added:** task
"""
    todo_file = Path(tempfile.mkdtemp()) / "test.md"
    todo_file.write_text(content, encoding='utf-8')
    result = autotodo_list(str(todo_file), 'done')
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST CONTINUES WHEN SECTION NOT FOUND
def test_autotodo_list_continues_when_section_not_found(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n", encoding='utf-8')
    result = autotodo_list(str(todo_file), 'in_progress')
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST CONTINUES WHEN SECTION MISSING
def test_autotodo_list_continues_when_section_missing(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n", encoding='utf-8')
    result = autotodo_list(str(todo_file), 'nonexistent')
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST SKIPS SECTIONS WITH NO TASKS
def test_autotodo_list_skips_sections_with_no_tasks(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n#### IN PROGRESS\n#### DONE\n", encoding='utf-8')
    result = autotodo_list(str(todo_file), 'in_progress')
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST ALL SECTIONS EMPTY
def test_autotodo_list_all_sections_empty(temp_dir):
    todo_file = Path(temp_dir) / "empty.md"
    todo_file.write_text("### HEADER\n", encoding='utf-8')
    result = autotodo_list(str(todo_file))
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST CONTINUES WHEN SECTION NOT FOUND BRANCH
def test_autotodo_list_continues_when_section_not_found_branch():
    content = """### HEADER
#### TASK
"""
    result = autotodo_list(content, 'in_progress')
    assert isinstance(result, list)

# TEST FOR AUTOTODO LIST CONTINUES WHEN SECTION NOT FOUND DIRECT
def test_autotodo_list_continues_when_section_not_found_direct(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task
""", encoding='utf-8')
    from unittest.mock import patch
    with patch('autotools.autotodo.core._find_section', return_value=(-1, -1)):
        result = autotodo_list(str(todo_file), 'in_progress')
        assert isinstance(result, list)
        assert len(result) == 0

# TEST FOR AUTOTODO LIST SKIPS MISSING SECTIONS
def test_autotodo_list_skips_missing_sections():
    result = autotodo_list('test.md', None)
    assert isinstance(result, list)
