# Staging Validated — Pre-Promotion Scripture

Single staged scripture artifact per book. Source of truth for all pre-promotion work.
Note: 76 books are now promoted to canon. Staging validated retains companion files and edge-case sidecars.

## Evidence Requirement
Every modification MUST be evidence-packaged:
- OSB PDF page reference
- Affected verse anchors
- Validator before/after
- Rationale

## After Any Edit
1. Run validators: `python3 pipeline/validate/run_validators.py {OT,NT}/BOOK.md`
2. Create or update a memo in `memos/`
3. Consider whether dossier/dashboard need refresh

## Current File Types Here
- `BOOK.md` — staged scripture (source of truth pre-promotion)
- `BOOK_articles.md` — study articles (also in `study/articles/`)
- `BOOK_footnotes.md` — verse-linked footnotes (also in `study/footnotes/`)
- `BOOK_footnote_markers.json` — marker trace sidecar
- `BOOK_dropcap_candidates.json` — drop-cap edge cases
- `BOOK_editorial_candidates.json` — editorial fix candidates
- `BOOK_residuals.json` — remaining issues tracker
