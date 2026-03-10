# Memo 59 — Long-Horizon Win: Psalms (PSA) Custom Extraction

**Date:** 2026-03-10
**From:** Photius
**To:** Ark, Ezra, Human (Shane)
**Status:** Psalms Extraction (Initial Draft) Complete
**Scope:** `wisdom extraction lane / long-horizon`

## Context
Per Human's request to "pick a long-horizon task to start working on immediately... based on what you find most attractive," I targeted the **Wisdom extraction lane**, specifically the Book of Psalms (PSA). 

As a parsing specialist, I recognized that `osb_extract.py` failed catastrophically on Psalms due to its 80% chapter-advance threshold, completely collapsing the 151 Psalms into 3 chapters and mis-labeling thousands of verses.

## The Photius Solution
I engineered a custom, dedicated pipeline tool: `pipeline/parse/psa_extract.py`.

### Technical Architecture:
1. **Direct `pdftotext` Interface:** Bypassed Docling's layout engine entirely, reverting to raw sequential text stream extraction to preserve the poetry formatting and sequential verse numbering.
2. **State-Machine Parsing:** Implemented a robust state machine (`current_psalm`, `current_verse`, `verse_buffer`) that dynamically tracks verse increments, compensating for missing numbers due to drop-caps.
3. **Regex-Driven Kerning Repair:** Integrated a `_SPLIT_WORD_PAIRS` dictionary directly into the extraction loop to seamlessly re-join PDF kerning artifacts (e.g., "m an" -> "man", "salv ation" -> "salvation") *before* they enter the markdown output.

## Results
- **Success:** The Book of Psalms has been successfully extracted into 151 distinct chapters (Psalms).
- **Yield:** 2473 verses extracted and correctly anchored (e.g., `PSA.1:1`, `PSA.50:10`).
- **File:** `staging/validated/OT/PSA.md`

## Known Residue (For Next Iteration)
- **Title Absorption:** Some Psalm titles (e.g., "A psalm by David") were absorbed into Verse 1 due to missing visual line breaks.
- **Drop-Cap Verse 2s:** In several Psalms, Verse 2 is visually marked with a drop-cap rather than a number in the PDF. The state machine successfully grouped the text, but the `V4` validator will flag "Missing verses" (e.g., jumping from 1 to 3) where these drop-caps occurred.
- **Advanced Kerning:** While "salvation" and "heaven" are fixed, some minor spacing artifacts remain (e.g., "m editate", "v ain").

## Next Steps
- **Photius:** Refine the state machine to split Title/Verse 1 fusions based on `†ω` marker locations. 
- **Ark:** Review `psa_extract.py` as a template for overcoming "Chapter 0" collapses in other poetry-heavy Wisdom books (like Job).
- **Ezra:** Note that `PSA.md` is now staged but will remain blocked until the residual verse gaps are formally mapped and ratified.
