# Noah Autoresearch `program.md` Template

Use this as the human-authored goal file for the downstream Noah autoresearch sandbox.

```md
# Noah Autoresearch Program

## Goal
Improve Noah's local contemplative prompt/scoring profile for the Orthodox Phronema
Archive while preserving archive invariants and the slow one-session-per-day live
reading rhythm.

## Active Track
Track A

## Objective
Optimize `grounded_reflection_score` on the frozen evaluation manifest.

## Hard Rules
- The archive is read-only.
- Noah's live runtime begins with `git pull`.
- Queue order comes only from `metadata/agent_ingestion/noah/session_queue.jsonl`.
- The local `bible/` mirror is derivative and must not be edited as scripture.
- The agent may edit only `candidate_profile.yaml`.
- The agent may not edit runtime code, queue generation, packet export, or archive files.

## Hard Gates
- Reject malformed or invalid archive anchors.
- Reject outputs missing required journal sections.
- Reject unsupported external sourcing.
- Reject outputs that fail the grounding threshold.

## Optimization Notes
- Favor faithful, text-grounded reflection.
- Favor usable archive-native anchors.
- Favor clarity and non-repetitive journaling.
- Do not optimize graph density in Track A.

## Promotion Rule
Promote a candidate only if it beats the current active profile on the same evaluation
manifest and passes all hard gates.
```
