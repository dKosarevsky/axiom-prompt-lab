#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="${1:-$(date +%Y-%m-%d)}"
RUN_DIR="$ROOT_DIR/reports/runs/$RUN_ID"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is required to run promptfoo report evals." >&2
  exit 2
fi

mkdir -p "$RUN_DIR"
cd "$ROOT_DIR/evals"

promptfoo eval -c promptfooconfig.report.yaml \
  --output "$RUN_DIR/results.json" \
  --output "$RUN_DIR/results.csv" \
  --output "$RUN_DIR/results.html"

echo "artifacts: $RUN_DIR"
