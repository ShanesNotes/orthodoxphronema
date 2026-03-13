"""
recover_markers.py — Systematically recover footnote markers from PDF to Markdown.

1. Reads page range from registry.
2. Extracts text with markers from PDF.
3. Finds matching verse in Markdown.
4. Re-inserts markers.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PDF_PATH  = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
REGISTRY  = REPO_ROOT / "schemas" / "anchor_registry.json"

def clean_for_match(text: str) -> str:
    """Clean text to improve matching between PDF and MD."""
    # Remove markers, verse numbers, and normalize whitespace
    t = re.sub(r'[†ω]', '', text)
    t = re.sub(r'^\d+', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def recover_for_book(book_code: str, md_path: Path):
    with open(REGISTRY) as f:
        registry = json.load(f)
        
    if book_code not in registry["page_ranges"]:
        print(f"Error: {book_code} not found in registry")
        return
        
    txt_range = registry["page_ranges"][book_code]["text"]
    start, end = txt_range
    
    print(f"[recover] Extracting markers for {book_code} from PDF pages {start}-{end}...")
    cmd = ["pdftotext", "-f", str(start), "-l", str(end), str(PDF_PATH), "-"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return
        
    pdf_text = result.stdout
    
    # We want to find sentences ending in markers or having markers
    # OSB markers are usually at the end of a phrase or verse.
    
    # Pattern to find marker and some preceding text
    # e.g. "some text here.†"
    RE_MARKER_CONTEXT = re.compile(r'([^.!?]{5,20}[.!?]?\s*)([†ω]+)')
    
    matches = RE_MARKER_CONTEXT.findall(pdf_text)
    print(f"[recover] Found {len(matches)} marker contexts in PDF.")
    
    md_content = md_path.read_text(encoding="utf-8")
    lines = md_content.splitlines()
    
    recovered_count = 0
    for context, markers in matches:
        clean_context = clean_for_match(context)
        if not clean_context: continue
        
        # Search for this context in md lines
        found = False
        for i, line in enumerate(lines):
            # Only match verse lines
            if not re.match(r"^[A-Z0-9]{2,4}\.\d+:", line):
                continue
                
            clean_line = clean_for_match(line)
            if clean_context in clean_line:
                # Check if markers already there
                if markers in lines[i]:
                    found = True
                    break
                
                # Insert markers after the context
                # We need to find the exact spot in the original line
                # But md line might have single quotes, pdf has double.
                # Just find the phrase and append markers.
                
                # Try a fuzzy find/replace on this line
                pattern = re.escape(context.strip()).replace(r'\"', '[\'"]').replace(r"\'", '[\'"]')
                # Note: this is getting complex. 
                # Simpler: just append to the line if the line matches the anchor we expect.
                
                # Actually, let's just report the match for now to see if it works.
                # print(f"  Match: {line[:30]}... -> {markers}")
                
                # Better: Use the anchor found in the PDF if possible.
                # But pdftotext doesn't always have clean anchor lines.
                
                # Let's try to just insert it into the line
                # Find the phrase in the line
                # We'll normalize both for the search
                pass
        
    print("[recover] Logic needs refinement for robust insertion. Use reindex_markers.py for now after manual/semi-auto insertion.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recover markers from PDF")
    parser.add_argument("--book", required=True)
    parser.add_argument("--md", type=Path, required=True)
    args = parser.parse_args()
    recover_for_book(args.book, args.md)
