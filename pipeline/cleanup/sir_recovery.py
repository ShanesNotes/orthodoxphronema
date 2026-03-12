"""
sir_recovery.py — Recover missing Verse 1s in Sirach.
"""

import re
import json
from pathlib import Path
from pipeline.common.pdf_source import extract_pdf_text
from pipeline.common.paths import PDF_PATH, REGISTRY_PATH

REPO_ROOT = Path(__file__).parent.parent.parent
SIR_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "SIR.md"

def get_psa_style_verse_1(ch: int) -> str:
    # Estimate page based on progress. Sirach is pages 2293-2397 (51 chapters)
    # Roughly 2 pages per chapter.
    est_page = 2293 + (ch - 1) * 2
    # Search for "Chapter X" or just the digit centered?
    # Actually, let's just find the text between Chapter X and Verse 2.
    text = extract_pdf_text(est_page, est_page + 2, PDF_PATH, layout=True)
    
    # Simple strategy for Photius: 
    # Look for centered digit 'ch' followed by text, ending before '2'
    # Or look for narrative heading if present.
    
    # For now, I'll manually define the common Verse 1s or use a very targeted 
    # extract if I can find the pattern.
    return ""

def recover_sirach():
    if not SIR_PATH.exists():
        return

    lines = SIR_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    
    # Common Verse 1s identified from PDF probe or Brenton comparison (manually verified for OSB)
    v1_map = {
        1: "All wisdom comes from the Lord And is with Him forever.†",
        2: "My son, if you come to serve the Lord, Prepare your soul for temptation.",
        3: "Hear me, your father, O children, And do likewise, that you may be saved.",
        4: "My son, do not deprive the poor of his living, And do not make the needy eyes wait long.",
        5: "Do not set your heart on your possessions, And do not say , \"I am independent.\" †",
        # ... this is tedious. I should try to automate the 'Text between Ch and V2'
    }

    current_ch = 0
    for line in lines:
        if line.startswith("## Chapter "):
            current_ch = int(line.split(" ")[2])
            new_lines.append(line)
            # Check if next line is already SIR.CH:1
            continue
        
        m = re.match(r'^SIR\.(\d+):(\d+)', line)
        if m:
            ch = int(m.group(1))
            v = int(m.group(2))
            if v == 2 and ch in v1_map:
                # Insert missing Verse 1
                new_lines.append(f"SIR.{ch}:1 {v1_map[ch]}")
            new_lines.append(line)
        else:
            new_lines.append(line)

    # SIR_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    # For now, just print the missing chapters found in SIR.md
    
    found_v1s = set()
    for line in lines:
        m = re.match(r'^SIR\.(\d+):1\b', line)
        if m:
            found_v1s.add(int(m.group(1)))
    
    missing = [ch for ch in range(1, 52) if ch not in found_v1s]
    print(f"Chapters missing Verse 1: {missing}")

if __name__ == "__main__":
    recover_sirach()
