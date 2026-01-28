import pytest
import tempfile
import shutil

from pathlib import Path
from autotools.autonote.core import DEFAULT_NOTES_FILE

# FIXTURES

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def notes_file(temp_dir):
    return Path(temp_dir) / DEFAULT_NOTES_FILE

@pytest.fixture
def existing_notes_file(temp_dir):
    notes_path = Path(temp_dir) / DEFAULT_NOTES_FILE
    notes_path.write_text("""# NOTES

- **[2026-01-28 10:00:00]** First note
- **[2026-01-28 11:00:00]** Second note
- Note without timestamp
""", encoding='utf-8')
    return notes_path
