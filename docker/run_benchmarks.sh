#!/bin/bash

set -euo pipefail

export CI=1
export PYTHONDONTWRITEBYTECODE=1

BENCHMARK_OUTPUT_DIR=${BENCHMARK_OUTPUT_DIR:-/benchmarks/data}
BENCHMARK_WORKDIR=${BENCHMARK_WORKDIR:-/tmp/autotools-benchmarks}
BENCHMARK_RUN_ID=${BENCHMARK_RUN_ID:-$(date -u +run_%Y%m%dT%H%MZ)}

export BENCHMARK_OUTPUT_DIR
export BENCHMARK_WORKDIR
export BENCHMARK_RUN_ID

mkdir -p "$BENCHMARK_OUTPUT_DIR"
mkdir -p "$BENCHMARK_WORKDIR"

echo "Running AutoTools CLI benchmarks..."
echo "Platform: ${PLATFORM:-Ubuntu}"
echo "Python: $(python --version 2>&1)"
echo "Run ID: $BENCHMARK_RUN_ID"
echo "Output dir: $BENCHMARK_OUTPUT_DIR"
echo "Workdir: $BENCHMARK_WORKDIR"
echo

python /app/docker/benchmark_runner.py
