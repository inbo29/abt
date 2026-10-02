#!/usr/bin/env bash
# Builds design-system/components/bundle.js from design-system/components/src/
# and copies the design-system files the screens load into screens/ds/abt/.
set -euo pipefail
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(cd "$TOOLS/.." && pwd)"
cd "$TOOLS"
mkdir -p out
npx --no-install esbuild "$ROOT/design-system/components/src/index.tsx" \
  --bundle --format=iife --target=es2019 \
  --jsx=transform --jsx-factory=React.createElement --jsx-fragment=React.Fragment \
  --minify --legal-comments=none --outfile=out/bundle.js --log-level=warning
python3 - "$ROOT" <<'PY'
import json, os, shutil, sys
root = sys.argv[1]
comps = ["Icon", "Button", "StatusBadge", "Money", "EventCode", "DateTime", "KpiTile", "DataTable", "BudgetBar", "ApprovalSteps", "AuditLog", "Alert", "ScheduleGrid", "Tabs", "Segmented", "TextField", "Select", "MoneyField", "Checkbox", "Attachment", "SideNav", "MobileTabBar"]
hdr = {"format": 4, "namespace": "Abt", "components": [{"name": c} for c in comps]}
js = open(os.path.join(root, 'tools', 'out', 'bundle.js'), encoding='utf-8').read()
assert '</script' not in js.lower() and '<!--' not in js, 'bundle must not contain </script or <!--'
out = '/* @ds-bundle: ' + json.dumps(hdr, separators=(',', ':')) + ' */\n/* ABT Ops components. Icons: Lucide (ISC License, https://lucide.dev). */\n' + js
for rel in ('design-system/components/bundle.js', 'screens/ds/abt/components/bundle.js'):
    with open(os.path.join(root, rel), 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
# The screens load their own copies of these design-system files.
shutil.copyfile(os.path.join(root, 'design-system/components/bundle.css'), os.path.join(root, 'screens/ds/abt/components/bundle.css'))
shutil.copyfile(os.path.join(root, 'design-system/tokens.json'), os.path.join(root, 'screens/ds/abt/tokens.json'))
print('bundle.js', len(out.encode('utf-8')), 'bytes -> design-system/components, screens/ds/abt/components')
PY
