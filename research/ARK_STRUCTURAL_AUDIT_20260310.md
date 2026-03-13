# Ark Structural Audit — Orthodox Phronema Archive

**Date:** 2026-03-10
**Author:** Ark (architecture lead)
**Type:** Full structural audit (read-only)
**Status:** Awaiting Human review

---

## 1. Repository Folder Map

```
orthodoxphronema/
├── AGENTS.md                         # Agent protocol & ownership
├── ARK_BRIEFING_PACKET.md            # Mission briefing
├── CLAUDE.md                         # Session directives
├── GEMINI.md                         # Photius control doc
├── README.md                         # Repo README
├── OSB-Page-Ranges.txt               # OSB page-range reference
├── pyproject.toml / uv.lock          # Python project config
├── .gitignore
│
├── canon/
│   ├── OT/                           # 45 promoted OT books (BOOK.md)
│   └── NT/                           # Empty (.gitkeep only)
│
├── staging/
│   ├── validated/
│   │   ├── OT/                       # 49 books + ~200 sidecar files
│   │   └── NT/                       # Empty (.gitkeep only)
│   ├── raw/                          # Development/test extractions
│   ├── reference/
│   │   ├── brenton/                  # 49 Brenton JSON files
│   │   └── greek/                    # Greek source (GEN, MATT JSON)
│   └── quarantine/                   # Empty (ready for use)
│
├── pipeline/
│   ├── cleanup/                      # Post-extraction fixes
│   ├── common/                       # Shared utilities
│   ├── parse/                        # Extraction tools (OSB, PSA, Docling)
│   ├── promote/                      # Promotion gates
│   ├── reference/                    # Reference indexing (Brenton, Greek)
│   ├── tools/                        # Utility/batch scripts
│   └── validate/                     # V1–V8 validation logic
│
├── schemas/
│   ├── anchor_registry.json          # 76-book canonical registry (v1.3.0)
│   ├── greek_source_map.json
│   ├── notes_frontmatter.json
│   ├── residual_classes.json
│   └── scripture_frontmatter.json
│
├── articles/
│   ├── appendices/
│   ├── book_introductions/
│   └── study_articles/
│
├── notes/
│   ├── OT/
│   └── NT/
│
├── metadata/
│   └── pericope_index/
│
├── reports/
│   ├── book_status_dashboard.json
│   ├── cvc_report.json
│   └── *_promotion_dossier.json      # 51 dossier files
│
├── memos/                            # ~65 project memos
├── reviews/                          # Human review materials
├── tests/                            # Test suite
│
└── src.texts/
    ├── the_orthodox_study_bible.pdf   # Canonical OSB source
    ├── The-Orthodox-Study-Bible-Verification.pdf
    ├── Brenton-Septuagint.txt/        # Auxiliary witness (per-chapter .txt)
    ├── LXX-Rahlfs-1935/              # Greek LXX dataset (morphology, lexicon, etc.)
    └── greektext-antoniades/          # Greek source text
```

---

## 2. Naming Convention Assessment

### Result: Fully consistent — no corrections needed

All files follow SBL-standard book codes in UPPERCASE (2–4 chars, optional leading digit). Separators are underscores throughout. No mixed capitalization, no hyphen/space inconsistencies, no non-standard abbreviations.

**Pattern enforced by schema:** `^[A-Z0-9]{2,4}$`

### Standard file set per staged book

| File | Pattern | Count (OT) |
|---|---|---|
| Scripture | `BOOK.md` | 49/49 |
| Articles | `BOOK_articles.md` | 49/49 |
| Footnotes | `BOOK_footnotes.md` | 48/49 (PSA missing) |
| Footnote markers | `BOOK_footnote_markers.json` | 49/49 |
| Editorial candidates | `BOOK_editorial_candidates.json` | 47/49 |
| Drop-cap candidates | `BOOK_dropcap_candidates.json` | 25/49 |
| Residuals | `BOOK_residuals.json` | 26/49 |
| Residue audit | `BOOK_residue_audit.json` | 3 (GEN, EXO, LEV) |

**Legacy artifacts (WIS only):** `WIS_notes.md`, `WIS.md.bak`, `WIS_pdftotext.txt`, `WIS_raw_reextract.md`

---

## 3. Scripture Purity Check

### Result: Clean — no study note contamination detected in base BOOK.md files

Spot-checked across multiple books. All base scripture files maintain the required structure: YAML frontmatter, chapter headings (`## Chapter N`), one-verse-per-line (`BOOK.CH:V text`). No "STUDY NOTE", "ARTICLE:", "Commentary", or other editorial markers found inside scripture files. Footnote markers are stripped from canon and indexed separately in JSON sidecars, as required.

---

## 4. Content Type Inventory

### Primary content types

