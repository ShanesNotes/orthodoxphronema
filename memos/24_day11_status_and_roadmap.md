# Memo 24 — Day 11 Status, Roadmap, and Decisions Needed

**Date:** 2026-03-08
**Author:** `ark`
**Type:** `status + roadmap`
**Status:** `active`
**Scope:** `Phase 1 project-wide — GEN / EXO / LEV / infrastructure`
**Audience:** `human` + `ezra`

---

## What Happened Today

Day 11 was the most productive implementation day so far: three major deliverables plus
two infrastructure improvements, all committed and pushed.

### A. Backlog Commit + Push (commit `1b88440`)

All uncommitted work from the immutability enforcement session (Day 10e) was staged,
committed, and pushed. This included:

- OSB immutability policy (memo 22) — binding decision that canon artifacts are
  OSB-faithful; no Brenton/Greek text insertions
- GEN.25:34 removal (osb_source_absent, ratified)
- Per-entry ratification gate in `promote.py`
- 5-class residual taxonomy (`schemas/residual_classes.json`)
- 76-book scan navigation aid (`staging/reference/osb_scan_navigation.json`)
- Greek source text indexer and pilot schema
- 3 new regression tests for the promotion gate

### B. EXO Structural-Fused Resolution (commit `69ac54f`)

EXO was blocked on 10 `structural_fused` V9 errors — inline verse numbers in
enumeration-pattern text that the parser couldn't split. All 10 were resolved by
manual verse separation:

| Source line | Fused verses | Content type |
|---|---|---|
| EXO.21:23 | 24, 25 | lex talionis ("eye for eye...") |
| EXO.25:3 | 4, 5, 6, 7 | tabernacle material list |
| EXO.34:6 | 7 | divine attributes declaration |
| EXO.35:5 | 6, 7, 8 | tabernacle material list |

Three OCR artifacts were fixed inline: `children'schildren` → `children's children`,
`awilling` → `a willing`, `fulllength` → `full-length`.

**Result:** V9 PASS, V4 PASS, promote dry-run exit 0. EXO is now promotion-eligible
(pending Ezra audit).

### C. LEV Extraction + Cleanup (commit `f32e169`)

Leviticus was extracted as the third book. This uncovered and required fixing two
significant infrastructure issues:

#### C1. CVC Correction (Critical Discovery)

The registry's `chapter_verse_counts` for LEV was completely wrong — unverified plan
data totaling 713 verses. Brenton LXX witness shows 27 chapters totaling **859 verses**.
18 of 27 chapter counts were incorrect. Key examples:

| Chapter | Old CVC | Brenton (correct) | Impact |
|---|---|---|---|
| 5 | 19 | 26 | LXX numbering, not Hebrew |
| 6 | 30 | 23 | LXX numbering, not Hebrew |
| 12 | 29 | 8 | Off by 3.6x — chapter advance blocked |
| 13 | 36 | 59 | Off by 1.6x |
| 14 | 9 | 57 | Off by 6.3x |

**This means any book with CVC from the original plan data is suspect.** We must verify
all CVC against Brenton before extracting each new book. The fix was applied and the
registry bumped to v1.2.0.

#### C2. Chapter Advance Guard Enhancement

The 80% chapter-advance threshold worked for GEN/EXO but failed at LEV ch6→ch7 (only
23/30 = 76.7% verses extracted before the boundary). A new **backward-signal fallback**
was added:

- Primary: 80% threshold (unchanged, proven safe)
- Fallback: if `chapter_num < current_verse AND current_verse >= 60% of max_v`, advance
- Rationale: false advances always have `chapter_num ≥ current_verse`, so the backward
  check never fires for them. True missed advances have `chapter_num << current_verse`.

This is provably safe against all known false-advance cases and recovered LEV from
6 chapters / 165 unique anchors to 27 chapters / 850 unique anchors.

#### C3. LEV Final State

| Check | Result | Detail |
|---|---|---|
| V1 anchor uniqueness | PASS | 850 unique anchors |
| V2 chapter count | PASS | 27 chapters |
| V3 chapter sequence | PASS | 1–27 sequential |
| V4 verse gaps | INFO | 6 residual missing anchors (2 gap groups) |
| V7 completeness | WARN | 850/859 (99.0%) |
| V8 heading integrity | PASS | — |
| V9 embedded verse | PASS | After manual separation of 23 embedded verses |

Cleanup applied: 93 R2 fixes, 17 R7 Brenton auto-splits, 22 dropcap repairs.
One leaked Pentecost study article removed (7 numbered sub-points misidentified as verses).
Sidecar generated with 6 `docling_issue` residuals.

### D. Sidecar Generator (in commit `f32e169`)

Added `--generate-sidecar` flag to `validate_canon.py`:

- Collects all V4 gap anchors after validation
- Generates draft `BOOK_residuals.json` with `docling_issue` default classification
- Refuses to overwrite existing sidecars (safety)
- 1 new test added and passing

This eliminates the manual step of creating residual sidecars after each extraction.

### E. Test Suite

All **20 tests** pass (was 19 at session start — 1 new sidecar test added).

---

## Where We Are Now

### Book Status Dashboard

| Book | Verses | V7% | V9 | Promote? | Blocker |
|---|---|---|---|---|---|
| **GEN** | 1529/1532 | 99.8% | PASS | **Ready** | Awaiting Human confirmation |
| **EXO** | 1171/1166 | 100.4% | PASS | **Ready** | Awaiting Ezra audit |
| **LEV** | 850/859 | 99.0% | PASS | Not yet | Awaiting cleanup review + Ezra audit |

