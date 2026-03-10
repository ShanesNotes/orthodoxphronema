"""
audit_cleanup_residue.py — Post-cleanup residue audit for staged canon files.

After deterministic cleanup (fix_omissions.py) has run, this script flags
remaining OCR-like artifacts by comparing OSB tokens against Brenton tokens
at the verse level. Output only — no auto-fix.

Detection classes:
  fused_article   — OSB token matches Brenton bigram (short_prefix + word)
  fused_compound  — OSB token appears to be two Brenton words concatenated

Usage:
    python3 audit_cleanup_residue.py staging/validated/OT/GEN.md
    python3 audit_cleanup_residue.py staging/validated/OT/GEN.md --brenton-dir staging/reference/brenton
    python3 audit_cleanup_residue.py staging/validated/OT/GEN.md --min-score 0.7
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
from pipeline.common.paths import REPO_ROOT, BRENTON_DIR as _BRENTON_DIR
from pipeline.common.patterns import RE_VERSE_LINE, SHORT_PREFIXES

_DEFAULT_BRENTON_DIR = _BRENTON_DIR

# Short prefixes to check for fused_article class — includes "the" (superset)
_SHORT_PREFIXES = SHORT_PREFIXES | {"the"}

# Maximum Levenshtein distance to consider tokens "similar enough" for compound detection
_MAX_EDIT_DIST = 2


def _load_normalize_module():
    from pipeline.reference import normalize_reference_text
    return normalize_reference_text


def levenshtein(a: str, b: str) -> int:
    """Simple Levenshtein distance (DP). O(len(a)*len(b))."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j-1] + 1,
                            prev[j-1] + (0 if ca == cb else 1)))
        prev = curr
    return prev[len(b)]


def detect_fused_articles(osb_token: str, bren_bigrams: set[tuple[str, str]]) -> str | None:
    """Return split form if osb_token is a fused_article, else None."""
    for p in _SHORT_PREFIXES:
        if osb_token.startswith(p) and len(osb_token) > len(p) + 2:
            suffix = osb_token[len(p):]
            if len(suffix) >= 3 and (p, suffix) in bren_bigrams:
                return f"{p} {suffix}"
    return None


def detect_fused_compounds(osb_token: str, bren_bigrams: set[tuple[str, str]],
                            min_part: int = 3) -> str | None:
    """
    Return split form if osb_token looks like two Brenton words concatenated.
    Only checks splits where both parts are >= min_part chars.
    """
    n = len(osb_token)
    for split_at in range(min_part, n - min_part + 1):
        left = osb_token[:split_at]
        right = osb_token[split_at:]
        if (left, right) in bren_bigrams:
            return f"{left} {right}"
    return None


def audit_file(
    path: Path,
    brenton_dir: Path,
    min_verse_score: float,
) -> list[dict]:
    """
    Scan staged canon file for residual OCR artifacts verse-by-verse.
    Returns list of finding dicts.
    """
    norm = _load_normalize_module()
    book_code = path.stem

    brenton_index = norm.load_brenton_index(book_code, brenton_dir)
    if brenton_index is None:
        print(
            f"ERROR: No Brenton index for {book_code} at {brenton_dir}. "
            "Run index_brenton.py first.",
            file=sys.stderr
        )
        sys.exit(1)

    findings: list[dict] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        m = RE_VERSE_LINE.match(line)
        if not m:
            continue
        book, chapter_s, verse_s, text = m.group(1), m.group(2), m.group(3), m.group(4)
        anchor = f"{book}.{chapter_s}:{verse_s}"
        chapter, verse = int(chapter_s), int(verse_s)

        brenton_verse = norm.get_brenton_verse(brenton_index, chapter, verse)
        if not brenton_verse:
            continue

        norm_osb = norm.normalize_for_compare(text)
        norm_bren = norm.normalize_for_compare(brenton_verse)
        verse_score = norm.token_similarity(norm_osb, norm_bren)

        # Skip high-confidence verses — no residue expected
        if verse_score >= 0.95:
            continue

        osb_tokens = norm.tokenize(norm_osb)
        bren_tokens = norm.tokenize(norm_bren)
        bren_set = set(bren_tokens)

        # Build Brenton bigrams for compound detection
        bren_bigrams: set[tuple[str, str]] = set()
        for i in range(len(bren_tokens) - 1):
            bren_bigrams.add((bren_tokens[i], bren_tokens[i + 1]))

        for tok in osb_tokens:
            # Skip tokens already in Brenton vocabulary
            if tok in bren_set:
                continue
            # Skip very short tokens
            if len(tok) < 4:
                continue

            # Class 1: fused_article
            split_form = detect_fused_articles(tok, bren_bigrams)
            if split_form:
                findings.append({
                    "anchor": anchor,
                    "osb_token": tok,
                    "brenton_context": split_form,
                    "classification": "fused_article",
                    "verse_similarity": round(verse_score, 4),
                    "action": "human_review",
                })
                continue

            # Class 2: fused_compound (two Brenton words concatenated)
            # Only check if below score threshold to reduce false positives
            if verse_score < min_verse_score:
                split_form = detect_fused_compounds(tok, bren_bigrams)
                if split_form:
                    findings.append({
                        "anchor": anchor,
                        "osb_token": tok,
                        "brenton_context": split_form,
                        "classification": "fused_compound",
                        "verse_similarity": round(verse_score, 4),
                        "action": "human_review",
                    })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Post-cleanup residue audit: flags remaining OCR artifacts using Brenton."
    )
    parser.add_argument("path", type=Path, help="Staged canon .md file")
    parser.add_argument(
        "--brenton-dir", type=Path, default=_DEFAULT_BRENTON_DIR,
        help=f"Brenton JSON index directory (default: {_DEFAULT_BRENTON_DIR})"
    )
    parser.add_argument(
        "--min-score", type=float, default=0.80,
        help="Verse similarity threshold below which fused_compound detection activates (default: 0.80)"
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"File not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    book_code = args.path.stem
    print(f"Auditing residue in {args.path} ...")

    findings = audit_file(args.path, args.brenton_dir, args.min_score)

    # Write sidecar JSON
    out_path = args.path.with_name(f"{book_code}_residue_audit.json")
    fused_art = [f for f in findings if f["classification"] == "fused_article"]
    fused_cmp = [f for f in findings if f["classification"] == "fused_compound"]

    payload = {
        "book_code": book_code,
        "total_findings": len(findings),
        "fused_article": len(fused_art),
        "fused_compound": len(fused_cmp),
        "findings": findings,
    }
    out_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"Wrote: {out_path}")
    print(f"  Total findings : {len(findings)}")
    print(f"  fused_article  : {len(fused_art)}")
    print(f"  fused_compound : {len(fused_cmp)}")

    if findings:
        print("\nSample findings:")
        for f in findings[:10]:
            print(f"  {f['anchor']:15s} {f['osb_token']:20s} → {f['brenton_context']}"
                  f"  [{f['classification']}]")
        if len(findings) > 10:
            print(f"  ... and {len(findings) - 10} more (see {out_path.name})")


if __name__ == "__main__":
    main()
