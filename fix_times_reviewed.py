import os
import re

problems_dir = "problems"

for root, dirs, files in os.walk(problems_dir):
    for fname in files:
        if fname.endswith(".py"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r") as f:
                content = f.read()

            # If already has times_reviewed, ensure it's >= 5
            if "times_reviewed" in content:
                def replace_tr(m):
                    val = int(m.group(1))
                    if val < 5:
                        return f"times_reviewed  = 6"
                    return m.group(0)
                new_content = re.sub(r"times_reviewed\s+=\s+([0-9]+)", replace_tr, content)
                if new_content != content:
                    with open(fpath, "w") as f:
                        f.write(new_content)
                    print(f"Updated times_reviewed: {fpath}")
            else:
                # Insert times_reviewed = 6 after revisit_in_days line
                new_content = re.sub(
                    r"(revisit_in_days\s*=\s*[0-9]+)",
                    r"\1\ntimes_reviewed  = 6",
                    content
                )
                if new_content != content:
                    with open(fpath, "w") as f:
                        f.write(new_content)
                    print(f"Added times_reviewed: {fpath}")
                else:
                    print(f"SKIPPED (no revisit_in_days found): {fpath}")

print("Done.")
