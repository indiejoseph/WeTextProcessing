#!/usr/bin/env python3
"""Convert the expected 'spoken' parts in test data files under tn/cantonese/test/data
from Simplified Chinese to Traditional Chinese.

Format: each line contains 'written => spoken' or 'written\tspoken'
"""
from pathlib import Path

try:
    from opencc import OpenCC
except Exception:
    OpenCC = None


def convert_test_file(path: Path, cc: "OpenCC") -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    lines = []
    for line in text.splitlines(True):
        if "=>" in line:
            left, right = line.split("=>", 1)
            new_right = cc.convert(right.strip())
            new_line = f"{left.strip()} => {new_right}"
            if line.rstrip("\n") != new_line:
                changed += 1
            lines.append(new_line + ("\n" if line.endswith("\n") else ""))
        elif "\t" in line:
            left, right = line.split("\t", 1)
            new_right = cc.convert(right.strip())
            new_line = f"{left}\t{new_right}"
            if line.rstrip("\n") != new_line:
                changed += 1
            lines.append(new_line + ("\n" if line.endswith("\n") else ""))
        else:
            lines.append(line)
    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def main():
    if OpenCC is None:
        print("opencc not available. Install opencc-python-reimplemented")
        return
    cc = OpenCC("s2t")
    root = Path("tn/cantonese/test/data")
    files = list(root.glob("*.txt"))
    total_changed = 0
    for f in files:
        changed = convert_test_file(f, cc)
        if changed:
            print("Converted", f)
            total_changed += changed
    print("Done. Lines changed:", total_changed)


if __name__ == "__main__":
    main()
