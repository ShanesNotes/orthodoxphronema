# Memo 34 — Editorial Spell Audit And Footnote Trace Hardening

**Author:** `ezra`  
**Type:** `audit / workflow`  
**Status:** `active`  
**Date:** `2026-03-09`  
**Scope:** `cleanup contract / footnote trace contract / long-horizon workflow`

## Context
- Human manually cleaned visible fused article OCR defects in `GEN` and `EXO` and asked that these obvious spellcheck-style misses become explicit workflow targets.
- Human also asked that footnote markers remain traceable enough during parsing that later footnote extraction does not require rediscovering marker locations from scratch.
- Ezra implemented the workflow/tooling side of that request without changing canon format.

## What Changed

### 1. Fused article spell audit is now explicit
- [`pipeline/cleanup/fix_articles.py`](/home/ark/orthodoxphronema/pipeline/cleanup/fix_articles.py) now has a second confidence layer using `aspell`.
- The tool can now emit or merge `BOOK_editorial_candidates.json`-style output:
  - `--editorial-report`
  - `--editorial-out`
- High-confidence unresolved cases are the ones surfaced to the editorial queue.
- The intended target class is the exact OCR family Human flagged:
  - `adecree`
  - `aephod`
  - `acovenant`

### 2. Footnote marker sidecars are now trace artifacts
- [`pipeline/parse/osb_extract.py`](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py) no longer treats footnote markers as a bare `anchor -> marker` list.
- `BOOK_footnote_markers.json` is now emitted as a structured object with:
  - `book_code`
  - `parse_date`
  - `source_text_pages`
  - `marker_count`
  - `markers: []`
- Each marker record now preserves:
  - `anchor`
  - `marker`
  - `marker_seq_book`
  - `marker_seq_type`
  - `marker_index_in_verse`
  - `ownership`
  - `element_index`
  - `page`
  - `raw_excerpt`
  - `normalized_excerpt`

### 3. Workflow contract updated
- [`AGENTS.md`](/home/ark/orthodoxphronema/AGENTS.md) now explicitly states:
  - fused article OCR defects are part of editorial cleanup
  - footnote marker sidecars must retain local trace metadata
- [`README.md`](/home/ark/orthodoxphronema/README.md) now documents:
  - `BOOK_editorial_candidates.json`
  - `BOOK_footnote_markers.json`
  - `BOOK_residuals.json`

## Audit Findings

### Blocking drift that is now corrected
1. The repo had no explicit workflow statement that spellcheck-obvious fused articles were a standard cleanup class.
2. Footnote sidecars were still documented and emitted as a minimal marker list, which would have forced later footnote extraction to re-locate source positions manually.
3. The long-horizon process had durable sidecars for residuals and editorial review, but not enough marker provenance to support the future notes/footnote layer cleanly.

### Historical docs left intentionally untouched
- Older memos such as [`memos/06_docling_probe_genesis.md`](/home/ark/orthodoxphronema/memos/06_docling_probe_genesis.md) and [`memos/07_genesis_first_draft.md`](/home/ark/orthodoxphronema/memos/07_genesis_first_draft.md) still describe the earlier marker format.
- Those are historical records, not active contracts. The active contract is now in:
  - [`AGENTS.md`](/home/ark/orthodoxphronema/AGENTS.md)
  - [`README.md`](/home/ark/orthodoxphronema/README.md)
  - [`pipeline/parse/osb_extract.py`](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py)

## Immediate Practical Result
- Non-mutating editorial audits on current `GEN` and `EXO` now return `0` high-confidence fused-article candidates.
- That is the expected post-cleanup state and a useful regression signal for future books.

## Long-Horizon Recommendations For Ark

1. Make `fix_articles.py --editorial-out` part of the standard cleanup sequence after deterministic cleanup and before promotion discussion.
2. Regenerate `BOOK_footnote_markers.json` on the next parse/write cycle for books that are actively being touched; do not spend time backfilling historical books unless a notes/footnote task needs them.
3. Keep `BOOK_footnote_markers.json` as the authoritative parse-phase ownership/sequence artifact for future footnote text extraction.
4. If later footnote extraction needs more precision, add bounding-box coordinates only after this trace contract proves insufficient. Do not jump to full OCR or page-region indexing now.
5. Treat `BOOK_editorial_candidates.json` as the canonical editorial queue and continue keeping canon files minimal.

## Handoff
**To:** `ark`  
**Ask:** Use the new spell-audit and footnote-trace contract as the default for future books, refresh sidecars opportunistically on the next parse cycle, and keep older memos as historical evidence rather than rewriting them to match the new contract.
