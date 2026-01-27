import pytest
from autotools.autotodo import *  # NOSONAR

# TEST FOR CLEAN EMPTY LINES AFTER INSERT
def test_clean_empty_lines_after_insert():
    lines = ['line1', '- task', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1
    assert '#### SECTION' in lines
    assert lines.index('#### SECTION') > lines.index('- task')

# TEST FOR CLEAN EMPTY LINES AFTER INSERT NO SECTION
def test_clean_empty_lines_after_insert_no_section():
    lines = ['line1', '- task', '', '']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines == ['line1', '- task']

# TEST FOR CLEAN EMPTY LINES AFTER INSERT KEEPS ONE BEFORE SECTION
def test_clean_empty_lines_after_insert_keeps_one_before_section():
    lines = ['line1', '- task', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines == ['line1', '- task', '', '#### SECTION']

# TEST FOR CLEAN EMPTY LINES AFTER INSERT MULTIPLE EMPTY
def test_clean_empty_lines_after_insert_multiple_empty():
    lines = ['line1', '- task', '', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1
    assert '#### SECTION' in lines

# TEST FOR CLEAN EMPTY LINES AFTER INSERT NO EMPTY LINES
def test_clean_empty_lines_after_insert_no_empty_lines():
    lines = ['line1', '- task', '#### SECTION']
    original = lines.copy()
    _clean_empty_lines_after_insert(lines, 1)
    assert lines == original

# TEST FOR CLEAN EMPTY LINES AFTER INSERT STOPS AT SECTION
def test_clean_empty_lines_after_insert_stops_at_section():
    lines = ['line1', '- task', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines[2] == '' or lines[2] == '#### SECTION'

# TEST FOR CLEAN EMPTY LINES AFTER INSERT MULTIPLE BEFORE SECTION
def test_clean_empty_lines_after_insert_multiple_before_section():
    lines = ['line1', '- task', '', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1
    assert '#### SECTION' in lines

# TEST FOR CLEAN EMPTY LINES AFTER INSERT REMOVES MULTIPLE
def test_clean_empty_lines_after_insert_removes_multiple():
    lines = ['line1', '- task', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1

# TEST FOR CLEAN EMPTY LINES AFTER INSERT EARLY RETURN
def test_clean_empty_lines_after_insert_early_return():
    lines = ['line1', '- task']
    _clean_empty_lines_after_insert(lines, 1)
    assert len(lines) == 2

# TEST FOR CLEAN EMPTY LINES AFTER INSERT REMOVES IN LOOP
def test_clean_empty_lines_after_insert_removes_in_loop():
    lines = ['line1', '- task', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1

# TEST FOR CLEAN EMPTY LINES AFTER INSERT CHECKS IN LOOP
def test_clean_empty_lines_after_insert_checks_in_loop():
    lines = ['line1', '- task', '', '', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert lines.count('') == 1

# TEST FOR CLEAN EMPTY LINES AFTER INSERT BOUNDS CHECK FALSE
def test_clean_empty_lines_after_insert_bounds_check_false():
    lines = ['line1', '- task', '', '#### SECTION']
    _clean_empty_lines_after_insert(lines, 1)
    assert '- task' in lines

# TEST FOR EXTRACT TASK PREFIX AND TEXT WITH CONTENT
def test_extract_task_prefix_and_text_with_content():
    result = _extract_task_prefix_and_text("- [ ] **fix:** test description")
    assert result == ('fix', 'test description')

# TEST FOR EXTRACT TASK PREFIX AND TEXT WITH PRIORITY
def test_extract_task_prefix_and_text_with_priority():
    result = _extract_task_prefix_and_text("- [ ] **fix:** ![HIGH][high] test description")
    assert result == ('fix', 'test description')

# TEST FOR EXTRACT TASK PREFIX AND TEXT NO CONTENT
def test_extract_task_prefix_and_text_no_content():
    result = _extract_task_prefix_and_text("- [ ] **fix:**")
    assert result == ('fix', '')

# TEST FOR EXTRACT TASK PREFIX AND TEXT FALLBACK
def test_extract_task_prefix_and_text_fallback():
    result = _extract_task_prefix_and_text("some other line")
    assert result == ('ing', 'some other line')

# TEST FOR EXTRACT TASK PREFIX AND TEXT WITH MID PRIORITY
def test_extract_task_prefix_and_text_with_mid_priority():
    result = _extract_task_prefix_and_text("- [ ] **fix:** ![MID][mid] test description")
    assert result == ('fix', 'test description')

# TEST FOR EXTRACT TASK PREFIX AND TEXT WITH LOW PRIORITY
def test_extract_task_prefix_and_text_with_low_priority():
    result = _extract_task_prefix_and_text("- [ ] **fix:** ![LOW][low] test description")
    assert result == ('fix', 'test description')

@pytest.mark.parametrize("prefix,expected", [
    ('fix', 'fixing'),
    ('add', 'adding'),
    ('change', 'changing'),
    ('update', 'updating'),
    ('fixing', 'fixing'),
    ('adding', 'adding'),
    ('study', 'studying'),
    ('try', 'trying'),
])
# TEST FOR PREFIX TO ING
def test_prefix_to_ing(prefix, expected):
    assert _prefix_to_ing(prefix) == expected

# TEST FOR PREFIX TO ING ENDING E
def test_prefix_to_ing_ending_e():
    assert _prefix_to_ing('change') == 'changing'
    assert _prefix_to_ing('update') == 'updating'

# TEST FOR PREFIX TO ING ENDING Y
def test_prefix_to_ing_ending_y():
    assert _prefix_to_ing('study') == 'studying'
    assert _prefix_to_ing('try') == 'trying'

# TEST FOR PREFIX TO ING ALREADY ING
def test_prefix_to_ing_already_ing():
    assert _prefix_to_ing('fixing') == 'fixing'
    assert _prefix_to_ing('adding') == 'adding'

# TEST FOR EXTRACT TEXT FROM TASKS LINE WITH CONTENT
def test_extract_text_from_tasks_line_with_content():
    result = _extract_text_from_tasks_line("- [ ] **fix:** test description")
    assert result == "test description"

# TEST FOR EXTRACT TEXT FROM TASKS LINE WITH PRIORITY
def test_extract_text_from_tasks_line_with_priority():
    result = _extract_text_from_tasks_line("- [ ] **fix:** ![HIGH][high] test description")
    assert result == "test description"

# TEST FOR EXTRACT TEXT FROM TASKS LINE NO CONTENT
def test_extract_text_from_tasks_line_no_content():
    result = _extract_text_from_tasks_line("- [ ] **fix:**")
    assert result == ""

# TEST FOR EXTRACT TEXT FROM TASKS LINE NO MATCH
def test_extract_text_from_tasks_line_no_match():
    result = _extract_text_from_tasks_line("invalid format")
    assert result == "invalid format"

# TEST FOR EXTRACT TEXT FROM IN PROGRESS LINE WITH CONTENT
def test_extract_text_from_in_progress_line_with_content():
    result = _extract_text_from_in_progress_line("- [ ] **fixing:** test description")
    assert result == "test description"

# TEST FOR EXTRACT TEXT FROM IN PROGRESS LINE NO CONTENT
def test_extract_text_from_in_progress_line_no_content():
    result = _extract_text_from_in_progress_line("- [ ] **fixing:**")
    assert result == ""

# TEST FOR EXTRACT TEXT FROM IN PROGRESS LINE FALLBACK
def test_extract_text_from_in_progress_line_fallback():
    result = _extract_text_from_in_progress_line("- some other format")
    assert result == "some other format"

# TEST FOR EXTRACT TEXT FROM IN PROGRESS LINE OLD FORMAT
def test_extract_text_from_in_progress_line_old_format():
    result = _extract_text_from_in_progress_line("- old format line")
    assert result == "old format line"

# TEST FOR EXTRACT TASK TEXT FROM LINE TASKS
def test_extract_task_text_from_line_tasks():
    result = _extract_task_text_from_line("- [ ] **fix:** test", "tasks")
    assert result == "test"

# TEST FOR EXTRACT TASK TEXT FROM LINE IN PROGRESS
def test_extract_task_text_from_line_in_progress():
    result = _extract_task_text_from_line("- [ ] **fixing:** test", "in_progress")
    assert result == "test"

# TEST FOR EXTRACT TASK TEXT FROM LINE OTHER
def test_extract_task_text_from_line_other():
    result = _extract_task_text_from_line("some line", "other")
    assert result == "some line"

# TEST FOR CREATE TASK LINE WITH PRIORITY
def test_create_task_line_with_priority():
    result = _create_task_line('fix', 'test', 'high')
    assert '![HIGH][high]' in result
    assert 'test' in result

# TEST FOR CREATE TASK LINE WITHOUT PRIORITY
def test_create_task_line_without_priority():
    result = _create_task_line('add', 'test', None)
    assert '![HIGH]' not in result
    assert 'test' in result

# TEST FOR CREATE TASK LINE RETURNS WITHOUT PRIORITY
def test_create_task_line_returns_without_priority():
    result = _create_task_line('fix', 'test', None)
    assert '**fix:** test' in result
    assert '![HIGH]' not in result

# TEST FOR CREATE TASK LINE WITH PRIORITY RETURNS FORMATTED
def test_create_task_line_with_priority_returns_formatted():
    result = _create_task_line('fix', 'test', 'high')
    assert '**fix:**' in result
    assert '![HIGH]' in result
