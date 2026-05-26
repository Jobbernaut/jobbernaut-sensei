<div align="center">
  <img src="https://raw.githubusercontent.com/jobbernaut/jobbernaut-sensei/main/logo.jpeg" alt="Jobbernaut Sensei Logo" width="180"/>
</div>

# Jobbernaut Sensei

> Navigate the vast space of the job market.

**Jobbernaut** is a cloud-native, event-driven open core intelligence platform designed to automate the most tedious parts of the job search: data extraction, resume tailoring, and document management.

**Jobbernaut Sensei** is the LeetCode practice & spaced-repetition CLI tool within the ecosystem — helping you sharpen your algorithmic skills with a structured review system. It's also an **AI-agent-friendly API**: every command outputs clean JSON, ready for agents like Cline, Claude Code, or ChatGPT to consume.

---

## 🚀 The Ecosystem at a Glance

| Repository | Role | Technology Stack |
|---|---|---|
| `jobbernaut-infra` | Foundation | Terraform (HCL), AWS IAM, S3, DynamoDB |
| `jobbernaut-tabs` | Frontend | Next.js, React, Tailwind CSS |
| `jobbernaut-backend` | Control | Python (AWS Lambda), Boto3, Pydantic |
| `jobbernaut-tailor` | Intelligence | Docker, Python, LangChain (AI), TeXLive (LaTeX) |
| `jobbernaut-extract` | Collection | Chrome Extension (Manifest V3), JavaScript |
| **`jobbernaut-sensei`** | **CLI Practice** | **Python (setuptools)** |

