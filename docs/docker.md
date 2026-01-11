# Docker Support

Open-AutoTools can be tested across multiple platforms using Docker containers.

## Usage

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

## Platform Support

Each platform-specific container includes:

- Python 3.11/3.12 environment
- All required dependencies (FFmpeg, Java, etc.)
- Automated test suite
- Volume mapping for persistent data

> **Note:** The Docker setup is primarily for testing and development. For regular use, install via pip as described in [installation.md](installation.md).
