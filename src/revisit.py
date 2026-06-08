'''
Daily review runner.

Usage:
    sensei revisit                   # overdue + due today + upcoming 7 days
    sensei revisit --all             # show every tracked problem
    sensei revisit --topic arrays    # filter by topic tag (partial match)
    sensei revisit --export          # export all problems to export.csv
    sensei revisit --export-md       # export all problems to export.md
'''

import json
import os
import csv
import sys
from datetime import date, timedelta

from utils import parse_metadata, find_solution_files, SKIP_DIRS

# ── ANSI colours ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def collect_problems(root):
    """Walk the repo and collect every solution file that has valid metadata."""
    problems = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            if filename in ("revisit.py", "mark.py"):
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
                "filepath":     filepath,
            })

    problems.sort(key=lambda p: p["due_date"])
    return problems


def extract_solution(filepath):
    """
    Read the .py file and return everything after the metadata block
    (after the last of the 4 required metadata lines).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return ""

    # Find the last line that is a metadata assignment
    meta_keys = {"last_solved", "revisit_in_days", "difficulty", "topic_tags"}
    last_meta_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        for key in meta_keys:
            if stripped.startswith(key) and "=" in stripped:
                last_meta_idx = i
                break

    if last_meta_idx == -1:
        return ""

    # Return everything after the metadata block, stripped of blank leading lines
    solution_lines = lines[last_meta_idx + 1:]
    # Drop leading blank lines
    while solution_lines and solution_lines[0].strip() == "":
        solution_lines.pop(0)

    return "".join(solution_lines).rstrip()


def export_csv(problems, root, today):
    """Write all problems to export.csv in the repo root."""
    out_path = os.path.join(root, "export.csv")
    fields   = ["Problem Name", "Difficulty", "Last Solved", "Next Review Date",
                "Days Until Due", "Topics", "Solution"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for p in problems:
            delta    = (p["due_date"] - today).days
            solution = extract_solution(p["filepath"])
            writer.writerow({
                "Problem Name":    p["label"].strip(),
                "Difficulty":      p["difficulty"],
                "Last Solved":     p["last_solved"].isoformat(),
                "Next Review Date": p["due_date"].isoformat(),
                "Days Until Due":  delta,
                "Topics":          ", ".join(p["topic_tags"]),
                "Solution":        solution,
            })

    return out_path


def export_md(problems, root, today):
    """Write all problems to export.md in the repo root."""
    out_path = os.path.join(root, "export.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Jobbernaut Sensei — Progress\n\n")
        f.write(f"_Generated: {today.isoformat()}_\n\n")
        f.write("| # | Problem | Difficulty | Last Solved | Next Review | Days Until Due | Topics |\n")
        f.write("|---|---------|------------|-------------|-------------|----------------|--------|\n")
        for p in problems:
            delta     = (p["due_date"] - today).days
            num_title = p["label"].strip()
            diff      = p["difficulty"]
            last      = p["last_solved"].isoformat()
            nxt       = p["due_date"].isoformat()
            topics    = ", ".join(p["topic_tags"])
            f.write(f"| {num_title} | {diff} | {last} | {nxt} | {delta} | {topics} |\n")

    return out_path


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
    do_json      = "--json"     in args
    do_export    = "--export"   in args
    do_export_md = "--export-md" in args
    topic_filter = None

    if "--topic" in args:
        idx = args.index("--topic")
        if idx + 1 < len(args):
            topic_filter = args[idx + 1].lower()

    problems_root = os.path.join(os.getcwd(), "problems")
    
    if not os.path.isdir(problems_root):
        if do_json:
            print(json.dumps({"error": "problems/ directory not found. Run 'sensei init' first."}))
        else:
            print(f"\n{GREY}  problems/ directory not found. Run 'sensei init' first.{RESET}\n")
        sys.exit(1)
    
    today         = date.today()
    problems      = collect_problems(problems_root)

    # ── Export mode ───────────────────────────────────────────────────────────
    if do_export or do_export_md:
        if not problems:
            print(f"\n{GREY}  No problems to export.{RESET}\n")
            return
        if do_export:
            out = export_csv(problems, os.getcwd(), today)
            print(f"\n{GREEN}[OK]{RESET}  Exported {BOLD}{len(problems)} problems{RESET} -> {CYAN}{os.path.relpath(out, os.getcwd())}{RESET}\n")
        if do_export_md:
            out = export_md(problems, os.getcwd(), today)
            print(f"\n{GREEN}[OK]{RESET}  Exported {BOLD}{len(problems)} problems{RESET} -> {CYAN}{os.path.relpath(out, os.getcwd())}{RESET}\n")
        return

    if topic_filter:
        problems = [
            p for p in problems
            if any(topic_filter in t.lower() for t in p["topic_tags"])
        ]

    overdue   = [p for p in problems if p["due_date"] <  today]
    due_today = [p for p in problems if p["due_date"] == today]
    upcoming  = [p for p in problems if today < p["due_date"] <= today + timedelta(days=7)]
    future    = [p for p in problems if p["due_date"] > today + timedelta(days=7)]

    # ── JSON mode (AI-agent friendly) ───────────────────────────────────────
    if do_json:
        def serialise(p):
            return {
                "label":         p["label"].strip(),
                "difficulty":    p["difficulty"],
                "last_solved":   p["last_solved"].isoformat(),
                "due_date":      p["due_date"].isoformat(),
                "days_until_due": (p["due_date"] - today).days,
                "topics":        p["topic_tags"],
                "topic_folder":  p["topic_folder"],
                "filepath":      os.path.relpath(p["filepath"], os.getcwd()),
            }

        output = {
            "generated":     today.isoformat(),
            "total_tracked": len(problems),
            "overdue":       len(overdue),
            "due_today":     len(due_today),
            "upcoming":      len(upcoming),
            "future":        len(future),
            "problems": (
                [serialise(p) for p in overdue]
                + [serialise(p) for p in due_today]
                + [serialise(p) for p in upcoming]
                + [serialise(p) for p in future]
            ),
        }
        print(json.dumps(output, indent=2))
        return

    # Cross-platform date formatting (Windows doesn't support %-d)
    import platform
    if platform.system() == 'Windows':
        date_str = today.strftime('%A, %B %#d %Y')
    else:
        date_str = today.strftime('%A, %B %-d %Y')
    
    print(f"\n{BOLD}{CYAN}Jobbernaut Sensei Revisit - {date_str}{RESET}")
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
