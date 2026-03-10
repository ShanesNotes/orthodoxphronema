"""
dropcap_verify.py — Detect and classify drop-cap omissions in staged canon files.

Two-stage model:
  Stage 1 (primary)   — OSB residual classifier: deterministic prefix map determines
                        the proposed repair. OSB residual shape is authoritative.
  Stage 2 (secondary) — Brenton prefix check: confirms or downgrades the proposal by
                        comparing only the repaired opening tokens against Brenton's
                        verse opening, with leading conjunctions stripped.

Key design rules:
  - Brenton does NOT generate the missing letter. Only the residual map does.
  - Brenton may DOWNGRADE a confirmed_auto to ambiguous_human.
  - Brenton never changes the proposed repair to a different letter.
  - Full-verse similarity scoring is NOT used (too noisy due to translation style gaps).
  - Only prefix comparison (first N tokens) is used for Brenton confirmation.

Classification tiers:
  confirmed_auto   — residual map matched AND Brenton prefix confirms (score >= 0.70)
                     OR residual map matched AND Brenton unavailable
  ambiguous_human  — residual map matched but Brenton disagrees (score < 0.40),
                     OR residual map unmatched, OR score in 0.40–0.70 range
  rejected         — (not used in this model; unmatched residuals → ambiguous_human)

Usage:
    python3 dropcap_verify.py staging/validated/OT/GEN.md
    python3 dropcap_verify.py staging/validated/OT/GEN.md --brenton-dir staging/reference/brenton
    python3 dropcap_verify.py staging/validated/OT/GEN.md --apply
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
from pipeline.common.paths import REPO_ROOT as _REPO_ROOT, BRENTON_DIR as _DEFAULT_BRENTON_DIR
from pipeline.common.patterns import RE_VERSE_LINE
RE_CHAPTER_VERSE_1 = re.compile(r'^[A-Z0-9]+\.\d+:1$')

# ---------------------------------------------------------------------------
# Stage 1: Deterministic residual map
# Each entry: (residual_prefix, repaired_prefix, missing_chars_count)
# The map covers all known drop-cap families observed in OSB PDF extraction.
# Ordering matters: longer prefixes first to prevent "ow" matching "oearly".
# ---------------------------------------------------------------------------
RESIDUAL_MAP: list[tuple[str, str, int]] = [
    # 2-char drop-cap initials (must come before 1-char entries that share prefix)
    ("nthe ",   "In the ",   2),   # "In the" — ch.1
    ("oearly ", "So early ", 2),   # "So early"
    ("tcame ",  "It came ",  2),   # "It came"
    # 1-char drop-cap initials
    ("ow ",     "Now ",      1),   # most common — 37 cases in Genesis
    ("hen ",    "Then ",     1),
    ("hus ",    "Thus ",     1),
    ("his ",    "This ",     1),
    ("fter ",   "After ",    1),
    ("nd ",     "And ",      1),
    ("o ",      "So ",       1),   # ambiguous: "No" or "So" — Brenton will arbitrate
    ("he ",     "The ",      1),
    ("ow,",     "Now,",      1),   # variant without trailing space
    ("ut ",     "But ",      1),
    ("n ",      "In ",       1),
    ("gain ",   "Again ",    1),   # "Again" → "Agian" never; residual "gain" → "Again"
]

# Brenton leading conjunctions to strip before prefix comparison
_BRENTON_SKIP_TOKENS = {
    "and", "but", "so", "now", "then", "thus", "for", "yet",
    "when", "after", "in", "behold", "moreover", "therefore",
}

# Prefix comparison token count
_PREFIX_TOKENS = 5

# Residuals that are inherently ambiguous between two possible drop-cap letters
# and cannot be reliably resolved by Brenton prefix comparison alone.
# These are always classified ambiguous_human regardless of Brenton score.
# "hen " → could be T+hen ("Then") or W+hen ("When"); Brenton often starts
# these verses with "And" so the stripped prefix comparison cannot distinguish.
_ALWAYS_AMBIGUOUS_RESIDUALS: set[str] = {"hen "}

# Brenton prefix score thresholds
_CONFIRM_THRESHOLD = 0.70   # >= this → Brenton confirms → confirmed_auto
_REJECT_THRESHOLD  = 0.40   # < this → Brenton disagrees → downgrade to ambiguous_human


def _load_normalize():
    from pipeline.reference import normalize_reference_text
    return normalize_reference_text


def _compare_prefix(repaired_text: str, brenton_verse: str, norm) -> float:
    """
    Compare the opening tokens of repaired OSB text against Brenton's verse opening.
    Strips leading conjunctions from Brenton before comparison.
    """
    osb_tokens = norm.tokenize(norm.normalize_for_compare(repaired_text))[:_PREFIX_TOKENS]

    bren_tokens = norm.tokenize(norm.normalize_for_compare(brenton_verse))
    # Strip leading conjunctions from Brenton (e.g. "And God said" → "God said")
    while bren_tokens and bren_tokens[0] in _BRENTON_SKIP_TOKENS:
        bren_tokens = bren_tokens[1:]
    bren_tokens = bren_tokens[:_PREFIX_TOKENS]

    if not osb_tokens or not bren_tokens:
        return 0.0
    return norm.token_similarity(" ".join(osb_tokens), " ".join(bren_tokens))


def classify_dropcap(
    anchor: str,
    text: str,
    chapter: int,
    verse: int,
    brenton_index: dict | None,
    norm,
) -> dict | None:
    """
    Classify a verse-1 drop-cap candidate.
    Returns candidate dict or None if the verse does not start lowercase.
    """
    if not text or not text[0].islower():
        return None

    # Stage 1: residual map lookup
    matched_repair: str | None = None
    matched_prefix: str | None = None
    residual_inherently_ambiguous = False

    for residual_prefix, repair_prefix, missing_count in RESIDUAL_MAP:
        if text.startswith(residual_prefix):
            matched_repair = repair_prefix + text[len(residual_prefix):]
            # missing_prefix = only the missing character(s), not the full repair prefix.
            # apply_repairs() prepends this to the existing text, so it must be just
            # the dropped character(s): e.g. "T" for "hen"→"Then", not "Then ".
            matched_prefix = repair_prefix[:missing_count]
            if residual_prefix in _ALWAYS_AMBIGUOUS_RESIDUALS:
                residual_inherently_ambiguous = True
            break

    # Stage 2: Brenton prefix confirmation
    brenton_verse: str | None = None
    prefix_score: float | None = None
    brenton_source = "unavailable"

    if brenton_index is not None and norm is not None:
        bv = norm.get_brenton_verse(brenton_index, chapter, verse)
        if bv:
            brenton_verse = bv
            brenton_source = "brenton"

    if matched_repair is None:
        # No residual match — unknown pattern
        return {
            "anchor": anchor,
            "residual": text[:60],
            "proposed_repair": None,
            "missing_prefix": None,
            "classification": "ambiguous_human",
            "prefix_score": None,
            "brenton_verse": brenton_verse[:80] if brenton_verse else None,
            "source": "residual_unmatched",
        }

    # We have a proposed repair from the residual map.
    # Now use Brenton (if available) to confirm or downgrade.
    if brenton_verse and norm:
        prefix_score = _compare_prefix(matched_repair, brenton_verse, norm)
        if residual_inherently_ambiguous:
            # "hen " residual cannot distinguish T+hen ("Then") from W+hen ("When").
            # Brenton prefix comparison also cannot disambiguate since both "Then X"
            # and "When X" score identically against Brenton's "And X" opening.
            # Force ambiguous regardless of score; human must verify via PDF.
            classification = "ambiguous_human"
        elif prefix_score >= _CONFIRM_THRESHOLD:
            classification = "confirmed_auto"
        elif prefix_score < _REJECT_THRESHOLD:
            classification = "ambiguous_human"  # Brenton disagrees — needs human
        else:
            # Middle range (0.40–0.70): treat as ambiguous regardless of residual match
            classification = "ambiguous_human"
    else:
        # Brenton unavailable — trust residual map alone.
        # "o " is inherently ambiguous ("So" or "No") — keep as ambiguous_human.
        # "hen " is inherently ambiguous ("Then" or "When") — always ambiguous_human.
        if text.startswith("o ") or residual_inherently_ambiguous:
            classification = "ambiguous_human"
        else:
            classification = "confirmed_auto"
        brenton_source = "heuristic_fallback"

    return {
        "anchor": anchor,
        "residual": text[:60],
        "proposed_repair": matched_repair[:80],
        "missing_prefix": matched_prefix,
        "classification": classification,
        "prefix_score": round(prefix_score, 4) if prefix_score is not None else None,
        "brenton_verse": brenton_verse[:80] if brenton_verse else None,
        "source": brenton_source,
    }


def scan_file(path: Path, brenton_dir: Path) -> list[dict]:
    """Scan a canon file for drop-cap candidates at chapter verse-1 positions."""
    book_code = path.stem
    norm = None
    brenton_index = None

    try:
        norm = _load_normalize()
        brenton_index = norm.load_brenton_index(book_code, brenton_dir)
        if brenton_index is None:
            print(
                f"WARNING: No Brenton index for {book_code} at {brenton_dir}. "
                "Using residual map only (no Brenton confirmation).",
                file=sys.stderr,
            )
    except Exception as e:
        print(f"WARNING: Could not load normalization module: {e}", file=sys.stderr)

    candidates = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = RE_VERSE_LINE.match(line)
        if not m:
            continue
        anchor, chapter_s, verse_s, text = m.group(1), m.group(2), m.group(3), m.group(4)

        if not RE_CHAPTER_VERSE_1.match(anchor):
            continue

        result = classify_dropcap(
            anchor, text, int(chapter_s), int(verse_s),
            brenton_index, norm,
        )
        if result:
            candidates.append(result)

    return candidates


def apply_repairs(path: Path, candidates_path: Path) -> int:
    """Apply ratified repairs from the candidates JSON to the canon file."""
    with open(candidates_path, encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("ratified"):
        print('ERROR: candidates JSON does not have "ratified": true', file=sys.stderr)
        print("Human must review and set ratified before --apply is safe.", file=sys.stderr)
        sys.exit(1)

    repairs: dict[str, str] = {}
    for c in data.get("candidates", []):
        if c["classification"] in ("confirmed_auto", "human_verified") and c.get("missing_prefix"):
            repairs[c["anchor"]] = c["missing_prefix"]

    if not repairs:
        print("No applicable repairs found in candidates JSON.")
        return 0

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    count = 0
    new_lines = []
    for line in lines:
        m = RE_VERSE_LINE.match(line.rstrip("\n"))
        if m and m.group(1) in repairs:
            anchor = m.group(1)
            prefix = repairs[anchor]
            old_text = m.group(4)
            new_lines.append(f"{anchor} {prefix}{old_text}\n")
            count += 1
            continue
        new_lines.append(line)

    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Applied {count} drop-cap repairs to {path}")
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Detect and classify drop-cap omissions: OSB-residual-first, Brenton-confirmed."
    )
    parser.add_argument("path", type=Path, help="Staged canon .md file")
    parser.add_argument(
        "--brenton-dir", type=Path, default=_DEFAULT_BRENTON_DIR,
        help=f"Brenton JSON index directory (default: {_DEFAULT_BRENTON_DIR})",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply repairs from ratified candidates JSON",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"File not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    book_code = args.path.stem
    candidates_path = args.path.with_name(f"{book_code}_dropcap_candidates.json")

    if args.apply:
        if not candidates_path.exists():
            print(f"Candidates file not found: {candidates_path}", file=sys.stderr)
            sys.exit(1)
        apply_repairs(args.path, candidates_path)
        return

    candidates = scan_file(args.path, args.brenton_dir)

    confirmed = sum(1 for c in candidates if c["classification"] == "confirmed_auto")
    ambiguous = sum(1 for c in candidates if c["classification"] == "ambiguous_human")

    output = {
        "book_code": book_code,
        "total_candidates": len(candidates),
        "confirmed_auto": confirmed,
        "ambiguous_human": ambiguous,
        "rejected": 0,
        "ratified": False,
        "candidates": candidates,
    }

    candidates_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote: {candidates_path}")
    print(f"  Total candidates : {output['total_candidates']}")
    print(f"  confirmed_auto   : {confirmed}")
    print(f"  ambiguous_human  : {ambiguous}")
    print(f"\nHuman must review, then set \"ratified\": true before --apply.")


if __name__ == "__main__":
    main()
