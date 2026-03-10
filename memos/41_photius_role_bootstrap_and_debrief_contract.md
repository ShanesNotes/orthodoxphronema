# Memo 41 — Photius Role Bootstrap And Debrief Contract

**Author:** `ezra`
**Type:** `workflow`
**Status:** `draft`
**Scope:** `gemini/photius bootstrap`

## Context
- Gemini CLI was installed into the repo and began operating without a repo-specific Gemini context file.
- The repo already contains Ark-specific directives in `CLAUDE.md`, creating a real risk that Gemini could infer Ark's identity or authority.
- Human wants to observe Gemini's parsing strengths without silently creating a second default writer.

## Objective
- Introduce an explicit Gemini identity and scope boundary at the repo root.
- Capture a durable end-of-run debrief contract so parsing lessons are preserved with evidence.
- Avoid changing the formal ownership contract in `AGENTS.md` until Human decides whether to ratify a lasting Photius role.

## Files / Artifacts
- `GEMINI.md`
- `memos/41_photius_role_bootstrap_and_debrief_contract.md`

## Findings Or Changes
- Added a repo-root `GEMINI.md` because Gemini CLI's default project context filename is `GEMINI.md`, not `AGENTS.md` or `CLAUDE.md`.
- Declared `Photius` as a bounded parsing specialist rather than a second Ark.
- Explicitly denied default write authority over `canon/`, `pipeline/`, `schemas/`, promotion logic, and protocol files.
- Added an end-of-run debrief contract that requires:
  - exact files read and changed
  - admission of any Ark-role confusion
  - parsing lessons grouped by failure class
  - a self-introduction memo drafted from the repo memo template
- Kept `AGENTS.md` unchanged in this step so the formal team contract is not silently rewritten.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Add `GEMINI.md` at repo root | Gemini CLI loads `GEMINI.md` by default for project context, so this is the smallest effective control point | Instructions may be too restrictive or too loose on first pass | Revise `GEMINI.md` or remove it if Human chooses a different role model |
| Define Photius as parsing specialist, not default committer | Preserves the repo's single-writer canon rule while still making Gemini useful for text-heavy work | May slow down direct execution if Human later wants broader Gemini writes | Ratify broader scope later in `AGENTS.md` or a follow-up memo |
| Require evidence-backed debrief before ending a substantial run | Preserves lessons learned and exposes role confusion early | Debriefs may be incomplete if not enforced by Human | Re-prompt Gemini with the debrief checklist or tighten `GEMINI.md` |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Repo had no Gemini-specific context file before this change | `pass` | `rg -n "GEMINI|Photius|photius|gemini" -S .` returned no matches in repo files before `GEMINI.md` was added |
| Gemini CLI default context filename is `GEMINI.md` | `pass` | `/usr/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/docs/cli/gemini-md.md` |
| Bootstrap change is coordination-only | `pass` | This step adds `GEMINI.md` and this memo only; no canon, parser, validator, or staging artifacts were edited by Ezra |

## Open Questions
- Should Photius remain read-mostly by default, or receive explicit write access to bounded `staging/` and sidecar paths?
- Should a future ratified team protocol add `photius` to `AGENTS.md`, or should the role remain local to `GEMINI.md`?

## Requested Next Action
- Human: let Photius complete a bounded run, then request the end-of-run debrief defined in `GEMINI.md`.
- Photius: draft a self-introduction memo using `memos/_template_work_memo.md` once the run is complete.
- Ark and Ezra: review Photius's debrief and decide whether the role should be formalized in `AGENTS.md`.

## Handoff
**To:** `human`  
**Ask:** `Run Photius under the new GEMINI.md context and require the debrief before trusting any lasting workflow conclusions.`

## Notes
- This memo intentionally does not modify the formal ownership table in `AGENTS.md`.
- The immediate goal is identity stability and evidence capture, not policy expansion.
