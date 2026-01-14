import pytest
import tempfile
import os
import sys
from unittest.mock import MagicMock

# FIXTURE FOR CREATING A TEMPORARY DIRECTORY WITH FILES
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

# FIXTURE FOR CREATING TEST FILES
@pytest.fixture
def create_test_file(temp_dir):
    def _create_file(filename, content=b"fake data", mode="wb"):
        filepath = os.path.join(temp_dir, filename)
        if 'b' in mode:
            with open(filepath, mode) as f:
                if isinstance(content, bytes): f.write(content)
                else: f.write(content.encode('utf-8'))
        else:
            with open(filepath, mode, encoding='utf-8') as f:
                if isinstance(content, bytes): f.write(content.decode('utf-8'))
                else: f.write(content)
        return filepath
    return _create_file

# FIXTURE FOR MOCK PYDUB
@pytest.fixture
def mock_pydub(monkeypatch):
    fake_pydub = MagicMock()
    fake_audio_segment = MagicMock()
    fake_pydub.AudioSegment = fake_audio_segment
    sys.modules['pydub'] = fake_pydub
    return fake_audio_segment

# FIXTURE FOR MOCK MOVIEPY
@pytest.fixture
def mock_moviepy(monkeypatch):
    fake_moviepy = MagicMock()
    fake_editor = MagicMock()
    fake_moviepy.editor = fake_editor
    sys.modules['moviepy'] = fake_moviepy
    sys.modules['moviepy.editor'] = fake_editor
    return fake_editor

# HELPER FOR MOCKING IMPORT ERRORS
def mock_import_error(monkeypatch, module_name, error_msg=None):
    original_import = __import__
    
    def mock_import(name, *args, **kwargs):
        if name == module_name or name.startswith(f'{module_name}.'):
            raise ImportError(error_msg or f"No module named '{module_name}'")
        return original_import(name, *args, **kwargs)
    
    monkeypatch.setattr('builtins.__import__', mock_import)

# HELPER TO CLEAN MODULES FROM SYSMODULES
def cleanup_sys_modules(*module_names):
    for module_name in module_names:
        if module_name in sys.modules:
            del sys.modules[module_name]
