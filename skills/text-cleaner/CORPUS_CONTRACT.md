# Corpus Contract — Text Cleaner Onboarding Specification

When importing any new text source into the Orthodox Phronema Archive, follow this
contract to ensure consistent cleanup, validation, and promotion quality.

The text-cleaner toolkit is designed to be **transposable** across corpus types:
scripture, patristic, liturgical, hagiographic, catechetical, or any structured
text extracted from PDF via Docling.

## Required Deliverables

For each new corpus entering the archive, provide these four artifacts:

### 1. Profile YAML

Create a YAML profile in `skills/text-cleaner/profiles/` defining:

```yaml
name: corpus-name
description: "Brief description of this corpus type"

# How lines are structured
line_format: anchor | plain | numbered

# Regex to extract anchors (null for plain text)
anchor_regex: '^(PATTERN)\s+(.*)'

# Lines to never modify
protected_zones:
  - '^---\s*$'       # YAML frontmatter
  - '^#{1,4}\s'      # Markdown headers

# Path to domain-specific word list (relative to repo root)
allowlist: schemas/my_corpus_terms.txt

# Single-letter prefixes that may be fused footnote markers
fused_prefixes: [a, b]

# Footnote structural checks (F1-F4) — enable for footnote/study content
footnote_checks: [F1, F2, F3, F4]

# Path to reference aliases for F4 source alias checking
reference_aliases_path: schemas/reference_aliases.yaml

# Known false positives for this corpus
false_positives:
  - word1
  - word2
```

**Key decisions:**
- `line_format: anchor` for structured texts with verse/section references
- `line_format: plain` for prose without anchors (footnotes, articles, homilies)
- `fused_prefixes` depends on the source edition's footnote marker style
- `footnote_checks` should be enabled for any companion content (footnotes, articles)

### 2. Domain Allowlist

A plain text file (one word per line) of terms specific to this corpus that
aspell would otherwise flag as unknown. Place in `schemas/`.

**Building an allowlist:**
```bash
# Auto-generate candidate list from corpus
python3 skills/text-cleaner/scripts/clean.py \
  --dir path/to/corpus/ --profile my-corpus --pass spell --json \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
words = sorted(set(f['original'] for f in data['findings'] if f['code'] == 'P6'))
print('\n'.join(words))
" > schemas/my_corpus_candidates.txt

# Human review: remove actual misspellings, keep proper nouns and domain terms
# Save result as schemas/my_corpus_terms.txt
```

**Common categories:**
- Proper nouns (names, places, titles)
- Theological/liturgical terms
- Transliterated Greek/Hebrew/Syriac
- Archaic English (thy, thee, hath, whence, etc.)

### 3. Replacement Map

A JSON file for the `fix.py` curated fixer. Starts empty and builds through
scan/review cycles.

```json
{
  "strip": {},
  "article": {},
  "context": []
}
```

**Building a replacement map:**
```bash
# Scan for fused tokens
python3 skills/text-cleaner/scripts/scan.py \
  --dir path/to/corpus/ --profile my-corpus --json > scan_output.json

# Generate draft map (heuristic classification)
python3 skills/text-cleaner/scripts/fix.py \
  --generate-map scan_output.json --output draft_map.json

# Human review: verify each classification (strip vs. article)
# Apply reviewed map
python3 skills/text-cleaner/scripts/fix.py \
  --dir path/to/corpus/ --map reviewed_map.json --profile my-corpus
```

### 4. Validation Specification

Document which validation checks apply to this corpus. Not all canon
validation rules (V1-V12) apply to every text type.

| Check | Scripture | Footnotes | Articles | Patristic | Liturgical |
|-------|-----------|-----------|----------|-----------|------------|
| V1 (anchor format) | Yes | No | No | Varies | No |
| V2 (verse sequence) | Yes | No | No | No | No |
| V3 (frontmatter) | Yes | Yes | Yes | Yes | Yes |
| V4 (completeness) | Yes | No | No | No | No |
| V5 (purity) | Yes | Yes | Yes | Yes | Yes |
| V6 (encoding) | Yes | Yes | Yes | Yes | Yes |
| P1-P5 (mechanical) | Yes | Yes | Yes | Yes | Yes |
| P6 (spelling) | Yes | Yes | Yes | Yes | Yes |
| P7 (quotes) | Yes | Yes | Yes | Yes | Yes |
| P4/P8 (fused) | Yes | Yes | Yes | Yes | Yes |
| F1-F4 (footnotes) | No | Yes | Yes | No | No |

## Onboarding Sequence

```
1. Extract text via Docling
   → Raw markdown in staging/raw/

2. Create profile YAML
   → skills/text-cleaner/profiles/my-corpus.yaml

3. Run clean.py --dry-run
   → Review findings, classify false positives

4. Update profile with false positives
   → Iterate until FP rate is acceptable

5. Run clean.py --apply (P1-P5 auto-fixes)
   → Commit with audit memo

6. Run scan.py for deep fused-token analysis
   → Generate and review replacement map

7. Run fix.py with curated map
   → Commit with audit memo

8. Build domain allowlist from P6 findings
   → Human-reviewed, committed to schemas/

9. Run clean.py --pass spell with allowlist
   → Final spell check, review remaining unknowns

10. If footnote content: enable F1-F4 in profile
    → Run clean.py --pass footnote --dry-run
    → Review and apply structural fixes

11. Write final audit memo
    → Document all changes, error counts, decisions

12. Promote to study/ or canon/ per AGENTS.md
```

## Key Principles

- **Profile-driven**: All corpus-specific behavior lives in YAML profiles, not code
- **Aspell-gated**: Only flag tokens that aspell rejects AND whose remainder it accepts
- **Human-in-the-loop**: D1/D5/F1-F4 findings require review before application
- **Audit trail**: Every correction batch gets an Ezra audit memo
- **Transposable**: Same tools, same workflow, different profile — works for any text
