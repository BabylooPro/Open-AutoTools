import re
from pathlib import Path
from typing import Optional, Literal

DEFAULT_TODO_FILE = "TODO.md"
PRIORITY_BADGES = {'high': '![HIGH][high]', 'mid': '![MID][mid]', 'low': '![LOW][low]'}

TODO_TEMPLATE = """
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
"""

# REGEX PATTERNS
PATTERN_TASK_HEADER = r'^#### TASK'
PATTERN_IN_PROGRESS = r'^#### IN PROGRESS'
PATTERN_DONE = r'^#### DONE'
PATTERN_DONE_SIMPLE = r'^#### DONE$'
PATTERN_TASK_LINE = r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\*'
PATTERN_TASK_ING = r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+ing:\*\*'
PATTERN_DONE_TASK = r'^[\s]*-[\s]*\[[\s]*x[\s]*\]'
PATTERN_EMPTY_ING = r'^-[\s]*\[[\s]*\][\s]*\*\*ing:\*\*[\s]*$'

# READS TODO FILE CONTENT
def _read_todo_file(todo_path: Path) -> str:
    if not todo_path.exists(): return TODO_TEMPLATE
    return todo_path.read_text(encoding='utf-8')

# WRITES TODO FILE CONTENT
def _write_todo_file(todo_path: Path, content: str):
    todo_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.write_text(content, encoding='utf-8')

# REMOVES EMPTY LINES AFTER INSERTION, KEEPS ONE IF BEFORE SECTION
def _clean_empty_lines_after_insert(lines: list, insert_idx: int):
    if insert_idx + 1 >= len(lines): return
    next_non_empty = insert_idx + 1

    while next_non_empty < len(lines) and lines[next_non_empty].strip() == '':
        next_non_empty += 1

    if next_non_empty < len(lines) and lines[next_non_empty].startswith('####'):
        _remove_excess_empty_lines_before_section(lines, insert_idx, next_non_empty)
    else:
        _remove_all_empty_lines_after_insert(lines, insert_idx)

# REMOVES EXCESS EMPTY LINES BEFORE SECTION HEADER
def _remove_excess_empty_lines_before_section(lines: list, insert_idx: int, next_non_empty: int):
    empty_count = next_non_empty - insert_idx - 1
    if empty_count > 1:
        for _ in range(empty_count - 1):
            if lines[insert_idx + 1].strip() == '': del lines[insert_idx + 1]

# REMOVES ALL EMPTY LINES AFTER INSERT
def _remove_all_empty_lines_after_insert(lines: list, insert_idx: int):
    while insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip() == '':
        del lines[insert_idx + 1]

