# Codex Project Deep Dive - 2026-03-12

**Author:** `Codex`  
**Type:** `external_research_audit`  
**Status:** `advisory`  
**Protocol:** non-governing external artifact under `AGENTS.md`; requires ratification in a numbered memo before it changes project policy

## Executive Snapshot

- Repo scale is already substantial: `97` Python files under `pipeline/` at roughly `19,986` LOC, `21` test files at roughly `4,126` LOC, `530` Markdown files, and `368` JSON files.
- Operational maturity is high. The board, ops board, memo index, dashboard, dossier layer, and completion-handshake vocabulary form a real production workflow rather than an ad hoc extraction repo.
- Code health is mixed. `pytest -q` currently reports `27 failed, 294 passed`.
- The live release train is asymmetric:
- OT is effectively complete at `49/49` promoted books, but OT lock is still governance-incomplete because `EST` remains the only live non-`V7` blocker and the `V7` drift packet still awaits ratification.
- NT is wide but unstable: dashboard state shows `27` staged books, with `15` still `extracting`, `6` `editorially_clean`, and `6` `promotion_ready`.
- The worktree is not clean. `reports/2JN_promotion_dossier.json` is modified, and `PROJECT_BOARD.md`, `research/`, and several helper artifacts are currently untracked.

## Strengths

- The project has real invariants, and they are mostly mirrored in code. `pipeline/validate/checks.py` and `pipeline/promote/gates.py` encode the same substrate-protection model described in `AGENTS.md` and the architecture memos.
- The repo has durable operational memory. `PROJECT_BOARD.md`, `memos/ezra_ops_board.md`, `memos/INDEX.md`, promotion dossiers, and the dashboard reduce the usual "chat-only" lossiness that hurts multi-agent work.
- The staged companion and sidecar model is strong. The distinction between scripture, articles, footnotes, markers, residuals, and editorial candidates is sharper than in most text-ingestion pipelines.
- `2JN` is a useful NT calibration point. Dashboard and dossier state both show a clean `promotion_ready` exemplar while larger NT books remain blocked.

## Findings

### 1. Blocking: promotion behavior has drifted away from the composed gate layer

Evidence:
- `pipeline/promote/gates.py` defines explicit D1-D5 gate functions for editorial candidates, freshness, sidecar field normalization, absorbed-content blocking, taxonomy-based ratification, and completeness.
- `pipeline/promote/promote.py` reimplements only a subset inline and does not call the gate module.
- `pytest tests/test_promote_gate.py -q` reports `13 failed, 9 passed`.

Observed drift:
- unresolved editorial candidates do not block
- stale dossiers do not block
- residuals using `class` instead of `classification` do not block
- absorbed-content descriptions do not block
- non-human or null ratification can still pass
- dossier output is missing expected metadata such as `allow_incomplete`, `staged_path`, `residuals_path`, and `editorial_path`
- dossier status synthesis treats some informational checks as `PASS`

Why it matters:
- This is the highest-risk code drift in the repo because it sits on the canon-promotion boundary. The governance docs describe a hard gate system; the current implementation is materially looser than that contract.

Recommended owner:
- `Ark` for implementation repair
- `Ezra` for post-fix audit and gate-contract review

### 2. Blocking: `osb_extract.py` is half-migrated between dict-shaped records and typed records

Evidence:
- `pipeline/common/types.py` defines `VerseRecord` and `FootnoteMarker` dataclasses.
- `pipeline/parse/osb_extract.py` still indexes verses and markers like dictionaries across `ExtractionState`, `_last_anchor`, `_emit_parts`, `build_canon_md`, and `write_outputs`.
- `pytest tests/test_verse_split.py -q` reports `8 failed, 12 passed`.

Observed drift:
- tests that seed `VerseRecord` objects fail because `osb_extract.py` still expects subscripting
- structured marker trace tests fail because marker payloads are still emitted as bare strings or minimal dicts instead of stable trace objects
- output generation still serializes marker sidecars as a flat list instead of a richer metadata-bearing structure

Why it matters:
- This is not just unit-test noise. The parser is the live NT stabilization lane, and this exact seam touches dedup behavior, chapter advance handling, column-split recovery, and marker provenance.

