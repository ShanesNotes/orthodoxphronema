"""
refine_notes.py — Specialized cleanup and restructuring for non-Scripture content.

Tasks:
1. Split BOOK_notes.md into BOOK_articles.md and BOOK_footnotes.md.
2. Clean up drop-cap artifacts in study articles (e.g., "T he" -> "The").
3. Extract small annotations from the OSB PDF "Notes" section and save to BOOK_footnotes.md.
4. Normalize quotes, dashes, and whitespace.

Usage:
    python3 pipeline/cleanup/refine_notes.py --book GEN
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
# Must be at start of string or following a newline
RE_FN_ANCHOR = re.compile(r'^(\d+):(\d+)(?:-(\d+))?\s*(.*)')

# Regex for drop-cap re-joining in articles
RE_DROP_CAP = re.compile(r"^([']?\s*)([A-Z])\s+([a-z])")

def normalize_text(text: str) -> str:
    """Normalize OCR artifacts."""
    t = text.replace('\t', ' ')
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('‘', "'").replace('’', "'")
    t = t.replace('—', '--').replace('–', '-')
    t = re.sub(r' {2,}', ' ', t)
    return t.strip()

def fix_drop_caps(text: str) -> str:
    """Fix "T he" -> "The" etc."""
    lines = text.splitlines()
    fixed_lines = []
    for line in lines:
        fixed_lines.append(RE_DROP_CAP.sub(r"\1\2\3", line))
    return "\n".join(fixed_lines)

def extract_pdf_footnotes(book_code: str, start_page: int, end_page: int, max_chapters: int) -> list[dict]:
    """Extract footnotes from the OSB PDF using pdftotext."""
    cmd = ["pdftotext", "-f", str(start_page), "-l", str(end_page), str(PDF_PATH), "-"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []

    lines = result.stdout.splitlines()
    notes = []
    current_note = None
    last_ch = 0
    last_v = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = RE_FN_ANCHOR.match(line)
        if match:
            ch_num, v_start_num, v_end_num, body = match.groups()
            ch = int(ch_num)
            v_start = int(v_start_num)
            
            # 1. Book Boundary Check
            if ch > max_chapters:
                if current_note:
                    current_note["body_paras"].append(normalize_text(line))
                continue
                
            # 2. Monotonicity Check
            # OSB footnote anchors are strictly increasing.
            # References like "(see 3:14)" might match the regex if line-wrapped.
            if ch < last_ch or (ch == last_ch and v_start <= last_v):
                if current_note:
                    current_note["body_paras"].append(normalize_text(line))
                continue

            # Save previous note
            if current_note:
                notes.append(current_note)

            last_ch = ch
            last_v = v_start
            
            anchor = f"{book_code}.{ch}:{v_start}"
            anchor_display = f"{ch}:{v_start}-{v_end_num}" if v_end_num else f"{ch}:{v_start}"

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

def process_book(book_code: str):
    with open(REGISTRY) as f:
        registry = json.load(f)

    # 1. Determine testament and max chapters
    testament = "OT"
    max_chapters = 150
    for b in registry["books"]:
        if b["code"] == book_code:
            testament = b["testament"]
            max_chapters = b["chapters"]
            break

    book_dir = STAGING / testament
    notes_path = book_dir / f"{book_code}_notes.md"
    articles_path = book_dir / f"{book_code}_articles.md"
    
    if articles_path.exists() and not notes_path.exists():
        input_path = articles_path
    else:
        input_path = notes_path

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return

    print(f"Refining {book_code} non-Scripture content...")

    raw_content = input_path.read_text(encoding="utf-8")
    cleaned_content = fix_drop_caps(raw_content)
    cleaned_content = re.sub(r'content_type: study_articles', 'content_type: article', cleaned_content)
    cleaned_content = re.sub(r'source: ".*"', 'source: "OSB-v1"', cleaned_content)

    articles_path.write_text(cleaned_content, encoding="utf-8")
    if notes_path.exists() and notes_path != articles_path:
        notes_path.unlink()
    print(f"  Cleaned articles written to {articles_path}")

    if book_code in registry["page_ranges"]:
        fn_range = registry["page_ranges"][book_code]["footnotes"]
        if fn_range:
            notes = extract_pdf_footnotes(book_code, fn_range[0], fn_range[1], max_chapters)
            if notes:
                fn_md_path = book_dir / f"{book_code}_footnotes.md"
                frontmatter = f"""---
book_code: {book_code}
content_type: footnotes
source: "OSB-v1"
parse_date: "{date.today()}"
status: staging
---

## Footnotes
"""
                md_parts = [frontmatter]
                for n in notes:
                    md_parts.append(f"\n### {n['anchor_display']}")
                    md_parts.append(f"*(anchor: {n['anchor']})*\n")
                    md_parts.append("\n\n".join(n["body_paras"]))
                    md_parts.append("")
                
                fn_md_path.write_text("\n".join(md_parts), encoding="utf-8")
                print(f"  Extracted {len(notes)} footnotes to {fn_md_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refine OSB notes and articles")
    parser.add_argument("--book", required=True, help="Book code")
    args = parser.parse_args()
    process_book(args.book)
