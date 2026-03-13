"""
frontmatter.py — YAML frontmatter parsing for canon Markdown files.
"""
from __future__ import annotations

import re

RE_FM_FIELD = re.compile(r'^(\w+):\s*(.+)')


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Parse YAML frontmatter from lines (between --- delimiters).

    Returns (frontmatter_dict, first_body_line_index).
    """
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fm: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        m = RE_FM_FIELD.match(lines[i])
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
        i += 1
    return fm, i + 1  # skip closing ---


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split file text into (frontmatter_block, body_text).

    frontmatter_block includes the opening and closing ---.
    body_text is everything after the closing ---.
    Returns ("", text) if no frontmatter delimiters found.
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

    fm_block = "".join(lines[:end_idx + 1])
    body = "".join(lines[end_idx + 1:])
    return fm_block, body


def update_frontmatter_field(text: str, field: str, value: str) -> str:
    """Update a single field in the frontmatter section.

    Replaces the first line matching `^field:` with `field: value`.
    """
    return re.sub(
        rf'^({re.escape(field)}:\s*).*$',
        rf'\g<1>{value}',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def update_frontmatter(fm_block: str, promote_date: str, checksum: str) -> str:
    """Update promote_date, status, and checksum in a frontmatter block."""
    updated = update_frontmatter_field(fm_block, "promote_date", f'"{promote_date}"')
    updated = update_frontmatter_field(updated, "status", "promoted")
    updated = update_frontmatter_field(updated, "checksum", f'"{checksum}"')
    return updated
