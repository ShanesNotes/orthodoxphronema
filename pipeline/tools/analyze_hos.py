#!/usr/bin/env python3
"""Analyze HOS.md verse number sequence to find chapter boundaries."""
import re
import sys

with open("staging/validated/OT/HOS.md") as f:
    lines = f.readlines()

verse_re = re.compile(r"^HOS\.0:(\d+)\s(.+)$")

items = []
for i, line in enumerate(lines):
    line = line.rstrip()
    m = verse_re.match(line)
    if m:
        vnum = int(m.group(1))
        text_preview = m.group(2)[:80]
        items.append((vnum, text_preview, i+1))

print("Verse number sequence:")
prev_vnum = 0
for idx, (vnum, text, lineno) in enumerate(items):
    marker = ""
    if vnum < prev_vnum:
        marker = "  <--- DROP"
    sys.stdout.write("  L%3d  v%2d  %s%s\n" % (lineno, vnum, text, marker))
    prev_vnum = vnum

print("\nTotal verses:", len(items))
