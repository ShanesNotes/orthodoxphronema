# Orthodox Phronema Archive — Project Knowledge Base

> **Purpose:** Condensed master reference for the claude.ai Project context window.
> **Date:** 2026-03-10 | **Version:** 1.0
> **Canonical sources:** Memos 01–03, 22, 25, 53, 60, AGENTS.md, ops board

---

## 1. What This Project Is

A structured, clean-source archive of Orthodox Christian theological content built from the Orthodox Study Bible (OSB). The core thesis: an immutable Scripture substrate with dense, traceable outward linkage into patristics, liturgics, and theology. The failure mode being engineered against is *contamination* — commentary bleeding into Scripture, broken references, and unrecoverable provenance.

---

## 2. Repository Structure (Canonical)

```
orthodoxphronema/
├── canon/                          # PROMOTED scripture only
│   ├── OT/BOOK.md                  # 45 of 49 OT books promoted
│   └── NT/                         # Empty — NT not yet extracted
│
├── staging/
│   ├── validated/{OT,NT}/          # Working scripture + companions
│   │   ├── BOOK.md                 # Staged scripture (one-verse-per-line)
│   │   ├── BOOK_articles.md        # Study articles / commentary blocks
│   │   ├── BOOK_footnotes.md       # Verse-linked footnotes
│   │   ├── BOOK_footnote_markers.json  # Marker trace sidecar
│   │   ├── BOOK_editorial_candidates.json  # Optional
│   │   ├── BOOK_dropcap_candidates.json    # Optional
│   │   └── BOOK_residuals.json     # Optional (ratified exceptions)
│   ├── raw/                        # Docling output, unvalidated
│   ├── reference/
│   │   ├── brenton/BOOK.json       # Auxiliary witness (49 OT)
│   │   └── greek/BOOK.json         # Greek source (GEN, MATT only)
│   └── quarantine/                 # Failed validation
│
├── pipeline/
│   ├── parse/                      # Extraction (Docling primary)
│   ├── validate/                   # V1–V8 checks
│   ├── promote/                    # Staging → canon gate
│   ├── cleanup/                    # Post-extraction fixes
│   ├── common/                     # Shared utilities
│   ├── tools/                      # Batch scripts
│   └── reference/                  # Brenton/Greek indexing
│
├── schemas/
│   ├── anchor_registry.json        # 76-book registry (v1.3.0)
│   ├── scripture_frontmatter.json
│   ├── notes_frontmatter.json
│   ├── residual_classes.json
│   └── greek_source_map.json
│
├── reports/
│   ├── book_status_dashboard.json  # Machine-readable live state
│   └── BOOK_promotion_dossier.json # Per-book promotion evidence
│
├── metadata/pericope_index/        # Liturgical reading boundaries
├── articles/                       # Placeholder (content in staging companions)
├── notes/                          # Placeholder (content in staging companions)
├── memos/                          # ~103 project memos
├── reviews/                        # Human review materials
├── tests/                          # Test suite
│
├── src.texts/
│   ├── the_orthodox_study_bible.pdf  # Canonical extraction source
│   ├── The-Orthodox-Study-Bible-Verification.pdf  # Secondary witness
│   ├── Brenton-Septuagint.txt/     # Auxiliary witness
│   ├── LXX-Rahlfs-1935/           # Greek LXX dataset
│   └── greektext-antoniades/       # Greek source text
│
├── AGENTS.md                       # Agent protocol (source of truth)
├── CLAUDE.md                       # Session directives
├── GEMINI.md                       # Photius control doc
└── ARK_BRIEFING_PACKET.md          # Mission briefing
```

---

## 3. Book Code Registry (76-Book Orthodox Canon)

### Old Testament (49 books)

