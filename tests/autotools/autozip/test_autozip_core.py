import pytest
import os
import zipfile
import tarfile
import tempfile
import shutil
from pathlib import Path
from autotools.autozip.core import (
    autozip_compress,
    _compress_zip,
    _compress_tar_gz,
    _compress_tar_bz2,
    _compress_tar_xz,
    _compress_tar,
    _get_format_from_extension
)

# FIXTURES

@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def test_file(temp_dir):
    file_path = Path(temp_dir) / "test.txt"
    file_path.write_text("TEST CONTENT")
    return str(file_path)

@pytest.fixture
def test_dir(temp_dir):
    dir_path = Path(temp_dir) / "test_dir"
    dir_path.mkdir()
    (dir_path / "file1.txt").write_text("FILE 1 CONTENT")
    (dir_path / "file2.txt").write_text("FILE 2 CONTENT")
    subdir = dir_path / "subdir"
    subdir.mkdir()
    (subdir / "file3.txt").write_text("FILE 3 CONTENT")
    return str(dir_path)

# TESTS FOR _get_format_from_extension

# TEST FOR ZIP EXTENSION
def test_get_format_from_extension_zip():
    assert _get_format_from_extension("archive.zip") == "zip"
    assert _get_format_from_extension("ARCHIVE.ZIP") == "zip"

# TEST FOR TAR.GZ EXTENSIONS
@pytest.mark.parametrize("ext", [".tar.gz", ".tgz"])
def test_get_format_from_extension_tar_gz(ext):
    assert _get_format_from_extension(f"archive{ext}") == "tar.gz"
    assert _get_format_from_extension(f"ARCHIVE{ext.upper()}") == "tar.gz"

# TEST FOR TAR.BZ2 EXTENSIONS
@pytest.mark.parametrize("ext", [".tar.bz2", ".tbz2"])
def test_get_format_from_extension_tar_bz2(ext):
    assert _get_format_from_extension(f"archive{ext}") == "tar.bz2"
    assert _get_format_from_extension(f"ARCHIVE{ext.upper()}") == "tar.bz2"

# TEST FOR TAR.XZ EXTENSIONS
@pytest.mark.parametrize("ext", [".tar.xz", ".txz"])
def test_get_format_from_extension_tar_xz(ext):
    assert _get_format_from_extension(f"archive{ext}") == "tar.xz"
    assert _get_format_from_extension(f"ARCHIVE{ext.upper()}") == "tar.xz"

# TEST FOR TAR EXTENSION
def test_get_format_from_extension_tar():
    assert _get_format_from_extension("archive.tar") == "tar"
    assert _get_format_from_extension("ARCHIVE.TAR") == "tar"

# TEST FOR INVALID EXTENSION
def test_get_format_from_extension_invalid():
    with pytest.raises(ValueError, match="UNSUPPORTED ARCHIVE FORMAT"): _get_format_from_extension("archive.unknown")

# TESTS FOR _compress_zip

# TEST FOR ZIP WITH SINGLE FILE
def test_compress_zip_single_file(temp_dir, test_file):
    output = Path(temp_dir) / "archive.zip"
    result = _compress_zip([test_file], str(output), compression_level=6)
    
    assert result == str(output)
    assert output.exists()

    with zipfile.ZipFile(output, 'r') as zipf:
        assert "test.txt" in zipf.namelist()
        assert zipf.read("test.txt") == b"TEST CONTENT"

# TEST FOR ZIP WITH DIRECTORY
def test_compress_zip_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.zip"
    result = _compress_zip([test_dir], str(output), compression_level=6)
    
    assert result == str(output)
    assert output.exists()
    
    with zipfile.ZipFile(output, 'r') as zipf:
        names = zipf.namelist()
        assert any("file1.txt" in name for name in names)
        assert any("file2.txt" in name for name in names)
        assert any("file3.txt" in name for name in names)

# TEST FOR ZIP WITH MULTIPLE FILES
def test_compress_zip_multiple_files(temp_dir, test_file):
    file2 = Path(temp_dir) / "test2.txt"
    file2.write_text("TEST 2 CONTENT")
    
    output = Path(temp_dir) / "archive.zip"
    result = _compress_zip([test_file, str(file2)], str(output), compression_level=6)
    
    assert result == str(output)
    with zipfile.ZipFile(output, 'r') as zipf:
        assert "test.txt" in zipf.namelist()
        assert "test2.txt" in zipf.namelist()

