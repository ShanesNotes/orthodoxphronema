"""
extract_footnotes.py — Extract annotations from the OSB PDF "Notes" section.

Usage:
    python3 pipeline/cleanup/extract_footnotes.py --book GEN
"""

import argparse
import json
import re
import subprocess
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).parent.parent.parent
PDF_PATH  = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
REGISTRY  = REPO_ROOT / "schemas" / "anchor_registry.json"
STAGING   = REPO_ROOT / "staging" / "validated"

# Regex for footnote anchor: "1:1 " or "1:4-25 " at start of line
# Note: OSB sometimes has a space or newline after the anchor.
RE_ANCHOR = re.compile(r'^(\d+):(\d+)(?:-(\d+))?\s*(.*)')

def normalize_text(text: str) -> str:
    """Normalize OCR artifacts."""
    t = text.replace('\t', ' ')
    # Normalize quotes
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('‘', "'").replace('’', "'")
    # Normalize dashes
    t = t.replace('—', '--').replace('–', '-')
    # Collapse whitespace
    t = re.sub(r' {2,}', ' ', t)
    return t.strip()

def parse_footnotes(text: str, book_code: str) -> list[dict]:
    lines = text.splitlines()
    notes = []
    current_note = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = RE_ANCHOR.match(line)
        if match:
            # Save previous note
            if current_note:
                notes.append(current_note)

            ch, v_start, v_end, body = match.groups()
            anchor = f"{book_code}.{ch}:{v_start}"
            if v_end:
                # We record the range but use the start-verse as primary anchor
                anchor_display = f"{ch}:{v_start}-{v_end}"
            else:
                anchor_display = f"{ch}:{v_start}"

            current_note = {
                "anchor": anchor,
                "anchor_display": anchor_display,
                "body_paras": [normalize_text(body)] if body.strip() else []
            }
        elif current_note:
            current_note["body_paras"].append(normalize_text(line))

    if current_note:
        notes.append(current_note)

    return notes

def main():
    parser = argparse.ArgumentParser(description="Extract OSB footnotes")
    parser.add_argument("--book", required=True, help="Book code (e.g. GEN)")
    args = parser.parse_args()

    with open(REGISTRY) as f:
        registry = json.load(f)

    if args.book not in registry["page_ranges"]:
        print(f"Error: {args.book} not found in registry page_ranges")
        return

    fn_range = registry["page_ranges"][args.book]["footnotes"]
    start, end = fn_range

    print(f"[extract] Extracting {args.book} footnotes from pages {start}-{end}...")
    
    cmd = ["pdftotext", "-f", str(start), "-l", str(end), str(PDF_PATH), "-"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running pdftotext: {result.stderr}")
        return

    notes = parse_footnotes(result.stdout, args.book)
    print(f"[extract] Found {len(notes)} footnote entries.")

    # Build Markdown
    testament = "OT" # Default, could be looked up
    for b in registry["books"]:
        if b["code"] == args.book:
            testament = b["testament"]
            break

    out_path = STAGING / testament / f"{args.book}_footnotes.md"
    
    frontmatter = f"""---
book_code: {args.book}
content_type: footnotes
source: "OSB-v1"
parse_date: "{date.today()}"
status: staging
---

## Footnotes
"""
    
    md_content = [frontmatter]
    for n in notes:
        md_content.append(f"\n### {n['anchor_display']}")
        md_content.append(f"*(anchor: {n['anchor']})*\n")
        md_content.append("\n\n".join(n["body_paras"]))
        md_content.append("")

    out_path.write_text("\n".join(md_content), encoding="utf-8")
    print(f"[extract] Written to {out_path}")

if __name__ == "__main__":
    main()
