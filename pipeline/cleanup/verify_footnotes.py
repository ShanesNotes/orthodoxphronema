"""
verify_footnotes.py — Verify that footnote anchors in notes files match markers in Scripture.

Usage:
    python3 pipeline/cleanup/verify_footnotes.py --book GEN
"""

import argparse
import json
import re
import sys
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import STAGING_ROOT, REGISTRY_PATH
from pipeline.common.registry import book_testament, chapter_verse_counts, load_registry

STAGING = STAGING_ROOT
ANCHOR_RE = re.compile(r"^([A-Z0-9]+)\.(\d+):(\d+)$")
VERSE_LINE_RE = re.compile(r"^([A-Z0-9]+\.\d+:\d+)\s+")

def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def extract_anchors_from_md(path: Path) -> set[str]:
    content = path.read_text(encoding="utf-8")
    # Match *(anchor: GEN.1:1)*
    return set(re.findall(r'\(anchor: ([A-Z0-9]+\.\d+:\d+)\)', content))


def extract_scripture_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = VERSE_LINE_RE.match(line)
        if match:
            anchors.add(match.group(1))
    return anchors


def anchor_registry_error(anchor: str, book_code: str, cvc: dict[int, int] | None) -> str | None:
    match = ANCHOR_RE.match(anchor)
    if not match:
        return "malformed_anchor"
    book, ch_s, v_s = match.groups()
    if book != book_code:
        return "wrong_book_code"
    if cvc is None:
        return None
    chapter = int(ch_s)
    verse = int(v_s)
    if chapter not in cvc:
        return "invalid_chapter"
    if verse < 1 or verse > cvc[chapter]:
        return "invalid_verse"
    return None


def partition_anchors(
    anchors: set[str],
    book_code: str,
    cvc: dict[int, int] | None,
) -> tuple[set[str], dict[str, str]]:
    valid: set[str] = set()
    invalid: dict[str, str] = {}
    for anchor in anchors:
        error = anchor_registry_error(anchor, book_code, cvc)
        if error is None:
            valid.add(anchor)
        else:
            invalid[anchor] = error
    return valid, invalid

def verify_book(book_code: str):
    registry = load_registry(REGISTRY_PATH)
    testament = book_testament(registry, book_code)
    markers_path = STAGING / testament / f"{book_code}_footnote_markers.json"
    notes_path   = STAGING / testament / f"{book_code}_footnotes.md"
    scripture_path = STAGING / testament / f"{book_code}.md"

    if not markers_path.exists():
        print(f"Error: {markers_path} not found")
        return 1
    if not notes_path.exists():
        print(f"Error: {notes_path} not found")
        return 1
    if not scripture_path.exists():
        print(f"Error: {scripture_path} not found")
        return 1

    markers_data = load_json(markers_path)
    if isinstance(markers_data, list):
        marker_anchors = {m["anchor"] for m in markers_data}
    else:
        marker_anchors = {m["anchor"] for m in markers_data["markers"]}
    note_anchors = extract_anchors_from_md(notes_path)
    scripture_anchors = extract_scripture_anchors(scripture_path)
    cvc = chapter_verse_counts(registry, book_code)

    valid_marker_anchors, invalid_marker_anchors = partition_anchors(marker_anchors, book_code, cvc)
    valid_note_anchors, invalid_note_anchors = partition_anchors(note_anchors, book_code, cvc)

    print(f"Verifying {book_code} footnotes...")
    print(f"  Scripture markers : {len(marker_anchors)}")
    print(f"  Footnote entries  : {len(note_anchors)}")
    print(f"  Scripture anchors : {len(scripture_anchors)}")

    missing_in_notes = valid_marker_anchors - valid_note_anchors
    missing_in_scripture = valid_note_anchors - valid_marker_anchors
    marker_anchor_gaps = valid_marker_anchors - scripture_anchors
    note_anchor_gaps = valid_note_anchors - scripture_anchors

    issue_count = 0

    if invalid_marker_anchors:
        issue_count += len(invalid_marker_anchors)
        print(f"\nERROR: {len(invalid_marker_anchors)} marker anchor(s) are invalid by registry:")
        for anchor, reason in sorted(invalid_marker_anchors.items())[:10]:
            print(f"  - {anchor} ({reason})")
        if len(invalid_marker_anchors) > 10:
            print(f"  ... and {len(invalid_marker_anchors)-10} more")

    if invalid_note_anchors:
        issue_count += len(invalid_note_anchors)
        print(f"\nERROR: {len(invalid_note_anchors)} footnote anchor(s) are invalid by registry:")
        for anchor, reason in sorted(invalid_note_anchors.items())[:10]:
            print(f"  - {anchor} ({reason})")
        if len(invalid_note_anchors) > 10:
            print(f"  ... and {len(invalid_note_anchors)-10} more")

    if missing_in_notes:
        issue_count += len(missing_in_notes)
        print(f"\nWARNING: {len(missing_in_notes)} markers in Scripture have no corresponding footnote:")
        for a in sorted(list(missing_in_notes))[:10]:
            print(f"  - {a}")
        if len(missing_in_notes) > 10:
            print(f"  ... and {len(missing_in_notes)-10} more")

    if missing_in_scripture:
        issue_count += len(missing_in_scripture)
        print(f"\nWARNING: {len(missing_in_scripture)} footnotes in section have no marker in Scripture:")
        for a in sorted(list(missing_in_scripture))[:10]:
            print(f"  - {a}")
        if len(missing_in_scripture) > 10:
            print(f"  ... and {len(missing_in_scripture)-10} more")

    if marker_anchor_gaps:
        issue_count += len(marker_anchor_gaps)
        print(f"\nERROR: {len(marker_anchor_gaps)} marker anchor(s) do not exist in staged Scripture:")
        for a in sorted(list(marker_anchor_gaps))[:10]:
            print(f"  - {a}")
        if len(marker_anchor_gaps) > 10:
            print(f"  ... and {len(marker_anchor_gaps)-10} more")

    if note_anchor_gaps:
        issue_count += len(note_anchor_gaps)
        print(f"\nERROR: {len(note_anchor_gaps)} footnote anchor(s) do not exist in staged Scripture:")
        for a in sorted(list(note_anchor_gaps))[:10]:
            print(f"  - {a}")
        if len(note_anchor_gaps) > 10:
            print(f"  ... and {len(note_anchor_gaps)-10} more")

    if issue_count == 0:
        print("\nPASS: All anchors match perfectly.")
        return 0

    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify OSB footnotes")
    parser.add_argument("--book", required=True, help="Book code (e.g. GEN)")
    args = parser.parse_args()
    sys.exit(verify_book(args.book))