Notes:
- GEN has been audited multiple times by Ezra (memos 16, 18, 22). All 3 residuals ratified.
  The immutability rollback was itself an Ezra directive. Promotion is mechanically ready.
- EXO's V7 shows 1171 > 1166 (5 extra verses from over-splits in ch32/35/36). The CVC may
  need minor correction, but this is non-blocking under `--allow-incomplete`.
- LEV residuals need classification review and ratification before promotion eligibility.

### Infrastructure State

| Component | Version | Status |
|---|---|---|
| Registry | v1.2.0 | LEV CVC corrected; other books still suspect |
| Validator | V1–V9 + sidecar gen | All checks operational |
| Promote gate | Sidecar + per-entry ratification | Ready |
| Tests | 20/20 passing | Coverage: validation, promotion, sidecar |
| Parser | backward-signal guard | Handles >20% verse loss gracefully |

### Known Technical Debt

1. **Unverified CVC for ~50 books** — Plan data CVC is unreliable. Must verify against
   Brenton before each extraction. A batch verification script would save time.
2. **Fused articles** — "aburnt", "asoul", "aman" etc. are systematic OCR artifacts
   across all books (~200-250 per book). A dedicated `fix_articles.py` would eliminate
   manual cleanup. Currently handled by `fix_omissions.py` R7 only partially.
3. **EXO CVC over-count** — 5 extra verses in ch32/35/36 need investigation. These may
   be over-splits from the parser or genuine OSB numbering differences vs Brenton.

---

## Where We're Going

### Immediate Decisions Needed

**For Human:**

1. **GEN promotion** — Confirm to run `python3 pipeline/promote/promote.py --book GEN --allow-incomplete`.
   This writes `canon/OT/GEN.md` with checksum and promote_date. All gates pass.
   Ezra has audited GEN multiple times; residuals are ratified.

2. **CVC verification strategy** — LEV's CVC was garbage. Two options:
   - (a) Verify each book's CVC against Brenton immediately before extraction (safe, per-book)
   - (b) Batch-verify all 76 books' CVC now (thorough, one-time cost ~1 hour)
   - Recommendation: option (b) — prevents this class of bug entirely.

3. **Next extraction priority** — Options:
   - NUM (Pentateuch book 4 — large, tests the full pipeline)
   - DEU (Pentateuch book 5 — completes Pentateuch)
   - A short NT book (e.g., PHM, 2JN — proves cross-testament pipeline)

**For Ezra:**

4. **EXO audit** — EXO now passes all structural gates. Ready for audit. Key changes
   since last review: 10 structural_fused verses manually separated, 3 OCR fixes.
   File: `staging/validated/OT/EXO.md`

5. **LEV audit** — First pass extraction with cleanup applied. 850/859 verses, 99.0%.
   6 docling_issue residuals need classification review.
   File: `staging/validated/OT/LEV.md`

6. **Backward-signal safety review** — The new chapter advance fallback is provably safe
   (false advances always have `chapter_num ≥ current_verse`), but a second pair of eyes
   on the logic would be valuable. File: `pipeline/parse/osb_extract.py`, lines ~744-752.

### Proposed Day 12 Plan

| Priority | Task | Depends on |
|---|---|---|
| 1 | GEN promotion (if Human confirms) | Human decision |
| 2 | Batch CVC verification (all 76 books) | Nothing |
| 3 | NUM extraction + cleanup | CVC verification |
| 4 | `fix_articles.py` — systematic fused-article repair | Nothing |
| 5 | EXO CVC investigation (ch32/35/36 over-count) | Nothing |

### Phase 1 Completion Trajectory

With GEN/EXO/LEV at 99%+, the pipeline is proven for Pentateuch-scale books. The
remaining extraction bottleneck is CVC verification + parser edge cases per book.
At current pace (~1 book per session with cleanup), the 5-book Pentateuch could be
complete by Day 14, and the full 76-book canon by approximately Day 30-35.

The `--generate-sidecar` workflow improvement and backward-signal guard mean each new
book requires less manual intervention than GEN/EXO did.

---

## Files Changed Today

| File | Change |
|---|---|
| `staging/validated/OT/EXO.md` | 4 lines split into 14 (structural_fused resolution) |
| `staging/validated/OT/EXO_residuals.json` | Cleared all 10 blocking entries |
| `staging/validated/OT/LEV.md` | New — 850 verses, cleanup applied |
| `staging/validated/OT/LEV_residuals.json` | New — 6 docling_issue entries |
| `staging/validated/OT/LEV_*.json` | New — dropcap, footnote, residue sidecars |
| `pipeline/parse/osb_extract.py` | Backward-signal chapter advance fallback |
| `pipeline/validate/validate_canon.py` | `--generate-sidecar` flag + helper functions |
| `schemas/anchor_registry.json` | v1.2.0 — LEV CVC corrected (713→859) |
| `tests/test_validate.py` | 1 new sidecar generation test |
| `memos/22_osb_immutability_and_secondary_verification_policy.md` | New (Day 10e backlog) |
| `memos/23_lev_extraction_report.md` | New — LEV extraction details |
| `reports/GEN_promotion_dossier.json` | Regenerated |
| `reports/EXO_promotion_dossier.json` | Generated (exit 0) |

---

## Handoff

**To Human:** Review decisions 1-3 above. GEN promotion is the highest-priority
unblocked item.

**To Ezra:** EXO and LEV are ready for audit. The backward-signal logic in
`osb_extract.py` would benefit from your safety review. LEV residuals need
classification verification.

**From Ark:** Standing by for Human confirmation on GEN promotion and next-book
priority. Will begin CVC batch verification if approved.
