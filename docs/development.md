# Development

Open-AutoTools is developed using Python 3.11.

## Setup Development Environment

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

# install test dependencies directly (optional)
pip install -e ".[test]"

# Build the package locally
python -m build  # Creates dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Install from local wheel file
pip install dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Check installation and development mode
autotools --version  # Should show "Development mode: enabled" when using pip install -e .
```

## Running Tests

See [autotest.md](autotest.md) for detailed information about running the test suite.
