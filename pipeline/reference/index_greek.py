"""
index_greek.py — Build verse-level JSON indexes from Greek source texts.

Reads schemas/greek_source_map.json and produces:
  staging/reference/greek/BOOK.json

Each output file has the shape:
  {
    "book_code": "GEN",
    "source": "Rahlfs LXX 1935",
    "script": "polytonic",
    "chapters": {
      "1": ["ἐν ἀρχῇ ἐποίησεν ὁ θεὸς ...", ...],
      ...
    }
  }

Usage:
    python3 pipeline/reference/index_greek.py GEN      # one OT book
    python3 pipeline/reference/index_greek.py MATT     # one NT book
    python3 pipeline/reference/index_greek.py --all    # all mapped books
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT

MAP_PATH = REPO_ROOT / "schemas" / "greek_source_map.json"
OUTPUT_DIR = REPO_ROOT / "staging" / "reference" / "greek"

# Strip inline morphology/Strong's markup from LXX SQLite text
RE_MARKUP = re.compile(r"<[^>]+>[^<]*</[^>]+>|<[^>]+>")


def load_map() -> dict:
    with open(MAP_PATH, encoding="utf-8") as f:
        return json.load(f)


def strip_markup(text: str) -> str:
    """Remove <S>...</S> and <m>...</m> tags, leaving just the Greek words."""
    clean = RE_MARKUP.sub("", text)
    # Collapse multiple spaces
    return re.sub(r"  +", " ", clean).strip()


def index_ot_book(book_code: str, entry: dict, source_map: dict) -> dict:
    """Index an OT book from the LXX SQLite database."""
    db_path = REPO_ROOT / source_map["sources"]["lxx"]["db_path"]
    book_num = entry["lxx_book_number"]

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        "SELECT chapter, verse, text FROM verses WHERE book_number=? ORDER BY chapter, verse",
        (book_num,),
    )

    chapters: dict[str, list[str]] = defaultdict(list)
    for ch, vs, text in cur.fetchall():
        chapters[str(ch)].append(strip_markup(text))

    conn.close()

    return {
        "book_code": book_code,
        "source": source_map["sources"]["lxx"]["name"],
        "script": source_map["sources"]["lxx"]["script"],
        "total_verses": sum(len(v) for v in chapters.values()),
        "total_chapters": len(chapters),
        "chapters": dict(sorted(chapters.items(), key=lambda x: int(x[0]))),
    }


def index_nt_book(book_code: str, entry: dict, source_map: dict) -> dict:
    """Index an NT book from the Antoniades plaintext files."""
    text_dir = REPO_ROOT / source_map["sources"]["antoniades"]["text_dir"]
    filepath = text_dir / entry["file"]

    chapters: dict[str, list[str]] = defaultdict(list)
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: "chapter:verse text..."
            m = re.match(r"(\d+):(\d+)\s+(.*)", line)
            if m:
                ch, _vs, text = m.group(1), m.group(2), m.group(3)
                chapters[ch].append(text.strip())

    return {
        "book_code": book_code,
        "source": source_map["sources"]["antoniades"]["name"],
        "script": source_map["sources"]["antoniades"]["script"],
        "total_verses": sum(len(v) for v in chapters.values()),
        "total_chapters": len(chapters),
        "chapters": dict(sorted(chapters.items(), key=lambda x: int(x[0]))),
    }


def index_book(book_code: str) -> Path:
    source_map = load_map()
    book_code = book_code.upper()

    if book_code in source_map["ot_books"]:
        entry = source_map["ot_books"][book_code]
        result = index_ot_book(book_code, entry, source_map)
    elif book_code in source_map["nt_books"]:
        entry = source_map["nt_books"][book_code]
        result = index_nt_book(book_code, entry, source_map)
    else:
        print(f"ERROR: {book_code} not found in greek_source_map.json", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{book_code}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[index_greek] {book_code}: {result['total_chapters']} chapters, "
          f"{result['total_verses']} verses → {out_path}")
    return out_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline/reference/index_greek.py BOOK [BOOK ...]")
        print("       python3 pipeline/reference/index_greek.py --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        source_map = load_map()
        codes = list(source_map["ot_books"].keys()) + list(source_map["nt_books"].keys())
    else:
        codes = [c.upper() for c in sys.argv[1:]]

    for code in codes:
        index_book(code)


if __name__ == "__main__":
    main()
