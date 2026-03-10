#!/usr/bin/env python3
"""Deduplicate headings in JOB.md — keep only the first occurrence of each heading text."""

import re
from pathlib import Path

JOB_MD = Path("/home/ark/orthodoxphronema/staging/validated/OT/JOB.md")

def main():
    lines = JOB_MD.read_text().splitlines()
    seen = set()
    out = []
    skip_blanks_after_removed = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            if line in seen:
                # Remove this heading and surrounding blank lines
                # Look back to remove preceding blank line
                while out and out[-1].strip() == '':
                    out.pop()
                # Skip this heading line
                i += 1
                # Skip following blank line(s)
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
                continue
            else:
                seen.add(line)
        out.append(line)
        i += 1

    content = "\n".join(out) + "\n"
    JOB_MD.write_text(content)

    heading_count = sum(1 for l in out if l.startswith("### "))
    verse_count = len(re.findall(r'^JOB\.\d+:\d+', content, re.MULTILINE))
    print(f"Unique headings remaining: {heading_count}")
    print(f"Verse lines: {verse_count}")

if __name__ == "__main__":
    main()
