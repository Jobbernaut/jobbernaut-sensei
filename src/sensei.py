import json
import os
import sys
import mark
import new
import lopen
import revisit


def cmd_init():
    """Scaffold an empty problems/ directory."""
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    problems_dir = os.path.join(repo_root, "problems")

    if os.path.isdir(problems_dir):
        print(f"\n  ✓  Problems directory already exists: {problems_dir}\n")
        return

    os.makedirs(problems_dir)
    placeholder = os.path.join(problems_dir, ".gitkeep")
    with open(placeholder, "w") as f:
        f.write("")

    print(f"\n  ✓  Initialized empty problems/ directory at:")
    print(f"     {problems_dir}\n")
    print(f"     Run 'sensei new' to scaffold your first problem!\n")


def cmd_show():
    """Show a problem's metadata and solution code (agent-friendly)."""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: sensei show <problem>"}))
        sys.exit(1)

    query = " ".join(sys.argv[2:])
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    prob_root = os.path.join(repo_root, "problems")

    # Use same matching logic from mark/lopen
    files = _find_solution_files(prob_root)
    match = _find_match(query, files)

    if match is None:
        print(json.dumps({"error": f"No match found for: {query}"}))
        sys.exit(1)

    # Read metadata
    meta = revisit.parse_metadata(match)
    if meta is None:
        print(json.dumps({"error": f"Could not parse metadata from {match}"}))
        sys.exit(1)

    # Read solution code
    solution = revisit.extract_solution(match)

    # Build label
    stem = os.path.splitext(os.path.basename(match))[0]
    parts = stem.split("-")
    if parts[0].isdigit():
        number = parts[0]
        title = " ".join(parts[1:]).title()
        label = f"{int(number)}. {title}"
    else:
        label = stem.replace("-", " ").title()

    # Relative path for context
    rel_path = os.path.relpath(match, repo_root)

    result = {
        "label": label,
        "number": parts[0] if parts[0].isdigit() else None,
        "title": title if parts[0].isdigit() else label,
        "filepath": rel_path,
        "metadata": {
            "last_solved": meta["last_solved"].isoformat(),
            "revisit_in_days": meta["revisit_in_days"],
            "difficulty": meta["difficulty"],
            "topic_tags": meta["topic_tags"],
            "due_date": (meta["last_solved"] + __import__("datetime").timedelta(days=meta["revisit_in_days"])).isoformat(),
        },
        "solution": solution,
    }
    print(json.dumps(result, indent=2))


def cmd_status():
    """Quick summary as JSON for AI agents."""
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    problems_root = os.path.join(repo_root, "problems")
    from datetime import date, timedelta

    today = date.today()
    problems = revisit.collect_problems(problems_root)

    if not problems:
        print(json.dumps({"total": 0, "overdue": 0, "due_today": 0, "upcoming": 0, "problems": []}))
        return

    overdue = [p for p in problems if p["due_date"] < today]
    due_today = [p for p in problems if p["due_date"] == today]
    upcoming = [p for p in problems if today < p["due_date"] <= today + timedelta(days=7)]

    result = {
        "total": len(problems),
        "overdue": len(overdue),
        "due_today": len(due_today),
        "upcoming": len(upcoming),
        "problems": [
            {
                "label": p["label"].strip(),
                "difficulty": p["difficulty"],
                "last_solved": p["last_solved"].isoformat(),
                "due_date": p["due_date"].isoformat(),
                "days_until_due": (p["due_date"] - today).days,
                "topics": p["topic_tags"],
                "topic_folder": p["topic_folder"],
            }
            for p in problems
        ],
    }
    print(json.dumps(result, indent=2))


def _find_solution_files(root: str) -> list:
    """Walk the repo and return all .py solution files."""
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "docs"}
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(dirpath, filename))
    return files


def _normalise(s: str) -> str:
    """Lowercase, strip punctuation, collapse spaces."""
    return __import__("re").sub(r"[^a-z0-9]", "", s.lower())


def _find_match(query, files):
    """Fuzzy match query against file paths. Same logic as mark/lopen."""
    q = _normalise(query)

    if q.isdigit():
        for f in files:
            stem = os.path.splitext(os.path.basename(f))[0]
            parts = stem.split("-")
            if parts[0] == q:
                return f
        return None

    candidates = []
    for f in files:
        stem = _normalise(os.path.splitext(os.path.basename(f))[0])
        if q in stem:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        candidates.sort(key=lambda f: _normalise(os.path.splitext(os.path.basename(f))[0]).index(q))
        return candidates[0]
    return None


def main():
    if len(sys.argv) < 2:
        print("\n  Jobbernaut Sensei CLI")
        print("  Usage: sensei <command> [args]\n")
        print("  Available commands:")
        print("    init     - Initialize the problems/ directory")
        print("    revisit  - Run daily review (--json for agent-friendly output)")
        print("    new      - Scaffold a new problem")
        print("    open     - Open a problem in editor/browser")
        print("    mark     - Mark a problem as solved (--rating e|g|h|s for non-interactive)")
        print("    show     - Show problem metadata + solution (JSON output)")
        print("    status   - Quick summary statistics (JSON output)")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
        return
    elif cmd == "show":
        cmd_show()
        return
    elif cmd == "status":
        cmd_status()
        return

    # Remove 'sensei' and the command name from argv for the sub-scripts
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if cmd == "mark":
        mark.main()
    elif cmd == "new":
        new.main()
    elif cmd == "open":
        lopen.main()
    elif cmd == "revisit":
        revisit.main()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()