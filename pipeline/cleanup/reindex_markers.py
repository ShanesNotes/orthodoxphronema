"""
reindex_markers.py — Regenerate footnote marker JSON from validated Markdown.

Useful when markers were missed in initial Docling extraction or when
chapter boundaries were shifted manually.
"""

import argparse
import json
import re
from pathlib import Path
from datetime import date

def extract_markers_from_md(md_path: Path) -> list[dict]:
    content = md_path.read_text(encoding="utf-8")
    book_code = md_path.stem
    
    # Markers to find
    MARKERS = ["†ω", "†", "ω"]
    
    markers = []
    marker_seq_book = 0
    
    lines = content.splitlines()
    for line in lines:
        # Match verse: BOOK.CH:V Text
        m = re.match(r"^([A-Z0-9]{2,4})\.(\d+):(\d+)\s+(.*)", line)
        if m:
            b, ch, v, text = m.groups()
            anchor = f"{b}.{ch}:{v}"
            
            # Find markers in this verse
            # We look for all occurrences
            for marker in MARKERS:
                # We use regex to find the marker, avoiding overlaps (longest first)
                # But actually they are distinct characters.
                # Just find all occurrences of any of the marker strings
                pass
            
            # Simple approach: check for each marker type
            # Note: order matters if multiple markers in one verse
            # OSB usually has them at the end of phrases.
            
            # Find all markers in the text
            found = []
            for marker in ["†ω", "†", "ω"]:
                start = 0
                while True:
                    idx = text.find(marker, start)
                    if idx == -1: break
                    found.append((idx, marker))
                    start = idx + len(marker)
            
            # Sort by position in verse
            found.sort()
            
            for i, (idx, marker) in enumerate(found, 1):
                marker_seq_book += 1
                markers.append({
                    "marker": marker,
                    "anchor": anchor,
                    "marker_index_in_verse": i,
                    "marker_seq_book": marker_seq_book,
                    # We lose page/excerpt metadata here, but Photius can recover it if needed
                    "source": "reindexed_from_md"
                })
                
    return markers

def main():
    parser = argparse.ArgumentParser(description="Reindex markers from MD")
    parser.add_argument("md_file", type=Path, help="Path to BOOK.md")
    args = parser.parse_args()
    
    if not args.md_file.exists():
        print(f"Error: {args.md_file} not found")
        return
        
    markers = extract_markers_from_md(args.md_file)
    
    out_path = args.md_file.parent / f"{args.md_file.stem}_footnote_markers.json"
    
    data = {
        "book_code": args.md_file.stem,
        "reindex_date": str(date.today()),
        "marker_count": len(markers),
        "markers": markers
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"[reindex] Found {len(markers)} markers in {args.md_file.name}")
    print(f"[reindex] Updated {out_path.name}")

if __name__ == "__main__":
    main()
