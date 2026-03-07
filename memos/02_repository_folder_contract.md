# Repository + Folder Contract
**Author:** Ark | **Date:** 2026-03-06 | **Status:** RATIFIED 2026-03-06

---

## Decision

This document defines the canonical directory layout for `orthodoxphronema`. No directory outside this spec should be created without an amendment to this contract. No file should be placed in a directory that does not match its type.

---

## Full Tree

```
orthodoxphronema/
|
├── canon/                        # PROMOTED, VALIDATED content only
│   ├── OT/
│   │   ├── GEN.md                # One file per book
│   │   ├── EXO.md
│   │   ├── ... (49 OT books)
│   │   └── BOOK_INDEX.md         # Ordered list with canon positions
│   └── NT/
│       ├── MAT.md
│       ├── ... (27 NT books)
│       └── BOOK_INDEX.md
│
├── notes/                        # Study notes and footnotes (separated from canon)
│   ├── OT/
│   │   └── GEN_notes.md          # Mirrors canon structure
│   └── NT/
│       └── MAT_notes.md
│
├── articles/                     # OSB introductions, essays, appendices
│   ├── book_introductions/
│   ├── study_articles/
│   └── appendices/
│
├── schemas/                      # JSON schemas for validation
│   ├── scripture_frontmatter.json
│   ├── notes_frontmatter.json
│   └── anchor_registry.json      # Locked anchor → reference table
│
├── pipeline/                     # All ingestion and processing scripts
│   ├── parse/
│   │   └── docling_parse.py      # Docling-based PDF extractor
│   ├── validate/
│   │   ├── check_purity.py       # No commentary in canon files
│   │   ├── check_anchors.py      # All anchors resolve
│   │   ├── check_schema.py       # Frontmatter conforms to schema
│   │   └── check_completeness.py # All 76 books present
│   └── promote/
│       └── promote.py            # Moves validated → canon with commit
│
├── staging/                      # Ephemeral — never commit to canon directly
│   ├── raw/                      # Docling output, unvalidated
│   └── validated/                # Passed validation, awaiting promotion
│
├── reports/                      # Validation run outputs (committed for audit)
│   └── YYYY-MM-DD_validation.md
│
├── src.texts/                    # Raw source documents — IMMUTABLE after intake
│   └── the_orthodox_study_bible.pdf
│
├── memos/                        # Ark-to-human communication
│   └── *.md
│
├── CLAUDE.md                     # System directives
├── ARK_BRIEFING_PACKET.md        # Mission briefing
└── README.md                     # Project overview (human-facing)
```

---

## Directory Rules

| Directory | Rule |
|-----------|------|
| `canon/` | Only modified by the promote script via a deliberate commit. Never edited manually. |
| `notes/` `articles/` | May be edited, but all canon anchors referenced must exist and be validated before merge. |
| `staging/` | Never committed to canon directly. Contents are transient. |
| `src.texts/` | Add-only. Never modify or delete a source file. |
| `schemas/` | Changes require a version bump and migration plan. |
| `pipeline/` | Scripts are version-controlled; changes require testing on staging before use on canon. |
| `memos/` | Human-readable status and requests. Not part of the corpus. |

---

## Book Code Registry (76-Book Orthodox Canon)

The following table defines the authoritative book codes. **No anchor may be written until this table is ratified.**

### Old Testament (49 books — Septuagint/Orthodox canon)

| Code | Book | Notes |
|------|------|-------|
| GEN | Genesis | |
| EXO | Exodus | |
| LEV | Leviticus | |
| NUM | Numbers | |
| DEU | Deuteronomy | |
| JOS | Joshua | |
| JDG | Judges | |
| RUT | Ruth | |
| 1SA | 1 Samuel | |
| 2SA | 2 Samuel | |
| 1KI | 1 Kings | |
| 2KI | 2 Kings | |
| 1CH | 1 Chronicles | |
| 2CH | 2 Chronicles | |
| 1ES | 1 Ezra (1 Esdras) | Deuterocanonical — separate book per OSB TOC |
| EZR | 2 Ezra (Ezra) | OSB name: "2 Ezra" |
| NEH | Nehemiah | |
| TOB | Tobit | Deuterocanonical |
| JDT | Judith | Deuterocanonical |
| EST | Esther | Includes deuterocanonical additions |
| 1MA | 1 Maccabees | Deuterocanonical |
| 2MA | 2 Maccabees | Deuterocanonical |
| 3MA | 3 Maccabees | Deuterocanonical |
| 4MA | 4 Maccabees | APPENDIX ONLY — not counted in 76; not in OSB main TOC |
| PSA | Psalms | LXX numbering locked (PSA.1–PSA.151 incl. Ps 151) |
| PMN | Prayer of Manasseh | APPENDIX ONLY — appendix to 2CH, not counted in 76 |
| PRO | Proverbs | |
| ECC | Ecclesiastes | |
| SNG | Song of Songs | |
| JOB | Job | |
| WIS | Wisdom of Solomon | Deuterocanonical |
| SIR | Sirach | Deuterocanonical |
| HOS | Hosea | |
| AMO | Amos | |
| MIC | Micah | |
| JOL | Joel | Corrected from JOE per SBL standard |
| OBA | Obadiah | |
| JON | Jonah | |
| NAH | Nahum | |
| HAB | Habakkuk | |
| ZEP | Zephaniah | |
| HAG | Haggai | |
| ZEC | Zechariah | |
| MAL | Malachi | |
| ISA | Isaiah | |
| JER | Jeremiah | |
| BAR | Baruch | Deuterocanonical |
| LAM | Lamentations | |
| LJE | Letter of Jeremiah | Deuterocanonical |
| EZK | Ezekiel | |
| DAN | Daniel | Includes deuterocanonical additions |

### New Testament (27 books)

| Code | Book |
|------|------|
| MAT | Matthew |
| MRK | Mark |
| LUK | Luke |
| JOH | John |
| ACT | Acts |
| ROM | Romans |
| 1CO | 1 Corinthians |
| 2CO | 2 Corinthians |
| GAL | Galatians |
| EPH | Ephesians |
| PHP | Philippians |
| COL | Colossians |
| 1TH | 1 Thessalonians |
| 2TH | 2 Thessalonians |
| 1TI | 1 Timothy |
| 2TI | 2 Timothy |
| TIT | Titus |
| PHM | Philemon |
| HEB | Hebrews |
| JAS | James |
| 1PE | 1 Peter |
| 2PE | 2 Peter |
| 1JN | 1 John |
| 2JN | 2 John |
| 3JN | 3 John |
| JUD | Jude |
| REV | Revelation |

---

## Scripture File Frontmatter Schema

```yaml
---
book_code: GEN
book_name: Genesis
testament: OT
canon_position: 1          # Position in the 76-book Orthodox canon
source: OSB-v1             # Source identifier
parse_date: 2026-03-06
checksum: sha256:<hash>    # SHA-256 of the verse text body only
status: promoted           # staging | validated | promoted
---
```

**Rationale:** Checksum covers the verse text body only (not frontmatter), enabling detection of silent corruption or unauthorized edits.

**Risks:** Checksum must be recomputed and updated any time a correction is promoted. The promote script must automate this.

**Rollback:** Invalid frontmatter is caught by `check_schema.py` before promotion. Canon files are never touched if validation fails.

**Owner:** Ark (schema design) + Human (ratification)
