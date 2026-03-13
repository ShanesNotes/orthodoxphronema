# Phase 3 Pre-Work — Agent Planning Prompt (Claude Code CLI, Plan Mode)

> **Generated:** 2026-03-10 by Cowork session
> **Target agent:** Ark (Claude Code CLI, `--plan` mode)
> **Prerequisite reads:** `AGENTS.md`, `CLAUDE.md`, `memos/BACKLINK-SCHEMA.md`, `memos/GEMINI_BACKLINK_SCHEMA_20260310.md`

---

## Situational Briefing (verified state as of this session)

### ADJ-4 Resolved — Canon URI Format

The canon directory is flat by testament:

```
canon/
├── OT/          # 45 promoted .md files + .gitkeep
│   ├── GEN.md
│   ├── EXO.md
│   ├── ... (45 total)
│   └── .gitkeep
├── NT/          # empty — .gitkeep only
│   └── .gitkeep
└── .gitkeep
```

**Confirmed `canon_uri` format:** `canon/{testament}/{BOOK_CODE}.md`
No subdirectories below testament. Phase 3 backlink schema should use this two-level path.

### Dashboard State (from `reports/book_status_dashboard.json`)

| Status               | Count | Notes                                          |
|----------------------|-------|-------------------------------------------------|
| `promoted`           | 45    | All in `canon/OT/`                              |
| `extracting`         | 28    | PSA (OT) + 27 NT books — all blocked by "no promotion dossier" |
| `editorially_clean`  | 2     | PRO, SIR — blocked by unratified residuals, NOT V4 |
| `structurally_passable` | 1  | JOB — V4 WARN (12 missing anchors), V7 WARN    |

**SNG and WIS are already `promoted`.** No promotion action needed.

### Unratified Residuals

| Book | Unratified | Flag     |
|------|-----------|----------|
| PRO  | 130       | CRITICAL |
| SIR  | 63        | HIGH     |
| JOB  | 43        | HIGH     |
| HOS  | 10        | THRESHOLD|
| JER  | 9         | —        |
| EZK  | 1         | —        |

### JOB V4 Warnings (12 missing anchors)

All are verse-gap warnings — likely Docling drop-cap extraction artifacts:

- ch.17: jumps 1→3, ch.18: jumps 1→3, ch.19: jumps 3→5
- ch.23: jumps 6→10, ch.23: jumps 12→16
- ch.24: jumps 1→3, ch.36: jumps 29→31, ch.39: jumps 0→2

### 28 Extracting Books

All blocked by `"no promotion dossier"`. One OT holdout (PSA — staged at `staging/validated/OT/PSA.md`, 2934 lines). Remaining 27 are the entire NT canon:

MAT, MRK, LUK, JOH, ACT, ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM, HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD, REV

**NT staging does not exist yet** — `staging/validated/NT/` is an empty directory.

### V11/V12 Gate Audit

**Implemented in code, never run against the corpus.**

| Gate | Definition | Location |
|------|-----------|----------|
| V11  | Docling column-split artifacts (split-word detection) | `pipeline/validate/checks.py:424-476` |
| V12  | Verse's own number leaked into text body | `pipeline/validate/checks.py:483-503` |

Registered in:
- `pipeline/tools/batch_validate.py:129` (in check list `["V10", "V11", "V12"]`)
- `pipeline/tools/generate_book_status_dashboard.py:40` as `EDITORIAL_VALIDATION_KEYS = ("V11", "V12")`

Related cleanup tooling:
- `pipeline/cleanup/fix_split_words.py` — uses V11 logic to apply fixes (line 5 docstring)
- `pipeline/cleanup/purity_audit.py:148` — finds live split-word residue using V11 patterns

**Every book in the dashboard shows `V11: "MISSING"` and `V12: "MISSING"`.**
No references to V11/V12 exist in `schemas/` (checked: `schemas/anchor_registry.json`, `schemas/greek_source_map.json`, `schemas/notes_frontmatter.json`, `schemas/residual_classes.json`, `schemas/scripture_frontmatter.json`).

---

## File & Directory Reference Index

These are all paths verified as existing and relevant to planning. Read any of these as needed.

### Governance

