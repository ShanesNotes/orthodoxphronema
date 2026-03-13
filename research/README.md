# research/ — Naming Convention

## File Naming Pattern

```
[AGENT]_[TOPIC_SLUG]_[YYYYMMDD].md
```

- **Agent prefix:** `GEMINI`, `GROK`, `ARK`, `CLAUDE`, `HUMAN`
- **Topic slug:** 2–4 words, `ALL_CAPS_UNDERSCORED`, describing the subject not the task
- **Date:** Always suffixed, never prefixed. Format `YYYYMMDD`.

## Special Prefixes

- `SUPERSEDED_` — Document has been replaced by a numbered memo. Retained for audit trail.
- `_RAW_` suffix in topic slug — Unprocessed agent output (the synthesis memo is the actionable version).

## Reference Documents

`PROJECT-KNOWLEDGE.md` and `PROJECT-KNOWLEDGE-STRATEGIC.md` are standing reference docs, not time-stamped research artifacts. They do not follow the agent-prefix convention.

## Relationship to Memos

Research files are raw or advisory input. They do not have numbered memo prefixes. Actionable synthesis goes into `memos/` as a numbered memo. The memo references the research file; Cowork executes from the memo, not the raw research.

## Directory Structure

Flat until a clear clustering pattern emerges (8–10 files per cluster minimum). Do not create subdirectories preemptively.
