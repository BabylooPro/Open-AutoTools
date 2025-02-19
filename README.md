# Open-AutoTools

[PYPI_BADGE]: https://badge.fury.io/py/Open-AutoTools.svg
[PYPI_URL]: https://pypi.org/project/Open-AutoTools/
[PYTHON_BADGE]: https://img.shields.io/badge/Python-3.11-blue.svg
[PYTHON_URL]: https://www.python.org/downloads/
[CHANGELOG_BADGE]: https://img.shields.io/badge/CHANGELOG-red.svg
[CHANGELOG_URL]: CHANGELOG.md
[TODO_BADGE]: https://img.shields.io/badge/TODO-purple.svg
[TODO_URL]: TODO.md
[TOTAL_STABILITY]: https://img.shields.io/badge/Total%20Stability-73%25-yellow

[![PyPI][PYPI_BADGE]][PYPI_URL] [![Python][PYTHON_BADGE]][PYTHON_URL] [![CHANGELOG][CHANGELOG_BADGE]][CHANGELOG_URL] [![TODO][TODO_BADGE]][TODO_URL] ![Total Stability][TOTAL_STABILITY]

Open-AutoTools is a comprehensive Python CLI toolkit that streamlines everyday developer tasks through a collection of powerful command-line utilities. Each tool is designed to enhance productivity directly from your terminal.

https://github.com/BabylooPro/Open-AutoTools/assets/35376790/d57f2b9d-55f8-4368-bb40-c0010eb9d49a

## How to install to use directly

To install Open-AutoTools, use the following command in your terminal: `pip install open-autotools`

This command installs all the necessary tools to integrate Open-AutoTools into your workflow.

You can also find the package on PyPI at: https://pypi.org/project/Open-AutoTools/

## How to develop more features

Open-AutoTools is developed using Python 3.11.

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

# Install project dependencies
pip install -r requirements.txt

