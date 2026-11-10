#!/usr/bin/env python3
"""Regenerate/check platform and Soar tables from the bundled Expo glyph map."""
import argparse
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
rows = []
for line in (root / "assets/glyphmap.txt").read_text(encoding="utf-8").splitlines():
    name, value = line.split("\t")
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError(f"invalid icon name {name!r}")
    scalar = int(value, 16)
    if scalar > 0x10FFFF or 0xD800 <= scalar <= 0xDFFF:
        raise ValueError(f"invalid Unicode scalar for {name}")
    rows.append((name, value, chr(scalar)))
if len(rows) != 7448 or [r[0] for r in rows] != sorted({r[0] for r in rows}):
    raise ValueError("map must contain 7,448 sorted unique names")
chunks = []
current = ""
for name, value, _ in rows:
    line = f"{name}\t{value}\n"
    if len(current) + len(line) > 10000:
        chunks.append(current)
        current = ""
    current += line
if current:
    chunks.append(current)
literals = ",\n".join(json.dumps(chunk, ensure_ascii=True) for chunk in chunks)
soar_table = json.dumps("".join(f"{name}\t{glyph}\n" for name, _, glyph in rows), ensure_ascii=False)
files = [
    (root / "android/src/dev/soar/plugins/materialicons/MaterialIconsModule.kt", r'(private val data = arrayOf\(\n).*?(\n        \)\.joinToString\(""\))', literals),
    (root / "ios/Sources/MaterialIconsModule.swift", r'(private static let data = \[\n).*?(\n    \]\.joined\(\))', literals),
    (root / "soar/MaterialCommunityIcon.soar", r'(const table = ).*?(;\n)', soar_table),
]
parser = argparse.ArgumentParser()
parser.add_argument("--write", action="store_true", help="write generated tables; default checks them")
args = parser.parse_args()
for path, pattern, replacement in files:
    original = path.read_text(encoding="utf-8")
    generated, count = re.subn(pattern, lambda m: m.group(1) + replacement + m.group(2), original, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"generated section missing in {path}")
    if args.write:
        path.write_text(generated, encoding="utf-8")
    elif generated != original:
        raise SystemExit(f"stale generated table: {path}")
print("All generated tables match 7,448 glyphs.")
