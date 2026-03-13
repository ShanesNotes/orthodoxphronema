# PM Health Audit — Orthodox Phronema Archive

**Date:** 2026-03-10
**Author:** Project Manager (Claude)
**Type:** Full project health audit (read-only)
**Status:** Awaiting Human review

---

## 1. STRUCTURE CHECK — Canonical Spec vs. Reality

The canonical directory layout is defined in `memos/02_repository_folder_contract.md` (ratified 2026-03-06). The following compares that spec to what actually exists on disk.

### Directories matching spec (healthy)

| Directory | Spec | Actual | Status |
|---|---|---|---|
| `canon/OT/` | 49 books | 45 promoted `.md` files | Active — 4 pending |
| `canon/NT/` | 27 books | Empty (`.gitkeep`) | Expected — NT not yet started |
| `staging/validated/OT/` | Working buffer | 49 books + ~250 sidecar files | Healthy |
| `staging/validated/NT/` | Working buffer | Empty (`.gitkeep`) | Expected |
| `staging/raw/` | Docling output | Present with dev/test extractions | Healthy |
| `schemas/` | 3 core files | 5 files (3 core + 2 additions) | Healthy extension |
| `memos/` | Communication layer | 103 memos | Healthy |
| `reports/` | Validation evidence | 51 dossiers + 3 operational files | Healthy |
| `src.texts/` | Immutable sources | OSB PDF + Brenton + LXX datasets | Healthy |

### Structural drift: directories added beyond spec

| Directory | Purpose | Assessment |
|---|---|---|
| `pipeline/cleanup/` | Post-extraction fixes | Deliberate — complements parse/validate/promote |
| `pipeline/common/` | Shared utilities | Deliberate |
| `pipeline/tools/` | Batch/utility scripts | Deliberate |
| `pipeline/reference/` | Brenton/Greek indexing | Deliberate |
| `pipeline/metadata/` | Pericope generation | Deliberate |
| `staging/reference/` | Brenton/Greek witness files | Deliberate |
| `staging/quarantine/` | Per spec, now present | Healthy |
| `metadata/pericope_index/` | Liturgical reading boundaries | Deliberate Phase 2 prep |
| `reviews/` | Human review materials | Useful addition |
| `tests/` | Test suite | Essential addition |

**Verdict:** All pipeline extensions are purposeful and reflect operational maturity. No accidental sprawl detected. The spec should be amended to reflect the current reality.

### Structural drift: spec items missing or empty

| Item | Spec Requirement | Status | Severity |
|---|---|---|---|
| `canon/OT/BOOK_INDEX.md` | Ordered list with canon positions | Missing | LOW — metadata available in anchor_registry.json |
| `canon/NT/BOOK_INDEX.md` | Ordered list with canon positions | Missing | LOW — NT not yet started |
| `notes/OT/` | Mirrored footnote structure | Empty | MEDIUM — footnotes live in staging companions instead |
| `notes/NT/` | Mirrored footnote structure | Empty | LOW — NT not started |
| `articles/book_introductions/` | OSB introductions | Empty | MEDIUM — introductions not yet extracted from OSB |
| `articles/study_articles/` | OSB essays | Empty | MEDIUM — articles live in staging `_articles.md` companions |
| `articles/appendices/` | OSB appendix material | Empty | LOW — appendices not yet scoped |

**Key finding:** The `notes/` and `articles/` directories defined in the original spec remain empty because the project evolved to use staging-side companion files (`BOOK_articles.md`, `BOOK_footnotes.md`) instead. This is documented in Memo 53 and AGENTS.md. The spec should be updated to reflect this architectural decision — either populate `notes/` and `articles/` at promotion time, or officially retire them in favor of the companion model.

### Top-level file inventory

Present and expected: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `ARK_BRIEFING_PACKET.md`, `README.md`, `OSB-Page-Ranges.txt`, `pyproject.toml`, `uv.lock`, `.gitignore`

---

## 2. PROGRESS INVENTORY — Per-Book Completion

### Summary Statistics

| Tier | Books | % of 76 | Avg Completion |
|---|---|---|---|
| Promoted to canon | 45 | 59.2% | 95% |
| Editorially clean (promotion-ready) | 2 (PRO, SIR) | 2.6% | 75% |
| Structurally passable | 1 (JOB) | 1.3% | 60% |
| Staged but blocked | 1 (PSA) | 1.3% | 60% |
| Not yet extracted (NT) | 27 | 35.5% | 0% |
| **Overall project** | **76** | | **~59%** |

### OT Detailed Status (49 books)

#### Promoted (45 books — 95% each)

All have: staged `.md`, canon `.md`, `_articles.md`, `_footnotes.md`, `_footnote_markers.json`, promotion dossier.

