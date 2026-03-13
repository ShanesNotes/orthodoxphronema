"""
generate_pericope_index.py — Build a pericope navigation index from a canon/staged book.

Contract:
  - Input: canon/ or staging/validated/ BOOK.md file
  - Detects narrative headings written as `### Heading`
  - Computes the exact anchor range each heading covers
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
from pipeline.common.patterns import RE_ANCHOR

DEFAULT_OUT_DIR = REPO_ROOT / "metadata" / "pericope_index"

RE_HEADING = re.compile(r"^### (.+)$")


def chapter_range(start_anchor: str | None, end_anchor: str | None) -> str | None:
    if start_anchor is None or end_anchor is None:
        return None
    _, start_cv = start_anchor.split(".", 1)
    _, end_cv = end_anchor.split(".", 1)
    start_ch = start_cv.split(":", 1)[0]
    end_ch = end_cv.split(":", 1)[0]
    return start_ch if start_ch == end_ch else f"{start_ch}-{end_ch}"


def extract_pericopes(path: Path) -> dict:
    path = path.resolve()
    lines = path.read_text(encoding="utf-8").splitlines()
    book_code = path.stem
    pericopes: list[dict] = []
    pending: dict | None = None
    last_anchor: str | None = None

    def close_pending() -> None:
        nonlocal pending
        if pending is None:
            return
        pending["end_anchor"] = last_anchor if pending["start_anchor"] is not None else None
        if pending["start_anchor"] is None or pending["end_anchor"] is None:
            pending["verse_count"] = 0
            pending["chapter_range"] = None
        else:
            start_bk, start_rest = pending["start_anchor"].split(".", 1)
            end_bk, end_rest = pending["end_anchor"].split(".", 1)
            start_ch, start_v = map(int, start_rest.split(":", 1))
            end_ch, end_v = map(int, end_rest.split(":", 1))
            if start_bk == end_bk and start_ch == end_ch:
                pending["verse_count"] = end_v - start_v + 1
            else:
                pending["verse_count"] = None
            pending["chapter_range"] = chapter_range(
                pending["start_anchor"], pending["end_anchor"]
            )
        pericopes.append(pending)
        pending = None

    for line in lines:
        m_heading = RE_HEADING.match(line)
        if m_heading:
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
        if pending is not None and pending["start_anchor"] is None:
            pending["start_anchor"] = anchor
        last_anchor = anchor
        book_code = m_anchor.group(1)

    close_pending()

    try:
        generated_from = str(path.relative_to(REPO_ROOT))
    except ValueError:
        generated_from = str(path)

    return {
        "book_code": book_code,
        "pericopes": pericopes,
        "generated_from": generated_from,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


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
