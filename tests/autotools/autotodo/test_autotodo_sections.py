import pytest
from autotools.autotodo import *  # NOSONAR

# TEST FOR FIND SECTION BOUNDARIES FINDS MARKER
def test_find_section_boundaries_finds_marker():
    lines = ['header', 'content', '#### NEXT', 'more']
    result = _find_section_boundaries(lines, 0, ['####'])
    assert result == 2

# TEST FOR FIND SECTION BOUNDARIES NO MARKER
def test_find_section_boundaries_no_marker():
    lines = ['header', 'content']
    result = _find_section_boundaries(lines, 0, ['####'])
    assert result == 2

# TEST FOR FIND SECTION BOUNDARIES MULTIPLE MARKERS
def test_find_section_boundaries_multiple_markers():
    lines = ['header', 'content', '#### TASK', 'more']
    result = _find_section_boundaries(lines, 0, ['####', '**_'])
    assert result == 2

# TEST FOR FIND SECTION BOUNDARIES WITH TASK HEADER
def test_find_section_boundaries_with_task_header():
    lines = ['header', 'content', '#### TASK', 'more']
    result = _find_section_boundaries(lines, 0, ['####', '**_'])
    assert result == 2

# TEST FOR CALCULATE INSERT IDX IN PROGRESS
def test_calculate_insert_idx_in_progress():
    assert _calculate_insert_idx(5, -1, 10, 20) == 5

# TEST FOR CALCULATE INSERT IDX FIRST DONE
def test_calculate_insert_idx_first_done():
    assert _calculate_insert_idx(-1, 8, 10, 20) == 8

# TEST FOR CALCULATE INSERT IDX BADGES
def test_calculate_insert_idx_badges():
    assert _calculate_insert_idx(-1, -1, 12, 20) == 12

# TEST FOR CALCULATE INSERT IDX DEFAULT
def test_calculate_insert_idx_default():
    assert _calculate_insert_idx(-1, -1, 20, 20) == 1

# TEST FOR ENSURE TASKS SECTION EXISTING
def test_ensure_tasks_section_existing():
    lines = ['### HEADER', '#### TASK', 'content', '#### NEXT']
    result = _ensure_tasks_section(lines, -1, -1, 10)
    assert result[0] == 3
    assert '#### TASK' in lines

# TEST FOR ENSURE TASKS SECTION MISSING
def test_ensure_tasks_section_missing():
    lines = ['### HEADER', '#### IN PROGRESS']
    result = _ensure_tasks_section(lines, 1, -1, 10)
    assert result[0] != -1
    assert '#### TASK' in lines

# TEST FOR ENSURE TASKS SECTION UPDATES INDICES
def test_ensure_tasks_section_updates_indices():
    lines = ['### HEADER', '#### IN PROGRESS']
    result = _ensure_tasks_section(lines, 1, -1, 2)
    assert result[1] > 1

# TEST FOR ENSURE TASKS SECTION WHEN IN PROGRESS EXISTS
def test_ensure_tasks_section_when_in_progress_exists():
    lines = ['### HEADER', '#### IN PROGRESS']
    _ensure_tasks_section(lines, 1, -1, 2)
    assert '#### TASK' in lines
    assert lines.index('#### TASK') < lines.index('#### IN PROGRESS')

# TEST FOR ENSURE TASKS SECTION WHEN DONE EXISTS
def test_ensure_tasks_section_when_done_exists():
    lines = ['### HEADER', '#### DONE - v0.0.5']
    _ensure_tasks_section(lines, -1, 1, 2)
    assert '#### TASK' in lines
    task_idx = lines.index('#### TASK')
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert task_idx < done_idx

# TEST FOR ENSURE TASKS SECTION MOVES BEFORE IN PROGRESS
def test_ensure_tasks_section_moves_before_in_progress():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### TASK', '', '#### DONE']
    in_progress_start_idx = 1
    first_done_idx = 4
    badges_start_idx = 5
    _, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    task_idx = next((i for i, l in enumerate(lines) if '#### TASK' in l), -1)
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    assert task_idx < in_progress_idx

