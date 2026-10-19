Status: active
Updated: 2026-03-12

# systemd 服务写文件时的权限排查

## 适用场景

服务以非 root 用户跑，需要写某个目录。

## 做法

1. `systemctl show <svc> -p User` 看跑在哪个用户。
2. `ls -ld <目录>` 看属主和权限。
3. `sudo -u <user> touch <目录>/test` 复现。
4. 改属主或 ACL，不要直接 777。

## 坑

- 只看进程属主不够：父目录没有 `x` 权限也进不去。
- 日志里的 `Permission denied` 不一定是文件权限，可能是 SELinux（先 `getenforce`）。

## 出处

2026-03-12 实测。
