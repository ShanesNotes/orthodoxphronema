"""
generate_pericope_index.py — Build a pericope navigation index from a canon/staged book.

Contract:
  - Input: canon/ or staging/validated/ BOOK.md file
  - Detects narrative headings written as `### Heading`
  - Collects pre-heading verses into a synthetic preamble pericope
  - Falls back to chapter-level pericopes for uncovered ranges
  - Computes accurate cross-chapter verse counts via CVC data
  - Writes metadata/pericope_index/BOOK.json by default
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import re

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT
from pipeline.common.patterns import RE_ANCHOR, RE_CHAPTER_HDR
from pipeline.common.registry import load_registry, book_meta, chapter_verse_counts

DEFAULT_OUT_DIR = REPO_ROOT / "metadata" / "pericope_index"

RE_HEADING = re.compile(r"^### (.+)$")


def _chapter_range(start_anchor: str | None, end_anchor: str | None) -> str | None:
    if start_anchor is None or end_anchor is None:
        return None
    _, start_cv = start_anchor.split(".", 1)
    _, end_cv = end_anchor.split(".", 1)
    start_ch = start_cv.split(":", 1)[0]
    end_ch = end_cv.split(":", 1)[0]
    return start_ch if start_ch == end_ch else f"{start_ch}-{end_ch}"


def _compute_verse_count(
    start_anchor: str | None,
    end_anchor: str | None,
    cvc: dict[int, int] | None,
) -> int | None:
    """Compute verse count using CVC data for cross-chapter ranges."""
    if start_anchor is None or end_anchor is None:
        return 0
    _, start_rest = start_anchor.split(".", 1)
    _, end_rest = end_anchor.split(".", 1)
    start_ch, start_v = map(int, start_rest.split(":", 1))
    end_ch, end_v = map(int, end_rest.split(":", 1))
    if start_ch == end_ch:
        return end_v - start_v + 1
    if cvc is None:
        return None
    # remaining verses in start chapter + full intermediate chapters + used in end chapter
    total = cvc.get(start_ch, start_v) - start_v + 1
    for ch in range(start_ch + 1, end_ch):
        total += cvc.get(ch, 0)
    total += end_v
    return total


def _make_pericope(title: str, start_anchor: str | None, end_anchor: str | None,
                   cvc: dict[int, int] | None) -> dict:
    return {
        "title": title,
        "start_anchor": start_anchor,
        "end_anchor": end_anchor,
        "verse_count": _compute_verse_count(start_anchor, end_anchor, cvc),
        "chapter_range": _chapter_range(start_anchor, end_anchor),
        "notes_anchors": [],
        "source_companions": [],
        "cross_ref_candidates": [],
        "liturgical_context": None,
        "alt_versification": None,
        "embedding_status": "pending",
        "provenance": None,
    }


def extract_pericopes(path: Path, registry: dict | None = None) -> dict:
    path = path.resolve()
    lines = path.read_text(encoding="utf-8").splitlines()

    # Resolve book_code from first anchor encountered
    book_code = path.stem
    # Strip position prefix (e.g. "01_GEN" -> "GEN")
    if "_" in book_code:
        book_code = book_code.split("_", 1)[1]

    # Load registry for CVC and book name
    if registry is None:
        registry = load_registry()
    try:
        meta = book_meta(registry, book_code)
        book_name = meta["name"]
    except ValueError:
        book_name = book_code
    cvc = chapter_verse_counts(registry, book_code)

    pericopes: list[dict] = []
    preamble_anchors: list[str] = []
    pending: dict | None = None
    last_anchor: str | None = None
    first_heading_seen = False

    def close_pending() -> None:
        nonlocal pending
        if pending is None:
            return
        pending["end_anchor"] = last_anchor if pending["start_anchor"] is not None else None
        pending["verse_count"] = _compute_verse_count(
            pending["start_anchor"], pending["end_anchor"], cvc
        )
        if pending["start_anchor"] is None or pending["end_anchor"] is None:
            pending["chapter_range"] = None
        else:
            pending["chapter_range"] = _chapter_range(
                pending["start_anchor"], pending["end_anchor"]
            )
        pericopes.append(pending)
        pending = None

    for line in lines:
        m_heading = RE_HEADING.match(line)
        if m_heading:
            # Phase 1A: close preamble on first heading
            if not first_heading_seen and preamble_anchors:
                pericopes.append(_make_pericope(
                    f"{book_name} \u2014 Opening",
                    preamble_anchors[0],
                    preamble_anchors[-1],
                    cvc,
                ))
            first_heading_seen = True
            close_pending()
            pending = {
                "title": m_heading.group(1).strip(),
                "start_anchor": None,
                "end_anchor": None,
                "verse_count": None,
                "chapter_range": None,
                "notes_anchors": [],
                "source_companions": [],
                "cross_ref_candidates": [],
                "liturgical_context": None,
                "alt_versification": None,
                "embedding_status": "pending",
                "provenance": None,
            }
            continue

        m_anchor = RE_ANCHOR.match(line)
        if not m_anchor:
            continue
        anchor = f"{m_anchor.group(1)}.{int(m_anchor.group(2))}:{int(m_anchor.group(3))}"

        if not first_heading_seen:
            # Phase 1A: collect pre-heading anchors
            preamble_anchors.append(anchor)
        else:
            if pending is not None and pending["start_anchor"] is None:
                pending["start_anchor"] = anchor
        last_anchor = anchor
        book_code = m_anchor.group(1)

    close_pending()

    # Phase 1A: if no headings at all, preamble_anchors has everything
    # but we don't emit it here — fill_chapter_gaps handles heading-less books
    if not first_heading_seen and preamble_anchors:
        # No headings found; pericopes list is empty.
        # fill_chapter_gaps will create chapter-level pericopes.
        pass

    try:
        generated_from = str(path.relative_to(REPO_ROOT))
    except ValueError:
        generated_from = str(path)

    # Phase 1B: fill chapter gaps
    pericopes = fill_chapter_gaps(pericopes, path, book_code, book_name, cvc)

    return {
        "book_code": book_code,
        "pericopes": pericopes,
        "generated_from": generated_from,
        "generated_at": datetime.fromtimestamp(
            path.stat().st_mtime, timezone.utc
        ).replace(microsecond=0).isoformat(),
    }


def _parse_anchor(anchor: str) -> tuple[str, int, int]:
    """Parse 'BOOK.CH:V' into (book, chapter, verse)."""
    book, rest = anchor.split(".", 1)
    ch, v = rest.split(":", 1)
    return book, int(ch), int(v)


def _scan_chapters(path: Path) -> dict[int, tuple[str, str]]:
    """Scan a canon file and return {chapter_num: (first_anchor, last_anchor)}."""
    lines = path.read_text(encoding="utf-8").splitlines()
    chapters: dict[int, tuple[str | None, str | None]] = {}
    current_ch: int | None = None
    for line in lines:
        m_ch = RE_CHAPTER_HDR.match(line)
        if m_ch:
            current_ch = int(m_ch.group(1))
            continue
        m_anchor = RE_ANCHOR.match(line)
        if m_anchor:
            anchor = f"{m_anchor.group(1)}.{int(m_anchor.group(2))}:{int(m_anchor.group(3))}"
            ch_from_anchor = int(m_anchor.group(2))
            ch_key = ch_from_anchor
            if ch_key not in chapters:
                chapters[ch_key] = (anchor, anchor)
            else:
                chapters[ch_key] = (chapters[ch_key][0], anchor)
    return {k: v for k, v in chapters.items() if v[0] is not None}


def fill_chapter_gaps(
    pericopes: list[dict],
    path: Path,
    book_code: str,
    book_name: str,
    cvc: dict[int, int] | None,
) -> list[dict]:
    """Fill uncovered chapter ranges with chapter-level pericopes.

    For heading-less books (PSA, PRO, etc.), every chapter becomes its own pericope.
    For books with sparse headings, gaps between heading-based pericopes are filled.
    PSA special case: each chapter is titled "Psalm N" (the natural liturgical unit).
    """
    chapter_map = _scan_chapters(path)
    if not chapter_map:
        return pericopes

    all_chapters = sorted(chapter_map.keys())

    # If no heading-based pericopes, create one per chapter
    if not pericopes:
        result = []
        for ch in all_chapters:
            first, last = chapter_map[ch]
            if book_code == "PSA":
                title = f"Psalm {ch}"
            else:
                title = f"{book_name} \u2014 Chapter {ch}"
            result.append(_make_pericope(title, first, last, cvc))
        return result

    # Build a set of covered chapters from existing pericopes
    covered_chapters: set[int] = set()
    for p in pericopes:
        if p["start_anchor"] is None or p["end_anchor"] is None:
            continue
        _, s_ch, _ = _parse_anchor(p["start_anchor"])
        _, e_ch, _ = _parse_anchor(p["end_anchor"])
        for ch in range(s_ch, e_ch + 1):
            covered_chapters.add(ch)

    # Find uncovered chapters and insert chapter-level pericopes
    uncovered = [ch for ch in all_chapters if ch not in covered_chapters]
    if not uncovered:
        return pericopes

    # Build synthetic pericopes for uncovered chapters
    synthetics: list[dict] = []
    for ch in uncovered:
        if ch not in chapter_map:
            continue
        first, last = chapter_map[ch]
        if book_code == "PSA":
            title = f"Psalm {ch}"
        else:
            title = f"{book_name} \u2014 Chapter {ch}"
        synthetics.append(_make_pericope(title, first, last, cvc))

    # Merge: sort all pericopes by start_anchor
    merged = pericopes + synthetics
    merged.sort(key=lambda p: _parse_anchor(p["start_anchor"]) if p["start_anchor"] else ("", 0, 0))
    return merged


def write_pericope_index(path: Path, out_dir: Path = DEFAULT_OUT_DIR) -> Path:
    payload = extract_pericopes(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{payload['book_code']}.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a pericope index from a staged/promoted book."
    )
    parser.add_argument("path", type=Path, help="Path to BOOK.md")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR})",
    )
    args = parser.parse_args()

    out_path = write_pericope_index(args.path, args.out_dir)
    print(out_path)


if __name__ == "__main__":
    main()
