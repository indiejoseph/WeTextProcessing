#!/usr/bin/env python3
from pathlib import Path

src = Path("tn/cantonese/data/char/traditional_to_simple.tsv")
dst = Path("tn/cantonese/data/char/simple_to_traditional.tsv")

if not src.exists():
    print("Source file not found:", src)
else:
    lines = []
    for line in src.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            a, b = line.split("\t", 1)
            lines.append(f"{b}\t{a}")
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Generated", dst)
