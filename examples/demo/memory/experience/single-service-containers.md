Status: active
Updated: 2026-04-01

# For a single small service, containers may not save effort

## Symptom

Started with Docker; ended up installing a daemon for one container, and had to learn another layer of logs and networking.

## Cause

The benefits of isolation are nearly zero on one machine with one service; when things break, there is one more layer to debug.

## Next time

Ask three questions: how many machines? how many services? how many environments? If all are small, run it directly.

## Don't repeat

Don't default to containers just because "everyone uses containers".
