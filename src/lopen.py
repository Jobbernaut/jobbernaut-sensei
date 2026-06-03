'''
Open a problem's LeetCode URL in the browser.

Usage:
    sensei open 217
    sensei open contains-duplicate
    sensei open "valid anagram"
'''

import os
import subprocess
import sys

from utils import find_solution_files, find_match, extract_url

# ── ANSI colours ──────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def open_in_browser(url: str) -> None:
    if sys.platform == "darwin":
        subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif sys.platform == "win32":
        subprocess.Popen(["cmd", "/c", "start", "", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        print(f"\n  {CYAN}Usage: sensei open <number | slug | title words>{RESET}\n")
        sys.exit(1)

    query     = " ".join(argv)
    prob_root = os.path.join(os.getcwd(), "problems")
    
    if not os.path.isdir(prob_root):
        print(f"\n  {GREY}problems/ directory not found. Run 'sensei init' first.{RESET}\n")
        sys.exit(1)
    
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
