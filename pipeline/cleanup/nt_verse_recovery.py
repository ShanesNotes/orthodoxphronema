"""
nt_verse_recovery.py — Post-extraction verse-split recovery for NT books.

Scans each verse line for embedded verse numbers (digits followed by any text)
that V9 detects but the parser didn't split. Uses the book's CVC from the
registry to know expected verse counts and only splits at plausible boundaries.

Usage:
    python3 pipeline/cleanup/nt_verse_recovery.py staging/validated/NT/EPH.md --in-place
    python3 pipeline/cleanup/nt_verse_recovery.py staging/validated/NT/EPH.md --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
REGISTRY = REPO_ROOT / "schemas" / "anchor_registry.json"

# Pattern: digit(s) followed by a space and a letter (upper or lower).
# Requires word boundary before digit to avoid matching mid-number splits.
RE_EMBEDDED = re.compile(
    r'(?<=[.!?;:,\-\u2013\u2014"\'\u201d\u2019])\s+'  # punctuation before the digit
    r'(\d+)\s+'                            # verse number
    r'([A-Za-z])'                          # start of verse text
)

# Fallback: digit after space, followed by uppercase letter (no punct required)
RE_EMBEDDED_UC = re.compile(
    r'\s+(\d+)\s+([A-Z])'
)


def load_cvc(book_code: str) -> dict[int, int]:
    """Load chapter_verse_counts for a book from registry."""
    reg = json.loads(REGISTRY.read_text())
    for sec in ("books", "OT", "NT"):
        if sec in reg and book_code in reg[sec]:
            meta = reg[sec][book_code]
            break
    else:
        meta = reg.get(book_code, {})
    cvc_list = meta.get("chapter_verse_counts", [])
    return {i + 1: v for i, v in enumerate(cvc_list)}


def recover_verses(filepath: Path, dry_run: bool = False) -> int:
    """Scan file for embedded verses and split them out. Returns count of splits."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Detect book code from first anchor line
    book_code = None
    for line in lines:
        m = re.match(r'^([A-Z0-9]{2,4})\.\d+:\d+\s', line)
        if m:
            book_code = m.group(1)
            break
    if not book_code:
        print(f"  No anchors found in {filepath.name}", file=sys.stderr)
        return 0

    cvc = load_cvc(book_code)

    # Build set of existing anchors
    existing = set()
    for line in lines:
        m = re.match(r'^([A-Z0-9]{2,4}\.\d+:\d+)\s', line)
        if m:
            existing.add(m.group(1))

    new_lines = []
    total_splits = 0

    for line in lines:
        m = re.match(r'^([A-Z0-9]{2,4})\.(\d+):(\d+)\s+(.*)', line)
        if not m:
            new_lines.append(line)
            continue

        bc, ch_s, v_s, body = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        if ch_s == 0:
            new_lines.append(line)
            continue

        max_v = cvc.get(ch_s, 999)
        segments = _split_body(body, ch_s, v_s, max_v, bc, existing)

        if len(segments) <= 1:
            new_lines.append(line)
        else:
            for (seg_v, seg_text) in segments:
                anchor = f"{bc}.{ch_s}:{seg_v}"
                new_lines.append(f"{anchor} {seg_text}")
            total_splits += len(segments) - 1

    if total_splits > 0:
        result = "\n".join(new_lines) + "\n"
        if dry_run:
            print(f"  [dry-run] Would split {total_splits} verses in {filepath.name}")
        else:
            filepath.write_text(result, encoding="utf-8")
            print(f"  Split {total_splits} embedded verses in {filepath.name}")
    else:
        print(f"  No embedded verses found in {filepath.name}")

    return total_splits


def _split_body(body: str, ch: int, start_v: int, max_v: int,
                book_code: str, existing: set[str]) -> list[tuple[int, str]]:
    """Split a verse body at embedded verse number boundaries."""
    segments: list[tuple[int, str]] = []
    current_v = start_v
    current_text = body
    pos = 0

    while pos < len(current_text):
        # Try to find next embedded verse number
        best_match = None
        best_pos = len(current_text)

        for pattern in (RE_EMBEDDED, RE_EMBEDDED_UC):
            m = pattern.search(current_text, pos + 1)
            if m and m.start() < best_pos:
                vnum = int(m.group(1))
                # Must be a plausible verse number:
                # - Greater than current verse
                # - Within chapter's verse count
                # - Not already existing as a separate line (would be a dup)
                anchor = f"{book_code}.{ch}:{vnum}"
                if (vnum > current_v and vnum <= max_v
                        and anchor not in existing):
                    best_match = m
                    best_pos = m.start()

        if best_match is None:
            break

        # Split at this position
        vnum = int(best_match.group(1))
        before_text = current_text[:best_pos].rstrip()
        after_text = current_text[best_match.start():].lstrip()
        # Remove the verse number from the start of after_text
        after_text = re.sub(r'^\s*\d+\s+', '', after_text, count=1)

        if before_text:
            segments.append((current_v, before_text))

        current_v = vnum
        current_text = after_text
        pos = 0
        existing.add(f"{book_code}.{ch}:{vnum}")  # track so we don't split again

    if current_text.strip():
        segments.append((current_v, current_text.strip()))

    if len(segments) <= 1:
        return [(start_v, body)]  # no useful split found

    return segments


def main():
    parser = argparse.ArgumentParser(description="Recover embedded NT verses")
    parser.add_argument("files", nargs="+", help="Markdown files to process")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    total = 0
    for f in args.files:
        p = Path(f)
        if p.exists():
            total += recover_verses(p, dry_run=args.dry_run or not args.in_place)

    print(f"\nTotal splits: {total}")


if __name__ == "__main__":
    main()
