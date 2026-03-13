# NT Final Editorial Queue Closeout (`2PE`, `1TI`, `JAS`) — 2026-03-13

**Author:** `ark`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT staged scripture + sidecar alignment + canon promotion + state refresh`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After `TIT` was promoted in Memo `115`, the only remaining NT books in the editorially clean queue were `2PE`, `1TI`, and `JAS`.
- All three books were structurally passable, but each still carried local fused-word residue and footnote-marker drift. `2PE` also retained a small study-article leak and closing-versification residue.

## Objective
- Remove the remaining local scripture residue in the final three NT queue books.
- Realign each marker sidecar to the extracted footnote anchors.
- Promote every source-clean book from the same staged text that passed validation and audit.

## Files / Artifacts
- `staging/validated/NT/2PE.md`
- `staging/validated/NT/2PE_footnote_markers.json`
- `staging/validated/NT/1TI.md`
- `staging/validated/NT/1TI_footnote_markers.json`
- `staging/validated/NT/JAS.md`
- `staging/validated/NT/JAS_footnote_markers.json`
- `canon/NT/2PE.md`
- `canon/NT/1TI.md`
- `canon/NT/JAS.md`
- `reports/2PE_promotion_dossier.json`
- `reports/1TI_promotion_dossier.json`
- `reports/JAS_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- `2PE`
  - Removed the leaked article-title string from `2PE.1:13`.
  - Restored the collapsed verse boundary so `2PE.1:20` and `2PE.1:21` are separate again.
  - Merged staged `2PE.3:19` into `2PE.3:18` after checking the OSB PDF, which ends the chapter with verse `18` followed by `Amen`.
  - Cleaned the remaining local fused/article residue such as `areminder`, `avoice`, `awhich`, `alight`, `adark`, `aspoke`, `apreacher`, `areviling`, `aheart`, `adumb`, `afrom`, `a person`, `a thief`, and `a great`.
  - Realigned `2PE_footnote_markers.json` to the `22` extracted footnote anchors.
- `1TI`
  - Cleaned the remaining local fused/article and note-letter residue across the book, including `atrue`, `apure`, `agood`, `ablasphemer`, `apersecutor`, `apreacher`, `ateacher`, `awoman`, `aman`, `abishop`, `ahot`, `alittle`, `aacceptable`, `ameans`, `asnare`, and `aroot`.
  - Removed local note-letter residue such as `Christ aand not lying-ateacher`, `God a was manifested`, `ain faith`, `aof men`, and `awe can`.
  - Realigned `1TI_footnote_markers.json` to the `30` extracted footnote anchors.
- `JAS`
  - Cleaned the final fused/article and note-letter residue across the book, including `awave`, `adouble`, `aflower`, `aburning`, `akind`, `ahearer`, `adoer`, `aman`, `amirror`, `aforgetful`, `apoor`, `agood`, `atransgressor`, `abrother`, `astricter`, `aforest`, `aworld`, `avapor`, `awitness`, `arighteous`, `anature`, `asinner`, `asoul`, and `amultitude`.
  - Removed stray note-letter residue such as `amy beloved`, `aworks` / `bworks`, `Who bare you`, `ain aday`, and trailing marker letters on `JAS.2:20`, `JAS.3:12`, `JAS.4:6`, `JAS.5:9`, and `JAS.5:12`.
  - Realigned `JAS_footnote_markers.json` to the `29` extracted footnote anchors.
- Promoted all three books into `canon/NT/`.
- Refreshed the three dossiers and the dashboard. The dashboard now shows `61` promoted books and no remaining `editorially_clean` entries.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Close the final three NT queue books as one packet | They were the only remaining books in the editorial queue and all were bounded local cleanup jobs | A missed ambiguous residue could force a re-open of one book | Reopen the affected staged lines, re-run verification, and re-promote only that book |
| Use the footnote files as the anchor authority for marker-sidecar repair | The `*_footnotes.md` layers were already source-derived, while the sidecars were the drifting layer | A wrong anchor list could hide a real scripture-side mismatch | Compare sidecar anchors directly against `*_footnotes.md` and rerun `verify_footnotes.py` |
| Resolve `2PE.3:19` by PDF-backed merge instead of registry drift expansion | The local OSB text span shows the chapter ending at verse `18` with the doxology and `Amen` | A bad merge would create a real verse-loss defect | Reopen chapter 3 against the PDF and restore the prior split if new source evidence appears |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2PE.md` | `warn` | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1TI.md` | `warn` | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/JAS.md` | `pass` | structural validation clean |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2PE` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1TI` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book JAS` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/2PE.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/1TI.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/JAS.md` | `pass` | `0` candidates |
| `python3 pipeline/promote/promote.py --book 2PE --dry-run` | `pass` | canon preview clean; `V8` only |
| `python3 pipeline/promote/promote.py --book 1TI --dry-run` | `pass` | canon preview clean; `V8` only |
| `python3 pipeline/promote/promote.py --book JAS --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book 2PE` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book 1TI` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book JAS` | `pass` | canon write complete |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | `pass` | dashboard refreshed to `61` promoted |
| `python3 - <<'PY' ... extract_pdf_text(...) ... PY` for `2PE` | `pass` | local OSB PDF confirmed `2PE.1:13`, `2PE.1:20-21`, and `2PE.3:18` closing shape |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | three staged books, three marker sidecars, three canon files, three dossiers, dashboard |
| `Verification run` | `done` | validators, footnote verifier, purity audit, dry-run promote, promote, targeted PDF checks for `2PE` |
| `Artifacts refreshed` | `done` | `reports/2PE_promotion_dossier.json`, `reports/1TI_promotion_dossier.json`, `reports/JAS_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `2PE` and `1TI` retain allowed `V8` heading-density warnings; the NT editorial queue itself is now closed |
| `Next owner` | `ezra` | route NT editorial queue closeout and hand the next NT work back to extraction / longer-horizon lanes rather than promotion rescue |

## Requested Next Action
- Update the live boards so the NT editorial queue routes as complete and no longer advertises any remaining `editorially_clean` books.

## Handoff
**To:** `ezra`  
**Ask:** `Close the NT editorial queue on the live boards and reroute NT work to the remaining extraction or structural lanes, not more promotion cleanup.`
