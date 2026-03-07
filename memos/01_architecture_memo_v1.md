# Architecture Memo v1 — Orthodox Phronema Archive
**Author:** Ark | **Date:** 2026-03-06 | **Status:** Proposed

---

## Core Thesis

The Orthodox Phronema Archive is a text graph rooted in an immutable Scripture substrate. Every architectural decision must protect that substrate's purity while enabling dense, traceable linkage outward into patristics, liturgics, and theology. The failure mode we are engineering against is *contamination*: commentary bleeding into Scripture, references that break silently, and provenance that cannot be reconstructed.

---

## Substrate Decision

**Decision:** GitHub repo (`orthodoxphronema`) is the single canonical source of truth. Obsidian vault 'eve' is a human-facing workspace and review layer only — it may lag behind canon and must never be treated as authoritative.

**Rationale:**
- Git provides immutable, auditable commit history — exactly the provenance model we need.
- PR-style review gates enforce the promotion workflow without custom tooling.
- Plain-text files (Markdown + YAML frontmatter) are diff-able, human-readable, and tool-agnostic.
- Obsidian can *read from* the repo (symlink or sync) but never *writes back* to canon.

**Risks:**
- Git is not designed for large binary files. The OSB PDF must stay in `src.texts/` and be excluded from future LFS consideration only if the repo grows unwieldy.
- Merge conflicts on Scripture files must be treated as a red-flag event, not a routine resolution.

**Rollback:** If GitHub becomes unavailable, the local clone is complete and self-sufficient. A second bare clone on the local machine provides redundancy at zero cost.

**Owner:** Ark (architecture) + Human (GitHub account and remote management)

---

## File Format

**Decision:** UTF-8 Markdown with YAML frontmatter. One file per biblical book for Scripture; mirrored structure for notes and articles.

**Rationale:**
- Human-readable without tooling.
- Git diffs are meaningful at the line level.
- YAML frontmatter carries machine-readable metadata (book code, canon position, source, checksum) without polluting the text body.
- Obsidian renders it natively.

**Risks:** Markdown has no enforced schema — the YAML frontmatter must be validated by the pipeline, not trusted.

**Rollback:** Format is trivially convertible. If we later adopt a structured format (TEI-XML, USFM), a migration script operating on validated Markdown is straightforward.

**Owner:** Ark

---

## Anchor Scheme

**Decision:** Every verse receives a canonical anchor in the form `BOOK.CHAPTER:VERSE` using standard SBL-style book codes (e.g., `GEN.1:1`, `PS.118:1`, `MATT.5:3`). Anchors are embedded as Markdown heading IDs or explicit `<a id="...">` tags to support deep linking.

**Rationale:**
- Single, unambiguous reference key for all downstream linking.
- Human-legible and collision-free across the 76-book Orthodox canon.
- Maps cleanly to existing biblical reference conventions.

**Risks:** The OSB uses Septuagint numbering for Psalms and deuterocanonical books — we must establish a definitive numbering table before any anchor is written. No anchor may be created without that table being locked.

**Rollback:** Anchor scheme is additive metadata; changing codes requires a bulk sed-style migration. This is painful but survivable if caught early. Do not allow any downstream file to reference an anchor until the scheme is ratified.

**Owner:** Ark (scheme design) + Human (ratification)

---

## Ingestion Pipeline

**Decision:** Three-stage pipeline: **Parse → Stage → Promote**.

```
src.texts/osb.pdf
      |
   [Docling]
      |
staging/raw/          ← structured JSON + extracted text, unvalidated
      |
   [Validate]
      |
staging/validated/    ← passes all checks, awaiting promotion
      |
   [Promote]  ← manual or gated step
      |
canon/                ← immutable until next deliberate change
```

**Rationale:**
- Staging buffers prevent untested output from touching canon.
- Each stage transition is a git commit, giving us a full audit trail.
- Docling is the mandated parser (CLAUDE.md directive) and handles complex PDF layouts better than naive text extraction.

**Risks:** The OSB PDF is a scan or typeset document — Docling's accuracy is unknown until we run it. We must inspect parse output before any promotion.

**Rollback:** Staging directories are ephemeral. Canon is only modified by deliberate promotion commits. Rolling back a bad promotion is a `git revert` on the promotion commit.

**Owner:** Ark (pipeline scripts) + Human (promotion approval)

---

## Separation of Concerns (Non-Negotiable)

Scripture files (`canon/`) contain ONLY:
- YAML frontmatter (metadata)
- Verse text with anchors
- No footnotes, no cross-reference prose, no commentary

Notes/articles (`notes/`, `articles/`) contain:
- All study notes, footnotes, introductions
- Back-references to canon anchors (never inline in canon)

This separation is enforced by the validation layer, not by convention.

---

## Scale Architecture (Forward View)

Phase 1: OSB substrate (this memo)
Phase 2: Patristic linkage — each patristic quote gets a record pointing to its canon anchor(s)
Phase 3: Liturgical texts (Septuagint, liturgical books) cross-linked to canon
Phase 4: Theological index — topical and thematic graph over the full corpus

Each phase is additive. Earlier phases are never modified except for validated corrections with full audit trail.
