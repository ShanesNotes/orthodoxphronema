# MEMO: Noah Ingestion Handoff

> Sandbox draft only. Superseded for official repo behavior by Memo `125`.
> For the active experimental runtime path, use
> `experimental/noah/MINIMAL_RUNTIME_RUNBOOK.md`.

**Date:** 2026-03-13
**Status:** PROPOSED
**Author:** Photius (Gemini CLI)

## Objective
To define the pathing and data structures for "Noah" (OpenClaw agent) to ingest the Orthodox Phronema Archive in canonical order.

## Current Direction

This handoff is historical. The active experiment now differs from this original draft in
three important ways:

1. Pericope sessions, not whole-book or chapter-file traversal, are the default unit.
2. The runtime begins with `git pull` against a local repo mirror before selecting the
   next session.
3. The downstream vault grows a local `bible/` mirror of the exact session source so
   the scripture seed accumulates inside Noah's own Obsidian workspace.

For the current practical path, use:

- `metadata/agent_ingestion/noah/session_queue.jsonl`
- `experimental/noah/MINIMAL_RUNTIME_RUNBOOK.md`
- `experimental/noah/LEGACY_PROTOTYPES.md`

## Validation Results
* **Registry Version:** 1.4.0
* **Promoted Books:** 76 (Verified in `reports/book_status_dashboard.json`)
* **Checksum Verification:** Genesis (01_GEN.md) checksum matches promoted dossier.

## Next Steps
1. Use the official Noah queue as the only traversal source.
2. Treat enrichment layers as future experimental variants, not baseline input.
3. Keep all runtime state and scripture mirrors local to the downstream environment.

---
**Files changed:** `experimental/noah_ingestion_handoff.md` (Created)
**Verification run:** Checked `canon/` and `metadata/` structure.
**Artifacts refreshed:** None.
**Remaining known drift:** Original chapter/enrichment framing is now legacy only.
**Next owner:** Human / Ark (runtime implementation off the generic runbook)
