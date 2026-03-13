# ECC Chapter Restructure — Memo 48

**Date:** 2026-03-10
**Author:** Ark
**Status:** COMPLETE

## Problem

ECC.md had a severe chapter-collapse: only 4 chapters detected out of 12 expected. The extractor's 80%/60% chapter-advance threshold failed on ECC's short chapters (10-29 verses each), causing chapters 4-12 to be collapsed into chapter 3 with recycled verse numbers. V7 was 36.0% (80/222).

## Approach

1. Parsed verse lines from the original ECC.md (with chapter 0/1/2/3 structure)
2. Filtered 5 noise/study-article lines (Author, Date, Background, Major Theme, Outline content)
3. Used Jaccard word-overlap (threshold 0.25) against `staging/reference/brenton/ECC.json` to reassign each verse to its correct chapter:verse anchor
4. Resolved duplicates by keeping highest Jaccard score
5. Rebuilt chapter headers (## Chapter N) in correct order
6. Applied targeted split-word and OCR fusion fixes
7. Globally deduplicated narrative headings (the extractor had cycled through the same heading pool ~10x per heading due to chapter collapse)
8. Updated body checksum in frontmatter

## Outcome

**Final validation: PASSED WITH WARNINGS (no errors)**

```
V1  PASS  No duplicate anchors (208 unique)
V2  PASS  Chapter count: 12
V3  PASS  Chapter sequence 1–12 is sequential
V4  INFO  Residual missing-anchor count is 13
V8  PASS  No fragment headings detected
V9  PASS  No embedded verses detected
V10 WARN  3 potential absorbed verse(s) detected
V11 PASS  No split-word suspects detected
V12 PASS  No inline verse-number leakage detected
```

**Verse coverage: 208/222 = 93.7%**

| Ch | Expected | Got | Coverage | Notes |
|----|----------|-----|----------|-------|
| 1  | 18       | 16  | 88.9%   | v9, v11 absorbed into v10 (V10 confirmed) |
| 2  | 26       | 26  | 100.0%  | |
| 3  | 22       | 22  | 100.0%  | |
| 4  | 16       | 17  | 106.2%  | 1 may be ch boundary edge case |
| 5  | 20       | 12  | 60.0%   | 8 verses not extracted — parser gap |
| 6  | 12       | 12  | 100.0%  | |
| 7  | 29       | 28  | 96.6%   | v18 absorbed into v17 or v19 |
| 8  | 17       | 16  | 94.1%   | v2 absorbed into v1 (V10 confirmed) |
| 9  | 18       | 17  | 94.4%   | v18 not recovered |
| 10 | 20       | 20  | 100.0%  | |
| 11 | 10       | 10  | 100.0%  | |
| 12 | 14       | 12  | 85.7%   | v1 and v8 not recovered |

## Remaining Issues (for residuals sidecar)

- **14 missing verses** (V4 gaps) — extraction failures, not chapter-structure errors
- **Chapter 5** is the most gapped (8 missing): v10-v16, v20. These correspond to ECC 5:9-20 content about wealth, sleep, and the rich man's burden — likely absorbed into surrounding verses by the extractor
- **V10 absorbed**: ECC.1:9 and 1:11 present in 1:10; ECC.8:2 present in 8:1
- **Narrative headings**: Globally deduplicated to 1 occurrence each. The true OSB heading placements for chs 4-12 should be verified against the PDF in a future pass

## Tooling Created

- `/home/ark/orthodoxphronema/pipeline/tools/fix_ecc_chapters.py` — general Jaccard-based chapter restructure tool (proven pattern, reusable for similar short-chapter books)

## Open Questions

1. Chapter 4 has 17 verses vs. CVC 16 — verify ECC 4:17 (currently assigned there; Brenton has 4:17 as the "Keep thy foot" verse which is part of the text)
2. Chapter 5 gap: were v10-16 and v20 extracted but discarded, or never reached by the parser? Re-extraction from OSB PDF p.~530-535 recommended
3. Should the narrative headings for chs 4-12 be restored after PDF verification?

## Promotion Eligibility

ECC is **NOT promotion-ready** at this time:
- Missing residuals sidecar (ECC_residuals.json)
- No editorial candidates sidecar (ECC_editorial_candidates.json)
- Chapter 5 gap needs human review
- V10 absorbed content not ratified
- Ezra audit not performed

Status: **EDITORIALLY_STAGED** (chapter structure fixed, not yet promotion-gated)
