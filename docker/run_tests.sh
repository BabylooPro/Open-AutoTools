#!/bin/bash

set -euo pipefail

# VERBOSE MODE (0=quiet, 1=verbose)
VERBOSE=${VERBOSE:-1}

# FORCE CI MODE FOR DETERMINISTIC OUTPUT (DISABLE UPDATE CHECKS, MASK IPS)
export CI=1

# CREATE DOWNLOAD DIRECTORY
BASE_WORKDIR=${BASE_WORKDIR:-/data/downloads}

# USE A UNIQUE WORKDIR PER PLATFORM+PYTHON TO AVOID COLLISIONS
PLATFORM_SAFE=${PLATFORM:-unknown}
PY_SAFE=${PYTHON_VERSION:-unknown}
WORKDIR=${WORKDIR:-${BASE_WORKDIR}/${PLATFORM_SAFE}-py${PY_SAFE}}

# CREATE WORKDIR
mkdir -p "$WORKDIR"

# PRINT BASIC RUNTIME INFO (HELPS DEBUG)
echo "Running AutoTools smoke tests..."
echo "Platform: ${PLATFORM:-unknown}"
echo "Python: $(python --version 2>&1)"
echo "Workdir: $WORKDIR"

# RUN SMOKE TESTS WITH VERBOSE OUTPUT IF VERBOSE=1
if [ "$VERBOSE" = "1" ]; then
  autotools smoke --workdir "$WORKDIR" --verbose
else
  autotools smoke --workdir "$WORKDIR" --quiet
fi

# PRINT SUCCESS MESSAGE
echo -e "\nAll tests completed!"