- `AGENTS.md` — agent ownership boundaries (Ark, Ezra, Photius, Human)
- `CLAUDE.md` — Ark system directives and session protocol

### Canon (promoted output)

- `canon/OT/*.md` — 45 promoted OT books
- `canon/NT/.gitkeep` — empty, awaiting NT promotion

### Staging (pipeline working area)

- `staging/validated/OT/` — validated OT books (including PSA.md, JOB.md, PRO.md, SIR.md)
- `staging/validated/NT/` — empty directory
- `staging/raw/probe/` — raw Docling probe output
- `staging/reference/brenton/` — Brenton LXX reference texts
- `staging/reference/greek/` — Greek source reference texts
- `staging/quarantine/` — quarantined problem files

### Pipeline Code

**Parsing:**
- `pipeline/parse/osb_extract.py` — primary OSB extractor
- `pipeline/parse/psa_extract.py` — PSA-specific extractor
- `pipeline/parse/article_tracker.py` — study article tracking
- `pipeline/parse/chapter_tracker.py` — chapter state machine
- `pipeline/parse/docling_probe.py` — Docling PDF probe

**Validation:**
- `pipeline/validate/checks.py` — all validation gates V1–V12
- `pipeline/validate/validate_canon.py` — per-book validation runner
- `pipeline/validate/pdf_edge_case_check.py` — V4 edge-case PDF spot-checker

**Promotion:**
- `pipeline/promote/promote.py` — promotion execution
- `pipeline/promote/gates.py` — promotion gate logic

**Cleanup (Photius domain, Ark review for batch):**
- `pipeline/cleanup/fix_split_words.py` — V11 split-word fixer
- `pipeline/cleanup/purity_audit.py` — purity sweep using V11 patterns
- `pipeline/cleanup/sir_recovery.py`, `sir_recovery_v2.py`, `sir_final_recovery.py`, `sir_residue_recovery.py` — SIR recovery pipeline
- `pipeline/cleanup/job_residue_recovery.py`, `job_final_recovery.py` — JOB recovery tools
- `pipeline/cleanup/restructure_psa.py`, `restructure_wis.py` — structural restructuring
- `pipeline/cleanup/fix_articles.py`, `fix_heading_duplication.py`, `fix_omissions.py` — editorial fixes
- `pipeline/cleanup/extract_footnotes.py`, `verify_footnotes.py`, `refine_notes.py` — footnote pipeline
- `pipeline/cleanup/recover_markers.py`, `reindex_markers.py` — marker recovery
- `pipeline/cleanup/dropcap_verify.py` — drop-cap artifact verification
- `pipeline/cleanup/apply_purity_cleanup.py`, `audit_cleanup_residue.py` — purity cleanup execution

**Batch tools:**
- `pipeline/tools/generate_book_status_dashboard.py` — dashboard generator
- `pipeline/tools/batch_validate.py` — batch validation runner (V1–V12)
- `pipeline/tools/batch_dossier.py` — batch promotion dossier generator
- `pipeline/tools/batch_reextract.py` — batch re-extraction
- `pipeline/tools/verify_all_cvc.py` — chapter-verse-count verifier
- `pipeline/tools/check_stale_dossiers.py` — stale dossier detector
- `pipeline/tools/pdf_verify.py` — PDF source verification
- `pipeline/tools/add_verse_counts.py` — verse count annotation

**Metadata:**
- `pipeline/metadata/generate_pericope_index.py` — pericope index generator

**Reference indexing:**
- `pipeline/reference/index_brenton.py` — Brenton LXX indexer
- `pipeline/reference/index_greek.py` — Greek source indexer
- `pipeline/reference/normalize_reference_text.py` — reference text normalizer

**Common/shared:**
- `pipeline/common/config.py`, `paths.py`, `patterns.py`, `registry.py`, `types.py`, `text.py`, `frontmatter.py`, `poetry.py`, `pdf_source.py`

### Schemas

- `schemas/scripture_frontmatter.json` — scripture frontmatter schema
- `schemas/notes_frontmatter.json` — notes/footnotes frontmatter schema
- `schemas/anchor_registry.json` — verse anchor registry schema
- `schemas/residual_classes.json` — residual classification schema
- `schemas/greek_source_map.json` — Greek source mapping schema

