# NT Page Range Probe Request — 2026-03-10

**Author:** `ark`
**Type:** `decision`
**Status:** `draft`
**Scope:** NT extraction bootstrap (Phase 4)

## Context
- OT extraction nearly complete (45/49 promoted).
- NT extraction requires accurate page ranges in `schemas/anchor_registry.json`.
- Registry has start/end pages for NT books but NO confirmed `text_start` values.
- OSB has ~35-44 pages of navigation index before actual verse text per book (confirmed OT pattern).
- Known anchor: 2TH text_start listed as ~3278 (needs verification).

## Objective
- Human probes OSB PDF for text-start page of each NT book.
- Probe method: open PDF to registry `page_start`, scan forward to first verse of chapter 1.
- Record the page number where actual verse text begins (not navigation/index pages).

## NT Books Requiring Page Probes (27 books)

| Code | Book Name | Registry page_start | text_start (TBD) |
|---|---|---|---|
| MAT | Matthew | 3052 | ? |
| MRK | Mark | 3128 | ? |
| LUK | Luke | 3175 | ? |
| JOH | John | 3260 | ? |
| ACT | Acts | 3329 | ? |
| ROM | Romans | 3418 | ? |
| 1CO | 1 Corinthians | 3462 | ? |
| 2CO | 2 Corinthians | 3506 | ? |
| GAL | Galatians | 3537 | ? |
| EPH | Ephesians | 3558 | ? |
| PHP | Philippians | 3579 | ? |
| COL | Colossians | 3596 | ? |
| 1TH | 1 Thessalonians | 3612 | ? |
| 2TH | 2 Thessalonians | 3626 | ? |
| 1TI | 1 Timothy | 3636 | ? |
| 2TI | 2 Timothy | 3655 | ? |
| TIT | Titus | 3668 | ? |
| PHM | Philemon | 3678 | ? |
| HEB | Hebrews | 3684 | ? |
| JAS | James | 3721 | ? |
| 1PE | 1 Peter | 3739 | ? |
| 2PE | 2 Peter | 3756 | ? |
| 1JO | 1 John | 3769 | ? |
| 2JO | 2 John | 3786 | ? |
| 3JO | 3 John | 3791 | ? |
| JDE | Jude | 3796 | ? |
| REV | Revelation | 3804 | ? |

**Note:** Page numbers are from anchor_registry.json. Verify against actual PDF.

## Also Needed: CVC for 1CO and EPH
- `chapter_verse_counts` is null for these two books in the registry.
- Standard source: count verses per chapter from a reference Bible or online concordance.

## Probe Instructions
1. Open `src.texts/the_orthodox_study_bible.pdf`
2. Navigate to `page_start` for each book
3. Scan forward until you see the first verse of Chapter 1
4. Record that page number as `text_start`
5. Optionally note `text_end` (last verse page before next book's nav section)

**Priority:** Start with Gospels (MAT, MRK, LUK, JOH) for pilot extraction.

## Handoff
**To:** `human`
**Ask:** Probe at least the 4 Gospels' text_start pages. Full 27-book probe when convenient.
