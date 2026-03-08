# Boundary-Shape Parser Fix — 2026-03-07

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `pipeline/parse/osb_extract.py` — RE_VERSE_SPLIT, _LC_OPENERS, _LC_VERSE_PAT, _lc_boundary_valid

## Context
- Ezra's source verification (memo 11) and PDF edge-case gate (memo 12) identified three failure classes in V4 gaps.
- PDF spot-check confirms all GEN gaps (27/27) and most EXO gaps match real verse boundaries in the source.
- The parser's boundary regex and opener allowlist are too narrow to capture these shapes.

## Failure Classes

### Class A: Opening punctuation after digit (no whitespace)
`18(He dwelt`, `14(for you shall`, `7(a cherub`, `5"so they may`
- `RE_VERSE_SPLIT` requires `\s+` before uppercase — fails when digit is fused to `(` or `"`
- Fix: add Case 2 alternation allowing optional whitespace + opening punct + letter

### Class B: Lowercase openers not in `_LC_OPENERS`
`the` (6x GEN), `he/she/we/it` (pronouns), `that` (3x), `to` (2x), `since`, `against`, `behold`, `let`, `saying`, `entered`, `come`, `throughout`, `opposite`, `as`
- Fix: expand `_LC_OPENERS` from 14 to ~35 words

### Class C: Fused digit-to-text (zero whitespace)
`2that`, `43behold`, `10come`, `29the`, `25throughout`
- `_LC_VERSE_PAT` requires `\s+` between digit and opener — fails on zero whitespace
- Fix: `\s+` → `\s*` (with optional opening punctuation)

### Class D: Comma-gated valid openers (Signal 2 false rejection)
`were, 5 and said` — `were` in `_INLINE_NUM_CTX` triggers Signal 2 rejection, but comma indicates clause boundary
- Fix: add Signal 1b — comma/semicolon + sequential acceptance

### Class E: Separate issues (not addressed here)
- GEN.49:2: poetic-block carryover (Docling TextItem classification)
- EXO.4:5: Docling OCR corruption (`5's othey` for `5 so`)
- EXO.9:3: PDF match not found

## Changes

| File | Line | Change |
|---|---|---|
| `osb_extract.py:58` | `RE_VERSE_SPLIT` | Add Case 2 alternation: `\s*(?=[(\[\'"\u201c\u2018][A-Za-z])` |
| `osb_extract.py:75-76` | `_LC_OPENERS` | Expand from 14 → ~35 words |
| `osb_extract.py:78-80` | `_LC_VERSE_PAT` | `\s+` → non-capturing group `(?:\s*[punct]*\s*)` |
| `osb_extract.py:325-361` | `_lc_boundary_valid` | Add Signal 1b: comma/semicolon + sequential |
| `osb_extract.py:395-396` | `_lc_split` | `best_match.start(2)` → `best_match.end(1)` for correct punct inclusion |
| `osb_extract.py:96` | `_LC_OPENERS` | Add `if` conditional opener |

### Class F: Column-merge path bypassing lc recovery
- When Docling splits text across TextItems, the continuation merge path only checked `RE_VERSE_SPLIT`, never `_LC_VERSE_PAT`
- Fix: add `or _LC_VERSE_PAT.search(merged)` to the column-merge re-split condition
- File: `osb_extract.py` ~line 702

### Class G: Early return bypassing lc recovery
- `split_verses_in_text` returned before `_recover_lc_splits` when `RE_VERSE_SPLIT.split()` yielded a single part
- Fix: call `_recover_lc_splits(results)` in the single-part branch before return
- File: `osb_extract.py` ~line 315

## Results (after registry correction — see below)

| Metric | Day 9 (before) | After fixes + registry correction |
|--------|---------------|-----------------------------------|
| **GEN V4 gaps** | 28 groups / 33 missing | **1 group / 1 missing** (V4 interior) |
| **GEN V7** | 97.3% (1492/1533) | **99.8% (1529/1532)** |
| **EXO V4 gaps** | 33 groups / 70 missing | **4 groups / 10 missing** (V4 interior) |
| **EXO V7** | 92.8% (1100/1185) | **99.6% (1161/1166)** |

## Registry Corrections (memo 14 finding)

