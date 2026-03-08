# Lowercase Verse Split Strategy + Marker Ownership Fix — 2026-03-07

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `parser / GEN + EXO`

## Context
- Prompted by Day 8 audit finding: V4 gap count (GEN 67, EXO 66) was the primary remaining
  blocker for scale, not cleanup.
- Prior state: `RE_VERSE_SPLIT` only matches uppercase-start verse boundaries. Verses beginning
  with lowercase conjunctions/adverbs (and, then, for, so, but, etc.) were silently merged into
  the preceding verse body.
- Footnote markers were mistakenly attributed to the following verse (pre-boundary capture was
  discarded). OSB physically trails markers after verse-terminal punctuation.

## Objective
- Add a second-pass lc-split recovery stage to `split_verses_in_text`.
- Correct marker ownership: boundary markers from `RE_VERSE_SPLIT` group 1 → preceding verse.
- Reduce V4 gap counts for GEN and EXO; establish targets for further work.

## Files / Artifacts
- `pipeline/parse/osb_extract.py` — `_LC_OPENERS`, `_INLINE_NUM_CTX`, `_lc_boundary_valid`,
  `_lc_split`, `_recover_lc_splits`, `split_verses_in_text` (marker ownership loop, line ~307)
- `staging/validated/OT/GEN.md` — current staged artifact
- `staging/validated/OT/EXO.md` — current staged artifact

## Findings Or Changes

Two distinct fixes, both in `split_verses_in_text` and its call chain:

1. **lc-split recovery**: `_recover_lc_splits` runs as a post-pass on the results list.
   `_lc_split` iterates each verse body looking for `_LC_VERSE_PAT` matches.
   `_lc_boundary_valid` gates each candidate on three signals (terminal punct → inline numeral
   context rejection → sequential +1). Body markers remain on the first sub-segment
   (conservative; position lost after stripping).

2. **Marker ownership**: `markers_str` (RE_VERSE_SPLIT group 1) is now appended to
   `results[-1][3]` rather than discarded. This recovers boundary-captured markers that trail
   a verse.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| `_LC_OPENERS` = narrow conjunctions/adverbs only | Pronouns/articles produce too many false positives | Under-recovery for verses starting "He", "A", "The" | Expand cautiously after auditing remaining gaps |
| Signal 3 (sequential +1) as fallback | Most verse sequences are +1; catches gaps lacking terminal punct | May split inline ordinal sequences | Disable Signal 3 if false-positive surge observed |
| Body markers → first sub-segment | Conservative; intra-body position lost | Marker anchored to wrong sub-verse in lc-split cases | Accept as known limitation; record in sidecar |
| Boundary markers (group 1) → preceding verse | OSB physically places markers after verse-terminal punct | Typesetting anomaly could place marker before verse num | Spot-check against PDF page snippets |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| V4 GEN gaps before Day 9 | 67 | Day 8 extraction run |
| V4 GEN gaps after Day 9 | 28 | Day 9 extraction run |
| V4 EXO gaps before Day 9 | 66 | Day 8 extraction run |
| V4 EXO gaps after Day 9 | 33 | Day 9 extraction run |
| GEN marker count after fix | 243 | Day 9 extraction run |
| EXO marker count after fix | 516 | Day 9 extraction run |

## Open Questions
- What are the opener words for the remaining 28 GEN / 33 EXO gaps? (audit needed)
- Are remaining gaps recoverable by widening `_LC_OPENERS` (e.g., adding "he", "she", "they")?
- Should lc-split marker assignment be revisited for NT books where marker density is higher?
- Are any Signal 3 acceptances producing false splits? (Need diff against ground-truth count)

## Requested Next Action
- Ezra: audit the V4 gap lists for GEN and EXO — classify each remaining gap by its first word
  to determine whether `_LC_OPENERS` expansion or new signals would close them.
- Ark: after Ezra's audit, decide on `_LC_OPENERS` expansion or a new Signal 4 (first-person pronoun).
- Human: confirm promotion readiness threshold (acceptable V4 gap count before first canon promotion).

## Handoff
**To:** `ezra`
**Ask:** audit remaining V4 gap anchors for GEN and EXO; classify by opener word; flag any
that appear to be false splits rather than missed boundaries.

## Notes
- Keep this memo short enough to scan.
- Prefer exact file paths.
- If the change affects canon quality, include before/after counts where possible.
- If ambiguity remains, point to the sidecar JSON or source evidence.
