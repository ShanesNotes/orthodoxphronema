"""
canon_audit.py — Identify structural gaps and truncations in canon/.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
CANON_DIR = REPO_ROOT / "canon" / "OT"

def audit_book(file_path: Path):
    lines = file_path.read_text(encoding="utf-8").splitlines()
    report = []
    anchors = {} # anchor -> line_num
    
    for i, line in enumerate(lines):
        line_num = i + 1
        # Match anchor: BOOK.CH:V Text
        m = re.match(r'^([A-Z0-9]{3}\.\d+:\d+)\s+(.*)', line)
        if m:
            anchor = m.group(1)
            text = m.group(2).strip()
            
            # 1. Check for duplicates
            if anchor in anchors:
                report.append(f"DUPLICATE: {anchor} at lines {anchors[anchor]} and {line_num}")
            anchors[anchor] = line_num
            
            # 2. Check for truncation
            # If it ends in a letter or comma, it's likely truncated
            if text and text[-1].isalpha() or text.endswith(','):
                # Filter out some false positives (common words that end sentences in poetry?)
                # Actually, most OSB sentences end in ., !, ?, or †
                if not any(text.endswith(p) for p in ['.', '!', '?', '†', '"', "'", '”', '’', ';', ':', ')']):
                    report.append(f"TRUNCATED?: {anchor} ends with '{text[-10:]}'")
                    
    return report

def run_audit():
    print("Starting global canon structural audit...")
    for file_path in CANON_DIR.glob("*.md"):
        results = audit_book(file_path)
        if results:
            print(f"\nIssues in {file_path.name}:")
            for r in results:
                print(f"  {r}")

if __name__ == "__main__":
    run_audit()
