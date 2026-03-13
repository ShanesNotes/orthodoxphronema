# Memo 35 — Group 4: Post-Exilic + Deuterocanon Historical Extraction Status

**Date:** 2026-03-09
**Author:** Ark
**Scope:** 1ES, EZR, NEH, TOB, JDT, EST, 1MA, 2MA, 3MA (9 books)

## Summary

All 9 books in Group 4 are extracted, cleaned, validated, and have promotion dossiers.
Total: 23 OT books now extracted (Pentateuch 5 + Historical A 5 + Historical B 4 + Group 4 9).

## Per-Book Status

| Book | V7% | Verses | Gaps | Structural Issues | Status |
|------|-----|--------|------|-------------------|--------|
| 1ES | 99.7% | 315/316 | 1 | None | editorially_clean |
| EZR | 99.5% | 207/208 | 1 | None | promotion_ready |
| NEH | 99.7% | 403/404 | 1 | None | editorially_clean |
| TOB | 99.3% | 282/284 | 2 | None | editorially_clean |
| JDT | 100.0% | 339/339 | 0 | None | promotion_ready |
| EST | 99.5% | 194/195 | 1 | Catastrophic: ch0-7→ch1-10 | editorially_clean |
| 1MA | 99.8% | 922/924 | 2 | V9 splits (5), ch3 duplicates | editorially_clean |
| 2MA | 99.5% | 552/555 | 3 | V9 splits (4) | editorially_clean |
| 3MA | 99.6% | 227/228 | 1 | Catastrophic: ch2→ch2-7, V9 splits (2) | editorially_clean |

## Notable Structural Reconstructions

### EST (Esther)
- OSB integrates Greek additions A-F at narrative positions
- Registry corrected: 16ch → 10ch, CVC updated to match OSB structure
- Ch0 (Addition A) merged into ch1; ch7 split into ch7-10
- V9 splits: 1:10→1:11, 2:5→2:6, 9:8→9:9, 9:22→9:23/9:24
- Ch3 duplicate 3:14/3:15 renumbered to 3:16/3:17

### 3MA (3 Maccabees)
- Chapters 3-7 collapsed into ch2 (extractor missed 5 chapter advances)
- Reconstructed using Brenton content matching for chapter boundaries
- 9 recurring page-layout section headers removed (Docling artifact)
- V9 splits: 5:6→5:6+5:7+5:8, 6:2→6:2+6:3
- Ch1 CVC mismatch: 28 extracted vs 29 in registry (OSB versification)

### 1MA (1 Maccabees)
- Ch3 duplicate anchors 3:46-48 resolved (poetic continuation merged into 3:45)
- 5 V9 embedded verse splits

## Tooling Improvements

### dropcap_verify.py bug fix
- `missing_prefix` field was storing the full repair prefix (e.g., "Then ") instead of just the missing character(s) (e.g., "T")
- `apply_repairs()` prepends `missing_prefix` to existing text, so the full prefix caused double text ("Then hen Philopator...")
- Fix: `matched_prefix = repair_prefix[:missing_count]` — now stores only the dropped character(s)

### fix_3ma_structure.py (new)
- Content-based chapter boundary detection using Brenton first-verse signatures
- Handles re-running on already-reconstructed files (flattens verses first)
- V9 split integration for ch5 and ch6

## Promotion Blockers

All 9 books blocked on D5 gate: `ratified_by: 'human'` required on residuals sidecar.
JDT is the only book at V7 100% — all others have docling_issue residuals.

## Next Steps

1. Human ratification of residuals for Ezra audit
2. Continue to Group 5 (Wisdom/Poetry: PSA, PRO, ECC, SNG, JOB, WIS, SIR)
3. Psalms (PSA) will be the most challenging extraction (150 chapters, poetry layout)
