"""
sir_final_recovery.py — Final surgical recovery for Sirach residual gaps (Line-by-Line).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
SIR_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "SIR.md"

def final_fix():
    if not SIR_PATH.exists():
        return

    lines = SIR_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if line.strip() == "## Chapter 36":
            # Check if next few lines have V1
            has_v1 = False
            for j in range(i+1, min(i+5, len(lines))):
                if "SIR.36:1" in lines[j]:
                    has_v1 = True; break
            if not has_v1:
                new_lines.append("")
                new_lines.append("SIR.36:1 Have mercy upon us, O Lord God of all, and behold us, and send Your fear upon all the nations. †")
        
        if line.strip() == "## Chapter 38":
            has_v1 = False
            for j in range(i+1, min(i+5, len(lines))):
                if "SIR.38:1" in lines[j]:
                    has_v1 = True; break
            if not has_v1:
                new_lines.append("")
                new_lines.append("SIR.38:1 Honor the physician with the honor due him for his services, For the Lord created him . †")

    SIR_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("Line-by-Line Sirach surgical fixes applied.")

if __name__ == "__main__":
    final_fix()
