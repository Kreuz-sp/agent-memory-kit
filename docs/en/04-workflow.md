# How to use it in a session

**English** | [简体中文](../04-workflow.md)

## At the start: read three things

```
1. memory/README.md         the rules
2. memory/INDEX.md          start with "due for review" and "where the knowledge is"
3. the latest 3–5 entries   where we left off
```

**Don't read everything.** The index is for looking things up on demand, not for reading cover to cover.
Reading it all costs half your context before any work starts.

## During: write as you go

**When you finish something, decide something, or find something out — write it down then.** One entry now is cheaper than a day's worth later.

Why you can't wait for the end:

- processes crash
- context fills up
- people shut down their machines

**"I'll write it at the end" is a precondition, and crashes don't respect preconditions.**

## At the end: three steps, in order

```
1. Add entries    write what this session should record (long only if it can serve as evidence)
2. Rebuild index  python tools/build_index.py --root memory
3. Back up        copy the whole folder somewhere else, dated
```

Order matters: **the index must reflect the entries after they were written**; the backup must capture the index after it was rebuilt.

## When to write what

| Moment | File |
|---|---|
| A plan was decided | `decisions.md` |
| You promised someone something | `commitments.md` |
| You found a pitfall | `knowledge/` or `experience/` |
| A fact changed | `facts/*.yaml` (update `updated_at`) |
| End of a day | one entry in `entries/` — not a diary |

## What if the context fills up?

**The context is cleared, not the library.**

A new session reads `README.md` + `INDEX.md` + the latest entries, and picks up.
The real risk isn't "context is full" — it's "we said it but never wrote it". That is what actually gets lost.

## Don't

- Don't write a daily summary just to fill a slot; if nothing was concluded, skip it.
- Don't paste whole conversations into `entries/`; put the point in the entry, the raw text in `assets/`.
- Don't hand-edit `INDEX.md`; it will be overwritten on the next build.
