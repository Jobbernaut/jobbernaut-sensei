'''
Scaffold a new problem file from the template.

Usage:
    sensei new 217 contains-duplicate 1-arrays-and-hashing
    sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
    sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set --open
'''

import argparse
import os
import sys
from datetime import date

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def slug_to_folder(number: str, slug: str) -> str:
    """'217' + 'contains-duplicate' → '217-Contains-Duplicate'"""
    titled = "-".join(part.title() for part in slug.split("-"))
    return f"{number}-{titled}"


def slug_to_title(slug: str) -> str:
    """'contains-duplicate' → 'Contains Duplicate'"""
    return slug.replace("-", " ").title()


def build_content(number: str, slug: str, difficulty: str, tags: list, today: str) -> str:
    url       = f"https://leetcode.com/problems/{slug}/"
    tags_repr = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    return f'''\'\'\'
{url}
\'\'\'

last_solved     = "{today}"
revisit_in_days = 1
times_reviewed  = 0
difficulty      = "{difficulty}"
topic_tags      = {tags_repr}

class Solution:
    def solve(self) -> None:
        # TODO: implement
        pass
'''


def open_in_editor(path: str) -> None:
    import subprocess
    editor = os.environ.get("EDITOR", "")
    if editor:
        subprocess.run([editor, path])
    else:
        subprocess.run(["code", path])


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="new",
        description="Scaffold a new LeetCode problem file.",
    )
    parser.add_argument("number",   help="LeetCode problem number, e.g. 217")
    parser.add_argument("slug",     help="LeetCode slug, e.g. contains-duplicate")
    parser.add_argument("category", help="Topic folder, e.g. 1-arrays-and-hashing")
    parser.add_argument(
        "-d", "--difficulty",
        default="medium",
        choices=["easy", "medium", "hard"],
        help="Difficulty (default: medium)",
    )
    parser.add_argument(
        "-t", "--tags",
        nargs="+",
        default=["topic"],
        metavar="TAG",
        help="Topic tags, e.g. -t arrays hash-map",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the file in $EDITOR / code after creation",
    )

    args = parser.parse_args()

    folder_name = slug_to_folder(args.number, args.slug)
    problem_dir = os.path.join(os.getcwd(), "problems", args.category, folder_name)
    file_name   = f"{folder_name}.py"
    file_path   = os.path.join(problem_dir, file_name)

    if os.path.exists(file_path):
        print(f"\n  {YELLOW}Already exists:{RESET} {os.path.relpath(file_path, os.getcwd())}\n")
        sys.exit(1)

    os.makedirs(problem_dir, exist_ok=True)

    today   = date.today().isoformat()
    content = build_content(args.number, args.slug, args.difficulty, args.tags, today)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    title = slug_to_title(args.slug)
    rel   = os.path.relpath(file_path, os.getcwd())
    print(f"\n  {GREEN}[OK]{RESET}  Created  {BOLD}{CYAN}{args.number}. {title}{RESET}")
    print(f"       {GREY}{rel}{RESET}\n")

    if args.open:
        open_in_editor(file_path)


if __name__ == "__main__":
    main()
