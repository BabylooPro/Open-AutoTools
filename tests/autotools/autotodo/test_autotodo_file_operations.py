import pytest
from pathlib import Path
from autotools.autotodo import *  # NOSONAR

# TEST FOR READ TODO FILE NONEXISTENT
def test_read_todo_file_nonexistent(todo_file):
    result = _read_todo_file(todo_file)
    assert "### TO DO LIST" in result
    assert "#### TASK" in result

# TEST FOR READ TODO FILE EXISTING
def test_read_todo_file_existing(existing_todo_file):
    result = _read_todo_file(existing_todo_file)
    assert "test task 1" in result
    assert "test task 2" in result

# TEST FOR WRITE TODO FILE
def test_write_todo_file(todo_file):
    content = "TEST CONTENT"
    _write_todo_file(todo_file, content)
    assert todo_file.exists()
    assert todo_file.read_text(encoding='utf-8') == content

# TEST FOR WRITE TODO FILE CREATES DIR
def test_write_todo_file_creates_dir(temp_dir):
    todo_path = Path(temp_dir) / "subdir" / "nested" / DEFAULT_TODO_FILE
    _write_todo_file(todo_path, "CONTENT")
    assert todo_path.exists()
    assert todo_path.parent.exists()