# TEST FOR ZIP WITH COMPRESSION LEVELS
@pytest.mark.parametrize("level", [0, 1, 6, 9])
def test_compress_zip_compression_levels(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.zip"
    result = _compress_zip([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR ZIP WITH OUT OF RANGE COMPRESSION LEVELS
@pytest.mark.parametrize("level", [-1, 10, 15])
def test_compress_zip_compression_level_clamping(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.zip"
    result = _compress_zip([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR ZIP WITH NONEXISTENT FILE
def test_compress_zip_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.zip"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        _compress_zip([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TESTS FOR _compress_tar_gz

# TEST FOR TAR.GZ WITH SINGLE FILE
def test_compress_tar_gz_single_file(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.gz"
    result = _compress_tar_gz([test_file], str(output), compression_level=6)
    
    assert result == str(output)
    assert output.exists()

    with tarfile.open(output, 'r:gz') as tar:
        names = tar.getnames()
        assert "test.txt" in names

# TEST FOR TAR.GZ WITH DIRECTORY
def test_compress_tar_gz_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.tar.gz"
    result = _compress_tar_gz([test_dir], str(output), compression_level=6)
    assert result == str(output)
    assert output.exists()
    with tarfile.open(output, 'r:gz') as tar:
        names = tar.getnames()
        assert any("file1.txt" in name for name in names)

# TEST FOR TAR.GZ WITH COMPRESSION LEVELS
@pytest.mark.parametrize("level", [1, 6, 9])
def test_compress_tar_gz_compression_levels(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.gz"
    result = _compress_tar_gz([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ WITH OUT OF RANGE COMPRESSION LEVELS
@pytest.mark.parametrize("level", [0, 10, 15])
def test_compress_tar_gz_compression_level_clamping(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.gz"
    result = _compress_tar_gz([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ WITH NONEXISTENT FILE
def test_compress_tar_gz_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.tar.gz"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        _compress_tar_gz([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TESTS FOR _compress_tar_bz2

# TEST FOR TAR.BZ2 WITH SINGLE FILE
def test_compress_tar_bz2_single_file(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.bz2"
    result = _compress_tar_bz2([test_file], str(output), compression_level=6)
    assert result == str(output)
    assert output.exists()
    with tarfile.open(output, 'r:bz2') as tar: assert "test.txt" in tar.getnames()

# TEST FOR TAR.BZ2 WITH DIRECTORY
def test_compress_tar_bz2_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.tar.bz2"
    result = _compress_tar_bz2([test_dir], str(output), compression_level=6)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 WITH COMPRESSION LEVELS
@pytest.mark.parametrize("level", [1, 6, 9])
def test_compress_tar_bz2_compression_levels(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.bz2"
    result = _compress_tar_bz2([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 WITH OUT OF RANGE COMPRESSION LEVELS
@pytest.mark.parametrize("level", [0, 10, 15])
def test_compress_tar_bz2_compression_level_clamping(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.bz2"
    result = _compress_tar_bz2([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 WITH NONEXISTENT FILE
def test_compress_tar_bz2_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.tar.bz2"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"): 
        _compress_tar_bz2([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TESTS FOR _compress_tar_xz

# TEST FOR TAR.XZ WITH SINGLE FILE
def test_compress_tar_xz_single_file(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.xz"
    result = _compress_tar_xz([test_file], str(output), compression_level=6)
    assert result == str(output)
    assert output.exists()
    with tarfile.open(output, 'r:xz') as tar: assert "test.txt" in tar.getnames()

# TEST FOR TAR.XZ WITH DIRECTORY
def test_compress_tar_xz_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.tar.xz"
    result = _compress_tar_xz([test_dir], str(output), compression_level=6)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ WITH COMPRESSION LEVELS
@pytest.mark.parametrize("level", [0, 1, 6, 9])
def test_compress_tar_xz_compression_levels(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.xz"
    result = _compress_tar_xz([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ WITH OUT OF RANGE COMPRESSION LEVELS
@pytest.mark.parametrize("level", [-1, 10, 15])
def test_compress_tar_xz_compression_level_clamping(temp_dir, test_file, level):
    output = Path(temp_dir) / "archive.tar.xz"
    result = _compress_tar_xz([test_file], str(output), compression_level=level)
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ WITH NONEXISTENT FILE
def test_compress_tar_xz_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.tar.xz"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        _compress_tar_xz([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TESTS FOR _compress_tar

# TEST FOR TAR WITH NONEXISTENT FILE
def test_compress_tar_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.tar"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        _compress_tar([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TESTS FOR autozip_compress

# TEST FOR ZIP FORMAT
def test_autozip_compress_zip(temp_dir, test_file):
    output = Path(temp_dir) / "archive.zip"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR ZIP FORMAT WITH EXPLICIT FORMAT
def test_autozip_compress_zip_explicit_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="zip")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ FORMAT
def test_autozip_compress_tar_gz(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.gz"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ FORMAT WITH TGZ EXTENSION
def test_autozip_compress_tgz(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tgz"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ FORMAT WITH EXPLICIT FORMAT
def test_autozip_compress_tar_gz_explicit_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tar.gz")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.GZ FORMAT WITH TGZ ALIAS
def test_autozip_compress_tgz_alias(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tgz")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 FORMAT
def test_autozip_compress_tar_bz2(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.bz2"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 FORMAT WITH TBZ2 EXTENSION
def test_autozip_compress_tbz2(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tbz2"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 FORMAT WITH EXPLICIT FORMAT
def test_autozip_compress_tar_bz2_explicit_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tar.bz2")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.BZ2 FORMAT WITH TBZ2 ALIAS
def test_autozip_compress_tbz2_alias(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tbz2")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ FORMAT
def test_autozip_compress_tar_xz(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar.xz"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ FORMAT WITH TXZ EXTENSION
def test_autozip_compress_txz(temp_dir, test_file):
    output = Path(temp_dir) / "archive.txz"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ FORMAT WITH EXPLICIT FORMAT
def test_autozip_compress_tar_xz_explicit_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tar.xz")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR.XZ FORMAT WITH TXZ ALIAS
def test_autozip_compress_txz_alias(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="txz")
    assert result == str(output)
    assert output.exists()

# TEST FOR TAR FORMAT
def test_autozip_compress_tar(temp_dir, test_file):
    output = Path(temp_dir) / "archive.tar"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()
    with tarfile.open(output, 'r') as tar: assert "test.txt" in tar.getnames()

# TEST FOR TAR FORMAT WITH EXPLICIT FORMAT
def test_autozip_compress_tar_explicit_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.unknown"
    result = autozip_compress([test_file], str(output), archive_format="tar")
    assert result == str(output)
    assert output.exists()

# TEST FOR COMPRESSION LEVEL
def test_autozip_compress_compression_level(temp_dir, test_file):
    output = Path(temp_dir) / "archive.zip"
    result = autozip_compress([test_file], str(output), compression_level=9)
    assert result == str(output)
    assert output.exists()

# TEST FOR MULTIPLE SOURCES
def test_autozip_compress_multiple_sources(temp_dir, test_file, test_dir):
    output = Path(temp_dir) / "archive.zip"
    result = autozip_compress([test_file, test_dir], str(output))
    assert result == str(output)
    assert output.exists()

# TEST FOR EMPTY SOURCE PATHS
def test_autozip_compress_empty_sources(temp_dir):
    output = Path(temp_dir) / "archive.zip"
    with pytest.raises(ValueError, match="NO SOURCE PATHS PROVIDED"):
        autozip_compress([], str(output))

# TEST FOR NONEXISTENT SOURCE
def test_autozip_compress_nonexistent_source(temp_dir):
    output = Path(temp_dir) / "archive.zip"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        autozip_compress([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TEST FOR UNSUPPORTED FORMAT
def test_autozip_compress_unsupported_format(temp_dir, test_file):
    output = Path(temp_dir) / "archive.zip"
    with pytest.raises(ValueError, match="UNSUPPORTED FORMAT"):
        autozip_compress([test_file], str(output), archive_format="unknown")

# TEST FOR CASE INSENSITIVE FORMAT
@pytest.mark.parametrize("format_name", ["ZIP", "TAR.GZ", "TAR.BZ2", "TAR.XZ", "TAR"])
def test_autozip_compress_case_insensitive_format(temp_dir, test_file, format_name):
    output = Path(temp_dir) / f"archive.{format_name.lower()}"
    result = autozip_compress([test_file], str(output), archive_format=format_name)
    assert result == str(output)
    assert output.exists()

# TEST FOR OUTPUT DIRECTORY CREATION
def test_autozip_compress_creates_output_dir(temp_dir, test_file):
    output = Path(temp_dir) / "subdir" / "archive.zip"
    result = autozip_compress([test_file], str(output))
    assert result == str(output)
    assert output.exists()
    assert output.parent.exists()

# TEST FOR DIRECTORY COMPRESSION
def test_autozip_compress_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.zip"
    result = autozip_compress([test_dir], str(output))
    assert result == str(output)
    assert output.exists()
    
    with zipfile.ZipFile(output, 'r') as zipf:
        names = zipf.namelist()
        assert any("file1.txt" in name for name in names)

# TEST FOR TAR FORMAT WITH DIRECTORY
def test_autozip_compress_tar_directory(temp_dir, test_dir):
    output = Path(temp_dir) / "archive.tar"
    result = autozip_compress([test_dir], str(output))
    assert result == str(output)
    assert output.exists()
    
    with tarfile.open(output, 'r') as tar:
        names = tar.getnames()
        assert any("test_dir" in name for name in names)

# TEST FOR TAR FORMAT WITH NONEXISTENT FILE
def test_autozip_compress_tar_nonexistent_file(temp_dir):
    output = Path(temp_dir) / "archive.tar"
    with pytest.raises(FileNotFoundError, match="SOURCE PATH NOT FOUND"):
        autozip_compress([str(Path(temp_dir) / "nonexistent.txt")], str(output))

# TEST FOR BRANCH COVERAGE (18->11, 39->32, 56->49, 73->66, 140->133)
def test_compress_zip_path_not_file_not_dir(temp_dir):
    from unittest.mock import patch, MagicMock
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("CONTENT")

    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False
    mock_path.is_dir.return_value = False
    mock_path.name = "test.txt"
    
    output = Path(temp_dir) / "archive.zip"
    
    with patch('autotools.autozip.core.Path', return_value=mock_path):
        result = _compress_zip([str(test_file)], str(output), 6)
        assert result == str(output)
        assert output.exists()

# TEST FOR TAR.GZ WITH PATH THAT IS NEITHER FILE NOR DIR
def test_compress_tar_gz_path_not_file_not_dir(temp_dir):
    from unittest.mock import patch, MagicMock
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("CONTENT")
    
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False
    mock_path.is_dir.return_value = False
    mock_path.name = "test.txt"
    mock_path.__str__ = lambda self: str(test_file)
    mock_path.__fspath__ = lambda self: str(test_file)
    
    output = Path(temp_dir) / "archive.tar.gz"
    
    def path_side_effect(path_arg):
        if str(path_arg) == str(test_file): return mock_path
        return Path(path_arg)
    
    with patch('autotools.autozip.core.Path', side_effect=path_side_effect):
        result = _compress_tar_gz([str(test_file)], str(output), 6)
        assert result == str(output)
        assert output.exists()

# TEST FOR TAR.BZ2 WITH PATH THAT IS NEITHER FILE NOR DIR
def test_compress_tar_bz2_path_not_file_not_dir(temp_dir):
    from unittest.mock import patch, MagicMock
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("CONTENT")
    
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False
    mock_path.is_dir.return_value = False
    mock_path.name = "test.txt"
    mock_path.__str__ = lambda self: str(test_file)
    mock_path.__fspath__ = lambda self: str(test_file)
    
    output = Path(temp_dir) / "archive.tar.bz2"
    
    def path_side_effect(path_arg):
        if str(path_arg) == str(test_file): return mock_path
        return Path(path_arg)
    
    with patch('autotools.autozip.core.Path', side_effect=path_side_effect):
        result = _compress_tar_bz2([str(test_file)], str(output), 6)
        assert result == str(output)
        assert output.exists()

# TEST FOR TAR.XZ WITH PATH THAT IS NEITHER FILE NOR DIR
def test_compress_tar_xz_path_not_file_not_dir(temp_dir):
    from unittest.mock import patch, MagicMock
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("CONTENT")
    
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = False
    mock_path.is_dir.return_value = False
    mock_path.name = "test.txt"
    mock_path.__str__ = lambda self: str(test_file)
    mock_path.__fspath__ = lambda self: str(test_file)
    
    output = Path(temp_dir) / "archive.tar.xz"
    
    def path_side_effect(path_arg):
        if str(path_arg) == str(test_file): return mock_path
        return Path(path_arg)
    
    with patch('autotools.autozip.core.Path', side_effect=path_side_effect):
        result = _compress_tar_xz([str(test_file)], str(output), 6)
        assert result == str(output)
        assert output.exists()

# TEST FOR TAR WITH PATH THAT IS NEITHER FILE NOR DIR
def test_compress_tar_path_not_file_not_dir(temp_dir):
    from unittest.mock import patch, MagicMock
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("CONTENT")
    
    mock_source_path = MagicMock(spec=Path)
    mock_source_path.exists.return_value = True
    mock_source_path.is_file.return_value = False
    mock_source_path.is_dir.return_value = False
    mock_source_path.name = "test.txt"
    mock_source_path.__str__ = lambda self: str(test_file)
    mock_source_path.__fspath__ = lambda self: str(test_file)
    
    output = Path(temp_dir) / "archive.tar"
    output_str = str(output)
    call_count = [0]
    
    def path_side_effect(path_arg):
        path_str = str(path_arg)
        call_count[0] += 1
        if call_count[0] == 1: return Path(path_arg)
        elif path_str == str(test_file): return mock_source_path
        else: return Path(path_arg)
    
    with patch('autotools.autozip.core.Path', side_effect=path_side_effect):
        result = autozip_compress([str(test_file)], output_str)
        assert result == output_str
        assert Path(output_str).exists()
