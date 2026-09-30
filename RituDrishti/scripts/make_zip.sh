#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p frontend/public/downloads
python - <<'PY'
import zipfile
from pathlib import Path
root=Path.cwd(); out=root/'frontend/public/downloads/RituDrishti_code.zip'
excluded={'node_modules','.git','.venv','venv','__pycache__','.pytest_cache','build','downloads','test_reports','.cache'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if not p.is_file() or any(x in excluded for x in p.relative_to(root).parts): continue
  if p.name=='.env' or p.suffix in {'.parquet','.joblib','.pyc','.log','.zip'}: continue
  z.write(p,Path('RituDrishti')/p.relative_to(root))
print(out)
PY