# EXTRACTS PREFIX AND TEXT FROM TASK LINE
def _extract_task_prefix_and_text(task_line: str) -> tuple[str, str]:
    match = re.match(r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*(\w+):\*\* (.+)', task_line)
    if match:
        prefix = match.group(1)
        task_text = match.group(2)
        for badge in PRIORITY_BADGES.values(): task_text = task_text.replace(badge, '').strip()
        return prefix, task_text
    
    match = re.match(r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*(\w+):\*\*', task_line)
    if match:
        prefix = match.group(1)
        task_text = re.sub(PATTERN_TASK_LINE, '', task_line).strip()
        for badge in PRIORITY_BADGES.values(): task_text = task_text.replace(badge, '').strip()
        return prefix, task_text
    
    return 'ing', task_line.strip()

# CONVERTS PREFIX TO "ing" FORM
def _prefix_to_ing(prefix: str) -> str:
    if prefix.endswith('ing'): return prefix
    if prefix.endswith('e'): return prefix[:-1] + 'ing'
    if prefix.endswith('y'): return prefix + 'ing'
    return prefix + 'ing'

# EXTRACTS TASK TEXT FROM TASKS LINE
def _extract_text_from_tasks_line(task_line: str) -> str:
    match = re.match(r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\* (.+)', task_line)
    if match:
        task_text = match.group(1)
        for badge in PRIORITY_BADGES.values(): task_text = task_text.replace(badge, '').strip()
        return task_text
    return re.sub(PATTERN_TASK_LINE, '', task_line).strip()

# EXTRACTS TASK TEXT FROM IN_PROGRESS LINE
def _extract_text_from_in_progress_line(task_line: str) -> str:
    match = re.match(r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+ing:\*\* (.+)', task_line)
    if match: return match.group(1).strip()
    match_empty = re.match(r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+ing:\*\*[\s]*$', task_line)
    if match_empty: return ''
    return re.sub(r'^[\s]*-[\s]+', '', task_line).strip()

# EXTRACTS TASK TEXT FROM DONE/IN_PROGRESS LINE
def _extract_task_text_from_line(task_line: str, section: str) -> str:
    if section == 'tasks': return _extract_text_from_tasks_line(task_line)
    if section == 'in_progress': return _extract_text_from_in_progress_line(task_line)
    return task_line.strip()

# INSERTS TASK LINE INTO SECTION
def _insert_task_into_section(lines: list, section_start: int, section_end: int, new_task_line: str, task_pattern: str):
    last_task_idx = -1
    for i in range(section_start + 1, min(section_end, len(lines))):
        if re.match(task_pattern, lines[i]): last_task_idx = i
    
    if last_task_idx != -1:
        insert_idx = last_task_idx + 1
        lines.insert(insert_idx, new_task_line)
        _clean_empty_lines_after_insert(lines, insert_idx)
    else:
        insert_idx = section_start + 1
        while insert_idx < len(lines) and lines[insert_idx].strip() == '': insert_idx += 1
        lines.insert(insert_idx, new_task_line)
        if insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip() == '': del lines[insert_idx + 1]

# FINDS SECTION BOUNDARIES IN LINES
def _find_section_boundaries(lines: list, start_idx: int, end_markers: list) -> int:
    for j in range(start_idx + 1, len(lines)):
        line_stripped = lines[j].strip()
        if any(line_stripped.startswith(marker) for marker in end_markers): return j
    return len(lines)

# CALCULATES INSERT INDEX FOR NEW SECTION
def _calculate_insert_idx(in_progress_start_idx: int, first_done_idx: int, badges_start_idx: int, lines_len: int) -> int:
    # TASK SECTION SHOULD BE BEFORE IN PROGRESS AND DONE
    if first_done_idx != -1: return first_done_idx
    if in_progress_start_idx != -1: return in_progress_start_idx
    if badges_start_idx < lines_len: return badges_start_idx
    return 1

# CREATES TASKS SECTION IF MISSING
def _ensure_tasks_section(lines: list, in_progress_start_idx: int, first_done_idx: int, badges_start_idx: int) -> tuple[int, int, int, int]:
    tasks_start_idx, tasks_end_idx = _find_tasks_section(lines)
    if tasks_end_idx == -1: return _create_new_tasks_section(lines, in_progress_start_idx, first_done_idx, badges_start_idx)
    else: return _reposition_existing_tasks_section(lines, tasks_start_idx, tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx)

# FINDS TASKS SECTION INDICES
def _find_tasks_section(lines: list) -> tuple[int, int]:
    for i, line in enumerate(lines):
        if re.match(PATTERN_TASK_HEADER, line):
            tasks_end_idx = _find_section_boundaries(lines, i, ['####', '**_'])
            return i, tasks_end_idx
    return -1, -1

# CREATES NEW TASKS SECTION
def _create_new_tasks_section(lines: list, in_progress_start_idx: int, first_done_idx: int, badges_start_idx: int) -> tuple[int, int, int, int]:
    insert_idx = _calculate_insert_idx(in_progress_start_idx, first_done_idx, badges_start_idx, len(lines))
    tasks_section = ['', '#### TASK', '', '']
    for i, section_line in enumerate(tasks_section): lines.insert(insert_idx + i, section_line)
    
    tasks_end_idx = insert_idx + len(tasks_section)
    section_len = len(tasks_section)

    if in_progress_start_idx != -1 and in_progress_start_idx >= insert_idx: in_progress_start_idx += section_len
    if first_done_idx != -1 and first_done_idx >= insert_idx: first_done_idx += section_len

    badges_start_idx += section_len
    return tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx

# REPOSITIONS EXISTING TASKS SECTION
def _reposition_existing_tasks_section(lines: list, tasks_start_idx: int, tasks_end_idx: int, in_progress_start_idx: int, first_done_idx: int, badges_start_idx: int) -> tuple[int, int, int, int]:
    target_pos = _calculate_target_position(tasks_start_idx, in_progress_start_idx, first_done_idx)
    
    if target_pos != -1: tasks_end_idx, in_progress_start_idx, first_done_idx = _move_tasks_section(
            lines, tasks_start_idx, tasks_end_idx, target_pos, in_progress_start_idx, first_done_idx
        )
    
    return tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx

# CALCULATES TARGET POSITION FOR TASKS SECTION
def _calculate_target_position(tasks_start_idx: int, in_progress_start_idx: int, first_done_idx: int) -> int:
    if first_done_idx != -1 and tasks_start_idx > first_done_idx: return first_done_idx
    elif in_progress_start_idx != -1 and tasks_start_idx > in_progress_start_idx: return in_progress_start_idx
    return -1

# MOVES TASKS SECTION TO TARGET POSITION
def _move_tasks_section(lines: list, tasks_start_idx: int, tasks_end_idx: int, target_pos: int, in_progress_start_idx: int, first_done_idx: int) -> tuple[int, int, int]:
    task_section_lines = lines[tasks_start_idx:tasks_end_idx]
    del lines[tasks_start_idx:tasks_end_idx]
    for i, line in enumerate(task_section_lines): lines.insert(target_pos + i, line)

    section_len = len(task_section_lines)
    tasks_end_idx = target_pos + section_len
    
    in_progress_start_idx = _update_in_progress_idx_after_move(in_progress_start_idx, tasks_start_idx, target_pos, section_len)
    first_done_idx = _update_done_idx_after_move(first_done_idx, section_len)
    
    return tasks_end_idx, in_progress_start_idx, first_done_idx

# UPDATES IN PROGRESS INDEX AFTER TASK SECTION MOVE
def _update_in_progress_idx_after_move(in_progress_start_idx: int, tasks_start_idx: int, target_pos: int, section_len: int) -> int:
    if in_progress_start_idx != -1:
        if in_progress_start_idx >= tasks_start_idx or in_progress_start_idx >= target_pos: 
            in_progress_start_idx += section_len
    return in_progress_start_idx

# UPDATES DONE INDEX AFTER TASK SECTION MOVE
def _update_done_idx_after_move(first_done_idx: int, section_len: int) -> int:
    if first_done_idx != -1:
        first_done_idx += section_len
    return first_done_idx

# MOVES IN PROGRESS SECTION TO CORRECT POSITION
def _move_in_progress_section(lines: list, in_progress_start_idx: int, in_progress_end_idx: int, correct_idx: int) -> int:
    in_progress_lines = lines[in_progress_start_idx:in_progress_end_idx]
    del lines[in_progress_start_idx:in_progress_end_idx]
    if in_progress_start_idx < correct_idx: correct_idx -= (in_progress_end_idx - in_progress_start_idx)
    for i, section_line in enumerate(in_progress_lines): lines.insert(correct_idx + i, section_line)
    return correct_idx + len(in_progress_lines)

# REMOVES EMPTY PLACEHOLDERS FROM IN PROGRESS
def _remove_empty_placeholders(lines: list, start_idx: int, end_idx: int):
    lines_to_remove = []
    
    for i in range(start_idx + 1, end_idx):
        if re.match(PATTERN_EMPTY_ING, lines[i].strip()): lines_to_remove.append(i)
    
    for i in reversed(lines_to_remove):
        del lines[i]
        if end_idx > i: end_idx -= 1

# FINDS IN PROGRESS SECTION POSITION
def _find_in_progress_position(lines: list) -> tuple[int, int]:
    for i, line in enumerate(lines):
        if re.match(PATTERN_IN_PROGRESS, line):
            end_idx = _find_section_boundaries(lines, i, ['####', '**_', '['])
            return i, end_idx
    return -1, -1

# HANDLES IN PROGRESS SECTION
def _handle_in_progress_section(lines: list, in_progress_start_idx: int, in_progress_end_idx: int, correct_idx: int, first_done_idx: int, badges_start_idx: int) -> int:
    if in_progress_start_idx != -1:
        if in_progress_start_idx != correct_idx: badges_start_idx = _move_in_progress_section(lines, in_progress_start_idx, in_progress_end_idx, correct_idx)
        in_progress_start_idx, in_progress_end_idx = _find_in_progress_position(lines)
        if in_progress_start_idx != -1: _remove_empty_placeholders(lines, in_progress_start_idx, in_progress_end_idx)
    else:
        in_progress_section = ['', '#### IN PROGRESS', '', '']
        for i, section_line in enumerate(in_progress_section): lines.insert(correct_idx + i, section_line)
        if first_done_idx != -1: first_done_idx += len(in_progress_section)
        badges_start_idx += len(in_progress_section)
    
    return badges_start_idx

# CHECKS IF DONE SECTIONS EXIST
def _check_done_sections(lines: list) -> tuple[bool, bool]:
    has_done_simple = any(re.match(PATTERN_DONE_SIMPLE, line.strip()) for line in lines)
    has_done_versioned = any(re.match(PATTERN_DONE, line.strip()) and not re.match(PATTERN_DONE_SIMPLE, line.strip()) for line in lines)
    return has_done_simple, has_done_versioned

# REMOVES EMPTY SIMPLE DONE SECTION
def _remove_empty_simple_done(lines: list) -> bool:
    for i, line in enumerate(lines):
        if re.match(PATTERN_DONE_SIMPLE, line.strip()):
            simple_done_end = _find_section_boundaries(lines, i, ['####', '**_', '['])
            section_content = [l.strip() for l in lines[i:simple_done_end] if l.strip() and not l.strip().startswith('####')]
            if not section_content or (len(section_content) == 1 and section_content[0] == '- [x] **added:**'):
                del lines[i:simple_done_end]
                return False
            break
    return True

# HANDLES DONE SECTION
def _handle_done_section(lines: list, badges_start_idx: int):
    has_done_simple, has_done_versioned = _check_done_sections(lines)
    if has_done_versioned and has_done_simple: has_done_simple = _remove_empty_simple_done(lines)

    if not has_done_simple and not has_done_versioned:
        done_section = ['', '#### DONE', '', '- [x] **added:**', '']
        for i, section_line in enumerate(done_section):
            lines.insert(badges_start_idx + i, section_line)

# ENSURES REQUIRED SECTIONS EXIST IN TODO CONTENT
def _ensure_sections(content: str) -> str:
    lines = content.split('\n')
    initial_indices = _find_initial_section_indices(lines)
    
    tasks_end_idx, _unused1, _unused2, badges_start_idx = _ensure_tasks_section(
        lines, initial_indices['in_progress_start'], initial_indices['first_done'], initial_indices['badges_start']
    )
    
    recalculated_indices = _recalculate_section_indices(lines)
    correct_in_progress_idx = _calculate_correct_in_progress_position(tasks_end_idx, recalculated_indices['first_done'])
    
    badges_start_idx = _handle_in_progress_section(
        lines, recalculated_indices['in_progress_start'], recalculated_indices['in_progress_end'], 
        correct_in_progress_idx, recalculated_indices['first_done'], badges_start_idx
    )

    _handle_done_section(lines, badges_start_idx)
    
    return '\n'.join(lines)

# FINDS INITIAL SECTION INDICES IN LINES
def _find_initial_section_indices(lines: list) -> dict:
    in_progress_start_idx = -1
    first_done_idx = -1
    badges_start_idx = len(lines)

    for i, line in enumerate(lines):
        if in_progress_start_idx == -1 and re.match(PATTERN_IN_PROGRESS, line): in_progress_start_idx = i
        if first_done_idx == -1 and re.match(PATTERN_DONE, line.strip()) and not re.match(PATTERN_DONE_SIMPLE, line.strip()): first_done_idx = i
        if line.strip().startswith('[') and ']:' in line and badges_start_idx == len(lines): badges_start_idx = i
    
    return {'in_progress_start': in_progress_start_idx, 'first_done': first_done_idx, 'badges_start': badges_start_idx}

# RECALCULATES SECTION INDICES AFTER TASK REORGANIZATION
def _recalculate_section_indices(lines: list) -> dict:
    in_progress_start_idx = -1
    in_progress_end_idx = -1
    first_done_idx = -1
    
    for i, line in enumerate(lines):
        if in_progress_start_idx == -1 and re.match(PATTERN_IN_PROGRESS, line):
            in_progress_start_idx = i
            in_progress_end_idx = _find_section_boundaries(lines, i, ['####', '**_', '['])
        if first_done_idx == -1 and re.match(PATTERN_DONE, line.strip()) and not re.match(PATTERN_DONE_SIMPLE, line.strip()): first_done_idx = i
    
    return {'in_progress_start': in_progress_start_idx, 'in_progress_end': in_progress_end_idx, 'first_done': first_done_idx}

# CALCULATES CORRECT POSITION FOR IN PROGRESS SECTION
def _calculate_correct_in_progress_position(tasks_end_idx: int, first_done_idx: int) -> int:
    if first_done_idx != -1: return first_done_idx
    return tasks_end_idx

# FINDS DONE SECTION (PREFERS SIMPLE OVER VERSIONED)
def _find_done_section(lines: list) -> int:
    for i, line in enumerate(lines):
        if re.match(PATTERN_DONE_SIMPLE, line.strip()): return i
    for i, line in enumerate(lines):
        if re.match(PATTERN_DONE, line.strip()) and not re.match(PATTERN_DONE_SIMPLE, line.strip()): return i
    return -1

# FINDS SECTION START INDEX
def _find_section_start(lines: list, section_name: str, pattern: str) -> int:
    if section_name == 'done': return _find_done_section(lines)
    for i, line in enumerate(lines):
        if re.match(pattern, line): return i
    return -1

# FINDS SECTION IN TODO CONTENT
def _find_section(content: str, section_name: str) -> tuple[int, int]:
    patterns = {'tasks': PATTERN_TASK_HEADER, 'in_progress': PATTERN_IN_PROGRESS, 'done': PATTERN_DONE}
    
    pattern = patterns.get(section_name.lower())
    if not pattern:
        raise ValueError(f"UNKNOWN SECTION: {section_name}")
    
    lines = content.split('\n')
    start_idx = _find_section_start(lines, section_name, pattern)
    if start_idx == -1: return -1, -1

    end_idx = _find_section_boundaries(lines, start_idx, ['####', '**_'])
    return start_idx, end_idx

# CREATES TASK LINE WITH OPTIONAL PRIORITY
def _create_task_line(prefix: str, task_text: str, priority: Optional[Literal['high', 'mid', 'low']] = None) -> str:
    if priority:
        priority_badge = PRIORITY_BADGES.get(priority or 'mid', PRIORITY_BADGES['mid'])
        return f"- [ ] **{prefix}:** {priority_badge} {task_text}"
    return f"- [ ] **{prefix}:** {task_text}"

# FINDS LAST TASK INDEX IN SECTION
def _find_last_task_in_section(lines: list, start_idx: int, end_idx: int) -> int:
    last_task_idx = -1
    for i in range(start_idx + 1, end_idx):
        if re.match(PATTERN_TASK_LINE, lines[i]): last_task_idx = i
    return last_task_idx

# INSERTS TASK LINE INTO EMPTY SECTION
def _insert_task_into_empty_section(lines: list, start_idx: int, task_line: str):
    insert_idx = start_idx + 1
    while insert_idx < len(lines) and lines[insert_idx].strip() == '': insert_idx += 1
    empty_before = insert_idx - start_idx - 1
    
    if empty_before > 1:
        for _ in range(empty_before - 1):
            if start_idx + 1 >= len(lines): break
            if lines[start_idx + 1].strip() == '':
                del lines[start_idx + 1]
                insert_idx -= 1
    lines.insert(insert_idx, task_line)

# ADDS TASK TO SECTION
def _add_task_to_section(content: str, section: str, task_text: str, prefix: str = 'fix', priority: Optional[Literal['high', 'mid', 'low']] = None) -> str:
    if section != 'tasks':
        raise ValueError(f"CANNOT ADD TASK TO SECTION: {section}")
    
    content = _ensure_sections(content)
    lines = content.split('\n')
    start_idx, end_idx = _find_section(content, section)
    
    if start_idx == -1:
        raise ValueError(f"SECTION '{section}' NOT FOUND IN TODO FILE")
    
    task_line = _create_task_line(prefix, task_text, priority)
    last_task_idx = _find_last_task_in_section(lines, start_idx, end_idx)
    
    if last_task_idx != -1:
        insert_idx = last_task_idx + 1
        lines.insert(insert_idx, task_line)
        _clean_empty_lines_after_insert(lines, insert_idx)
    else:
        _insert_task_into_empty_section(lines, start_idx, task_line)
    
    return '\n'.join(lines)

# GETS TASK LINE BY INDEX
def _get_task_line_by_index(lines: list, task_lines: list, task_index: int) -> tuple[int, str]:
    if task_index < 0 or task_index >= len(task_lines):
        raise ValueError(f"TASK INDEX {task_index} OUT OF RANGE")
    task_line_idx = task_lines[task_index]
    return task_line_idx, lines[task_line_idx]

# MOVES TASK TO IN PROGRESS
def _move_to_in_progress(content: str, task_index: int, section: str) -> str:
    content = _ensure_sections(content)
    lines = content.split('\n')
    task_lines = _find_task_lines_in_section(lines, section)
    
    task_line_idx, task_line = _get_task_line_by_index(lines, task_lines, task_index)
    prefix, task_text = _extract_task_prefix_and_text(task_line)
    lines.pop(task_line_idx)
    
    updated_content = '\n'.join(lines)
    updated_content = _ensure_sections(updated_content)
    lines = updated_content.split('\n')

    prefix_ing = _prefix_to_ing(prefix)
    new_task_line = f"- [ ] **{prefix_ing}:** {task_text}"

    in_progress_start, in_progress_end = _find_section(updated_content, 'in_progress')
    if in_progress_start == -1:
        raise ValueError("IN PROGRESS SECTION NOT FOUND")
    
    _insert_task_into_section(lines, in_progress_start, in_progress_end, new_task_line, PATTERN_TASK_ING)
    
    return '\n'.join(lines)

# MOVES TASK TO DONE
def _move_to_done(content: str, task_index: int, section: str) -> str:
    content = _ensure_sections(content)
    lines = content.split('\n')
    task_lines = _find_task_lines_in_section(lines, section)
    
    task_line_idx, task_line = _get_task_line_by_index(lines, task_lines, task_index)
    task_text = _extract_task_text_from_line(task_line, section)
    lines.pop(task_line_idx)
    
    updated_content = '\n'.join(lines)
    updated_content = _ensure_sections(updated_content)
    lines = updated_content.split('\n')

    new_task_line = f"- [x] **added:** {task_text}"
    
    done_start, done_end = _find_section(updated_content, 'done')
    if done_start == -1:
        raise ValueError("DONE SECTION NOT FOUND")
    
    _insert_task_into_section(lines, done_start, done_end, new_task_line, PATTERN_DONE_TASK)
    
    return '\n'.join(lines)

# FINDS TASK LINES IN SECTION
def _find_task_lines_in_section(lines: list, section: str) -> list[int]:
    task_lines = []
    patterns = { 'tasks': PATTERN_TASK_LINE, 'in_progress': PATTERN_TASK_ING, 'done': PATTERN_DONE_TASK }
    pattern = patterns.get(section)
    if pattern:
        for i, line in enumerate(lines):
            if re.match(pattern, line): task_lines.append(i)
    return task_lines

# REMOVES TASK FROM SECTION
def _remove_task(content: str, task_index: int, section: str) -> str:
    lines = content.split('\n')
    task_lines = _find_task_lines_in_section(lines, section)
    
    if task_index < 0 or task_index >= len(task_lines):
        raise ValueError(f"TASK INDEX {task_index} OUT OF RANGE")
    
    lines.pop(task_lines[task_index])
    return '\n'.join(lines)

# ADDS A TASK
def autotodo_add_task(todo_path: str, description: str, prefix: str = 'fix', priority: Optional[Literal['high', 'mid', 'low']] = None):
    todo_file = Path(todo_path)
    content = _read_todo_file(todo_file)
    content = _add_task_to_section(content, 'tasks', description, prefix, priority)
    _write_todo_file(todo_file, content)
    return str(todo_file)

# MOVES TASK TO IN PROGRESS
def autotodo_start(todo_path: str, task_index: int, section: Literal['tasks']):
    todo_file = Path(todo_path)
    content = _read_todo_file(todo_file)
    content = _move_to_in_progress(content, task_index, section)
    _write_todo_file(todo_file, content)
    return str(todo_file)

# MOVES TASK TO DONE
def autotodo_done(todo_path: str, task_index: int, section: Literal['tasks', 'in_progress']):
    todo_file = Path(todo_path)
    content = _read_todo_file(todo_file)
    content = _move_to_done(content, task_index, section)
    _write_todo_file(todo_file, content)
    return str(todo_file)

# REMOVES TASK
def autotodo_remove(todo_path: str, task_index: int, section: Literal['tasks', 'in_progress', 'done']):
    todo_file = Path(todo_path)
    content = _read_todo_file(todo_file)
    content = _remove_task(content, task_index, section)
    _write_todo_file(todo_file, content)
    return str(todo_file)

# EXTRACTS TASK LINES FROM SECTION
def _extract_task_lines_from_section(lines: list, start_idx: int, end_idx: int) -> list[str]:
    section_lines = []
    for i in range(start_idx + 1, min(end_idx, len(lines))):
        line = lines[i]
        stripped = line.strip()
        if stripped == '' or stripped == '---': continue
        if stripped.startswith('####') or (stripped.startswith('[') and ']:' in stripped): break
        if stripped.startswith('-'): section_lines.append(stripped)
    return section_lines

# LISTS TASKS IN SECTION
def autotodo_list(todo_path: str, section: Optional[Literal['tasks', 'in_progress', 'done']] = None):
    todo_file = Path(todo_path)
    content = _read_todo_file(todo_file)
    content = _ensure_sections(content)
    
    sections_to_show = [section] if section else ['tasks', 'in_progress', 'done']
    result = []
    
    for sec in sections_to_show:
        try: start_idx, end_idx = _find_section(content, sec)
        except ValueError: continue
        if start_idx == -1: continue

        lines = content.split('\n')
        section_lines = _extract_task_lines_from_section(lines, start_idx, end_idx)
        if section_lines: result.append((sec, section_lines))
    
    return result
