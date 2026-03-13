# Memo Index — Orthodox Phronema Archive

> **Last updated:** 2026-03-13
> **Role:** Memo governance overlay
> **Covers:** `189` memo files (`32` active, `~155` archived)
> **See also:** `PROJECT_BOARD.md` for PM state and `memos/ezra_ops_board.md` for live dispatch

---

## Governing / Current

These memos define active policy, protocol, or default workflow. When they conflict with older memos, these win.

| Memo | Scope | Supersedes |
|---|---|---|
| `01_architecture_memo_v1.md` | Foundational architecture | — |
| `02_repository_folder_contract.md` | Directory structure contract | — |
| `03_validation_spec.md` | Core validation contract | — |
| `22_osb_immutability_and_secondary_verification_policy.md` | Source authority | — |
| `46_ark_review_photius_scope_ratification.md` | Photius scope | `41`–`45` chain (archived) |
| `47_ezra_delivery_ops_protocol.md` | Ezra ops loop | — |
| `52_photius_staged_fix_acceptance_criteria.md` | Photius evidence contract | — |
| `53_footnote_workflow_and_link_standards_ratification.md` | Footnote + link standards | — |
| `59_ezra_strategic_leadership_role_ratification.md` | Ezra leadership lane | `04_agent_delegation_map.md` in part |
| `60_completion_handshake_and_stale_state_clarity.md` | Completion and stale-state vocabulary | — |
| `62_ot_purity_pass_and_editorial_queue_integration.md` | Purity audit workflow | — |
| `69_v11v12_activation_and_phase2_3_bootstrap.md` | `V11` / `V12` live; Phase 3 prep | — |
| `70_workflow_consolidation.md` | Project board, memo index, research separation | — |

## Awaiting Human Ratification

| Memo | Ask |
|---|---|
| `51_historical_residual_ratification_packet_a.md` | `JDG`, `1SA`, `2SA` historical residuals |
| `91_ot_canon_lock_ratification_packet.md` | 17 V7-only books + `EST` disposition |

## Phase 3 Design

| Memo | Scope |
|---|---|
| `67_phase3_schema_design.md` | Phase 3 schema draft |
| `86_anchor_extraction_pipeline_research_synthesis.md` | R1 extraction pipeline (Cowork tasks) |
| `87_duckdb_citation_graph_research_synthesis.md` | DuckDB citation graph (Cowork tasks) |
| `88_phase3_ratified_spec.md` | **Governing** Phase 3 spec |
| `105_genesis_future_layer_seed.md` | Metadata substrate seed (prototype) |
| `106_reference_alias_authority_and_normalization_seed.md` | Alias authority (foundation) |

## Active Operational

| Memo | Workstream |
|---|---|
| `85_long_horizon_repo_cleanup_program.md` | Repo cleanup program (resolved as of 2026-03-13) |
| `98_contract_repair_and_state_refresh.md` | Shared contract repair truth |
| `68_nt_page_range_probe_request.md` | NT bootstrap prep (deferred) |
| `18_gen_readability_blocker_decision.md` | Readability policy |
| `20_greek_source_text_acquisition.md` | Future: Greek source layer |
| `21_greek_witness_layer_pilot.md` | Future: Greek witness pilot |

## Live Coordination

| File | Purpose |
|---|---|
| `ezra_ops_board.md` | Live tactical dispatch |
| `ezra-audit-log.md` | Ezra audit trail |
| `_template_work_memo.md` | Standard memo template |

---

## Archive

`155` memos moved to `memos/archive/` on 2026-03-13 as part of the Phase 2 → Phase 3 transition. All files retain their original memo numbers for cross-reference integrity. Git history is preserved via `git mv`.

| Directory | Contents | Count |
|---|---|---|
| `archive/phase2_cleanup_reports/` | Per-book `08_*_cleanup_report.md` files | 47 |
| `archive/phase2_promotion/` | OT and NT promotion execution memos | 33 |
| `archive/phase2_stabilization/` | Stabilization sprints, footnote alignment, recovery | 26 |
| `archive/planning_historical/` | Day plans, horizon plans, evidence packets, workflow evolution | 23 |
| `archive/phase1_extraction/` | Early extraction reports and probes | 14 |
| `archive/parser_validation/` | Parser fixes, edge-case checks, validation evolution | 9 |
| `archive/agent_negotiation/` | Photius role bootstrap/negotiation chain (41–45) | 5 |

### Numbering Reconciliation (2026-03-12)

| Canonical memo | Reconciled from | Location |
|---|---|---|
| `99_structural_drift_evidence_packet.md` | duplicate `90` | `archive/planning_historical/` |
| `100_dossier_schema_drift_packet.md` | duplicate `91` | `archive/planning_historical/` |
| `101_photius_companion_recovery_evidence.md` | duplicate `94` | `archive/planning_historical/` |

---

## Research / Advisory Inputs

`research/` is the canonical home for non-governing artifacts: external AI outputs, advisory audits, speculative designs, and PM/reference syntheses. See `research/README.md` for naming conventions.

## Memo Creation Protocol

### Use A Numbered Memo When
- protocol changes
- meaningful implementation milestones
- audits with findings
- ratification asks

### Do Not Write A Standalone Memo When
- it is only a same-day status ping
- it is only a queue update better suited to `memos/ezra_ops_board.md`
- it is only a PM-state change better suited to `PROJECT_BOARD.md`
- it is advisory research or synthesis better suited to `research/`

### Numbering Rule
- Numbered memos remain the durable team record.
- Do not reuse numeric prefixes for new memos.
- Advisory and research artifacts never receive numbered memo prefixes.
- Next available memo number: `120`

### Metadata For New Memos
```text
Workstream: [canon-hygiene | phase3-design | phase3-impl | workflow | future-layers]
Phase: [2 | 3]
Supersedes: [memo number or none]
Superseded by: [memo number or none]
```
