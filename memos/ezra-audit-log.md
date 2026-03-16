# Ezra Audit Log

## 2026-03-06
- Mode: Chief Auditor & Purity Guardian
- Scope: Orthodox Phronema Archive
- Status: Active
- Notes:
  - Audit focus locked: chapter drift, footnote pairing, study-article leakage, purity violations.
  - Tracking initialized per user instruction.

## 2026-03-06 (alias setup)
- Action: Added shell alias for quick launch.
- Alias: `alias ezra="cd ~/orthodoxphronema && codex"`
- Result: Alias line present in `~/.bashrc`; non-interactive shell could not resolve alias immediately.
- Next step: open a new terminal or run `source ~/.bashrc` in your interactive shell.

## 2026-03-06 (repo familiarization)
- Action: Full repository survey after Ark push to `main`.
- Scope reviewed:
  - Project docs: `README.md`, `CLAUDE.md`, architecture and validation memos
  - Core pipeline: `pipeline/parse/osb_extract.py`, `pipeline/validate/validate_canon.py`
  - Registry and schemas: `schemas/anchor_registry.json`
  - Current staged Genesis outputs: `staging/validated/OT/GEN.md`, `GEN_notes.md`, `GEN_footnote_markers.json`
- Current state:
  - No promoted canon files yet; Genesis remains the only staged scripture artifact.
  - Major chapter-drift / duplicate-anchor failures are resolved in the current Genesis pass.
  - Remaining issues are mostly unsplit verses, OCR/drop-cap loss, malformed narrative headings, and note-title normalization defects.
  - Validator now detects missing verse jumps, but purity enforcement is still heuristic and narrow.
- High-priority audit focus next turn:
  - Verse-split misses in Genesis
  - Footnote marker duplication and pairing assumptions
  - Narrative heading contamination inside canon

## 2026-03-07 (Day 5 audit)
- Action: Audited post-push Day 5 promotion and validation state.
- Verified:
  - `pipeline/promote/promote.py` implements frontmatter promotion fields correctly.
  - `staging/validated/OT/GEN_notes.md` title normalization is improved.
  - `staging/validated/OT/GEN_footnote_markers.json` no longer contains the duplicate `GEN.48:3` marker pair.
- Findings:
  - Promotion still proceeds with `V4` missing-verse warnings and `V7` completeness gap warnings.
  - `validate_canon.py` surfaces structural incompleteness but does not escalate it to promotion-blocking severity.
  - Staged Genesis still contains malformed `###` headings that current validation does not catch.

## 2026-03-07 (Day 6 audit)
- Action: Verified post-fix Day 6 validator and promotion behavior directly from current files.
- Verified:
  - `promote.py --dry-run --book GEN` now blocks on `V7` and exits `2`.
  - `promote.py --dry-run --book GEN --allow-incomplete` proceeds and exits `0`.
  - `validate_canon.py` now includes `V8` heading-integrity checks.
  - Former malformed Genesis fragment headings are absent from staged `GEN.md`.
- Residual architectural gap:
  - Only `GEN` currently has `chapter_verse_counts` in `schemas/anchor_registry.json`.
  - As a result, future non-Genesis books would skip `V7`, and promotion would still rely on non-blocking `V4` gap warnings unless the gate is generalized.

## 2026-03-07 (instruction review: Genesis cleanup)
- Action: Reviewed proposed Ark instruction for `fix_omissions.py` against repo memos and current pipeline state.
- Conclusion:
  - The ratification-first structure is good.
  - The automatic inference of missing first letters is not safe as written and conflicts with prior memo guidance that drop-cap omissions are not auto-fixable without source-backed certainty.
  - Automatically applying the exact same cleanup script to every future book at parse time would violate the project's validation-first / no-silent-transformation standard unless each cleanup rule is bounded, auditable, and validator-backed.
- Repo state note:
  - Current checkout still only contains staged Genesis artifacts; no staged Exodus file is present.