Ezra's audit (memo 14) identified that the V7 completeness gap was conflating two different problems:
1. **True parser misses** — verses present in the OSB PDF but not captured by the parser
2. **Registry/chaptering deltas** — `chapter_verse_counts` entries derived from a different LXX numbering tradition

### EXO registry corrections (19 verses)
Three-way comparison (staged vs Brenton vs registry) confirmed 7 chapters with bad registry counts.
Staged + Brenton agreed in all cases; registry was the outlier.

| Chapter | Old registry | Corrected (Brenton) | Delta | Note |
|---------|-------------|-------------------|-------|------|
| 7 | 25 | 29 | +4 | ch7/8 boundary: OSB/LXX puts 7:26-29 in ch7 |
| 8 | 32 | 28 | -4 | mirror of ch7 |
| 22 | 31 | 30 | -1 | registry 1 high |
| 28 | 43 | 38 | -5 | registry 5 high |
| 35 | 35 | 32 | -3 | staged+Brenton agree at 32 |
| 38 | 31 | 27 | -4 | registry 4 high |
| 40 | 38 | 32 | -6 | registry 6 high |

Old EXO total: 1185 → Corrected: **1166** (net -19)

### GEN registry correction (1 verse)
| Chapter | Old registry | Corrected (Brenton) | Delta |
|---------|-------------|-------------------|-------|
| 31 | 55 | 54 | -1 |

Old GEN total: 1533 → Corrected: **1532** (net -1)

## Residual Classification

### GEN residuals (3 verses, 99.8%)

| Verse | Category | PDF evidence | Note |
|-------|----------|-------------|------|
| GEN.14:24 | **parser miss** | `24except only what the young men...` | fused `24except`; `except` not in `_LC_OPENERS` |
| GEN.25:34 | **source gap** | not found in PDF text layer | OSB text ends ch25 at v33; no bread/lentils/pottage text in PDF |
| GEN.49:2 | **Docling issue** | text present (poetry section) | poetic-block TextItem boundary, not regex |

### EXO residuals (5 verses against Brenton, 4 V4 interior gaps)

| Verse(s) | Category | PDF evidence | Note |
|-----------|----------|-------------|------|
| EXO.21:24-25 | **source/parser** | not found | `eye`, `burn` as verse openers — body nouns |
| EXO.25:4-7 | **source/parser** | not found | material list (`blue`, `ram`, `sardius`) |
| EXO.34:7 | **parser miss** | `7preserving` matched | fused specific verb, not generalizable |
| EXO.35:6-8 | **resolved** | `6blue 7ram 8sardius` matched | staged ch35=32 matches Brenton ch35=32; V4 gap is local fused numbering, not net deficit |

### Staged over-count (investigate)
| Book.Ch | Staged | Brenton | Note |
|---------|--------|---------|------|
| GEN.32 | 32 | 33 | Brenton extends ch32 into OSB's ch33:1; OSB count is correct |
| GEN.35 | 29 | 28 | staged 1 over Brenton; numbering tradition difference |
| EXO.32 | 35 | 34 | staged 1 over Brenton; may be OSB-specific verse split |
| EXO.36 | 39 | 38 | staged 1 over Brenton; may be OSB-specific verse split |

## Validation
- Full pipeline re-run: extract → fix_omissions → R7 brenton → dropcap_verify → validate
- PDF edge-case check (`--json-out`) confirms matched/unmatched gaps
- Registry corrected against Brenton (independent LXX witness)
- No regressions in V1/V2/V3/V8

## Recoverable parser misses (not yet implemented)
- GEN.14:24: add `except` to `_LC_OPENERS` — low false-positive risk, common clause-starting word
- GEN.49:2: requires Docling TextItem reclassification, not parser regex
- EXO.34:7: add `preserving` to `_LC_OPENERS` — very book-specific, high false-positive risk

**Policy**: per memo 14 and Human directive, no further heuristic expansion until residuals are classified via PDF spot-check and the source-policy distinction is resolved.

## Footnote Marker Note
- EXO marker count fluctuates between Docling runs (516 → 190) — Docling non-determinism, not parser regression
- GEN markers stable (~244). EXO markers likely require investigation at footnote extraction phase.
- One stray marker found in EXO.15:26 text — minor, not blocking
