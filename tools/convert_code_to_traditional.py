#!/usr/bin/env python3
from pathlib import Path

try:
    from opencc import OpenCC
except Exception:
    OpenCC = None

if OpenCC is None:
    print("opencc not installed")
    raise SystemExit(1)

cc = OpenCC("s2t")
root = Path("tn/cantonese")
py_files = list(root.rglob("*.py"))
changed = []
for f in py_files:
    text = f.read_text(encoding="utf-8")
    new_text = cc.convert(text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        changed.append(str(f))
print("Converted files:", len(changed))
for c in changed:
    print(" ", c)