## 2026-03-07 (cleanup verification and drop-cap strategy)
- Action: Verified current `fix_omissions.py`, `GEN_clean.md`, and `08_gen_cleanup_report.md`.
- Confirmed:
  - Cleanup script is conservative and keeps drop-cap repair in report-only mode.
  - Report and output paths exist as claimed.
- Residual note:
  - `GEN_clean.md` still contains unresolved fused-word artifacts such as `ashepherd`, `amanufacturer`, `alawgiver`, `aspreading`, and `acoffin`.
- Recommendation:
  - Use LLMs for proposal/ranking only on drop-cap repair.
  - Require source-backed confirmation via per-anchor provenance and PDF/page snippet verification before canon adoption.

## 2026-03-07 (strict pre-ratification cleanup audit)
- Action: Ran an additional read-only scan of `GEN_clean.md` for unresolved cleanup misses.
- Confirmed unresolved fused compounds remain at multiple anchors, including:
  - `GEN.4:2` `ashepherd`
  - `GEN.4:22` `asmith`, `amanufacturer`
  - `GEN.6:16` `acubit`
  - `GEN.9:14` `acloud`
  - `GEN.9:20` `ahusbandman`
  - `GEN.9:23` `agarment`
  - `GEN.10:9` `ahunter`
  - `GEN.11:4` `aname`
  - `GEN.45:7` `aremnant`
  - `GEN.47:26` `alaw`
  - `GEN.48:19` `apeople`, `amultitude`
  - `GEN.49:10` `alawgiver`
  - `GEN.49:15` `afarmer`
  - `GEN.49:19` `araider`
  - `GEN.49:21` `aspreading`
  - `GEN.49:22` `agrown-up`
  - `GEN.50:11` `adeep`
  - `GEN.50:26` `acoffin`

## 2026-03-07 (workflow recommendation: single staged artifact)
- Action: Reviewed whether `GEN.md` and `GEN_clean.md` should coexist long-term.
- Recommendation:
  - Keep one staged scripture artifact per book.
  - Apply bounded cleanup directly to the staged file once the cleanup rules are approved.
  - Preserve auditability through git commits, diff reports, and sidecar/memo outputs rather than parallel `*_clean.md` files.
- Reason:
  - Parallel clean files are useful for one-off experimentation but become noisy for versioning and promotion semantics.

## 2026-03-07 (Brenton auxiliary witness review)
- Action: Reviewed newly added Brenton Septuagint text corpus and current cleanup scripts.
- Confirmed:
  - Brenton files exist chapter-by-chapter under `src.texts/Brenton-Septuagint.txt/`.
  - Sample chapter files for Genesis 1 and Exodus 1 are structurally usable: two-line header plus one verse-like line per verse.
  - `fix_omissions.py` now supports per-book allowlists and in-place cleanup.
  - `dropcap_verify.py` is still heuristic-only and should be superseded by a Brenton-backed verification path.
- Planning conclusion:
  - Brenton can serve as an auxiliary witness for micro-corrections and confidence scoring, but not as a replacement text source.

## 2026-03-07 (drop-cap model critique)
- Action: Reviewed Brenton-backed `dropcap_verify.py` and current `GEN_dropcap_candidates.json`.
- Findings:
  - The current model brute-forces `A`–`Z` against full-verse Brenton similarity, which overfits to Brenton's frequent leading `And`.
  - This produces implausible proposals like `Aow`, `Ahen`, and `Ahus`.
  - Genesis drop-cap residuals are dominated by a very small prefix family: `ow` (37), `hen` (6), `hus` (2), `nthe` (1), `his` (1), `fter` (1), `oearly` (1), `tcame` (1).
- Recommendation:
  - Use OSB residual-shape heuristics as the primary classifier for drop-caps.
  - Use Brenton only as a secondary confirmation signal on prefix compatibility, not as the letter generator.

## 2026-03-07 (Day 8 workflow review)
- Action: Reviewed the post-Day-8 cleanup / drop-cap / validation stack.
- Confirmed:
  - `dropcap_verify.py` is now OSB-residual-first and no longer lets Brenton generate letters.
  - Deterministic normalization rules R2/R5 are already integrated into `osb_extract.py`.
  - Registry `chapter_verse_counts` now covers 64 books, so V7 scaling is much stronger.
