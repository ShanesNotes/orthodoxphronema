# Memo 78 — Parallel Planning Dispatch (Ark + Ezra)

**Author:** `cowork`
**Type:** `workflow`
**Status:** `active`
**Scope:** `parallel agent dispatch`
**Date:** `2026-03-11`

## Status Verification (as of 2026-03-11)

### Dashboard Truth
- OT promoted: `45/49`
- OT holdouts: `4` (PRO, SIR, JOB, PSA) — all `editorially_clean`
- PRO: `dry-run` ready, `130` unratified residuals, governance-closeout only
- SIR: `dry-run` ready, `63` unratified residuals, visible polish complete (Memo 74)
- JOB: `blocked`, 7 live gap groups remain, one bounded recovery pass pending (Memo 75)
- PSA: `blocked`, systematic verse-2/title recovery in progress under Photius
- NT: `27/27` extracted to staging (Memo 77), `1` promotion_ready (2JN), `26` extracting/blocked
- NT range: V7 67.7% (EPH) to 100% (2JN), most between 85–100%

### Memo Chain Health
- Memo 72 is the OT closeout control doc (supersedes 71)
- Memo 73 packages PRO+SIR ratification — awaiting Human
- Memo 74 completed SIR polish and JOB editorial closure
- Memo 75 built JOB residual triage packet — one recovery pass remains
- Memo 76/77 completed full NT extraction sprint — all 27 books staged
- Ops board last updated 2026-03-10, needs refresh for NT landing

### What Changed Since Last Ops Board Update
1. All 27 NT books extracted and staged (Memo 77)
2. Parser fixes for NT chapter detection landed (RE_COMMA_INTS, bare-number, SectionHeader)
3. 2JN is the sole clean NT book (0 errors, 0 warnings)
4. EPH flagged as critical recovery target (V7 67.7%)
5. V1 failures widespread in NT (duplicate anchor pattern)
6. V9 fails universally for NT (expected — OT-tailored checks)

### Open Human Decisions (unchanged)
- RES-1: Ratify PRO/SIR residual posture (Memo 73)
- RES-2: Ratify historical packet JDG/1SA/2SA (Memo 51)
- JOB residual posture pending one more recovery pass (Memo 75)

---

## ARK Planning Prompt

```
SESSION CONTEXT — Ark (Claude Code)
Date: 2026-03-11
Read CLAUDE.md and ARK_BRIEFING_PACKET.md to confirm session protocol.
Read AGENTS.md to confirm role boundaries.

CURRENT STATE:
- 45/49 OT promoted. 4 holdouts (PRO, SIR, JOB, PSA) are Ezra/Photius lanes.
- All 27 NT books extracted to staging/validated/NT/ (Memo 77).
- Parser fixes landed for NT chapter detection in osb_extract.py.
- 2JN is fully clean. EPH is critical (V7 67.7%). TIT borderline (78.3%).
- V1 failures in most NT books (duplicate anchors from inline verse numbers).
- V9 fails universally for NT (expected, OT-tailored).
- Dashboard refreshed. Dossiers generated for all 27 NT books.

YOUR LANE (Phase 4 — NT stabilization):
Ark owns NT pipeline and structural work. Do NOT touch OT holdouts
unless a parser/schema escalation surfaces.

PRIORITY 1 — NT V1 duplicate-anchor resolution
Most NT books fail V1 due to inline verse numbers parsed as duplicates.
This is the single highest-leverage fix across the NT corpus.
- Diagnose the duplicate-anchor pattern: are these OT quotation verse
  numbers bleeding through, poetry indentation markers, or column-split
  artifacts?
- Implement a targeted parser or cleanup fix in the extraction pipeline.
- Re-validate affected books and measure V1 pass-rate improvement.
- Write a memo (suggest Memo 79) with findings, fix description, and
  before/after validation counts.

PRIORITY 2 — EPH targeted recovery
EPH is at 67.7% V7 — well below the 80% threshold.
- Diagnose the verse loss: article absorption? column-split? page boundary?
- Implement a targeted fix (parser-level if systematic, cleanup if isolated).
- Re-extract or patch EPH and re-validate.
- Include EPH findings in the same or a companion memo.

PRIORITY 3 — NT V2/chapter-count anomalies
JOH has 26 chapters detected (expected 22 + Ch0). 2CO has 15 (expected 14).
- Diagnose false chapter advances.
- Fix if the root cause is in the parser; note if it requires manual sidecar.

PRIORITY 4 — TIT recovery (if bandwidth allows)
TIT is at 78.3% — just under threshold. Quick win if the loss pattern is
similar to a fixed book.

CONSTRAINTS:
- Stay on NT. OT only interrupts for parser/schema escalation or a
  promotion checkpoint that Ezra routes to you.
- Follow completion handshake protocol: memo, verification, artifact refresh.
- Refresh dashboard after any batch of structural fixes.
- Do not promote any NT books yet — staging only.

DELIVERABLES THIS SESSION:
1. V1 duplicate-anchor diagnosis and fix (highest leverage)
2. EPH recovery to >= 80% V7
3. JOH/2CO chapter-count fix or documented workaround
4. Memo 79 (or 79+80) documenting NT stabilization results
5. Dashboard refresh after fixes land
```