**Note: No V11/V12 schema definitions exist.**

### Reports

- `reports/book_status_dashboard.json` — master dashboard (source of truth for status)
- `reports/cvc_report.json` — chapter-verse-count report
- `reports/{BOOK}_promotion_dossier.json` — per-book promotion dossiers (50 exist, all OT)

### Memos (today's and governance-relevant)

- `research/PM-report-2026-03-10.md` — today's PM report
- `research/ark-structural-audit-2026-03-10.md` — today's structural audit
- `memos/BACKLINK-SCHEMA.md` — Phase 3 backlink schema design
- `memos/GEMINI_BACKLINK_SCHEMA_20260310.md` — Gemini's backlink schema contribution
- `memos/GROK_ENGINEERING_AUDIT_20260310.md` — Grok's engineering audit
- `research/PROJECT-KNOWLEDGE.md` — project knowledge base
- `research/PROJECT-KNOWLEDGE-STRATEGIC.md` — strategic project knowledge
- `memos/ezra_ops_board.md` — Ezra operational board

### Tests

- `tests/test_checks.py` — validation checks tests
- `tests/test_validate.py` — validate_canon tests
- `tests/test_gates.py`, `test_promote_gate.py` — promotion gate tests
- `tests/test_book_status_dashboard.py` — dashboard generation tests
- `tests/test_purity_audit.py` — purity audit tests
- `tests/test_fix_split_words.py` — V11 split-word fix tests
- `tests/test_fix_articles.py` — article fix tests
- `tests/test_dropcap_verify.py` — drop-cap verification tests
- `tests/test_batch_tools.py` — batch tool tests
- `tests/test_common.py`, `test_metadata_format.py`, `test_cvc_overrides.py`, `test_verse_split.py`, `test_poetry_extraction.py`, `test_article_tracker.py`, `test_chapter_tracker.py`, `test_index_brenton.py`, `test_verify_footnotes.py`

---

## Planning Directives

Use this briefing to enter plan mode for the following decision tree:

### Decision 1 — V11/V12 Activation

The checks exist but produce `MISSING` for every book. Before Phase 3 can define editorial gates, V11/V12 need a batch run. Plan:
1. Whether `batch_validate.py` can run V11/V12 as-is or needs a wiring fix
2. Whether to run against all 45 promoted canon books or just the 3 non-promoted (PRO, SIR, JOB)
3. How results should be recorded (dashboard regeneration? memo?)

### Decision 2 — PRO/SIR Residual Resolution Path

PRO (130 unratified) and SIR (63 unratified) are the only `editorially_clean` books. Their path to promotion requires either:
- Residual ratification (classify each as acceptable, PDF-source, or extraction artifact)
- Additional recovery runs (SIR has 4 recovery scripts; PRO has `restructure_pro.py`)
- Human waiver

Plan the most efficient resolution approach.

### Decision 3 — JOB V4 Remediation

JOB is `structurally_passable` with 12 missing anchors (V4 WARN) and 43 unratified residuals. Per `CLAUDE.md` session protocol: before widening parser allowlists on V4 books under 100 missing anchors, run `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/JOB.md`. Plan this gate.

### Decision 4 — Phase 3 Schema Foundation

With ADJ-4 resolved (`canon/{testament}/{BOOK}.md`), the backlink schema can now be drafted. Reference `memos/BACKLINK-SCHEMA.md` and `memos/GEMINI_BACKLINK_SCHEMA_20260310.md` for prior design work. Plan what schema artifacts need to land in `schemas/` and whether any `pipeline/metadata/` tooling needs creation.

### Decision 5 — NT Pipeline Bootstrap

28 books are `extracting` with "no promotion dossier." All 27 NT books have zero staging artifacts. PSA is the sole OT holdout (staged but undossiered). Plan the extraction and dossier generation sequence.

---

## Constraints

- Follow `AGENTS.md` ownership boundaries strictly
- Write/update a memo in `memos/` BEFORE implementing any substantial change
- Do not begin Phase 3 or Phase 2 tagging work — this prompt is for PLANNING ONLY
- Confirm Ezra audit is recorded or waived before any promotion execution
- Use `EnterPlanMode` — do not execute changes in this session
