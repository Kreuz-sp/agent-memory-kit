# Demo memory: Alex

> A **fictional** mini library that shows what a filled-in memory looks like.
> Alex is a made-up full-stack developer; every name, company, and project here is fake.

```
examples/demo/memory/
├─ facts/           3 YAML files
├─ entries/         3 entries (core / record / record)
├─ knowledge/       1 note
├─ experience/      1 note
├─ decisions.md     1 decision
├─ commitments.md   1 open commitment
└─ open-threads.md  4 threads
```

Build the index:

```bash
python tools/build_index.py --root examples/demo/memory
```

Then open `examples/demo/memory/INDEX.md`.
