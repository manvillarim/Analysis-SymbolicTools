#!/usr/bin/env bash
# Full experimental pipeline. Every step is resumable: re-running skips the
# measurements already stored in results/.
set -euo pipefail
cd "$(dirname "$0")/.."

export MEMORY_MAX="${MEMORY_MAX:-10G}"

# 0. tools and subjects (pinned in repro/versions.env)
./repro/setup.sh

# 1. per test case: verdict, time and peak memory (both tools with Z3)
./repro/run.py pertest
./repro/run.py reparse

# 2. concrete confirmation of every counterexample, trace triage, classification
./repro/confirm.py
./repro/triage.py
./repro/classify.py

# 3. complete suite, 10 runs per tool and subject (interleaved)
./repro/run.py suite --runs 10

# 4. sensitivity of the verdicts to the exploration bounds
./repro/run.py pertest --out results/sensitivity \
    --halmos-args "--loop 4 --solver-timeout-assertion 600s" \
    --hevm-args "--max-iterations 20 --smt-timeout 600"
./repro/run.py reparse --out results/sensitivity

# 5. supplementary: Halmos with its own default solver (Yices)
./repro/run.py pertest --out results/halmos_yices --tools halmos --halmos-args "--solver yices"
./repro/run.py reparse --out results/halmos_yices
./repro/run.py suite --out results/halmos_yices --tools halmos --runs 10 --halmos-args "--solver yices"

# 6. tables and figures
./repro/analyze.py
