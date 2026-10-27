# bluh

A Claude Code setup for agents that remember what they learn, check each other's work,
and improve between sessions. Based on Anthropic's "context engineering" talk at AI DevCon
(memory as files, production guardrails, out-of-band "dreaming"), plus a role-separated
agent team.

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Memory protocol and team rules, loaded every session |
| `memory/MEMORY.md` | Index of memory files (imported into `CLAUDE.md`) |
| `memory/org/` | Human-curated, read-only to agents |
| `memory/notes/ledger.md` | Append-only log of every attempt and its verdict |
| `memory/scratch/` | Per-session working notes, not committed |
| `memory/proposals/` | `/dream` output, waiting for a human decision |
| `scripts/memwrite.py` | The only way agents write memory: hash-checked, permission-tiered, logged to `memory/CHANGELOG.md` |
| `scripts/collect_transcripts.py` | Turns recent Claude Code sessions into digests for `/dream` |
| `.claude/agents/` | `worker` (does), `skeptic` (attacks), `librarian` (searches memory), `dream-analyst` |
| `.claude/skills/dream/` | The `/dream` command |
| `.claude/settings.json` | Blocks direct edits to `memory/org/` and `memory/notes/` |

## How it maps to the talk

- **Memory as files:** plain markdown that agents search with grep. Only the index loads up front.
- **Versioning:** git, plus `memory/CHANGELOG.md` recording who changed what and why.
- **Concurrency:** `memwrite.py write --expect <hash>` refuses the write if the file changed since it was read.
- **Permissions:** `org/` is read-only to agents, `notes/` is written only through the script, `scratch/` is free.
- **Dreaming:** `/dream` reads recent sessions in parallel, keeps patterns seen in at least 2 sessions,
  and writes proposals with evidence. A human accepts or rejects each one.

## Use it

1. Edit `memory/org/principles.md` with what this project is about.
2. Work normally. Claude reads memory first, logs to the ledger last, and sends results to `skeptic`.
3. Run `/dream` weekly, then tick accept or reject in `memory/proposals/<date>.md`.

To use this in another repo, copy `CLAUDE.md`, `.claude/`, `memory/` and `scripts/` into it.

The settings block the edit tools. A shell command could still write to these files directly,
so the settings are a guardrail, not a sandbox.
