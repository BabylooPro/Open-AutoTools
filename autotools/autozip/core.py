import os
import zipfile
import tarfile
import lzma
from pathlib import Path

# COMPRESSES FILES/DIRECTORIES TO ZIP FORMAT
def _compress_zip(source_paths, output_path, compression_level=6):
    compression_level = min(max(compression_level, 0), 9)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                raise FileNotFoundError(f"SOURCE PATH NOT FOUND: {source_path}")
            
            if source.is_file():
                zipf.write(source, source.name)
            elif source.is_dir():
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(source)
                        zipf.write(file_path, arcname)
    
    return output_path

# COMPRESSES FILES/DIRECTORIES TO TAR.GZ FORMAT
def _compress_tar_gz(source_paths, output_path, compression_level=6):
    compression_level = min(max(compression_level, 1), 9)
    
    with tarfile.open(output_path, 'w:gz', compresslevel=compression_level) as tar:
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                raise FileNotFoundError(f"SOURCE PATH NOT FOUND: {source_path}")
            tar.add(source, arcname=source.name)
    
    return output_path

# COMPRESSES FILES/DIRECTORIES TO TAR.BZ2 FORMAT
def _compress_tar_bz2(source_paths, output_path, compression_level=6):
    compression_level = min(max(compression_level, 1), 9)
    
    with tarfile.open(output_path, 'w:bz2', compresslevel=compression_level) as tar:
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                raise FileNotFoundError(f"SOURCE PATH NOT FOUND: {source_path}")
            tar.add(source, arcname=source.name)
    
    return output_path

# COMPRESSES FILES/DIRECTORIES TO TAR.XZ FORMAT
def _compress_tar_xz(source_paths, output_path, compression_level=6):
    compression_level = min(max(compression_level, 0), 9)

    import lzma
    with lzma.open(output_path, 'wb', preset=compression_level) as lzma_file:
        with tarfile.open(fileobj=lzma_file, mode='w') as tar:
            for source_path in source_paths:
                source = Path(source_path)
                if not source.exists():
                    raise FileNotFoundError(f"SOURCE PATH NOT FOUND: {source_path}")
                tar.add(source, arcname=source.name)
    
    return output_path

# DETERMINES OUTPUT FORMAT FROM FILE EXTENSION
def _get_format_from_extension(output_path):
    path_str = str(output_path).lower()
    if path_str.endswith('.tar.gz') or path_str.endswith('.tgz'): return 'tar.gz'
    elif path_str.endswith('.tar.bz2') or path_str.endswith('.tbz2'): return 'tar.bz2'
    elif path_str.endswith('.tar.xz') or path_str.endswith('.txz'): return 'tar.xz'
    elif path_str.endswith('.tar'): return 'tar'
    elif path_str.endswith('.zip'): return 'zip'
    else:
        ext = Path(output_path).suffix.lower()
        raise ValueError(f"UNSUPPORTED ARCHIVE FORMAT: {ext}\nSUPPORTED: .zip, .tar.gz, .tar.bz2, .tar.xz, .tar")

# COMPRESSES FILES/DIRECTORIES TO TAR FORMAT (UNCOMPRESSED)
def _compress_tar(source_paths, output_path):
    with tarfile.open(output_path, 'w') as tar:
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                raise FileNotFoundError(f"SOURCE PATH NOT FOUND: {source_path}")
            tar.add(source, arcname=source.name)

    return output_path

# COMPRESSES FILES AND DIRECTORIES INTO VARIOUS ARCHIVE FORMATS
def autozip_compress(source_paths, output_path, archive_format=None, compression_level=6):
    if not source_paths:
        raise ValueError("NO SOURCE PATHS PROVIDED")
    
    output = Path(output_path)
    if archive_format is None: archive_format = _get_format_from_extension(output_path)
    archive_format = archive_format.lower()
    output.parent.mkdir(parents=True, exist_ok=True)
    
    if archive_format == 'zip': return _compress_zip(source_paths, str(output), compression_level)
    elif archive_format in ('tar.gz', 'tgz'): return _compress_tar_gz(source_paths, str(output), compression_level)
    elif archive_format in ('tar.bz2', 'tbz2'): return _compress_tar_bz2(source_paths, str(output), compression_level)
    elif archive_format in ('tar.xz', 'txz'): return _compress_tar_xz(source_paths, str(output), compression_level)
    elif archive_format == 'tar': return _compress_tar(source_paths, str(output))
    else: raise ValueError(f"UNSUPPORTED FORMAT: {archive_format}\nSUPPORTED: zip, tar.gz, tar.bz2, tar.xz, tar")
