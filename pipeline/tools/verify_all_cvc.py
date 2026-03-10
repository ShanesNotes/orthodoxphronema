"""
verify_all_cvc.py — Batch CVC verification against Brenton Septuagint.

Compares chapter_verse_counts in anchor_registry.json against actual
Brenton chapter files. Reports mismatches and optionally auto-fixes.

Supports cvc_overrides in the registry to mark intentional LXX/MT
versification differences that should not be "corrected".

Usage:
    python3 pipeline/tools/verify_all_cvc.py                  # report only
    python3 pipeline/tools/verify_all_cvc.py --fix             # update registry (all)
    python3 pipeline/tools/verify_all_cvc.py --fix-safe        # update only non-overridden
    python3 pipeline/tools/verify_all_cvc.py --book NUM DEU    # specific books
    python3 pipeline/tools/verify_all_cvc.py --report-json reports/cvc_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import (
    REPO_ROOT,
    REGISTRY_PATH as REGISTRY,
    BRENTON_SOURCE_DIR as BRENTON_DIR,
)

RE_FILENAME = re.compile(r'^eng-Brenton_(\d{3})_([A-Z0-9]+)_(\d{2,3})_read\.txt$')

# Brenton code → registry code
BRENTON_ALIASES: dict[str, str] = {
    "DAG": "DAN",
    "ESG": "EST",
    "NAM": "NAH",
}

# Books in Brenton that are outside our 76-book canon or are sub-parts
BRENTON_SKIP: set[str] = {
    "000",  # metadata
    "4MA",  # 4 Maccabees (appendix)
    "MAN",  # Prayer of Manasseh (appendix)
    "BEL",  # Bel and the Dragon (part of DAN additions)
    "SUS",  # Susanna (part of DAN additions)
}


def parse_brenton_chapter(path: Path) -> int:
    """Count non-empty verse lines in a Brenton chapter file (skip 2-line header)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return sum(1 for ln in lines[2:] if ln.strip())


def load_brenton_counts() -> dict[str, dict[int, int]]:
    """
    Build dict: registry_code → {chapter_num: verse_count} from Brenton files.
    """
    result: dict[str, dict[int, int]] = {}
    for path in sorted(BRENTON_DIR.glob("eng-Brenton_*_*_*_read.txt")):
        m = RE_FILENAME.match(path.name)
        if not m:
            continue
        brenton_code = m.group(2)
        chapter_num = int(m.group(3))

        if brenton_code in BRENTON_SKIP:
            continue

        # Map to registry code
        reg_code = BRENTON_ALIASES.get(brenton_code, brenton_code)

        if reg_code not in result:
            result[reg_code] = {}
        result[reg_code][chapter_num] = parse_brenton_chapter(path)

    return result


def load_registry() -> tuple[dict, list[dict]]:
    """Load registry, return (full_data, books_list)."""
    from pipeline.common.registry import load_registry as _load
    data = _load(REGISTRY)
    return data, data["books"]


# ── Override helpers ──────────────────────────────────────────────────────────

def load_overrides(reg_data: dict) -> dict:
    """Read cvc_overrides.entries from registry data. Returns {} if absent."""
    return reg_data.get("cvc_overrides", {}).get("entries", {})


def is_chapter_overridden(overrides: dict, code: str, ch_num: int) -> bool:
    """Check if a specific chapter is covered by an override entry."""
    book_overrides = overrides.get(code, {})
    return str(ch_num) in book_overrides


def is_chapter_count_overridden(overrides: dict, code: str) -> bool:
    """Check if a book's chapter-count mismatch is covered by an override."""
    book_overrides = overrides.get(code, {})
    return "_chapter_count" in book_overrides


# ── Core verification ─────────────────────────────────────────────────────────

