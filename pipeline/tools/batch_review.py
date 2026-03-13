#!/usr/bin/env python3
"""batch_review.py — Review all 76 books in biblical order.

Produces a compact review card per book:
  - V1-V12 check status
  - Verse count vs registry
  - Purity candidates (if sidecar exists)
  - Trailing marker residue
  - Spacing artifacts
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))

from pipeline.validate.validate_canon import run_validation
from pipeline.common.patterns import RE_ANCHOR
from pipeline.common.paths import canon_filepath

REGISTRY = REPO / "schemas" / "anchor_registry.json"

RE_TRAILING_LETTER = re.compile(r"^[A-Z0-9]+\.\d+:\d+\s.*\s[a-z]$")
RE_LORD_SPACING = re.compile(r"L\s+ORD")
RE_FUSED_MARKER = re.compile(r"\b[ab][a-z]{2,}")


def load_books():
    with open(REGISTRY) as f:
        reg = json.load(f)
    return sorted(reg["books"], key=lambda b: b["position"])


def find_file(book):
    code = book["code"]
    testament = book["testament"]
    canon = canon_filepath(testament, code)
    if canon.exists():
        return canon, "canon"
    staging = REPO / "staging" / "validated" / testament / f"{code}.md"
    if staging.exists():
        return staging, "staging"
    return None, "missing"


def count_trailing_markers(path):
    hits = []
    for line in path.read_text().splitlines():
        if RE_TRAILING_LETTER.match(line):
            hits.append(line[:80])
    return hits


def count_lord_spacing(path):
    hits = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if RE_LORD_SPACING.search(line):
            hits.append((i, line[:80]))
    return hits


def review_book(book):
    code = book["code"]
    name = book["name"]
    pos = book["position"]
    cvc = book.get("chapter_verse_counts", [])
    expected = sum(cvc) if cvc else None

    filepath, location = find_file(book)
    if filepath is None:
        return {
            "code": code, "name": name, "position": pos,
            "status": "MISSING", "location": location,
        }

    result = run_validation(filepath)
    total_anchors = result.metadata.get("total_anchors", 0)

    checks_summary = {}
    for c in result.checks:
        checks_summary[c.name] = c.status

    trailing = count_trailing_markers(filepath)
    lord_sp = count_lord_spacing(filepath)

    # Purity sidecar
    testament = book["testament"]
    purity_sidecar = REPO / "staging" / "validated" / testament / f"{code}_editorial_candidates.json"
    purity_count = 0
    if purity_sidecar.exists():
        try:
            data = json.load(open(purity_sidecar))
            purity_count = data.get("total_candidates", 0)
        except Exception:
            pass

    issues = []
    for c in result.checks:
        if c.status == "FAIL":
            issues.extend(c.errors[:3])
        if c.status == "WARN":
            issues.extend(c.warnings[:3])
    if trailing:
        issues.append(f"Trailing marker residue: {len(trailing)} lines")
    if lord_sp:
        issues.append(f"L ORD spacing: {len(lord_sp)} hits")

    overall = "clean"
    if any(c.status == "FAIL" for c in result.checks):
        overall = "FAIL"
    elif issues:
        overall = "issues"

    return {
        "code": code, "name": name, "position": pos,
        "location": location, "status": overall,
        "checks": checks_summary,
        "verses": total_anchors, "expected": expected,
        "purity_candidates": purity_count,
        "trailing_markers": len(trailing),
        "lord_spacing": len(lord_sp),
        "issues": issues,
    }


def main():
    books = load_books()
    results = []
    clean_count = 0
    issue_count = 0
    missing_count = 0

    for book in books:
        r = review_book(book)
        results.append(r)

        pos = r["position"]
        code = r["code"]
        name = r["name"]

        if r["status"] == "MISSING":
            print(f"  {pos:2d}. {code:4s} {name:25s} — MISSING")
            missing_count += 1
            continue

        loc_tag = f"[{r['location']}]"
        verses_str = f"{r['verses']}/{r['expected']}" if r['expected'] else f"{r['verses']}"
        checks_line = " ".join(
            f"{k}:{'✓' if v == 'PASS' else '!' if v == 'FAIL' else '~' if v == 'WARN' else '?'}"
            for k, v in r["checks"].items()
        )

        if r["status"] == "clean":
            print(f"  {pos:2d}. {code:4s} {name:25s} {loc_tag:10s} {verses_str:>12s}  CLEAN  {checks_line}")
            clean_count += 1
        else:
            marker = "FAIL" if r["status"] == "FAIL" else "WARN"
            print(f"  {pos:2d}. {code:4s} {name:25s} {loc_tag:10s} {verses_str:>12s}  {marker:5s}  {checks_line}")
            for iss in r["issues"][:5]:
                print(f"       → {iss[:100]}")
            issue_count += 1

    print(f"\n{'─'*80}")
    print(f"  Summary: {clean_count} clean, {issue_count} with issues, {missing_count} missing")
    print(f"  Total: {len(results)}/76 books reviewed")

    # Save JSON report
    out = REPO / "reports" / "batch_review_76.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print(f"  Report saved: {out}")


if __name__ == "__main__":
    main()
