# Liturgical Cross-References Parsing

**Date:** 2026-03-14
**Source:** Orthodox Study Bible "This passage is read at" references (pages 10410-10774)
**Output:** `/home/ark/orthodoxphronema/reference/liturgical-crossrefs.json`

## Task Summary

Parsed the OSB liturgical cross-references from a 1164-line text file into structured JSON, mapping scripture passages to their liturgical occasions.

## Input Format

Two patterns in the source file:

1. **Implicit book references (Genesis through early OT):** Lines starting with verse ranges, no book prefix
   - Example: `1:1-3 This passage is read during Vespers on Great and Holy Saturday.`

2. **Explicit book references (later books):** Lines with book abbreviation, verse ranges, and occasion text
   - Example: `Gen 17:1, 2, 4–8, 9–12, 14: These verses are read at the Feast of the Circumcision of Our Lord Jesus Christ.`

Special notes:
- Form feed characters (`\x0c`) separated major sections
- Multi-line occasion descriptions required lookahead collection
- Verse ranges included complex patterns: `13:1–3, 10–12, 14–16; 22:29`
- Unicode en-dash (`–`) used instead of ASCII hyphen

## Parser Implementation

**File:** `/home/ark/orthodoxphronema/parse_osb_liturgical.py`

Key features:
- Regex pattern for explicit refs: `^([A-Za-z0-9]+)\s+(.*?):\s*([A-Z].+)$`
  - Captures book name, verse range (with internal colons), and occasion text
- Implicit references matched: `^([0-9:,–\-;\s]+?)\s+(.+)`
- Book name normalization via lookup table (3-letter codes per repo standard)
- Multi-line occasion text collection with forward-lookahead
- Form feed removal for cleaner parsing

## Output Format

```json
{
  "meta": {
    "source": "Orthodox Study Bible",
    "description": "Liturgical cross-references: scripture passages and their liturgical occasions",
    "extracted": "2026-03-14",
    "count": 307
  },
  "entries": [
    {
      "reference": "GEN 1:1-3",
      "occasions": ["This passage is read during Vespers on Great and Holy Saturday"],
      "needs_review": true
    },
    ...
  ]
}
```

All occasions consolidated into a single-string array (future enhancement: could split on conjunctions).

## Results

**Total entries parsed:** 307

| Book | Explicit | Implicit | Total |
|------|----------|----------|-------|
| GEN  | 1        | 35       | 36    |
| EXO  | 2        | 118      | 120   |
| MIC  | 1        | 10       | 11    |
| ISA  | 2        | 26       | 28    |
| MAT  | 1        | 25       | 26    |
| LUK  | 1        | 19       | 20    |
| JOH  | 2        | 29       | 31    |
| 1CO  | 1        | 24       | 25    |
| HEB  | 1        | 9        | 10    |

**Explicit references captured (12 total):**
- GEN 17:1, 2, 4–8, 9–12, 14
- EXO 12:51; 13:1–3, 10–12, 14–16; 22:29
- EXO 14:15–18, 21–23, 27–29
- MIC 4:6, 7; 5:1–3
- ISA 8:1–4, 8–10
- ISA 19:1–5, 12, 16, 19–21
- MAT 10:32, 33, 37, 38; 19:27–30
- LUK 6:17–23; 10:22–24; 14:25–35
- JOH 5:17–30; 6:35–44, 48–54
- JOH 19:25–27; 21:24, 25
- 1CO 15:20–28, 39–57
- HEB 11:9, 10, 17–23, 32–40

## Data Quality Notes

**Known issues marked for review:**

1. **Implicit book assignments** (marked `needs_review: true`)
   - 295 of 307 entries are implicit references without explicit book names
   - Book assignment assumes sequential progression through OSB canon
   - Anchor points at explicit references help, but some assignments may be ambiguous
   - Genesis and Exodus contain the largest blocks of implicit refs

2. **Verse reference formats preserved as-is**
   - Unicode en-dash (`–`) preserved in ranges
   - Semicolon-separated alternative readings preserved (e.g., `13:1–3, 10–12, 14–16; 22:29`)
   - Some references may have malformed chapter-verse combos (e.g., `1:24-3`) from OCR

3. **Occasion text normalization**
   - Whitespace collapsed and trimmed
   - Trailing punctuation removed
   - Multi-line descriptions consolidated into single string

## Next Steps (Optional)

If higher precision needed:
1. Manual review of implicit Genesis/Exodus block to verify book transitions
2. Validate all 295 implicit references against OSB text structure
3. Normalize verse reference format (standardize range separators)
4. Split occasion text on conjunctions (`,` and `and`) to create multiple occasion entries
5. Add confidence scores per book assignment

## Files Generated

- `/home/ark/orthodoxphronema/reference/liturgical-crossrefs.json` (49 KB, 307 entries)
- `/home/ark/orthodoxphronema/parse_osb_liturgical.py` (reusable parser, 9 KB)
