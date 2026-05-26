<div align="center">
  <img src="https://raw.githubusercontent.com/jobbernaut/jobbernaut-sensei/main/logo.jpeg" alt="Jobbernaut Sensei Logo" width="180"/>
</div>

# Jobbernaut Sensei

> Navigate the vast space of the job market.

**Jobbernaut** is a cloud-native, event-driven open core intelligence platform designed to automate the most tedious parts of the job search: data extraction, resume tailoring, and document management. It transforms a scattered manual process into a streamlined, intelligent pipeline.

**Jobbernaut Sensei** is the LeetCode practice & spaced-repetition CLI tool within the ecosystem — helping you sharpen your algorithmic skills with a structured review system.

---

## 🚀 The Ecosystem at a Glance

The ecosystem is composed of 5 decoupled micro-repositories working in harmony, plus this CLI tool.

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

- **Spaced Repetition:** Never forget a solution — the CLI schedules reviews based on your difficulty rating.
- **One-Command Scaffolding:** Create new problem files with pre-filled metadata in seconds.
- **ATS-Ready Tracking:** Export your progress to CSV or Markdown.
- **Context-Aware Fuzzy Matching:** Open or mark problems by number, slug, or title words.
- **Zsh Completions:** Tab-complete problem names and categories.

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

## 📖 Commands

### `sensei revisit` — daily review runner

```bash
sensei revisit
```

**Example output:**
```
📅  Jobbernaut Sensei Revisit — Tuesday, May 26 2026

🟢  UPCOMING (7 days)
──────────────────────────────────────────────────────────────────────────
  in 3d          [hard  ]   124. Binary Tree Maximum Path Sum      (trees)
  in 4d          [medium]   853. Car Fleet                         (stack, monotonic-stack)

──────────────────────────────────────────────────────────────────────────
  0 problem(s) need attention today.  Total tracked: 22
```

| Flag | What it does |
|------|-------------|
| _(none)_ | Overdue + due today + upcoming 7 days |
| `--all` | Everything, including far-future problems |
| `--topic arrays` | Filter by topic tag (partial match) |
| `--export` | Export all problems to `export.csv` |
| `--export-md` | Export all problems to `export.md` |

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

### `sensei open` — open a problem

```bash
sensei open 217
sensei open contains-duplicate
sensei open 217 --no-browser   # editor only
```

Accepts problem number, slug, or title words — same fuzzy matching as `mark`.

### `sensei mark` — mark a problem as reviewed

```bash
sensei mark 217
sensei mark contains-duplicate
```

Updates `last_solved` to today and sets `revisit_in_days` based on your rating.

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