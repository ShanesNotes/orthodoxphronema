#!/usr/bin/env python3
"""
normalize_companion_frontmatter.py
Normalize YAML frontmatter in all companion *_articles.md files.

Fixes applied:
  1. content_type: study_articles  ->  article
  2. source: (long-form)           ->  "OSB-v1"
  3. status: staged                ->  staging
  4. NT article files: add missing book_name, promote_date, canon_anchors_referenced
"""
from __future__ import annotations

import argparse
import sys as _sys
from pathlib import Path as _Path

import yaml

# ── repo-root bootstrap ──────────────────────────────────────────────────────
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.paths import STAGING_ROOT, REGISTRY_PATH  # noqa: E402
from pipeline.common.registry import load_registry, book_meta, book_testament  # noqa: E402

CANONICAL_SOURCE = "OSB-v1"

# ── YAML helpers ─────────────────────────────────────────────────────────────

def _split_frontmatter(text: str) -> tuple[str, str]:
    """Return (yaml_string_between_fences, body_after_closing_fence).

    If the file does not start with ``---``, returns ("", text).
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return "", text

    yaml_str = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1:])
    return yaml_str, body


def _rebuild(fm: dict, body: str) -> str:
    """Re-serialize frontmatter dict + body into a complete file string."""
    dumped = yaml.safe_dump(
        fm,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    return f"---\n{dumped}---\n{body}"


# ── normalization logic ──────────────────────────────────────────────────────

def normalize(path: _Path, registry: dict) -> tuple[str | None, list[str]]:
    """Return (new_text | None, list_of_change_descriptions).

    Returns None as first element when no changes are needed.
    """
    text = path.read_text(encoding="utf-8")
    yaml_str, body = _split_frontmatter(text)
    if not yaml_str:
        return None, []

    fm: dict = yaml.safe_load(yaml_str)
    if fm is None:
        return None, []

    changes: list[str] = []

    # Derive book code from filename (e.g. PSA_articles.md -> PSA)
    code = path.stem.split("_")[0]

    # 1. content_type: study_articles -> article
    if fm.get("content_type") == "study_articles":
        fm["content_type"] = "article"
        changes.append("content_type: study_articles -> article")

    # 2. source: long-form -> "OSB-v1"
    src = fm.get("source", "")
    if src and src != CANONICAL_SOURCE:
        fm["source"] = CANONICAL_SOURCE
        changes.append(f"source: {src!r} -> {CANONICAL_SOURCE!r}")

    # 3. status: staged -> staging
    if fm.get("status") == "staged":
        fm["status"] = "staging"
        changes.append("status: staged -> staging")

    # 4. Add missing fields for NT article files
    testament = book_testament(registry, code)
    if testament == "NT":
        if "book_name" not in fm:
            meta = book_meta(registry, code)
            book_name = meta.get("name", code)
            # Insert book_name right after book_code by rebuilding ordered dict
            new_fm: dict = {}
            for k, v in fm.items():
                new_fm[k] = v
                if k == "book_code":
                    new_fm["book_name"] = book_name
            fm = new_fm
            changes.append(f"add book_name: {book_name!r}")

        if "promote_date" not in fm:
            # Insert promote_date after parse_date
            new_fm = {}
            for k, v in fm.items():
                new_fm[k] = v
                if k == "parse_date":
                    new_fm["promote_date"] = None
            fm = new_fm
            changes.append("add promote_date: null")

        if "canon_anchors_referenced" not in fm:
            fm["canon_anchors_referenced"] = []
            changes.append("add canon_anchors_referenced: []")

    if not changes:
        return None, []

    return _rebuild(fm, body), changes


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize YAML frontmatter in companion article files.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes (default is dry-run).",
    )
    args = parser.parse_args()
    dry_run = not args.apply

    registry = load_registry()

    article_files = sorted(STAGING_ROOT.rglob("*_articles.md"))
    total_changed = 0

    for path in article_files:
        new_text, changes = normalize(path, registry)
        if new_text is None:
            continue
        total_changed += 1
        rel = path.relative_to(STAGING_ROOT)
        tag = "[DRY-RUN]" if dry_run else "[APPLY]"
        print(f"{tag} {rel}")
        for c in changes:
            print(f"       {c}")
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")

    mode = "dry-run" if dry_run else "applied"
    print(f"\n--- {total_changed} file(s) would be changed ({mode}) ---")


if __name__ == "__main__":
    main()
