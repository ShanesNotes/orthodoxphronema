# NT Purity Patch And PSA Marker Triage — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `nt scripture purity / psa marker triage`
**Workstream:** `canon-hygiene`  
**Phase:** `2`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After the freeze push, the live NT scripture-side blocker had narrowed to `JOH`, `LUK`, and `REV`.
- Photius's completed companion extraction work proved the footnote layer was no longer the missing piece; the staged scripture and marker sidecars themselves were drifting.
- `PSA` remained open from Memo `104`, but the open question was whether the marker issue was a small repair or a systemic collapse.

## Objective
- Repair the specific NT scripture/marker defects that were blocking clean companion alignment in `JOH`, `LUK`, and `REV`.
- Verify whether `PSA_footnote_markers.json` was tractable in the same pass.
- Leave untouched any broader NT cleanup that was not part of the evidenced defect packet.

## Files / Artifacts
- `staging/validated/NT/JOH.md`
- `staging/validated/NT/LUK.md`
- `staging/validated/NT/LUK_footnote_markers.json`
- `staging/validated/NT/REV.md`
- `staging/validated/NT/REV_footnote_markers.json`

## Findings Or Changes
- Repaired the end of `JOH`.
  - Folded the fake `Chapter 22`–`25` tail back into `JOH.21:22-25`.
  - Restored the correct chapter count and removed the missing-scripture mismatch for `JOH.21:24-25`.
  - Cleaned the fused `21:15-19` block enough to restore verse boundaries without reopening the whole chapter.
- Repaired `LUK.17`.
  - Merged the stray `LUK.17:38` text back into `LUK.17:37`.
  - Moved the `The Tenacious Widow` heading to the correct side of the chapter break.
  - Retargeted the lone invalid footnote marker from `LUK.17:38` to `LUK.17:37`.
- Repaired `REV`.
  - Split the swallowed `REV.4:11` out of `REV.4:10`.
  - Removed the phantom `REV.22:22` and `REV.22:23` markers from `REV_footnote_markers.json`.
- Triaged `PSA` instead of forcing a fake repair.
  - `verify_footnotes.py --book PSA` shows only `3` effective marker anchors across `73` raw markers and one invalid `PSA.0:7`.
  - The sidecar is not suffering from a local off-by-one issue; it is systemically collapsed around Psalm-incorporated headings/openers.
  - That work needs a dedicated marker-index lane, not a blind hand patch.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Fix NT defects directly in staged scripture/marker files | The defects were local, source-evident, and already blocking companion alignment | Minor textual cleanup in `JOH.21` could still need later source spot-checking | Reopen the local lines from git if a later OSB check contradicts the patch |
| Leave `PSA` marker repair deferred | The sidecar collapse is systemic and not safe to guess through by hand | Psalm linkage remains broken tonight | Take a dedicated parser/index repair lane for Psalms |
| Do not regenerate dossiers/dashboard in this pass | No promotion-state change occurred; this was staged purity work only | `JOH`, `LUK`, and `REV` dossiers remain stale relative to staging | Regenerate or explicitly defer them in the next book-readiness lane |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Full suite | `pass` | `pytest -q` |
| `JOH` validation | `pass_with_warnings` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/JOH.md` |
| `LUK` validation | `pass_with_warnings` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/LUK.md` |
| `REV` validation | `pass_with_warnings` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/REV.md` |
| NT footnote verification after patch | `warn_only` | `python3 pipeline/cleanup/verify_footnotes.py --book JOH`; `--book LUK`; `--book REV` |
| PSA marker triage | `warn` | `python3 pipeline/cleanup/verify_footnotes.py --book PSA` -> `73` raw markers, `3` effective anchors, invalid `PSA.0:7` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `JOH.md`, `LUK.md`, `LUK_footnote_markers.json`, `REV.md`, `REV_footnote_markers.json` |
| `Verification run` | `done` | targeted validator runs, targeted footnote verification, full suite |
| `Artifacts refreshed` | `deferred` | no dossier/dashboard refresh; staged-book purity only |
| `Remaining known drift` | `present` | `PSA_footnote_markers.json` systemic collapse; `JOH` / `LUK` / `REV` promotion dossiers now explicitly stale; wider NT warning set still exists in books like `EPH`, `MAT`, and `HEB` |
| `Next owner` | `ark` | package the next book-level NT lane and separate the Psalm marker-index repair from ordinary cleanup |

## Requested Next Action
- Treat `JOH`, `LUK`, and `REV` as repaired local blockers, then re-rank the NT lane around the remaining live warning books.
- Open a dedicated Psalm marker-index repair task rather than continuing ad hoc line edits.

## Handoff
**To:** `ark`  
**Ask:** `Accept the NT local repairs, keep PSA as a separate marker-index problem, and do not let its systemic sidecar collapse sprawl into the generic NT cleanup lane.`
