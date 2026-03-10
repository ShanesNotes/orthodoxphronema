# Memo 51 — Historical Residual Ratification Packet A

**Author:** `ezra`
**Type:** `decision`
**Status:** `in_review`
**Scope:** `human ratification / residual governance / capped decision packet`

## Context
- Ezra's operating rule is to cap Human-facing ratification asks at 3 open items.
- The current governance-blocked historical books are `JDG`, `1SA`, and `2SA`.
- Their staged text is no longer the primary issue; the active blocker is top-level sidecar ratification.

## Objective
- Convert the current historical residual blockers into one bounded Human packet.
- Keep the ask binary and evidence-backed.
- Separate staged text quality from residual-governance state.

## Files / Artifacts
- `memos/51_historical_residual_ratification_packet_a.md`
- `staging/validated/OT/JDG_residuals.json`
- `staging/validated/OT/1SA_residuals.json`
- `staging/validated/OT/2SA_residuals.json`

## Findings Or Changes
- **Packet item 1 — JDG**
  - Book: `JDG`
  - Live blocker: sidecar top-level `ratified_by` is `null`
  - Residuals: `1`
  - Residual class: `osb_source_absent`
  - Ask: accept `JDG.11:40` as a non-blocking OSB/LXX source absence and ratify the sidecar
- **Packet item 2 — 1SA**
  - Book: `1SA`
  - Live blocker: sidecar top-level `ratified_by` is `null`
  - Residuals: `19`
  - Residual class: `osb_source_absent`
  - Ask: accept the contiguous `1SA.17:34-52` block as OSB/LXX-shorter-text source absence and ratify the sidecar as one grouped decision
- **Packet item 3 — 2SA**
  - Book: `2SA`
  - Live blocker: sidecar top-level `ratified_by` is `null`
  - Residuals: `1` live residual + `1` resolved entry
  - Residual class: live residual `osb_source_absent`
  - Ask: accept `2SA.23:40` as a non-blocking OSB/LXX source absence and ratify the sidecar
- `3MA` remains blocked for the same top-level governance reason, but is intentionally held for Packet B so the current Human ask stays capped at 3 items.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Package `JDG`, `1SA`, and `2SA` together | They are the active historical-governance blockers and fit the current historical release lane | `1SA` is a larger ask than the other two | Split `1SA` into a separate packet if Human prefers smaller asks |
| Treat `1SA.17:34-52` as one grouped decision | All 19 entries represent one contiguous source-absence claim, not 19 unrelated issues | A grouped decision can obscure a single mistaken anchor if evidence is weak | Re-open the sidecar and review the block anchor-by-anchor |
| Hold `3MA` for Packet B | Preserves the 3-item cap and keeps the first packet focused on the historical lane | `3MA` waits longer for ratification | Promote it into Packet A later if another item is deferred |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `JDG` sidecar is blocked only on top-level ratification | `pass` | `staging/validated/OT/JDG_residuals.json` |
| `1SA` sidecar is blocked only on top-level ratification | `pass` | `staging/validated/OT/1SA_residuals.json` |
| `2SA` sidecar is blocked only on top-level ratification | `pass` | `staging/validated/OT/2SA_residuals.json` |
| Per-entry residuals are already marked `ratified: true` | `pass` | `staging/validated/OT/JDG_residuals.json`, `staging/validated/OT/1SA_residuals.json`, `staging/validated/OT/2SA_residuals.json` |
| Packet size respects the 3-item cap | `pass` | This memo contains exactly 3 Human decisions |

## Open Questions
- Does Human want `1SA` treated as one grouped decision, or broken out into a dedicated packet because of its size?

## Requested Next Action
- Human: decide yes/no on sidecar-level ratification for `JDG`, `1SA`, and `2SA`.
- Ezra: if ratified, convert the affected books from governance-blocked to audit/promotion sequencing.
- Ark: hold promotion execution until Ezra confirms the ratified state is reflected in the refreshed artifacts.

## Handoff
**To:** `human`  
**Ask:** `Review Packet A and decide whether JDG, 1SA, and 2SA should receive top-level sidecar ratification as non-blocking OSB/LXX source-absence cases.`

## Notes
- This packet is intentionally about governance, not about rewriting the staged text.
- `3MA` is deferred to a later packet only to preserve the Human ask cap.
