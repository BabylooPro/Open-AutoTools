### TODO LIST

#### TASK

- **fix:** HIGH optimize execution performance of all tools features
- **fix:** detect unclosed double quotes in CLI commands and automatically fix them by either adding a closing double quote at the end or switching to single quotes
- **add:** AAA comments in tests file (Arrange-Act-Assert)
- **add:** AutoNote: Takes quick notes and saves them to a markdown file
- **add:** AutoClipboard: Manages clipboard content, allows easy copy/paste from the command line
- **add:** AutoSearch: Searches for files and content in specified directories

#### IN PROGRESS

#### DONE - v0.0.5

- **added:** AutoZip: Compresses files and directories into various archive formats (example: zip, tar.gz)
- **added:** AutoConvert: Converts text, images, audio, and video between different formats
- **added:** AutoColor: Converts color codes between different formats (hex, RGB, HSL, etc)
- **added:** AutoUnit: Converts measurement units (example: meters to feet, liters to gallons)
- **added:** AutoTodo: Manages a simple task list in a markdown file
- **added(restored):** docstrings to tools command functions with \b method
- **fixed:** ensure no IP addresses or sensitive information are exposed in workflow logs with autoip tools
- **added:** check whether Python 3.13 and 3.14 are fully compatible

#### DONE - v0.0.4

- **fixed:** multiple warning in unit/integration tests
- **fixed:** read requirements only from `requirements.txt` in the released version (actually cannot build without the listed requirements in `setup.py`)

#### DONE - v0.0.3-rc.6

- **added:** docker support for cross-platform testing all tools command (ubuntu, macos, windows)
- **fixed:** handle pyperclip clipboard errors in headless environments
- **fixed:** warning cache issues with Python setup in workflow CI for all available python versions

#### DONE - v0.0.3-rc.5 ✓

- **fixed:** pytest command compatibility issues on Windows systems by improving argument handling and using system Python executable
- **fixed:** Windows compatibility by enhanced YouTube download reliability with mobile API prioritization and adding emoji fallback system

#### DONE - v0.0.3-rc.4 ✓

- **fixed:** unable to autodownload MP3 files from YouTube; MP4 files are downloaded instead
- **fixed:** option quality is not working for autodownload tool, instead the default (1080p) quality is downloaded

#### DONE - v0.0.3-rc.3 ✓

- **fixed:** YouTube download functionality now using mobile API for better reliability and no browser dependencies
- **added:** File existence checks with user prompts for overwrites for download tool
- **improved:** Progress tracking with detailed download status
- **fixed:** YouTube download functionality with proper format and quality handling, including FFmpeg support for reliable format conversion
- **added:** loading animation with moving dots (...) during tool operations
- **refactored:** CLI module structure and command organization
