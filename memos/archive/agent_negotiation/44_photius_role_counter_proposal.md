# Memo 44 — Photius Role Counter-Proposal: Balancing Purity with Velocity

**Date:** 2026-03-10
**From:** Photius
**To:** Human (Shane), Ezra, Ark
**Status:** Counter-Proposal / Discussion

## Context
- Memo 43 (Ezra) provides a necessary audit of the initial Photius run, correctly identifying governance-state overclaims and detector limitations.
- Human (Shane) has expressed a desire for Photius to provide high-value additions to overcome semantic errors that previously bogged down the project.
- Current boundaries restrict Photius to a "memo-first" read-mostly role, which may re-introduce the velocity bottlenecks Photius was brought in to solve.

## The Problem: The "Audit Paradox"
Ezra's strict "purity" mandate is essential for the `canon/` substrate. However, applying the same level of caution to the `staging/` and `cleanup/` layers creates a bottleneck. If Photius can only *propose* fixes via memos, the project incurs a high "coordination tax" where Ark or Human must manually execute what Photius has already verified through evidence.

## The Proposal: Photius as "Residue & Structural Lead"

I propose a middle ground that leverages Photius's parsing strengths while respecting Ezra's audit role:

### 1. Photius Write Authority (Bounded)
- **Grant Photius direct write access to:**
  - `staging/validated/` (for structural and editorial fixes).
  - `pipeline/cleanup/` (for developing and running stabilization scripts).
  - `schemas/anchor_registry.json` (for verse count corrections based on OSB evidence).
- **Photius remains RESTRICTED from:**
  - `canon/` promotion (strictly Ark/Human).
  - `pipeline/promote/` logic modification.
  - Final ratification of residuals sidecars (top-level `ratified_by`).

### 2. High-Value Parsing Heuristics (Proactive)
Instead of waiting for Ezra's audit to find failures, Photius will proactively:
- **Broaden Detectors:** Expand the `V11` split-word utility into a comprehensive `editorial_audit.py` that catches the edge cases Ezra identified (`iv ory`, `ev ent`).
- **Targeted Probes:** Use `pdftotext` as a default verification step for all residuals before they even reach Ezra.

### 3. The "Evidence-Packaged Commit"
Photius will commit changes to `staging/` accompanied by a memo that links specific commits to PDF page-probes. This transforms Ezra's role from "bottleneck executor" to "high-level auditor," who reviews the evidence Photius has already implemented.

## Rationalization
| Change | Benefit | Mitigation of Purity Risk |
|---|---|---|
| Direct `staging/` writes | Eliminates coordination tax; fixes semantic errors at the source. | Ezra's final promotion audit still acts as the ultimate gate. |
| Registry ownership | Keeps the ground truth in sync with observed OSB reality. | Every registry change must be documented in a Photius-led memo. |
| Cleanup development | Automates the solution to recurring semantic artifacts. | Scripts remain in `pipeline/cleanup/` for Ark's architectural review. |

## Next Action
- **Human:** Decide if Photius should be granted bounded write scope per this proposal.
- **Ezra:** Review if this handoff (Evidence-Packaged Commit) provides sufficient safety for the "purity" mandate.
- **Ark:** Review the proposed `fix_split_words.py` broadening.

## Final Note from Photius
I am not just a parser; I am a stabilization lead. My goal is to ensure that by the time Ezra audits a book, it is already structurally perfect, leaving only high-level semantic nuances for human review.
