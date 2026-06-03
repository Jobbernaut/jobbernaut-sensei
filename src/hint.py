'''
Show problem metadata + LeetCode URL without the solution code.
Agent-friendly JSON output for quizzing/coaching.

Usage:
    sensei hint 217
    sensei hint contains-duplicate
    sensei hint "valid anagram"
'''

import json
import os
import sys
from datetime import date, timedelta

from utils import parse_metadata, find_solution_files, find_match, extract_url


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: sensei hint <problem>"}))
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    prob_root = os.path.join(os.getcwd(), "problems")

    if not os.path.isdir(prob_root):
        print(json.dumps({"error": "problems/ directory not found. Run 'sensei init' first."}))
        sys.exit(1)

    files = find_solution_files(prob_root, exclude_files={"hint.py", "revisit.py", "mark.py"})
    match = find_match(query, files)

    if match is None:
        print(json.dumps({"error": f"No match found for: {query}"}))
        sys.exit(1)

    meta = parse_metadata(match)
    if meta is None:
        print(json.dumps({"error": f"Could not parse metadata from {match}"}))
        sys.exit(1)

    # Build label
    stem = os.path.splitext(os.path.basename(match))[0]
    parts = stem.split("-")
    if parts[0].isdigit():
        number = parts[0]
        title = " ".join(parts[1:]).title()
        label = f"{int(number)}. {title}"
    else:
        number = None
        title = stem.replace("-", " ").title()
        label = title

    due_date = meta["last_solved"] + timedelta(days=meta["revisit_in_days"])
    today = date.today()
    url = extract_url(match)

    result = {
        "label": label,
        "number": number,
        "title": title,
        "difficulty": meta["difficulty"],
        "topics": meta["topic_tags"],
        "url": url,
        "status": {
            "last_solved": meta["last_solved"].isoformat(),
            "due_date": due_date.isoformat(),
            "days_until_due": (due_date - today).days,
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
