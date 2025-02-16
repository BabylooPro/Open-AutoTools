# Changelog

All notable changes to Open-AutoTools will be documented in this file.

## [0.0.3] - Unreleased

### Added

- Added AutoSpell command for spell checking and correction in multiple languages
- Added flag --version to show current version and check for updates

### Changed

- Improved all tools flag --help message with better formatting

## [0.0.2.post2] - 2025-02-16

### Added

- added metadata for pypi distribution and link README.md to pypi

## [0.0.2.post1] - 2025-02-16

### Fixed

- Fixed missing dependencies installation on Windows
- Force list hardcoded requirements in setup.py with latest versions
- Prevent unnecessary commits when no changes exist
- Update setup.py to handle requirements file more robustly

### Added

- Added setuptools requirement for package management
- Added file verification and wheel package
- Added checkout master branch with full git history
- Added write permissions for contents workflow action
- Added publish to PyPI workflow with release page

### Changed

- Updated workflow to use master branch
- Updated publish workflow for proper git push

## [0.0.2] - 2025-02-15

### Added

- Added autoip command for network and IP-related utilities
- Added autolower command for text lowercase transformation
- Added autopassword command for secure password generation

### Changed

- Improved browser cookie auth and user consent system for autodownload command
- Enhanced error handling for better download reliability for autodownload command
- Migrated from youtube-dl to yt-dlp
- Refactored autotranslate command with in new structure

### Removed

- Removed old unmaintained autotranslate and autocorrect features

## [0.0.1] - 2024-09-10

### Added

- Initial project setup
- Added Autotools CLI module
- Added Autocorrect functionality using Rewriter API
- Added Autocaps core function definition
- Added initial Autotools package structure
- Added setup package distribution

[0.0.2.post1]: https://github.com/BabylooPro/Open-AutoTools/releases/tag/v0.0.2.post1
[0.0.2]: https://github.com/BabylooPro/Open-AutoTools/releases/tag/v0.0.2
[0.0.1]: https://github.com/BabylooPro/Open-AutoTools/releases/tag/v0.0.1

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
