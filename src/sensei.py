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
    # Create a placeholder so the directory isn't empty
    placeholder = os.path.join(problems_dir, ".gitkeep")
    with open(placeholder, "w") as f:
        f.write("")

    print(f"\n  ✓  Initialized empty problems/ directory at:")
    print(f"     {problems_dir}\n")
    print(f"     Run 'sensei new' to scaffold your first problem!\n")


def main():
    if len(sys.argv) < 2:
        print("\n  Jobbernaut Sensei CLI")
        print("  Usage: sensei <command> [args]\n")
        print("  Available commands:")
        print("    init     - Initialize the problems/ directory")
        print("    revisit  - Run daily review")
        print("    new      - Scaffold a new problem")
        print("    open     - Open a problem in editor/browser")
        print("    mark     - Mark a problem as solved\n")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
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