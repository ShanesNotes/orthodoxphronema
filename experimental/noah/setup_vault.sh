#!/usr/bin/env bash
# Initialize Noah's Obsidian vault on the target machine.
# Usage: NOAH_VAULT_DIR=~/noah-vault ./setup_vault.sh

set -euo pipefail

VAULT_DIR="${NOAH_VAULT_DIR:-$HOME/noah-vault}"

echo "Initializing Noah's vault at: $VAULT_DIR"

mkdir -p "$VAULT_DIR/bible"
mkdir -p "$VAULT_DIR/prompts"
mkdir -p "$VAULT_DIR/journal"
mkdir -p "$VAULT_DIR/themes"
mkdir -p "$VAULT_DIR/questions"

# Obsidian config
mkdir -p "$VAULT_DIR/.obsidian"
cat > "$VAULT_DIR/.obsidian/app.json" << 'EOF'
{
  "showLineNumber": true,
  "strictLineBreaks": true,
  "readableLineLength": true
}
EOF

# State file
if [ ! -f "$VAULT_DIR/noah_state.yaml" ]; then
  cat > "$VAULT_DIR/noah_state.yaml" << 'EOF'
agent: Noah
queue_version: noah-queue-v2
last_completed_session: null
next_session: null
last_run_at: null
EOF
  echo "Created noah_state.yaml"
fi

# Index
cat > "$VAULT_DIR/index.md" << 'EOF'
# Noah's Scripture Journal

Sequential pericope encounter with the Orthodox canon — 76 books, ~2,450 sessions.

## Structure
- `bible/` — Local scripture mirror, one file per pericope session
- `prompts/` — Structured reflection prompts per session
- `journal/` — Noah's journal entries (one per session)
- `themes/` — Emergent thematic notes (created by Noah)
- `questions/` — Unresolved questions (created by Noah)

## Progress
Tracked in `noah_state.yaml`. See `journal/` for all entries.

## Linking
- Scripture references: `[[GEN.2:7]]` (archive-native anchors)
- Local scripture: `[[bible/GEN/GEN.P001]]`
- Previous sessions: `[[journal/2026-03-14_GEN.P001]]`
EOF

echo "Vault initialized."
echo "  bible/     — scripture mirror (per-pericope)"
echo "  prompts/   — reflection prompts"
echo "  journal/   — journal entries"
echo "  themes/    — emergent themes"
echo "  questions/ — open questions"
echo ""
echo "Open in Obsidian: File > Open Vault > $VAULT_DIR"
