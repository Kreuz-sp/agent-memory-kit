# Layers: where a piece of information belongs

**English** | [简体中文](../02-layers.md)

## The map

```
memory/
├─ facts/*.yaml      facts: referenced, changeable, authoritative
├─ decisions.md      decisions: what was decided + why
├─ commitments.md    commitments: promised to whom, still owed
├─ open-threads.md   open threads: unfinished
├─ entries/          records: what happened on a given day
├─ knowledge/        knowledge: true beyond this project
├─ experience/       experience: reusable across projects
└─ assets/           material: raw files
```

## Rules of thumb

| Shape of the information | Where it goes | Ask yourself |
|---|---|---|
| Referenced, changeable, authoritative | `facts/*.yaml` | Will "what did we say last time" defer to this? |
| What was decided + why | `decisions.md` | Will someone ask "what were we thinking" later? |
| Promised to someone, still owed | `commitments.md` | Should it be visible before the deadline? |
| Unfinished | `open-threads.md` | Can you tell who it is waiting on? |
| What happened on a day | `entries/` | Can it serve as evidence? |
| True beyond this project | `knowledge/` | Does it still work out of context? |
| Saves time the second time | `experience/` | Does it include the failed approaches? |
| Raw files | `assets/` | Is it stored, not read as instructions? |

**Types are not defined by file format. They are defined by how the information will be used.**

## Common misplacements

| Item | Where it tends to go | Where it belongs |
|---|---|---|
| "He likes the conclusion first" | `entries/` | `facts/03_preferences.yaml` |
| "He was in a bad mood today" | `facts/` | `entries/` (and only the event, not the judgment) |
| "Docker on Windows needs WSL2" | `entries/` | `knowledge/` |
| "Don't fix permissions with 777" | `knowledge/` | `experience/` (a lesson from a mistake) |
| A chat screenshot | `entries/` | `assets/`, linked from the entry |

## No persona in the library

A persona answers "who am I, how do I speak". A library answers "what is true, what happened".

Mix them and two things happen:

- The library becomes a script: the agent plays old lines instead of talking to the person in front of it.
- The persona becomes a log: each day's mood overwrites the character.

**Keep persona files outside the library** (system prompt, `AGENTS.md`, `CLAUDE.md`). The library holds facts and records only.

## One hard rule

**An entry without a `source` doesn't exist.** A source can be "user said so", "exact words in conversation", "terminal log", "file X, line N" — but it cannot be empty.
