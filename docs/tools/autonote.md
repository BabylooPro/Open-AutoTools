# AutoNote

## Description

Takes quick notes and saves them to a Markdown file (NOTES.md by default). Supports adding notes with optional timestamps and listing notes with optional limit. Notes are stored in a simple Markdown format with timestamps.

## Usage

```bash
autonote --add "note text" [OPTIONS]
autonote --list [--limit N]
```

## Options

- `--file, -f`: Path to notes file (default: NOTES.md)
- `--add`: Add a new note
- `--no-timestamp`: Add note without timestamp
- `--list`: List all notes
- `--limit N`: Limit number of notes when listing (shows last N notes)

## Examples

### Adding Notes

```bash
# Add a note with timestamp (default)
autonote --add "Meeting with team at 3pm"

# Add a note without timestamp
autonote --add "Remember to update docs" --no-timestamp

# Add a note to a custom file
autonote --file my-notes.md --add "Custom note"
```

### Listing Notes

```bash
# List all notes
autonote --list

# List last 5 notes
autonote --list --limit 5

# List notes from custom file
autonote --file my-notes.md --list --limit 10
```

## Note Format

Notes are stored in Markdown format with the following structure:

```markdown
# Notes

- **[2026-01-28 14:30:00]** Meeting with team at 3pm

- Remember to update docs

- **[2026-01-28 15:45:00]** Another note with timestamp
```

When `--no-timestamp` is used, notes are stored without timestamps:

```markdown
- Note without timestamp
```

## File Structure

If the notes file doesn't exist, it will be created automatically with the following template:

```markdown
# Notes
```

## Notes

- Only one operation can be performed at a time (either `--add` or `--list`)
- Timestamps are added automatically in the format `YYYY-MM-DD HH:MM:SS`
- When listing with `--limit`, the last N notes are shown (most recent first)
- Notes are appended to the file in chronological order
- The tool automatically manages file structure and empty line cleanup