# For development, install in editable mode
pip install -e .
```

## Key Features

### AutoCaps ![Stability][AUTOCAPS_EFF]

- **Description:** Converts any text entered by the user to uppercase.
- **Usage:**
  ```
  ~ ❯ autocaps "Your text here."
  ```
- **Output:**
  ```
  YOUR TEXT HERE.
  ```

### AutoLower ![Stability][AUTOLOWER_EFF]

- **Description:** Converts any text entered by the user to lowercase.
- **Usage:**
  ```
  ~ ❯ autolower "Your text here."
  ```
- **Output:**
  ```
  your text here.
  ```

### AutoPassword ![Stability][AUTOPASSWORD_EFF]

- **Description:** Generates secure random passwords and encryption keys with customizable options.
- **Usage:**
  ```
  ~ ❯ autopassword --length 16
  ~ ❯ autopassword --no-special --length 8
  ~ ❯ autopassword --gen-key
  ~ ❯ autopassword --password-key "your-password" --analyze
  ```
- **Options:**

  - `--length, -l`: Set password length (default: 12)
  - `--no-uppercase, -u`: Exclude uppercase letters
  - `--no-numbers, -n`: Exclude numbers
  - `--no-special, -s`: Exclude special characters
  - `--min-special, -m`: Minimum number of special characters (default: 1)
  - `--min-numbers, -d`: Minimum number of numbers (default: 1)
  - `--analyze, -a`: Show password strength analysis
  - `--gen-key, -g`: Generate a random encryption key
  - `--password-key, -p`: Generate an encryption key from password

  ### AutoDownload ![Stability][AUTODOWNLOAD_EFF]

- **Description:** Downloads videos from YouTube and files from other sources.
- **Usage:**

  ```bash
  # Download YouTube video in MP4 format
  ~ ❯ autodownload https://youtube.com/watch?v=example

  # Download with specific format and quality
  ~ ❯ autodownload https://youtube.com/watch?v=example --format mp3
  ~ ❯ autodownload https://youtube.com/watch?v=example --quality 1080p
  ```

- **Options:**

  - `--format, -f`: Choose output format (mp4 or mp3)
  - `--quality, -q`: Select video quality (best, 1440p, 1080p, 720p, 480p, 360p, 240p)

- **Features:**

  - Automatic bot detection bypass
  - Mobile API integration for better Stability
  - Progress tracking with detailed status
  - Multiple quality options
  - MP3 audio extraction
  - Downloads to user's Downloads folder
  - Supports both YouTube and general file downloads
  - File existence checks with user prompts

- **Setup Requirements:**

  - No special setup required
  - **Technical Requirements:**
    - Internet connection
    - Sufficient storage space
    - yt-dlp library (automatically installed)
    - FFmpeg (required for format conversion)

  > **Note:** The tool uses YouTube's mobile API for better compatibility and reliability.

### AutoIP ![Stability][AUTOIP_EFF]

- **Description:** Displays network information including IP addresses, connectivity tests, speed tests, and more.
- **Usage:**

  ```bash
  ~ ❯ autoip
  ~ ❯ autoip --speed
  ~ ❯ autoip --location
  ~ ❯ autoip --no-ip --test --speed
  ```

- **Options:**

  - `--test, -t`: Run connectivity tests to popular services
  - `--speed, -s`: Run internet speed test
  - `--monitor, -m`: Monitor real-time network traffic
  - `--interval, -i`: Monitoring interval in seconds
  - `--ports, -p`: Check status of common ports
  - `--dns, -d`: Show DNS server configuration
  - `--location, -l`: Show IP geolocation information
  - `--no-ip, -n`: Hide IP addresses display

- **Features:**
  - Local and public IP detection (IPv4 & IPv6)
  - Internet speed testing
  - Network connectivity checks
  - Monitoring interval (10 seconds)
  - Real-time traffic monitoring
  - Port scanning
  - DNS server information
  - IP geolocation

### AutoTranslate ![Stability][AUTOTRANSLATE_EFF]

- **Description:** Translates text between languages with automatic source language detection.
- **Usage:**

  ```
  ~ ❯ autotranslate "Bonjour le monde" --to en
  Hello world

  ~ ❯ autotranslate "Hello world" --to fr --copy
  Bonjour le monde
  // Result also copied to clipboard

  ~ ❯ autotranslate "こんにちは" --to en --detect
  [Detected: ja] Hello

  ~ ❯ autotranslate --list-languages
  // Shows all supported languages
  ```

- **Options:**
  - `--to`: Target language code (default: en)
  - `--from`: Source language code (default: auto-detect)
  - `--copy`: Copy translation to clipboard
  - `--detect`: Show detected source language
  - `--list-languages`: Show all supported language codes and names
  - `--output, -o`: Save translation to file

### AutoSpell (unreleased) ![Stability][AUTOSPELL_EFF]

- **Description:** Checks and corrects spelling in text with multi-language support.
- **Usage:**
  ```
  ~ ❯ autospell "Your text with misspellings"
  ~ ❯ autospell --lang fr "Votre texte avec des fautes"
  ~ ❯ autospell --fix "Text to autocorrect"
  ```
- **Options:**
  - `--lang, -l`: Language code (default: auto)
  - `--fix, -f`: Auto-fix text and copy to clipboard
  - `--copy, -c`: Copy result to clipboard
  - `--list-languages`: Show supported languages
  - `--json, -j`: Output results as JSON
  - `--ignore, -i`: Error types to ignore (spelling/grammar/style/punctuation)
  - `--interactive, -n`: Interactive mode - confirm each correction
  - `--output, -o`: Save corrections to file

### Test Suite (DEVELOPMENT ONLY)

- **Description:** Run the test suite for Open-AutoTools
- **Usage:**
  ```bash
  ~ ❯ autotools test
  ```
- **Options:**

  - `--unit, -u`: Run only unit tests
  - `--integration, -i`: Run only integration tests
  - `--no-cov`: Disable coverage report
  - `--html`: Generate HTML coverage report
  - `--module, -m`: Test specific module (e.g., autocaps, autolower)

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

[AUTOCAPS_EFF]: https://img.shields.io/badge/Stability-99%25-success
[AUTOLOWER_EFF]: https://img.shields.io/badge/Stability-99%25-success
[AUTOPASSWORD_EFF]: https://img.shields.io/badge/Stability-90%25-success
[AUTOTRANSLATE_EFF]: https://img.shields.io/badge/Stability-25%25-red
[AUTOSPELL_EFF]: https://img.shields.io/badge/Stability-25%25-red
[AUTODOWNLOAD_EFF]: https://img.shields.io/badge/Stability-75%25-yellow
[AUTOIP_EFF]: https://img.shields.io/badge/Stability-95%25-success