Recommended owner:
- `Ark`

### 3. High: shared helper contracts have drifted from tests and likely from older callers

Evidence:
- `pytest tests/test_common.py -q` reports `6 failed, 34 passed`.
- `pipeline/common/registry.py` now returns `None` for missing books and a dict-shaped `page_ranges()` result.
- `pipeline/common/frontmatter.py` exposes `update_frontmatter_field()` but not `update_frontmatter()`.
- `pipeline/common/text.py` assumes a filesystem path for staged discovery; tests still expect simple list-based filtering.
- `pipeline/common/patterns.py` is missing expected entries such as `overlooked`.

Observed drift:
- this looks like an uncompleted common-layer refactor rather than isolated test breakage
- the failures cluster around API shape and backwards compatibility, not algorithmic correctness

Why it matters:
- This is the kind of drift that silently increases agent error rates because higher-level scripts and tests stop agreeing on what the shared utilities mean.

Recommended owner:
- `Ark`

### 4. Medium: live surfaces are coherent overall, but several artifacts can still mislead operators

Evidence:
- `git diff -- reports/2JN_promotion_dossier.json` shows a local timestamp and `registry_version` change from `1.3.0` to `1.4.0`.
- Dashboard state says `WIS` is fully clean (`PASS` across `V1`-`V9`) while staged editorial candidates still show `2` unresolved entries in `staging/validated/OT/WIS_editorial_candidates.json`.
- Dashboard state says `EST` is `promoted` with a dry-run dossier, while `staging/validated/OT/EST_residuals.json` still has a non-ratified residual and the boards correctly frame it as the OT lock blocker.

Interpretation:
- The boards are currently doing the right thing by naming these distinctions, but the underlying artifacts still require careful reading. A future agent that relies only on dashboard or dossier state could overstate cleanliness.

Recommended owner:
- `Ezra`

### 5. Medium: the project already has a strong agent protocol, but it is carrying too much responsibility at the repo root

Evidence:
- Root `AGENTS.md` is rich and useful, but it owns architecture, release train, role protocol, external AI policy, artifact policy, extraction policy, validation contract, and memo contract in one place.
- Official Codex `AGENTS.md` guidance emphasizes layered instructions from global scope through nested project scope, with nearer files overriding broader guidance.

Why it matters:
- The current root document is strong as a constitution, but not ideal as the only runtime instruction surface. Subsystem-specific constraints for `pipeline/parse/`, `pipeline/promote/`, `research/`, and `staging/validated/` are distinct enough to benefit from local instruction files.

Recommended owner:
- `Ark` for architecture
- `Ezra` for workflow wording and operator-fit review

## Representative Book Truth

| Book | Dashboard / dossier shape | Reading |
|---|---|---|
| `2JN` | `promotion_ready`, dry-run dossier, all core checks pass | current NT exemplar |
| `MAT` | blocked, `V4/WARN`, `V7/WARN`, `V8/WARN`, no residual sidecar | extraction debt, not governance debt |
| `HEB` | blocked, `V4/WARN`, `V7/WARN`, `V8/WARN`, `V9/FAIL`, no residual sidecar | parser and structure debt |
| `EPH` | blocked, `V4/WARN`, `V7/WARN`, `V8/WARN`, `V9/FAIL`, no residual sidecar | sharp NT stabilization target |
| `ROM` | blocked, `V4/FAIL`, `V7/WARN`, `V9/FAIL`, no residual sidecar | structurally worse than the successful footnote pilot might imply |
| `EST` | promoted / dry-run dossier with residual sidecar present | governance-closeout problem, not broad OT instability |
| `WIS` | promoted / dry-run dossier fully clean, but staged editorial candidates still `2` | canonical cleanliness and staged/editorial cleanliness are separate truths |

## Codex-Native Blueprint

### 1. Split the instruction stack by subsystem

Grounding:
- OpenAI's `AGENTS.md` guidance recommends layered instructions discovered from global scope through project and nested directories, with closer files overriding broader ones.

