"""
nt_dedup_merge.py — Merge duplicate anchor lines in NT staging files.

When the extractor emits the same verse twice (e.g., from column splits),
this script merges them by appending the shorter text to the longer one,
or keeping the longer text if one is a subset.

Usage:
    python3 pipeline/cleanup/nt_dedup_merge.py staging/validated/NT/MAT.md --in-place
    python3 pipeline/cleanup/nt_dedup_merge.py staging/validated/NT/*.md --in-place
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RE_ANCHOR = re.compile(r'^([A-Z0-9]{2,4}\.\d+:\d+)\s+(.*)')


def dedup_file(filepath: Path, dry_run: bool = False) -> int:
    """Merge duplicate anchors in a single file. Returns merge count."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    # First pass: find all anchors and their line indices
    anchor_lines: dict[str, list[int]] = {}
    for i, line in enumerate(lines):
        m = RE_ANCHOR.match(line)
        if m:
            anchor = m.group(1)
            anchor_lines.setdefault(anchor, []).append(i)

    # Find duplicates
    dups = {a: idxs for a, idxs in anchor_lines.items() if len(idxs) > 1}
    if not dups:
        return 0

    # For each duplicate: keep the line with the longest body, mark others for removal
    remove_indices: set[int] = set()
    for anchor, idxs in dups.items():
        # Get body text for each occurrence
        bodies = []
        for idx in idxs:
            m = RE_ANCHOR.match(lines[idx])
            bodies.append((idx, m.group(2) if m else ""))

        # Keep the longest body
        bodies.sort(key=lambda x: len(x[1]), reverse=True)
        keep_idx, keep_body = bodies[0]

        for idx, body in bodies[1:]:
            # If the shorter body adds new content, append it
            if body and body not in keep_body:
                # Only append if substantially different (not just a prefix/suffix)
                if len(body) > 10 and body[:20] != keep_body[:20]:
                    lines[keep_idx] = f"{anchor} {keep_body} {body}"
                    keep_body = f"{keep_body} {body}"
            remove_indices.add(idx)

    if not remove_indices:
        return 0

    new_lines = [line for i, line in enumerate(lines) if i not in remove_indices]
    merges = len(remove_indices)

    if dry_run:
        print(f"  [{filepath.stem}] Would merge {merges} duplicate anchors")
    else:
        filepath.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"  [{filepath.stem}] Merged {merges} duplicate anchors")

    return merges


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Merge duplicate NT anchors")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dry_run = args.dry_run or not args.in_place
    total = 0
    for f in args.files:
        p = Path(f)
        if p.exists() and p.suffix == ".md":
            total += dedup_file(p, dry_run=dry_run)

    print(f"\nTotal merges: {total}")


if __name__ == "__main__":
    main()
