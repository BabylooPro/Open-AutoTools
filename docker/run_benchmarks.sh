#!/bin/bash

set -euo pipefail

export CI=1
export PYTHONDONTWRITEBYTECODE=1

PLATFORM_SAFE=$(printf '%s' "${PLATFORM:-unknown}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-')
PLATFORM_SAFE=${PLATFORM_SAFE%-}
PLATFORM_SAFE=${PLATFORM_SAFE:-unknown}

BENCHMARK_OUTPUT_DIR=${BENCHMARK_OUTPUT_DIR:-/data/benchmarks/${PLATFORM_SAFE}}
BENCHMARK_WORKDIR=${BENCHMARK_WORKDIR:-/tmp/autotools-benchmarks}

export BENCHMARK_OUTPUT_DIR
export BENCHMARK_WORKDIR

mkdir -p "$BENCHMARK_OUTPUT_DIR"
mkdir -p "$BENCHMARK_WORKDIR"

echo "Running AutoTools CLI benchmarks..."
echo "Platform: ${PLATFORM:-Ubuntu}"
echo "Python: $(python --version 2>&1)"
echo "Output dir: $BENCHMARK_OUTPUT_DIR"
echo "Workdir: $BENCHMARK_WORKDIR"
echo

python /app/docker/benchmark_runner.py
