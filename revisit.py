'''
Daily review runner.

Usage:
    python revisit.py                   # overdue + due today + upcoming 7 days
    python revisit.py --all             # show every tracked problem
    python revisit.py --topic arrays    # filter by topic tag (partial match)
'''

import os
import ast
import sys
from datetime import date, timedelta

# ── ANSI colours ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def parse_metadata(filepath):
    """
    Reads a .py solution file and extracts the 4 metadata variables.
    Returns None if any required field is missing or malformed.
    """
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


def collect_problems(root):
    """Walk the repo and collect every solution file that has valid metadata."""
    problems = []
    skip_dirs = {"copy_templates", ".git", "__pycache__", "venv", ".venv", "docs"}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            if filename == "revisit.py":
                continue

            filepath = os.path.join(dirpath, filename)
            meta = parse_metadata(filepath)
            if meta is None:
                continue

            # "217-Contains-Duplicate.py" -> "217. Contains Duplicate"
            stem  = os.path.splitext(filename)[0]
            parts = stem.split("-")
            if parts[0].isdigit():
                number = parts[0]
                title  = " ".join(parts[1:]).title()
                label  = f"{int(number):>4}. {title}"
            else:
                label = stem.replace("-", " ").title()

            rel_dir      = os.path.relpath(dirpath, root)
            topic_folder = rel_dir.split(os.sep)[0]
            due_date     = meta["last_solved"] + timedelta(days=meta["revisit_in_days"])

            problems.append({
                "label":        label,
                "topic_folder": topic_folder,
                "topic_tags":   meta["topic_tags"],
                "difficulty":   meta["difficulty"],
                "last_solved":  meta["last_solved"],
                "due_date":     due_date,
            })

    problems.sort(key=lambda p: p["due_date"])
    return problems


def days_label(delta):
    if delta == 0:
        return f"{YELLOW}today       {RESET}"
    elif delta < 0:
        return f"{RED}{abs(delta)}d ago     {RESET}"
    else:
        return f"{GREEN}in {delta}d        {RESET}"


def print_section(title, colour, problems, today):
    if not problems:
        return
    print(f"\n{colour}{BOLD}{title}{RESET}")
    print(f"{GREY}{'─' * 74}{RESET}")
    for p in problems:
        delta    = (p["due_date"] - today).days
        dlabel   = days_label(delta)
        diff_str = f"[{p['difficulty']:<6}]"
        tags_str = f"({', '.join(p['topic_tags'])})"
        print(f"  {dlabel}  {diff_str}  {BOLD}{p['label']:<38}{RESET}  {GREY}{tags_str}{RESET}")


def main():
    args         = sys.argv[1:]
    show_all     = "--all" in args
    topic_filter = None

    if "--topic" in args:
        idx = args.index("--topic")
        if idx + 1 < len(args):
            topic_filter = args[idx + 1].lower()

    root     = os.path.dirname(os.path.abspath(__file__))
    today    = date.today()
    problems = collect_problems(root)

    if topic_filter:
        problems = [
            p for p in problems
            if any(topic_filter in t.lower() for t in p["topic_tags"])
        ]

    overdue   = [p for p in problems if p["due_date"] <  today]
    due_today = [p for p in problems if p["due_date"] == today]
    upcoming  = [p for p in problems if today < p["due_date"] <= today + timedelta(days=7)]
    future    = [p for p in problems if p["due_date"] > today + timedelta(days=7)]

    print(f"\n{BOLD}{CYAN}📅  LeetCode Revisit — {today.strftime('%A, %B %-d %Y')}{RESET}")
    if topic_filter:
        print(f"{GREY}    Filtered by topic: {topic_filter}{RESET}")

    if not problems:
        print(f"\n{GREY}  No problems with metadata found.{RESET}\n")
        return

    print_section("🔴  OVERDUE",            RED,    overdue,   today)
    print_section("🟡  DUE TODAY",          YELLOW, due_today, today)
    print_section("🟢  UPCOMING (7 days)",  GREEN,  upcoming,  today)

    if show_all and future:
        print_section("⚪  FUTURE",          GREY,   future,    today)

    total = len(overdue) + len(due_today)
    print(f"\n{GREY}{'─' * 74}{RESET}")
    print(f"  {BOLD}{total} problem(s){RESET} need attention today.  "
          f"Total tracked: {len(problems)}\n")


if __name__ == "__main__":
    main()
