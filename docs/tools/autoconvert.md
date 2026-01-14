# AutoConvert

## Description

Converts text, images, audio, and video files between different formats. Supports a wide range of format conversions for various media types.

## Supported Formats

### Text Formats

-   **Input**: txt, md, markdown, json, xml, html, htm, csv
-   **Output**: txt, md, markdown, json, xml, html, htm, csv

### Image Formats

-   **Input/Output**: jpg, jpeg, png, gif, bmp, webp, tiff, tif, ico, svg

> **Note**: SVG is detected as an image format but conversion may have limitations depending on the target format.

### Audio Formats

-   **Input/Output**: mp3, wav, ogg, flac, aac, m4a, wma, opus

> **Note**: WMA and Opus formats are detected but may require additional codec support in FFmpeg.

### Video Formats

-   **Input/Output**: mp4, avi, mov, mkv, wmv, flv, webm, m4v

> **Note**: WMV, FLV, and M4V formats are detected but may require additional codec support in FFmpeg.

## Usage

```bash
autoconvert <input_file> <output_file>
```

### Options

-   `--input-type, -i`: Force input file type (text/image/audio/video)
-   `--output-type, -o`: Force output file type (text/image/audio/video)
-   `--format, -f`: Output format (overrides output file extension)

## Examples

### Text Conversions

```bash
# Convert text to JSON
autoconvert document.txt document.json

# Convert JSON to XML
autoconvert data.json data.xml

# Convert HTML to Markdown
autoconvert page.html page.md

# Convert text to HTML
autoconvert content.txt content.html
```

### Image Conversions

```bash
# Convert JPG to PNG
autoconvert photo.jpg photo.png

# Convert PNG to WebP
autoconvert image.png image.webp

# Convert GIF to JPG
autoconvert animation.gif animation.jpg
```

### Audio Conversions

```bash
# Convert MP3 to WAV
autoconvert song.mp3 song.wav

# Convert WAV to FLAC
autoconvert audio.wav audio.flac

# Convert OGG to MP3
autoconvert track.ogg track.mp3
```

### Video Conversions

```bash
# Convert MP4 to AVI
autoconvert video.mp4 video.avi

# Convert MOV to MP4
autoconvert movie.mov movie.mp4

# Convert AVI to WebM
autoconvert clip.avi clip.webm
```

### Using Format Options

```bash
# Specify format explicitly
autoconvert input.jpg output.png --format png

# Force input type
autoconvert file.txt file.json --input-type text --output-type text
```

## Dependencies

AutoConvert requires additional dependencies for different conversion types:

-   **Images**: `Pillow` (PIL)
-   **Audio**: `pydub` (requires FFmpeg)
-   **Video**: `moviepy` (requires FFmpeg)

Install dependencies:

```bash
pip install Pillow pydub moviepy
```

> **Note**: For audio and video conversions, you also need to install FFmpeg on your system:

-   **macOS**: `brew install ffmpeg`
-   **Linux**: `sudo apt-get install ffmpeg` or `sudo yum install ffmpeg`
-   **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Error Handling

The tool will display clear error messages if:

-   Input file doesn't exist
-   Required dependencies are not installed
-   Conversion fails due to unsupported format or corrupted file
-   Output directory cannot be created

## Notes

-   The tool automatically detects file types based on file extensions
-   Output directories are created automatically if they don't exist
-   Text conversions preserve content while changing format structure
-   Image conversions handle transparency (RGBA) appropriately for formats that don't support it (example: converting RGBA PNG to JPG)
-   Audio and video conversions may take longer depending on file size and system performance
-   Cross-type conversions (example: text to image) are not supported - conversions must be within the same media type
-   The `--format` option overrides the output file extension and automatically detects the output type