| Group | Books | Validation | Notes |
|---|---|---|---|
| Pentateuch | GEN, EXO, LEV, NUM, DEU | PASS/WARN | Foundation books; GEN/EXO/LEV have detailed residue audits |
| Historical A | JOS, JDG, RUT, 1SA, 2SA | PASS/WARN | JOS has known chapter-20 structural debt per ops board |
| Historical B | 1KI, 2KI, 1CH, 2CH | PASS/WARN | 1KI has chapter drift documented in Memo 54 |
| Post-Exilic | 1ES, EZR, NEH | PASS/WARN | 1ES needs dossier refresh per ops board |
| Deuterocanon | TOB, JDT, EST, 1MA, 2MA, 3MA | PASS/WARN | Solid |
| Wisdom | ECC, SNG, WIS | PASS | WIS has legacy artifacts to clean up |
| Major Prophets | ISA, JER, BAR, LAM, LJE, EZK, DAN | PASS/WARN | Large books; all promoted |
| Minor Prophets | HOS, AMO, MIC, JOL, OBA, JON, NAH, HAB, ZEP, HAG, ZEC, MAL | PASS/WARN | All 12 promoted |

#### Not Yet Promoted (4 books)

| Book | Status | Completion | Blockers |
|---|---|---|---|
| PRO (Proverbs) | Editorially clean | 75% | Awaiting final review + promotion execution |
| SIR (Sirach) | Editorially clean | 75% | Awaiting final review + promotion execution |
| JOB (Job) | Structurally passable | 60% | 4 editorial candidates pending; V4/V7 warnings |
| PSA (Psalms) | Extracting | 60% | Missing `PSA_footnotes.md`; LXX numbering complexity |

### NT Status (27 books — all at 0%)

No NT books have been extracted. The staging and canon NT directories contain only `.gitkeep` placeholders. All 27 books (MAT through REV) remain in the extraction queue.

### Known Structural Holds (from Ezra ops board)

These promoted books carry documented structural debt that should be addressed:

| Book | Issue | Documented In |
|---|---|---|
| JOS | Chapter-20 absorption; marker/index desync | Memo 56 |
| 1KI | Chapter drift across ch. 10-15; stale markers | Memo 54 |
| 1ES | Stale dossier after marker recovery | Ops board |
| JDG, 1SA, 2SA | Governance-blocked on residual ratification | Memo 51 |

---

## 3. PHRONEMA CANDIDATES — Hyperlinking Inventory

### Content pattern density across the corpus

| Pattern | Files Found | Highest-Density Sources | Hyperlinking Potential |
|---|---|---|---|
| Saint references | 45 files | JOB_footnotes (55), SIR_footnotes (23), EZK_footnotes (17) | HIGH — patristic cross-references |
| Feast references | 32 files | EXO (6), 2MA_footnotes (6), DEU (5) | HIGH — liturgical calendar links |
| Liturgical references | 36 files | NUM_footnotes (38), NUM (33), LEV_footnotes (14) | HIGH — ritual law → liturgical practice |
| Marian references | 22 files | EXO_footnotes (9), EZK_footnotes (7), 1CH_footnotes (5) | HIGH — typological interpretation |
| Conciliar references | 19 files | PRO (5), JDT (5), PRO_footnotes (4) | MEDIUM — governance/authority themes |
| Hierarchical refs | 15 files | NUM_footnotes (5), GEN_footnotes (3) | MEDIUM — ecclesiology links |
| Martyr references | 13 files | JER_footnotes (3), 2MA_footnotes (3) | MEDIUM — hagiographical cross-refs |
| Liturgical hymns | 1 file | NUM_footnotes only | LOW — minimal at this stage |

### Existing cross-reference infrastructure

| Asset | Status | Notes |
|---|---|---|
| Link syntax `[[GEN.1:1]]` | Frozen (Memo 53) | Ready for use, not yet deployed |
| Backlink artifact path | Reserved | `metadata/anchor_backlinks/GEN.1.1.json` — deferred to Phase 2 |
| Pericope index | Genesis only | `metadata/pericope_index/GEN.json` — tool exists at `pipeline/metadata/generate_pericope_index.py` |
| Brenton reference index | 49 OT books | `staging/reference/brenton/*.json` |
| Greek reference index | 2 books | `staging/reference/greek/` (GEN, MATT) |
| Internal wiki-links (`[[`) | 0 files | Greenfield — no existing link syntax in any content file |

### Top 10 Phronema Hyperlinking Candidates (by annotation density)

1. JOB_footnotes.md — 55 saint refs, rich patristic commentary
2. NUM_footnotes.md — 38 liturgical + 5 hierarchical refs
3. NUM.md — 33 liturgical refs in scripture text
4. SIR_footnotes.md — 23 saint refs, wisdom tradition
5. EZK_footnotes.md — 17 saint + 7 Marian refs, temple theology
6. DAN_footnotes.md — 16 saint refs, apocalyptic/prophetic
7. SNG_footnotes.md — 15 saint refs, mystical theology
8. LEV_footnotes.md — 14 liturgical refs, priestly/sacramental
9. EXO_footnotes.md — 9 Marian + 6 feast refs, typology
10. 2MA_footnotes.md — 6 feast + 3 martyr refs, liturgical history

