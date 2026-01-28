import pytest
from pathlib import Path
from autotools.autonote.core import (
    autonote_add,
    autonote_list,
    _read_notes_file,
    _write_notes_file,
    DEFAULT_NOTES_FILE,
    NOTES_TEMPLATE
)

# UNIT TESTS

# TEST FOR READ NOTES FILE NONEXISTENT
def test_read_notes_file_nonexistent(notes_file):
    result = _read_notes_file(notes_file)
    assert "# NOTES" in result
    assert NOTES_TEMPLATE.strip() in result

# TEST FOR READ NOTES FILE EXISTING
def test_read_notes_file_existing(existing_notes_file):
    result = _read_notes_file(existing_notes_file)
    assert "First note" in result
    assert "Second note" in result
    assert "Note without timestamp" in result

# TEST FOR WRITE NOTES FILE
def test_write_notes_file(notes_file):
    content = "# NOTES\n\nTest content"
    _write_notes_file(notes_file, content)
    assert notes_file.exists()
    assert notes_file.read_text(encoding='utf-8') == content

# TEST FOR WRITE NOTES FILE CREATES DIR
def test_write_notes_file_creates_dir(temp_dir):
    notes_path = Path(temp_dir) / "subdir" / "nested" / DEFAULT_NOTES_FILE
    _write_notes_file(notes_path, "CONTENT")
    assert notes_path.exists()
    assert notes_path.parent.exists()

# TEST FOR ADD NOTE WITH TIMESTAMP
def test_autonote_add_with_timestamp(notes_file):
    result = autonote_add(str(notes_file), "Test note")
    assert Path(result).exists()
    content = Path(result).read_text(encoding='utf-8')
    assert "Test note" in content
    assert "**[" in content
    assert "]**" in content

# TEST FOR ADD NOTE WITHOUT TIMESTAMP
def test_autonote_add_without_timestamp(notes_file):
    result = autonote_add(str(notes_file), "Test note", timestamp=False)
    assert Path(result).exists()
    content = Path(result).read_text(encoding='utf-8')
    assert "Test note" in content
    assert "**[" not in content
    assert "- Test note" in content

# TEST FOR ADD NOTE TO EXISTING FILE
def test_autonote_add_to_existing(existing_notes_file):
    initial_content = existing_notes_file.read_text(encoding='utf-8')
    result = autonote_add(str(existing_notes_file), "New note")
    content = Path(result).read_text(encoding='utf-8')
    assert "New note" in content
    assert "First note" in content
    assert "Second note" in content
    assert len(content) > len(initial_content)

# TEST FOR ADD NOTE CREATES HEADER IF MISSING
def test_autonote_add_creates_header(temp_dir):
    notes_path = Path(temp_dir) / "notes.md"
    notes_path.write_text("Some content\n", encoding='utf-8')
    autonote_add(str(notes_path), "Test note")
    content = notes_path.read_text(encoding='utf-8')
    assert "# NOTES" in content

# TEST FOR LIST NOTES EMPTY FILE
def test_autonote_list_empty_file(notes_file):
    notes_file.write_text("# NOTES\n\n", encoding='utf-8')
    result = autonote_list(str(notes_file))
    assert result == []

# TEST FOR LIST NOTES NONEXISTENT FILE
def test_autonote_list_nonexistent(temp_dir):
    notes_path = Path(temp_dir) / "nonexistent.md"
    result = autonote_list(str(notes_path))
    assert result == []

# TEST FOR LIST NOTES WITH CONTENT
def test_autonote_list_with_content(existing_notes_file):
    result = autonote_list(str(existing_notes_file))
    assert len(result) == 3
    assert "First note" in result[0]
    assert "Second note" in result[1]
    assert "Note without timestamp" in result[2]

# TEST FOR LIST NOTES WITH LIMIT
def test_autonote_list_with_limit(existing_notes_file):
    result = autonote_list(str(existing_notes_file), limit=2)
    assert len(result) == 2
    assert "Second note" in result[0]
    assert "Note without timestamp" in result[1]

