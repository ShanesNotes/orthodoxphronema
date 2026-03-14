---
name: canon-spell-audit
description: >
  Detection-only spelling audit for Orthodox Phronema Archive canon and staging
  files. Wraps the existing pipeline/tools/spell_audit.py with the biblical names
  allowlist to quickly scan individual books or the full corpus for unknown words.
  Use this skill when the user wants to: check spelling in a specific book, audit
  spelling across the corpus, build or update the biblical names allowlist, or
  investigate specific flagged words. Also trigger for "spell check", "unknown
  words", "dictionary check", "aspell audit", or any spelling-related query about
  the archive. This is a read-only skill — it never modifies files.
---

# Canon Spell Audit

A detection-only skill that runs aspell against canon/staging files with the
project's biblical names allowlist. Reports unknown words grouped by frequency
and location without making any changes.

## When to Use

- Quick spelling check on a single book before promotion
- Full-corpus audit to identify dictionary gaps
- Building or updating the biblical names allowlist
- Investigating whether a specific word is in the allowlist

## Usage

The existing `spell_audit.py` script is the engine. Run it from the repo root:

```bash
# Single book
python3 pipeline/tools/spell_audit.py --file canon/OT/01_GEN.md

# Full OT directory
python3 pipeline/tools/spell_audit.py --dir canon/OT

# Full OT with allowlist filtering
python3 pipeline/tools/spell_audit.py --dir canon/OT \
  --allowlist schemas/biblical_names.txt

# Build/update the allowlist from current corpus
python3 pipeline/tools/spell_audit.py --build-allowlist --dir canon/OT \
  --output schemas/biblical_names.txt

# JSON output for programmatic processing
python3 pipeline/tools/spell_audit.py --dir canon/OT \
  --allowlist schemas/biblical_names.txt \
  --output-json reports/spell_audit.json
```

## Interpreting Results

The script outputs flagged words grouped by book, with occurrence counts
and verse anchors. Common categories of flagged words:

1. **Biblical proper nouns** — Add these to the allowlist
2. **Archaic English** (`hast`, `thou`, `doth`) — Add to allowlist
3. **Septuagint terms** (`Sheol`, `Selah`) — Add to allowlist
4. **Actual misspellings** — These need correction via `canon-proofreader`
5. **OCR artifacts** — Residual fused/split words; use `canon-proofreader`

## Allowlist Management

The allowlist at `schemas/biblical_names.txt` is one word per line. To update:

1. Run the audit and review flagged words
2. Sort legitimate words into the allowlist
3. Re-run to verify the false positives are eliminated
4. Commit the updated allowlist

The `--build-allowlist` flag auto-generates an allowlist from words that appear
in 3+ books (heuristic: if it's in multiple books, it's probably intentional).

## Key Files

- `pipeline/tools/spell_audit.py` — The audit engine
- `schemas/biblical_names.txt` — Biblical names allowlist
- `reports/spell_audit.json` — Output report (when using `--output-json`)

## Limitations

- Aspell's English dictionary doesn't include archaic biblical English
- Proper nouns are always flagged unless in the allowlist
- Hyphenated words may be split and each half checked independently
- Does NOT detect contextual errors (wrong word, correct spelling)
