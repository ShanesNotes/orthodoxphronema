# Codex Optimization Execution Plan - 2026-03-12

**Author:** `Codex`  
**Type:** `external_research_execution_plan`  
**Status:** `advisory`  
**Protocol:** non-governing external artifact under `AGENTS.md`

## Purpose

Turn the 2026-03-12 deep-dive findings into an execution sequence that:

- uses Photius today on bounded high-throughput evidence work
- leaves Ark one clean core lane at a time tomorrow
- avoids policy churn while the repo still has active contract drift

This plan assumes Ark is unavailable until 2026-03-13 and that Photius is available now.

## Optimization Priorities

### Priority 1: Repair promotion contract drift

Why first:
- it is the highest-risk mismatch between documented workflow and live code
- it sits directly on the canon-promotion boundary
- the failing test cluster is clean and well-bounded

Primary surfaces:
- `pipeline/promote/promote.py`
- `pipeline/promote/gates.py`
- `tests/test_promote_gate.py`

Done when:
- the live promote path delegates to the composed gate layer or matches it behaviorally
- dossier fields match the expected evidence contract
- the promotion-gate test cluster is green

### Priority 2: Finish the `osb_extract.py` typed-record migration

Why second:
- parser drift is real, but the repo already has recent NT stabilization momentum
- the failure cluster is implementation-local and should be handled as one coherent migration
- leaving this half-migrated will keep future parser work brittle

Primary surfaces:
- `pipeline/parse/osb_extract.py`
- `pipeline/common/types.py`
- `tests/test_verse_split.py`

Done when:
- extraction state and output generation use one stable internal record model
- marker traces have a stable structured payload
- the verse-split test cluster is green

### Priority 3: Close the common-layer contract drift

Why third:
- important, but lower risk than promotion and parser seams
- likely a compatibility cleanup lane rather than new design work
- best handled after Ark has restored the two more dangerous boundaries

Primary surfaces:
- `pipeline/common/registry.py`
- `pipeline/common/frontmatter.py`
- `pipeline/common/text.py`
- `pipeline/common/patterns.py`
- `tests/test_common.py`

Done when:
- tests and helper APIs agree on the intended contract
- symbols under dispute are either restored or callers/tests are updated in one pass

## Agent Orchestration

### Ezra lane: route, compress, and hand off

Ezra should own:
- converting the deep-dive findings into tomorrow's implementation queue
- keeping `memos/ezra_ops_board.md` aligned only if routing materially changes
- ensuring Human sees no more than the existing bounded decision load

Ezra should not absorb implementation in `pipeline/promote/`, `pipeline/parse/`, or `pipeline/common/` while Ark is out, unless Photius discovers a truly trivial non-architectural fix and Human explicitly prefers immediate action.

### Photius lane: evidence packaging, not core implementation

Photius is the best fit today for:
- mismatch reports
- line-referenced migration maps
- contract censuses
- repeated test-run evidence packaging

Photius should not edit:
- `pipeline/promote/`
- `pipeline/parse/`
- `pipeline/validate/`
- `schemas/`

Photius should deliver:
1. promotion-gate drift packet
2. parser typed-record migration packet
3. common-layer contract census

These should become Ark-ready packets, not independent strategy documents.

### Ark lane tomorrow: one core lane at a time

Ark should execute in this order:

1. promotion gate repair
2. parser typed-record migration
3. common-layer compatibility cleanup

Reason:
- this minimizes canon-boundary risk first
- then restores parser stability
- then removes lower-level helper drift

## Suggested Today / Tomorrow Sequence

### Today: evidence compression

1. Photius runs the delegated packet already prepared.
2. Ezra consolidates Photius output with the existing deep-dive findings.
3. Ezra publishes one concise implementation queue for Ark's return.

### Tomorrow morning: Ark picks up Priority 1

Ark implementation target:
- make `promote.py` align with `gates.py`
- restore dossier schema expectations
- make `tests/test_promote_gate.py` green

Exit condition:
- no parser or common-layer work started until the promote lane is closed or paused with a memo-quality handoff

### Tomorrow after Priority 1: Ark picks up Priority 2

Ark implementation target:
- normalize `osb_extract.py` around a single internal record shape
- finish marker trace structure migration
- make `tests/test_verse_split.py` green

### After parser stability: Ark picks up Priority 3

Ark implementation target:
- resolve helper API intent in one compatibility pass
- make `tests/test_common.py` green

## Codex-Native Optimizations To Defer

These are worthwhile, but should wait until the code contracts above stop moving:

- nested `AGENTS.md` files under `pipeline/parse/`, `pipeline/promote/`, `staging/validated/`, and `research/`
- repo-local skills for book audit, promotion audit, NT stabilization, and Phase 3 contract checking
- broader multi-agent fan-out beyond bounded read-heavy review lanes
- project-scoped MCP beyond documentation lookup

Reason:
- otherwise the repo will encode unstable assumptions into new automation surfaces

## Concrete Deliverables Expected

### From Photius

- one durable memo or report with all three evidence packets
- exact failing tests
- exact file references
- grouped findings
- no implementation changes

### From Ezra

- one compressed routing packet for Ark
- optional ops-board refresh only if the priority order changes

### From Ark

- repaired promote path and dossier schema
- repaired parser typed-record seam
- reconciled common helper contract
- targeted verification after each lane, not one giant mixed pass

## Risks To Watch

- accidental scope creep from "optimization" into workflow redesign before code repair
- Photius being asked to implement in Ark-owned core surfaces
- stale boards after evidence changes
- mixed-lane commits that blur whether promotion, parser, or helper regressions were fixed

## Recommended Verification Order

1. `pytest tests/test_promote_gate.py -q`
2. `pytest tests/test_verse_split.py -q`
3. `pytest tests/test_common.py -q`
4. `pytest -q`

That order matches the recommended repair order and keeps regression signals localized.

## Ratification Path

Because this artifact is external and non-governing, adopt it only through a numbered memo if its routing or protocol recommendations become project policy.
