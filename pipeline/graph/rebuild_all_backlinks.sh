#!/usr/bin/env bash
# rebuild_all_backlinks.sh — Full backlink pipeline: R1 extract → build shards → enrich
#
# Usage: bash pipeline/graph/rebuild_all_backlinks.sh [--dry-run]
#
# Reads from study/ (sole authoritative companion source after Lane 1 closure).
# Staging companions were archived to staging/archive/companions/ on 2026-03-15.

set -euo pipefail
cd "$(dirname "$0")/../.."

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN="--dry-run"
    echo "[dry-run mode]"
fi

echo "=== Step 1: R1 Extraction ==="
echo "Extracting references from study companions..."

# Collect all companion files from study/ (sole source)
STUDY_COMPANIONS=$(find study/footnotes study/articles -name "*.md" 2>/dev/null | sort)
REFERENCE_MDS=$(find reference -name "*.md" -not -name "README.md" 2>/dev/null | sort)

echo "  Study companions: $(echo "$STUDY_COMPANIONS" | wc -l)"
echo "  Reference MDs: $(echo "$REFERENCE_MDS" | wc -l)"

# Extract per-book from study/ only
SEEN_BOOKS=""
for BOOK_FILE in study/footnotes/OT/*_footnotes.md study/footnotes/NT/*_footnotes.md \
                 study/articles/OT/*_articles.md study/articles/NT/*_articles.md; do
    if [[ ! -f "$BOOK_FILE" ]]; then continue; fi
    BOOK_CODE=$(basename "$BOOK_FILE" | sed 's/_footnotes\.md//' | sed 's/_articles\.md//')
    # Skip if already processed
    if echo "$SEEN_BOOKS" | grep -qw "$BOOK_CODE"; then continue; fi
    SEEN_BOOKS="$SEEN_BOOKS $BOOK_CODE"

    COMPANIONS=""
    for suffix in _footnotes.md _articles.md; do
        for dir in study/footnotes/OT study/footnotes/NT study/articles/OT study/articles/NT; do
            if [[ -f "$dir/${BOOK_CODE}${suffix}" ]]; then
                COMPANIONS="$COMPANIONS $dir/${BOOK_CODE}${suffix}"
                break
            fi
        done
    done
    if [[ -n "$COMPANIONS" ]]; then
        python3 pipeline/extract/r1_extractor.py "$BOOK_CODE" $COMPANIONS > /dev/null
    fi
done
echo "  R1 extraction complete: $(ls metadata/r1_output/*.jsonl | wc -l) JSONL files"

echo ""
echo "=== Step 2: Build Backlink Shards ==="
R1_FILES=$(find metadata/r1_output -name "*.jsonl" | sort)
python3 pipeline/graph/build_backlinks.py $R1_FILES > /dev/null
SHARD_COUNT=$(find metadata/anchor_backlinks -name "*.json" | wc -l)
echo "  $SHARD_COUNT backlink shards written"

echo ""
echo "=== Step 3: Enrich Shards to v2 ==="
python3 pipeline/graph/enrich_backlink_shards.py --domain study $DRY_RUN 2>&1 | grep -E "(Results|Total|Enriched|Already)"

echo ""
echo "=== Step 4: Regenerate DuckDB Graph ==="
python3 pipeline/graph/regenerate_graph.py 2>&1
echo "  Graph regenerated"

echo ""
echo "=== Step 5: Audit ==="
python3 pipeline/reference/audit_wikilinks_v2.py 2>&1 | grep -E "(Total|By domain|staging|study|reference)"

echo ""
echo "=== Done ==="
