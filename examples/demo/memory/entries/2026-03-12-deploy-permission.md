---
date: 2026-03-12
tier: record
review: 2026-09-12
status: active
supersedes:
---

# Deployment blocked by systemd permissions

> Time: 2026-03-12 evening
> Context: first production deploy of Atlas
> Present: Alex, me

## What happened (the part that can serve as evidence)

- The service ran as `User=app`, but `/var/lib/atlas` was owned by root, so it couldn't write.
- The error was `Permission denied`; it took half an hour to realize it was directory permissions, not SELinux.

## What was decided / changed

- From now on, run `ls -ld` on the directory before deploying.

## Still open

- [ ] Put this into the deployment doc (promised to Zhou)

## Source

Terminal output, `journalctl -u atlas`.