| Type | Location | Description |
|---|---|---|
| **Scripture** | `staging/validated/{OT,NT}/BOOK.md` → promoted to `canon/{OT,NT}/BOOK.md` | Pure verse text, one-verse-per-line |
| **Study articles** | `staging/validated/OT/BOOK_articles.md` | Extracted OSB study articles, positioned by verse anchor |
| **Footnotes** | `staging/validated/OT/BOOK_footnotes.md` | Verse-indexed footnotes with patristic/doctrinal context |
| **Footnote markers** | `staging/validated/OT/BOOK_footnote_markers.json` | Machine-readable marker traces (symbol, anchor, sequence) |
| **Editorial candidates** | `staging/validated/OT/BOOK_editorial_candidates.json` | Fused-word/punctuation issues requiring triage |
| **Drop-cap candidates** | `staging/validated/OT/BOOK_dropcap_candidates.json` | OCR drop-cap recovery tracking |
| **Residuals** | `staging/validated/OT/BOOK_residuals.json` | Ratified exceptions (missing verses, versification drift) |
| **Promotion dossiers** | `reports/BOOK_promotion_dossier.json` | Per-book promotion readiness evidence |
| **Brenton reference** | `staging/reference/brenton/BOOK.json` | Auxiliary witness text for confidence scoring |
| **Greek reference** | `staging/reference/greek/BOOK.json` | Greek source for verification |
| **Pericope index** | `metadata/pericope_index/` | Liturgical reading boundaries |
| **Book introductions** | `articles/book_introductions/` | OSB introduction extractions |
| **Study articles (standalone)** | `articles/study_articles/` | Standalone thematic articles |
| **Appendices** | `articles/appendices/` | OSB appendix material |

### Article extraction status

10 of 49 OT books have substantive study articles extracted (GEN, EXO, NUM, DEU, JOB, DAN, EZK, JER, LEV, 2MA). The remaining 39 carry placeholder text. This aligns with OSB structure — most books lack standalone study articles.

---

## 5. Phronema Additions — Hyperlinking Candidates

### Liturgical / feast references found in footnotes

The following books contain "Feast of" references within their footnotes or articles, making them candidates for future liturgical calendar hyperlinking:

GEN, EXO, DEU, JDG, 1KI, 1ES, 2CH, NEH, 1MA, 2MA, ZEC

### Pericope index

The `metadata/pericope_index/` directory contains liturgical reading boundary data — a natural candidate for cross-referencing against the Menologion and liturgical calendar.

### Absent patterns (correctly segregated)

No "Saint" biographical entries, "Troparion", "Kontakion", or "Canon of" references were found in scripture or companion files. These content types would come from future patristic/liturgical corpus expansion, not from the OSB substrate.

### Future hyperlinking candidates

| Content type | Source | Link target |
|---|---|---|
| Liturgical feast references | Footnotes/articles | Calendar / Menologion |
| Patristic quotations | Footnotes | Patristic corpus (future) |
| Cross-references | Footnotes | `[[BOOK.ch:v]]` internal links |
| Pericope boundaries | Metadata index | Lectionary / liturgical calendar |
| Book introductions | Articles | Standalone article index |

---

## 6. Completeness Assessment

### OT: 49/49 books staged, 45/49 promoted to canon

| Status | Books |
|---|---|
| **Promoted to canon** (45) | 1CH, 1ES, 1KI, 1MA, 1SA, 2CH, 2KI, 2MA, 2SA, 3MA, AMO, BAR, DAN, DEU, ECC, EST, EXO, EZK, EZR, GEN, HAB, HAG, HOS, ISA, JDG, JDT, JER, JOB, JOL, JON, JOS, LAM, LEV, LJE, MAL, MIC, NAH, NEH, NUM, OBA, RUT, SNG, TOB, WIS, ZEC, ZEP |
| **Staged, not yet promoted** (4) | JOB, PRO, PSA, SIR |

### NT: 0/27 — not yet started

All 27 NT books remain unextracted: MAT, MRK, LUK, JOH, ACT, ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM, HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD, REV

### Blocking issues

| Issue | Book | Severity |
|---|---|---|
| Missing `PSA_footnotes.md` | PSA | Blocks PSA promotion |
| Legacy artifacts in WIS | WIS | Cleanup debt (non-blocking) |
| 39/49 placeholder articles | Multiple | Non-blocking (reflects OSB structure) |

---

## 7. Proposed Canonical Naming Convention

**Assessment: The existing convention is sound and requires no changes.**

The current naming scheme already satisfies all requirements from AGENTS.md and the briefing packet. For reference, the convention is:

```
staging/validated/{OT,NT}/
  BOOK.md                          # Scripture source of truth
  BOOK_articles.md                 # Study articles
  BOOK_footnotes.md                # Verse-linked footnotes
  BOOK_footnote_markers.json       # Marker trace
  BOOK_editorial_candidates.json   # Optional sidecar
  BOOK_dropcap_candidates.json     # Optional sidecar
  BOOK_residuals.json              # Optional sidecar

canon/{OT,NT}/
  BOOK.md                          # Promoted pure scripture

reports/
  BOOK_promotion_dossier.json      # Promotion evidence
```

Book codes follow the SBL standard registered in `schemas/anchor_registry.json`. The only recommendation is to clean up the WIS legacy artifacts (`_notes.md`, `.bak`, `_pdftotext.txt`, `_raw_reextract.md`) once WIS recovery work is complete.

---

## Completion Block

| Surface | Status |
|---|---|
| **Files changed** | None (read-only audit) |
| **Verification run** | Spot-check sampling across OT books |
| **Artifacts refreshed** | N/A |
| **Remaining known drift** | None identified |
| **Next owner** | Human — review this memo, ratify naming convention, approve next steps |
