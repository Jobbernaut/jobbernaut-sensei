import sys
import mark
import new
import lopen
import revisit

def main():
    if len(sys.argv) < 2:
        print("\n  Jobbernaut Sensei CLI")
        print("  Usage: sensei <command> [args]\n")
        print("  Available commands:")
        print("    revisit  - Run daily review")
        print("    new      - Scaffold a new problem")
        print("    open     - Open a problem in editor/browser")
        print("    mark     - Mark a problem as solved\n")
        sys.exit(1)

    cmd = sys.argv[1]
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
