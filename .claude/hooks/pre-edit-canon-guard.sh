#!/bin/bash
# Pre-edit hook: blocks direct edits to canon/ files
# Exit code 2 = BLOCK the operation in Claude Code

TOOL_INPUT="$CLAUDE_TOOL_INPUT"

# Check if the edit targets a canon file
if echo "$TOOL_INPUT" | grep -q "/canon/"; then
  echo "BLOCKED: Direct edit to canon/ detected."
  echo "Canon files are modified ONLY by the promote script."
  echo "Use: python3 pipeline/promote/promote_book.py staging/validated/{OT,NT}/BOOK.md"
  exit 2
fi

# Check if edit targets src.texts (add-only)
if echo "$TOOL_INPUT" | grep -q "/src.texts/"; then
  echo "WARNING: src.texts/ is add-only. Modifications to existing source texts are forbidden."
  exit 2
fi

exit 0