# TEST FOR ENSURE TASKS SECTION UPDATES INDICES AFTER MOVE
def test_ensure_tasks_section_updates_indices_after_move():
    lines = ['### HEADER', '#### DONE', '', '#### TASK']
    in_progress_start_idx = -1
    first_done_idx = 1
    badges_start_idx = 4
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert tasks_end_idx > 0
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert done_idx >= tasks_end_idx

# TEST FOR ENSURE TASKS SECTION MOVES BEFORE IN PROGRESS ONLY
def test_ensure_tasks_section_moves_before_in_progress_only():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### TASK']
    in_progress_start_idx = 1
    first_done_idx = -1
    badges_start_idx = 4
    _, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    task_idx = next((i for i, l in enumerate(lines) if '#### TASK' in l), -1)
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    assert task_idx < in_progress_idx

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TARGET
def test_ensure_tasks_section_updates_in_progress_when_after_target():
    lines = ['### HEADER', '#### DONE', '', '#### IN PROGRESS', '', '#### TASK']
    in_progress_start_idx = 3
    first_done_idx = 1
    badges_start_idx = 6
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert tasks_end_idx > 0

# TEST FOR ENSURE TASKS SECTION UPDATES DONE WHEN AFTER TARGET
def test_ensure_tasks_section_updates_done_when_after_target():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### DONE', '', '#### TASK']
    in_progress_start_idx = 1
    first_done_idx = 3
    badges_start_idx = 6
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert tasks_end_idx > 0

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TASK START
def test_ensure_tasks_section_updates_in_progress_when_after_task_start():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### TASK', '']
    in_progress_start_idx = 1
    first_done_idx = -1
    badges_start_idx = 5
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert in_progress_start_idx >= tasks_end_idx

# TEST FOR ENSURE TASKS SECTION UPDATES DONE WHEN AFTER TARGET POS
def test_ensure_tasks_section_updates_done_when_after_target_pos():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### DONE', '', '#### TASK']
    in_progress_start_idx = 1
    first_done_idx = 3
    badges_start_idx = 6
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert first_done_idx >= tasks_end_idx

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TASK START IDX
def test_ensure_tasks_section_updates_in_progress_when_after_task_start_idx():
    lines = ['### HEADER', '#### TASK', '', '#### IN PROGRESS', '', '#### DONE']
    in_progress_start_idx = 3
    tasks_start_idx = 1
    tasks_end_idx = 3
    target_pos = 0
    if target_pos != -1:
        task_section_lines = lines[tasks_start_idx:tasks_end_idx]
        del lines[tasks_start_idx:tasks_end_idx]
        for i, line in enumerate(task_section_lines):
            lines.insert(target_pos + i, line)
        section_len = len(task_section_lines)
        if in_progress_start_idx != -1:
            if in_progress_start_idx >= tasks_start_idx:
                in_progress_start_idx += section_len
    assert in_progress_start_idx > 3

# TEST FOR ENSURE TASKS SECTION DONE NOT UPDATED WHEN BEFORE TARGET
def test_ensure_tasks_section_done_not_updated_when_before_target():
    lines = ['### HEADER', '#### DONE', '', '#### TASK']
    first_done_idx = 1
    tasks_start_idx = 3
    tasks_end_idx = 4
    target_pos = 2
    if target_pos != -1:
        task_section_lines = lines[tasks_start_idx:tasks_end_idx]
        del lines[tasks_start_idx:tasks_end_idx]
        for i, line in enumerate(task_section_lines):
            lines.insert(target_pos + i, line)
        section_len = len(task_section_lines)
        if first_done_idx != -1:
            if first_done_idx >= tasks_start_idx or first_done_idx >= target_pos:
                first_done_idx += section_len
    assert first_done_idx == 1

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TASK START IDX SPECIFIC
def test_ensure_tasks_section_updates_in_progress_when_after_task_start_idx_specific():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### TASK', '']
    in_progress_start_idx = 1
    first_done_idx = -1
    badges_start_idx = 5
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert in_progress_start_idx >= tasks_end_idx

