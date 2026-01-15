# AutoZip

## Description

Compresses files and directories into various archive formats. Supports ZIP, TAR.GZ, TAR.BZ2, TAR.XZ, and uncompressed TAR formats with customizable compression levels.

## Supported Formats

-   **ZIP**: `.zip` - Standard ZIP archive format
-   **TAR.GZ**: `.tar.gz`, `.tgz` - Gzip-compressed tar archive
-   **TAR.BZ2**: `.tar.bz2`, `.tbz2` - Bzip2-compressed tar archive
-   **TAR.XZ**: `.tar.xz`, `.txz` - XZ-compressed tar archive
-   **TAR**: `.tar` - Uncompressed tar archive

## Usage

```bash
autozip <sources...> --output <archive_path> [OPTIONS]
```

### Options

-   `--output, -o`: Output archive path (required, extension determines format)
-   `--format, -f`: Archive format (auto-detected from output extension if not specified)
-   `--compression, -c`: Compression level (0-9, default: 6)

## Examples

### Basic Usage

```bash
# Compress a single file to ZIP
autozip file.txt -o archive.zip

# Compress multiple files
autozip file1.txt file2.txt -o backup.zip

# Compress a directory
autozip project/ -o project.zip
```

### Different Archive Formats

```bash
# Create a TAR.GZ archive
autozip data/ -o backup.tar.gz

# Create a TAR.BZ2 archive
autozip project/ -o release.tar.bz2

# Create a TAR.XZ archive
autozip files/ -o archive.tar.xz

# Create an uncompressed TAR archive
autozip documents/ -o archive.tar
```

### Compression Levels

```bash
# Maximum compression (slower, smaller file)
autozip large_file.txt -o compressed.zip --compression 9

# Minimum compression (faster, larger file)
autozip file.txt -o archive.zip --compression 0

# Default compression level (6)
autozip file.txt -o archive.zip
```

### Explicit Format Specification

```bash
# Specify format explicitly (overrides extension)
autozip file.txt -o archive.unknown --format zip

# Use short format aliases
autozip data/ -o backup.unknown --format tgz
autozip project/ -o release.unknown --format tbz2
autozip files/ -o archive.unknown --format txz
```

### Mixed Sources

```bash
# Compress files and directories together
autozip file1.txt dir1/ file2.txt dir2/ -o mixed.zip
```

## Compression Levels

Compression levels range from 0 to 9:

-   **0**: No compression (fastest, largest file)
-   **1-5**: Low to medium compression (faster, larger file)
-   **6**: Default compression (balanced speed and size)
-   **7-9**: High to maximum compression (slower, smaller file)

> **Note**: Compression level behavior varies by format:
>
> -   **ZIP**: Supports levels 0-9
> -   **TAR.GZ**: Minimum level is 1 (0 is clamped to 1)
> -   **TAR.BZ2**: Minimum level is 1 (0 is clamped to 1)
> -   **TAR.XZ**: Supports levels 0-9

## Format Detection

The tool automatically detects the archive format from the output file extension:

-   `.zip` → ZIP format
-   `.tar.gz` or `.tgz` → TAR.GZ format
-   `.tar.bz2` or `.tbz2` → TAR.BZ2 format
-   `.tar.xz` or `.txz` → TAR.XZ format
-   `.tar` → TAR format (uncompressed)

You can override the detected format using the `--format` option.

## Error Handling

The tool displays clear error messages if:

-   No source paths are provided
-   Source files or directories don't exist
-   Compression level is out of range (0-9)
-   Unsupported archive format is specified
-   Output directory cannot be created

## Notes

-   Output directories are created automatically if they don't exist
-   The tool preserves directory structure when compressing directories
-   Archive size is displayed after successful compression (in KB or MB)
-   Format names are case-insensitive (ZIP, zip, Zip all work)
-   Multiple source paths can be compressed into a single archive
-   The tool handles both files and directories in the same archive
