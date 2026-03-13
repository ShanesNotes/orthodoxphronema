# NT Extracting Tranche B Promotions and Phase C Holds

Date: 2026-03-13
Workstream: nt-prep
Phase: 2
Supersedes: none
Superseded by: none

## Summary

Continued the remaining NT `extracting` lane with a bounded `pdftotext`-backed surgical pass. Promoted `2CO` and `HEB`, then triaged the next tranche candidates and left explicit holds for books that no longer fit a local cleanup-only lane.

## What Changed

- Repaired [`staging/validated/NT/2CO.md`](/home/ark/orthodoxphronema/staging/validated/NT/2CO.md):
  - removed fused/article residue across chapters `1` to `13`
  - corrected the source-confirmed closing-verse shape from staged `## Chapter 14` / `2CO.14:1` to `2CO.13:14`
  - fixed nearby local spacing residue including `Christ who`, `us see`, and the end-of-book benediction anchor
- Realigned [`staging/validated/NT/2CO_footnote_markers.json`](/home/ark/orthodoxphronema/staging/validated/NT/2CO_footnote_markers.json) by replacing the stray `2CO.11:21` marker anchor with `2CO.4:18`
- Promoted [`canon/NT/2CO.md`](/home/ark/orthodoxphronema/canon/NT/2CO.md) and refreshed [`reports/2CO_promotion_dossier.json`](/home/ark/orthodoxphronema/reports/2CO_promotion_dossier.json)
- Repaired [`staging/validated/NT/HEB.md`](/home/ark/orthodoxphronema/staging/validated/NT/HEB.md):
  - removed broad fused/article and note-letter residue across the staged text
  - cleaned local marker-letter leakage such as `purged our sins`, `do if God permits`, `to renew`, `in my chains`, `and tempest`, and `or shot`
  - closed the final `asecond` residues in `HEB.8:7` and `HEB.9:28`
- Rebuilt [`staging/validated/NT/HEB_footnote_markers.json`](/home/ark/orthodoxphronema/staging/validated/NT/HEB_footnote_markers.json) from the live `HEB_footnotes.md` anchor set to eliminate sidecar drift
- Promoted [`canon/NT/HEB.md`](/home/ark/orthodoxphronema/canon/NT/HEB.md) and refreshed [`reports/HEB_promotion_dossier.json`](/home/ark/orthodoxphronema/reports/HEB_promotion_dossier.json)
- Regenerated [`reports/book_status_dashboard.json`](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)

## Source Verification

- `2CO` end-of-book shape was checked against the OSB PDF text span for chapter `13`, confirming:
  - `2CO.13:12`
  - `2CO.13:13`
  - `2CO.13:14`
- No whole-book re-extraction was used. `pdftotext` remained a targeted verifier, not a replacement scripture source.

## Verification Run

- `python3 pipeline/validate/validate_canon.py staging/validated/NT/2CO.md`
- `python3 pipeline/cleanup/verify_footnotes.py --book 2CO`
- `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/2CO.md`
- `python3 pipeline/promote/promote.py --book 2CO --dry-run`
- `python3 pipeline/promote/promote.py --book 2CO`
- `python3 pipeline/validate/validate_canon.py staging/validated/NT/HEB.md`
- `python3 pipeline/cleanup/verify_footnotes.py --book HEB`
- `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/HEB.md`
- `python3 pipeline/promote/promote.py --book HEB --dry-run`
- `python3 pipeline/promote/promote.py --book HEB`
- `python3 pipeline/tools/generate_book_status_dashboard.py`

## Tranche Classification

- Promoted now:
  - `2CO`
  - `HEB`
- Held for broader work:
  - `ROM`: still has `V7` gap `431/433`, invalid `ROM.16:25` marker/footnote anchor, and wider sidecar drift
  - `1CO`: still has `V7` gap `436/446`, `131` purity candidates, and marker-sidecar drift
  - `ACT`: only `V8` structurally, but still has `269` purity candidates and major footnote-sidecar drift (`100` marker-only / `20` footnote-only)
  - `REV`: still has `V12` inline verse-number leakage at `REV.1:6`, `222` purity candidates, and broad marker-sidecar drift

## Files Changed

- [`staging/validated/NT/2CO.md`](/home/ark/orthodoxphronema/staging/validated/NT/2CO.md)
- [`staging/validated/NT/2CO_footnote_markers.json`](/home/ark/orthodoxphronema/staging/validated/NT/2CO_footnote_markers.json)
- [`canon/NT/2CO.md`](/home/ark/orthodoxphronema/canon/NT/2CO.md)
- [`reports/2CO_promotion_dossier.json`](/home/ark/orthodoxphronema/reports/2CO_promotion_dossier.json)
- [`staging/validated/NT/HEB.md`](/home/ark/orthodoxphronema/staging/validated/NT/HEB.md)
- [`staging/validated/NT/HEB_footnote_markers.json`](/home/ark/orthodoxphronema/staging/validated/NT/HEB_footnote_markers.json)
- [`canon/NT/HEB.md`](/home/ark/orthodoxphronema/canon/NT/HEB.md)
- [`reports/HEB_promotion_dossier.json`](/home/ark/orthodoxphronema/reports/HEB_promotion_dossier.json)
- [`reports/book_status_dashboard.json`](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)

## Artifacts Refreshed

- `2CO` promotion dossier
- `HEB` promotion dossier
- dashboard

## Remaining Known Drift

- `GAL` still looks locally clean but remains blocked by the current `V11` / purity false positive on `GAL.5:24`
- `PHP` remains a registry-versification hold, not a local scripture cleanup book
- `ROM`, `1CO`, `ACT`, and `REV` are still extracting and should not be routed as quick promote books without another dedicated pass

## Next Owner

- Ark: take the next bounded extracting pass from `GAL` false-positive adjudication or a smaller cleanup target such as `COL` / `1PE`
- Ezra: refresh the ops board to show `2CO` and `HEB` promoted and re-rank the remaining extracting queue around explicit hold classes
- Human: no new ratification packet is required from this tranche
