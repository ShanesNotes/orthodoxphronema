import json
import re
from pathlib import Path

REPO_ROOT = Path("/home/ark/orthodoxphronema")
PSA_MARKERS_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "PSA_footnote_markers.json"
PSA_SCRIPTURE_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "PSA.md"
PSA_FOOTNOTES_OUT = REPO_ROOT / "staging" / "validated" / "OT" / "PSA_footnotes.md"

def get_real_anchor(excerpt, scripture_text):
    # Clean excerpt for matching
    clean_excerpt = excerpt.replace("†ω", "").replace("†", "").replace("††", "").strip()
    # Try to find the line containing this excerpt
    lines = scripture_text.splitlines()
    for line in lines:
        if clean_excerpt in line:
            m = re.match(r"^(PSA\.\d+:\d+)", line)
            if m:
                return m.group(1)
    return None

def generate_psa_footnotes():
    with open(PSA_MARKERS_PATH) as f:
        markers_data = json.load(f)
    
    scripture_text = PSA_SCRIPTURE_PATH.read_text(encoding="utf-8")
    
    # Use my previous extraction logic to get the footnotes dictionary
    from extract_psa_footnotes import extract_footnotes
    fns_dict = extract_footnotes()
    
    output = []
    output.append("---")
    output.append("book_code: PSA")
    output.append("content_type: footnotes")
    output.append('source: "OSB-v1"')
    output.append('parse_date: "2026-03-11"')
    output.append("status: staging")
    output.append("---")
    output.append("")
    output.append("## Footnotes")
    output.append("")
    
    seen_anchors = set()
    recoverable_count = 0
    unrecoverable_markers = []

    for m in markers_data["markers"]:
        real_anchor = get_real_anchor(m["raw_excerpt"], scripture_text)
        if not real_anchor:
            unrecoverable_markers.append(f"Marker {m['marker_seq_book']} at page {m['page']} excerpt '{m['raw_excerpt']}'")
            continue
            
        if real_anchor in seen_anchors:
            continue
            
        # Extract CH:V from PSA.CH:V
        ch_v = real_anchor.replace("PSA.", "")
        
        if ch_v in fns_dict:
            output.append(f"### {ch_v}")
            output.append(f"*(anchor: {real_anchor})*")
            output.append("")
            output.append(fns_dict[ch_v])
            output.append("")
            seen_anchors.add(real_anchor)
            recoverable_count += 1
        else:
            # Try to match by chapter only if it's verse 1 (superscription)
            # Many titles have notes labeled simply by chapter in some extractions
            # But here fns_dict has "1:1", "2:1" etc.
            unrecoverable_markers.append(f"No footnote text found for anchor {real_anchor} (CH:V {ch_v})")

    PSA_FOOTNOTES_OUT.write_text("\n".join(output), encoding="utf-8")
    print(f"Created PSA_footnotes.md with {recoverable_count} entries.")
    if unrecoverable_markers:
        print(f"Unrecoverable markers: {len(unrecoverable_markers)}")
        # print("\n".join(unrecoverable_markers[:10]))

if __name__ == "__main__":
    generate_psa_footnotes()
