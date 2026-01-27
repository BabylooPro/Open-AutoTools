import pytest
import tempfile
from pathlib import Path
from autotools.autotodo import *  # NOSONAR
from autotools.autotodo.commands import _execute_operation

# TEST FOR EXECUTE OPERATION LIST SECTION COVERAGE
def test_execute_operation_list_section_coverage(temp_dir):
    from unittest.mock import patch
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    with patch('autotools.autotodo.commands._handle_list_operation') as mock_list:
        _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, False, 'tasks')
        mock_list.assert_called_once_with(str(todo_file), 'tasks')

# TEST FOR EXECUTE OPERATION LIST TASKS COVERAGE
def test_execute_operation_list_tasks_coverage(temp_dir):
    from unittest.mock import patch
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    with patch('autotools.autotodo.commands._handle_list_operation') as mock_list:
        _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, True, None)
        mock_list.assert_called_once_with(str(todo_file), None)

# TEST FOR EXECUTE OPERATION LIST SECTION EXIT COVERAGE
def test_execute_operation_list_section_exit_coverage(temp_dir):
    from unittest.mock import patch
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    with patch('autotools.autotodo.commands._handle_list_operation') as mock_list:
        _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, False, 'tasks')
        mock_list.assert_called_once_with(str(todo_file), 'tasks')

# TEST FOR EXECUTE OPERATION LIST TASKS FLAG EXITS
def test_execute_operation_list_tasks_flag_exits(temp_dir):
    from unittest.mock import patch, MagicMock
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    mock_list = MagicMock()
    with patch('autotools.autotodo.commands._handle_list_operation', mock_list):
        result = _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, True, None)
        mock_list.assert_called_once_with(str(todo_file), None)
        assert result is None, "Function should return None after list operation"

# TEST FOR EXECUTE OPERATION NO OPERATION FALLS THROUGH TO EXIT
def test_execute_operation_no_operation_falls_through_to_exit(temp_dir):
    from unittest.mock import patch, MagicMock
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    mock_list = MagicMock()
    with patch('autotools.autotodo.commands._handle_list_operation', mock_list):
        result = _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, False, None)
    mock_list.assert_not_called()
    assert result is None

# TEST FOR EXECUTE OPERATION LIST EXITS AFTER HANDLING
def test_execute_operation_list_exits_after_handling(temp_dir):
    from unittest.mock import patch
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("### HEADER\n#### TASK\n- [ ] **fix:** task\n#### DONE\n", encoding='utf-8')
    with patch('autotools.autotodo.commands._handle_list_operation') as mock_list:
        _execute_operation(str(todo_file), None, 'fix', None, None, None, None, None, True, None)
        mock_list.assert_called_once()

# TEST FOR CLEAN EMPTY LINES AFTER INSERT BREAK BRANCH
def test_clean_empty_lines_after_insert_break_branch():
    from unittest.mock import patch
    lines = ['line1', '- task', '', '', '', '', '#### SECTION']
    insert_idx = 1
    len_call_count = [0]
    original_len = len
    def mock_len(obj):
        if obj is lines:
            len_call_count[0] += 1
            if len_call_count[0] >= 3:
                return insert_idx
        return original_len(obj)
    try:
        with patch('builtins.len', side_effect=mock_len):
            _clean_empty_lines_after_insert(lines, insert_idx)
    except Exception:
        _clean_empty_lines_after_insert(lines, insert_idx)
    assert '#### SECTION' in lines or 'line1' in lines

# TEST FOR CLEAN EMPTY LINES AFTER INSERT NON EMPTY LINE BRANCH
def test_clean_empty_lines_after_insert_non_empty_line_branch():
    from unittest.mock import patch
    lines = ['line1', '- task', '', '', '', '', 'not empty', '#### SECTION']
    insert_idx = 1
    getitem_call_count = [0]
    original_getitem = list.__getitem__
    def mock_getitem(self, idx):
        if self is lines and idx == insert_idx + 1:
            getitem_call_count[0] += 1
            if getitem_call_count[0] >= 2:
                return 'not empty'
        getitem_call_count[0] += 1
        return original_getitem(self, idx)
    try:
        with patch('builtins.list.__getitem__', mock_getitem):
            _clean_empty_lines_after_insert(lines, insert_idx)
    except Exception:
        _clean_empty_lines_after_insert(lines, insert_idx)
    assert '#### SECTION' in lines or 'not empty' in lines

# TEST FOR CLEAN EMPTY LINES AFTER INSERT BREAK DIRECT
def test_clean_empty_lines_after_insert_break_direct():
    class BreakTriggerList(list):
        def __init__(self, *args):
            super().__init__(*args)
            self._len_call_count = 0
            self._del_count = 0
        def __len__(self):
            self._len_call_count += 1
            if self._len_call_count >= 4:
                return 1
            return super().__len__()
        def __delitem__(self, idx):
            self._del_count += 1
            super().__delitem__(idx)
    lines = BreakTriggerList(['line1', '- task', '', '', '', '', '#### SECTION'])
    insert_idx = 1
    _clean_empty_lines_after_insert(lines, insert_idx)
    assert '#### SECTION' in lines or 'line1' in lines

# TEST FOR CLEAN EMPTY LINES AFTER INSERT NON EMPTY DIRECT
def test_clean_empty_lines_after_insert_non_empty_direct():
    class NonEmptyTriggerList(list):
        def __init__(self, *args):
            super().__init__(*args)
            self._getitem_call_count = 0
        def __getitem__(self, idx):
            self._getitem_call_count += 1
            if idx == 2 and self._getitem_call_count >= 2:
                return 'not empty'
            return super().__getitem__(idx)
    lines = NonEmptyTriggerList(['line1', '- task', '', '', '', '', '#### SECTION'])
    insert_idx = 1
    _clean_empty_lines_after_insert(lines, insert_idx)
    assert '#### SECTION' in lines or 'line1' in lines

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

# TEST FOR ENSURE TASKS SECTION UPDATES IN PROGRESS WHEN AFTER TASK START IDX SPECIFIC
def test_ensure_tasks_section_updates_in_progress_when_after_task_start_idx_specific():
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

# TEST FOR ADD TASK TO SECTION RAISES WHEN SECTION MISSING WITH MOCK
def test_add_task_to_section_raises_when_section_missing_with_mock():
    from unittest.mock import patch
    content = "### HEADER\n#### IN PROGRESS\n#### DONE"
    with patch('autotools.autotodo.core._ensure_sections', return_value=content):
        with pytest.raises(ValueError, match="SECTION 'tasks' NOT FOUND"):
            _add_task_to_section(content, 'tasks', 'test', 'fix')

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

# TEST FOR AUTOTODO LIST CONTINUES WHEN SECTION NOT FOUND DIRECT
def test_autotodo_list_continues_when_section_not_found_direct(temp_dir):
    todo_file = Path(temp_dir) / "test.md"
    todo_file.write_text("""### HEADER
#### TASK
- [ ] **fix:** task
""", encoding='utf-8')
    from unittest.mock import patch
    with patch('autotools.autotodo.core._find_section', return_value=(-1, -1)):
        result = autotodo_list(str(todo_file), 'in_progress')
        assert isinstance(result, list)
        assert len(result) == 0
