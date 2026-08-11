# Contributing to LeetCode Sensei

## Project Layout

```
leetcode-sensei/
├── src/                    # All CLI source code
│   ├── sensei.py           # Entry point — command routing
│   ├── new.py              # sensei new
│   ├── mark.py             # sensei mark
│   ├── hint.py             # sensei hint
│   ├── lopen.py            # sensei open
│   ├── revisit.py          # sensei revisit + collect_problems()
│   ├── rebalance.py        # sensei rebalance
│   ├── progress.py         # sensei progress
│   └── utils.py            # Shared helpers (parse_metadata, find_match, …)
├── tests/
│   ├── conftest.py         # Shared fixtures (temp_workspace, sample_problem_file, …)
│   ├── test_utils.py       # Unit tests for utils.py
│   ├── test_commands.py    # Integration tests (subprocess)
│   └── test_commands_direct.py  # Direct-call tests (higher coverage)
├── problems/               # User's tracked LeetCode solutions (not shipped)
├── pyproject.toml          # Build config, test settings, dependencies
├── AGENTS.md               # AI coaching protocol — read before touching SRS logic
├── ROADMAP.md              # Planned features
└── CONTRIBUTING.md         # This file
```

## Setting Up

```bash
git clone https://github.com/Overkill-Labs/leetcode-sensei.git
cd leetcode-sensei
pip install -e ".[test]"
```

That's it. No Docker, no database, no config files.

Verify the install:

```bash
sensei --help
pytest
```

## Architecture

Every command is a self-contained module in `src/`. `sensei.py` routes by command name and strips its own argv before delegating:

```python
sys.argv = [sys.argv[0]] + sys.argv[2:]   # remove "sensei" and the subcommand
new.main()                                 # receives clean argv
```

Commands that don't need argv stripping (status, show, progress) are handled directly in `sensei.py` before the strip line.

**`collect_problems(root)`** in `revisit.py` is the central data source. It walks `problems/`, parses metadata from every `.py` file via `parse_metadata()`, and returns a sorted list of dicts. Most commands build on top of this — avoid duplicating that logic.

Problem files are plain Python. The metadata block is a set of module-level assignments that `parse_metadata()` reads with `ast.walk`:

```python
last_solved     = "2026-08-10"
revisit_in_days = 7
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]
```

## Adding a New Command

1. Create `src/<command>.py` with a `main()` function
2. Add `import <command>` to `src/sensei.py`
3. Add a routing branch in `sensei.main()`:
   - Before the `sys.argv` strip if the command doesn't need subcommand args
   - After the strip (in the `if cmd == ...` chain) if it does
4. Add it to `pyproject.toml` under `py-modules`
5. Add it to the help text in `sensei.main()`
6. Write tests in `tests/test_commands_direct.py`

## Running Tests

```bash
pytest                          # full suite with coverage
pytest tests/test_commands_direct.py -v   # just the direct tests
pytest -k "progress"            # filter by name
```

Coverage target: **>85%** overall. New modules should hit >90%.

## Writing Tests

Use `test_commands_direct.py` for new tests — it calls `main()` functions directly, which gives better coverage than subprocess calls.

Fixtures are in `conftest.py`:

- `temp_workspace` — empty temp dir, cwd changed to it
- `initialized_workspace` — temp dir with `problems/` created
- `sample_problem_file` — single valid problem file
- `multiple_problems` — three problems with different due states (overdue, due today, future)

For commands that hit external services (LeetCode GraphQL, browser), mock them:

```python
with patch("new.fetch_leetcode_metadata", return_value={...}):
    new.main()
```

## Commit Guidelines

This repo uses **Conventional Commits**. Every commit message must follow:

```
<type>(<scope>): <short description>
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `chore` | Maintenance (deps, config, build, non-feature code) |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code restructure with no behavior change |
| `perf` | Performance improvement |

### Scopes

Use the area of the codebase affected:

| Scope | Covers |
|-------|--------|
| `cli` | New or changed command |
| `srs` | SRS algorithm logic (intervals, progression gate, load smoothing) |
| `build` | `pyproject.toml`, packaging |
| `agents` | `AGENTS.md` coaching protocol |
| `docs` | `README.md`, `ROADMAP.md`, `CONTRIBUTING.md` |

### Examples

```
feat(cli): add sensei progress dashboard
fix(srs): cap progression gate at correct tier boundary
chore(build): add progress to py-modules
test: add coverage for url mode in sensei new
docs(agents): document sensei new url form
refactor(cli): extract _scaffold() from new.main()
```

### Rules

- Subject line: lowercase, no period, ≤72 characters
- Use imperative mood: "add" not "added", "fix" not "fixes"
- One logical change per commit — if you need "and" in the subject, split it
- No `Co-Authored-By` trailers

## Releases

Releases are cut by pushing a version tag. The CI pipeline picks it up and publishes to PyPI automatically.

```bash
# 1. Bump version in pyproject.toml
# 2. Commit
git add pyproject.toml
git commit -m "chore(build): bump version to X.Y.Z"

# 3. Tag and push
git tag -a vX.Y.Z -m "vX.Y.Z"
git push
git push origin vX.Y.Z
```

Version scheme: `MAJOR.MINOR.PATCH`

- `PATCH` — bug fixes, doc updates, test additions
- `MINOR` — new commands or features, backward-compatible changes
- `MAJOR` — breaking changes to CLI interface or problem file format

## Changing SRS Logic

The SRS algorithm (intervals, progression gate, load smoothing) is intentionally conservative. Changes here affect real review schedules.

Before touching `mark.py` or any interval logic:

1. Read the relevant sections of `AGENTS.md` — the coaching agent depends on this behavior being well-defined
2. Update the rating table in `AGENTS.md` if intervals change
3. Update `tests/test_commands.py::TestComputeInterval` and `TestProgressionGate`
4. Note the change in the commit body with a reason

## Problem File Format

Do not change the metadata field names or their order without updating `utils.parse_metadata()` and all tests that create fixture files. The format is the stable public interface between the CLI and user data.

Current required fields: `last_solved`, `revisit_in_days`, `difficulty`, `topic_tags`
Optional: `times_reviewed` (defaults to 0 if absent)
