# Phase 2 — Complete OSB Extraction & Repo Reorganization

**Date:** 2026-03-14
**Author:** Ark
**Status:** Plan — awaiting human approval

---

## Context

Phase 1 delivered:
- **Canon** (76 books): scripture text, fully proofread and immutable in `canon/`
- **Staging** (152 files): footnotes + study articles per book, cleaned and validated in `staging/validated/`

Phase 2 extracts everything else of value from the 12,301-page OSB PDF and reorganizes
the repository for maximal usefulness as a complete Orthodox study resource.

---

## 1. Page Range Manifest

### Currently Extracted (12,075 pages)

| Section | Pages | Count | Location |
|---------|-------|-------|----------|
| Scripture text (76 books) | 49–3943 | 3,893 | `canon/` |
| Footnotes & articles (76 books) | 4120–10409 | 6,290 | `staging/validated/` |
| "This passage is read at" notes | 10410–10774 | 365 | *identified, not yet parsed* |
| Hyperlinked appended notes | 10775–12301 | 1,527 | *identified, not yet parsed* |

### Unextracted Gaps (226 pages)

| Gap | Pages | Count | Content |
|-----|-------|-------|---------|
| **Front Matter** | 1–48 | 48 | See §2 below |
| **NT Divider** | 3076–3077 | 2 | Book list divider page (no extractable content) |
| **Back Matter Intro** | 3944–4119 | 176 | See §3 below |

### Total PDF: 12,301 pages. Accounted: 12,301. Truly unextracted valuable content: ~222 pages.

---

## 2. Front Matter Sections (pages 1–48)

| Priority | Section | Approx Pages | Extract? | Notes |
|----------|---------|-------------|----------|-------|
| — | Title page / Copyright | 1–2 | No | Legal boilerplate, already documented |
| — | Table of Contents | 3 | No | Structural; this memo supersedes |
| — | Acknowledgments | 4–5 | No | Credits list, low reference value |
| — | Special Recognition | 6 | No | Donor list |
| **A** | Introduction to the OSB | 7–11 | **Yes** | Editorial introduction explaining the OSB's purpose, translation methodology, LXX/NKJV sourcing, Jeremiah/Malachi verse mapping |
| **B** | OT Books Listed and Compared | 12–19 | **Yes** | Side-by-side comparison of Orthodox OT canon vs. Protestant/Catholic canons |
| **A** | Source Abbreviations | 20–24 | **Yes** | Patristic source abbreviation key used throughout all footnotes |
| **A** | Overview of the Books of the Bible | 25–32 | **Yes** | Bishop Basil's introduction to all 76 books (brief summary of each) |
| **A** | Introducing the Orthodox Church | 33–47 | **Yes** | History of Orthodoxy from NT through Great Schism to present — substantial essay |
| — | OT Divider Page | 48 | No | Book list only |

**Extractable front matter: ~40 pages across 5 sections.**

---

## 3. Back Matter Sections (pages 3944–4119 + 10410–12301)

### Gap between scripture and footnotes (pages 3944–4119, ~176 pages)

| Priority | Section | Approx Lines | Extract? | Notes |
|----------|---------|-------------|----------|-------|
| **A** | The Bible: God's Revelation to Man | ~435 | **Yes** | Essay by Bishop Joseph on reading Scripture in the Orthodox tradition |
| **A** | How to Read the Bible | ~500 | **Yes** | Essay by Bishop Kallistos Ware on the four characteristics of the Orthodox "Scriptural mind" |
| **A** | Lectionary | ~950 | **Yes** | Complete liturgical reading schedule (Triodion, Great Lent, Holy Week, Pascha, Pentecost, fixed feasts) — maps scripture readings to the Church calendar |
| **A** | Glossary | ~1,530 | **Yes** | Theological term definitions cross-referenced to scripture |
| **B** | Morning Prayers | ~124 | **Yes** | Daily prayer texts |
| **B** | Evening Prayers | ~74 | **Yes** | Daily prayer texts |
| **C** | Index to Annotations | ~1,786 | Review | Topic index pointing into footnotes — useful as metadata but may not need full extraction |
| **C** | Index to Study Articles | ~82 | Review | Article index — small enough to extract |
| **B** | The Seventy | ~92 | **Yes** | List of the 70 LXX translators |
| — | Illustrations | ~38 | No | Image references, not text content |
| — | Endnotes | ~2 | No | Minimal |

### Already-identified misc sections (pages 10410–12301)

| Priority | Section | Pages | Extract? | Notes |
|----------|---------|-------|----------|-------|
| **A** | "This passage is read at" notes | 10410–10774 | **Yes** | Liturgical cross-references linking scripture to feast days — high value for the lectionary |
| **B** | Hyperlinked appended notes | 10775–12301 | Review | Need probe extraction to assess content type and value |

---

## 4. Proposed Repository Structure

