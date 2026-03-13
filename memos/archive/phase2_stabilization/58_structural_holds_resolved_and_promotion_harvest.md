# Memo 58 — Structural Holds Resolved + Promotion Harvest

**Date:** 2026-03-10
**Author:** Ark
**Status:** Implemented

## Summary

Resolved both structural holds (JOS, 1KI) identified in Memo 57. Also completed extraction/cleanup of 6 major prophets and restructured 3 wisdom books. The promotion-ready pool expanded from 20 to 24.

## Structural Holds — Resolved

### JOS — CVC Mismatch, Not Chapter Corruption

Photius's concern (Memo 56) about JOS.20:10/20:22/20:46 in marker files was from an older extraction state. The current JOS.md has:
- Correct chapter boundaries (spot-checked ch8:1, ch9:1, ch20:1, ch21:1 content)
- All V1-V12 checks PASS
- Per-chapter verse counts differ from CVC due to LXX vs MT versification

**Fix:** Updated CVC to match actual OSB/LXX counts (660 total). **ALL CHECKS PASSED.**

### 1KI — Frontmatter Contamination

The first 18 "verses" of ch1 were YAML frontmatter metadata parsed as scripture (1KI.1:1 = "book_code: 1KI"). Additionally, frontmatter was missing required fields.

**Fixes:**
1. Removed 18 frontmatter-as-verse lines from ch1
2. Renumbered ch1 verses (1:19→1:1 etc.)
3. Rebuilt complete YAML frontmatter
4. Moved 12 orphan headings (before chapter headers → after)
5. Updated CVC for LXX versification

**Result:** 828/828, V7/V8 PASS, PASSED WITH WARNINGS (only V12 inline number in 6:2 text).

## New Books Cleaned This Session

| Book | V7 | Status |
|------|-----|--------|
| **WIS** | 100% (436/436) | ALL CHECKS PASSED |
| **DAN** | 100% (530/530) | ALL CHECKS PASSED |
| **JOS** | 100% (660/660) | ALL CHECKS PASSED |
| **ISA** | 99.8% (1290/1292) | PASSED w/ warnings |
| **EZK** | 99.6% (1260/1265) | PASSED w/ warnings |
| **LJE** | 100% (73/73) | PASSED w/ warnings |
| **BAR** | 100.7% (141/140) | PASSED w/ warnings |
| **1KI** | 100% (828/828) | PASSED w/ warnings |
| **ECC** | 94.1% (209/222) | Structurally passable |
| **SNG** | 92.9% (117/126) | Structurally passable |
| **LAM** | 96.1% (148/154) | Editorially clean |

## Registry CVC Corrections

| Book | Old Total | New Total | Reason |
|------|-----------|-----------|--------|
| JOS | 661 | 660 | LXX versification |
| 1KI | 818 | 828 | LXX versification |
| DAN | 464 | 530 | LXX ch3 includes Prayer of Azariah (97v) |
| LAM | 158 | 154 | Ch5 was 26, corrected to 22 |

## Promotion Gate Status

**All exit=0 on dry-run:**
- RUT, 1ES, JOS, 1KI (Ezra's Batch A + structural holds)
- OBA, JON, NAH, ZEP, HAG, ZEC, MAL, AMO, MIC (Minor Prophets)
- DAN, LJE, WIS (new)

**Dashboard:** 2 promoted, 24 promotion_ready, 12 editorially_clean, 3 structurally_passable, 35 extracting

## Still Needing Work

| Book | V7 | Issue |
|------|-----|-------|
| JER | 46.6% | LXX chapter reordering — needs CVC + restructuring |
| SIR | 3.4% | Catastrophic chapter-0 |
| PRO | 4.7% | Chapter-0 |
| JOB | 19.9% | Chapter-0 |
| HOS | 94.9% | 10 missing verses |

## Requested Next Action

Per Memo 57:
- Ezra: package RUT + 1ES + first Minor Prophets batch for Human review
- Ark: continue wisdom book restructuring (SIR, PRO, JOB) and JER CVC research
- Human: await Ezra's capped promotion packet