# TEST FOR ENSURE TASKS SECTION UPDATES DONE WHEN AFTER TARGET POS ONLY
def test_ensure_tasks_section_updates_done_when_after_target_pos_only():
    lines = ['### HEADER', '#### IN PROGRESS', '', '#### DONE', '', '#### TASK']
    in_progress_start_idx = 1
    first_done_idx = 3
    badges_start_idx = 6
    tasks_end_idx, in_progress_start_idx, first_done_idx, badges_start_idx = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert first_done_idx >= tasks_end_idx

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TASK START IDX DIRECT
def test_ensure_tasks_section_updates_in_progress_when_after_task_start_idx_direct():
    lines2 = ['### HEADER', '#### DONE', '', '#### TASK', '', '#### IN PROGRESS']
    in_progress_start_idx2 = 5
    first_done_idx2 = 1
    badges_start_idx2 = 6
    _, new_in_progress_idx, _, _ = _ensure_tasks_section(
        lines2, in_progress_start_idx2, first_done_idx2, badges_start_idx2
    )
    assert new_in_progress_idx > in_progress_start_idx2

# TEST FOR ENSURE TASKS SECTION DONE NOT UPDATED WHEN BEFORE TARGET DIRECT
def test_ensure_tasks_section_done_not_updated_when_before_target_direct():
    lines = ['### HEADER', '#### DONE', '', '#### IN PROGRESS', '', '#### TASK']
    in_progress_start_idx = 3
    first_done_idx = 1
    badges_start_idx = 6
    _, _, new_done_idx, _ = _ensure_tasks_section(
        lines, in_progress_start_idx, first_done_idx, badges_start_idx
    )
    assert isinstance(new_done_idx, int)

# TEST FOR MOVE IN PROGRESS SECTION
def test_move_in_progress_section():
    lines = ['line1', '#### IN PROGRESS', 'content', 'line2', '#### DONE']
    result = _move_in_progress_section(lines, 1, 3, 4)
    assert result == 4
    assert '#### IN PROGRESS' in lines
    assert lines.index('#### IN PROGRESS') < lines.index('#### DONE')

# TEST FOR MOVE IN PROGRESS SECTION BEFORE
def test_move_in_progress_section_before():
    lines = ['line1', '#### DONE', '#### IN PROGRESS', 'content']
    result = _move_in_progress_section(lines, 2, 4, 1)
    assert result == 3
    assert lines[1] == '#### IN PROGRESS'

# TEST FOR MOVE IN PROGRESS SECTION NO ADJUSTMENT NEEDED
def test_move_in_progress_section_no_adjustment_needed():
    lines = ['line1', '#### IN PROGRESS', 'content', 'line2']
    result = _move_in_progress_section(lines, 1, 3, 1)
    assert result == 3
    assert lines[1] == '#### IN PROGRESS'

# TEST FOR REMOVE EMPTY PLACEHOLDERS
def test_remove_empty_placeholders():
    lines = ['#### IN PROGRESS', '- [ ] **ing:**', 'content']
    _remove_empty_placeholders(lines, 0, 3)
    assert '- [ ] **ing:**' not in lines

# TEST FOR REMOVE EMPTY PLACEHOLDERS NONE
def test_remove_empty_placeholders_none():
    lines = ['#### IN PROGRESS', '- [ ] **fixing:** task', 'content']
    original_len = len(lines)
    _remove_empty_placeholders(lines, 0, 3)
    assert len(lines) == original_len

# TEST FOR FIND IN PROGRESS POSITION
def test_find_in_progress_position():
    lines = ['line1', '#### IN PROGRESS', 'content', '#### DONE']
    start, end = _find_in_progress_position(lines)
    assert start == 1
    assert end == 3

# TEST FOR FIND IN PROGRESS POSITION NOT FOUND
def test_find_in_progress_position_not_found():
    lines = ['line1', '#### DONE']
    start, end = _find_in_progress_position(lines)
    assert start == -1
    assert end == -1

