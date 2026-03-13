import re
import subprocess
from pathlib import Path

PDF_PATH = "/home/ark/orthodoxphronema/src.texts/the_orthodox_study_bible.pdf"

def extract_footnotes():
    # Psalms footnotes range: 6116-6247
    footnotes = {}
    current_key = None
    current_text = []

    for page in range(6116, 6248):
        cmd = ["pdftotext", "-f", str(page), "-l", str(page), PDF_PATH, "-"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        lines = res.stdout.splitlines()
        
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            
            # Match "X:Y " or "X:Y-Z " or just "X:Y" at start of line
            m = re.match(r"^(\d+):(\d+)(?:-\d+)?(?:\s+(.*))?$", line_strip)
            if m:
                # Save previous
                if current_key:
                    footnotes[current_key] = " ".join(current_text).strip()
                
                ch = m.group(1)
                vs = m.group(2)
                current_key = f"{ch}:{vs}"
                rest = m.group(3)
                current_text = [rest] if rest else []
            else:
                if current_key:
                    current_text.append(line_strip)
                    
    # Save last
    if current_key:
        footnotes[current_key] = " ".join(current_text).strip()
        
    return footnotes

if __name__ == "__main__":
    fns = extract_footnotes()
    print(f"Extracted {len(fns)} footnote entries.")
    # Print keys
    keys = sorted(fns.keys(), key=lambda x: [int(p) for p in x.split(':')])
    print(f"Sample keys: {keys[:20]}")
    # Check for 2:1
    if "2:1" in fns:
        print(f"2:1: {fns['2:1'][:100]}...")
