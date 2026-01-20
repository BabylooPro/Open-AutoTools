#!/usr/bin/env bash

set -euo pipefail

# DETERMINE SCRIPT AND COMPOSE FILE LOCATIONS
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"

# SET PYTHON VERSIONS AND SERVICES TO TEST
PYTHON_VERSIONS=(${PYTHON_VERSIONS:-"3.10 3.11 3.12 3.13 3.14"})
SERVICES=(${SERVICES:-"ubuntu macos windows"})

# DETECT AND CONFIGURE DOCKER COMPOSE COMMAND
if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
else
  echo "ERROR: docker compose NOT FOUND (NEED docker-compose OR docker compose PLUGIN)." >&2
  exit 127
fi

# PRINT MATRIX CONFIGURATION
echo "RUNNING DOCKER MATRIX TESTS"
echo "COMPOSE FILE: ${COMPOSE_FILE}"
echo "PYTHON VERSIONS: ${PYTHON_VERSIONS[*]}"
echo "SERVICES: ${SERVICES[*]}"
echo

# RUN MATRIX FOR EACH PYTHON VERSION AND SERVICE
for v in "${PYTHON_VERSIONS[@]}"; do
  for svc in "${SERVICES[@]}"; do
    echo "== ${svc} / Python ${v} =="
    COMPOSE_PROFILES=single PYTHON_VERSION="${v}" "${COMPOSE[@]}" -f "${COMPOSE_FILE}" run --build --rm "${svc}"
    echo
  done
done

# PRINT SUCCESS MESSAGE
echo "ALL MATRIX TESTS PASSED."
