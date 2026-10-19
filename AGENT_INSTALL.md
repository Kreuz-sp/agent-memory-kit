# Let your agent install it

**English** | [简体中文](AGENT_INSTALL.zh-CN.md)

> This file is written for the agent — and for the human who copies it.

## Requirements

The agent needs: **file read/write**, **Python**, and the path to this repo.

## Copy this

```
I want to add a file-based memory to this project.

1. Read <repo>/README.md and <repo>/docs/01-why.md first.
2. Copy <repo>/template/memory to <project>/memory.
3. Using the rules in <repo>/docs/02-layers.md, fill in what you can confirm.
   Leave the rest empty with a TODO. Do not invent.
4. Run python <repo>/tools/build_index.py --root <project>/memory.
5. Report back: which files you read, what you filled in, what you left empty,
   and whether the index was generated.
```

## For the human: check it once

- [ ] Open `memory/facts/*.yaml` — every record has a `source`; delete the ones without
- [ ] Open `memory/entries/` — the first entry contains nothing invented
- [ ] `memory/INDEX.md` starts with an empty "due for review" section
- [ ] `memory/README.md` is in your agent's instructions

## Why step 3 says "do not invent"

Most agents will "helpfully" fill the blanks: guess your city, infer your job from a folder name.

Nobody notices, and the memory is now dirty. **Empty is better than invented**: empty is a TODO, invented is debt.

## After it's installed

- Words you keep searching for → add to `memory/topics.txt`
- The same pitfall twice → write it to `memory/experience/`
- New machine or project → update `memory/facts/04_environment.yaml`

Re-run the index after any change.
