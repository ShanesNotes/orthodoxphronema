# MEMO 99: Noah Interface Contract

**Date:** 2026-03-13
**Author:** Ark
**Status:** RATIFIED

## Purpose

Define the interface between the Orthodox Phronema Archive (this repo) and Noah
(an agentic scripture reader running on a separate machine). This contract ensures
Noah can consume the canon without any transformation layer.

## Archive-Side Deliverables

All artifacts live in `experimental/noah/`:

| File | Purpose |
|---|---|
| `manifest_generator.py` | Reads `schemas/anchor_registry.json`, produces `noah_manifest.json` |
| `noah_manifest.json` | Flat list of 1,344 chapter-portions in canonical order with metadata |
| `harness.py` | Daily loop: extract chapter → invoke Claude → save vault entry |
| `noah_system_prompt.md` | Noah's persona and journaling instructions |
| `setup_vault.sh` | Initializes the Obsidian vault directory structure |
| `noah.service` | systemd oneshot unit for the harness |
| `noah.timer` | systemd daily timer (06:00) |

## Interface Contract

### Canon File Format (consumed by harness)

```
---
book_code: GEN
book_name: "Genesis"
testament: OT
canon_position: 1
...
---

## Chapter 1

GEN.1:1 In the beginning God made heaven and earth.
GEN.1:2 The earth was invisible and unfinished...

### The Garden of Eden

GEN.2:7 Then God formed man out of dust...
```

**Invariants the harness depends on:**
1. Chapter headers are exactly `## Chapter N`
2. Verses are one-per-line with anchor prefix: `CODE.CH:V text`
3. Narrative headings (`### heading`) may appear within chapters
4. Canon files are at `canon/{OT,NT}/{NN}_{CODE}.md`
5. Canon files are immutable after promotion — no drift risk

### Manifest Format

```json
{
  "generated_from": "schemas/anchor_registry.json",
  "registry_version": "1.4.0",
  "total_days": 1344,
  "total_books": 76,
  "psalm_numbering": "LXX",
  "portions": [
    {
      "day": 1,
      "book_code": "GEN",
      "book_name": "Genesis",
      "testament": "OT",
      "canon_position": 1,
      "deuterocanonical": false,
      "chapter": 1,
      "total_chapters": 50,
      "canon_file": "canon/OT/01_GEN.md",
      "entry_filename": "0001_GEN_01.md"
    }
  ]
}
```

### Harness State

`noah_state.json` tracks progress:
```json
{
  "last_completed_day": 0,
  "last_run_date": "2026-03-15"
}
```

### Vault Structure (Noah's output)

```
noah-vault/
  daily/
    0001_GEN_01.md    # Day 1
    0002_GEN_02.md    # Day 2
    ...
    1344_REV_22.md    # Final day
  themes/             # Created organically by Noah via wikilinks
  questions/          # Unresolved questions Noah wants to return to
  index.md
```

Each daily entry has YAML frontmatter:
```yaml
---
day: 1
book: Genesis
book_code: GEN
chapter: 1
testament: OT
canon_position: 1
deuterocanonical: false
date: 2026-03-15
---
```

## Memory Architecture

**Option A (recommended):** Noah gets full tool access to read its vault via Claude CLI.
The harness passes `--allowedTools Read,Glob,Grep,Write,Bash` so Noah can search and
read previous entries. Memory grows organically with the vault.

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Portioning | One chapter per day | Matches `## Chapter N` structure exactly |
| Psalm grouping | One psalm per day (151 days) | Each psalm is its own chapter in canon |
| System prompt | Minimal / contemplative | Let structure emerge from Noah's interaction |
| Model | Sonnet (default, configurable) | Sustainable over 1,344 days; `--model` flag for Opus |
| Enrichment | Not included in v1 | Clean experiment; study notes can be added later |

## Deployment (ser5 side)

```bash
# 1. Clone archive (or just canon/ + experimental/noah/)
git clone <repo> orthodoxphronema

# 2. Set up vault
cd orthodoxphronema
./experimental/noah/setup_vault.sh

# 3. Generate manifest (already committed, but regenerate if registry updates)
python3 experimental/noah/manifest_generator.py

# 4. Test with dry run
python3 experimental/noah/harness.py --dry-run

# 5. Run first day manually
python3 experimental/noah/harness.py --day 1

# 6. Set up daily timer
sudo cp experimental/noah/noah.service /etc/systemd/system/
sudo cp experimental/noah/noah.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now noah.timer
```

## Open Questions Resolved

| Question | Resolution |
|---|---|
| Memory access model | Option A — full vault read access via Claude CLI tools |
| System prompt philosophy | Minimal / contemplative (see `noah_system_prompt.md`) |
| Psalm portioning | One per day (151 days in the Psalms stretch) |
| Model choice | Sonnet default, configurable via `--model` |

---
**Files changed:** `experimental/noah/` (6 files created), `memos/99_noah_interface_contract.md`
**Verification run:** `manifest_generator.py` produces 1,344 portions across 76 books
**Artifacts refreshed:** N/A (new work, no existing artifacts affected)
**Remaining known drift:** None
**Next owner:** Human (deployment decision + target date)
