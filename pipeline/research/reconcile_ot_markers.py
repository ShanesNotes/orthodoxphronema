import json
import re
from pathlib import Path

REPO_ROOT = Path("/home/ark/orthodoxphronema")
OT_DIR = REPO_ROOT / "staging" / "validated" / "OT"
OUT_DIR = REPO_ROOT / "reports" / "ot_marker_reconciliation"

# Anchor-based parsing is the structural truth
RE_FOOTNOTE_ANCHOR = re.compile(
    r"^\*\(anchor:\s+([A-Z0-9]{3}\.\d+:\d+)\)\*\s*$",
    re.MULTILINE,
)

def reconcile_book(book_code):
    m_path = OT_DIR / f"{book_code}_footnote_markers.json"
    f_path = OT_DIR / f"{book_code}_footnotes.md"
    s_path = OT_DIR / f"{book_code}.md"
    
    if not m_path.exists() or not f_path.exists():
        return None
        
    with open(m_path) as f:
        m_data = json.load(f)
        if isinstance(m_data, dict):
            markers = m_data.get("markers", [])
        else:
            markers = m_data
            
    f_content = f_path.read_text(encoding="utf-8")
    fn_anchors = RE_FOOTNOTE_ANCHOR.findall(f_content)
    unique_fn_anchors = set(fn_anchors)
            
    scripture_text = s_path.read_text(encoding="utf-8") if s_path.exists() else ""
    
    marker_anchors = [m.get("anchor") for m in markers if m.get("anchor")]
    unique_marker_anchors = sorted(list(set(marker_anchors)))
    
    matching = []
    missing_footnote = []
    orphaned = []
    
    for anchor in unique_marker_anchors:
        # Check if anchor exists in scripture
        if scripture_text and anchor not in scripture_text:
            orphaned.append(anchor)
            
        if anchor in unique_fn_anchors:
            matching.append(anchor)
        else:
            missing_footnote.append(anchor)
            
    # Also find footnotes without markers
    missing_marker = sorted(list(unique_fn_anchors - set(marker_anchors)))
    
    report = {
        "book": book_code,
        "total_markers": len(markers),
        "unique_marker_anchors": len(unique_marker_anchors),
        "total_footnote_entries": len(fn_anchors),
        "unique_footnote_anchors": len(unique_fn_anchors),
        "matching_anchors": len(matching),
        "missing_footnote_entries": missing_footnote,
        "missing_markers_in_scripture": missing_marker,
        "orphaned_anchors": orphaned,
        "structural_pattern": "Standard"
    }
    
    # Observe patterns
    if any("0:" in a for a in unique_marker_anchors):
        report["structural_pattern"] = "Chapter-zero drift detected in markers"
    elif len(missing_footnote) > len(matching):
        report["structural_pattern"] = "Heavy footnote gap"
        
    return report

def run_reconciliation():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    books = ["PSA", "SIR", "1ES", "ECC", "1SA", "DEU", "NUM"]
    for b in books:
        print(f"Reconciling {b}...")
        report = reconcile_book(b)
        if report:
            (OUT_DIR / f"{b}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(f"  Report written: {b}.json (Matches: {report['matching_anchors']})")

if __name__ == "__main__":
    run_reconciliation()