---

## 4. OPEN QUESTIONS — Unresolved Architectural Decisions

### Blocking (prevents next milestone)

| # | Question | Owner | Source | Impact |
|---|---|---|---|---|
| 1 | Should the empty `notes/` and `articles/` directories be populated at promotion, or officially retired in favor of staging companions? | Human + Ark | Spec drift analysis | Determines canon companion strategy |
| 2 | What is the path to promote PRO and SIR? Both are editorially clean. | Human | Ops board | 2 books waiting on decision |
| 3 | How should PSA's missing footnotes be resolved? | Ark | Memo 65, ops board | Blocks PSA promotion |
| 4 | Should JOS and 1KI structural resets happen before or after remaining OT promotions? | Ark | Memos 54, 56 | Affects promotion sequencing |

### Strategic (affects project direction)

| # | Question | Owner | Source |
|---|---|---|---|
| 5 | When does NT extraction begin? What is the trigger? | Human | Memo 25 long-horizon plan |
| 6 | Should the editorial gate become a formal validator or remain an audit sidecar? | Ark | Memo 26 |
| 7 | Legacy `_notes.md` assumptions persist in 4 pipeline files — clear in one pass or support alias period? | Ark | Memo 53 |
| 8 | Should the repo folder contract (Memo 02) be formally amended to reflect current reality? | Human + Ark | This audit |

### Deferred (Phase 2+)

| # | Question | Owner | Source |
|---|---|---|---|
| 9 | Backlink artifact implementation timing | Human | Memo 53 |
| 10 | Obsidian (Eve vault) integration approach | Human | Memo 01 |
| 11 | Pericope index expansion beyond Genesis | Ark | metadata/pericope_index/ |
| 12 | Patristic corpus acquisition and schema | Human | Memo 01, Phase 2 |

---

## 5. PROJECT ROADMAP — Prioritized Three-Phase Plan

### Phase 1: Structural Cleanup and OT Completion

**Goal:** All 49 OT books promoted to canon with clean companions. Spec drift resolved. NT extraction planned.

**Duration estimate:** 2-3 weeks

| Priority | Task | Owner | Blocked By | Done When |
|---|---|---|---|---|
| P0 | Promote PRO and SIR (both editorially clean) | Ark + Human | Human approval | Both in `canon/OT/` with dossiers |
| P0 | Resolve JOB editorial candidates (4 items) | Ark | Nothing | JOB promoted or blockers documented |
| P1 | Extract PSA footnotes | Ark | Nothing | `PSA_footnotes.md` exists and validates |
| P1 | JOS structural reset (chapter-20 absorption) | Ark | Nothing | JOS dossier refreshed, structural hold lifted |
| P1 | 1KI structural reset (chapter drift) | Ark | JOS learnings | 1KI markers and dossier aligned |
| P1 | 1ES dossier refresh | Ezra | Nothing | Dossier matches current staged state |
| P2 | Resolve JDG/1SA/2SA residual ratification | Human | Memo 51 packet | Governance hold lifted |
| P2 | Clean up WIS legacy artifacts | Ark | Nothing | `_notes.md`, `.bak`, `_pdftotext.txt`, `_raw_reextract.md` removed |
| P2 | Clear legacy `_notes.md` assumptions in pipeline code | Ark | Nothing | 4 files updated per Memo 53 |
| P3 | Amend Memo 02 folder contract to reflect current reality | Ark + Human | This audit | Spec matches disk |
| P3 | Generate `BOOK_INDEX.md` for canon/OT/ | Ark | Nothing | Index file exists with canon positions |
| P3 | Decide fate of empty `notes/` and `articles/` directories | Human | Nothing | Decision documented |
| P3 | Plan NT extraction sequence and probe session | Ark | OT cleanup stable | NT plan memo written |

**Phase 1 exit criteria:**
- 49/49 OT books promoted (or blockers formally documented and accepted)
- Zero stale dossiers or structural holds
- Folder contract amended
- NT extraction plan approved

---

### Phase 2: Phronema Content Tagging and Inventory

**Goal:** All phronema-relevant content (saints, feasts, liturgical references, Marian typology) tagged and indexed. Pericope index expanded. NT extraction underway.

**Duration estimate:** 4-6 weeks (overlaps with NT extraction)

