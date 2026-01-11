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

# INFO: if you want to run tests and some errors occur before see test executable
# install test dependencies directly (optional)
pip install -e ".[test]"

# INFO: if you want to build the package locally and install it to test your new features
# Build the package locally
python -m build  # Creates dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Install from local wheel file
pip install dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Check installation and development mode
autotools --version  # Should show "Development mode: enabled" when using pip install -e .
```

## Key Features

### AutoCaps ![Stability][AUTOCAPS_EFF]

-   **Description:** Converts any text entered by the user to uppercase.
-   **Usage:**
    ```
    ~ ❯ autocaps "Your text here."
    ```
-   **Output:**
    ```
    YOUR TEXT HERE.
    ```

### AutoLower ![Stability][AUTOLOWER_EFF]

-   **Description:** Converts any text entered by the user to lowercase.
-   **Usage:**
    ```
    ~ ❯ autolower "Your text here."
    ```
-   **Output:**
    ```
    your text here.
    ```

### AutoPassword ![Stability][AUTOPASSWORD_EFF]

-   **Description:** Generates secure random passwords and encryption keys with customizable options.
-   **Usage:**
    ```
    ~ ❯ autopassword --length 16
    ~ ❯ autopassword --no-special --length 8
    ~ ❯ autopassword --gen-key
    ~ ❯ autopassword --password-key "your-password" --analyze
    ```
-   **Options:**

    -   `--length, -l`: Set password length (default: 12)
    -   `--no-uppercase, -u`: Exclude uppercase letters
    -   `--no-numbers, -n`: Exclude numbers
    -   `--no-special, -s`: Exclude special characters
    -   `--min-special, -m`: Minimum number of special characters (default: 1)
    -   `--min-numbers, -d`: Minimum number of numbers (default: 1)
    -   `--analyze, -a`: Show password strength analysis
    -   `--gen-key, -g`: Generate a random encryption key
    -   `--password-key, -p`: Generate an encryption key from password

### AutoIP ![Stability][AUTOIP_EFF]

-   **Description:** Displays network information including IP addresses, connectivity tests, speed tests, and more.
-   **Usage:**

    ```bash
    ~ ❯ autoip
    ~ ❯ autoip --speed
    ~ ❯ autoip --location
    ~ ❯ autoip --no-ip --test --speed
    ```

-   **Options:**

    -   `--test, -t`: Run connectivity tests to popular services
    -   `--speed, -s`: Run internet speed test
    -   `--monitor, -m`: Monitor real-time network traffic
    -   `--interval, -i`: Monitoring interval in seconds
    -   `--ports, -p`: Check status of common ports
    -   `--dns, -d`: Show DNS server configuration
    -   `--location, -l`: Show IP geolocation information
    -   `--no-ip, -n`: Hide IP addresses display

-   **Features:**

    -   Local and public IP detection (IPv4 & IPv6)
    -   Internet speed testing
    -   Network connectivity checks
    -   Monitoring interval (10 seconds)
    -   Real-time traffic monitoring
    -   Port scanning
    -   DNS server information
    -   IP geolocation

    -   **Compatibility:**

    -   Windows 10/11 ✓
    -   macOS 15+ ✓
    -   Linux ✗

### Test Suite (DEVELOPMENT ONLY)

-   **Description:** Run the test suite for Open-AutoTools
-   **Usage:**
    ```bash
    ~ ❯ autotools test
    ```
-   **Options:**

    -   `--unit, -u`: Run only unit tests
    -   `--integration, -i`: Run only integration tests
    -   `--no-cov`: Disable coverage report
    -   `--html`: Generate HTML coverage report (saved in `htmlcov/`)
    -   `--module, -m`: Test specific module (e.g., autocaps, autolower)

-   **Coverage Configuration:**

    Coverage settings are configured in `.coveragerc`. The default configuration includes:

    -   Branch coverage
    -   Exclusion of test files and virtual environments
    -   HTML reports in `htmlcov/` directory
    -   XML reports in `coverage.xml`

## Docker Support

Open-AutoTools can be tested across multiple platforms using Docker containers:

```bash
# Build and run tests for all platforms
docker-compose build
docker-compose up

# Test specific platform
docker-compose up ubuntu    # For Ubuntu
docker-compose up macos     # For macOS
docker-compose up windows   # For Windows

# Clean up
docker-compose down --remove-orphans
```

Each platform-specific container includes:

-   Python 3.11/3.12 environment
-   All required dependencies (FFmpeg, Java, etc.)
-   Automated test suite
-   Volume mapping for persistent data

> **Note:** The Docker setup is primarily for testing and development. For regular use, install via pip as described above.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

[AUTOCAPS_EFF]: https://img.shields.io/badge/Stability-99%25-success
[AUTOLOWER_EFF]: https://img.shields.io/badge/Stability-99%25-success
[AUTOPASSWORD_EFF]: https://img.shields.io/badge/Stability-90%25-success
[AUTOIP_EFF]: https://img.shields.io/badge/Stability-95%25-success
