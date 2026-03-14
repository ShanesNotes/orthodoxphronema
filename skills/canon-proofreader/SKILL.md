---
name: canon-proofreader
description: >
  Comprehensive proofreading and correction skill for Orthodox Phronema Archive
  canon scripture files, footnotes, and study articles. Detects and fixes spelling
  errors, fused words, split words, punctuation spacing issues, double words,
  OCR residue, and quote/apostrophe problems across all 76 canon books and 152
  staging companion files. Use this skill whenever the user mentions: proofreading
  canon, fixing scripture errors, correcting text in canon/, cleaning up footnotes
  or study articles, running a correction pass, fixing spelling in the archive,
  or any text-quality improvement across the Orthodox Phronema corpus. Also trigger
  when the user says "swiss cheese errors", "missed errors", "remaining typos",
  or refers to post-pipeline cleanup of promoted books.
---

# Canon Proofreader

Orchestrates a multi-pass correction pipeline across the Orthodox Phronema Archive.
This skill catches errors that slipped through the existing regex-based cleanup
scripts (`fix_articles.py`, `fix_omissions.py`, `fix_split_words.py`,
`canon_purity_fixer.py`) — the "swiss cheese" gaps between overlapping layers.

## When to Use

- Correcting published canon scripture in `canon/OT/` and `canon/NT/`
- Correcting footnotes and study articles in `staging/validated/`
- Running a full-corpus correction pass before a release milestone
- Spot-checking individual books after re-extraction

## Architecture

The proofreader runs **three passes** in sequence:

1. **Pass 1 — Deterministic Regex** (`scripts/proofread.py --pass regex`)
   Catches mechanical errors with zero false positives: missing space after
   punctuation, space before punctuation, double words, fused preposition+word
   compounds not in existing allowlists, multiple consecutive spaces.

2. **Pass 2 — Aspell + Biblical Dictionary** (`scripts/proofread.py --pass spell`)
   Runs aspell with the project's `schemas/biblical_names.txt` allowlist.
   Reports unknown words per anchor with confidence scoring. Does NOT auto-fix —
   outputs a review manifest.

3. **Pass 3 — LLM-Assisted Review** (Claude reads the manifest)
   You (Claude) review the Pass 1 + Pass 2 manifest, apply judgment on ambiguous
   cases, and produce the final correction set. This is where domain knowledge
   of Septuagint/Orthodox biblical English matters.

## Quick Start

```bash
# Full corpus — dry run (generates report only)
python3 skills/canon-proofreader/scripts/proofread.py \
  --scope all --dry-run --report-dir reports/proofread/

# Single book — dry run
python3 skills/canon-proofreader/scripts/proofread.py \
  --file canon/OT/01_GEN.md --dry-run

# Full corpus — apply fixes (Pass 1 auto-fixes only)
python3 skills/canon-proofreader/scripts/proofread.py \
  --scope all --apply --report-dir reports/proofread/

# Include staging footnotes and articles
python3 skills/canon-proofreader/scripts/proofread.py \
  --scope all --include-staging --dry-run
```

## Workflow

Follow this sequence for a full correction pass:

1. **Run dry-run on entire corpus** to generate the correction manifest
2. **Review the manifest** — the JSON report groups findings by category and book
3. **Apply Pass 1 auto-fixes** (these are safe, deterministic corrections)
4. **Review Pass 2 spell findings** — use your judgment on each flagged word
5. **Write an Ezra audit memo** to `memos/` documenting all changes before any
   canon promotion (per AGENTS.md protocol)
6. **Run `canon-validator`** skill to verify no regressions were introduced
7. **Commit changes** with a descriptive message referencing the memo

## File Format Context

Canon files use this format:
- YAML frontmatter between `---` delimiters
- `## Chapter N` headers
- One verse per line: `BOOK.CH:VS Text of the verse here.`
- No blank lines between verses within a chapter

The proofreader script understands this format and will never modify frontmatter,
chapter headers, or verse anchors. It only touches the text portion after the anchor.

## Error Categories

| Code | Category | Auto-Fix? | Description |
|------|----------|-----------|-------------|
| P1 | Missing space after punctuation | Yes | `word.Next` → `word. Next` |
| P2 | Space before punctuation | Yes | `word .` → `word.` |
| P3 | Double word | Yes | `the the` → `the` |
| P4 | Fused preposition+word | Review | `ofthe` → `of the` |
| P5 | Multiple consecutive spaces | Yes | `word  next` → `word next` |
| P6 | Spelling (aspell) | Review | Unknown words flagged |
| P7 | Unbalanced quotes | Report | Mismatched `'` or `"` counts |
| P8 | Fused conjunction+word | Review | `andhe` → `and he` |

## Important Notes

- **Never modify verse anchors** — the `BOOK.CH:VS` prefix is sacrosanct
- **Never modify YAML frontmatter** — only verse text is in scope
- **Ezra audit required** — per AGENTS.md, all corrections to canon/ must be
  documented in a memo before promotion
- **Brenton cross-reference** — when available, use Brenton as ground truth for
  ambiguous corrections (the script supports `--reference brenton`)
- Read `references/error_patterns.md` for detailed examples of each error category
