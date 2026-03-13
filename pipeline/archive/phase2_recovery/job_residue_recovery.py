"""
job_residue_recovery.py — Photius-style surgical residue recovery for Job.
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
JOB_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "JOB.md"
PDF_PATH = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"

def get_text_range(start_page: int, end_page: int) -> str:
    cmd = ["pdftotext", "-f", str(start_page), "-l", str(end_page), str(PDF_PATH), "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def clean_job(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    splits = [
        ("hav e", "have"), ("lov e", "love"), ("ev il", "evil"), ("ov er", "over"),
        ("m y", "my"), ("y ou", "you"), ("v oice", "voice"), ("heav en", "heaven"),
        ("v ain", "vain"), ("m an", "man"), ("m many", "many"), ("m ercy", "mercy")
    ]
    for old, new in splits:
        text = text.replace(old, new)
    return text.strip()

def find_missing_verse(ch: int, v: int) -> str:
    # Approximate page: Job is 1959 - 2029 (42 chapters)
    # Approx 1.6 pages per chapter.
    est_page = 1959 + int((ch-1) * 1.6)
    text = get_text_range(max(1959, est_page - 2), min(2029, est_page + 4))
    
    # We look for the verse number 'v' in the neighborhood of 'ch'
    # For Verse 1, it's often 'ch Text' or 'ch\nText' or 'ch\n1 Text'
    if v == 1:
        # Pattern: \n(ch)\s+([A-Z].*?)\n or \n(ch)\n\s*([A-Z].*?)\n
        match = re.search(rf"\n{ch}\s+([A-Z].*?)\n", text)
        if not match:
            match = re.search(rf"\n{ch}\n\s*1\s+([A-Z].*?)\n", text)
        if not match:
            match = re.search(rf"\n{ch}\n\s*([A-Z].*?)\n", text)
            
        if match:
            v_text = match.group(1).strip()
            # Capture multi-line if needed
            remaining = text[match.end():]
            for line in remaining.splitlines():
                line_strip = line.strip()
                if not line_strip: continue
                if re.match(r"^\d+\b", line_strip): break
                v_text += " " + line_strip
            return clean_job(v_text)
    else:
        # For non-verse 1, it's '\n(v)\n(TEXT)' or '\n(v) (TEXT)'
        match = re.search(rf"\n{v}\n\s*([A-Z].*?)\n", text)
        if not match:
            match = re.search(rf"\n{v}\s+([A-Z].*?)\n", text)
        
        if match:
            v_text = match.group(1).strip()
            remaining = text[match.end():]
            for line in remaining.splitlines():
                line_strip = line.strip()
                if not line_strip: continue
                if re.match(r"^\d+\b", line_strip): break
                v_text += " " + line_strip
            return clean_job(v_text)
            
    return ""

def recover_job():
    print("Surgically recovering Job residuals...")
    if not JOB_PATH.exists():
        return

    text = JOB_PATH.read_text(encoding="utf-8")
    
    # Known missing verses from dossier:
    # 8:1, 9:16, 17:1, 17:2, 18:1, 18:2, 18:12, 19:3, 19:4, 20:1, 21:1, 22:1, 
    # 23:6-9, 23:12-15, 23:17, 24:1, 24:2, 25:1, 26:1, 27:22, 30:31, 34:1, 34:2,
    # 36:29, 36:30, 37:12, 39:1, 40:1, 40:3
    
    missing = [
        (8, 1), (9, 16), (17, 1), (17, 2), (18, 1), (18, 2), (18, 12), (19, 3), (19, 4),
        (20, 1), (21, 1), (22, 1), (23, 6), (23, 7), (23, 8), (23, 9), (23, 12), (23, 13),
        (23, 14), (23, 15), (23, 17), (24, 1), (24, 2), (25, 1), (26, 1), (27, 22), (30, 31),
        (34, 1), (34, 2), (36, 29), (36, 30), (37, 12), (39, 1), (40, 1), (40, 3)
    ]
    
    v_map = {}
    for ch, v in missing:
        txt = find_missing_verse(ch, v)
        if txt:
            print(f"  Recovered JOB.{ch}:{v}: {txt[:50]}...")
            v_map[(ch, v)] = txt
        else:
            print(f"  FAILED to recover JOB.{ch}:{v}")

    # Final pass: insert into file
    lines = text.splitlines()
    final_output = []
    
    for i, line in enumerate(lines):
        final_output.append(line)
        # Check for chapter header to insert V1
        if line.startswith("## Chapter "):
            ch_num = int(line.split(" ")[2])
            if (ch_num, 1) in v_map:
                final_output.append("")
                final_output.append(f"JOB.{ch_num}:1 {v_map[(ch_num, 1)]}")
        
        # Check for preceding verse to insert missing middle verse
        m = re.match(r'^JOB\.(\d+):(\d+)', line)
        if m:
            ch_num, v_num = int(m.group(1)), int(m.group(2))
            next_v = v_num + 1
            if (ch_num, next_v) in v_map:
                # Only insert if it doesn't already exist in next few lines
                exists = False
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].startswith(f"JOB.{ch_num}:{next_v} "):
                        exists = True; break
                if not exists:
                    final_output.append("")
                    final_output.append(f"JOB.{ch_num}:{next_v} {v_map[(ch_num, next_v)]}")

    JOB_PATH.write_text("\n".join(final_output) + "\n", encoding="utf-8")
    print("Recovery complete.")

if __name__ == "__main__":
    recover_job()