def verify(book_filter: list[str] | None = None, fix: bool = False,
           fix_missing: bool = False, fix_safe: bool = False,
           report_json: str | None = None) -> int:
    """
    Compare registry CVC against Brenton. Returns number of mismatched books
    (excluding overridden ones).
    """
    brenton = load_brenton_counts()
    reg_data, books = load_registry()
    overrides = load_overrides(reg_data)

    total_books = 0
    matched = 0
    mismatched = 0
    overridden = 0
    missing_cvc = 0
    no_brenton = 0
    corrections: list[dict] = []
    report_entries: list[dict] = []

    for book in books:
        code = book["code"]
        if book_filter and code not in book_filter:
            continue

        total_books += 1
        expected_chapters = book["chapters"]
        registry_cvc = book.get("chapter_verse_counts")

        # Check Brenton coverage
        if code not in brenton:
            no_brenton += 1
            status = "NO_BRENTON"
            if registry_cvc:
                status += f" (has unverified CVC, total={sum(registry_cvc)})"
            else:
                status += " (no CVC)"
            print(f"  {code:4s}  {status}")
            report_entries.append({"code": code, "status": "NO_BRENTON"})
            continue

        brenton_chs = brenton[code]
        brenton_ch_count = len(brenton_chs)

        # Build Brenton CVC array (1-indexed chapters)
        brenton_cvc = []
        for ch in range(1, max(brenton_chs.keys()) + 1):
            brenton_cvc.append(brenton_chs.get(ch, 0))

        brenton_total = sum(brenton_cvc)

        if not registry_cvc:
            missing_cvc += 1
            print(f"  {code:4s}  MISSING_CVC  brenton={brenton_ch_count}ch/{brenton_total}v  → will populate")
            corrections.append({
                "code": code,
                "action": "populate",
                "old_cvc": None,
                "new_cvc": brenton_cvc,
                "old_total": 0,
                "new_total": brenton_total,
            })
            report_entries.append({"code": code, "status": "MISSING_CVC"})
            continue

        # Compare
        registry_total = sum(registry_cvc)
        reg_len = len(registry_cvc)

        if reg_len != brenton_ch_count:
            # Check if chapter-count mismatch is overridden
            if is_chapter_count_overridden(overrides, code):
                overridden += 1
                override_info = overrides[code]["_chapter_count"]
                print(f"  {code:4s}  OVERRIDE  chapter_count registry={reg_len}ch"
                      f" brenton={brenton_ch_count}ch"
                      f" — {override_info.get('reason', 'intentional')}")
                report_entries.append({
                    "code": code, "status": "OVERRIDE_ONLY",
                    "reason": override_info.get("reason", ""),
                })
                continue

            mismatched += 1
            print(f"  {code:4s}  CHAPTER_COUNT_MISMATCH  registry={reg_len}ch  brenton={brenton_ch_count}ch")
            if not fix_safe:
                corrections.append({
                    "code": code,
                    "action": "fix_chapters",
                    "old_cvc": registry_cvc,
                    "new_cvc": brenton_cvc,
                    "old_total": registry_total,
                    "new_total": brenton_total,
                })
            report_entries.append({"code": code, "status": "CHAPTER_COUNT_MISMATCH"})
            continue

        # Per-chapter comparison
        chapter_diffs = []
        overridden_diffs = []
        for i in range(reg_len):
            if registry_cvc[i] != brenton_cvc[i]:
                ch_num = i + 1
                if is_chapter_overridden(overrides, code, ch_num):
                    overridden_diffs.append((ch_num, registry_cvc[i], brenton_cvc[i]))
                else:
                    chapter_diffs.append((ch_num, registry_cvc[i], brenton_cvc[i]))

        if chapter_diffs and overridden_diffs:
            # Partial override — some diffs overridden, some not
            mismatched += 1
            diff_str = ", ".join(
                f"ch{ch}: {old}→{new}" for ch, old, new in chapter_diffs
            )
            ovr_str = ", ".join(
                f"ch{ch}" for ch, _, _ in overridden_diffs
            )
            print(f"  {code:4s}  PARTIAL_OVERRIDE  "
                  f"({len(chapter_diffs)} mismatch, {len(overridden_diffs)} overridden)  "
                  f"[{diff_str}]  overridden: [{ovr_str}]")

            if not fix_safe:
                corrections.append({
                    "code": code,
                    "action": "fix_values",
                    "old_cvc": registry_cvc,
                    "new_cvc": brenton_cvc,
                    "old_total": registry_total,
                    "new_total": brenton_total,
                    "diffs": chapter_diffs + overridden_diffs,
                })
            else:
                # fix-safe: build a corrected CVC that only changes non-overridden chapters
                safe_cvc = list(registry_cvc)
                for ch_num, _, new_val in chapter_diffs:
                    safe_cvc[ch_num - 1] = new_val
                corrections.append({
                    "code": code,
                    "action": "fix_values",
                    "old_cvc": registry_cvc,
                    "new_cvc": safe_cvc,
                    "old_total": registry_total,
                    "new_total": sum(safe_cvc),
                    "diffs": chapter_diffs,
                })

            report_entries.append({
                "code": code, "status": "PARTIAL_OVERRIDE",
                "mismatched_chapters": [ch for ch, _, _ in chapter_diffs],
                "overridden_chapters": [ch for ch, _, _ in overridden_diffs],
            })

        elif not chapter_diffs and overridden_diffs:
            # All diffs are overridden
            overridden += 1
            ovr_str = ", ".join(
                f"ch{ch}: {old}→{new}" for ch, old, new in overridden_diffs
            )
            print(f"  {code:4s}  OVERRIDE_ONLY  "
                  f"({len(overridden_diffs)} overridden)  [{ovr_str}]")
            report_entries.append({
                "code": code, "status": "OVERRIDE_ONLY",
                "overridden_chapters": [ch for ch, _, _ in overridden_diffs],
            })

        elif chapter_diffs:
            # No overrides, pure mismatch
            mismatched += 1
            diff_str = ", ".join(
                f"ch{ch}: {old}→{new}" for ch, old, new in chapter_diffs
            )
            print(f"  {code:4s}  CVC_MISMATCH  ({len(chapter_diffs)} chapters)  "
                  f"total {registry_total}→{brenton_total}  [{diff_str}]")
            corrections.append({
                "code": code,
                "action": "fix_values",
                "old_cvc": registry_cvc,
                "new_cvc": brenton_cvc,
                "old_total": registry_total,
                "new_total": brenton_total,
                "diffs": chapter_diffs,
            })
            report_entries.append({
                "code": code, "status": "CVC_MISMATCH",
                "mismatched_chapters": [ch for ch, _, _ in chapter_diffs],
            })
        else:
            matched += 1
            print(f"  {code:4s}  OK  {reg_len}ch/{registry_total}v")
            report_entries.append({"code": code, "status": "OK"})

    # Summary
    print(f"\n{'='*60}")
    print(f"Total books checked: {total_books}")
    print(f"  Matched:     {matched}")
    print(f"  Mismatched:  {mismatched}")
    print(f"  Overridden:  {overridden}")
    print(f"  Missing CVC: {missing_cvc}")
    print(f"  No Brenton:  {no_brenton}")

    # Determine which fix mode to apply
    effective_fix = fix or fix_safe

    if fix_missing and not effective_fix:
        populate_only = [c for c in corrections if c["action"] == "populate"]
        if populate_only:
            print(f"\nApplying {len(populate_only)} missing CVC population(s) to registry...")
            apply_corrections(reg_data, populate_only)
            print("Registry updated (missing CVCs only).")
            remaining = len(corrections) - len(populate_only)
            if remaining:
                print(f"  {remaining} mismatch(es) NOT applied — need manual review.")
        else:
            print("\nNo missing CVCs to populate.")
    elif corrections and effective_fix:
        label = "safe " if fix_safe else ""
        print(f"\nApplying {len(corrections)} {label}correction(s) to registry...")
        apply_corrections(reg_data, corrections)
        print("Registry updated.")
    elif corrections and not effective_fix:
        print(f"\n{len(corrections)} correction(s) available.")
        print(f"  Run with --fix-missing to populate missing CVCs only (safe).")
        print(f"  Run with --fix-safe to apply only non-overridden corrections.")
        print(f"  Run with --fix to apply ALL corrections (use with caution).")

    # Write JSON report if requested
    if report_json:
        affected = [e["code"] for e in report_entries
                    if e["status"] not in ("OK", "NO_BRENTON", "OVERRIDE_ONLY")]
        report = {
            "total_books": total_books,
            "matched": matched,
            "mismatched": mismatched,
            "overridden": overridden,
            "missing_cvc": missing_cvc,
            "no_brenton": no_brenton,
            "affected_books": affected,
            "entries": report_entries,
        }
        report_path = Path(report_json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\nJSON report written: {report_path}")

    return mismatched + missing_cvc


def apply_corrections(reg_data: dict, corrections: list[dict]):
    """Apply CVC corrections to registry and write back."""
    code_to_correction = {c["code"]: c for c in corrections}

    for book in reg_data["books"]:
        if book["code"] in code_to_correction:
            corr = code_to_correction[book["code"]]
            book["chapter_verse_counts"] = corr["new_cvc"]
            # Also fix chapters count if it differs
            if len(corr["new_cvc"]) != book["chapters"]:
                book["chapters"] = len(corr["new_cvc"])

    # Bump version
    old_version = reg_data.get("registry_version", "1.2.0")
    parts = old_version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    new_version = ".".join(parts)
    reg_data["registry_version"] = new_version

    # Add changelog entry
    from datetime import date
    codes = sorted(code_to_correction.keys())
    entry = {
        "version": new_version,
        "date": str(date.today()),
        "description": f"CVC batch verification against Brenton. "
                       f"Corrected/populated: {', '.join(codes)}."
    }
    reg_data.setdefault("registry_changelog", []).append(entry)

    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"  Registry version: {old_version} → {new_version}")
    for c in corrections:
        action = c["action"]
        print(f"  {c['code']}: {action}  {c['old_total']}→{c['new_total']}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch verify CVC in anchor_registry.json against Brenton."
    )
    parser.add_argument(
        "--book", nargs="*", metavar="CODE",
        help="Book code(s) to verify. Default: all."
    )
    parser.add_argument(
        "--fix", action="store_true",
        help="Apply ALL corrections to anchor_registry.json (use with caution)."
    )
    parser.add_argument(
        "--fix-missing", action="store_true",
        help="Only populate missing CVCs from Brenton (safe)."
    )
    parser.add_argument(
        "--fix-safe", action="store_true",
        help="Apply only corrections NOT covered by overrides."
    )
    parser.add_argument(
        "--report-json", metavar="FILE",
        help="Write structured JSON report with per-book status."
    )
    args = parser.parse_args()

    book_filter = [b.upper() for b in args.book] if args.book else None

    if not BRENTON_DIR.exists():
        print(f"ERROR: Brenton directory not found: {BRENTON_DIR}", file=sys.stderr)
        sys.exit(1)

    print("Batch CVC Verification — Registry vs Brenton")
    print(f"Registry: {REGISTRY}")
    print(f"Brenton:  {BRENTON_DIR}")
    print()

    issues = verify(book_filter, fix=args.fix, fix_missing=args.fix_missing,
                    fix_safe=args.fix_safe, report_json=args.report_json)
    sys.exit(1 if issues > 0 and not (args.fix or args.fix_safe) else 0)


if __name__ == "__main__":
    main()
