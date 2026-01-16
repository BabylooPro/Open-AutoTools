#!/bin/bash

set -euo pipefail

# VERBOSE MODE (0=quiet, 1=verbose)
VERBOSE=${VERBOSE:-1}

# FORCE CI MODE FOR DETERMINISTIC OUTPUT (DISABLE UPDATE CHECKS, MASK IPS)
export CI=1

# CREATE DOWNLOAD DIRECTORY
mkdir -p /data/downloads

echo "Running AutoTools smoke tests..."

if [ "$VERBOSE" = "1" ]; then
  autotools smoke --workdir /data/downloads --verbose
else
  autotools smoke --workdir /data/downloads --quiet
fi

echo -e "\nAll tests completed!"
