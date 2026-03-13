# NT Titus Cleanup And Promotion — 2026-03-13

**Author:** `ark`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `TIT staged scripture + sidecar alignment + canon promotion + state refresh`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After the `JUD` / `PHM` packet, `TIT` was the smallest remaining NT cleanup target.
- The book still carried local fused-word residue, footnote-anchor drift, and one `V7` overcount caused by an extra staged `TIT.3:16` line.

## Objective
- Remove the remaining local OCR and note-letter residue in `TIT`.
- Reconcile the marker sidecar to the extracted footnote anchors.
- Resolve the staged overcount only if the OSB PDF confirmed the closing verse shape.
- Promote `TIT` from the same staged file that passed validation and audit.

## Files / Artifacts
- `staging/validated/NT/TIT.md`
- `staging/validated/NT/TIT_footnote_markers.json`
- `canon/NT/TIT.md`
- `reports/TIT_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Cleaned the explicit fused/article residue in `TIT`, including:
  - `TIT.1:1` `abondservant` -> `a bondservant`
  - `TIT.1:4` `atrue` -> `a true`
  - `TIT.1:6-8` `aman`, `abishop`, `amust`, `asteward`, `alover` -> their source-backed plain forms
  - `TIT.1:12` `aprophet` -> `a prophet`
  - `TIT.2:7` `apattern` -> `a pattern`
  - `TIT.3:8` `afaithful` -> `a faithful`
  - `TIT.3:10-11` `adivisive`, `aperson` -> `a divisive`, `a person`
- Removed stray note-letter residue from:
  - `TIT.1:4` `Christ a our Savior` -> `Christ our Savior`
  - `TIT.2:7-8` trailing orphan `a` markers
- Realigned `TIT_footnote_markers.json` to the ten extracted footnote anchors:
  - `TIT.1:1`, `TIT.1:5`, `TIT.1:10`, `TIT.2:1`, `TIT.2:3`, `TIT.2:11`, `TIT.2:13`, `TIT.3:5`, `TIT.3:7`, `TIT.3:10`
- Verified the closing verse shape against the local OSB PDF span for chapter 3:
  - the source shows verse `15` followed by `Grace be with you all. Amen.`
  - staged `TIT.3:16` was therefore merged into `TIT.3:15`
- Promoted `TIT` into `canon/NT/` and refreshed the dossier plus dashboard.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Merge staged `TIT.3:16` into `TIT.3:15` | The registry expects `15` verses in chapter 3 and the OSB PDF places `Amen` under verse `15` | A bad merge would create a real verse-loss defect | Reopen chapter 3 from the OSB PDF and restore the staged split if new evidence appears |
| Align the sidecar directly to `TIT_footnotes.md` anchors | The footnote extraction was already source-derived; the sidecar was the drifting layer | A wrong anchor would hide a real scripture-side marker miss | Compare the sidecar against `TIT_footnotes.md` and rerun `verify_footnotes.py` |
| Promote immediately after the clean pass | `TIT` passed validation, footnote verification, purity audit, and dry-run preview in the same lane | None beyond ordinary promotion drift if surfaces were not refreshed | Re-run promote and dashboard generation |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/TIT.md` | `pass` | structural validation clean |
| `python3 pipeline/cleanup/verify_footnotes.py --book TIT` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/TIT.md` | `pass` | `0` candidates |
| `python3 pipeline/promote/promote.py --book TIT --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book TIT` | `pass` | canon write complete |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | `pass` | dashboard refreshed to `58` promoted |
| `python3 - <<'PY' ... extract_pdf_text(...) ... PY` | `pass` | local OSB PDF shows `TIT.3:15` ending with `Grace be with you all. Amen.` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | staged scripture, marker sidecar, canon file, dossier, dashboard |
| `Verification run` | `done` | validator, footnote verifier, purity audit, dry-run promote, promote, targeted PDF check |
| `Artifacts refreshed` | `done` | `reports/TIT_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | the remaining NT queue is `1TI`, `2PE`, and `JAS` |
| `Next owner` | `ezra` | route `TIT` as promoted and rerank the final three NT cleanup targets from current verifier output |

## Requested Next Action
- Update live routing so `TIT` is no longer treated as an editorially clean hold, then take the next smallest bounded NT cleanup lane.

## Handoff
**To:** `ezra`  
**Ask:** `Treat TIT as promoted and dispatch the next cleanup packet from 2PE, 1TI, and JAS.`
