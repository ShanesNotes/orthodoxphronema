# NT Extracting Tranche A Checkpoint (`EPH` promoted, `GAL` held) — 2026-03-13

**Author:** `ark`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT staged scripture + sidecar alignment + canon promotion + hold classification`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After Memo `116`, the remaining NT work shifted from the closed editorial queue to the `15` books still marked `extracting`.
- The first bounded tranche from that set was `EPH`, `PHP`, `COL`, `1PE`, and `GAL`, with the expectation that only source-local issues would be repaired in this lane.

## Objective
- Use `pdftotext`-backed spot checks to close the lightest locally-fixable books first.
- Promote any book that clears validation, footnote verification, and purity audit.
- Hold books whose remaining blocker is no longer a local scripture defect.

## Files / Artifacts
- `staging/validated/NT/EPH.md`
- `staging/validated/NT/EPH_footnote_markers.json`
- `staging/validated/NT/GAL.md`
- `staging/validated/NT/GAL_footnote_markers.json`
- `canon/NT/EPH.md`
- `reports/EPH_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- `EPH`
  - Removed the remaining fused/article and note-letter residue in local scripture lines such as `awhich`, `abeing`, `aholy`, `adwelling`, `aminister`, `adescended`, `aperfect`, `asacrifice`, `asweet`, `aglorious`, `aman`, `agreat`, `aslave`, `aagainst`, and `abeloved`.
  - Removed stray note-letter residue from lines like `who ais`, `fellowship aof`, `you aall`, `fruit of the Spirit ais`, `for we are members ... afor`, and `your own Master also ais`.
  - Realigned `EPH_footnote_markers.json` to the full `53` extracted footnote-anchor set.
  - Promoted `EPH` into `canon/NT/`.
- `GAL`
  - Removed the remaining local fused/article and note-letter residue in bounded lines such as `adifferent`, `abondservant`, `aand`, `ahad`, `acompel`, `aman`, `aminister`, `atransgressor`, `abefore`, `acurse`, `atree`, `awho`, `athat`, `amediator`, `alaw`, `atutor`, `achild`, `aslave`, `awoman`, `ason`, `agood`, `abondwoman`, `afreewoman`, `atwo`, `ayoke`, `adebtor`, `afornication`, `adrunkenness`, `aone`, `aspirit`, `athe`, and `anew`.
  - Realigned `GAL_footnote_markers.json` to the `56` extracted footnote anchors.
  - Targeted `pdftotext` checks confirmed the cleaned source shape for anchors around `GAL.1:18`, `GAL.2:14-18`, `GAL.3:13-21`, `GAL.4:1-24`, `GAL.5:1-3`, and `GAL.6:1-15`.
  - `GAL` still trips the current `V11`/purity heuristics on the legitimate phrase `Christ’s have crucified` at `GAL.5:24`. That is a detector false positive, not a confirmed scripture defect, so the book was held instead of force-promoted.
- `PHP`
  - Re-checking the live book showed its `V7` warning is registry drift, not local scripture damage: staged chapter counts are `30/30/21/23` while the registry still expects `30/23/25/17`.
  - This book was not edited in this tranche and should route as a schema/registry hold, not a local `pdftotext` cleanup book.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promote `EPH` immediately after the clean pass | It cleared validator, footnote, and purity gates in the same lane | None beyond normal dossier/dashboard drift if surfaces were not refreshed | Re-run promote and dashboard generation |
| Hold `GAL` on the detector false positive | The remaining warning is from the heuristic matching `Christ’s have`, not from source-backed residue | The stale dossier still understates current cleanup progress | Reopen only if the detector or validator is adjusted, or if a new source-backed defect appears |
| Do not touch `PHP` in this tranche | Its active blocker is registry mismatch, not local scripture residue | Throughput slows if schema work is deferred | Reclassify to a registry packet instead of forcing local edits |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/EPH.md` | `pass` | structural validation clean |
| `python3 pipeline/cleanup/verify_footnotes.py --book EPH` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/EPH.md` | `pass` | `0` candidates |
| `python3 pipeline/promote/promote.py --book EPH --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book EPH` | `pass` | canon write complete |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/GAL.md` | `warn` | `V8` plus heuristic `V11` only |
| `python3 pipeline/cleanup/verify_footnotes.py --book GAL` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/GAL.md` | `warn` | one false-positive split-word residue at `GAL.5:24` |
| `python3 - <<'PY' ... extract_pdf_text(...) ... PY` for `EPH` and `GAL` | `pass` | targeted OSB checks confirmed the repaired ambiguous anchors |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | `pass` | dashboard refreshed to `62` promoted / `14` extracting |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `EPH` and `GAL` staged books and sidecars, `canon/NT/EPH.md`, dossier, dashboard |
| `Verification run` | `done` | validator, footnote verifier, purity audit, dry-run promote, promote, targeted PDF checks |
| `Artifacts refreshed` | `partial` | `reports/EPH_promotion_dossier.json`, `reports/book_status_dashboard.json`; `GAL` dossier intentionally not refreshed because the book is held |
| `Remaining known drift` | `present` | `GAL` dashboard state still reflects stale dossier truth; `PHP` remains a registry-mismatch hold |
| `Next owner` | `ezra` | route `EPH` as promoted, mark `GAL` as a detector-false-positive hold, and send the next local cleanup lane to `HEB` |

## Requested Next Action
- Treat `EPH` as closed and promoted.
- Route `GAL` to a small follow-up decision on the `GAL.5:24` detector false positive rather than more scripture surgery.
- Treat `PHP` as a registry packet, not a local `pdftotext` packet.

## Handoff
**To:** `ezra`  
**Ask:** `Refresh the live boards so EPH routes as promoted, GAL routes as a false-positive hold, PHP routes as registry drift, and HEB becomes the next local cleanup target.`
