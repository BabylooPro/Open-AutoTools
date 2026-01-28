import pytest
import tempfile
import shutil

from pathlib import Path
from click.testing import CliRunner
from autotools.cli import autonote

# INTEGRATION TESTS

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

# TEST FOR ADD NOTE CLI
def test_autonote_cli_add(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test note", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output
    assert str(notes_file) in result.output
    assert notes_file.exists()
    content = notes_file.read_text(encoding='utf-8')
    assert "Test note" in content

# TEST FOR ADD NOTE CLI WITHOUT TIMESTAMP
def test_autonote_cli_add_no_timestamp(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test note", "--no-timestamp", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output
    content = notes_file.read_text(encoding='utf-8')
    assert "Test note" in content
    assert "**[" not in content

# TEST FOR LIST NOTES CLI EMPTY
def test_autonote_cli_list_empty(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("# NOTES\n\n", encoding='utf-8')
    runner = CliRunner()
    result = runner.invoke(autonote, ["--list", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "NO NOTES FOUND" in result.output

# TEST FOR LIST NOTES CLI WITH CONTENT
def test_autonote_cli_list_with_content(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("""# NOTES

- **[2026-01-28 10:00:00]** First note
- **[2026-01-28 11:00:00]** Second note
""", encoding='utf-8')
    runner = CliRunner()
    result = runner.invoke(autonote, ["--list", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "NOTES (2):" in result.output
    assert "[2026-01-28 10:00:00]" in result.output
    assert "First note" in result.output
    assert "[2026-01-28 11:00:00]" in result.output
    assert "Second note" in result.output
    assert "**[" not in result.output  # NO MARKDOWN IN TERMINAL

# TEST FOR LIST NOTES CLI WITH LIMIT
def test_autonote_cli_list_with_limit(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("""# NOTES

- **[2026-01-28 10:00:00]** First note
- **[2026-01-28 11:00:00]** Second note
- **[2026-01-28 12:00:00]** Third note
""", encoding='utf-8')
    runner = CliRunner()
    result = runner.invoke(autonote, ["--list", "--limit", "2", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "NOTES (2):" in result.output
    assert "Second note" in result.output
    assert "Third note" in result.output
    assert "First note" not in result.output

# TEST FOR CLI NO OPERATION
def test_autonote_cli_no_operation():
    runner = CliRunner()
    result = runner.invoke(autonote, [])
    assert result.exit_code != 0
    assert "ERROR: NO OPERATION SPECIFIED" in result.output

# TEST FOR CLI MULTIPLE OPERATIONS
def test_autonote_cli_multiple_operations(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test", "--list", "--file", str(notes_file)])
    assert result.exit_code != 0
    assert "ERROR: ONLY ONE OPERATION" in result.output

# TEST FOR ADD AND LIST WORKFLOW
def test_autonote_cli_add_and_list_workflow(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()

    result = runner.invoke(autonote, ["--add", "First note", "--file", str(notes_file)])
    assert result.exit_code == 0

    result = runner.invoke(autonote, ["--add", "Second note", "--file", str(notes_file)])
    assert result.exit_code == 0

    result = runner.invoke(autonote, ["--list", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "NOTES (2):" in result.output
    assert "First note" in result.output
    assert "Second note" in result.output

# TEST FOR DEFAULT FILE PATH
def test_autonote_cli_default_file(temp_dir):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(temp_dir)
        runner = CliRunner()
        result = runner.invoke(autonote, ["--add", "Test note"])
        assert result.exit_code == 0
        notes_file = Path(temp_dir) / "NOTES.md"
        assert notes_file.exists()
    finally:
        os.chdir(old_cwd)

# TEST FOR SPECIAL CHARACTERS IN NOTE
def test_autonote_cli_special_chars(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Note with @#$%^&*()", "--file", str(notes_file)])
    assert result.exit_code == 0
    content = notes_file.read_text(encoding='utf-8')
    assert "@#$%^&*()" in content

# TEST FOR UNICODE IN NOTE
def test_autonote_cli_unicode(temp_dir):
    notes_file = Path(temp_dir) / "NOTES.md"
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Note avec accents: éàèù", "--file", str(notes_file)])
    assert result.exit_code == 0
    content = notes_file.read_text(encoding='utf-8')
    assert "éàèù" in content

# TEST FOR EXCEPTION HANDLING
def test_autonote_cli_exception_handling(temp_dir, monkeypatch):
    notes_file = Path(temp_dir) / "NOTES.md"

    def mock_autonote_add(*args, **kwargs):
        raise ValueError("Test error")
    
    from autotools.autonote import commands as autonote_commands
    monkeypatch.setattr(autonote_commands, "autonote_add", mock_autonote_add)
    
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test note", "--file", str(notes_file)])

    assert result.exit_code == 1
    assert "UNEXPECTED ERROR" in result.output
    assert "Test error" in result.output

# TEST FOR UPDATE MESSAGE DISPLAY
def test_autonote_cli_with_update_message(temp_dir, monkeypatch):
    notes_file = Path(temp_dir) / "NOTES.md"

    def mock_check_for_updates():
        return "Update available: v2.0.0"
    
    from autotools.autonote import commands as autonote_commands
    monkeypatch.setattr(autonote_commands, "check_for_updates", mock_check_for_updates)
    
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test note", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "Update available" in result.output

# TEST FOR ADD NOTE WITHOUT UPDATE MESSAGE
def test_autonote_cli_add_without_update_message(temp_dir, monkeypatch):
    notes_file = Path(temp_dir) / "NOTES.md"

    def mock_check_for_updates():
        return None
    
    from autotools.autonote import commands as autonote_commands
    monkeypatch.setattr(autonote_commands, "check_for_updates", mock_check_for_updates)
    
    runner = CliRunner()
    result = runner.invoke(autonote, ["--add", "Test note", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output
    assert "Test note" in notes_file.read_text(encoding='utf-8')

# TEST FOR LIST NOTES WITH UPDATE MESSAGE
def test_autonote_cli_list_with_update_message(temp_dir, monkeypatch):
    notes_file = Path(temp_dir) / "NOTES.md"
    notes_file.write_text("# NOTES\n\n- **[2026-01-28 10:00:00]** Test note\n", encoding='utf-8')
    
    def mock_check_for_updates():
        return "Update available: v2.0.0"
    
    from autotools.autonote import commands as autonote_commands
    monkeypatch.setattr(autonote_commands, "check_for_updates", mock_check_for_updates)
    
    runner = CliRunner()
    result = runner.invoke(autonote, ["--list", "--file", str(notes_file)])
    assert result.exit_code == 0
    assert "Update available" in result.output
