"""
dropcap_verify.py — Detect and classify drop-cap omissions in staged canon files.

Docling does NOT expose per-element page numbers, so PDF re-probe cannot
recover the missing glyph. This script uses heuristic pattern matching on
verse-1 text residuals to propose single-letter repairs.

Usage:
    python3 dropcap_verify.py staging/validated/OT/GEN.md          # generate candidates JSON
    python3 dropcap_verify.py staging/validated/OT/GEN.md --apply  # apply after human ratification
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RE_VERSE_LINE = re.compile(r'^([A-Z0-9]+\.\d+:\d+) (.+)')

# Heuristic repair table: residual prefix -> (repair_prefix, classification)
# "confirmed_auto" = unambiguous single-letter prepend
# "ambiguous_human" = multiple possibilities, needs human decision
REPAIR_TABLE: list[tuple[str, str, str]] = [
    # residual_start, repaired_start, classification
    ("nthe ", "In the ", "confirmed_auto"),
    ("oearly ", "So early ", "confirmed_auto"),
    ("tcame ", "It came ", "confirmed_auto"),

    # T-prefix residuals
    ("hen ", "Then ", "confirmed_auto"),
    ("hus ", "Thus ", "confirmed_auto"),
    ("his ", "This ", "confirmed_auto"),

    # N-prefix residuals
    ("ow ", "Now ", "confirmed_auto"),

    # A-prefix residuals
    ("fter ", "After ", "confirmed_auto"),
    ("nd ", "And ", "confirmed_auto"),

    # S-prefix residuals
    ("o ", "So ", "ambiguous_human"),  # could be "No" — needs context
]


def classify_dropcap(anchor: str, text: str) -> dict | None:
    """Classify a verse line's drop-cap residual. Returns candidate dict or None."""
    # Only chapter X verse 1 should have drop-caps
    if not re.match(r'^[A-Z0-9]+\.\d+:1$', anchor):
        return None

    # Must start lowercase
    if not text or not text[0].islower():
        return None

    for residual, repair, classification in REPAIR_TABLE:
        if text.startswith(residual):
            repaired = repair + text[len(residual):]
            return {
                "anchor": anchor,
                "residual": text[:50],
                "proposed_repair": repaired[:80],
                "missing_letter": repair[0],
                "classification": classification,
            }

    # No match — ambiguous
    return {
        "anchor": anchor,
        "residual": text[:50],
        "proposed_repair": None,
        "missing_letter": None,
        "classification": "ambiguous_human",
    }


def scan_file(path: Path) -> list[dict]:
    """Scan a canon file for drop-cap candidates."""
    candidates = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = RE_VERSE_LINE.match(line)
        if not m:
            continue
        anchor, text = m.group(1), m.group(2)
        result = classify_dropcap(anchor, text)
        if result:
            candidates.append(result)
    return candidates


def apply_repairs(path: Path, candidates_path: Path) -> int:
    """Apply ratified repairs from the candidates JSON to the canon file."""
    with open(candidates_path, encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("ratified"):
        print("ERROR: candidates JSON does not have \"ratified\": true", file=sys.stderr)
        print("Human must review and set ratified before --apply is safe.", file=sys.stderr)
        sys.exit(1)

    # Build repair map: anchor -> repaired text prefix
    repairs: dict[str, str] = {}
    for c in data.get("candidates", []):
        if c["classification"] == "confirmed_auto" and c.get("proposed_repair"):
            repairs[c["anchor"]] = c["missing_letter"]
        elif c["classification"] == "human_verified" and c.get("missing_letter"):
            repairs[c["anchor"]] = c["missing_letter"]

    if not repairs:
        print("No applicable repairs found in candidates JSON.")
        return 0

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    count = 0
    new_lines = []
    for line in lines:
        m = RE_VERSE_LINE.match(line.rstrip("\n"))
        if m and m.group(1) in repairs:
            anchor = m.group(1)
            text = m.group(2)
            letter = repairs[anchor]
            # Prepend the missing letter
            if text[0].islower():
                # Handle special cases where letter + residual needs spacing
                if letter.upper() + text[0:] != letter.upper() + text:
                    new_text = letter.upper() + text
                else:
                    new_text = letter.upper() + text
                new_lines.append(f"{anchor} {new_text}\n")
                count += 1
                continue
        new_lines.append(line)

    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Applied {count} drop-cap repairs to {path}")
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Detect and classify drop-cap omissions in staged canon files."
    )
    parser.add_argument("path", type=Path, help="Staged canon .md file")
    parser.add_argument("--apply", action="store_true",
                        help="Apply repairs from ratified candidates JSON")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"File not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    book_code = args.path.stem
    candidates_path = args.path.with_name(f"{book_code}_dropcap_candidates.json")

    if args.apply:
        if not candidates_path.exists():
            print(f"Candidates file not found: {candidates_path}", file=sys.stderr)
            sys.exit(1)
        apply_repairs(args.path, candidates_path)
        return

    # Scan mode
    candidates = scan_file(args.path)

    output = {
        "book_code": book_code,
        "total_candidates": len(candidates),
        "confirmed_auto": sum(1 for c in candidates if c["classification"] == "confirmed_auto"),
        "ambiguous_human": sum(1 for c in candidates if c["classification"] == "ambiguous_human"),
        "ratified": False,
        "candidates": candidates,
    }

    candidates_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"Wrote: {candidates_path}")
    print(f"  Total candidates: {output['total_candidates']}")
    print(f"  confirmed_auto:   {output['confirmed_auto']}")
    print(f"  ambiguous_human:  {output['ambiguous_human']}")
    print(f"\nHuman must review, then set \"ratified\": true before --apply.")


if __name__ == "__main__":
    main()