- Main optimization conclusion:
  - Drop-cap repair is no longer the bottleneck.
  - The primary remaining blocker for scale is parser-side lowercase-start verse splitting (`V4` gaps), not cleanup.

## 2026-03-07 (footnote-marker placement concern)
- Action: Reviewed current footnote-marker extraction assumptions in `osb_extract.py`.
- Finding:
  - Current code and comments still assume markers appear at verse starts / before next verse numbers.
  - User observation indicates OSB markers are visually placed after verse punctuation, i.e. trailing the verse they annotate.
- Implication:
  - Marker ownership should be treated as belonging to the preceding verse boundary, not the following one.
  - `_recover_lc_splits()` comment and marker propagation logic are structurally unsafe under the observed source layout.

## 2026-03-15 (NUM re-promotion audit)
- Action: Audited NUM staging for re-promotion after 1:1 truncation fix and 6:27 recovery.
- Scope: NUM.1:1 full text, NUM.6:27 existence, ch16/17 and ch29/30 LXX boundaries.
- Result: **PASS — cleared for re-promotion.**
- Verified:
  - NUM.1:1 full verse present (ends "...saying,"); canon had truncation at "test".
  - NUM.6:27 restored (was missing from canon, absorbed into 6:23 during extraction, fixed 2026-03-10).
  - Ch16 ends at v35, ch17 starts at v1 (LXX numbering correct).
  - Ch29 ends at v39, ch30 starts at v1 (LXX numbering correct).
  - 1,288 anchors match registry v1.7.6 expectation.
  - D1 editorial: clear (0 candidates). Residuals: 0 open.
- Non-blocking observations:
  - Residuals file carries registry_version 1.2.2 (historical trace, not gate input).
- Promoted: 2026-03-15, checksum 7c372929.

## 2026-03-15 (DEU re-promotion audit)
- Action: Audited DEU staging for re-promotion after mega-line fix.
- Scope: Chapter 29-31 region (previously fused into 7,281-char mega-line at 29:1).
- Result: **PASS — cleared for re-promotion.**
- Verified:
  - Ch29 verses 1-28 each on own line, no gaps/duplicates.
  - Ch30 verses 1-20 each on own line (registry corrected 19→20 at v1.7.5).
  - DEU.30:19 and DEU.30:20 correctly separate.
  - Chapter headers 29/30/31 properly placed.
  - V1-V4, V7-V9 all PASS (962/962 anchors).
  - Residuals sidecar: zero open items.
  - Content integrity vs canon mega-line: text matches across all spot-checked verses.
- Non-blocking observations:
  - "afar land" vs "a far land" at DEU.29:21 — pre-existing OCR artifact, not introduced by fix.
  - Em-dash normalization (hyphen vs em-dash) — pre-existing, book-wide pattern.
- Promoted: 2026-03-15, checksum ae2dee8d.

## 2026-03-07 (team workflow review)
- Action: Reviewed current collaboration pattern against proposed dual-agent workflow changes.
- Recommendation:
  - Keep Ark as sole writer / committer / architectural owner for now.
  - Use repo-native artifacts (`memos/`, `reports/`, staged outputs) for handoff before adding a new `reviews/` folder.
  - Split responsibility by risk:
    - Ark owns implementation and promotion paths.
    - Ezra owns audits, risk briefs, parser/cleanup critiques, and decision memos.
- Reason:
  - This preserves single-threaded ownership of canon-affecting writes while reducing copy/paste loss through durable handoff documents.

## 2026-03-07 (workflow protocol formalized)
- Action: Replaced the old Ezra-only `AGENTS.md` with a team protocol and added a reusable memo template.
- Files:
  - `AGENTS.md`
  - `memos/_template_work_memo.md`
- Outcome:
  - Single-writer ownership is now explicit.
  - `memos/` is formalized as the default durable handoff layer.
  - Memo expectations for substantial changes are now documented in-repo.
