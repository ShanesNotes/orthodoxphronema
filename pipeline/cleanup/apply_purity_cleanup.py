"""
apply_purity_cleanup.py — Apply poetry kerning splits to a staged file.
"""

import sys
import re
from pathlib import Path
from pipeline.common.poetry import clean_poetry_text

def apply_cleanup(file_path: Path):
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        return

    lines = file_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    
    # Target common patterns: SIR.CH:V, PSA.CH:V, etc.
    # Pattern: BOOK.CH:V Text
    re_anchor = re.compile(r'^[A-Z0-9]{3}\.\d+:\d+\s+')

    for line in lines:
        if re_anchor.match(line):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                anchor, text = parts
                cleaned_text = clean_poetry_text(text)
                new_lines.append(f"{anchor} {cleaned_text}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Purity cleanup applied to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 apply_purity_cleanup.py <file_path>")
    else:
        apply_cleanup(Path(sys.argv[1]))