📘 **Documentation:** For deep dives into the architecture, data flows, and setup guides, visit [jobbernaut-docs](https://github.com/jobbernaut/jobbernaut-docs).

---

## ⚡️ Key Features

- **Spaced Repetition:** Never forget a solution — schedules reviews based on your difficulty rating.
- **One-Command Scaffolding:** Create new problem files with pre-filled metadata in seconds.
- **ATS-Ready Tracking:** Export your progress to CSV or Markdown.
- **Context-Aware Fuzzy Matching:** Open or mark problems by number, slug, or title words.
- **Zsh Completions:** Tab-complete problem names and categories.
- **🤖 AI-Agent Friendly:** Every command outputs clean JSON — `sensei revisit --json`, `sensei status`, `sensei show <problem>`.
- **Non-Interactive Marking:** `sensei mark 217 --rating e` — perfect for agent-driven tutoring sessions.

---

## 📦 Setup

```bash
pip install jobbernaut-sensei
```

Initialize a `problems/` directory:

```bash
sensei init
```

---

## 🔁 Daily Loop

### 1. Morning — see what's due
```bash
sensei revisit
```

### 2. Start a problem — scaffold it
```bash
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
```

### 3. Open a problem — jump back in
```bash
sensei open 217
```

### 4. After solving — mark it
```bash
sensei mark 217
```

You'll be prompted with one question:

```
  How did it go?

    [e]  easy      → 90 days
    [g]  good      → 30 days
    [h]  hard      → 7 days
    [s]  struggled → 3 days
```

Press one key. `last_solved` and `revisit_in_days` are updated automatically.

---

## 📖 Command Reference

### `sensei revisit` — daily review runner

```bash
sensei revisit
sensei revisit --all
sensei revisit --topic arrays
sensei revisit --json            # AI-agent friendly JSON output
sensei revisit --export
sensei revisit --export-md
```

**Colored terminal output:**
```
📅  Jobbernaut Sensei Revisit — Tuesday, May 26 2026

🟢  UPCOMING (7 days)
──────────────────────────────────────────────────────────────────────────
  in 3d          [hard  ]   124. Binary Tree Maximum Path Sum      (trees)
  in 4d          [medium]   853. Car Fleet                         (stack, monotonic-stack)

──────────────────────────────────────────────────────────────────────────
  0 problem(s) need attention today.  Total tracked: 22
```

**JSON output** (`--json`):
```json
{
  "generated": "2026-05-26",
  "total_tracked": 22,
  "problems": [
    {
      "label": "124. Binary Tree Maximum Path Sum",
      "difficulty": "hard",
      "last_solved": "2026-05-26",
      "due_date": "2026-05-29",
      "days_until_due": 3,
      "topics": ["trees"],
      "topic_folder": "7-trees",
      "filepath": "problems/7-trees/..."
    }
  ]
}
```

| Flag | What it does |
|------|-------------|
| _(none)_ | Overdue + due today + upcoming 7 days |
| `--all` | Everything, including far-future problems |
| `--topic arrays` | Filter by topic tag (partial match) |
| `--json` | Structured JSON output for AI agents |
| `--export` | Export all problems to `export.csv` |
| `--export-md` | Export all problems to `export.md` |

---

### `sensei status` — quick summary

```bash
sensei status
```

Returns a lightweight JSON snapshot of your tracker state:

```json
{
  "total": 22,
  "overdue": 0,
  "due_today": 0,
  "upcoming": 4,
  "problems": [
    { "label": "124. Binary Tree Maximum Path Sum", "difficulty": "hard", ... }
  ]
}
```

Ideal for AI agents to quickly assess a user's practice state before a tutoring session.

---

### `sensei show <problem>` — inspect a problem

```bash
sensei show 217
sensei show contains-duplicate
```

Returns **metadata + your saved solution code** as JSON:

```json
{
  "label": "217. Contains Duplicate",
  "number": "217",
  "title": "Contains Duplicate",
  "filepath": "problems/1-arrays-and-hashing/...",
  "metadata": {
    "last_solved": "2026-05-14",
    "revisit_in_days": 90,
    "difficulty": "easy",
    "topic_tags": ["arrays", "hashing"],
    "due_date": "2026-08-12"
  },
  "solution": "class Solution:\n    def containsDuplicate(..."
}
```

Use this to fetch a problem for analysis, code review, or tutoring.

---

### `sensei new` — scaffold a new problem

```bash
sensei new 217 contains-duplicate 1-arrays-and-hashing
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set --open
```

| Argument | Description |
|----------|-------------|
| `number` | LeetCode problem number |
| `slug` | LeetCode URL slug, e.g. `contains-duplicate` |
| `category` | Topic folder, e.g. `1-arrays-and-hashing` |
| `-d / --difficulty` | `easy` / `medium` / `hard` (default: `medium`) |
| `-t / --tags` | One or more topic tags |
| `--open` | Open the file in `$EDITOR` / `code` immediately |

---

### `sensei open` — open a problem

```bash
sensei open 217
sensei open contains-duplicate
sensei open 217 --no-browser   # editor only
```

Accepts problem number, slug, or title words — same fuzzy matching as `mark`.

---

### `sensei mark` — mark a problem as reviewed

```bash
sensei mark 217
sensei mark contains-duplicate
sensei mark 217 --rating e     # non-interactive (AI-agent friendly)
```

| Flag | What it does |
|------|-------------|
| _(none)_ | Interactive prompt for difficulty rating |
| `--rating e` | Mark as easy (90 days until next review) |
| `--rating g` | Mark as good (30 days) |
| `--rating h` | Mark as hard (7 days) |
| `--rating s` | Mark as struggled (3 days) |

The `--rating` flag skips the interactive prompt — perfect for AI agents tutoring a user and updating the schedule automatically.

---

## 🤖 AI-Agent Integration

See **[`AGENTS.md`](AGENTS.md)** — a complete tool-calling guide for integrating `sensei` into any AI coding agent's toolset.

Quick reference:

```bash
sensei status                     # Assess user's practice state
sensei revisit --json             # Get full review data
sensei show <problem>             # Inspect problem + solution
sensei mark <problem> --rating g  # Update schedule after tutoring
```

---

## 🔧 Zsh Shell Completions

Tab-complete `sensei` subcommands, problem numbers/names, and category names.

**Add to `~/.zshrc`:**
```zsh
fpath=(/path/to/jobbernaut-sensei/src/completions $fpath)
autoload -Uz compinit && compinit
```

Then reload: `source ~/.zshrc`

---

## ⚖️ License

Unless otherwise noted, all repositories within the Jobbernaut organization are licensed under the **PolyForm Noncommercial License 1.0.0**.

If a repository lacks a specific LICENSE file, the license located at [Jobbernaut/LICENSE.md](https://github.com/jobbernaut/jobbernaut-sensei/blob/main/LICENSE) applies by default.

You are free to use, modify, and learn from this code for **personal or non-commercial** purposes.