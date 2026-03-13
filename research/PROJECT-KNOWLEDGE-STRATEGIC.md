# Orthodox Phronema Archive — Strategic Reference

> Timeless architectural spec for the claude.ai Project context window.
> Contains only durable decisions. No operational status, no current holds, no transient counts.

---

## 1. Project Purpose

The Orthodox Phronema Archive is a structured, clean-source archive of Orthodox Christian theological content built from the Orthodox Study Bible (OSB). It is a text graph rooted in an immutable Scripture substrate, with dense, traceable outward linkage into patristics, liturgics, and theology.

The failure mode being engineered against is *contamination*: commentary bleeding into Scripture, references that break silently, and provenance that cannot be reconstructed.

The repository (`orthodoxphronema`) is the single canonical source of truth. Git provides immutable, auditable commit history. Plain-text files (Markdown + YAML frontmatter) are diff-able, human-readable, and tool-agnostic.

---

## 2. Repository Structure

```
orthodoxphronema/
├── canon/{OT,NT}/BOOK.md           # Promoted, validated scripture only
├── staging/
│   ├── validated/{OT,NT}/          # Working scripture + companions
│   │   ├── BOOK.md                 #   Staged scripture
│   │   ├── BOOK_articles.md        #   Study articles
│   │   ├── BOOK_footnotes.md       #   Verse-linked footnotes
│   │   └── BOOK_footnote_markers.json  # Marker trace sidecar
│   ├── raw/                        # Parser output, unvalidated
│   ├── reference/{brenton,greek}/  # Auxiliary witness files
│   └── quarantine/                 # Failed validation
├── pipeline/
│   ├── parse/                      # Extraction tools
│   ├── validate/                   # Validation checks
│   ├── promote/                    # Staging → canon gate
│   ├── cleanup/                    # Post-extraction fixes
│   ├── common/                     # Shared utilities
│   ├── tools/                      # Batch scripts
│   └── reference/                  # Witness indexing
├── schemas/                        # anchor_registry.json + frontmatter schemas
├── reports/                        # Dashboard + per-book promotion dossiers
├── metadata/pericope_index/        # Liturgical reading boundaries
├── memos/                          # Project memos
├── src.texts/                      # Immutable source documents (add-only)
├── tests/                          # Test suite
├── AGENTS.md                       # Agent protocol
├── CLAUDE.md                       # Session directives
└── ARK_BRIEFING_PACKET.md          # Mission briefing
```

### Directory rules

| Directory | Rule |
|---|---|
| `canon/` | Only modified by the promote script via deliberate commit. Never edited manually. |
| `staging/` | Never committed to canon directly. Contents are transient working state. |
| `src.texts/` | Add-only. Never modify or delete a source file. |
| `schemas/` | Changes require a version bump and migration plan. |
| `pipeline/` | Changes require testing on staging before use on canon. |
| `memos/` | Human-readable status and decisions. Not part of the corpus. |

---

## 3. Book Code Registry — 76-Book Orthodox Canon

### Old Testament (49 books)

| Group | Codes |
|---|---|
| Pentateuch | GEN, EXO, LEV, NUM, DEU |
| Historical A | JOS, JDG, RUT, 1SA, 2SA |
| Historical B | 1KI, 2KI, 1CH, 2CH |
| Post-Exilic | 1ES, EZR, NEH |
| Deuterocanon Historical | TOB, JDT, EST, 1MA, 2MA, 3MA |
| Wisdom | PSA, PRO, ECC, SNG, JOB, WIS, SIR |
| Major Prophets | ISA, JER, BAR, LAM, LJE, EZK, DAN |
| Minor Prophets | HOS, AMO, MIC, JOL, OBA, JON, NAH, HAB, ZEP, HAG, ZEC, MAL |

### New Testament (27 books)

| Group | Codes |
|---|---|
| Gospels | MAT, MRK, LUK, JOH |
| History | ACT |
| Pauline | ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM |
| General | HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD |
| Apocalyptic | REV |

### Special codes

| Code | Note |
|---|---|
| 4MA | Appendix only, not counted in 76 |
| PMN | Prayer of Manasseh, appendix to 2CH, not counted in 76 |
| PSA | Uses LXX numbering (Ps 1–151 including Ps 151) |

---

## 4. Naming and Anchor Conventions

**Book codes:** SBL-standard, UPPERCASE, 2–4 characters. Pattern: `^[A-Z0-9]{2,4}$`

**Canonical anchor format:** `BOOK.CHAPTER:VERSE` — e.g., `GEN.1:1`, `PSA.118:1`, `MATT.5:3`. Anchors are unique, sequential, and complete per book. No anchor may be created without the 76-book registry being locked.

**File naming per staged book:**

