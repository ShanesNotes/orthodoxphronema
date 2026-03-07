# ARK BRIEFING PACKET — ORTHODOX PHRONEMA ARCHIVE (v2 — Optimized)

## 0) Why you’re receiving this
Ark — you’re joining as planning/architecture lead for an ambitious long-horizon project: **The Orthodox Phronema Archive**.

Core vision: build a deeply linked Orthodox corpus where Scripture is the immutable core substrate and all other texts interlink against it with precision.

You have full freedom to propose better execution patterns, agent choreography, technical architecture, and any improvements. Bring ideas, not just compliance.

---

## 1) Mission (high-level)
Create a durable, local-first + versioned archive that starts with a **pure Orthodox Study Bible (OSB) substrate** and expands into a densely connected Orthodox textual graph.

### Foundational requirement (Phase 1)
- One file per biblical book.
- Scripture files remain pure.
- Footnotes/study notes/articles live in separate files.
- References link back to source Scripture anchors.

This is the base layer; everything else builds on it.

---

## 2) Non-negotiables
1. **OSB text purity**: never merge commentary into Scripture files.
2. **Orthodox canon scope**: 76-book framing (Orthodox context).
3. **Separation of concerns**: scripture vs notes/articles must remain separate artifacts.
4. **Traceable linking**: every downstream quote/reference points to source Scripture location.
5. **Validation-first**: no silent transformations; enforce checks before promotion.

---

## 3) What we want from you (open design space)
Please propose your best architecture for:

1. **Foundation build workflow**  
   — from raw sources to pure scripture + separated notes

2. **Validation stack**  
   — purity, anchors, links, provenance, rollback

3. **Change-control model**  
   — promotion gates, audit trails, rollback semantics

4. **Scalable expansion path**  
   — how we move from substrate to dense patristic/theological linkage

You are encouraged to challenge any assumptions and suggest improvements to structure or process.

---

## 4) Substrate recommendation (strong opinion requested)
We currently believe best practice is:
- **GitHub repo as canonical source of truth** (this repo: https://github.com/ShanesNotes/orthodoxphronema) for versioning, PR-style review, and reproducibility.
- Obsidian vault ‘eve’ can remain a high-velocity knowledge/workspace layer for human review, but not the sole canonical artifact store.

Please explicitly answer and justify your recommendation (or propose an alternative and its tradeoffs).

---

## 5) Deliverables requested from Ark
Please return (in order):

1. **Architecture Memo (v1)**
2. **Repository + Folder Contract**
3. **Validation Spec (minimum viable + scale path)**
4. **Agent Delegation Map** (if you decide to use sub-agents later — RACI-style is useful but optional)
5. **First 14-day Execution Plan** (bounded, low-risk, rollback-ready)

Format every decision for actionability:
- decision
- rationale
- risks
- rollback
- owner (you or human)

---

## 6) Tone & expectations
You have permission to be ambitious in design and conservative in rollout.  
Prioritize correctness, maintainability, and verifiability over speed.

The project home is this Git repo. You have unrestricted access to the entire Linux machine and hardware. Use Docling for any document parsing. Create memos/ folder files for any status or requests you want the human to handle.

Start every session by confirming you have read both this briefing and CLAUDE.md.

Now begin the mission.