---

## EZRA Planning Prompt

```
SESSION CONTEXT — Ezra (Codex)
Date: 2026-03-11
Read AGENTS.md to confirm role boundaries.
Read memos/ezra_ops_board.md for current dispatch state.

CURRENT STATE:
- 45/49 OT promoted. Holdouts: PRO, SIR, JOB, PSA.
- PRO + SIR ratification packet ready (Memo 73). SIR polish complete (Memo 74).
  Awaiting Human sign-off on RES-1.
- JOB has 7 live gap groups (Memo 75). One bounded recovery pass remains
  before converting to a human ratification ask.
- PSA under Photius systematic recovery — do not absorb.
- NT extraction complete (Memo 77): 27 books staged, Ark owns NT stabilization.
- Ops board needs refresh to reflect NT landing and current lane assignments.

YOUR LANE (OT closeout + ops + selective engineering):
Ezra owns OT closeout sequencing, ops board, and at most one
high-leverage engineering lane.

PRIORITY 1 — Ops board refresh
The ops board was last updated 2026-03-10 and does not reflect the NT
extraction landing. Update memos/ezra_ops_board.md:
- Add NT extraction completion to snapshot (27 books staged, Memo 77).
- Update Ark's lane from "NT extraction kickoff" to "NT stabilization"
  with priorities: V1 dedup, EPH recovery, chapter-count fixes.
- Confirm PRO/SIR/JOB/PSA lane statuses are still accurate.
- Confirm release train is unchanged (Packet A: PRO+SIR, Packet B: JOB,
  Packet C: PSA).

PRIORITY 2 — JOB bounded recovery pass
Memo 75 identifies 7 live gap groups: 17:2, 18:2, 19:4, 23:7-9,
23:13-15, 24:2, 36:30, 39:1.
- Use pdf_edge_case_check.py and pdf_verify.py to attempt one final
  source-backed recovery for each gap group.
- For gaps confirmed absent from the PDF text layer, mark as
  "source-absent — ratify as-is."
- For gaps with evidence, attempt targeted staged fixes.
- If the tail does not shrink materially, convert Memo 75 into the
  human ratification ask for JOB residuals.
- Write findings as Memo 80 (or update Memo 75 in place).

PRIORITY 3 — NT extraction audit pass
Memo 77 requests an Ezra audit pass on NT extraction quality.
- Spot-check 3-5 representative NT books across quality tiers:
  one high (2JN or MAT), one mid (HEB or ROM), one low (EPH or TIT).
- Verify that parser fixes (RE_COMMA_INTS, bare-number detection) did
  not introduce regressions in OT books.
- Flag any systemic patterns that Ark should address in Priority 1-3.
- Write findings as a memo or append to ops board cross-agent awareness.

PRIORITY 4 — Human decision packaging
If Human comes online, the ratification queue is:
- RES-1: PRO + SIR (Memo 73) — ready now
- JOB residuals — ready after Priority 2 lands
- RES-2: Historical packet JDG/1SA/2SA (Memo 51) — unchanged
Keep the human-facing ask count at <= 3.

CONSTRAINTS:
- Do not touch NT staged files — Ark owns NT pipeline.
- Do not absorb PSA — Photius owns that lane.
- Follow Ezra lane-selection order: unblock > package > reconcile >
  selective engineering > long-horizon visibility.
- Follow completion handshake protocol for any substantial changes.
- If OT parser/schema issues surface during JOB work, escalate to Ark
  rather than fixing directly.

DELIVERABLES THIS SESSION:
1. Refreshed ops board reflecting NT landing
2. JOB recovery pass results (materially reduced or ratification-ready)
3. NT audit spot-check findings
4. Updated dispatch for Ark, Photius, and Human
```

---

## Parallel Execution Notes

These two prompts are designed to run simultaneously with zero blocking dependencies:

| Agent | Lane | Touches | Does NOT Touch |
|-------|------|---------|----------------|
| Ark | NT stabilization (V1, EPH, chapters) | `pipeline/parse/`, `staging/validated/NT/`, `reports/`, memos 79+ | OT staged files, ops board, PRO/SIR/JOB/PSA |
| Ezra | OT closeout + ops + NT audit (read-only) | `memos/ezra_ops_board.md`, `staging/validated/OT/JOB.md`, memos 80+ | NT staged files, `pipeline/parse/`, canon/ |

The only convergence point is the dashboard (`reports/book_status_dashboard.json`), which should be refreshed by whichever agent finishes a state-changing batch last. If both need to refresh, Ark goes first (NT changes), then Ezra reconciles (OT changes).

Photius continues PSA recovery independently — no dispatch change needed.
