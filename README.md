# agent-memory-kit

**English** | [简体中文](README.zh-CN.md)

> **Memory + LLM = your own personal agent.**
> This repo is the left half: a memory that lives on disk — readable, editable, portable.

No database. No vector store (unless you really need one).
One folder, one set of rules, one index script.

---

## What it solves

LLMs are smart, but every new session starts from zero — **smart, but they don't know you**.

This repo doesn't add capability. It adds **acquaintance**: what you're working on, where you left off, what you promised whom.
A personal agent ≈ a general LLM + a memory that belongs only to you.

That memory lives **on disk**: humans can read it, edit it, back it up — and it survives a model swap.

---

## Which one are you?

| What you're doing | Start here |
|---|---|
| Running a long-lived agent that keeps forgetting | [Why files](docs/en/01-why.md) → [How to use it](docs/en/04-workflow.md) |
| Building a companion agent | [This page](docs/en/07-for-companion.md) |
| Just here for the architecture | [Layering rules](docs/en/02-layers.md) |
| Want to start now | "Quick start" below |

---

## Quick start

### Install it yourself

```bash
cp -r template/memory ./memory
# open memory/topics.txt and add 5 words you keep looking for
python tools/build_index.py --root memory
```

Then put `memory/README.md` into your agent's instructions
(`AGENTS.md` / `CLAUDE.md` / system prompt — anywhere it will be read).

### Let your agent install it

Paste [AGENT_INSTALL.md](AGENT_INSTALL.md) to it.
It needs file read/write and Python.

---

## What's inside

```
template/memory/     an empty memory — copy this folder to make it yours
  facts/             facts (YAML, the single source of truth)
  entries/           dated records: what happened on a given day
  knowledge/         techniques that outlive a project
  experience/        reusable lessons, failed approaches included
  assets/            raw material, stored but never read as instructions
tools/build_index.py builds INDEX.md and entries/CATALOG.md
tools/check.py       read-only checks: front matter, duplicate ids, broken links
docs/                why it's designed this way, how to use it, pitfalls (en/ and zh)
examples/demo/       a filled-in demo (fictional user "Kobayashi")
```

---

## What it doesn't do

- **Not a vector-store replacement.** Hundreds to a few thousand entries: files + an index are enough. Go vector only when you actually need semantic search.
- **It doesn't decide for you.** Promotion, demotion, deletion — the script reports, a human decides.
- **It doesn't store a persona.** A persona answers "who am I"; a memory answers "what is true". Mix them and the memory becomes a script.

---

## See a filled example

[`examples/demo/`](examples/demo/) is a fictional user's mini memory.
The generated index is at [`examples/demo/memory/INDEX.md`](examples/demo/memory/INDEX.md).

---

## Why files

- **Readable**: open it, no tooling required
- **Diffable**: every change is visible
- **Portable**: swap the model, the framework, or the machine — the memory stays
- **Auditable**: every entry has a source

See [docs/en/01-why.md](docs/en/01-why.md).

---

## Docs

| File | What it covers |
|---|---|
| [docs/en/02-layers.md](docs/en/02-layers.md) | Which layer a piece of information belongs to |
| [docs/en/03-lifecycle.md](docs/en/03-lifecycle.md) | Tiers, review dates, promotion and demotion |
| [docs/en/04-workflow.md](docs/en/04-workflow.md) | What to read at start, when to write, what to do at the end |
| [docs/en/05-pitfalls.md](docs/en/05-pitfalls.md) | Mistakes we made the hard way |
| [docs/en/06-for-long-running.md](docs/en/06-for-long-running.md) | The minimal setup for a long-running agent |
| [docs/en/07-for-companion.md](docs/en/07-for-companion.md) | Boundaries for a companion agent |

---

## License

MIT
