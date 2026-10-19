# How to write a fact

`facts/` is the **single authoritative source of facts**. Other files may reference it, but must not copy it.

## One record

```yaml
records:
  - id: workplace             # unique, stable; ASCII only, never rename
    value: "Some Company · ops"  # the fact, one line
    updated_at: 2026-03-01    # when this fact was confirmed
    source: user said so      # where it came from
    confidence: high          # high / medium / low
    note: ""                  # optional: boundaries, exceptions
```

## Rules

- Once an `id` is used, don't change it. If it must change, mark the old one `superseded_by` and start a new record.
- `value` states a fact, not a judgment. "He's been tired lately" is not a fact; "he worked six night shifts in a row" is.
- `source` is mandatory. An entry without a source is a rumor.
- `confidence` is for you: when it's `low`, ask before using it.
- The top-level `last_updated` is just the file's date. **Each record's `updated_at` is what counts.**

## What doesn't belong here

- One-off conversation content → `entries/`
- How to install or fix something → `knowledge/`
- "Whether this person is reliable" → not in the library at all; record what happened
