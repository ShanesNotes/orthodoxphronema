# Codex Photius Delegation Packet - 2026-03-12

**Author:** `Codex`  
**Type:** `external_delegation_packet`  
**Status:** `ready`  
**Audience:** `Photius`  
**Protocol:** non-governing external artifact under `AGENTS.md`

## Role

Operate as `Photius` under `AGENTS.md` and `GEMINI.md`.

You are not `Ark`.
You are not `Ezra`.
This is a bounded evidence-packaging lane only.

## Hard Constraints

- Do not edit `canon/`
- Do not edit `pipeline/parse/`
- Do not edit `pipeline/promote/`
- Do not edit `pipeline/validate/`
- Do not edit `schemas/`
- Do not perform implementation work
- You may write only bounded evidence artifacts in `memos/` or `reports/`

## Mission

Package implementation-ready evidence for Ark's return on 2026-03-13 so he can repair three known contract-drift lanes without rediscovering them.

## Task 1: Promotion Gate Drift Packet

Read:
- [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py)
- [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py)
- [test_promote_gate.py](/home/ark/orthodoxphronema/tests/test_promote_gate.py)

Produce a line-referenced mismatch report grouped into:
- missing gate enforcement
- dossier schema drift
- validation status drift

For each finding include:
- exact expected behavior from tests or `gates.py`
- actual behavior in `promote.py`
- exact failing test names
- whether the issue is blocking or non-blocking

## Task 2: Parser Typed-Record Migration Packet

Read:
- [osb_extract.py](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py)
- [types.py](/home/ark/orthodoxphronema/pipeline/common/types.py)
- [test_verse_split.py](/home/ark/orthodoxphronema/tests/test_verse_split.py)

Produce a line-referenced migration checklist showing every place `osb_extract.py` still assumes dict-shaped records instead of typed records.

Group findings into:
- verse record access
- heading or article access
- marker trace structure
- output serialization shape

For each item include:
- exact file and line
- current assumption
- expected typed shape implied by tests and `types.py`
- whether it belongs to one coherent migration or a separate issue

## Task 3: Common Layer Contract Census

Read:
- [registry.py](/home/ark/orthodoxphronema/pipeline/common/registry.py)
- [frontmatter.py](/home/ark/orthodoxphronema/pipeline/common/frontmatter.py)
- [text.py](/home/ark/orthodoxphronema/pipeline/common/text.py)
- [patterns.py](/home/ark/orthodoxphronema/pipeline/common/patterns.py)
- [test_common.py](/home/ark/orthodoxphronema/tests/test_common.py)

For each failing test, classify the issue as one of:
- stale test expectation
- incomplete refactor
- accidental regression

For each disputed symbol include:
- symbol name
- current behavior
- expected behavior from tests or callers
- recommended direction: restore old contract or update tests and callers

## Output Requirements

- findings first
- exact file references
- exact failing tests
- grouped by task and failure class
- explicit distinction between observed fact and inference
- no implementation changes

## Required Verification

Run and cite:

1. `pytest tests/test_promote_gate.py -q`
2. `pytest tests/test_verse_split.py -q`
3. `pytest tests/test_common.py -q`

## Completion Requirements

Create one durable artifact in `memos/` or `reports/` and include:

- `Files read`
- `Verification run`
- `Artifacts refreshed`
- `Remaining known drift`
- `Next owner`

## Success Condition

Ark should be able to open your artifact and immediately implement:

1. the promote repair lane
2. the parser typed-record repair lane
3. the common-layer compatibility lane

without having to rediscover the current mismatch picture.
