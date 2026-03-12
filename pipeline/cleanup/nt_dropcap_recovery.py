"""
nt_dropcap_recovery.py — Systematic drop-cap OCR recovery for NT books.

The OSB PDF uses decorative drop-cap (large initial letter) formatting at the
start of each chapter. Docling OCR consistently drops these initial characters,
producing lines like:
    MAT.1:1 he book of the genealogy...   (should be "The book...")
    MAT.2:1 ow after Jesus was born...    (should be "Now after...")

This tool:
1. Scans all NT books for first-verse-of-chapter drop-cap artifacts
2. Infers the missing prefix using known English/NKJV patterns
3. Applies high-confidence fixes only
4. Generates a manifest of all changes for audit trail

Usage:
    python3 pipeline/cleanup/nt_dropcap_recovery.py                  # dry-run
    python3 pipeline/cleanup/nt_dropcap_recovery.py --apply          # apply fixes
    python3 pipeline/cleanup/nt_dropcap_recovery.py --book MAT       # single book

Per EXTRACTION_POLICY.md: Drop-cap recovery is OSB-residual-first.
These are mechanical OCR artifacts with deterministic recovery.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"

RE_ANCHOR = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)\s+(.*)')
RE_CHAPTER = re.compile(r'^## Chapter (\d+)')


def build_fix_table() -> list[tuple[re.Pattern, str, str]]:
    """Build ordered list of (pattern, replacement, confidence).

    Each entry: when the verse text matches pattern, replace the matched
    portion with `replacement`. Order matters — first match wins.

    Replacement strings use the full corrected prefix (including any
    needed space insertion for fused OCR artifacts).
    """
    rules = []

    def add(pat: str, repl: str, conf: str = 'high'):
        rules.append((re.compile(pat), repl, conf))

    # ── Unambiguous multi-char fused patterns (most specific first) ─────
    add(r'^nthose\b', 'In those')           # "nthose days" → "In those days"
    add(r'^nthe\b', 'In the')               # "nthe same" → "In the same"
    add(r'^tthat\b', 'At that')             # "tthat time" → "At that time"
    add(r'^tis\b', 'It is')                 # "tis actually" → "It is actually"
    add(r'^oit was', 'So it was')           # "oit was" → "So it was"
    add(r'^owe\b', 'Do we')                 # "owe begin" → "Do we begin"
    add(r'^fthen\b', 'If then')             # "fthen you" → "If then you"
    add(r'^othen\b', 'So then')             # "othen Pilate" → "So then Pilate"
    add(r'^ethen\b', 'We then')             # "ethen, as workers" → "We then..."
    add(r'^ealso\b', 'He also')             # "ealso said" → "He also said"
    add(r'^ybrethren\b', 'My brethren')     # "ybrethren" → "My brethren"
    add(r'^rdo\b', 'Or do')                 # "rdo you" → "Or do you"

    # ── Unambiguous single-letter prefixes (longer patterns first) ──────
    add(r'^herefore\b', 'Therefore')
    add(r'^here were\b', 'There were')
    add(r'^here is\b', 'There is')
    add(r'^here was\b', 'There was')
    add(r'^here do\b', 'Where do')          # JAS.4:1
    add(r'^hough\b', 'Though')
    add(r'^his will\b', 'This will')
    add(r'^his is\b', 'This is')
    add(r'^he Revelation\b', 'The Revelation')
    add(r'^he elders\b', 'The elders')
    add(r'^he book\b', 'The book')
    add(r'^he grace\b', 'The grace')

    # "hen" — context-dependent: Then vs When
    # "hen [subject] had/was" → typically "When"
    # "hen [subject] [past-verb]" → could be either
    # We disambiguate by what follows
    add(r'^hen He had\b', 'When He had')      # MAT.8:1
    add(r'^hen morning\b', 'When morning')    # MAT.27:1
    add(r'^hen Jesus had spoken', 'When Jesus had spoken')  # JOH.18:1
    add(r'^hen he heard\b', 'When he heard')
    add(r'^hen Herod\b', 'When Herod')
    add(r'^hen he saw\b', 'When he saw')
    # Default "hen" → "Then" (narrative sequence — most common in NT)
    add(r'^hen\b', 'Then')

    add(r'^ow\b', 'Now')
    add(r'^nd\b', 'And')
    add(r'^ut\b', 'But')
    add(r'^or\b', 'For')
    add(r'^et\b', 'Let')
    add(r'^he\b', 'The')                     # catch-all for remaining "he ..."
    add(r'^lessed\b', 'Blessed')
    add(r'^rethren\b', 'Brethren')
    add(r'^ehold\b', 'Behold')
    add(r'^eloved\b', 'Beloved')
    add(r'^ursue\b', 'Pursue')
    add(r'^mmediately\b', 'Immediately')
    add(r'^mitate\b', 'Imitate')
    add(r'^asters\b', 'Masters')
    add(r'^aul\b', 'Paul')
    add(r'^esus\b', 'Jesus')
    add(r'^tand\b', 'Stand')
    add(r'^inally\b', 'Finally')
    add(r'^hildren\b', 'Children')
    add(r'^eceive\b', 'Receive')
    add(r'^emind\b', 'Remind')
    add(r'^oreover\b', 'Moreover')
    add(r'^ome now\b', 'Come now')
    add(r'^ives\b', 'Wives')
    add(r'^are\b', 'Dare')
    add(r'^hat\b', 'What')
    add(r'^foolish\b', 'O foolish')
    add(r'^fter\b', 'After')
    add(r'^o He\b', 'So He')
    add(r'^o he\b', 'So he')

    # "I " prefix patterns (OCR dropped "I " entirely)
    add(r'^commend\b', 'I commend')
    add(r'^beseech\b', 'I beseech')
    add(r'^charge\b', 'I charge')
    add(r'^saw\b', 'I saw')
    add(r'^m I\b', 'Am I')

    # The two previously unmatched
    add(r'^h, that you\b', 'Oh, that you')   # 2CO.11:1
    add(r'^ou therefore\b', 'You therefore')  # 2TI.2:1

    return rules


FIX_TABLE = build_fix_table()


def infer_dropcap_fix(text: str) -> tuple[str, str, str] | None:
    """Given verse text with a suspected drop-cap, infer the fix.

    Returns (fixed_text, replacement_note, confidence) or None.
    """
    for pattern, replacement, confidence in FIX_TABLE:
        m = pattern.match(text)
        if m:
            # Replace the matched portion with the replacement
            fixed = replacement + text[m.end():]
            note = f"'{text[:m.end()]}' → '{replacement}'"
            return fixed, note, confidence
    return None


def scan_book(book_path: Path) -> list[dict]:
    """Scan a single NT book for drop-cap issues."""
    issues = []
    lines = book_path.read_text(encoding='utf-8').splitlines()
    book_code = book_path.stem

    in_chapter = None
    first_verse_seen = False

    for i, line in enumerate(lines):
        m_ch = RE_CHAPTER.match(line)
        if m_ch:
            in_chapter = int(m_ch.group(1))
            first_verse_seen = False
            continue

        m_anc = RE_ANCHOR.match(line)
        if m_anc and in_chapter is not None and not first_verse_seen:
            ch = int(m_anc.group(2))
            v = int(m_anc.group(3))
            text = m_anc.group(4)
            first_verse_seen = True

            if v == 1 and ch == in_chapter:
                first_char = text[0] if text else ''
                if first_char and first_char.islower():
                    fix = infer_dropcap_fix(text)
                    anchor = f"{book_code}.{ch}:{v}"
                    # Reconstruct anchor prefix
                    text_start_idx = line.index(text)
                    anchor_prefix = line[:text_start_idx]

                    issue = {
                        'anchor': anchor,
                        'line_num': i + 1,
                        'original_text': text,
                        'original_line': line,
                    }
                    if fix:
                        fixed_text, note, confidence = fix
                        issue['fixed_text'] = fixed_text
                        issue['note'] = note
                        issue['confidence'] = confidence
                        issue['fixed_line'] = anchor_prefix + fixed_text
                    else:
                        issue['confidence'] = 'unmatched'
                    issues.append(issue)

    return issues


def apply_fixes(book_path: Path, issues: list[dict], dry_run: bool = True) -> int:
    """Apply drop-cap fixes to a book file."""
    if not issues:
        return 0

    lines = book_path.read_text(encoding='utf-8').splitlines()
    applied = 0

    for issue in issues:
        if issue.get('confidence') not in ('high',):
            continue

        line_idx = issue['line_num'] - 1
        if lines[line_idx] == issue['original_line']:
            lines[line_idx] = issue['fixed_line']
            applied += 1
        else:
            print(f"  WARNING: Line {issue['line_num']} changed, skip {issue['anchor']}")

    if not dry_run and applied > 0:
        book_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    return applied


def main():
    parser = argparse.ArgumentParser(description="NT drop-cap OCR recovery")
    parser.add_argument('--apply', action='store_true', help='Apply fixes (default: dry-run)')
    parser.add_argument('--book', type=str, help='Process single book (e.g., MAT)')
    parser.add_argument('--manifest', type=str, help='Output manifest JSON path')
    args = parser.parse_args()

    if args.book:
        book_files = [NT_DIR / f"{args.book}.md"]
    else:
        book_files = sorted([
            f for f in NT_DIR.iterdir()
            if f.suffix == '.md' and '_' not in f.stem
        ])

    all_issues: list[dict] = []
    total_applied = 0

    for bf in book_files:
        if not bf.exists():
            print(f"  SKIP  {bf.stem}: file not found")
            continue

        issues = scan_book(bf)
        if not issues:
            continue

        matched = [i for i in issues if i.get('confidence') != 'unmatched']
        unmatched = [i for i in issues if i.get('confidence') == 'unmatched']

        mode = "APPLYING" if args.apply else "DRY-RUN"
        print(f"\n  {bf.stem}: {len(issues)} drop-cap issues"
              f" ({len(matched)} matched, {len(unmatched)} unmatched)")

        for issue in issues:
            if issue.get('confidence') == 'unmatched':
                print(f"    UNMATCHED  {issue['anchor']}: "
                      f"{issue['original_text'][:60]}")
            else:
                note = issue.get('note', '')
                print(f"    {mode:>8}  {issue['anchor']}: {note}")

        applied = apply_fixes(bf, issues, dry_run=not args.apply)
        total_applied += applied
        all_issues.extend(issues)

    # Summary
    total = len(all_issues)
    matched = len([i for i in all_issues if i.get('confidence') != 'unmatched'])
    unmatched = total - matched

    print(f"\n{'═' * 60}")
    print(f"  SUMMARY: {total} drop-cap issues found")
    if total > 0:
        print(f"    Matched:   {matched} ({matched/total*100:.0f}%)")
        print(f"    Unmatched: {unmatched}")
    if args.apply:
        print(f"    Applied:   {total_applied}")
    else:
        print(f"    Would apply: {matched}")

    # Write manifest
    manifest_path = (args.manifest
                     or str(REPO_ROOT / "reports" / "nt_dropcap_recovery_manifest.json"))
    manifest = {
        'scan_date': '2026-03-12',
        'tool': 'pipeline/cleanup/nt_dropcap_recovery.py',
        'mode': 'apply' if args.apply else 'dry-run',
        'total_issues': total,
        'matched': matched,
        'unmatched': unmatched,
        'applied': total_applied if args.apply else 0,
        'issues': [
            {
                'anchor': i['anchor'],
                'line_num': i['line_num'],
                'original_start': i['original_text'][:80],
                'fixed_start': i.get('fixed_text', '')[:80],
                'note': i.get('note', ''),
                'confidence': i.get('confidence', 'unmatched'),
            }
            for i in all_issues
        ],
    }
    Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)
    Path(manifest_path).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"\n  Manifest: {manifest_path}")


if __name__ == '__main__':
    main()
