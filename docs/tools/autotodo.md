# AutoTodo

## Description

Manages a simple task list in a Markdown file (TODO.md by default). Supports adding tasks with priorities, moving tasks between sections (TASK, IN PROGRESS, DONE), removing tasks, and listing tasks. Tasks are organized in a structured Markdown format with priority badges.

## Usage

```bash
autotodo --add-task "description" [OPTIONS]
autotodo --start INDEX --section tasks
autotodo --done INDEX --section SECTION
autotodo --remove INDEX --section SECTION
autotodo --list [--list-section SECTION]
```

## Options

- `--file, -f`: Path to TODO file (default: TODO.md)
- `--add-task`: Add a new task
- `--prefix`: Prefix for task (default: fix, examples: fix, add, change, update)
- `--priority, -p`: Priority for task (high, mid, low)
- `--start`: Move task to IN PROGRESS (requires --section tasks)
- `--done`: Move task to DONE (requires --section tasks or in_progress)
- `--remove`: Remove task (requires --section)
- `--section, -s`: Section for --start, --done, or --remove (tasks, in_progress, done)
- `--list`: List all tasks
- `--list-section`: List tasks in specific section (tasks, in_progress, done)

## Sections

The TODO file is organized into three sections:

- **TASK**: Tasks to be done
- **IN PROGRESS**: Tasks currently being worked on
- **DONE**: Completed tasks

## Examples

### Adding Tasks

```bash
# Add a task with default prefix (fix)
autotodo --add-task "fix login issue" --priority high

# Add a task with custom prefix
autotodo --add-task "add dark mode" --prefix add

# Add a task with priority
autotodo --add-task "update documentation" --prefix update --priority mid

# Add a low priority task
autotodo --add-task "refactor code" --prefix refactor --priority low
```

### Starting Tasks

```bash
# Move task at index 0 from TASK section to IN PROGRESS
autotodo --start 0 --section tasks
```

### Completing Tasks

```bash
# Move task at index 0 from TASK section to DONE
autotodo --done 0 --section tasks

# Move task at index 1 from IN PROGRESS section to DONE
autotodo --done 1 --section in_progress
```

### Removing Tasks

```bash
# Remove task at index 0 from TASK section
autotodo --remove 0 --section tasks

# Remove task at index 2 from IN PROGRESS section
autotodo --remove 2 --section in_progress

# Remove task at index 5 from DONE section
autotodo --remove 5 --section done
```

### Listing Tasks

```bash
# List all tasks from all sections
autotodo --list

# List only tasks from TASK section
autotodo --list-section tasks

# List only tasks from IN PROGRESS section
autotodo --list-section in_progress

# List only tasks from DONE section
autotodo --list-section done
```

### Custom TODO File

```bash
# Use a custom TODO file
autotodo --file my-tasks.md --add-task "custom task"
autotodo --file my-tasks.md --list
```

## Task Format

Tasks are stored in Markdown format with the following structure:

```markdown
- [ ] **prefix:** task description ![HIGH][high]
- [ ] **prefix:** task description ![MID][mid]
- [ ] **prefix:** task description ![LOW][low]
```

When a task is moved to IN PROGRESS, the prefix is converted to its "-ing" form:

```markdown
- [ ] **prefixing:** task description
```

When a task is completed, it's moved to DONE section with a checked checkbox:

```markdown
- [x] **prefixing:** task description
```

## Priority Badges

Tasks can have priority badges:

- `![HIGH][high]` - High priority (red badge)
- `![MID][mid]` - Medium priority (yellow badge)
- `![LOW][low]` - Low priority (green badge)

## File Structure

If the TODO file doesn't exist, it will be created automatically with the following template:

```markdown
### TO DO LIST

#### TASK

- [ ] **fix:** ![HIGH][high]

#### IN PROGRESS

- [ ] **refactoring:**

#### DONE

- [x] **added:**

[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
```

## Notes

- Only one operation can be performed at a time
- The `--section` option is required for `--start`, `--done`, and `--remove` operations
- Task indices are 0-based and refer to the position within the specified section
- The tool automatically manages section organization and empty line cleanup
- Tasks are sorted within their sections
- Empty sections are automatically cleaned up