**Pentateuch:** GEN, EXO, LEV, NUM, DEU
**Historical A:** JOS, JDG, RUT, 1SA, 2SA
**Historical B:** 1KI, 2KI, 1CH, 2CH
**Post-Exilic:** 1ES, EZR, NEH
**Deuterocanon Historical:** TOB, JDT, EST, 1MA, 2MA, 3MA
**Wisdom:** PSA, PRO, ECC, SNG, JOB, WIS, SIR
**Major Prophets:** ISA, JER, BAR, LAM, LJE, EZK, DAN
**Minor Prophets:** HOS, AMO, MIC, JOL, OBA, JON, NAH, HAB, ZEP, HAG, ZEC, MAL

### New Testament (27 books)

**Gospels:** MAT, MRK, LUK, JOH
**History:** ACT
**Pauline:** ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM
**General:** HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD
**Apocalyptic:** REV

### Special codes

4MA — Appendix only, not counted in 76.
PMN — Prayer of Manasseh, appendix to 2CH, not counted in 76.
PSA uses LXX numbering (Ps 1–151 including Ps 151).

---

## 4. Naming Conventions

**Book codes:** SBL-standard, UPPERCASE, 2–4 chars. Pattern: `^[A-Z0-9]{2,4}$`
**Anchor format:** `BOOK.CHAPTER:VERSE` (e.g., `GEN.1:1`, `PSA.118:1`, `MATT.5:3`)
**File naming:** `BOOK.md`, `BOOK_articles.md`, `BOOK_footnotes.md`, `BOOK_footnote_markers.json`
**Legacy:** `BOOK_notes.md` is transitional; new work targets `_articles.md` + `_footnotes.md`
**Cross-text link syntax (frozen):** `[[GEN.1:1]]` for authored Markdown; plain tokens in machine fields
**Backlink artifact path (reserved):** `metadata/anchor_backlinks/GEN.1.1.json`

---

## 5. Scripture File Format

```yaml
---
book_code: GEN
book_name: Genesis
testament: OT
canon_position: 1
source: OSB-v1
parse_date: 2026-03-06
checksum: sha256:<hash>    # verse text body only
status: promoted           # staging | validated | promoted
---

## Chapter 1

GEN.1:1 In the beginning God made heaven and earth.
GEN.1:2 The earth was invisible and unfinished...
```

**Constraints:** One-verse-per-line. No footnotes, cross-references, or commentary in scripture files. Footnote markers stripped and indexed in JSON sidecars. Study articles separated into companion files.

---

## 6. Pipeline and Validation

### Pipeline flow

```
src.texts/osb.pdf → [Docling] → staging/raw/ → [Validate] → staging/validated/ → [Promote] → canon/
```

### Extraction method selection

| Content | Primary tool | Fallback |
|---|---|---|
| Scripture pages | Docling | pdftotext (edge cases) |
| Notes/footnotes pages | pdftotext | Docling (debugging) |

### Validation checks (hard gates)

| Check | What it validates |
|---|---|
| V1 | Anchor uniqueness |
| V2 | Chapter count |
| V3 | Chapter sequence |
| V4 | Verse sequence / gap detection |
| V5 | Article bleed (study note contamination) |
| V6 | Frontmatter conformance |
| V7 | Completeness |
| V8 | Heading integrity |

### Promotion gate (all required)

1. Ark implementation complete
2. Validation run recorded
3. Ezra audit complete or explicitly waived
4. Human ratification of ambiguous cases
5. Ark promotion run from the same staged file

---

## 7. Source Authority

| Source | Role |
|---|---|
| OSB PDF (`the_orthodox_study_bible.pdf`) | Canonical extraction source |
| OSB Verification scan | Secondary OSB witness (manual only) |
| Brenton Septuagint | Auxiliary witness — confidence scoring only |
| Greek texts (Rahlfs/Antoniades) | Auxiliary witness — explanatory only |
| LLM inference | Proposal/ranking layer only, never authoritative |

**OSB immutability policy (Memo 22):** Canon artifacts are OSB-faithful. If both OSB witnesses omit a verse, classify it as source-absence. Never insert from auxiliary witnesses without explicit human exception.

---

## 8. Agent Protocol

