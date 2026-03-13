# GEN + EXO V4 Edge-Case Source Verification — 2026-03-07

**Author:** `ezra`
**Type:** `audit`
**Status:** `complete`
**Scope:** `GEN / EXO remaining V4 edge cases`

## Context
- Follow-up to [`10_lowercase_verse_split_strategy.md`](/home/ark/orthodoxphronema/memos/10_lowercase_verse_split_strategy.md).
- Goal: verify the disputed edge-case anchors against the OSB PDF source text, not just staged artifacts or Brenton.
- Source checked: [`src.texts/the_orthodox_study_bible.pdf`](/home/ark/orthodoxphronema/src.texts/the_orthodox_study_bible.pdf)
- Extraction method: `pdftotext -layout` on the registry text-page spans for `GEN` and `EXO`.

## Summary
The checked edge cases are real source-side verse boundaries in the OSB text layer. The failures are not explained by a simple lowercase-opener miss alone.

| Anchor | Source status | Verified source shape | Audit conclusion |
|---|---|---|---|
| `GEN.9:26` | present | `26 He also said,` | Verse exists; staged numbering drifted after a missed earlier split. |
| `GEN.14:2` | present | `2that they made war ...` | Digit is fused to opener; boundary exists but is shape-corrupted. |
| `GEN.25:18` | present | `18(He dwelt ...` | Boundary exists with parenthetical opener after the digit. |
| `GEN.49:2` | present | `2 "Gather together and hear ...` | Verse exists as a separate poetic block; staged text truncated `49:1` and lost `49:2`. |
| `EXO.4:5` | present | `5"so they may believe ...` | Boundary exists; digit is fused to opening quote/text. |
| `EXO.34:14` | present | `14(for you shall worship ...` | Boundary exists with parenthetical opener. |
| `EXO.38:7` | present | `7(a cherub at one end ...` | Boundary exists with parenthetical opener. |

## Verified Cases

### `GEN.9:26`
- Staged artifact:
  - [`staging/validated/OT/GEN.md:287`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L287)
  - [`staging/validated/OT/GEN.md:288`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L288)
  - [`staging/validated/OT/GEN.md:289`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L289)
- Source verification:
  - OSB text layer contains a distinct verse boundary: `26 He also said,`
- Conclusion:
  - `GEN.9:26` is not absent in the source.
  - The staged file mislabeled the following material as `GEN.9:25`, so this is a numbering-drift case after a missed split.

### `GEN.14:2`
- Staged artifact:
  - [`staging/validated/OT/GEN.md:424`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L424)
  - [`staging/validated/OT/GEN.md:425`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L425)
- Source verification:
  - OSB text layer shows: `... and Tidal king of nations, 2that they made war ...`
- Conclusion:
  - The verse boundary exists.
  - The digit is fused directly to the opener word, so a `\d+\s+word` assumption is too strict here.

### `GEN.25:18`
- Staged artifact:
  - [`staging/validated/OT/GEN.md:832`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L832)
  - [`staging/validated/OT/GEN.md:833`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L833)
- Source verification:
  - OSB text layer shows: `... was added to his people. 18(He dwelt opposite Egypt ...`
- Conclusion:
  - The verse boundary exists.
  - The opener is parenthetical; a candidate pattern must allow opening punctuation after the digit.

### `GEN.49:2`
- Staged artifact:
  - [`staging/validated/OT/GEN.md:1783`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L1783)
  - [`staging/validated/OT/GEN.md:1784`](/home/ark/orthodoxphronema/staging/validated/OT/GEN.md#L1784)
- Source verification:
  - OSB text layer shows:
    - `49 Now Jacob called his sons and said, "Gather together, that I may tell you what shall befall you in the last days ...`
    - `2 "Gather together and hear, you sons of Jacob, ...`
- Conclusion:
  - `GEN.49:2` is a real separate verse in the source.
  - This is not a lowercase-opener case; it is a poetic-block / truncation failure.

### `EXO.4:5`
- Staged artifact:
  - [`staging/validated/OT/EXO.md:106`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L106)
  - [`staging/validated/OT/EXO.md:107`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L107)
- Source verification:
  - OSB text layer shows: `... it became a rod in his hand), 5"so they may believe ...`
- Conclusion:
  - The verse boundary exists.
  - The staged `5's othey` shape is downstream OCR/text-normalization corruption, not absence in the PDF text layer.

### `EXO.34:14`
- Staged artifact:
  - [`staging/validated/OT/EXO.md:1240`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L1240)
  - [`staging/validated/OT/EXO.md:1241`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L1241)
- Source verification:
  - OSB text layer shows: `... graven images of their gods with fire 14(for you shall worship no other god ...`
- Conclusion:
  - The verse boundary exists.
  - Parenthetical openers must be supported explicitly.

### `EXO.38:7`
- Staged artifact:
  - [`staging/validated/OT/EXO.md:1373`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L1373)
  - [`staging/validated/OT/EXO.md:1374`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md#L1374)
- Source verification:
  - OSB text layer shows: `... two cherubim of pure gold 7(a cherub at one end ...`
- Conclusion:
  - The verse boundary exists.
  - Parenthetical opener handling is required here as well.

## Implications
- Expanding `_LC_OPENERS` alone will not close these cases.
- The candidate boundary pattern in [`pipeline/parse/osb_extract.py:56`](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py#L56) and [`pipeline/parse/osb_extract.py:78`](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py#L78) likely needs to tolerate:
  - digit fused to opener text, as in `2that`
  - digit followed by opening punctuation, as in `18(`, `14(`, `7(`
  - digit followed by opening quote, as in `5"so`
- `GEN.49:2` is a separate poetic-block truncation case and should not be treated as a normal lowercase-opener miss.

## Recommended Next Action
- Ark:
  - Add a boundary-shape pass or widen the split regex to allow optional opening punctuation / quote after the verse number.
  - Treat `GEN.49:2` as a separate parser-block carryover issue.
- Ezra:
  - After Ark patches the boundary shape handling, rerun the gap audit before any promotion decision.
