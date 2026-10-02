#!/usr/bin/env bash
# Rebuilds everything that is generated in this repository:
#   1. design tokens   -> design-system/tokens.json, screens/ds/abt/tokens.css
#   2. component bundle -> design-system/components/bundle.js (+ copies in screens/ds/abt/)
#   3. screens          -> screens/*.dc.html
# Running it on an unchanged checkout leaves `git status` clean.
set -euo pipefail
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHONDONTWRITEBYTECODE=1 python3 "$TOOLS/tokens/make_tokens.py"
bash "$TOOLS/design-system/build.sh"
bash "$TOOLS/screens/generate.sh"
echo "done"