| Agent | Role | Default scope |
|---|---|---|
| **Ark** | Architecture, core pipeline, promotion | Sole default writer/committer for canon-affecting work |
| **Ezra** | Strategic lead, audit, throughput | Analyze, validate, report, delivery ops, one engineering lane max |
| **Photius** | Parsing, staging recovery, cleanup | Bounded writes to staging/validated/ and pipeline/cleanup/ |
| **Human** | Adjudication, promotion approval, role changes | Final authority on ambiguous cases |

**WIP limits:** Ark: 1 core lane. Photius: 2 cleanup lanes or 1 batch + 1 book. Ezra: 1 audit queue + 1 ops board + 1 engineering lane max.

**Completion handshake (Memo 60):** Work is done when state, evidence, and handoff agree. Required surfaces: durable memo, verification run, affected artifacts refreshed or deferred.

---

## 9. Current Project Status (2026-03-10)

### Overall: ~59% complete

| Status | Count | Books |
|---|---|---|
| Promoted to canon | 45 | All OT except PRO, SIR, JOB, PSA |
| Editorially clean | 2 | PRO, SIR |
| Structurally passable | 1 | JOB |
| Staged but blocked | 1 | PSA (missing footnotes) |
| Not extracted (NT) | 27 | All NT books |

### Known structural holds on promoted books

| Book | Issue | Memo |
|---|---|---|
| JOS | Chapter-20 absorption, marker desync | 56 |
| 1KI | Chapter drift ch. 10-15, stale markers | 54 |
| 1ES | Stale dossier after marker recovery | Ops board |
| JDG, 1SA, 2SA | Governance-blocked on residual ratification | 51 |

---

## 10. Phase Roadmap

### Phase 1 — OT Completion (current)

Promote PRO, SIR, JOB. Extract PSA footnotes. Resolve structural holds on JOS, 1KI. Amend folder contract. Plan NT extraction.

### Phase 2 — NT Extraction + Phronema Tagging

NT probe session (MAT, ROM, REV) → bulk extraction. Design phronema annotation schema (saints, feasts, liturgical, Marian). Expand pericope index. Build entity index from footnotes.

### Phase 3 — Bidirectional Hyperlinking

Insert `[[BOOK.ch:v]]` links. Build backlink generator. V9 graph integrity. Liturgical calendar cross-links. Obsidian integration.

---

## 11. Open Decisions Requiring Human Action

1. Approve PRO and SIR for promotion (both editorially clean)
2. Decide fate of empty `notes/` and `articles/` dirs (populate at promotion vs. retire)
3. Ratify JDG/1SA/2SA residuals (Memo 51 packet)
4. Set NT extraction trigger (when to begin)
5. Amend Memo 02 folder contract to reflect current reality

---

## 12. Key Architectural Invariants

These are non-negotiable unless explicitly changed by Human:

- One-verse-per-line in canon
- Study article text must not appear in canon scripture files
- Footnote markers stripped from canon and indexed separately
- OSB is the sole canonical source; auxiliary witnesses are informational only
- `anchor_registry.json` is a controlled source of truth
- Changes to canonical workflow prefer tightening invariants over convenience
- Single writer (Ark), explicit handoff, durable evidence
- No content transitions between stages without passing all validation checks

---

## 13. Memo Index (Key Documents Only)

| Memo | Title | Status | Purpose |
|---|---|---|---|
| 01 | Architecture Memo v1 | Proposed | Core architecture decisions |
| 02 | Repository Folder Contract | Ratified | Canonical directory layout |
| 03 | Validation Spec | Proposed | V1–V11 check definitions |
| 22 | OSB Immutability Policy | In review | Source authority hierarchy |
| 25 | Long-Horizon Plan | Active | Phase 1+2 execution plan |
| 53 | Footnote/Link Standards | Implemented | Companion files, link syntax |
| 60 | Completion Handshake | Implemented | Agent done-definition protocol |
| — | AGENTS.md | Active | Agent roles, ownership, workflow |
| — | Ezra Ops Board | Active | Live queue and dispatch |
| — | book_status_dashboard.json | Active | Machine-readable book state |
