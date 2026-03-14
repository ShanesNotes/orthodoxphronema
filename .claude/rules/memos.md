---
paths:
  - memos/*.md
---

## Memo Protocol — Durable Evidence Artifacts

Memos preserve rationale, evidence, and reduce information loss between agents.

When creating or updating a memo:
1. Use template: `memos/_template_work_memo.md`
2. Include ALL required completion surfaces:
   - Files changed
   - Verification run
   - Artifacts refreshed (or explicitly declared stale with named surface)
   - Remaining known drift
   - Next owner

When a memo is required:
- Parser refactor
- Cleanup-rule expansion
- Validation-rule change
- Promotion-gate change
- Source-authority / workflow policy change
- Substantial staged recovery or dashboard/dossier affecting work

Stale-state vocabulary (use precisely):
- `stale dossier` = staged scripture changed but dossier not regenerated
- `stale dashboard` = generated dashboard not refreshed after state change
- `stale memo` = memo claims no longer match current repo artifacts

Ownership:
- Ark: implementation memos, architecture decisions
- Photius: recovery evidence, cleanup reports
- Ezra: audit logs, ops board, delivery ops
- Cowork: INDEX.md only (memo governance overlay)
