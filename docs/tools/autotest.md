# Test Suite (DEVELOPMENT ONLY)

## Description

Run the test suite for Open-AutoTools. Automatically installs pytest and pytest-cov if they are missing. Displays colored coverage metrics (green/yellow/red) based on coverage percentage.

## Usage

```bash
autotools test
```

## Options

- `--unit, -u`: Run only unit tests
- `--integration, -i`: Run only integration tests
- `--no-cov`: Disable coverage report
- `--html`: Generate HTML coverage report (saved in `htmlcov/`)
- `--module, -m`: Test specific module (e.g., autocaps, autolower)

## Coverage Configuration

Coverage settings are configured in `.coveragerc`. The default configuration includes:

- Branch coverage
- Exclusion of test files and virtual environments
- HTML reports in `htmlcov/` directory
- XML reports in `coverage.xml`

## Examples

```bash
# Run all tests
autotools test

# Run only unit tests
autotools test --unit

# Run only integration tests
autotools test --integration

# Test specific module
autotools test --module autocaps

# Generate HTML coverage report
autotools test --html

# Run tests without coverage
autotools test --no-cov
```
