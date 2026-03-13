# Reference Alias Authority And Normalization Seed — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `future-layer reference normalization / alias authority`
**Workstream:** `phase3-design`  
**Phase:** `3`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- The Genesis future-layer seed proved that the live companion corpus does not yet speak primarily in archive-native `[[BOOK.CH:V]]` links.
- The OSB footnotes instead contain many prose abbreviations such as `Jn 20:22`, `Mk 2:27`, and `Eph 5:32`.
- Hard-coding those aliases inside the extractor would not scale once the project expands into patristic references already present in the OSB and later patristic-source layers.

## Objective
- Move reference alias knowledge into a versioned, commit-controlled schema.
- Normalize biblical references through that schema today.
- Reserve a clean namespace for future patristic entity aliases without pretending that patristic passage resolution is already solved.

## Files / Artifacts
- `schemas/reference_aliases.yaml`
- `pipeline/reference/reference_aliases.py`
- `pipeline/extract/r1_extractor.py`
- `tests/test_reference_aliases.py`

## Findings Or Changes
- Added `schemas/reference_aliases.yaml` as the authoritative alias registry.
  - Biblical aliases normalize to canonical archive book codes.
  - Patristic aliases normalize only to canonical entity identities plus a context hint.
- Added `pipeline/reference/reference_aliases.py`.
  - Loads the YAML authority.
  - Builds canonical biblical and patristic alias maps.
  - Normalizes alias tokens without mixing biblical-anchor resolution and patristic-entity resolution.
- Replaced the hard-coded biblical alias map inside `pipeline/extract/r1_extractor.py`.
  - The Genesis R1 seed now resolves through the versioned schema instead of in-file constants.
  - The extractor remains strict about yielding only canonical archive anchor IDs.
- Added direct test coverage for:
  - OSB-style biblical aliases
  - Greek-form aliases
  - numbered-book aliases
  - patristic entity normalization boundaries

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep alias authority in `schemas/` | Alias drift is part of the controlled archival contract, not incidental code trivia | Schema can grow quickly over time | Keep file versioned and reviewed like other controlled schemas |
| Separate biblical and patristic namespaces | Biblical refs usually resolve to anchors; patristic refs usually do not | Early callers may want one unified resolver | Layer a unified resolver later without collapsing the namespaces |
| Normalize patristics to entities, not passages | `Ath` and `Chrysostom` are not sufficient to identify exact work/passage targets | Some future callers may over-assume resolvability | Require a later work/passage resolver stage before wikilink rewrite |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Alias schema + resolver tests | `pass` | `pytest tests/test_reference_aliases.py tests/test_future_seed.py -q` |
| Genesis seed rebuild through alias schema | `pass` | `python3 pipeline/metadata/build_future_seed.py --companion-base staging/validated` |
| Module syntax | `pass` | `python3 -m py_compile pipeline/reference/reference_aliases.py pipeline/extract/r1_extractor.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | alias schema, resolver module, extractor integration, tests, Memo `106` |
| `Verification run` | `done` | targeted alias tests, Genesis seed rebuild, py_compile |
| `Artifacts refreshed` | `done` | Genesis seed artifacts rebuilt through the schema-backed alias path |
| `Remaining known drift` | `present` | patristic passage/work resolution and wikilink rewrite remain future layers; current implementation normalizes entities only |
| `Next owner` | `ezra` | Next clean design lane is the structured reference resolver and safe wikilink rewrite contract |
