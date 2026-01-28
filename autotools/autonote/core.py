from pathlib import Path
from datetime import datetime
from typing import Optional

DEFAULT_NOTES_FILE = "NOTES.md"

NOTES_TEMPLATE = """# NOTES

"""

# READS NOTES FILE CONTENT
def _read_notes_file(notes_path: Path) -> str:
    if not notes_path.exists():
        return NOTES_TEMPLATE
    return notes_path.read_text(encoding='utf-8')

# WRITES NOTES FILE CONTENT
def _write_notes_file(notes_path: Path, content: str):
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(content, encoding='utf-8')

# ADDS A NOTE TO THE NOTES FILE
def autonote_add(notes_path: str, note: str, timestamp: Optional[bool] = True):
    notes_file = Path(notes_path)
    content = _read_notes_file(notes_file)
    
    lines = content.split('\n')
    
    # REMOVE TRAILING EMPTY LINES
    while lines and lines[-1].strip() == '':
        lines.pop()
    
    # ENSURE FILE HAS HEADER IF EMPTY OR MISSING
    if not lines or (len(lines) == 1 and lines[0].strip() == ''):
        lines = ['# NOTES', '']
    elif not any(line.strip().startswith('#') for line in lines):
        lines.insert(0, '# NOTES')
        lines.insert(1, '')
    
    # ADD NEW NOTE WITH TIMESTAMP
    if timestamp:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = f"- **[{timestamp_str}]** {note}"
    else:
        new_note = f"- {note}"
    
    lines.append(new_note)
    lines.append('')  # ADD EMPTY LINE AFTER NOTE
    
    content = '\n'.join(lines)
    _write_notes_file(notes_file, content)
    return str(notes_file)

# FORMATS NOTE FOR TERMINAL DISPLAY (REMOVES MARKDOWN)
def _format_note_for_terminal(note_line: str) -> str:
    # REMOVE LEADING DASH AND SPACES
    note = note_line.lstrip('-').strip()
    
    # EXTRACT TIMESTAMP IF PRESENT (SUPPORTS MULTIPLE FORMATS FOR COMPATIBILITY)
    import re
    # NEW FORMAT: **[YYYY-MM-DD HH:MM:SS]** note
    timestamp_match = re.match(r'\*\*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\*\*\s*(.+)', note)
    if timestamp_match:
        timestamp = timestamp_match.group(1)
        note_text = timestamp_match.group(2)
        return f"[{timestamp}] {note_text}"
    
    # FORMAT: [YYYY-MM-DD HH:MM:SS] note (WITHOUT BOLD)
    timestamp_match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s*(.+)', note)
    if timestamp_match:
        timestamp = timestamp_match.group(1)
        note_text = timestamp_match.group(2)
        return f"[{timestamp}] {note_text}"
    
    # OLD FORMAT: **YYYY-MM-DD HH:MM:SS**: note (FOR BACKWARD COMPATIBILITY)
    timestamp_match = re.match(r'\*\*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\*\*:\s*(.+)', note)
    if timestamp_match:
        timestamp = timestamp_match.group(1)
        note_text = timestamp_match.group(2)
        return f"[{timestamp}] {note_text}"
    
    # NO TIMESTAMP, RETURN AS IS
    return note

# LISTS NOTES FROM THE FILE
def autonote_list(notes_path: str, limit: Optional[int] = None, format_for_terminal: bool = False):
    notes_file = Path(notes_path)
    if not notes_file.exists():
        return []
    
    content = _read_notes_file(notes_file)
    lines = content.split('\n')
    
    notes = []
    for line in lines:
        stripped = line.strip()
        if stripped and stripped.startswith('-'):
            if format_for_terminal:
                notes.append(_format_note_for_terminal(stripped))
            else:
                notes.append(stripped)
    
    if limit and limit > 0:
        notes = notes[-limit:]  # GET LAST N NOTES
    
    return notes
