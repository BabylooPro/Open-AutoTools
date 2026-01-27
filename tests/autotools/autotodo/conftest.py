import pytest
import tempfile
import shutil
from pathlib import Path
from autotools.autotodo import *  # NOSONAR

# FIXTURES

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def todo_file(temp_dir):
    return Path(temp_dir) / DEFAULT_TODO_FILE

@pytest.fixture
def existing_todo_file(temp_dir):
    todo_path = Path(temp_dir) / DEFAULT_TODO_FILE
    todo_path.write_text("""### TODO LIST

#### TASK

- [ ] **fix:** test task 1
- [ ] **add:** test task 2

#### IN PROGRESS

- [ ] **fixing:** task in progress

#### DONE - v0.0.5

- [x] **added:** completed task

[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
""", encoding='utf-8')
    return todo_path
