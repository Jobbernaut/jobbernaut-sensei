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
import re
import sys
from datetime import date, timedelta


def parse_metadata(filepath):
    """Re-imported from revisit.py — reads metadata variables from .py solution."""
    import ast
    required = {"last_solved", "revisit_in_days", "difficulty", "topic_tags"}
    meta = {}

    try:
        with open(filepath, "r") as f:
            source = f.read()
    except OSError:
        return None

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in required:
                    try:
                        meta[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass

    if not required.issubset(meta.keys()):
        return None

    try:
        meta["last_solved"]     = date.fromisoformat(meta["last_solved"])
        meta["revisit_in_days"] = int(meta["revisit_in_days"])
    except (ValueError, TypeError):
        return None

    if not isinstance(meta["topic_tags"], list):
        meta["topic_tags"] = [meta["topic_tags"]]

    return meta


def extract_url(filepath):
    """Return the first leetcode.com/problems URL found in the file, or None."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r"https://leetcode\.com/problems/[^\s'\"]+", line)
                if m:
                    url = m.group(0).rstrip("/") + "/"
                    if "PROBLEM-SLUG" not in url:
                        return url
    except OSError:
        pass
    return None


def find_solution_files(root: str) -> list:
    """Walk the repo and return all .py solution files."""
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "docs"}
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for filename in filenames:
            if filename.endswith(".py") and filename not in ("hint.py", "revisit.py", "mark.py"):
                files.append(os.path.join(dirpath, filename))
    return files


def normalise(s: str) -> str:
    """Lowercase, strip punctuation, collapse spaces."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_match(query, files):
    """Fuzzy match query against file paths. Same logic as mark/lopen."""
    q = normalise(query)

    if q.isdigit():
        for f in files:
            stem = os.path.splitext(os.path.basename(f))[0]
            parts = stem.split("-")
            if parts[0] == q:
                return f
        return None

    candidates = []
    for f in files:
        stem = normalise(os.path.splitext(os.path.basename(f))[0])
        if q in stem:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        candidates.sort(key=lambda f: normalise(os.path.splitext(os.path.basename(f))[0]).index(q))
        return candidates[0]
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: sensei hint <problem>"}))
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    prob_root = os.path.join(repo_root, "problems")

    files = find_solution_files(prob_root)
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