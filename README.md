# Orthodox Phronema Archive

A durable, local-first, versioned archive rooted in the Orthodox Study Bible (OSB) as its immutable Scripture substrate, expanding into a densely linked Orthodox textual corpus.

## Core Invariants

1. Scripture files (`canon/`) are pure — no commentary, no footnotes inline.
2. The 76-book Orthodox canon is the scope.
3. Every reference traces back to a canon anchor (`BOOK.CHAPTER:VERSE`).
4. No content enters `canon/` without passing all validation checks.

## Structure

| Directory | Purpose |
|-----------|---------|
| `canon/` | Promoted, validated Scripture files (one per book) |
| `notes/` | Study notes and footnotes, separated from Scripture |
| `articles/` | OSB introductions, essays, appendices |
| `schemas/` | JSON schemas for validation |
| `pipeline/` | Ingestion, validation, and promotion scripts |
| `metadata/` | Generated navigation/index artifacts derived from canon |
| `staging/` | Pre-promotion work area (not canonical) |
| `reports/` | Validation run audit trail |
| `src.texts/` | Raw source documents (immutable after intake) |
| `memos/` | Ark-to-human communications |

## Architecture

See `memos/01_architecture_memo_v1.md` for full design rationale.

## Canon Format

Canonical Scripture files keep a simple, stable structure:
- `## Chapter X`
- `### Narrative Heading`
- `BOOK.CH:V text` on its own line

Derived navigation aids are generated separately. Example:
- `metadata/pericope_index/BOOK.json` — narrative heading to anchor-range index

## Staged Workflow Artifacts

The staged book in `staging/validated/{OT,NT}/BOOK.md` is the working source of truth
before promotion. Long-horizon cleanup and verification depend on a few sidecars:

- `BOOK_editorial_candidates.json`
  - durable editorial queue for unresolved high-confidence cleanup issues
  - includes fused article OCR defects, truncations, and similar promotion blockers
- `BOOK_footnote_markers.json`
  - structured trace index for stripped footnote markers
  - preserves marker order, verse ownership, and local trace context for later recovery
- `BOOK_residuals.json`
  - source-ambiguity and authority exceptions requiring ratification

Canonical files stay minimal. Cleanup, audit, and later AI/navigation layers should
prefer these sidecars over inflating the canon text itself.

## Status

Phase 1: OSB substrate ingestion — in progress.
