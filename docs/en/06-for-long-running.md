# Minimal setup for a long-running agent

**English** | [简体中文](../06-for-long-running.md)

> This assumes: you have an agent you'll keep using (coding, research, daily work),
> and every new session feels like amnesia.

## Step one: only three things

```
memory/
├─ entries/       what happened, day by day
├─ topics.txt     words you keep looking for
└─ README.md      the rules (copy from template)
```

No `facts/`, no `review`, no lifecycle.

Write down "what happened today" first. Get the index running.

## Step two: add layers when these signals appear

| You start thinking | Add |
|---|---|
| "What did we say about this last time?" | `facts/*.yaml` |
| The same pitfall, second time | `experience/` |
| Knowledge you reuse across projects | `knowledge/` |
| Promises keep slipping | `commitments.md` |
| Too many entries to browse | `tier` + `review` |

**Add when it hurts. Not before.**

## How to make the agent actually read it

Put this in its instructions (`AGENTS.md` / `CLAUDE.md` / system prompt):

```
At the start of every new session:
1. Read memory/README.md.
2. Read the top of memory/INDEX.md (due for review, where the knowledge is).
3. Read the latest 3–5 entries/.
4. When you need details, look them up via INDEX.md. Do not answer from impression.

After finishing something, deciding something, or finding something out:
write it to memory/entries/ right away. Don't wait until the end.
```

**The key is rule 4**: make it look things up when unsure, instead of guessing.
"I checked" and "I think it's probably" are different things.

## Common mistakes

- **Daily summaries**: skip days with no conclusions; they're noise.
- **Reading the whole library**: three things at the start is enough; reading everything eats context.
- **Mistaking context for memory**: context is a workbench; clearing it isn't loss. Saying it without writing it is loss.
- **Writing without reading**: if nobody reads it, it wasn't written. The index is the entry point.

## Check once a week

- [ ] Three blank days in a row in `entries/`? The habit didn't take.
- [ ] Is `INDEX.md` current? Did you rebuild after changing the library?
- [ ] Any TODOs that have been TODOs for weeks? Empty beats invented — but not forever.
