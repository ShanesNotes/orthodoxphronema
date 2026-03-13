"""
job_final_recovery.py — Final surgical recovery for Job residual gaps (Line-by-Line).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
JOB_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "JOB.md"

def final_fix():
    if not JOB_PATH.exists():
        return

    lines = JOB_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    
    for i, line in enumerate(lines):
        # 1. Ch 15 replacement
        if line.strip() == "JOB.15:1 Then Job answered the Lord and said:":
            new_lines.append("JOB.15:1 Then Eliphaz the Temanite answered and said: †")
            new_lines.append("")
            new_lines.append("JOB.15:2 Will a wise man give as an answer a breath of understanding, And does he satisfy the pain in his belly,")
            new_lines.append("")
            new_lines.append("JOB.15:3 Arguing with sayings which are not necessary And with words wherein is no profit?")
            new_lines.append("")
            new_lines.append("JOB.15:4 Have you not moreover cast off fear And accomplished such words before the Lord?")
            new_lines.append("")
            new_lines.append("JOB.15:5 You are guilty because of the words of your mouth, Nor have you discerned the words of the mighty.")
            new_lines.append("")
            new_lines.append("JOB.15:6 May your mouth convict you, and not I; For your lips will testify against you.")
            new_lines.append("")
            new_lines.append("JOB.15:7 What? Are you the first man who was born? Or were you made before the beaches?")
            continue

        # 2. Ch 34 insertion
        if line.strip() == "## Chapter 34":
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("JOB.34:1 Then Elihu continued and said: †")
            new_lines.append("")
            new_lines.append("JOB.34:2 Hear me, you wise men; Listen to me, you who have knowledge.")
            # Skip potential next blank lines to avoid tripling
            continue

        # 3. Ch 36 insertion
        if line.strip() == "JOB.36:28 The clouds will pour down, And the rain will fall upon many people.":
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("JOB.36:29 He will provide quietness, and who shall condemn Him? And who shall behold His face? He will do so against a nation and against a man together,")
            new_lines.append("")
            new_lines.append("JOB.36:30 To cause a hypocrite to be king, Because of the difficulty of the people.")
            continue

        # 4. Ch 40 cleanup
        if line.strip() == "## Chapter 40":
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("JOB.40:1 Then the Lord answered Job and said: †")
            # 40:2 already exists
            continue
        
        if line.strip() == "JOB.40:2 Will anyone evade judgment with the Mighty One? He who reproves God, let him answer it.":
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("JOB.40:3 Then Job answered the Lord and said: †")
            continue

        new_lines.append(line)

    JOB_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("Line-by-Line Job surgical fixes applied.")

if __name__ == "__main__":
    final_fix()