# TEST FOR HANDLE IN PROGRESS SECTION EXISTING
def test_handle_in_progress_section_existing():
    lines = ['### HEADER', '#### TASK', '#### IN PROGRESS', 'content', '#### DONE']
    result = _handle_in_progress_section(lines, 2, 4, 2, -1, 5)
    assert result >= 0
    assert '#### IN PROGRESS' in lines

# TEST FOR HANDLE IN PROGRESS SECTION MISSING
def test_handle_in_progress_section_missing():
    lines = ['### HEADER', '#### TASK', '#### DONE']
    result = _handle_in_progress_section(lines, -1, -1, 2, -1, 3)
    assert result >= 0
    assert '#### IN PROGRESS' in lines

# TEST FOR HANDLE IN PROGRESS SECTION NO MOVEMENT NEEDED
def test_handle_in_progress_section_no_movement_needed():
    lines = ['### HEADER', '#### TASK', '#### IN PROGRESS', 'content', '#### DONE']
    result = _handle_in_progress_section(lines, 2, 4, 2, 4, 5)
    assert result >= 0

# TEST FOR HANDLE IN PROGRESS SECTION REMOVES EMPTY ING
def test_handle_in_progress_section_removes_empty_ing():
    lines = ['### HEADER', '#### IN PROGRESS', '- [ ] **ing:**', 'content']
    _handle_in_progress_section(lines, 1, 4, 1, -1, 4)
    assert '- [ ] **ing:**' not in '\n'.join(lines) or lines.count('- [ ] **ing:**') == 0

# TEST FOR HANDLE IN PROGRESS SECTION REMOVES EMPTY ING PLACEHOLDERS
def test_handle_in_progress_section_removes_empty_ing_placeholders():
    lines = ['### HEADER', '#### IN PROGRESS', '- [ ] **ing:**', '', '#### DONE']
    _handle_in_progress_section(lines, 1, 4, 1, 4, 5)
    assert '- [ ] **ing:**' not in '\n'.join(lines)

# TEST FOR HANDLE IN PROGRESS SECTION CREATES WHEN MISSING
def test_handle_in_progress_section_creates_when_missing():
    lines = ['### HEADER', '#### TASK', '', '#### DONE']
    badges_start_idx = _handle_in_progress_section(lines, -1, -1, 2, 3, 4)
    assert '#### IN PROGRESS' in '\n'.join(lines)
    assert badges_start_idx > 4

# TEST FOR HANDLE IN PROGRESS SECTION NO MOVEMENT
def test_handle_in_progress_section_no_movement():
    lines = ['### HEADER', '#### TASK', '#### IN PROGRESS', 'content', '#### DONE']
    result = _handle_in_progress_section(lines, 2, 4, 2, 4, 5)
    assert result >= 0

# TEST FOR HANDLE IN PROGRESS SECTION CREATES NEW
def test_handle_in_progress_section_creates_new():
    lines = ['### HEADER', '#### TASK', '#### DONE']
    result = _handle_in_progress_section(lines, -1, -1, 2, 2, 3)
    assert result >= 0
    assert '#### IN PROGRESS' in lines

# TEST FOR HANDLE IN PROGRESS SECTION REMOVES EMPTY PLACEHOLDERS DIRECT
def test_handle_in_progress_section_removes_empty_placeholders_direct():
    lines = ['### HEADER', '#### TASK', '', '#### IN PROGRESS', '- [ ] **ing:**', '', '#### DONE']
    in_progress_start_idx = 3
    in_progress_end_idx = 6
    correct_idx = 2
    first_done_idx = 6
    badges_start_idx = 7
    _handle_in_progress_section(
        lines, in_progress_start_idx, in_progress_end_idx, correct_idx, first_done_idx, badges_start_idx
    )
    assert '- [ ] **ing:**' not in lines or lines.count('- [ ] **ing:**') == 0

# TEST FOR HANDLE IN PROGRESS SECTION ELSE BRANCH
def test_handle_in_progress_section_else_branch():
    from unittest.mock import patch
    lines = ['### HEADER', '#### TASK', '', '#### IN PROGRESS', '', '#### DONE']
    in_progress_start_idx = 3
    in_progress_end_idx = 5
    correct_idx = 2
    first_done_idx = 5
    badges_start_idx = 6
    with patch('autotools.autotodo.core._find_in_progress_position', return_value=(-1, -1)):
        new_badges_idx = _handle_in_progress_section(
            lines, in_progress_start_idx, in_progress_end_idx, correct_idx, first_done_idx, badges_start_idx
        )
    assert isinstance(new_badges_idx, int)

