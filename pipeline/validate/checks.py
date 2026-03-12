"""Composable V-check functions for canon validation.

Each function returns a CheckResult with name, status, errors, and warnings.
validate_file() in validate_canon.py orchestrates these checks.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pipeline.common.config import BRENTON_WORD_MATCH_THRESHOLD, HEADING_REPETITION_LIMIT
from pipeline.common.patterns import RE_ANCHOR, KNOWN_SPLIT_JOIN_WORDS
from pipeline.common.types import CheckResult

# ── Constants ────────────────────────────────────────────────────────────────

ARTICLE_BLEED_PATTERNS = [
    r'Fall of Adam caused mankind',
    r"Mankind.s strong propensity to commit sin",
    r"intellectual, desiring and incensive",
    r"We who are of Adam.s race are not guilty because of Adam.s sin",
    r"Even after the Fall, the intellectual",
    r"T he Holy Trinity is revealed both",
]

REQUIRED_FM_FIELDS = [
    "book_code", "book_name", "testament", "canon_position",
    "source", "parse_date", "status",
]

COMMON_FRAGMENT_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "for", "go",
    "he", "her", "him", "his", "i", "if", "in", "into", "is", "it",
    "me", "my", "no", "not", "of", "on", "or", "our", "out", "so",
    "the", "their", "them", "they", "to", "up", "us", "was", "we",
    "were", "who", "with", "you", "your",
}


# ── Gap computation (shared by V4, V9, V10) ─────────────────────────────────

def compute_v4_gaps(
    verses_by_chapter: dict[int, list[tuple[int, int]]],
) -> list[tuple[int, int, int]]:
    """Return list of (chapter, gap_from, gap_to) for each V4 gap."""
    gaps: list[tuple[int, int, int]] = []
    for ch, verse_list in sorted(verses_by_chapter.items()):
        prev_v = 0
        for (v, _lineno) in verse_list:
            if v > prev_v + 1:
                gaps.append((ch, prev_v, v))
            prev_v = max(prev_v, v)
    return gaps


# ── Individual checks ────────────────────────────────────────────────────────

def check_frontmatter(fm: dict) -> CheckResult:
    """V6: Required frontmatter fields."""
    errors = []
    for field in REQUIRED_FM_FIELDS:
        if field not in fm:
            errors.append(f"V6   Missing frontmatter field: {field}")
    status = "FAIL" if errors else "PASS"
    return CheckResult(name="V6", status=status, errors=errors, warnings=[])


def check_anchor_uniqueness(
    anchors: list[tuple[str, int, int, int]],
    anchor_set: set[str],
) -> CheckResult:
    """V1: No duplicate anchors."""
    # Find duplicates by checking if anchor was seen before
    seen: set[str] = set()
    duplicates: list[str] = []
    for (anchor_str, _ch, _v, lineno) in anchors:
        if anchor_str in seen:
            duplicates.append(f"  line {lineno}: {anchor_str}")
        seen.add(anchor_str)

    if duplicates:
        errors = [f"V1   {len(duplicates)} duplicate anchor(s):"]
        errors.extend(duplicates[:10])
        if len(duplicates) > 10:
            errors.append(f"     ... and {len(duplicates) - 10} more")
        return CheckResult(name="V1", status="FAIL", errors=errors, warnings=[])
    return CheckResult(name="V1", status="PASS", errors=[], warnings=[])


def check_chapter_count(
    chapters_seen: list[tuple[int, int]],
    expected_chapters: int | None,
    strict: bool = False,
) -> CheckResult:
    """V2: Correct number of chapters."""
    actual = len(chapters_seen)
    if expected_chapters is None:
        return CheckResult(name="V2", status="INFO", errors=[], warnings=[])

    if actual == expected_chapters:
        return CheckResult(name="V2", status="PASS", errors=[], warnings=[])

    msg = f"V2   Chapter count: expected {expected_chapters}, got {actual}"
    if strict:
        return CheckResult(name="V2", status="FAIL", errors=[msg], warnings=[])
    return CheckResult(name="V2", status="WARN", errors=[], warnings=[msg])


def check_chapter_sequence(
    chapters_seen: list[tuple[int, int]],
) -> CheckResult:
    """V3: Chapters are sequential with no gaps."""
    errors = []
    # Allow Chapter 0 as an optional intro/nav chapter before Chapter 1.
    offset = 0 if (chapters_seen and chapters_seen[0][0] == 0) else 1
    for i, (ch_num, lineno) in enumerate(chapters_seen):
        expected = i + offset
        if ch_num != expected:
            errors.append(
                f"V3   Chapter sequence broken at line {lineno}: "
                f"expected {expected}, got {ch_num}"
            )
    status = "FAIL" if errors else "PASS"
    return CheckResult(name="V3", status=status, errors=errors, warnings=[])


def check_verse_sequence(
    verses_by_chapter: dict[int, list[tuple[int, int]]],
    book_code: str | None = None,
) -> CheckResult:
    """V4: Within each chapter, verses are monotonically increasing."""
    errors = []
    warnings = []
    total_missing = 0
    gap_records: list[dict] = []
    missing_anchors: list[str] = []
    for ch, verse_list in sorted(verses_by_chapter.items()):
        prev_v = 0
        for (v, lineno) in verse_list:
            if v < prev_v:
                errors.append(
                    f"V4   Verse goes backward in ch.{ch} at line {lineno}: "
                    f"verse {v} after verse {prev_v}"
                )
            elif v > prev_v + 1:
                warnings.append(
                    f"V4   Missing verses in ch.{ch}: jumps from {prev_v} to {v}"
                )
                total_missing += v - prev_v - 1
                missing = list(range(prev_v + 1, v))
                gap_records.append(
                    {
                        "chapter": ch,
                        "from_verse": prev_v,
                        "to_verse": v,
                        "missing_verses": missing,
                    }
                )
                if book_code:
                    missing_anchors.extend(
                        f"{book_code}.{ch}:{missing_v}" for missing_v in missing
                    )
            prev_v = max(prev_v, v)

    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"
    return CheckResult(
        name="V4",
        status=status,
        errors=errors,
        warnings=warnings,
        data={
            "gaps": gap_records,
            "missing_anchors": missing_anchors,
            "total_missing": total_missing,
        },
    )


def check_article_bleed(
    lines: list[str],
    body_start: int,
) -> CheckResult:
    """V5: No article phrases leaked into canon."""
    errors = []
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        for pattern in ARTICLE_BLEED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                errors.append(
                    f"V5   Article text in canon at line {lineno}: {line[:80]!r}"
                )
                break
    status = "FAIL" if errors else "PASS"
    return CheckResult(name="V5", status=status, errors=errors, warnings=[])


def check_completeness(
    anchor_set: set[str],
    chapter_verse_counts_list: list | None,
) -> CheckResult:
    """V7: Total anchors match registry verse counts."""
    if not chapter_verse_counts_list:
        return CheckResult(
            name="V7",
            status="INFO",
            errors=[],
            warnings=[],
            data={"expected_total": None, "actual_total": len(anchor_set), "gap": None, "pct": None},
        )

    expected_total = sum(chapter_verse_counts_list)
    actual = len(anchor_set)
    gap = expected_total - actual
    if gap == 0:
        return CheckResult(
            name="V7",
            status="PASS",
            errors=[],
            warnings=[],
            data={"expected_total": expected_total, "actual_total": actual, "gap": 0, "pct": 100.0},
        )

    pct = actual / expected_total * 100
    msg = (
        f"V7   Completeness: {actual}/{expected_total} verses "
        f"({pct:.1f}%); gap of {gap}"
    )
    return CheckResult(
        name="V7",
        status="WARN",
        errors=[],
        warnings=[msg],
        data={"expected_total": expected_total, "actual_total": actual, "gap": gap, "pct": pct},
    )


def check_heading_integrity(
    lines: list[str],
    body_start: int,
    anchor_set: set[str],
) -> CheckResult:
    """V8: No fragment headings, repetition, or density anomalies."""
    from collections import Counter

    errors = []
    warnings = []

    heading_rows: list[tuple[int, str, int]] = []
    current_heading_line: int | None = None
    current_heading_text: str | None = None
    current_heading_verse_count = 0

    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        if line.startswith('### '):
            if current_heading_line is not None:
                heading_rows.append(
                    (current_heading_line, current_heading_text or "",
                     current_heading_verse_count)
                )
            current_heading_line = lineno
            current_heading_text = line[4:].rstrip()
            current_heading_verse_count = 0

            heading = current_heading_text
            if heading.endswith((':', ',')):
                errors.append(
                    f"V8   Fragment heading at line {lineno}: {line.rstrip()!r}"
                )
            elif heading[:1].isdigit():
                errors.append(
                    f"V8   Digit-leading heading at line {lineno}: {line.rstrip()!r}"
                )
            continue

        if current_heading_line is not None and RE_ANCHOR.match(line):
            current_heading_verse_count += 1

        if current_heading_line is not None and line.startswith('## Chapter '):
            heading_rows.append(
                (current_heading_line, current_heading_text or "",
                 current_heading_verse_count)
            )
            current_heading_line = None
            current_heading_text = None
            current_heading_verse_count = 0

    if current_heading_line is not None:
        heading_rows.append(
            (current_heading_line, current_heading_text or "",
             current_heading_verse_count)
        )

    # Heading repetition
    heading_counter = Counter()
    for line in lines[body_start:]:
        if line.startswith('### '):
            heading_counter[line[4:].rstrip()] += 1

    for title, count in heading_counter.items():
        if count > HEADING_REPETITION_LIMIT:
            errors.append(
                f"V8   Heading repetition: {title!r} appears {count} times"
            )

    # Heading density
    if len(heading_counter) > 0:
        chapter_count = len({a.split('.')[1].split(':')[0] for a in anchor_set})
        total_headings = sum(heading_counter.values())
        if total_headings > chapter_count * 3:
            density = total_headings / max(chapter_count, 1)
            warnings.append(
                f"V8   Heading density: {total_headings} headings"
                f" / {chapter_count} chapters ({density:.1f}/ch)"
            )

    # Headings not followed by verses
    for lineno, heading, verse_span in heading_rows:
        if verse_span == 0:
            errors.append(
                f"V8   Heading at line {lineno} is not followed by any verse "
                f"content: {heading!r}"
            )

    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"
    return CheckResult(name="V8", status=status, errors=errors, warnings=warnings)


def check_embedded_verses(
    gaps: list[tuple[int, int, int]],
    verse_line_map: dict[str, tuple[int, str]],
    book_code: str,
) -> CheckResult:
    """V9: Check if missing verses are embedded in adjacent verse lines."""
    errors = []
    for (gap_ch, gap_from, gap_to) in gaps:
        prev_anchor = f"{book_code}.{gap_ch}:{gap_from}"
        if prev_anchor not in verse_line_map:
            continue
        prev_lineno, prev_line = verse_line_map[prev_anchor]
        for missing_v in range(gap_from + 1, gap_to):
            if re.search(rf'(?<!\d){missing_v}(?!\d)', prev_line):
                errors.append(
                    f"V9   Embedded verse {book_code}.{gap_ch}:{missing_v} "
                    f"found inside {prev_anchor} at line {prev_lineno}"
                )
    status = "FAIL" if errors else "PASS"
    return CheckResult(name="V9", status=status, errors=errors, warnings=[])


def check_absorbed_content(
    gaps: list[tuple[int, int, int]],
    verse_line_map: dict[str, tuple[int, str]],
    book_code: str,
    brenton_path: Path,
) -> CheckResult:
    """V10: Brenton cross-reference for absorbed content."""
    if not brenton_path.exists():
        return CheckResult(name="V10", status="SKIP", errors=[], warnings=[])
    if not gaps:
        return CheckResult(name="V10", status="PASS", errors=[], warnings=[])

    try:
        with open(brenton_path, encoding="utf-8") as f:
            brenton_data = json.load(f)
        brenton_chapters = brenton_data.get("chapters", {})
    except Exception:
        return CheckResult(name="V10", status="SKIP", errors=[], warnings=[])

    warnings = []
    for (gap_ch, gap_from, gap_to) in gaps:
        ch_str = str(gap_ch)
        if ch_str not in brenton_chapters:
            continue
        brenton_verses = brenton_chapters[ch_str].get("verses", [])

        for missing_v in range(gap_from + 1, gap_to):
            b_idx = missing_v - 1
            if b_idx < 0 or b_idx >= len(brenton_verses):
                continue
            b_text = brenton_verses[b_idx].lower()
            if len(b_text) < 20:
                continue

            b_words = [w for w in re.findall(r'[a-z]+', b_text) if len(w) >= 4]
            if len(b_words) < 3:
                continue

            for check_v in [gap_from, gap_to]:
                check_anchor = f"{book_code}.{gap_ch}:{check_v}"
                if check_anchor not in verse_line_map:
                    continue
                _, osb_line = verse_line_map[check_anchor]
                osb_lower = osb_line.lower()

                matches = sum(1 for bw in b_words if bw in osb_lower)
                match_ratio = matches / len(b_words) if b_words else 0

                if match_ratio >= BRENTON_WORD_MATCH_THRESHOLD:
                    warnings.append(
                        f"V10  Absorbed content: {book_code}.{gap_ch}:{missing_v}"
                        f" likely present in {check_anchor}"
                        f" (Brenton word match: {matches}/{len(b_words)}"
                        f" = {match_ratio:.0%})"
                    )
                    break

    status = "WARN" if warnings else "PASS"
    return CheckResult(name="V10", status=status, errors=[], warnings=warnings)


def check_split_words(
    lines: list[str],
    body_start: int,
) -> CheckResult:
    """V11: Docling column-split artifacts."""
    RE_SPLIT_WORD = re.compile(
        r'(?<=[a-z])(ov|ev|iv|erv|alv|elv|olv|eav|av|arv|ilv) ([a-z])',
    )
    RE_LOWER_TOKEN = re.compile(r'\b[a-z]{1,10}\b')

    warnings = []
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        m_anc = RE_ANCHOR.match(line)
        if not m_anc:
            continue
        anchor_str = m_anc.group(1)
        text_part = line[m_anc.end():]
        seen_contexts: set[str] = set()

        for sm in RE_SPLIT_WORD.finditer(text_part):
            # Skip proper nouns (capitalized words ending in suffix pattern)
            word_start = text_part.rfind(' ', 0, sm.start()) + 1
            if word_start < sm.start() and text_part[word_start].isupper():
                continue
            context = text_part[max(0, sm.start() - 8):sm.end() + 8].strip()
            if context in seen_contexts:
                continue
            seen_contexts.add(context)
            warnings.append(
                f"V11  Split-word suspect at line {lineno}:"
                f" {context!r} in {anchor_str}"
            )

        token_matches = list(RE_LOWER_TOKEN.finditer(text_part))
        for left_match, right_match in zip(token_matches, token_matches[1:]):
            if left_match.end() + 1 != right_match.start():
                continue
            left = left_match.group(0)
            right = right_match.group(0)
            joined = f"{left}{right}"
            if left in COMMON_FRAGMENT_WORDS or right in COMMON_FRAGMENT_WORDS:
                continue
            if joined not in KNOWN_SPLIT_JOIN_WORDS:
                continue
            context = text_part[
                max(0, left_match.start() - 8):right_match.end() + 8
            ].strip()
            if context in seen_contexts:
                continue
            seen_contexts.add(context)
            warnings.append(
                f"V11  Split-word suspect at line {lineno}:"
                f" {context!r} in {anchor_str}"
            )

    status = "WARN" if warnings else "PASS"
    return CheckResult(name="V11", status=status, errors=[], warnings=warnings)


def check_inline_leakage(
    lines: list[str],
    body_start: int,
) -> CheckResult:
    """V12: Verse's own number leaked into text body."""
    RE_INLINE_VNUM = re.compile(r'[,;.]\s*(\d+)\s+[a-z]')

    warnings = []
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        m_anc = RE_ANCHOR.match(line)
        if not m_anc:
            continue
        verse_num = m_anc.group(3)
        text_part = line[m_anc.end():]
        for vm in RE_INLINE_VNUM.finditer(text_part):
            if vm.group(1) == verse_num:
                context = text_part[max(0, vm.start() - 4):vm.end() + 8].strip()
                warnings.append(
                    f"V12  Inline verse-number leakage at line {lineno}:"
                    f" {m_anc.group(1)}.{m_anc.group(2)}:{verse_num}"
                    f" contains {context!r}"
                )

    status = "WARN" if warnings else "PASS"
    return CheckResult(name="V12", status=status, errors=[], warnings=warnings)