```
orthodoxphronema/
├── canon/                          # IMMUTABLE — 76 books, one-verse-per-line
│   ├── OT/                         #   49 OT books
│   └── NT/                         #   27 NT books
│
├── study/                          # ALL study material (replaces staging/validated/)
│   ├── footnotes/                  #   Per-book footnotes
│   │   ├── OT/                     #     GEN_footnotes.md, EXO_footnotes.md, ...
│   │   └── NT/                     #     MAT_footnotes.md, MRK_footnotes.md, ...
│   ├── articles/                   #   Per-book study articles
│   │   ├── OT/                     #     GEN_articles.md, EXO_articles.md, ...
│   │   └── NT/                     #     MAT_articles.md, MRK_articles.md, ...
│   ├── introductions/              #   Book introductions (if present in footnotes)
│   │   ├── OT/
│   │   └── NT/
│   └── lectionary-notes/           #   "This passage is read at" per-book cross-refs
│       ├── OT/
│       └── NT/
│
├── reference/                      #  NEW — standalone reference material
│   ├── introduction-to-osb.md      #   Editorial introduction
│   ├── ot-books-compared.md        #   Orthodox vs Protestant/Catholic canon comparison
│   ├── source-abbreviations.md     #   Patristic source abbreviation key
│   ├── overview-of-books.md        #   Bishop Basil's overview of all 76 books
│   ├── introducing-orthodoxy.md    #   History of the Orthodox Church essay
│   ├── bible-gods-revelation.md    #   Bishop Joseph's essay
│   ├── how-to-read-the-bible.md    #   Bishop Kallistos Ware's essay
│   ├── glossary.md                 #   Theological glossary
│   ├── lectionary.md               #   Full liturgical reading calendar
│   ├── the-seventy.md              #   The 70 LXX translators
│   └── prayers/
│       ├── morning-prayers.md
│       └── evening-prayers.md
│
├── metadata/                       #   Index and cross-reference data
│   ├── index-to-annotations.md     #   Topic index → footnote locations
│   └── index-to-articles.md        #   Article index
│
├── schemas/                        #   Anchor registry, biblical names, etc.
├── pipeline/                       #   Extraction and validation tools
├── skills/                         #   Text-cleaner, canon-proofreader, etc.
├── memos/                          #   Audit trail
├── staging/                        #   Working area (raw, quarantine, reference)
└── src.texts/                      #   Source PDFs (gitignored)
```

### Key Design Decisions

1. **`study/` replaces `staging/validated/`** — The name "staging" implies temporary.
   Promoted content belongs in a permanent home. The move happens after Phase 2
   extraction is complete and all content is cleaned.

2. **`study/` splits footnotes from articles** — Currently each book has `BOOK_footnotes.md`
   and `BOOK_articles.md` colocated. Separating them into `study/footnotes/` and
   `study/articles/` makes it easier to work with all footnotes or all articles at once.

3. **`reference/` is flat** — These are standalone essays and reference documents, not
   per-book material. A flat directory with descriptive filenames is clearest.

4. **`study/lectionary-notes/`** — The "this passage is read at" data is per-book and
   per-verse, so it belongs alongside footnotes and articles in `study/`.

5. **`metadata/`** — Indexes are cross-cutting reference data, not study material per se.

---

## 5. Extraction Plan (Ordered Phases)

### Phase 2a — Back Matter Essays (priority A, ~6 sections)

1. Extract pages 3944–4119 via Docling
2. Split into individual section files based on header detection
3. Run `text-cleaner --profile patristic` on each
4. Manual review pass for OCR artifacts
5. Place cleaned files in `reference/`

**Estimated effort:** 1 session. These are prose essays — straightforward extraction.

### Phase 2b — Front Matter Reference Sections (priority A/B, ~5 sections)

1. Extract pages 1–48 via Docling
2. Split into individual sections
3. Run text-cleaner with appropriate profile
4. Special handling for "OT Books Listed and Compared" (tabular data)
5. Special handling for "Source Abbreviations" (structured key-value data)
6. Place cleaned files in `reference/`

**Estimated effort:** 1 session. The tabular content (canon comparison, abbreviations)
may need manual formatting.

### Phase 2c — Lectionary Cross-References (priority A)

1. Extract pages 10410–10774 ("this passage is read at" notes)
2. Parse the per-verse liturgical assignments
3. Organize by book into `study/lectionary-notes/`
4. Cross-reference against the full lectionary in `reference/lectionary.md`

**Estimated effort:** 1–2 sessions. The parsing logic needs development — these are
structured cross-references, not prose.

### Phase 2d — Hyperlinked Appended Notes (priority B, needs probe)

1. Probe-extract a sample from pages 10775–10850 to assess content type
2. If valuable: full extraction and cleanup
3. If redundant with existing footnotes: document and skip

**Estimated effort:** 0.5 sessions for probe; 1–2 if extraction proceeds.

### Phase 2e — Repo Reorganization

1. Create the `study/` and `reference/` directory structure
2. Move `staging/validated/` content into `study/footnotes/` and `study/articles/`
3. Move extracted reference material into `reference/`
4. Update all pipeline scripts and profiles to reference new paths
5. Update `schemas/anchor_registry.json` with new paths
6. Update `ARCHITECTURE.md` and `README.md`
7. Git commit with full audit trail

**Estimated effort:** 1 session. This is a rename/restructure operation with script updates.

### Phase 2f — Validation Pass

1. Run text-cleaner across all newly extracted content
2. Run canon-validator on canon/ to confirm nothing was disturbed
3. Verify all cross-references between study material and canon
4. Write final Phase 2 audit memo

**Estimated effort:** 0.5 sessions.

---

## 6. Open Questions (for Human)

1. **Repo rename timing:** Should the `staging/validated/` → `study/` move happen now
   (before extraction) or after all Phase 2 content is extracted? Moving first is cleaner
   but means more path updates.

2. **Lectionary format:** The full lectionary calendar is complex (Triodion, Pentecostarion,
   fixed feasts, moveable feasts). Should we preserve it as prose markdown, or parse it
   into structured YAML/JSON for programmatic use?

3. **Glossary format:** Same question — prose markdown or structured data (term → definition
   mapping)?

4. **Indexes:** The Index to Annotations (~1,786 lines) and Index to Study Articles (~82 lines)
   are essentially lookup tables. Extract as markdown, or parse into JSON for search?

5. **Hyperlinked notes probe:** Should I proceed with probing pages 10775+ now, or defer
   until the higher-priority sections are done?

---

*Generated by Ark. Pending human review and approval before execution.*
