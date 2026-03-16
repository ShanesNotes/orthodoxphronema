# Archived Staging Companions

These files were moved from `staging/validated/{OT,NT}/` on 2026-03-15 as part of Lane 1 closure.

## Why archived

After Lane 1 closure, `study/` is the sole authoritative source for companion files (footnotes and articles). The staging copies are redundant and were causing dual-source confusion in the R1 extraction pipeline.

## What's here

- `OT/` — 49 books x 2 files (footnotes + articles) = 98 files
- `NT/` — 27 books x 2 files = 54 files
- Total: 152 archived companion files

## What remains in staging/validated/

- `BOOK.md` — staged scripture files (pre-promotion working copies)
- `BOOK_residuals.json` — source-ambiguity sidecars (needed by promotion gates)
- `BOOK_editorial_candidates.json` — editorial sidecars (needed by D1 gate)
- `BOOK_footnote_markers.json` — marker trace index (needed for footnote verification)

## Authoritative companion sources

- Footnotes: `study/footnotes/{OT,NT}/BOOK_footnotes.md`
- Articles: `study/articles/{OT,NT}/BOOK_articles.md`
- Lectionary notes: `study/lectionary-notes/{OT,NT}/BOOK_lectionary.md`
