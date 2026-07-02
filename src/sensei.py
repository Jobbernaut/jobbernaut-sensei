import json
import os
import sys
import hint
import mark
import new
import lopen
import revisit
import rebalance
from utils import find_solution_files, find_match, parse_metadata


def cmd_init():
    """Scaffold an empty problems/ directory."""
    problems_dir = os.path.join(os.getcwd(), "problems")

    if os.path.isdir(problems_dir):
        print(f"\n  [OK]  Problems directory already exists: {problems_dir}\n")
        return

    os.makedirs(problems_dir)
    placeholder = os.path.join(problems_dir, ".gitkeep")
    with open(placeholder, "w") as f:
        f.write("")

    print(f"\n  [OK]  Initialized empty problems/ directory at:")
    print(f"        {problems_dir}\n")
    print(f"        Run 'sensei new' to scaffold your first problem!\n")


def cmd_show():
    """Show a problem's metadata and solution code (agent-friendly)."""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: sensei show <problem>"}))
        sys.exit(1)

    query = " ".join(sys.argv[2:])
    prob_root = os.path.join(os.getcwd(), "problems")

    if not os.path.isdir(prob_root):
        print(json.dumps({"error": "problems/ directory not found. Run 'sensei init' first."}))
        sys.exit(1)

    # Use same matching logic from mark/lopen
    files = find_solution_files(prob_root)
    match = find_match(query, files)

    if match is None:
        print(json.dumps({"error": f"No match found for: {query}"}))
        sys.exit(1)

    # Read metadata
    meta = parse_metadata(match)
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
        number = None
        title = stem.replace("-", " ").title()
        label = title

    # Relative path for context
    rel_path = os.path.relpath(match, os.getcwd())

    result = {
        "label": label,
        "number": number,
        "title": title,
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
    problems_root = os.path.join(os.getcwd(), "problems")
    from datetime import date, timedelta

    if not os.path.isdir(problems_root):
        print(json.dumps({"error": "problems/ directory not found. Run 'sensei init' first."}))
        sys.exit(1)

    today = date.today()
    problems = revisit.collect_problems(problems_root)

    if not problems:
        print(json.dumps({"total": 0, "overdue": 0, "due_today": 0, "upcoming": 0, "problems": []}))
        return

    overdue = [p for p in problems if p["due_date"] < today]
    due_today = [p for p in problems if p["due_date"] == today]
    upcoming = [p for p in problems if today < p["due_date"] <= today + timedelta(days=7)]
    
    active_queue = overdue + due_today + upcoming

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
            for p in active_queue
        ],
    }
    print(json.dumps(result, indent=2))


def main():
    if len(sys.argv) < 2:
        print("\n  Jobbernaut Sensei CLI")
        print("  Usage: sensei <command> [args]\n")
        print("  Available commands:")
        print("    init       - Initialize the problems/ directory")
        print("    revisit    - Run daily review (--json for agent-friendly output)")
        print("    new        - Scaffold a new problem")
        print("    open       - Open a problem in editor/browser")
        print("    hint       - Show problem metadata + URL only (no solution, for coaching)")
        print("    mark       - Mark a problem as solved (--rating e|g|h|s for non-interactive)")
        print("    show       - Show problem metadata + solution (JSON output)")
        print("    status     - Quick summary statistics (JSON output)")
        print("    rebalance  - Spread overloaded review days (--apply to write changes)")
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
    elif cmd == "hint":
        hint.main()
    elif cmd == "open":
        lopen.main()
    elif cmd == "revisit":
        revisit.main()
    elif cmd == "rebalance":
        rebalance.main()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
