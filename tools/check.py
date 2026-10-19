"""只读自检：front-matter、重复 id、knowledge/experience 的元数据、断链。

用法:
    python check.py --root memory

退出码:
    0 = 没有警告
    1 = 有警告（仍然不改任何文件）
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

TIERS = {"core", "record", "raw"}
STATUSES = {"active", "superseded", "archived"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
KV_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", re.M)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def front_matter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    data = {}
    for key, value in KV_RE.findall(m.group(1)):
        value = value.strip().strip('"').strip("'")
        if "  #" in value:
            value = value.split("  #", 1)[0].strip()
        data[key.lower()] = value
    return data


def check(root: Path) -> list[str]:
    warnings: list[str] = []

    # 1) facts 里的 id 不许重复
    seen: dict[str, list[str]] = {}
    for path in sorted((root / "facts").glob("*.yaml")):
        for ident in re.findall(r"^\s*-\s*id:\s*(\S+)", read_text(path), re.M):
            seen.setdefault(ident, []).append(path.name)
    for ident, files in seen.items():
        if len(files) > 1:
            warnings.append(f"重复的 id：{ident}（{', '.join(files)}）")

    # 2) knowledge / experience 必须有 Status 和 Updated
    for folder in ("knowledge", "experience"):
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name.startswith("_"):
                continue
            text = read_text(path)
            if not re.search(r"^Status:\s*(active|deprecated)\b", text, re.M):
                warnings.append(f"{folder}/{path.name}：缺少或无效的 Status")
            if not re.search(r"^Updated:\s*\d{4}-\d{2}-\d{2}\b", text, re.M):
                warnings.append(f"{folder}/{path.name}：缺少 Updated")

    # 3) entries 的 front-matter
    entries = root / "entries"
    if entries.is_dir():
        for path in sorted(entries.glob("*.md")):
            if path.name.startswith("_") or path.name == "CATALOG.md":
                continue
            fm = front_matter(read_text(path))
            if not fm:
                warnings.append(f"entries/{path.name}：缺少 front-matter")
                continue
            if not DATE_RE.match(fm.get("date", "")):
                warnings.append(f"entries/{path.name}：date 不是 YYYY-MM-DD")
            if fm.get("tier", "") not in TIERS:
                warnings.append(f"entries/{path.name}：tier 必须是 core / record / raw")
            if fm.get("status", "") not in STATUSES:
                warnings.append(f"entries/{path.name}：status 必须是 active / superseded / archived")
            if fm.get("tier") == "core" and not fm.get("review"):
                warnings.append(f"entries/{path.name}：core 条目必须有 review")
            if fm.get("review") and not DATE_RE.match(fm["review"]):
                warnings.append(f"entries/{path.name}：review 不是 YYYY-MM-DD")

    # 4) 导航页里的相对链接
    for name in ("README.md", "decisions.md", "commitments.md", "open-threads.md"):
        page = root / name
        if not page.exists():
            warnings.append(f"缺少导航页：{name}")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", read_text(page)):
            target = target.split("#")[0].strip()
            if not target or re.match(r"^[a-z]+:", target, re.I):
                continue
            if not (page.parent / target).exists():
                warnings.append(f"{name}：断链 {target}")

    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="记忆库只读自检")
    parser.add_argument("--root", type=Path, default=Path("memory"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"找不到目录：{root}")

    warnings = check(root)
    print(f"CHECK: {len(warnings)} 条警告；没有改动任何文件。")
    for warning in warnings:
        print("WARN:", warning)
    raise SystemExit(0 if not warnings else 1)


if __name__ == "__main__":
    main()
