# Repo Maximization Triage — 2026-03-08

**Author:** `ezra`
**Type:** `workflow`
**Status:** `in_review`
**Scope:** `future architecture / foundation-safe pull-forward ideas`

## Context
- Human shared brainstorming captured in `reviews/repo-maximization-review.md`.
- The ideas are directionally aligned with the long-term Orthodox Phronema vision, but they span multiple horizons:
  - immediate foundation-safe improvements
  - next-phase architecture
  - distant aspiration / research items
- The current project is still in Phase 1 substrate formation, with zero books promoted.

## Objective
- Preserve the strong ideas from the brainstorming review.
- Separate ideas worth acting on now from ideas that should remain deferred.
- Prevent exciting future architecture from destabilizing the current canon foundation work.

## Files / Artifacts
- `reviews/repo-maximization-review.md`
- `memos/16_foundation_audit_and_promotion_threshold_brief.md`
- `AGENTS.md`
- `README.md`

## Findings Or Changes
- High-value future vision: yes, the review correctly identifies the long-term shape.
  - A local-first, anchor-grounded Orthodox archive is consistent with the project’s architecture.
  - Bidirectional linkage from canon anchors outward is the right conceptual model.
  - Public site, semantic graph, API, and retrieval/chat layers are plausible downstream products of a clean canon substrate.
- The review over-pulls a few ideas too early if taken literally.
  - LoRA training, app development, graph databases, and public products are not current blockers and should not compete with first-promotion readiness.
  - Adding many empty top-level directories now would create the appearance of structure without stable content contracts.
- The most useful thing to pull forward now is not a new product layer. It is a small set of future-safe standards.

## Recommended Pull-Forward Changes (beneficial now)
- Define one cross-text anchor-link convention before Phase 2.
  - Example question to settle: `[[GEN.1:1]]` vs plain `GEN.1:1` reference tokens vs Markdown links.
  - This should be decided once, documented, and reused across patristics, liturgy, notes, and future APIs.
- Define a metadata frontmatter schema for future non-canon texts.
  - Suggested fields: `title`, `author`, `date`, `source`, `anchors_used`, `status`, `provenance`
  - This is cheap to standardize now and expensive to retrofit later.
- Define a backlink/index artifact shape before adding lots of linked texts.
  - Example output: `metadata/anchor_backlinks/GEN.1.1.json`
  - This keeps Obsidian, static site, API, and RAG options open without committing to one product.
- Keep future directory names documented, but do not create them all yet.
  - Reserve names such as `patristics/`, `liturgy/`, `canons/`, `metadata/`, `api/`, `graph/`
  - Materialize each only when the first real content contract exists.
- Treat “first hyperlinked prototype” as the real Phase 2 target.
  - That prototype could be intentionally small:
    - one promoted Scripture book
    - one linked patristic text
    - one backlink view
    - one export path

## Explicit Defers (good ideas, wrong time)
- LoRA / fine-tuning
- AI chat productization
- Neo4j / semantic graph build-out
- mobile app work
- public static site launch
- multilingual layer
- community contribution workflow

These are not rejected. They should wait until:
- first promotion policy is stable
- at least one clean linked-text contract exists
- anchor/link syntax is frozen
- promotion evidence and regression discipline are in place

## Foundation-Safe Architecture Direction
- Phase 1 remains: establish a trustworthy canon substrate.
- Phase 1.5 should be:
  - promotion-threshold policy
  - registry provenance discipline
  - report/dossier generation
  - link syntax + metadata contract for downstream texts
- Phase 2 can then be:
  - add one linked corpus
  - generate backlinks
  - expose local-first navigation

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Preserve the future archive vision | It aligns with the repo’s original direction | Can distract from substrate work | Keep it documented as deferred architecture |
| Pull forward standards, not products | Standards compound later without destabilizing now | Feels slower than shipping a visible app | Use a small linked-text prototype after first promotion |
| Reserve folders conceptually before creating them physically | Reduces empty-structure clutter | May feel less “built out” | Create folders when first content lands |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Vision alignment | pass | review correctly centers immutable Scripture substrate and verse-level anchoring |
| Immediate usefulness | mixed | strong standards ideas; product-layer suggestions are mostly premature |
| Foundation fit | pass with defer | metadata, linking, and backlink-shape work fit current phase if kept lightweight |

## Open Questions
- Does Human want the future anchor-link syntax to look like wiki-links, plain canonical tokens, or both?
- Does Ark want a dedicated `Phase 2 architecture` memo after the first promotion threshold is settled?
- Should future-text metadata live in a shared schema before the first non-canon corpus is added?

## Requested Next Action
- Ark: do not build Phase 2 products yet.
- Ark: when entering plan mode, include one small standards track for
  - link syntax
  - non-canon frontmatter schema
  - backlink/index artifact contract
- Human: keep the larger vision visible, but do not let it redefine the first-promotion gate.

## Handoff
**To:** `ark`
**Ask:** preserve the Phase 2 vision, but only pull forward the standards that reduce future rework without creating new moving parts today.