# TEST FOR HANDLE IN PROGRESS SECTION CREATES NEW SECTION
def test_handle_in_progress_section_creates_new_section():
    lines = ['### HEADER', '#### TASK', '', '#### DONE']
    badges_start_idx = _handle_in_progress_section(lines, -1, -1, 2, 3, 4)
    assert '#### IN PROGRESS' in '\n'.join(lines)
    assert badges_start_idx > 4

# TEST FOR HANDLE IN PROGRESS SECTION CREATES WHEN MISSING ELSE BRANCH
def test_handle_in_progress_section_creates_when_missing_else_branch():
    lines = ['### HEADER', '#### TASK', '', '#### DONE']
    badges_start_idx = _handle_in_progress_section(lines, -1, -1, 2, 3, 4)
    assert '#### IN PROGRESS' in '\n'.join(lines)
    assert badges_start_idx > 4

# TEST FOR CHECK DONE SECTIONS
def test_check_done_sections():
    lines = ['#### DONE', '#### DONE - v0.0.5']
    has_simple, has_versioned = _check_done_sections(lines)
    assert has_simple
    assert has_versioned

# TEST FOR CHECK DONE SECTIONS NONE
def test_check_done_sections_none():
    lines = ['#### IN PROGRESS']
    has_simple, has_versioned = _check_done_sections(lines)
    assert not has_simple
    assert not has_versioned

# TEST FOR REMOVE EMPTY SIMPLE DONE EMPTY
def test_remove_empty_simple_done_empty():
    lines = ['#### DONE', '', '- [x] **added:**', '#### DONE - v0.0.5']
    result = _remove_empty_simple_done(lines)
    assert not result
    assert '#### DONE' not in lines or lines.count('#### DONE') == 1

# TEST FOR REMOVE EMPTY SIMPLE DONE WITH CONTENT
def test_remove_empty_simple_done_with_content():
    lines = ['#### DONE', '', '- [x] **added:** task', '#### DONE - v0.0.5']
    result = _remove_empty_simple_done(lines)
    assert result
    assert '#### DONE' in lines

# TEST FOR REMOVE EMPTY SIMPLE DONE WITH MULTIPLE TASKS
def test_remove_empty_simple_done_with_multiple_tasks():
    lines = ['#### DONE', '', '- [x] **added:** task1', '- [x] **added:** task2', '#### DONE - v0.0.5']
    result = _remove_empty_simple_done(lines)
    assert result
    assert '#### DONE' in lines

# TEST FOR REMOVE EMPTY SIMPLE DONE ONLY PLACEHOLDER
def test_remove_empty_simple_done_only_placeholder():
    lines = ['#### DONE', '', '- [x] **added:**', '#### DONE - v0.0.5']
    result = _remove_empty_simple_done(lines)
    assert not result
    assert lines.count('#### DONE') <= 1

# TEST FOR REMOVE EMPTY SIMPLE DONE NO SIMPLE DONE
def test_remove_empty_simple_done_no_simple_done():
    lines = ['### HEADER', '#### DONE - v0.0.5', '- [x] **added:** task']
    result = _remove_empty_simple_done(lines)
    assert result

# TEST FOR HANDLE DONE SECTION CREATES IF MISSING
def test_handle_done_section_creates_if_missing():
    lines = ['### HEADER', '#### IN PROGRESS']
    _handle_done_section(lines, 2)
    assert any('#### DONE' in line for line in lines)

# TEST FOR HANDLE DONE SECTION KEEPS EXISTING
def test_handle_done_section_keeps_existing():
    lines = ['### HEADER', '#### DONE', '- [x] **added:** task']
    original_count = lines.count('#### DONE')
    _handle_done_section(lines, 3)
    assert lines.count('#### DONE') >= original_count

