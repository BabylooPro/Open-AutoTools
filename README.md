# Open-AutoTools

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

### AutoCaps

- **Description:** Converts any text entered by the user to uppercase.
- **Usage:**
  ```
  ~ ❯ autocaps "Your text here."
  ```
- **Output:**
  ```
  YOUR TEXT HERE.
  ```

### AutoLower

- **Description:** Converts any text entered by the user to lowercase.
- **Usage:**
  ```
  ~ ❯ autolower "Your text here."
  ```
- **Output:**
  ```
  your text here.
  ```

### AutoPassword

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

### AutoTranslate

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

### AutoSpell (unreleased)

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

### AutoDownload

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
  - Browser cookie integration
  - Progress tracking
  - Multiple quality options
  - MP3 audio extraction
  - Downloads to user's Downloads folder
  - Supports both YouTube and general file downloads

- **Setup Requirements:**

  - Chrome browser (or Chromium Browser) installed and configured:

    ```bash
    # First time setup:
    1. Open Chrome and sign in to YouTube
    2. Make sure you're logged into your Google account
    3. Accept YouTube's terms of service in browser
    ```

  - **Troubleshooting:**

    - If downloads fail with "Sign in to confirm you're not a bot":

      1. Open YouTube in Chrome
      2. Sign in if not already
      3. Solve any CAPTCHA if prompted
      4. Try download again

    - If you get cookie errors:
      1. Clear Chrome cookies
      2. Sign in to YouTube again
      3. Wait a few minutes before downloading

  - **Technical Requirements:**
    - Chrome browser (for cookie and session handling)
    - Active YouTube/Google account
    - Internet connection
    - Sufficient storage space
    - yt-dlp library (automatically installed)
    - FFmpeg (required for format conversion)

  > **Note:** The tool uses your Chrome browser's cookies to authenticate with YouTube. This is required to bypass YouTube's bot detection and download restrictions.

### AutoIP

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
