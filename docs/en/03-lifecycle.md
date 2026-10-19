# Lifecycle: memory expires too

**English** | [简体中文](../03-lifecycle.md)

## The problem

Most memory systems solve "how to store". Few solve "when to review, demote, or drop".

The result: entries pile up, the important ones drown, and stale claims keep getting quoted.

## Three fields

The header of every entry:

```yaml
---
date: 2026-01-01
tier: core | record | raw
review: 2026-07-01      # review date; raw may leave it empty
status: active | superseded | archived
supersedes:             # optional: filename of the entry this replaces
---
```

## Three tiers

| Tier | Holds | Rule |
|---|---|---|
| `core` | facts, decisions, commitments, open threads | never lost, never vague; **must have a review date** |
| `record` | what happened on a day | write it, don't chase completeness; review defaults to 6 months |
| `raw` | original details, back-and-forth | can be forgotten; stays out of the index body |

## Three actions

### Promote

A `record` that keeps being referenced (say ≥3 times) is no longer "that day" — it is "always true".

→ A human promotes it to `core`, or moves the fact into `facts/`.

### Demote

A `core` entry past its review date and no longer referenced.

→ Mark it `archived`. **Don't delete it**: it stays searchable, it just stops entering context.

### Conflict

A new fact contradicts an old one.

→ The new entry sets `supersedes: old-entry`; the old entry gets `status: superseded`.
**Don't edit the old entry** — if you edit it, you can't see what you used to believe.

## Tools report, they don't act

`build_index.py` lists at the top of `INDEX.md`:

- entries past their review date
- `core` entries without a review date

It **never** promotes, demotes, or deletes by itself.
All three require judgment, and judgment belongs to a human.

## Start minimal

Use `record` only at first, skip `review`.
Add the field when browsing becomes painful — **driven by pain, not by discipline**.
