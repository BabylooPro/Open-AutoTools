### TODO LIST

**_Bugs to fix_**

- [ ] **fix:** ![HIGH][high] ensure no IP addresses or sensitive information are exposed in workflow logs with autoip tools
- [ ] **fix:** ![HIGH][high] optimize execution performance of all tools features
- [ ] **fix:** ![MID][mid] detect unclosed double quotes in CLI commands and automatically fix them by either adding a closing double quote at the end or switching to single quotes
- [ ] **fix:** ![MID][mid] multiple warning in unit/integration tests
- [ ] **fix:** ![LOW][low] read requirements only from `requirements.txt` in the released version (actually cannot build without the listed requirements in `setup.py`)

---

**_New features to add_**

- [ ] **add:** automatic clipboard copy for all text output tools
- [ ] **add:** AutoZip: Compresses files and directories into various archive formats (e.g., zip, tar.gz)
- [ ] **add:** AutoNote: Takes quick notes and saves them to a text file
- [ ] **add:** AutoTodo: Manages a simple task list in a text file
- [ ] **add:** AutoClipboard: Manages clipboard content, allows easy copy/paste from the command line
- [ ] **add:** AutoSearch: Searches for files and content in specified directories
- [ ] **add:** AutoUnit: Converts measurement units (e.g., meters to feet, liters to gallons)
- [ ] **add:** AutoSearch: Searches for files and content in specified directories with an fast and intelligent search
- [ ] **add:** AutoColor: Converts color codes between different formats (hex, RGB, HSL)
- [ ] **add:** AutoConvert: Converts text, images, audio, and video between different formats

#### IN PROGRESS

- [ ] **fixing:** ![HIGH][high] windows pre-release download issue with HTTP 403 errors
  - _**info:** download works in dev mode but fails in pre-release with "HTTP Error 403: Forbidden"_
  - _**info:** issue specific to Windows, works fine on MacOS (pre-release or dev mode)_
  - _**info:** affects all video qualities (1440p, 1080p, 720p, 480p, 360p)_

#### DONE - v0.0.3-rc.6

- [x] **added:** docker support for cross-platform testing all tools command (ubuntu, macos, windows)
- [x] **fixed:** handle pyperclip clipboard errors in headless environments
- [x] **fixed:** warning cache issues with Python setup in workflow CI for all available python versions

#### DONE - v0.0.3-rc.5 ✓

- [x] **fixed:** pytest command compatibility issues on Windows systems by improving argument handling and using system Python executable
- [x] **fixed:** Windows compatibility by enhanced YouTube download reliability with mobile API prioritization and adding emoji fallback system

#### DONE - v0.0.3-rc.4 ✓

- [x] **fixed:** unable to autodownload MP3 files from YouTube; MP4 files are downloaded instead
- [x] **fixed:** option quality is not working for autodownload tool, instead the default (1080p) quality is downloaded

#### DONE - v0.0.3-rc.3 ✓

- [x] **fixed:** YouTube download functionality now using mobile API for better reliability and no browser dependencies
- [x] **added:** File existence checks with user prompts for overwrites for download tool
- [x] **improved:** Progress tracking with detailed download status
- [x] **fixed:** YouTube download functionality with proper format and quality handling, including FFmpeg support for reliable format conversion
- [x] **added:** loading animation with moving dots (...) during tool operations
- [x] **refactored:** CLI module structure and command organization

[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