| Priority | Task | Owner | Notes |
|---|---|---|---|
| P0 | Begin NT extraction — probe session (MAT, ROM, REV) | Ark | Validates pipeline for NT layout |
| P0 | NT bulk extraction — Gospels, then Epistles, then Revelation | Ark + Photius | Per Memo 25 groups 9-12 |
| P1 | Design phronema annotation schema | Ark + Human | Define tag vocabulary: saint, feast, liturgical, Marian, conciliar, martyr |
| P1 | Build phronema tag scanner | Ark | Automated extraction of tagged entities from footnotes/articles |
| P1 | Expand pericope index to all 49 OT books | Ark | Tool exists; run `generate_pericope_index.py` for each book |
| P2 | Build saint/feast entity index | Ark | Structured JSON: entity name → all referencing anchors |
| P2 | Tag top-10 highest-density footnote files (per Section 3) | Photius | Manual review + tag confirmation |
| P2 | Populate `articles/book_introductions/` from OSB | Photius | Extract introductions per book |
| P3 | Greek witness layer expansion | Ark | Extend `staging/reference/greek/` beyond GEN/MATT |

**Phase 2 exit criteria:**
- NT extraction complete (27/27 books in staging/validated/)
- Phronema tag schema ratified
- Entity index generated for OT footnotes
- Pericope index covers all 49 OT books

---

### Phase 3: Bidirectional Hyperlink Implementation

**Goal:** Dense, traceable links between scripture, footnotes, articles, saints, feasts, and liturgical readings. Full graph integrity.

**Duration estimate:** 6-8 weeks

| Priority | Task | Owner | Notes |
|---|---|---|---|
| P0 | Implement `[[BOOK.ch:v]]` link insertion in footnotes/articles | Ark | Syntax frozen per Memo 53 |
| P0 | Build backlink generator | Ark | Produces `metadata/anchor_backlinks/BOOK.ch.v.json` per the reserved contract |
| P1 | Cross-reference graph builder | Ark | Scripture → footnote → article → entity links |
| P1 | V9 link graph integrity validator | Ark | Per validation spec: every link resolves, no orphans |
| P2 | Liturgical calendar cross-linking | Ark | Pericope index → feast calendar → scripture anchors |
| P2 | Saint/feast entity pages | Ark | One page per entity with all back-references |
| P3 | Obsidian (Eve vault) integration | Human + Ark | Symlink or sync from canon to Obsidian vault |
| P3 | Full-text search and navigation layer | Ark | Anchor-based search across the corpus |

**Phase 3 exit criteria:**
- All footnotes and articles contain `[[BOOK.ch:v]]` links to scripture
- Backlink index generated for all 76 books
- V9 graph integrity passes with zero orphans
- Liturgical calendar cross-links operational
- Obsidian vault reads from canon

---

## Appendix A: Risk Register (Current)

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| PSA footnotes extraction fails due to LXX numbering complexity | HIGH | MEDIUM | Dedicated extraction session; leverage existing PSA_footnote_markers.json |
| JOS/1KI structural resets cascade into re-promotion | MEDIUM | MEDIUM | Isolate resets; test on JOS first |
| NT probe reveals parser incompatibility with NT layout | HIGH | LOW | Probe 3 diverse books before bulk |
| Legacy `_notes.md` code paths cause silent regression | LOW | MEDIUM | Clear in one bounded pass per Memo 53 |
| Phronema tagging scope creep delays NT extraction | MEDIUM | MEDIUM | Phase 2 tagging is parallel track, not blocking |
| Backlink implementation reveals anchor inconsistencies | MEDIUM | LOW | V3 anchor integrity already validated on all promoted books |

## Appendix B: Key Reference Documents

| Document | Path | Purpose |
|---|---|---|
| Architecture Memo v1 | `memos/01_architecture_memo_v1.md` | Core architectural decisions |
| Folder Contract | `memos/02_repository_folder_contract.md` | Canonical directory layout |
| Validation Spec | `memos/03_validation_spec.md` | V1–V11 check definitions |
| Agent Protocol | `AGENTS.md` | Role boundaries and workflow |
| Long-Horizon Plan | `memos/25_long_horizon_plan.md` | Full Phase 1–2 execution plan |
| Footnote Standards | `memos/53_footnote_workflow_and_link_standards_ratification.md` | Link syntax and companion file standards |
| Ezra Ops Board | `memos/ezra_ops_board.md` | Live queue and dispatch |
| Book Status Dashboard | `reports/book_status_dashboard.json` | Machine-readable book state |
| Ark Structural Audit | `research/ark-structural-audit-2026-03-10.md` | Same-day structural audit |

---

## Completion Block

| Surface | Status |
|---|---|
| **Files changed** | None (read-only audit) |
| **Verification run** | Cross-checked dashboard, dossiers, staged files, and canon against spec |
| **Artifacts refreshed** | N/A |
| **Remaining known drift** | Spec amendment needed (Memo 02); empty `notes/` and `articles/` require decision |
| **Next owner** | Human — review this report, approve roadmap priorities, decide open questions |
