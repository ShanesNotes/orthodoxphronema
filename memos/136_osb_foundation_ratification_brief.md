# OSB Foundation Ratification Brief — 2026-03-16

**Author:** `ark`
**Type:** `decision`
**Status:** `ratified`
**Scope:** Consolidated ratification of three pending memos to unblock Phase 3
**Workstream:** `canon-hygiene`
**Phase:** `2→3 transition`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

Three memos have been awaiting Human ratification, collectively blocking the
Phase 2→3 transition. Ark performed a technical verification pass on 2026-03-16
and found that **two of the three are already resolved at the data level** —
their sidecar artifacts already reflect `ratified_by: human`. Only the memo
status headers need updating to close those out. The third (Memo 88) is the
constitutional document for Phase 3 and requires a genuine ratification decision.

This brief consolidates all three into one decision surface.

---

## Summary of Findings

### 1. Memo 51 — Historical Residual Ratification (JDG, 1SA, 2SA)

**Current memo status:** `in_review`
**Actual data state:** Already ratified.

| Book | Sidecar `ratified_by` | Per-entry `ratified` | Residual count | Class |
|---|---|---|---|---|
| JDG | `human` | all `true` | 1 | `osb_source_absent` (JDG.11:40) |
| 1SA | `human` | all `true` | 19 | `osb_source_absent` (1SA.17:34-52 block) |
| 2SA | `human` | all `true` | 1 | `osb_source_absent` (2SA.23:40) |

**Verdict:** The sidecars are already ratified. The memo header just needs a
status flip from `in_review` → `ratified`. No new Human decision needed.

**Proposed action:** Ark updates Memo 51 status to `ratified` and refreshes
INDEX.md.

---

### 2. Memo 91 — OT Canon Lock (17 V7-only books + EST)

**Current memo status:** `in_review`

**Ask 2 (EST):** Already resolved at the data level.
- `EST_residuals.json` shows `ratified_by: human`, `ratified_date: 2026-03-15`
- `EST.4:6` classified `osb_source_absent`, `blocking: false`, `ratified: true`
- No further decision needed for EST.

**Ask 1 (17 V7-only books):** Needs ratification.

The OT structural audit (0 errors, 18 warnings) confirms all 18 warning books
are V7-only warnings (except EST which adds V4/V10). The 17 V7-only books show
clean chapter-boundary versification drift — not extraction defects. Evidence:

- 31/49 OT books are fully clean (0 errors, 0 warnings)
- 17 books show only V7 completeness warnings (verse count ±1–14 vs registry)
- Every case is explained by LXX/OSB chapter-boundary redistribution patterns
- No V1, V2, V3, V4, V8, or V9 failures in the V7-only set
- Residual sidecars for books with missing verses already classify them as
  `osb_source_absent`

**The 17 books:** GEN, EXO, NUM, DEU, JDG, 2KI, 1CH, 2CH, EZR, JOB, EZK,
TOB, JDT, SIR, BAR, 1MA, 3MA.

**What ratification means:** These V7 drift values are accepted as genuine
OSB/LXX versification differences, not pipeline defects. The anchor targets
are frozen and stable for Phase 3 wikilinks.

**Proposed action:** Human ratifies the 17-book V7 bundle. Ark then updates
Memo 91 status to `ratified` and refreshes INDEX.md.

---

### 3. Memo 88 — Phase 3 Ratified Specification

**Current memo status:** `draft`

This is the constitutional document for Phase 3. It consolidates the
three-layer architecture, five frozen adjudications, and implementation
sequencing into a single governing reference. Everything downstream depends
on this.

**What ratification locks:**

- **Three-layer architecture:** Canon flat-file (immutable) → domain-sharded
  backlinks (JSON) → DuckDB query layer
- **Five adjudications:**
  - ADJ-1: Backlink filename separator = hyphen (`PSA.44-10.json`)
  - ADJ-2: Wikilink syntax scope = everywhere outside canon
  - ADJ-3: Domain-sharded rollout = pre-sharded from day one
  - ADJ-4: Canon directory structure = `canon/OT/`, `canon/NT/`
  - ADJ-5: V11/V12 = informational only, not promotion gates
- **Implementation sequence:** R1 extractor (memo 86) → DuckDB schema
  (memo 87) → integration pilot on PSA

**What ratification unblocks:** The entire Phase 3 engineering lane. Without
this, no wikilinks work, no backlink extraction, no graph layer.

**Proposed action:** Human ratifies Memo 88 as the governing Phase 3 document.
Ark updates status from `draft` → `ratified` and archives the two superseded
skeleton files in `research/`.

---

## Decision Surface

| # | Memo | Human action needed | Effort |
|---|---|---|---|
| 1 | **Memo 51** (JDG/1SA/2SA residuals) | None — already ratified at data level. Approve status flip. | ~30 seconds |
| 2 | **Memo 91 Ask 2** (EST disposition) | None — already ratified at data level. | ~30 seconds |
| 3 | **Memo 91 Ask 1** (17 V7-only books) | **Ratify** the V7 drift set as genuine versification differences | ~2 minutes |
| 4 | **Memo 88** (Phase 3 spec) | **Ratify** as governing Phase 3 document | ~5 minutes |

**Total decision time:** Under 10 minutes for all four items.

---

## Post-Ratification Execution Plan

Once Human approves:

1. **Memo 51:** Ark flips status → `ratified`, updates INDEX.md
2. **Memo 91:** Ark flips status → `ratified`, updates INDEX.md, formally
   locks OT canon anchors
3. **Memo 88:** Ark flips status → `ratified`, updates INDEX.md, archives
   superseded skeleton files
4. **Phase 3 pilot:** Ark executes PSA backlink extraction pilot (highest
   annotation density book)
5. **3MA Packet B:** Ezra prepares the deferred 3MA sidecar ratification

---

## Validation / Evidence

| Check | Result | Evidence |
|---|---|---|
| OT structural audit — 0 errors | `pass` | `reports/canon_ot_structural_audit.json` |
| JDG/1SA/2SA sidecars already ratified | `pass` | `staging/validated/OT/{JDG,1SA,2SA}_residuals.json` |
| EST sidecar already ratified | `pass` | `staging/validated/OT/EST_residuals.json` |
| Coordination state aligned | `pass` | `reports/coordination_state.json` |
| 76/76 promotion dossiers fresh | `pass` | Dashboard — 0 stale |

## Completion Handshake

| Item | Status | Evidence |
|---|---|---|
| Files changed | `done` | This memo created |
| Verification run | `done` | OT audit, sidecar inspection, coordination check |
| Artifacts refreshed | `partial` | INDEX.md refresh pending post-ratification |
| Remaining known drift | `present` | Three memo headers still show pre-ratification status |
| Next owner | `human` | Approve the four items in the Decision Surface above |

## Handoff

**To:** `human`
**Ask:** Review the Decision Surface and approve. Ark will execute all
post-ratification updates in one batch.
