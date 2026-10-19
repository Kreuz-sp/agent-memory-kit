Status: active
Updated: 2026-03-12

# Debugging systemd service file permissions

## When it applies

A service runs as a non-root user and needs to write to a directory.

## How

1. `systemctl show <svc> -p User` to see which user it runs as.
2. `ls -ld <dir>` to check ownership and permissions.
3. `sudo -u <user> touch <dir>/test` to reproduce.
4. Fix ownership or ACLs; don't use 777.

## Pitfalls

- Checking the process owner is not enough: missing `x` on a parent directory also blocks access.
- `Permission denied` in logs is not always file permissions; it can be SELinux (check `getenforce`).

## Source

Tested 2026-03-12.