Proposal:
- Keep root `AGENTS.md` as the constitutional contract.
- Add nested instruction files for:
- `pipeline/parse/` to constrain parser changes, OCR heuristics, and source-verification expectations
- `pipeline/promote/` to restate gate and dossier invariants in execution-facing terms
- `staging/validated/` to bias any future agent toward evidence-backed book-local work only
- `research/` to make the external-output protocol impossible to miss

Why this fits this repo:
- Your current workflow is already role- and surface-aware. Layered instruction files would reduce prompt bloat while making it easier for Codex to stay inside local rules.

### 2. Convert recurring audit motions into repo skills

Grounding:
- OpenAI's Skills docs position skills as reusable task packages with progressive disclosure and optional scripts.

Proposal:
- Create a small `.agents/skills/` set for recurring high-value motions:
- `book-audit`: dossier + dashboard + sidecar + validator synthesis for one book
- `promotion-gate-audit`: compare `promote.py`, `gates.py`, tests, and dossier schema
- `nt-stabilization-dossier`: generate a concise MAT/HEB/EPH-style parser-risk packet
- `phase3-contract-check`: inspect memos `86/87/88`, metadata layout, and contract drift before graph work

Why this fits this repo:
- The repo already has ritualized workflows; skills would turn those rituals into loadable, bounded execution packets.

### 3. Use Codex multi-agent fan-out only where the repo already has clean ownership seams

Grounding:
- Official Codex docs treat multi-agent work as a first-class concept and pair it with worktree isolation.

Proposal:
- Use parallel agents for read-heavy analysis lanes only:
- one agent on promotion gates and dossiers
- one on parser/common test failures
- one on dashboard/board/memo state coherence
- Keep Ark as the only merge authority for core pipeline fixes and canon-affecting changes.

Why this fits this repo:
- The repo already uses single-writer discipline. Multi-agent work should accelerate evidence gathering, not blur ownership.

### 4. Add project-scoped MCP for documentation and tool context

Grounding:
- OpenAI's MCP guidance describes MCP as the path for giving Codex access to third-party documentation and developer tools, with configuration supported in project-scoped `.codex/config.toml`.

Proposal:
- Add project-scoped MCP only for bounded, high-signal contexts:
- official documentation lookup
- local schema/doc inspection helpers if you later expose them
- optional design-tool or browser integration for future Phase 3 graph UX work

Why this fits this repo:
- The project already has a large memo and report corpus. MCP should be used surgically, not as a substitute for the repo's own durable artifacts.

### 5. Standardize task packets around Codex prompting strengths

Grounding:
- The 2026 Codex Prompting Guide emphasizes clear upfront instructions, explicit constraints, and long-running autonomous execution when the task boundary is well specified.

Proposal:
- For high-value work, hand Codex a compact packet with:
- exact files or subsystems in scope
- success criteria
- forbidden surfaces
- required verification commands
- expected output artifact path

Why this fits this repo:
- Your project already thinks in packets, memos, and handoffs. Codex performs best when that packet is concrete rather than conversational.

## Priority Order

1. Repair promotion-gate drift before trusting any future promotion automation.
2. Resolve the `osb_extract.py` typed-record seam before broadening NT parser work.
3. Finish the common-utility contract cleanup so tests and helper APIs agree again.
4. Add nested `AGENTS.md` files and a first small skill set after the code contracts stop moving underneath them.
5. Use MCP and broader multi-agent fan-out only after the instruction and contract layers are stable.

## Evidence

- `pytest -q` -> `27 failed, 294 passed`
- `pytest tests/test_common.py -q` -> `6 failed, 34 passed`
- `pytest tests/test_promote_gate.py -q` -> `13 failed, 9 passed`
- `pytest tests/test_verse_split.py -q` -> `8 failed, 12 passed`
- `git status --short`
- `git diff -- reports/2JN_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- representative dossiers for `MAT`, `HEB`, `EPH`, `ROM`, `2JN`, `EST`, `WIS`
- `PROJECT_BOARD.md`
- `memos/ezra_ops_board.md`
- `memos/INDEX.md`

## External References

- AGENTS layering: https://developers.openai.com/codex/guides/agents-md
- Skills: https://developers.openai.com/codex/skills
- Multi-agents: https://developers.openai.com/codex/multi-agent
- MCP: https://developers.openai.com/codex/mcp/
- Prompting guide: https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
