---
name: text-cleaner
description: >
  General-purpose text extraction cleanup toolkit for the Orthodox Phronema Archive.
  Detects and fixes OCR/extraction artifacts from Docling (or other PDF-to-text tools):
  fused words, split words, punctuation spacing, doubled text, footnote marker residue,
  and spelling errors. Works with any structured text corpus — scripture, patristic
  writings, liturgical texts, hagiography, catechetical material, etc.

  Use this skill when the user mentions: cleaning extracted text, fixing OCR errors,
  proofreading imported documents, post-extraction cleanup, fixing PDF artifacts,
  correcting Docling output, text quality pass, corpus cleanup, or any text-quality
  improvement across the Archive. Also trigger for "swiss cheese errors", "fused words",
  "split words", "extraction artifacts", or references to post-pipeline cleanup of any
  text in the phronema.
---

# Text Cleaner

General-purpose extraction artifact cleanup for the Orthodox Phronema Archive.
This skill evolved from the canon-proofreader (which handled biblical scripture)
into a corpus-agnostic toolkit that works with any text imported via Docling or
similar PDF extraction tools.

## Architecture

```
text-cleaner/
├── SKILL.md              ← you are here
├── scripts/
│   ├── clean.py          ← multi-pass cleaner engine (regex + aspell)
│   ├── scan.py           ← deep fused-token scanner (aspell-batch)
│   └── fix.py            ← curated fused-token fixer (profile-driven)
├── profiles/
│   ├── canon.yaml        ← biblical scripture profile
│   ├── patristic.yaml    ← Church Fathers / theological prose
│   └── default.yaml      ← sensible defaults for unknown corpora
└── references/
    └── error_patterns.md ← detailed examples of each error category
```

## When to Use

- After importing any new text via Docling (or similar PDF extraction)
- Cleaning up scripture, patristic writings, liturgical texts, etc.
- Running a corpus-wide quality pass before publishing
- Spot-checking individual files after re-extraction
- Any time text has fused words, split words, or punctuation issues

## Quick Start

```bash
# Scan a single file with default profile
python3 skills/text-cleaner/scripts/clean.py --file path/to/file.md --dry-run

# Scan a directory with a specific profile
python3 skills/text-cleaner/scripts/clean.py \
  --dir path/to/corpus/ --profile canon --dry-run

# Deep scan for fused footnote markers
python3 skills/text-cleaner/scripts/scan.py --dir path/to/corpus/

# Apply fixes from a curated replacement map
python3 skills/text-cleaner/scripts/fix.py \
  --dir path/to/corpus/ --profile canon

# Full pipeline: clean → scan → fix → validate
python3 skills/text-cleaner/scripts/clean.py --dir canon/ --profile canon
python3 skills/text-cleaner/scripts/scan.py --dir canon/ --profile canon
python3 skills/text-cleaner/scripts/fix.py --dir canon/ --profile canon
```

## Profiles

Profiles configure the cleaner for different corpus types. Each profile defines:

| Setting | Purpose |
|---------|---------|
| `line_format` | How to parse each line (anchor+text, plain, numbered, etc.) |
| `anchor_regex` | Regex for extracting anchors from structured text |
| `protected_zones` | Patterns to never modify (frontmatter, headers, anchors) |
| `allowlist` | Path to domain-specific word list (biblical names, theological terms) |
| `fused_prefixes` | Which single-letter prefixes to check for fusion (a, b, c, d) |
| `context_patterns` | Multi-word fusions specific to this corpus (e.g., "along time") |
| `false_positives` | Known safe words that look like fusions (dwelled, coffered, etc.) |
| `reference_corpus` | Optional ground-truth corpus for cross-referencing (e.g., Brenton) |

### Built-in Profiles

**`canon`** — Biblical scripture (OSB/Septuagint)
- Anchor format: `BOOK.CH:VS Text here.`
- YAML frontmatter + `## Chapter N` headers
- Biblical names allowlist at `schemas/biblical_names.txt`
- Fused prefixes: a, b, c, d (OSB cross-reference markers)
- 14 known false positives (dwelled, coffered, bended, etc.)

**`patristic`** — Church Fathers, theological prose
- Anchor format: flexible (numbered paragraphs, sections, or plain)
- Greek/Latin theological term allowlist
- Fused prefixes: a, b (common in footnoted editions)
- Larger false-positive list (more archaic English)

**`default`** — Generic extracted text
- No anchor format assumed — processes every non-blank line
- Standard English aspell dictionary only
- Fused prefixes: a (most common extraction artifact)
- Minimal false-positive list

## Error Categories

All profiles share the same error taxonomy:

| Code | Category | Auto-Fix? | Description |
|------|----------|-----------|-------------|
| P1 | Missing space after punctuation | Yes | `word.Next` → `word. Next` |
| P2 | Space before punctuation | Yes | `word .` → `word.` |
| P3 | Double/repeated words | Yes | `the the` → `the` |
| P4 | Fused preposition+word | Review | `ofthe` → `of the` |
| P5 | Multiple consecutive spaces | Yes | `word  next` → `word next` |
| P6 | Spelling (aspell) | Review | Unknown words flagged |
| P7 | Unbalanced quotes | Report | Mismatched quote counts |
| P8 | Fused conjunction+word | Review | `andhe` → `and he` |
| D1 | Fused footnote marker | Review | `aword` → `a word` or `word` |
| D3 | OCR kerning splits | Review | `J ESUS` → `JESUS` |
| D5 | Fused common words | Review | `theLord` → `the Lord` |

## Workflow for New Corpora

When importing a new text collection into the Archive:

1. **Choose or create a profile** — start with `default`, customize as needed
2. **Run clean.py --dry-run** to see what the engine finds
3. **Review the findings** — sort into real errors vs false positives
4. **Update the profile** with any new false positives or allowlist entries
5. **Run clean.py --apply** for auto-fixable items (P1–P5)
6. **Run scan.py** for deep fused-token analysis
7. **Build a replacement map** for D1 findings (or let Claude classify them)
8. **Run fix.py** with the curated map
9. **Write an audit memo** documenting all changes
10. **Validate** using canon-validator (for scripture) or a simple diff review

## Extending with New Profiles

Create a YAML file in `profiles/` following this template:

```yaml
name: my-corpus
description: "Description of this corpus type"

line_format: anchor  # or: plain, numbered
anchor_regex: '^([A-Z0-9]+\.\d+:\d+)\s+(.*)'

protected_zones:
  - '^---\s*$'       # YAML frontmatter
  - '^#{1,4}\s'      # Markdown headers

allowlist: schemas/my_corpus_terms.txt

fused_prefixes: [a, b]

context_patterns:
  - pattern: '\balong time\b'
    replacement: 'a long time'

false_positives:
  - dwelled
  - coffered
  - bended

reference_corpus: null  # or path to ground-truth
```

## Relationship to canon-proofreader

The `canon-proofreader` skill remains available as a convenience wrapper.
Under the hood, it now delegates to `text-cleaner` with `--profile canon`.
The three original canon-proofreader scripts are preserved for backward
compatibility but new work should use the text-cleaner directly.

## Key Insight: Aspell-Gated Detection

The single most effective technique discovered during the canon cleanup was
**aspell-gated detection**: only flag a token as fused if aspell does NOT
recognize the full token AND DOES recognize the remainder after stripping
the suspected prefix. This eliminates ~97% of false positives compared
to pure regex matching. All scripts in this toolkit use this approach.
