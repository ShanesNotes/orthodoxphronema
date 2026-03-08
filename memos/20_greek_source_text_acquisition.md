# Memo 20: Greek Source Text Acquisition — 2026-03-08

**Author:** `ark`
**To:** `ezra`, `human`
**Type:** `planning`
**Status:** `active`
**Scope:** `Phase 2 infrastructure / Greek witness texts`

## Summary

Two open-source Greek text repositories have been cloned into `src.texts/` to serve as upstream witnesses for the Orthodox canon. These will enable Greek↔English alignment, verse-level cross-referencing, and eventual display of parallel Greek text alongside the OSB English extraction.

## Repositories Acquired

### 1. OT: Rahlfs 1935 LXX
- **Repo:** `eliranwong/LXX-Rahlfs-1935`
- **Local path:** `src.texts/LXX-Rahlfs-1935/`
- **License:** Public domain (1935 edition)
- **Format:** Word-level CSV (`text_accented.csv`, 623,693 words) + SQLite verse databases (`LXX1.SQLite3`: 54 books, 28,861 verses)
- **Script:** Full polytonic Greek with accents, breathings, and iota subscripts
- **Coverage:** 54 primary books + 6 variant recensions (OG and Theodotion for Daniel/Susanna/Bel; two Tobit recensions; two Joshua/Judges recensions)
- **Versification:** `08_versification/` contains Rahlfs→NRSV mapping tables (6,790 entries). Rahlfs uses LXX numbering throughout, which aligns with OSB numbering.

### 2. NT: 1904 Patriarchal Text (Antoniades)
- **Repo:** `byztxt/greektext-antoniades`
- **Local path:** `src.texts/greektext-antoniades/`
- **License:** Public domain (1904 edition)
- **Format:** Verse-level plaintext, `chapter:verse text` per line — immediately indexable
- **Script:** Monotonic lowercase (no accents or breathings)
- **Coverage:** 27 NT books (complete)
- **Book codes:** Non-standard (`MT`, `MR`, `LU`, `JOH`, `AC`, `RE`, etc.) — need mapping to our registry codes

## Canon Coverage vs Our 76-Book Scope

| Scope | Source | Coverage | Gaps |
|-------|--------|----------|------|
| 49 OT books | Rahlfs LXX | All 49 covered | Prayer of Manasseh likely folded into Odes |
| 27 NT books | Antoniades 1904 | All 27 covered | None |
| Bonus | Rahlfs | Psalms of Solomon, Odes | Not in our 76-book scope but available |

## Technical Assessment

### What's Ready Now
- **NT text is immediately usable.** Clean verse-per-line format. Only needs a book-code mapping table (e.g., `MT`→`MATT`, `RE`→`REV`).
- **LXX SQLite path is fastest.** `LXX1.SQLite3` has verse-level text with inline morphology markup (`<S>`, `<m>` tags) that can be stripped with a simple regex. No word-reassembly needed.
- **LXX versification aligns with OSB.** Both use LXX numbering, so Psalm/chapter offsets should be minimal. The mapping tables in `08_versification/` document known divergences.

### What Needs Work
1. **Book-code mapping table** — Both repos use different codes than our `anchor_registry.json`. A mapping file is needed before any indexing.
2. **NT accent restoration** — The Antoniades text is monotonic lowercase. For display-quality Greek, accents/breathings would need to be restored (either from a lookup table or a separate accented source). For alignment/reference purposes, unaccented is sufficient.
3. **Versification mapping** — While LXX↔OSB is largely aligned, specific divergences exist:
   - Psalms: LXX Ps 9 = MT Ps 9–10; LXX Ps 113 = MT Ps 114–115; etc.
   - Genesis 31–32: verse numbering differs between LXX and MT
   - Daniel: OSB uses Theodotion (DanTh) — the repo provides both OG and Th
4. **SQLite markup stripping** — LXX verses contain inline Strong's/morphology tags that need removal for plain text
5. **Prayer of Manasseh** — May be embedded in Odes; needs verification

## Relevance to OSB Source Fidelity

The OSB translation is based on:
- **OT:** Rahlfs 1935 LXX (this exact edition)
- **NT:** 1904 Patriarchal Text (this exact edition)

This means these Greek texts are the **direct upstream sources** for the English text we're extracting. They can serve as:
- **Verse existence witness:** Confirm whether a verse "missing" from our extraction actually exists in the Greek (vs. being a Docling parsing gap)
- **Verse boundary witness:** Confirm where verse splits should occur in fused-text passages
- **Content witness:** Cross-check OCR artifacts against the Greek original
- **Future parallel display:** Greek + English side-by-side in the archive

## Open Questions for Ezra

1. **Integration priority:** Should Greek indexing wait until Phase 1 English extraction is complete (all 76 books), or should we build the Greek index now as a verification tool for the remaining books?
2. **Accent policy for NT:** Accept monotonic as-is for reference, or require accent restoration before any Greek text enters the archive?
3. **Daniel recension:** OSB uses Theodotion — should we index only DanTh, or both OG and Th for scholarly completeness?
4. **Scope boundary:** Psalms of Solomon and Odes are available but outside our 76-book canon. Include as bonus or exclude?
5. **Verse mapping table:** Should the versification mapping live in `schemas/` (alongside anchor_registry) or in `staging/reference/`?

## Open Questions for Human

- **Storage:** The LXX repo is 673 MB (mostly SQLite). Should we gitignore the SQLite databases and only commit extracted plaintext indexes?
- **Next extraction priority** still open from memo 19: LEV/NUM (OT stress test) vs short NT book (cross-testament proof)?

## Proposed Next Steps (pending review)

1. Build book-code mapping table (`schemas/greek_book_codes.json`)
2. Extract verse-level plaintext from LXX SQLite (strip markup, write to `staging/reference/greek_lxx/BOOK.json`)
3. Index NT Antoniades into same format (`staging/reference/greek_nt/BOOK.json`)
4. Build versification mapping for Psalms and other divergent books
5. Use Greek verse counts as independent witness for `chapter_verse_counts` in the registry (especially the 12 books still missing CVC data)

## Files

| Path | Description |
|------|-------------|
| `src.texts/LXX-Rahlfs-1935/` | Rahlfs LXX repo (673 MB) |
| `src.texts/greektext-antoniades/` | Antoniades NT repo |
| `src.texts/LXX-Rahlfs-1935/01_wordlist_unicode/text_accented.csv` | Full polytonic word list |
| `src.texts/LXX-Rahlfs-1935/11_end-users_files/MyBible/Bibles/LXX1.SQLite3` | Verse-level LXX database |
| `src.texts/greektext-antoniades/textonly/unicode/` | 27 NT books, verse-per-line |
| `src.texts/LXX-Rahlfs-1935/08_versification/` | Verse mapping tables |
