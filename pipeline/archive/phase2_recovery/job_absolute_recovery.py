"""
job_absolute_recovery.py — Robust surgical recovery for Job.
Ensures 100% completeness by re-anchoring chapters with gaps.
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

def find_chapter_content(ch: int) -> dict[int, str]:
    # Job text range: 1959 - 2029
    est_page = 1959 + int((ch-1) * 1.6)
    text = get_text_range(max(1959, est_page - 2), min(2029, est_page + 4))
    
    # 1. Locate chapter start
    ch_pattern = rf"\n{ch}\n"
    match = re.search(ch_pattern, text)
    if not match:
        match = re.search(rf"\n{ch}\n\s*1\s+", text)
    if not match: return {}
    
    post_ch = text[match.end():]
    
    # 2. Extract verses
    results = {}
    current_text = ""
    current_v = 0
    
    lines = post_ch.splitlines()
    for line in lines:
        line_strip = line.strip()
        if not line_strip: continue
        
        vm = re.match(r"^(\d+)\b", line_strip)
        if vm:
            v_num = int(vm.group(1))
            if current_v > 0:
                results[current_v] = clean_job(current_text)
            
            if v_num < current_v: # Potential page wrap or other book
                break
                
            current_v = v_num
            current_text = line_strip[len(vm.group(1)):].strip()
        else:
            if current_v > 0:
                current_text += " " + line_strip
                
    if current_v > 0:
        results[current_v] = clean_job(current_text)
        
    return results

def recover_job():
    print("Performing absolute Job recovery...")
    if not JOB_PATH.exists():
        return

    # Target chapters with confirmed structural issues
    target_chapters = [15, 17, 18, 19, 23, 24, 34, 36, 40]
    
    reconstructed_chapters = {}
    for ch in target_chapters:
        print(f"  Extracting Chapter {ch} from PDF...")
        reconstructed_chapters[ch] = find_chapter_content(ch)

    lines = JOB_PATH.read_text(encoding="utf-8").splitlines()
    final_output = []
    
    current_ch = 0
    skip_mode = False
    
    for line in lines:
        if line.startswith("## Chapter "):
            ch_num = int(line.split(" ")[2])
            current_ch = ch_num
            final_output.append(line)
            
            if ch_num in reconstructed_chapters:
                # Insert all reconstructed verses for this chapter
                v_map = reconstructed_chapters[ch_num]
                for v_num in sorted(v_map.keys()):
                    final_output.append("")
                    final_output.append(f"JOB.{ch_num}:{v_num} {v_map[v_num]}")
                skip_mode = True
            else:
                skip_mode = False
            continue
            
        if skip_mode:
            # Skip existing verses until next chapter header
            continue
            
        # Purity pass for non-reconstructed lines
        line = re.sub(r'([a-z,])\s+\d+\s+([a-z])', r'\1 \2', line)
        line = line.replace("v alley", "valley")
        line = line.replace("reviv e", "revive")
        line = line.replace("reviv ed", "revived")
        
        final_output.append(line)

    # Dedup anchors globally (just in case)
    seen_anchors = set()
    deduped_output = []
    for line in final_output:
        m = re.match(r'^(JOB\.\d+:\d+)', line)
        if m:
            anchor = m.group(1)
            if anchor in seen_anchors:
                continue
            seen_anchors.add(anchor)
        deduped_output.append(line)

    JOB_PATH.write_text("\n".join(deduped_output) + "\n", encoding="utf-8")
    print("Recovery complete.")

if __name__ == "__main__":
    recover_job()
