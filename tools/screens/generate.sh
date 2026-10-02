#!/usr/bin/env bash
# Regenerates every screens/*.dc.html from the Python sources in this folder.
# Set ABT_SCREENS_DIR to write somewhere else (for example, to compare).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
for b in batch1 batch2a batch2b batch2c batch2d batch2e batch3a batch3b batch3c batch4a batch4b batch5; do
  PYTHONDONTWRITEBYTECODE=1 python3 "$b.py"
done
