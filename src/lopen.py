'''
Open a problem's LeetCode URL in the browser.

Usage:
    sensei open 217
    sensei open contains-duplicate
    sensei open "valid anagram"
'''

import os
import re
import subprocess
import sys

# ── ANSI colours ──────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "docs"}


def find_solution_files(root: str) -> list:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(dirpath, filename))
    return files


def normalise(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_match(query: str, files: list):
    q = normalise(query)

    if q.isdigit():
        for f in files:
            stem  = os.path.splitext(os.path.basename(f))[0]
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
        candidates.sort(
            key=lambda f: normalise(os.path.splitext(os.path.basename(f))[0]).index(q)
        )
        return candidates[0]
    return None


def extract_url(path: str):
    """Return the first leetcode.com/problems URL found in the file, or None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r"https://leetcode\.com/problems/[^\s'\"]+", line)
                if m:
                    url = m.group(0).rstrip("/") + "/"
                    if "PROBLEM-SLUG" not in url:
                        return url
    except OSError:
        pass
    return None


def open_in_browser(url: str) -> None:
    if sys.platform == "darwin":
        subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        print(f"\n  {CYAN}Usage: sensei open <number | slug | title words>{RESET}\n")
        sys.exit(1)

    query     = " ".join(argv)
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    prob_root = os.path.join(repo_root, "problems")
    files     = find_solution_files(prob_root)
    match     = find_match(query, files)

    if match is None:
        print(f"\n  {GREY}No match found for: \"{query}\"{RESET}\n")
        sys.exit(1)

    url = extract_url(match)
    if url is None:
        print(f"\n  {GREY}No LeetCode URL found for: \"{query}\"{RESET}\n")
        sys.exit(1)

    print(f"\n  {CYAN}Opening {url}{RESET}\n")
    open_in_browser(url)


if __name__ == "__main__":
    main()