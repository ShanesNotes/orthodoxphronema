"""
sir_residue_recovery.py — Photius-style surgical residue recovery for Sirach.
Focuses on missing Verse 1s using the 'CH VERSE_TEXT' combined pattern.
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
SIR_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "SIR.md"
PDF_PATH = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"

def get_text_range(start_page: int, end_page: int) -> str:
    cmd = ["pdftotext", "-f", str(start_page), "-l", str(end_page), str(PDF_PATH), "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def clean_poetry(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    splits = [
        ("hav e", "have"), ("lov e", "love"), ("ev il", "evil"), ("ov er", "over"),
        ("m y", "my"), ("y ou", "you"), ("v oice", "voice"), ("heav en", "heaven"),
        ("v ain", "vain"), ("m an", "man"), ("m many", "many"), ("m ercy", "mercy"),
        ("v essel", "vessel"), ("† ω", "†ω"), ("†ω", "†ω")
    ]
    for old, new in splits:
        text = text.replace(old, new)
    return text.strip()

def find_v1_for_chapter(ch: int) -> str:
    est_page = 2293 + int((ch-1) * 2.0)
    text = get_text_range(max(2293, est_page - 2), min(2397, est_page + 4))
    
    # Combined pattern: \n(CH) (TEXT)\n
    # Use a more flexible regex that allows intervening pericope titles
    # Search for digit 'ch' followed by optional pericope title, then Verse 1 text.
    # Pattern: \n(CH)\n ... optional ... 1? (TEXT)
    
    match = re.search(rf"\n{ch}\n", text)
    if not match:
        # Try finding digit as part of a line if it's not standalone
        match = re.search(rf"\n\s*{ch}\s+(?:[A-Z].*?)\n", text)
        if not match: return ""
    
    post_ch = text[match.end():]
    
    # Look for '1 ' or the first line starting with a Capital letter after some optional centered titles
    # Skip short centered titles (pericopes)
    v1_text = ""
    lines = post_ch.splitlines()
    found_start = False
    for line in lines:
        line_strip = line.strip()
        if not line_strip: continue
        
        # Check if it starts with '1 ' or just a capital letter if we haven't found a verse number yet
        v_match = re.match(r"^(?:1\s+)?([A-Z].*)", line_strip)
        if v_match and not found_start:
            # If it's a short centered-looking title, it's a pericope, skip it.
            # (Unless it's '1 ' specifically)
            if len(line_strip) < 40 and not line_strip.startswith("1 "):
                continue
            
            found_start = True
            v1_text = v_match.group(1)
            continue
        
        if found_start:
            if re.match(r"^\d+\b", line_strip): break # Next verse
            v1_text += " " + line_strip
            
    return clean_poetry(v1_text) if v1_text else ""

def recover_sirach():
    print("Surgically recovering Sirach residuals (Combined Mode)...")
    if not SIR_PATH.exists():
        return

    lines = SIR_PATH.read_text(encoding="utf-8").splitlines()
    found_v1s = set()
    for line in lines:
        m = re.match(r'^SIR\.(\d+):1\b', line)
        if m: found_v1s.add(int(m.group(1)))
    
    missing_v1s = [ch for ch in range(1, 52) if ch not in found_v1s]
    print(f"Missing Verse 1s: {len(missing_v1s)}")
    
    v1_map = {}
    for ch in missing_v1s:
        txt = find_v1_for_chapter(ch)
        if txt:
            print(f"  Recovered SIR.{ch}:1: {txt[:50]}...")
            v1_map[ch] = txt
        else:
            print(f"  FAILED to recover SIR.{ch}:1")

    final_output = []
    i = 0
    while i < len(lines):
        line = lines[i]
        final_output.append(line)
        if line.startswith("## Chapter "):
            ch_num = int(line.split(" ")[2])
            if ch_num in v1_map:
                has_v1 = False
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].startswith(f"SIR.{ch_num}:1"):
                        has_v1 = True; break
                if not has_v1:
                    final_output.append("")
                    final_output.append(f"SIR.{ch_num}:1 {v1_map[ch_num]}")
        i += 1

    SIR_PATH.write_text("\n".join(final_output) + "\n", encoding="utf-8")
    print("Recovery complete.")

if __name__ == "__main__":
    recover_sirach()
