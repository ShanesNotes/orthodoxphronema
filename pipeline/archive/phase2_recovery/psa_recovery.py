"""
psa_recovery.py — Recover missing verses in Psalms by splitting on markers and drop-caps.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PSA_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "PSA.md"

RE_ANCHOR = re.compile(r'^(PSA\.(\d+):(\d+))\s+(.*)$')
RE_VERSE_NUM = re.compile(r'^(\(\d+\)\s+)?\d+\s*')
RE_DROP_CAP_START = re.compile(r'([.!?]["\']?)\s+([A-Z])')

def recover_psalms():
    if not PSA_PATH.exists():
        print(f"Error: {PSA_PATH} not found.")
        return

    lines = PSA_PATH.read_text(encoding="utf-8").splitlines()
    
    # First pass: map anchors to their text
    anchors = []
    for i, line in enumerate(lines):
        m = RE_ANCHOR.match(line)
        if m:
            anchors.append({
                "line_idx": i,
                "anchor": m.group(1),
                "ch": int(m.group(2)),
                "v": int(m.group(3)),
                "text": m.group(4)
            })
    
    modified_indices = {}

    for i in range(len(anchors)):
        curr = anchors[i]
        next_anchor = anchors[i+1] if i + 1 < len(anchors) else None
        
        if next_anchor and next_anchor["ch"] == curr["ch"]:
            gap_size = next_anchor["v"] - curr["v"]
            if gap_size > 1:
                split_point = -1
                split_marker = ""
                
                if "†ω" in curr["text"]:
                    split_point = curr["text"].find("†ω")
                    split_marker = "†ω"
                elif "†" in curr["text"]:
                    split_point = curr["text"].find("†")
                    split_marker = "†"
                
                if split_point != -1:
                    title_part = curr["text"][:split_point + len(split_marker)].strip()
                    body_part = curr["text"][split_point + len(split_marker):].strip()
                    
                    if body_part:
                        v1_anchor = f"PSA.{curr['ch']}:{curr['v']}"
                        v2_anchor = f"PSA.{curr['ch']}:{curr['v']+1}"
                        title_part = RE_VERSE_NUM.sub("", title_part)
                        modified_indices[curr["line_idx"]] = [
                            f"{v1_anchor} {title_part}",
                            f"{v2_anchor} {body_part}"
                        ]
                        print(f"Recovered {v2_anchor} from {v1_anchor} (marker split)")
                        continue

                m_dc = RE_DROP_CAP_START.search(curr["text"])
                if m_dc:
                    split_idx = m_dc.end(1)
                    first_part = curr["text"][:split_idx].strip()
                    second_part = curr["text"][split_idx:].strip()
                    
                    v1_anchor = f"PSA.{curr['ch']}:{curr['v']}"
                    v2_anchor = f"PSA.{curr['ch']}:{curr['v']+1}"
                    first_part = RE_VERSE_NUM.sub("", first_part)
                    modified_indices[curr["line_idx"]] = [
                        f"{v1_anchor} {first_part}",
                        f"{v2_anchor} {second_part}"
                    ]
                    print(f"Recovered {v2_anchor} from {v1_anchor} (drop-cap split)")
                    continue

    final_output = []
    for i, line in enumerate(lines):
        if i in modified_indices:
            final_output.extend(modified_indices[i])
        else:
            m = RE_ANCHOR.match(line)
            if m and m.group(3) == "1":
                clean_text = RE_VERSE_NUM.sub("", m.group(4))
                final_output.append(f"{m.group(1)} {clean_text}")
            else:
                final_output.append(line)

    PSA_PATH.write_text("\n".join(final_output) + "\n", encoding="utf-8")
    print("PSA recovery complete.")

if __name__ == "__main__":
    recover_psalms()
