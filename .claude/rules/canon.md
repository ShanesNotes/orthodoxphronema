---
paths:
  - canon/**
---

## CRITICAL — Canon Protection

Canon files are the immutable promoted scripture substrate. They represent the final, audited, ratified output of the entire pipeline.

BEFORE any modification to a canon file:
1. Confirm this is a promotion operation executed by the promote script
2. Confirm Ezra audit is complete (check `memos/ezra-audit-log.md`) or explicitly waived
3. Confirm Human ratification of any ambiguous cases
4. Confirm the source is the SAME staged file that was validated and audited

Rules:
- Manual edits to canon files are FORBIDDEN — use the promote script only
- One-verse-per-line format is mandatory
- Study article text must NEVER appear in canon scripture files
- Footnote markers are stripped; indexed separately in BOOK_footnote_markers.json
- Only Ark + Human may execute promotion
