#!/usr/bin/env python3
"""Convert text files from Simplified Chinese to Traditional Chinese.

Usage:
  python tools/convert_to_traditional.py [--apply]

Default (no --apply) does a dry-run and prints which files would change.
"""
import argparse
from pathlib import Path

try:
    from opencc import OpenCC
except Exception:
    OpenCC = None


def convert_file(path: Path, cc: "OpenCC") -> bool:
    text = path.read_text(encoding="utf-8")
    new_lines = []
    changed = False
    for line in text.splitlines(True):
        if "\t" in line:
            parts = line.rstrip("\n").split("\t")
            new_parts = [cc.convert(p) for p in parts]
            new_line = "\t".join(new_parts) + ("\n" if line.endswith("\n") else "")
        else:
            new_line = cc.convert(line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)
    if changed:
        text = "".join(new_lines)
        # 爲 -> 為 and 啓 ->	啟 conversion is not covered by opencc 's2t' config, so we add a manual mapping
        text = text.replace("爲", "為")
        text = text.replace("啓", "啟")
        path.write_text(text, encoding="utf-8")
    return changed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="Modify files in-place")
    p.add_argument(
        "--root", default="tn/cantonese/data", help="Root data dir to convert"
    )
    args = p.parse_args()

    if OpenCC is None:
        print(
            "opencc not installed. Install with `pip install opencc-python-reimplemented`"
        )
        return

    cc = OpenCC("s2t")

    root = Path(args.root)
    if not root.exists():
        print(f"Root path {root} does not exist")
        return

    tsv_files = list(root.rglob("*.tsv"))
    changed_files = []
    for f in tsv_files:
        text = f.read_text(encoding="utf-8")
        # Quick check if contains any Chinese character probably simplified
        if not any("\u4e00" <= ch <= "\u9fff" for ch in text):
            continue
        if args.apply:
            changed = convert_file(f, cc)
            if changed:
                changed_files.append(str(f))
        else:
            # Dry-run: check conversion without writing
            new_text = "\n".join([cc.convert(line) for line in text.splitlines()])
            if new_text != text:
                changed_files.append(str(f))

    if args.apply:
        if changed_files:
            print("Converted files:")
            for c in changed_files:
                print("  ", c)
        else:
            print("No files changed.")
    else:
        if changed_files:
            print("Files that would change:")
            for c in changed_files:
                print("  ", c)
        else:
            print("No files would change.")


if __name__ == "__main__":
    main()