| File | Purpose |
|---|---|
| `BOOK.md` | Scripture source of truth |
| `BOOK_articles.md` | Study articles / commentary blocks |
| `BOOK_footnotes.md` | Verse-linked footnotes |
| `BOOK_footnote_markers.json` | Scripture-side marker trace |
| `BOOK_editorial_candidates.json` | Optional: fused-word / punctuation triage |
| `BOOK_dropcap_candidates.json` | Optional: OCR drop-cap recovery |
| `BOOK_residuals.json` | Optional: ratified exceptions |

**Cross-text link syntax (frozen):** `[[GEN.1:1]]` in authored Markdown. Plain anchor tokens (`GEN.1:1`) in machine-readable fields.

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
checksum: sha256:<hash>   # covers verse text body only, not frontmatter
status: promoted          # staging | validated | promoted
---

## Chapter 1

GEN.1:1 In the beginning God made heaven and earth.
GEN.1:2 The earth was invisible and unfinished...
```

**Format rules:** UTF-8 Markdown with YAML frontmatter. One file per biblical book. One verse per line. Chapter headings as `## Chapter N`. No footnotes, cross-references, or commentary inline. Footnote markers stripped from canon and indexed separately in JSON sidecars.

---

## 6. Source Authority

| Source | Role |
|---|---|
| OSB PDF | Canonical extraction source |
| OSB Verification scan | Secondary OSB witness (manual adjudication only) |
| Brenton Septuagint | Auxiliary witness — confidence scoring and explanation only |
| Greek texts (Rahlfs / Antoniades) | Auxiliary witness — explanatory only |
| LLM inference | Proposal / ranking layer only, never authoritative |

**Immutability policy:** Canon artifacts are OSB-faithful. If both OSB witnesses omit a verse, classify as source-absence. Never insert from auxiliary witnesses without explicit human exception. Verification ladder: (1) primary OSB PDF, (2) scanned OSB, (3) classify as source-absence, (4) consult Greek/Brenton only to explain the omission.

---

## 7. Agent Roles

| Agent | Role | Scope |
|---|---|---|
| **Ark** | Architecture, core pipeline, promotion | Sole default writer/committer for canon-affecting work |
| **Ezra** | Strategic lead, audit, throughput | Analyze, validate, report, delivery ops |
| **Photius** | Parsing, staging recovery, cleanup | Bounded writes to staging and cleanup tooling |
| **Human** | Adjudication, promotion approval | Final authority on ambiguous cases and role changes |

**Core principle:** Single writer, explicit handoff, durable evidence. Work is done when state, evidence, and handoff agree.

---

## 8. Phase Roadmap

### Phase 1 — Scripture Substrate

Extract, validate, and promote all 76 books from the OSB PDF into `canon/`. Establish pipeline tooling, validation gates, and agent workflow. Separate study articles and footnotes into companion files.

### Phase 2 — Phronema Content Layer

Extract the New Testament. Design and apply a phronema annotation schema covering saints, feasts, liturgical references, and Marian typology. Expand the pericope index across all books. Build entity indexes from footnote annotations. Acquire and index Greek witness texts.

### Phase 3 — Bidirectional Hyperlinking

Insert `[[BOOK.ch:v]]` cross-references throughout footnotes and articles. Build the backlink generator. Validate full graph integrity (no orphaned nodes, no dangling references). Implement liturgical calendar cross-links. Integrate with Obsidian as a human-facing review layer.

### Phase 4 — Theological Index (Forward View)

Topical and thematic graph over the full corpus: patristic linkage, liturgical text cross-references, and a searchable theological index across Scripture, notes, and patristic sources.

---

## 9. Architectural Invariants

These are non-negotiable unless explicitly changed by Human:

- One-verse-per-line in canon
- Study article text must not appear in canon scripture files
- Footnote markers stripped from canon and indexed separately
- OSB is the sole canonical source; auxiliary witnesses are informational only
- `anchor_registry.json` is a controlled source of truth; changes require a version bump
- Changes to canonical workflow prefer tightening invariants over convenience
- Single writer (Ark), explicit handoff, durable evidence
- No content transitions between pipeline stages without passing all validation checks
- Each phase is additive; earlier phases are never modified except for validated corrections with full audit trail
- Merge conflicts on Scripture files are a red-flag event, not a routine resolution

---

## 10. Pipeline Contract (Summary)

```
src.texts/osb.pdf → [Parse] → staging/raw/ → [Validate] → staging/validated/ → [Promote] → canon/
```

**Separation of concerns (non-negotiable):** Scripture files contain ONLY YAML frontmatter and verse text with anchors. Notes and articles contain all study notes, footnotes, and introductions, with back-references to canon anchors — never inline in canon.

**Validation is a hard gate, not a best-effort lint.** A partial pass is a fail. No content transitions between stages without passing all checks for that stage.

**Promotion requires:** implementation complete, validation recorded, audit complete or waived, human ratification of ambiguous cases, promotion run from the same staged file that was validated and audited.
