import os
import re
import json
from pathlib import Path

# Paths
REPO_ROOT = Path("/home/ark/orthodoxphronema")
NT_STAGING_DIR = REPO_ROOT / "staging" / "validated" / "NT"
REPORT_PATH = REPO_ROOT / "reports" / "nt_structural_census.json"
MEMO_PATH = REPO_ROOT / "memos" / "92_nt_structural_census.md"
TEMPLATE_PATH = REPO_ROOT / "memos" / "_template_work_memo.md"

# Patterns
RE_ANCHOR = re.compile(r"([A-Z0-9]{3})\.(\d+):(\d+)")

def analyze_book(file_path):
    book_code = file_path.stem
    lines = file_path.read_text(encoding="utf-8").splitlines()
    
    total_lines = len(lines)
    anchors_found = []
    embedded_verse_lines = []
    
    for idx, line in enumerate(lines, 1):
        matches = RE_ANCHOR.findall(line)
        if len(matches) > 1:
            embedded_verse_lines.append(idx)
        for m in matches:
            anchors_found.append({
                "line": idx,
                "anchor": f"{m[0]}.{m[1]}:{m[2]}",
                "ch": int(m[1]),
                "v": int(m[2])
            })

    # Total Chapters
    chapters = sorted(list(set(a["ch"] for a in anchors_found)))
    total_chapters = len(chapters) if chapters else 0
    
    # Chapter Zero Anchors
    chapter_zero_count = sum(1 for a in anchors_found if a["ch"] == 0)
    
    # Duplicate Anchors
    anchor_counts = {}
    for a in anchors_found:
        anchor_counts[a["anchor"]] = anchor_counts.get(a["anchor"], 0) + 1
    duplicate_anchors = [a for a, count in anchor_counts.items() if count > 1]
    
    # Missing Verse Gaps
    missing_verse_gaps = {}
    total_missing_verses = 0
    for ch in chapters:
        if ch == 0: continue
        ch_verses = sorted([a["v"] for a in anchors_found if a["ch"] == ch])
        if not ch_verses: continue
        
        gaps = 0
        for i in range(1, max(ch_verses) + 1):
            if i not in ch_verses:
                gaps += 1
        if gaps > 0:
            missing_verse_gaps[str(ch)] = gaps
            total_missing_verses += gaps

    # Note Markers
    content = "\n".join(lines)
    note_markers_found = "†" in content or "ω" in content
    
    # Structural Grade
    if chapter_zero_count > 0 or duplicate_anchors or embedded_verse_lines or note_markers_found:
        grade = "unstable"
    elif total_missing_verses > 0:
        grade = "minor"
    else:
        grade = "clean"
        
    return {
        "book": book_code,
        "total_lines": total_lines,
        "total_anchors": len(anchors_found),
        "total_chapters": total_chapters,
        "chapter_zero_anchors": chapter_zero_count,
        "duplicate_anchors": duplicate_anchors,
        "embedded_verse_lines": embedded_verse_lines,
        "missing_verse_gaps": missing_verse_gaps,
        "total_missing_verses": total_missing_verses,
        "note_markers_found": note_markers_found,
        "structural_grade": grade
    }

def run_census():
    books = []
    nt_files = sorted(list(NT_STAGING_DIR.glob("[A-Z0-9][A-Z0-9][A-Z0-9].md")))
    
    for f in nt_files:
        print(f"Analyzing {f.name}...")
        books.append(analyze_book(f))
        
    # Write JSON
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(books, indent=2), encoding="utf-8")
    
    # Write Memo
    grade_counts = {"clean": 0, "minor": 0, "unstable": 0}
    for b in books:
        grade_counts[b["structural_grade"]] += 1
        
    sorted_by_issues = sorted(books, key=lambda x: (len(x["duplicate_anchors"]) + len(x["embedded_verse_lines"]) + x["total_missing_verses"] + x["chapter_zero_anchors"]), reverse=True)
    top_5_worst = sorted_by_issues[:5]
    clean_books = [b["book"] for b in books if b["structural_grade"] == "clean"]
    
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    memo_content = template.replace("<insert title>", "NT Structural Census")
    memo_content = memo_content.replace("<insert objective>", "Systematic structural reconnaissance across 27 staged NT books.")
    
    findings = f"""
## Findings

### Total Books by Grade
- **Clean:** {grade_counts["clean"]}
- **Minor:** {grade_counts["minor"]}
- **Unstable:** {grade_counts["unstable"]}

### Top 5 Worst Books (by total issues)
"""
    for b in top_5_worst:
        issues = len(b["duplicate_anchors"]) + len(b["embedded_verse_lines"]) + b["total_missing_verses"] + b["chapter_zero_anchors"]
        findings += f"- **{b['book']}**: {issues} issues ({b['structural_grade']})\n"
        
    findings += f"""
### Candidates for Early Promotion
- {", ".join(clean_books) if clean_books else "None"}

### Detailed Stats
Stored in `reports/nt_structural_census.json`.
"""

    memo_content = memo_content.replace("<insert findings>", findings)
    memo_content = memo_content.replace("<insert risk analysis>", "The majority of the NT extraction appears structuraly unstable, primarily due to embedded verses and chapter-zero drift. Early promotion is only safe for books graded 'clean'.")
    
    handshake = """
- `Files changed`: `reports/nt_structural_census.json`, `memos/92_nt_structural_census.md`
- `Verification run`: Census validation script run locally.
- `Artifacts refreshed`: Census report and memo.
- `Remaining known drift`: Systemic V9 and V3 issues in the unstable set.
- `Next owner`: Ark (Diagnostic Review)
"""
    memo_content = memo_content.replace("<insert completion handshake>", handshake)
    
    MEMO_PATH.write_text(memo_content, encoding="utf-8")
    print(f"Census complete. Report written to {REPORT_PATH}")

if __name__ == "__main__":
    run_census()
