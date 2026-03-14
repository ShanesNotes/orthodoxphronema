#!/bin/bash
# Post-edit hook: logs edits to staging/validated/ for awareness
# Does not block — informational only

TOOL_INPUT="$CLAUDE_TOOL_INPUT"

if echo "$TOOL_INPUT" | grep -q "/staging/validated/"; then
  BOOK=$(echo "$TOOL_INPUT" | grep -oP '[A-Z0-9]+\.md' | head -1 | sed 's/\.md//')
  if [ -n "$BOOK" ]; then
    echo "NOTE: Staged book $BOOK was modified. Remember to:"
    echo "  1. Run validation: python3 pipeline/validate/run_validators.py on the file"
    echo "  2. Evidence-package the change (source page, affected anchors, before/after)"
    echo "  3. Update or create a memo documenting the change"
  fi
fi

exit 0
