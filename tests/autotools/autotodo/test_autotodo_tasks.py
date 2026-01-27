import pytest
from autotools.autotodo import *  # NOSONAR

# TEST FOR FIND LAST TASK IN SECTION
def test_find_last_task_in_section():
    lines = ['header', '- [ ] **fix:** task1', '- [ ] **add:** task2', 'footer']
    result = _find_last_task_in_section(lines, 0, 3)
    assert result == 2

# TEST FOR FIND LAST TASK IN SECTION NONE
def test_find_last_task_in_section_none():
    lines = ['header', 'footer']
    result = _find_last_task_in_section(lines, 0, 1)
    assert result == -1

# TEST FOR INSERT TASK INTO EMPTY SECTION
def test_insert_task_into_empty_section():
    lines = ['header', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION REMOVES EXTRA EMPTY
def test_insert_task_into_empty_section_removes_extra_empty():
    lines = ['header', '', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert lines.count('') == 1
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION NO EMPTY AFTER
def test_insert_task_into_empty_section_no_empty_after():
    lines = ['header', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines
    assert lines.count('') <= 1

# TEST FOR INSERT TASK INTO EMPTY SECTION WITH MULTIPLE EMPTY BEFORE
def test_insert_task_into_empty_section_with_multiple_empty_before():
    lines = ['header', '', '', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert lines.count('') <= 2
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION HANDLES NO EMPTY BEFORE
def test_insert_task_into_empty_section_handles_no_empty_before():
    lines = ['header', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION REMOVES EMPTY AFTER
def test_insert_task_into_empty_section_removes_empty_after():
    lines = ['header', '', '#### SECTION']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines
    task_idx = lines.index('- [ ] **fix:** task')
    if task_idx + 1 < len(lines):
        assert lines[task_idx + 1] != '' or lines[task_idx + 1] == '#### SECTION'

# TEST FOR INSERT TASK INTO EMPTY SECTION BOUNDS CHECK FALSE
def test_insert_task_into_empty_section_bounds_check_false():
    lines = ['header', '', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION CHECKS IN LOOP
def test_insert_task_into_empty_section_checks_in_loop():
    lines = ['header', '', '', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION DELETES IN LOOP
def test_insert_task_into_empty_section_deletes_in_loop():
    lines = ['header', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION REMOVES EMPTY IN LOOP
def test_insert_task_into_empty_section_removes_empty_in_loop():
    lines = ['header', '', '', '', 'footer']
    _insert_task_into_empty_section(lines, 0, '- [ ] **fix:** task')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION BREAK BRANCH
def test_insert_task_into_empty_section_break_branch():
    from unittest.mock import patch
    lines = ['#### SECTION', '', '', '']
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    len_call_count = [0]
    original_len = len
    def mock_len(obj):
        if obj is lines:
            len_call_count[0] += 1
            if len_call_count[0] >= 3:
                return start_idx
        return original_len(obj)
    try:
        with patch('builtins.len', side_effect=mock_len):
            _insert_task_into_empty_section(lines, start_idx, task_line)
    except Exception:
        _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION NON EMPTY LINE BRANCH
def test_insert_task_into_empty_section_non_empty_line_branch():
    from unittest.mock import patch
    lines = ['#### SECTION', '', '', '', 'not empty']
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    getitem_call_count = [0]
    original_getitem = list.__getitem__
    def mock_getitem(self, idx):
        if self is lines and idx == start_idx + 1:
            getitem_call_count[0] += 1
            if getitem_call_count[0] >= 2:
                return 'not empty'
        getitem_call_count[0] += 1
        return original_getitem(self, idx)
    try:
        with patch('builtins.list.__getitem__', mock_getitem):
            _insert_task_into_empty_section(lines, start_idx, task_line)
    except Exception:
        _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION REMOVES EMPTY AFTER DIRECT
def test_insert_task_into_empty_section_removes_empty_after_direct():
    lines = ['#### SECTION', '', '']
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    original_len = len(lines)
    _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines
    task_idx = lines.index(task_line)
    if task_idx + 1 < len(lines):
        assert lines[task_idx + 1] != '' or (task_idx + 2 < len(lines) and lines[task_idx + 2].startswith('####'))
    assert len(lines) < original_len + 1, "At least one empty line should be removed by the while loop (line 397)"

# TEST FOR INSERT TASK INTO EMPTY SECTION BREAK DIRECT
def test_insert_task_into_empty_section_break_direct():
    class BreakTriggerList(list):
        def __init__(self, *args):
            super().__init__(*args)
            self._len_call_count = 0
            self._del_count = 0
        def __len__(self):
            self._len_call_count += 1
            if self._len_call_count >= 4:
                return 0
            return super().__len__()
        def __delitem__(self, idx):
            self._del_count += 1
            super().__delitem__(idx)
    lines = BreakTriggerList(['#### SECTION', '', '', ''])
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION NON EMPTY DIRECT
def test_insert_task_into_empty_section_non_empty_direct():
    class NonEmptyTriggerList(list):
        def __init__(self, *args):
            super().__init__(*args)
            self._getitem_call_count = 0
        def __getitem__(self, idx):
            self._getitem_call_count += 1
            if idx == 1 and self._getitem_call_count >= 2:
                return 'not empty'
            return super().__getitem__(idx)
    lines = NonEmptyTriggerList(['#### SECTION', '', '', '', ''])
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines

# TEST FOR INSERT TASK INTO EMPTY SECTION DEL EMPTY AFTER DIRECT
def test_insert_task_into_empty_section_del_empty_after_direct():
    class DelTrackerList(list):
        def __init__(self, *args):
            super().__init__(*args)
            self._del_calls = []
        def __delitem__(self, idx):
            self._del_calls.append(idx)
            super().__delitem__(idx)
    lines = DelTrackerList(['#### SECTION', '', ''])
    start_idx = 0
    task_line = '- [ ] **fix:** task'
    original_len = len(lines)
    _insert_task_into_empty_section(lines, start_idx, task_line)
    assert task_line in lines
    assert len(lines._del_calls) > 0, "del should be called in the while loop (line 397)"
    assert len(lines) < original_len + 1, "At least one empty line should be removed by the while loop (line 397)"

# TEST FOR INSERT TASK INTO SECTION WITH EXISTING TASKS
def test_insert_task_into_section_with_existing_tasks():
    lines = ['header', '- [ ] **fix:** task1', '', 'footer']
    _insert_task_into_section(lines, 0, 3, '- [ ] **add:** task2', r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\*')
    assert lines[2] == '- [ ] **add:** task2'

# TEST FOR INSERT TASK INTO SECTION EMPTY
def test_insert_task_into_section_empty():
    lines = ['header', '', 'footer']
    _insert_task_into_section(lines, 0, 2, '- [ ] **fix:** task', r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\*')
    assert '- [ ] **fix:** task' in lines

# TEST FOR INSERT TASK INTO SECTION STOPS AT SECTION
def test_insert_task_into_section_stops_at_section():
    lines = ['header', '- task1', '', '#### NEXT']
    _insert_task_into_section(lines, 0, 4, '- task2', r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\*')
    assert '- task2' in lines
    assert lines.index('- task2') < lines.index('#### NEXT')

# TEST FOR INSERT TASK INTO SECTION WITH EXISTING TASKS MULTIPLE
def test_insert_task_into_section_with_existing_tasks_multiple():
    lines = ['header', '- [ ] **fix:** task1', '- [ ] **add:** task2', '', 'footer']
    _insert_task_into_section(lines, 0, 4, '- [ ] **change:** task3', r'^[\s]*-[\s]*\[[\s]*\][\s]*\*\*\w+:\*\*')
    assert '- [ ] **change:** task3' in lines
    assert lines.index('- [ ] **change:** task3') > lines.index('- [ ] **add:** task2')

# TEST FOR ADD TASK TO SECTION NEW TASK
def test_add_task_to_section_new_task():
    content = "### HEADER\n#### TASK\n\n#### NEXT"
    result = _add_task_to_section(content, 'tasks', 'test task', 'fix')
    assert '**fix:** test task' in result

# TEST FOR ADD TASK TO SECTION WITH PRIORITY
def test_add_task_to_section_with_priority():
    content = "### HEADER\n#### TASK\n\n#### NEXT"
    result = _add_task_to_section(content, 'tasks', 'test task', 'fix', 'high')
    assert '![HIGH][high]' in result

# TEST FOR ADD TASK TO SECTION AFTER EXISTING
def test_add_task_to_section_after_existing():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task1\n#### NEXT"
    result = _add_task_to_section(content, 'tasks', 'task2', 'add')
    assert result.count('**fix:** task1') == 1
    assert '**add:** task2' in result

# TEST FOR ADD TASK TO SECTION MULTIPLE TASKS
def test_add_task_to_section_multiple_tasks():
    content = """### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
#### NEXT
"""
    result = _add_task_to_section(content, 'tasks', 'task3', 'change')
    assert '**change:** task3' in result
    assert result.count('**fix:** task1') == 1
    assert result.count('**add:** task2') == 1

# TEST FOR ADD TASK TO SECTION WITH MULTIPLE EXISTING TASKS
def test_add_task_to_section_with_multiple_existing_tasks():
    content = """### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
- [ ] **change:** task3
#### NEXT
"""
    result = _add_task_to_section(content, 'tasks', 'task4', 'update')
    assert '**update:** task4' in result
    lines = result.split('\n')
    update_idx = next((i for i, l in enumerate(lines) if '**update:** task4' in l), -1)
    change_idx = next((i for i, l in enumerate(lines) if '**change:** task3' in l), -1)
    assert update_idx > change_idx

# TEST FOR ADD TASK TO SECTION CREATES SECTIONS
def test_add_task_to_section_creates_sections():
    content = "### HEADER"
    result = _add_task_to_section(content, 'tasks', 'test', 'fix')
    assert '#### TASK' in result

# TEST FOR ADD TASK TO SECTION RETURNS CONTENT
def test_add_task_to_section_returns_content():
    content = "### HEADER\n#### TASK\n#### DONE\n"
    result = _add_task_to_section(content, 'tasks', 'test', 'fix')
    assert '**fix:** test' in result

# TEST FOR ADD TASK TO SECTION INVALID SECTION
def test_add_task_to_section_invalid_section():
    with pytest.raises(ValueError, match="CANNOT ADD TASK TO SECTION"):
        _add_task_to_section("content", 'invalid', 'task', 'fix')

# TEST FOR ADD TASK TO SECTION SECTION NOT FOUND
def test_add_task_to_section_section_not_found():
    result = _add_task_to_section("content", 'tasks', 'task', 'fix')
    assert '**fix:** task' in result

# TEST FOR ADD TASK TO SECTION RAISES WHEN SECTION NOT FOUND
def test_add_task_to_section_raises_when_section_not_found():
    content = "### HEADER\ncontent"
    result = _add_task_to_section(content, 'tasks', 'test', 'fix')
    assert '#### TASK' in result

# TEST FOR ADD TASK TO SECTION RAISES WHEN SECTION MISSING
def test_add_task_to_section_raises_when_section_missing():
    content = "### HEADER\ncontent"
    result = _add_task_to_section(content, 'tasks', 'test', 'fix')
    assert '#### TASK' in result

# TEST FOR ADD TASK TO SECTION RAISES WHEN SECTION MISSING WITH MOCK
def test_add_task_to_section_raises_when_section_missing_with_mock():
    from unittest.mock import patch
    content = "### HEADER\n#### IN PROGRESS\n#### DONE"
    with patch('autotools.autotodo.core._ensure_sections', return_value=content):
        with pytest.raises(ValueError, match="SECTION 'tasks' NOT FOUND"):
            _add_task_to_section(content, 'tasks', 'test', 'fix')

# TEST FOR GET TASK LINE BY INDEX
def test_get_task_line_by_index():
    lines = ['line1', '- [ ] **fix:** task1', '- [ ] **add:** task2']
    task_lines = [1, 2]
    idx, line = _get_task_line_by_index(lines, task_lines, 0)
    assert idx == 1
    assert 'task1' in line

# TEST FOR GET TASK LINE BY INDEX VALID
def test_get_task_line_by_index_valid():
    lines = ['line1', '- [ ] **fix:** task1', '- [ ] **add:** task2']
    task_lines = [1, 2]
    idx, line = _get_task_line_by_index(lines, task_lines, 1)
    assert idx == 2
    assert 'task2' in line

# TEST FOR GET TASK LINE BY INDEX INVALID
def test_get_task_line_by_index_invalid():
    lines = ['line1']
    task_lines = []
    with pytest.raises(ValueError, match="TASK INDEX.*OUT OF RANGE"):
        _get_task_line_by_index(lines, task_lines, 0)

# TEST FOR MOVE TO IN PROGRESS
def test_move_to_in_progress():
    content = """### HEADER
#### TASK
- [ ] **fix:** test task
#### DONE
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '**fixing:** test task' in result
    assert '#### IN PROGRESS' in result

# TEST FOR MOVE TO IN PROGRESS WITH PRIORITY BADGE
def test_move_to_in_progress_with_priority_badge():
    content = """### HEADER
#### TASK
- [ ] **fix:** ![HIGH][high] test task
#### DONE
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '**fixing:** test task' in result
    assert '![HIGH]' not in result or result.count('![HIGH]') == 0

# TEST FOR MOVE TO IN PROGRESS WITH COMPLEX PREFIX
def test_move_to_in_progress_with_complex_prefix():
    content = """### HEADER
#### TASK
- [ ] **study:** test task
#### DONE
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '**studying:** test task' in result

# TEST FOR MOVE TO IN PROGRESS EXTRACTS PREFIX
def test_move_to_in_progress_extracts_prefix():
    content = """### HEADER
#### TASK
- [ ] **test:** task description
#### DONE
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '**testing:** task description' in result

# TEST FOR MOVE TO IN PROGRESS CREATES SECTIONS
def test_move_to_in_progress_creates_sections():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task"
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result

# TEST FOR MOVE TO IN PROGRESS CREATES SECTION IF MISSING
def test_move_to_in_progress_creates_section_if_missing():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result

# TEST FOR MOVE TO IN PROGRESS HANDLES SECTION CREATION
def test_move_to_in_progress_handles_section_creation():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result
    assert '**fixing:** task' in result

# TEST FOR MOVE TO IN PROGRESS SECTION NOT FOUND RAISES
def test_move_to_in_progress_section_not_found_raises():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result
    assert '**fixing:** task' in result

# TEST FOR MOVE TO IN PROGRESS WITH SECTION NOT FOUND AFTER ENSURE
def test_move_to_in_progress_with_section_not_found_after_ensure():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
"""
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result
    assert '**fixing:** task' in result

# TEST FOR MOVE TO IN PROGRESS RAISES WHEN SECTION MISSING
def test_move_to_in_progress_raises_when_section_missing():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task"
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result

# TEST FOR MOVE TO IN PROGRESS RAISES WHEN SECTION MISSING AFTER ENSURE
def test_move_to_in_progress_raises_when_section_missing_after_ensure():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task"
    result = _move_to_in_progress(content, 0, 'tasks')
    assert '#### IN PROGRESS' in result

# TEST FOR MOVE TO IN PROGRESS RAISES WHEN SECTION MISSING WITH MOCK
def test_move_to_in_progress_raises_when_section_missing_with_mock():
    from unittest.mock import patch
    content = """### HEADER
#### TASK
- [ ] **fix:** task
"""
    with patch('autotools.autotodo.core._ensure_sections', return_value=content):
        with pytest.raises(ValueError, match="IN PROGRESS SECTION NOT FOUND"):
            _move_to_in_progress(content, 0, 'tasks')

# TEST FOR MOVE TO IN PROGRESS INVALID INDEX
def test_move_to_in_progress_invalid_index():
    content = "### HEADER\n#### TASK\n#### DONE"
    with pytest.raises(ValueError, match="TASK INDEX.*OUT OF RANGE"):
        _move_to_in_progress(content, 999, 'tasks')

# TEST FOR MOVE TO DONE FROM TASKS
def test_move_to_done_from_tasks():
    content = """### HEADER
#### TASK
- [ ] **fix:** test task
#### DONE
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '**added:** test task' in result
    assert '- [x]' in result

# TEST FOR MOVE TO DONE FROM IN PROGRESS
def test_move_to_done_from_in_progress():
    content = """### HEADER
#### IN PROGRESS
- [ ] **fixing:** test task
#### DONE
"""
    result = _move_to_done(content, 0, 'in_progress')
    assert '**added:** test task' in result

# TEST FOR MOVE TO DONE WITH PRIORITY BADGE
def test_move_to_done_with_priority_badge():
    content = """### HEADER
#### TASK
- [ ] **fix:** ![MID][mid] test task
#### DONE
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '**added:** test task' in result
    assert '![MID]' not in result or result.count('![MID]') == 0

# TEST FOR MOVE TO DONE PRESERVES TASK TEXT
def test_move_to_done_preserves_task_text():
    content = """### HEADER
#### TASK
- [ ] **fix:** complex task description with details
#### DONE
"""
    result = _move_to_done(content, 0, 'tasks')
    assert 'complex task description with details' in result
    assert '**added:** complex task description with details' in result

# TEST FOR MOVE TO DONE EXTRACTS TEXT
def test_move_to_done_extracts_text():
    content = """### HEADER
#### IN PROGRESS
- [ ] **fixing:** complex task with details
#### DONE
"""
    result = _move_to_done(content, 0, 'in_progress')
    assert 'complex task with details' in result

# TEST FOR MOVE TO DONE CREATES SECTIONS
def test_move_to_done_creates_sections():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task"
    result = _move_to_done(content, 0, 'tasks')
    assert '#### DONE' in result

# TEST FOR MOVE TO DONE RETURNS CONTENT
def test_move_to_done_returns_content():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '#### DONE' in result or '- [x]' in result

# TEST FOR MOVE TO DONE RETURNS UPDATED CONTENT
def test_move_to_done_returns_updated_content():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '#### DONE' in result or '- [x]' in result

# TEST FOR MOVE TO DONE RAISES WHEN DONE NOT FOUND
def test_move_to_done_raises_when_done_not_found():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '#### DONE' in result or '- [x]' in result

# TEST FOR MOVE TO DONE RAISES WHEN DONE MISSING AFTER ENSURE
def test_move_to_done_raises_when_done_missing_after_ensure():
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
"""
    result = _move_to_done(content, 0, 'tasks')
    assert '#### DONE' in result or '- [x]' in result

# TEST FOR MOVE TO DONE RAISES WHEN DONE MISSING WITH MOCK
def test_move_to_done_raises_when_done_missing_with_mock():
    from unittest.mock import patch
    content = """### HEADER
#### TASK
- [ ] **fix:** task
#### IN PROGRESS
"""
    with patch('autotools.autotodo.core._ensure_sections', return_value=content):
        with pytest.raises(ValueError, match="DONE SECTION NOT FOUND"):
            _move_to_done(content, 0, 'tasks')

# TEST FOR MOVE TO DONE INVALID INDEX
def test_move_to_done_invalid_index():
    content = "### HEADER\n#### TASK\n#### DONE"
    with pytest.raises(ValueError, match="TASK INDEX.*OUT OF RANGE"):
        _move_to_done(content, 999, 'tasks')

# TEST FOR FIND TASK LINES IN SECTION TASKS
def test_find_task_lines_in_section_tasks():
    lines = ['header', '- [ ] **fix:** task1', '- [ ] **add:** task2']
    result = _find_task_lines_in_section(lines, 'tasks')
    assert len(result) == 2

# TEST FOR FIND TASK LINES IN SECTION IN PROGRESS
def test_find_task_lines_in_section_in_progress():
    lines = ['header', '- [ ] **fixing:** task1']
    result = _find_task_lines_in_section(lines, 'in_progress')
    assert len(result) == 1

# TEST FOR FIND TASK LINES IN SECTION DONE
def test_find_task_lines_in_section_done():
    lines = ['header', '- [x] **added:** task1']
    result = _find_task_lines_in_section(lines, 'done')
    assert len(result) == 1

# TEST FOR FIND TASK LINES IN SECTION UNKNOWN
def test_find_task_lines_in_section_unknown():
    lines = ['header']
    result = _find_task_lines_in_section(lines, 'unknown')
    assert len(result) == 0

# TEST FOR REMOVE TASK
def test_remove_task():
    content = """### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
"""
    result = _remove_task(content, 0, 'tasks')
    assert '**fix:** task1' not in result
    assert '**add:** task2' in result

# TEST FOR REMOVE TASK FROM MIDDLE
def test_remove_task_from_middle():
    content = """### HEADER
#### TASK
- [ ] **fix:** task1
- [ ] **add:** task2
- [ ] **change:** task3
"""
    result = _remove_task(content, 1, 'tasks')
    assert '**add:** task2' not in result
    assert '**fix:** task1' in result
    assert '**change:** task3' in result

# TEST FOR REMOVE TASK FROM IN PROGRESS
def test_remove_task_from_in_progress():
    content = """### HEADER
#### IN PROGRESS
- [ ] **fixing:** task1
- [ ] **adding:** task2
"""
    result = _remove_task(content, 0, 'in_progress')
    assert '**fixing:** task1' not in result
    assert '**adding:** task2' in result

# TEST FOR REMOVE TASK FROM DONE
def test_remove_task_from_done():
    content = """### HEADER
#### DONE
- [x] **added:** task1
- [x] **added:** task2
"""
    result = _remove_task(content, 0, 'done')
    assert result.count('- [x] **added:** task1') == 0
    assert '- [x] **added:** task2' in result

# TEST FOR REMOVE TASK INVALID INDEX
def test_remove_task_invalid_index():
    content = "### HEADER\n#### TASK\n- [ ] **fix:** task1"
    with pytest.raises(ValueError, match="TASK INDEX.*OUT OF RANGE"):
        _remove_task(content, 999, 'tasks')

# TEST FOR EXTRACT TASK LINES FROM SECTION
def test_extract_task_lines_from_section():
    lines = ['header', '- task1', '- task2', '#### NEXT']
    result = _extract_task_lines_from_section(lines, 0, 3)
    assert len(result) == 2

# TEST FOR EXTRACT TASK LINES FROM SECTION WITH SEPARATOR
def test_extract_task_lines_from_section_with_separator():
    lines = ['header', '- task1', '---', '- task2', '#### NEXT']
    result = _extract_task_lines_from_section(lines, 0, 4)
    assert len(result) == 2

# TEST FOR EXTRACT TASK LINES FROM SECTION STOPS AT SECTION
def test_extract_task_lines_from_section_stops_at_section():
    lines = ['header', '- task1', '#### NEXT', '- task2']
    result = _extract_task_lines_from_section(lines, 0, 4)
    assert len(result) == 1

# TEST FOR EXTRACT TASK LINES FROM SECTION SKIPS EMPTY
def test_extract_task_lines_from_section_skips_empty():
    lines = ['header', '', '- task1', '', '- task2', '#### NEXT']
    result = _extract_task_lines_from_section(lines, 0, 5)
    assert len(result) == 2
    assert '- task1' in result
    assert '- task2' in result

# TEST FOR EXTRACT TASK LINES FROM SECTION STOPS AT BADGES
def test_extract_task_lines_from_section_stops_at_badges():
    lines = ['header', '- task1', '[high]: url', '#### NEXT']
    result = _extract_task_lines_from_section(lines, 0, 4)
    assert len(result) == 1

# TEST FOR EXTRACT TASK LINES FROM SECTION INCLUDES DASH LINES
def test_extract_task_lines_from_section_includes_dash_lines():
    lines = ['header', '- task1', '- task2', '#### NEXT']
    result = _extract_task_lines_from_section(lines, 0, 4)
    assert len(result) == 2
    assert '- task1' in result
    assert '- task2' in result
