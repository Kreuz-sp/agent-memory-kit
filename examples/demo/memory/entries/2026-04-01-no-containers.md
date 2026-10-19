---
date: 2026-04-01
tier: core
review: 2026-10-01
status: active
supersedes:
---

# Decided: Atlas will not use containers

> Time: 2026-04-01 afternoon
> Context: deployment options
> Present: Alex, me

## What happened (the part that can serve as evidence)

- He asked: "One service on one machine — is Docker worth it?"
- We laid out the debugging cost of both paths; he made the call.

## What was decided / changed

- No Docker; systemd + venv directly.
- Why: one machine, one service; the isolation buys nothing, debugging costs more.
- Boundary: re-evaluate if a second machine or multiple environments appear.

## Still open

## Source

Exact words: "Not yet — wait until we actually need it."
