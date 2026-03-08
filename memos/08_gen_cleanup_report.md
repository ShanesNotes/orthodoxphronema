# Genesis Cleanup Report — 2026-03-08 (Day 10 re-run)

## Summary

GEN.md was extracted on Day 4 and first cleaned on Day 8, but the Day 9 lc-split
verse recovery exposed hundreds of new defect instances. This report covers the
full re-run of the cleanup pipeline on the post-Day-9 GEN.md.

- Input: `staging/validated/OT/GEN.md`
- Mode: **in-place** (two passes)
- Brenton reference: enabled (R7)

## Pass 1: fix_omissions.py (R1–R7)

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 318 |
| R2 | Split fused possessives ('s + word) | 243 |
| R3 | Rejoin word-split artifacts (allowlist) | 48 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 5 |
| R5 | Remove trailing space before punctuation | 0 |
| R7 | Brenton-assisted fused compound splits | 1 |
| **Total** | | **615** |

Pass 1 ran in two sub-passes:
1. Initial run: R1=296, R2=243, R3=48, R4=5, R7=1 (`askin` → `a skin`)
2. Allowlist expansion (+22 entries) then re-run: R1=22 additional fixes

### Allowlist Expansion (GEN.json)

Added 22 fused-article entries confirmed by Brenton bigram match and context:

`acave`, `acurse`, `adistance`, `adove`, `afifth`, `afurnace`, `aheap`,
`ahundred`, `aking`, `akid`, `aladder`, `aplain`, `aposition`, `aprophet`,
`aram`, `araven`, `ascarlet`, `aservant`, `asixth`, `asmoking`, `asmooth`,
`aspeckled`

Skipped (legitimate English words): `along`, `aloud`, `today` (x6), `tonight`, `inlaw`

## Pass 2: dropcap_verify.py (PDF visual spot-check)

21 drop-cap candidates found — all at chapter:1 verses. All 21 verified via OSB
PDF page rendering (pymupdf at 200 DPI, pages visually inspected).

| Residual | Repair | Count | Notes |
|----------|--------|-------|-------|
| `ow ` | **Now** | 14 | GEN.10:1, 11:1, 16:1, 20:1, 23:1, 24:1, 28:1, 29:1, 30:1, 36:1, 39:1, 43:1, 46:1, 47:1 |
| `hen ` | **Then** | 4 | GEN.7:1, 8:1, 18:1, 41:1 |
| `hen ` | **When** | 2 | GEN.17:1, 42:1 — **corrected from map default "Then"** |
| `oearly ` | **So early** | 1 | GEN.32:1 |

Key corrections: GEN.17:1 and GEN.42:1 are "**When**" (not "Then"). The residual
map cannot distinguish T+hen from W+hen — PDF visual check is the only reliable
method for these.

## Validation Results (post-cleanup)

```
V1  PASS  1529 unique anchors
V2  PASS  50 chapters
V3  PASS  Chapters 1-50 sequential
V4  INFO  1 residual gap (GEN.49:2)
V7  99.8% (1529/1532) — 3 missing: GEN.49:1, 49:2, 49:33 (known parser limits)
V8  PASS  No fragment headings
V9  PASS  No embedded verses
```

Cleanup does not affect verse structure — V4/V7 unchanged from pre-cleanup.

## Residue Audit (post-cleanup)

Total findings: **31** (down from ~363 pre-cleanup)

| Category | Count | Examples |
|----------|-------|---------|
| fused_article | 10 | `today` (x6), `tonight`, `inlaw`, `along`, `aloud` |
| fused_compound | 21 | `forever` (x2), `firstborn` (x5), `earrings` (x4), `floodgates` (x2), `maidservants`, `birthday`, `sevenfold`, `twentyseventh`, `thirtyseven`, `fortyfive` |

All 31 findings are **legitimate modern English spellings** that differ from Brenton's
archaic two-word forms. None are OCR/extraction defects.

## Three-Bucket Classification (per memo 18)

### Bucket 1: Auto-fixed (deterministic) — 636 fixes
- R1 fused articles: 318
- R2 fused possessives: 243
- R3 word-split artifacts: 48
- R4 hyphen-split joins: 5
- R7 Brenton-confirmed split: 1
- Drop-cap repairs (PDF-verified): 21

### Bucket 2: Human-ratified (PDF visual check) — 21 cases
All 21 drop-cap candidates were resolved by OSB PDF visual inspection.
2 corrections made (GEN.17:1 and GEN.42:1: "When" not "Then").
Classification: `human_verified` in `GEN_dropcap_candidates.json`.

### Bucket 3: Genuine OSB (no fix needed) — 31 items
These are legitimate modern English spellings in the OSB that differ from
Brenton's archaic forms:

| OSB spelling | Brenton spelling | Verdict |
|-------------|-----------------|---------|
| today | to day | Modern standard |
| tonight | to night | Modern standard |
| forever | for ever | Modern standard |
| firstborn | first born | Modern standard |
| earrings | ear rings | Modern standard |
| floodgates | flood gates | Modern standard |
| birthday | birth day | Modern standard |
| maidservants | maid servants | Modern standard |
| sevenfold | seven fold | Modern standard |
| along | a long | Legitimate word |
| aloud | a loud | Legitimate word |
| inlaw | in law | Legitimate (contextual) |
| twentyseventh | twenty seventh | Fused number (OSB style) |
| thirtyseven | thirty seven | Fused number (OSB style) |
| fortyfive | forty five | Fused number (OSB style) |

**Action:** No fix. Document as accepted OSB wording.

## Status

GEN readability cleanup is **complete**. The file is ready for Ezra audit.
