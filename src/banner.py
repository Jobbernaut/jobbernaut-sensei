import os
import sys

CYAN  = "\033[96m"
BOLD  = "\033[1m"
RESET = "\033[0m"

_BANNER = (
    f"\n{CYAN}{BOLD}"
    f"  ╔══════════════════════════════════╗\n"
    f"  ║                                  ║\n"
    f"  ║   Welcome to LeetCode Sensei     ║\n"
    f"  ║   A product of OverKill Labs     ║\n"
    f"  ║                                  ║\n"
    f"  ╚══════════════════════════════════╝"
    f"{RESET}\n"
)


def print_banner():
    try:
        marker = f"/tmp/.leetcode_sensei_{os.getsid(0)}"
        if os.path.exists(marker):
            return
        open(marker, "w").close()
    except Exception:
        return

    stream = sys.stderr if "--json" in sys.argv else sys.stdout
    print(_BANNER, file=stream)