# TEST FOR LIST NOTES FORMAT FOR TERMINAL
def test_autonote_list_format_terminal(existing_notes_file):
    result = autonote_list(str(existing_notes_file), format_for_terminal=True)
    assert len(result) == 3
    # CHECK FORMAT: [YYYY-MM-DD HH:MM:SS] note
    assert "[2026-01-28 10:00:00]" in result[0]
    assert "First note" in result[0]
    assert "**[" not in result[0]  # NO MARKDOWN IN TERMINAL OUTPUT
    assert "[2026-01-28 11:00:00]" in result[1]
    assert "Second note" in result[1]

# TEST FOR LIST NOTES FORMAT FOR TERMINAL WITHOUT TIMESTAMP
def test_autonote_list_format_terminal_no_timestamp(notes_file):
    notes_file.write_text("# NOTES\n\n- Note without timestamp\n", encoding='utf-8')
    result = autonote_list(str(notes_file), format_for_terminal=True)
    assert len(result) == 1
    assert "Note without timestamp" in result[0]

# TEST FOR ADD MULTIPLE NOTES
def test_autonote_add_multiple(notes_file):
    autonote_add(str(notes_file), "First note")
    autonote_add(str(notes_file), "Second note")
    autonote_add(str(notes_file), "Third note")
    result = autonote_list(str(notes_file))
    assert len(result) == 3
    assert "First note" in result[0]
    assert "Second note" in result[1]
    assert "Third note" in result[2]

# TEST FOR ADD NOTE TO EMPTY FILE
def test_autonote_add_to_empty_file(notes_file):
    notes_file.write_text("", encoding='utf-8')
    result = autonote_add(str(notes_file), "Test note")
    content = Path(result).read_text(encoding='utf-8')
    assert "# NOTES" in content
    assert "Test note" in content

# TEST FOR ADD NOTE TO FILE WITH ONLY WHITESPACE
def test_autonote_add_to_whitespace_only_file(notes_file):
    notes_file.write_text("   \n\n  ", encoding='utf-8')
    result = autonote_add(str(notes_file), "Test note")
    content = Path(result).read_text(encoding='utf-8')
    assert "# NOTES" in content
    assert "Test note" in content

# TEST FOR FORMAT NOTE WITH TIMESTAMP WITHOUT BOLD
def test_autonote_list_format_timestamp_without_bold(temp_dir):
    from autotools.autonote.core import _format_note_for_terminal
    note_line = "- [2026-01-28 10:00:00] Test note"
    result = _format_note_for_terminal(note_line)
    assert result == "[2026-01-28 10:00:00] Test note"

# TEST FOR FORMAT NOTE WITH OLD TIMESTAMP FORMAT
def test_autonote_list_format_old_timestamp_format(temp_dir):
    from autotools.autonote.core import _format_note_for_terminal
    note_line = "- **2026-01-28 10:00:00**: Test note"
    result = _format_note_for_terminal(note_line)
    assert result == "[2026-01-28 10:00:00] Test note"

# TEST FOR LIST NOTES WITH TIMESTAMP WITHOUT BOLD FORMAT
def test_autonote_list_with_timestamp_without_bold(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("# NOTES\n\n- [2026-01-28 10:00:00] Test note\n", encoding='utf-8')
    result = autonote_list(str(notes_file), format_for_terminal=True)
    assert len(result) == 1
    assert "[2026-01-28 10:00:00] Test note" in result[0]

# TEST FOR LIST NOTES WITH OLD TIMESTAMP FORMAT
def test_autonote_list_with_old_timestamp_format(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("# NOTES\n\n- **2026-01-28 10:00:00**: Test note\n", encoding='utf-8')
    result = autonote_list(str(notes_file), format_for_terminal=True)
    assert len(result) == 1
    assert "[2026-01-28 10:00:00] Test note" in result[0]