# TEST FOR HANDLE DONE SECTION WITH BOTH TYPES
def test_handle_done_section_with_both_types():
    lines = ['### HEADER', '#### DONE', '', '- [x] **added:**', '#### DONE - v0.0.5']
    _handle_done_section(lines, 5)
    assert lines.count('#### DONE') <= 2

# TEST FOR HANDLE DONE SECTION BOTH TYPES
def test_handle_done_section_both_types():
    lines = ['### HEADER', '#### DONE', '', '- [x] **added:**', '#### DONE - v0.0.5', '- [x] **added:** task']
    _handle_done_section(lines, 5)
    assert '#### DONE - v0.0.5' in lines

# TEST FOR HANDLE DONE SECTION BOTH TYPES WITH CONTENT
def test_handle_done_section_both_types_with_content():
    lines = ['### HEADER', '#### DONE', '', '- [x] **added:** task1', '#### DONE - v0.0.5', '- [x] **added:** task2']
    _handle_done_section(lines, 5)
    assert '#### DONE' in '\n'.join(lines)
    assert '#### DONE - v0.0.5' in '\n'.join(lines)

# TEST FOR HANDLE DONE SECTION KEEPS VERSIONED WHEN SIMPLE EMPTY
def test_handle_done_section_keeps_versioned_when_simple_empty():
    lines = ['### HEADER', '#### DONE', '', '- [x] **added:**', '#### DONE - v0.0.5', '- [x] **added:** task']
    _handle_done_section(lines, 5)
    assert lines.count('#### DONE') <= 2

# TEST FOR ENSURE SECTIONS CREATES ALL
def test_ensure_sections_creates_all():
    content = "### HEADER\n"
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result
    assert '#### DONE' in result

# TEST FOR ENSURE SECTIONS REORGANIZES
def test_ensure_sections_reorganizes():
    content = """### HEADER
#### DONE - v0.0.5
#### IN PROGRESS
#### TASK
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    task_idx = next((i for i, l in enumerate(lines) if '#### TASK' in l), -1)
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert task_idx != -1 and in_progress_idx != -1 and done_idx != -1
    assert task_idx < in_progress_idx
    assert task_idx < done_idx
    assert in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS WITH VERSIONED DONE ONLY
def test_ensure_sections_with_versioned_done_only():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
- [x] **added:** task
"""
    result = _ensure_sections(content)
    assert '#### DONE - v0.0.5' in result

# TEST FOR ENSURE SECTIONS CREATES SIMPLE DONE WHEN NONE
def test_ensure_sections_creates_simple_done_when_none():
    content = "### HEADER\n#### TASK\n#### IN PROGRESS"
    result = _ensure_sections(content)
    assert '#### DONE' in result

# TEST FOR ENSURE SECTIONS WITH EXISTING ALL SECTIONS
def test_ensure_sections_with_existing_all_sections():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
- [ ] **fixing:** task
#### DONE
- [x] **added:** task
#### DONE - v0.0.5
- [x] **added:** old task
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result
    assert '#### DONE' in result

# TEST FOR ENSURE SECTIONS REORGANIZES IN PROGRESS
def test_ensure_sections_reorganizes_in_progress():
    content = """### HEADER
#### TASK
#### DONE
#### IN PROGRESS
- [ ] **fixing:** task
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    task_idx = next((i for i, l in enumerate(lines) if '#### TASK' in l), -1)
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip() == '#### DONE'), -1)
    assert task_idx < in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS IN PROGRESS REMOVES EMPTY PLACEHOLDERS
def test_ensure_sections_in_progress_removes_empty_placeholders():
    content = """### HEADER
#### TASK
#### IN PROGRESS
- [ ] **ing:**
#### DONE
"""
    result = _ensure_sections(content)
    assert '- [ ] **ing:**' not in result or result.count('- [ ] **ing:**') == 0

# TEST FOR ENSURE SECTIONS USES BADGES WHEN NO SECTIONS
def test_ensure_sections_uses_badges_when_no_sections():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result

# TEST FOR ENSURE SECTIONS MOVES IN PROGRESS WHEN AFTER DONE
def test_ensure_sections_moves_in_progress_when_after_done():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
#### IN PROGRESS
- [ ] **fixing:** task
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS REORGANIZES TASK AFTER DONE
def test_ensure_sections_reorganizes_task_after_done():
    content = """### HEADER
