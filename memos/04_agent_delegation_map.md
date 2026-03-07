# Agent Delegation Map
**Author:** Ark | **Date:** 2026-03-06 | **Status:** Proposed

---

## Phase 1 (Current) — Lean Two-Actor Model

At this stage, full sub-agent delegation is premature. The corpus does not yet exist in structured form, and the most critical work is establishing validated patterns on a small number of books before scaling. Adding agent complexity before patterns are stable risks amplifying errors across the corpus.

### Actor: Ark (Planning + Execution Lead)
**Responsible for:**
- Architecture decisions and amendments to this contract
- Writing and maintaining all pipeline scripts
- Running Docling parse jobs
- Running all validation checks
- Writing promotion commits
- Producing memos for human action items

**Consulted on:**
- Any change to the anchor scheme, folder contract, or validation spec

**Not responsible for:**
- External source acquisition (human acquires)
- GitHub account management (human owns)
- Obsidian vault curation (human owns)

---

### Actor: Human
**Responsible for:**
- Providing and authorizing source documents in `src.texts/`
- Ratifying the book code registry and anchor scheme before production use
- Reviewing validation reports and approving promotion batches (PR approval)
- Managing the GitHub remote (push access, branch protection rules)
- Handling any external communications or acquisitions

**Consulted on:**
- Theological questions about text boundaries (e.g., is a given paragraph commentary or intro?)
- Canon scope decisions (any additions beyond the 76-book baseline)
- Prioritization of which books to process first

---

## Phase 2 — Specialized Sub-Agents (Introduced when corpus reaches ~20 books)

Once parsing patterns are stable and the validation suite is mature, specialized sub-agents can be delegated narrow, bounded tasks. Each sub-agent operates only on staging directories and produces output for Ark's review before any promotion.

| Agent | Role | Scope | Accountability |
|-------|------|-------|----------------|
| ParseAgent | Run Docling extractions; output to `staging/raw/` | `src.texts/` → `staging/raw/` | Ark reviews all output |
| ValidateAgent | Run V1–V4 checks; produce reports | `staging/raw/` → `staging/validated/` | Ark reviews reports; promotion is Ark-only |
| LinkAgent | Build cross-reference index from notes back to canon anchors | `notes/` + `canon/` | Ark reviews; no writes to canon |
| DiffAgent | Generate human-readable diff summaries at promotion | `staging/validated/` vs `canon/` | Output only; no writes |

**Decision:** Sub-agents are introduced incrementally. No sub-agent has write access to `canon/`. Ark is the only actor that runs the promote script.

**Rationale:** The canon is the irreplaceable artifact. Human and Ark review are the only gatekeepers for promotion. Sub-agents accelerate throughput on bounded, reversible tasks.

**Risks:** Sub-agent errors in staging are recoverable. The risk is sub-agent scope creep — each agent's file access must be explicitly bounded.

**Rollback:** Any sub-agent can be suspended without affecting canon. Staging directories are reset. Ark re-runs the affected step manually.

**Owner:** Ark (agent design and oversight)

---

## Phase 3 — Graph + Linking Agents (Future)

When patristic and liturgical texts are being added:

| Agent | Role |
|-------|------|
| PatristicLinkAgent | Match patristic quotes to canon anchors; flag ambiguous matches for human review |
| LiturgicalMapAgent | Map liturgical pericopes to their canon anchor ranges |
| IndexAgent | Maintain the full anchor registry and produce broken-link reports |

These agents are defined here as placeholders. Full specs will be written when Phase 2 is complete.

---

## RACI Summary

| Decision/Task | Ark | Human | ParseAgent | ValidateAgent |
|---------------|-----|-------|------------|---------------|
| Architecture changes | R/A | C | - | - |
| Source acquisition | I | R/A | - | - |
| Docling parse run | R | I | (Phase 2) | - |
| Validation run | R | I | - | (Phase 2) |
| Promotion approval | R | A | - | - |
| Git push to remote | I | R/A | - | - |
| Book code ratification | C | R/A | - | - |
| Obsidian vault | I | R/A | - | - |

R = Responsible | A = Accountable | C = Consulted | I = Informed
