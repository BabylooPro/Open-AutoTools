# Open-AutoTools

Open-AutoTools is an innovative project developed in Python, specifically designed to offer a suite of automated tools directly accessible via the terminal. This project aims to simplify and automate daily tasks for developers and terminal users. It is designed to be used as a set of CLI commands, making its features directly accessible from the user's terminal.

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
  - `--no-uppercase`: Exclude uppercase letters
  - `--no-numbers`: Exclude numbers
  - `--no-special`: Exclude special characters
  - `--min-special`: Minimum number of special characters (default: 1)
  - `--min-numbers`: Minimum number of numbers (default: 1)
  - `--gen-key`: Generate a random encryption key
  - `--password-key`: Generate an encryption key from a password
  - `--analyze`: Show password strength analysis

These examples demonstrate how the terminal will display the results after executing each command, providing a straightforward way for users to understand the immediate effects of these commands.

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

### AutoSpell (unreleased)

- **Description:** Checks and corrects spelling in text with multi-language support.
- **Usage:**
  ```
  ~ ❯ autospell "Your text with misspellings"
  ~ ❯ autospell --lang fr "Votre texte avec des fautes"
  ~ ❯ autospell --file document.txt
  ```
- **Options:**
  - `--lang`: Language code (default: en)
  - `--file`: Input from file
  - `--copy`: Copy corrected text to clipboard
  - `--suggest`: Show alternative suggestions
  - `--interactive`: Interactive correction mode

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

  - `--format`: Choose output format (mp4 or mp3)
  - `--quality`: Select video quality (best, 1440p, 1080p, 720p, 480p, 360p, 240p)

- **Features:**

  - Automatic bot detection bypass
  - Browser cookie integration
  - Progress tracking
  - Multiple quality options
  - MP3 audio extraction
  - Downloads to user's Downloads folder
  - Supports both YouTube and general file downloads

- **Setup Requirements:**

  - Chrome browser installed and configured:

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

  > **Note:** The tool uses your Chrome browser's cookies to authenticate with YouTube. This is required to bypass YouTube's bot detection and download restrictions.

### AutoIP

- **Description:** Displays network information including IP addresses, connectivity tests, speed tests, and more.
- **Usage:**

  ```bash
  # Display IP addresses
  ~ ❯ autoip

  # Run speed test
  ~ ❯ autoip --speed

  # Test connectivity
  ~ ❯ autoip --test

  # Show location info
  ~ ❯ autoip --location

  # Monitor network traffic
  ~ ❯ autoip --monitor

  # Check common ports
  ~ ❯ autoip --ports

  # Show DNS servers
  ~ ❯ autoip --dns

  # Hide IP display and only show tests
  ~ ❯ autoip --no-ip --test --speed
  ```

- **Options:**

  - `--test, -t`: Run connectivity tests to popular services
  - `--speed, -s`: Run internet speed test
  - `--monitor, -m`: Monitor real-time network traffic
  - `--ports, -p`: Check status of common ports
  - `--dns, -d`: Show DNS server configuration
  - `--location, -l`: Show IP geolocation information
  - `--no-ip, -n`: Hide IP addresses display

- **Features:**
  - Local and public IP detection (IPv4 & IPv6)
  - Internet speed testing
  - Network connectivity checks
  - Real-time traffic monitoring
  - Port scanning
  - DNS server information
  - IP geolocation

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