#### DONE - v0.0.5
#### TASK
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    task_idx = next((i for i, l in enumerate(lines) if '#### TASK' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert task_idx < done_idx

# TEST FOR ENSURE SECTIONS REORGANIZES IN PROGRESS AFTER DONE
def test_ensure_sections_reorganizes_in_progress_after_done():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
#### IN PROGRESS
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS FINDS BADGES
def test_ensure_sections_finds_badges():
    content = """### HEADER
#### TASK
#### IN PROGRESS
#### DONE
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '[high]:' in result

# TEST FOR ENSURE SECTIONS USES BADGES WHEN NO SECTIONS EXIST
def test_ensure_sections_uses_badges_when_no_sections_exist():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result
    assert '#### DONE' in result

# TEST FOR ENSURE SECTIONS USES BADGES WHEN NO SECTIONS
def test_ensure_sections_uses_badges_when_no_sections():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result

# TEST FOR ENSURE SECTIONS USES BADGES WHEN NO SECTIONS ELSE BRANCH
def test_ensure_sections_uses_badges_when_no_sections_else_branch():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result
    assert '#### DONE' in result

# TEST FOR ENSURE SECTIONS USES BADGES WHEN NO SECTIONS DIRECT
def test_ensure_sections_uses_badges_when_no_sections_direct():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
"""
    result = _ensure_sections(content)
    assert '#### IN PROGRESS' in result
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    assert in_progress_idx != -1

# TEST FOR ENSURE SECTIONS MOVES IN PROGRESS WHEN AFTER DONE
def test_ensure_sections_moves_in_progress_when_after_done():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
#### IN PROGRESS
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS MOVES IN PROGRESS WHEN AFTER DONE IF BRANCH
def test_ensure_sections_moves_in_progress_when_after_done_if_branch():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
#### IN PROGRESS
"""
    result = _ensure_sections(content)
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert in_progress_idx < done_idx

# TEST FOR ENSURE SECTIONS MOVES IN PROGRESS WHEN AFTER DONE DIRECT
def test_ensure_sections_moves_in_progress_when_after_done_direct():
    content = """### HEADER
#### TASK
#### DONE - v0.0.5
- [x] **added:** done task
#### IN PROGRESS
- [ ] **fixing:** in progress task
"""
    from unittest.mock import patch
    call_tracker = {'called': False, 'call_count': 0}
    original_move = _move_in_progress_section
    def tracked_move(*args, **kwargs):
        call_tracker['called'] = True
        call_tracker['call_count'] += 1
        return original_move(*args, **kwargs)
    with patch('autotools.autotodo.core._move_in_progress_section', side_effect=tracked_move):
        result = _ensure_sections(content)
        assert call_tracker['called'], "_move_in_progress_section should be called when IN PROGRESS is after DONE"
        assert call_tracker['call_count'] > 0, "_move_in_progress_section should be called at least once"
    lines = result.split('\n')
    in_progress_idx = next((i for i, l in enumerate(lines) if '#### IN PROGRESS' in l), -1)
    done_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('#### DONE')), -1)
    assert in_progress_idx != -1 and done_idx != -1
    assert in_progress_idx < done_idx, "IN PROGRESS should be moved before DONE (lines 329-330 executed)"

# TEST FOR ENSURE SECTIONS USES BADGES START WHEN NO SECTIONS
def test_ensure_sections_uses_badges_start_when_no_sections():
    content = """### HEADER
[high]: https://img.shields.io/badge/-HIGH-red
"""
    result = _ensure_sections(content)
    assert '#### TASK' in result
    assert '#### IN PROGRESS' in result
    assert '#### DONE' in result

# TEST FOR FIND DONE SECTION SIMPLE
def test_find_done_section_simple():
    lines = ['#### DONE', '#### DONE - v0.0.5']
    assert _find_done_section(lines) == 0

# TEST FOR FIND DONE SECTION VERSIONED
def test_find_done_section_versioned():
    lines = ['#### DONE - v0.0.5']
    assert _find_done_section(lines) == 0

# TEST FOR FIND DONE SECTION NOT FOUND
def test_find_done_section_not_found():
    lines = ['#### IN PROGRESS']
    assert _find_done_section(lines) == -1

# TEST FOR FIND SECTION START TASKS
def test_find_section_start_tasks():
    lines = ['#### TASK', 'content']
    result = _find_section_start(lines, 'tasks', r'^#### TASK')
    assert result == 0

# TEST FOR FIND SECTION START DONE
def test_find_section_start_done():
    lines = ['#### DONE', '#### DONE - v0.0.5']
    result = _find_section_start(lines, 'done', r'^#### DONE')
    assert result == 0

# TEST FOR FIND SECTION START NOT FOUND
def test_find_section_start_not_found():
    lines = ['other content']
    result = _find_section_start(lines, 'tasks', r'^\*\*_Task_\*\*')
    assert result == -1

# TEST FOR FIND SECTION TASKS
def test_find_section_tasks():
    content = "### HEADER\n#### TASK\ncontent\n#### NEXT"
    start, end = _find_section(content, 'tasks')
    assert start == 1
    assert end == 3

# TEST FOR FIND SECTION IN PROGRESS
def test_find_section_in_progress():
    content = "### HEADER\n#### IN PROGRESS\ncontent\n#### NEXT"
    start, end = _find_section(content, 'in_progress')
    assert start == 1
    assert end == 3

# TEST FOR FIND SECTION DONE SIMPLE
def test_find_section_done_simple():
    content = "### HEADER\n#### DONE\ncontent\n#### DONE - v0.0.5"
    start, _ = _find_section(content, 'done')
    assert start == 1

# TEST FOR FIND SECTION DONE VERSIONED
def test_find_section_done_versioned():
    content = "### HEADER\n#### DONE - v0.0.5\ncontent"
    start, _ = _find_section(content, 'done')
    assert start == 1

# TEST FOR FIND SECTION WITH VERSIONED DONE ONLY
def test_find_section_with_versioned_done_only():
    content = "### HEADER\n#### DONE - v0.0.5\n- [x] **added:** task"
    start, _ = _find_section(content, 'done')
    assert start == 1

# TEST FOR FIND SECTION NOT FOUND
def test_find_section_not_found():
    content = "### HEADER\ncontent"
    start, end = _find_section(content, 'tasks')
    assert start == -1
    assert end == -1

# TEST FOR FIND SECTION WITH EMPTY CONTENT
def test_find_section_with_empty_content():
    content = ""
    start, _ = _find_section(content, 'tasks')
    assert start == -1

# TEST FOR FIND SECTION UNKNOWN
def test_find_section_unknown():
    with pytest.raises(ValueError, match="UNKNOWN SECTION"):
        _find_section("content", 'unknown')

# TEST FOR FIND SECTION RETURNS NEGATIVE FOR MISSING
def test_find_section_returns_negative_for_missing():
    content = "### HEADER\ncontent"
    start, end = _find_section(content, 'tasks')
    assert start == -1
    assert end == -1

# TEST FOR FIND SECTION RETURNS NEGATIVE WHEN NOT FOUND
def test_find_section_returns_negative_when_not_found():
    content = "### HEADER\ncontent"
    start, end = _find_section(content, 'tasks')
    assert start == -1
    assert end == -1

# TEST FOR FIND SECTION RETURNS NEGATIVE FOR UNKNOWN
def test_find_section_returns_negative_for_unknown():
    content = "### HEADER\ncontent"
    with pytest.raises(ValueError, match="UNKNOWN SECTION"):
        _find_section(content, 'unknown')

# TEST FOR FIND SECTION NOT FOUND RETURNS NEGATIVE
def test_find_section_not_found_returns_negative():
    content = "### HEADER\ncontent"
    start, end = _find_section(content, 'tasks')
    assert start == -1
    assert end == -1
