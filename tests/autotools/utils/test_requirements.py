import os
import pytest
import tempfile
from unittest.mock import patch, mock_open
from autotools.utils.requirements import read_requirements

# TEST FOR READING REQUIREMENTS FROM EXISTING FILE
def test_read_requirements_existing_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        tmp.write("package1>=1.0.0\n")
        tmp.write("package2>=2.0.0\n")
        tmp.write("package3>=3.0.0\n")
        tmp_path = tmp.name
    
    try:
        with patch('autotools.utils.requirements.os.path.join') as mock_join, \
             patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
             patch('builtins.open', mock_open(read_data="package1>=1.0.0\npackage2>=2.0.0\npackage3>=3.0.0\n")):
            mock_join.return_value = tmp_path
            mock_abspath.return_value = tmp_path
            result = read_requirements("test-requirements.txt")
            assert len(result) == 3
            assert "package1>=1.0.0" in result
            assert "package2>=2.0.0" in result
            assert "package3>=3.0.0" in result
    finally:
        if os.path.exists(tmp_path): os.unlink(tmp_path)

# TEST FOR READING REQUIREMENTS WITH COMMENTS
def test_read_requirements_with_comments():
    content = "package1>=1.0.0\n# THIS IS A COMMENT\npackage2>=2.0.0\n  # ANOTHER COMMENT\npackage3>=3.0.0\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert len(result) == 3
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result
        assert "package3>=3.0.0" in result
        assert "# THIS IS A COMMENT" not in result

# TEST FOR READING REQUIREMENTS WITH EMPTY LINES
def test_read_requirements_with_empty_lines():
    content = "package1>=1.0.0\n\npackage2>=2.0.0\n  \npackage3>=3.0.0\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert len(result) == 3
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result
        assert "package3>=3.0.0" in result

# TEST FOR READING REQUIREMENTS WITH -r FLAG
def test_read_requirements_with_r_flag():
    content = "package1>=1.0.0\n-r other-requirements.txt\npackage2>=2.0.0\n--requirement dev-requirements.txt\npackage3>=3.0.0\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert len(result) == 3
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result
        assert "package3>=3.0.0" in result
        assert "-r other-requirements.txt" not in result
        assert "--requirement dev-requirements.txt" not in result

# TEST FOR READING REQUIREMENTS WITH MIXED CONTENT
def test_read_requirements_with_mixed_content():
    content = "package1>=1.0.0\n# COMMENT\n\n-r other.txt\npackage2>=2.0.0\n  # INLINE COMMENT\npackage3>=3.0.0\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert len(result) == 3
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result
        assert "package3>=3.0.0" in result

# TEST FOR READING REQUIREMENTS FROM MISSING FILE
def test_read_requirements_missing_file():
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', side_effect=FileNotFoundError("File not found")):
        mock_join.return_value = "/fake/path/nonexistent.txt"
        mock_abspath.return_value = "/fake/path/nonexistent.txt"
        result = read_requirements("nonexistent.txt")
        assert result == []
        assert isinstance(result, list)

# TEST FOR READING REQUIREMENTS WITH DEFAULT FILENAME
def test_read_requirements_default_filename():
    content = "package1>=1.0.0\npackage2>=2.0.0\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements()
        assert len(result) == 2
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result

# TEST FOR READING REQUIREMENTS WITH WHITESPACE
def test_read_requirements_with_whitespace():
    content = "  package1>=1.0.0  \n  package2>=2.0.0  \n  package3>=3.0.0  \n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert len(result) == 3
        assert "package1>=1.0.0" in result
        assert "package2>=2.0.0" in result
        assert "package3>=3.0.0" in result

# TEST FOR READING EMPTY REQUIREMENTS FILE
def test_read_requirements_empty_file():
    content = ""
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert result == []
        assert isinstance(result, list)

# TEST FOR READING REQUIREMENTS WITH ONLY COMMENTS
def test_read_requirements_only_comments():
    content = "# COMMENT 1\n# COMMENT 2\n  # COMMENT 3\n"
    with patch('autotools.utils.requirements.os.path.join') as mock_join, \
         patch('autotools.utils.requirements.os.path.abspath') as mock_abspath, \
         patch('builtins.open', mock_open(read_data=content)):
        mock_join.return_value = "/fake/path/requirements.txt"
        mock_abspath.return_value = "/fake/path/requirements.txt"
        result = read_requirements("requirements.txt")
        assert result == []
        assert isinstance(result, list)
