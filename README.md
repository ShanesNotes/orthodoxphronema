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
| `staging/` | Pre-promotion work area (not canonical) |
| `reports/` | Validation run audit trail |
| `src.texts/` | Raw source documents (immutable after intake) |
| `memos/` | Ark-to-human communications |

## Architecture

See `memos/01_architecture_memo_v1.md` for full design rationale.

## Status

Phase 1: OSB substrate ingestion — in progress.
