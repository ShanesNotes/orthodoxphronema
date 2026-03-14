---
name: canon-proofreader
description: >
  Convenience wrapper for proofreading Orthodox Phronema canon scripture files.
  Delegates all detection and correction logic to the text-cleaner skill with
  --profile canon. Use this skill when the user mentions: proofreading canon,
  fixing scripture errors, correcting text in canon/, running a correction pass,
  fixing spelling in the archive, or any text-quality improvement across the
  corpus. For footnote/article cleanup, use text-cleaner directly with
  --profile footnotes.
---

# Canon Proofreader (Wrapper)

This skill is a **thin wrapper** around `text-cleaner` with `--profile canon`.

All detection and correction logic lives in `skills/text-cleaner/scripts/`:
- `clean.py` — multi-pass cleaner engine (P1-P8 regex + aspell)
- `scan.py` — deep fused-token scanner (D1-D6)
- `fix.py` — curated fused-token fixer (replacement map driven)

The canon-proofreader scripts (`proofread.py`, `deep_scan.py`,
`fix_fused_markers.py`) translate their legacy CLI interface into
equivalent text-cleaner calls. New work should use text-cleaner directly.

## Quick Start

These commands are equivalent:

```bash
# Via canon-proofreader (legacy interface)
python3 skills/canon-proofreader/scripts/proofread.py --scope all --dry-run

# Via text-cleaner (canonical interface)
python3 skills/text-cleaner/scripts/clean.py --scope canon --profile canon --dry-run
```

## Wrapper Mapping

| canon-proofreader | text-cleaner equivalent |
|-------------------|------------------------|
| `proofread.py --scope all` | `clean.py --scope canon --profile canon` |
| `proofread.py --file X` | `clean.py --file X --profile canon` |
| `proofread.py --include-staging` | + `clean.py --scope staging --profile staging` |
| `deep_scan.py --scope canon` | `scan.py --dir canon/ --profile canon` |
| `fix_fused_markers.py --scope canon` | `fix.py --dir canon/ --profile canon` |

## When to Use text-cleaner Directly

For any of these tasks, use `text-cleaner` with the appropriate profile:

- **Footnote structural cleanup:** `--profile footnotes` (F1-F4 patterns)
- **Study article cleanup:** `--profile staging`
- **New corpus onboarding:** See `skills/text-cleaner/CORPUS_CONTRACT.md`
- **Batch manifest operations:** `skills/text-cleaner/scripts/manifest.py`

## Error Categories

All P1-P8 categories remain the same (see text-cleaner SKILL.md for full list).
The footnotes profile adds F1-F4 for structural cleanup.

## Important Notes

- **Never modify verse anchors** — the `BOOK.CH:VS` prefix is sacrosanct
- **Never modify YAML frontmatter** — only verse text is in scope
- **Ezra audit required** — per AGENTS.md, all corrections to canon/ must be
  documented in a memo before promotion
