### TODO LIST

**_Bugs to fix_**

- [ ] **fix:** ![HIGH][high] optimize execution performance of all tools features
- [ ] **fix:** ![MID][mid] detect unclosed double quotes in CLI commands and automatically fix them by either adding a closing double quote at the end or switching to single quotes
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

- [ ] **fix:** ![HIGH][high] unable to autodownload MP3 files from YouTube; MP4 files are downloaded instead
- [ ] **fix:** ![HIGH][high] option quality is not working for autodownload tool, instead the default (1080p) quality is downloaded

#### DONE - v0.0.3-rc.4

-

#### DONE - v0.0.3-rc.3

- [x] **fixed:** YouTube download functionality now using mobile API for better reliability and no browser dependencies
- [x] **added:** File existence checks with user prompts for overwrites for download tool
- [x] **improved:** Progress tracking with detailed download status
- [x] **fixed:** YouTube download functionality with proper format and quality handling, including FFmpeg support for reliable format conversion
- [x] **added:** loading animation with moving dots (...) during tool operations
- [x] **refactored:** CLI module structure and command organization

[high]: https://img.shields.io/badge/-HIGH-red
[mid]: https://img.shields.io/badge/-MID-yellow
[low]: https://img.shields.io/badge/-LOW-green
