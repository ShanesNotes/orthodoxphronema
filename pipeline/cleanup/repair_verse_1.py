"""
repair_verse_1.py — Repair truncated Verse 1s in historical books.
"""

import re
import subprocess
from pathlib import Path
from pipeline.common.pdf_source import extract_pdf_text, estimate_chapter_page_range
from pipeline.common.paths import PDF_PATH, canon_filepath

REPO_ROOT = Path(__file__).parent.parent.parent
CANON_DIR = REPO_ROOT / "canon" / "OT"

def find_v1_text(book_code: str, ch: int) -> str:
    """Find the full text of Verse 1 by looking between Chapter digit and Verse 2."""
    try:
        start_p, end_p = estimate_chapter_page_range(book_code, ch)
    except:
        return ""
        
    # Extract text with layout to help identify verse digits
    text = extract_pdf_text(start_p, end_p + 1, PDF_PATH, layout=True)
    
    # 1. Find Chapter Digit 'ch'
    # Pattern: Digit on its own line or at start of line with large space
    ch_pattern = rf"(?:\n\s*|\n){ch}(?:\s+|\n)"
    match_ch = re.search(ch_pattern, text)
    if not match_ch:
        # try without layout if layout is messy
        text_plain = extract_pdf_text(start_p, end_p + 1, PDF_PATH, layout=False)
        match_ch = re.search(rf"\n{ch}\s+", text_plain)
        if not match_ch: return ""
        text = text_plain
        
    post_ch = text[match_ch.end():]
    
    # 2. Find Verse 2 Digit '2'
    # Pattern: ' 2' or '\n2 ' or footnote+2
    v2_pattern = r"(?:\s+|[†ω])2(?:\s+|[A-Z\"'])"
    match_v2 = re.search(v2_pattern, post_ch)
    if not match_v2:
        return ""
        
    v1_text = post_ch[:match_v2.start()].strip()
    
    # Clean up v1_text (newlines, extra spaces, OCR artifacts)
    v1_text = v1_text.replace("\n", " ")
    v1_text = re.sub(r'\s+', ' ', v1_text)
    
    return v1_text

def repair_book(book_code: str):
    file_path = canon_filepath("OT", book_code)
    if not file_path.exists(): return
    
    print(f"Repairing Verse 1s in {file_path.name}...")
    lines = file_path.read_text(encoding="utf-8").splitlines()
    modified = False
    new_lines = []
    
    for line in lines:
        m = re.match(r'^([A-Z0-9]{3})\.(\d+):1\s+(.*)', line)
        if m:
            b, ch, text = m.groups()
            ch = int(ch)
            
            # Check if Verse 1 looks truncated (short and no period)
            if len(text) < 100 and not any(text.strip().endswith(p) for p in ['.', '!', '?', '†']):
                print(f"  Attempting recovery for {b}.{ch}:1...")
                full_text = find_v1_text(b, ch)
                if full_text and len(full_text) > len(text):
                    print(f"    Recovered: {full_text[:50]}...")
                    line = f"{b}.{ch}:1 {full_text}"
                    modified = True
                else:
                    print(f"    Failed to find longer text in PDF.")
        
        new_lines.append(line)
        
    if modified:
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"  Successfully repaired {file_path.name}")

def process_all_books():
    print("Starting global Verse 1 structural repair...")
    for file_path in CANON_DIR.glob("*.md"):
        code = file_path.stem.split("_", 1)[1] if "_" in file_path.stem else file_path.stem
        repair_book(code)
    print("Global repair complete.")

if __name__ == "__main__":
    process_all_books()
