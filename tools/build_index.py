"""文件式记忆库：生成 INDEX.md 与 entries/CATALOG.md。

用法:
    python build_index.py --root memory
    python build_index.py --root memory --today 2026-01-01   # 手动指定"今天"，测试用

产出（都在 --root 目录下）:
    INDEX.md
    entries/CATALOG.md

设计原则:
    · 只读源文件，只写两个生成物；
    · 主题词从 topics.txt 读，一行一个正则——不要把主题写死在代码里；
    · 判断（晋升 / 降级 / 删不删）留给人，脚本只报告。
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

SKIP_DIRS = {"assets", ".git", "__pycache__", "node_modules"}
GENERATED = {"INDEX.md", "CATALOG.md"}
TEXT_EXT = {".md", ".yaml", ".yml", ".txt"}

DATE_RE = re.compile(r"(?<!\d)(20\d{2}-\d{2}-\d{2})(?!\d)")
QUOTE_RE = re.compile(r"[「『]([^」』\n]{2,40})[」』]")
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
KV_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", re.M)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def front_matter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    for key, value in KV_RE.findall(m.group(1)):
        value = value.strip().strip('"').strip("'")
        if "  #" in value:
            value = value.split("  #", 1)[0].strip()
        data[key.lower()] = value
    return data


def strip_front_matter(text: str) -> str:
    return FM_RE.sub("", text, count=1)


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_dir() or path.name in GENERATED or path.name == "topics.txt":
            continue
        parts = path.relative_to(root).parts[:-1]
        if any(part in SKIP_DIRS for part in parts):
            continue
        if path.suffix.lower() in TEXT_EXT:
            yield path


def load_topics(root: Path) -> list[str]:
    path = root / "topics.txt"
    if not path.exists():
        return []
    topics: list[str] = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            re.compile(line)
        except re.error:
            continue
        topics.append(line)
    return list(dict.fromkeys(topics))


def load_entries(root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    folder = root / "entries"
    if not folder.is_dir():
        return entries
    for path in sorted(folder.glob("*.md")):
        if path.name in GENERATED or path.name.startswith("_"):
            continue
        text = read_text(path)
        fm = front_matter(text)
        entries.append(
            {
                "rel": rel(path, root),
                "title": title_of(text, path.stem),
                "date": fm.get("date") or path.stem[:10],
                "tier": (fm.get("tier") or "record").lower(),
                "review": fm.get("review", ""),
                "status": (fm.get("status") or "active").lower(),
            }
        )
    return entries


def scan(root: Path, topics: list[str]):
    hits: dict[str, list[tuple[str, int]]] = defaultdict(list)
    datehits: dict[str, set[str]] = defaultdict(set)
    quotes: dict[str, set[str]] = defaultdict(set)
    total = 0
    for path in iter_files(root):
        text = strip_front_matter(read_text(path))
        name = rel(path, root)
        lines = text.splitlines()
        total += len(lines)
        for i, line in enumerate(lines, 1):
            for topic in topics:
                if re.search(topic, line):
                    hits[topic].append((name, i))
            for found in DATE_RE.findall(line):
                datehits[found].add(name)
            for quote in QUOTE_RE.findall(line):
                quotes[quote].add(name)
    return hits, datehits, quotes, total


def knowledge_links(root: Path) -> list[str]:
    lines: list[str] = []
    for folder, label in (("knowledge", "knowledge/"), ("experience", "experience/")):
        base = root / folder
        if not base.is_dir():
            continue
        files = sorted(
            p for p in base.glob("*.md") if not p.name.startswith("_") and p.name != "README.md"
        )
        if not files:
            continue
        lines += [f"**{label}**", ""]
        for path in files:
            lines.append(f"- [{title_of(read_text(path), path.stem)}]({folder}/{path.name})")
        lines.append("")
    return lines


def build_index(root: Path, today: str) -> None:
    topics = load_topics(root)
    entries = load_entries(root)
    hits, datehits, quotes, total = scan(root, topics)

    out: list[str] = [
        "# 索引",
        "",
        "> 自动生成：`python tools/build_index.py --root memory`。**不要手改。**",
        f"> 生成日：{today} · 文件行数：{total} · 条目：{len(entries)}",
        "",
        "---",
        "",
        "## 待复核",
        "",
    ]

    due = [e for e in entries if e["status"] == "active" and e["review"] and e["review"] <= today]
    missing = [e for e in entries if e["status"] == "active" and e["tier"] == "core" and not e["review"]]

    if due:
        out += ["| 条目 | 日期 | 档 | 复核日 |", "|---|---|---|---|"]
        for e in sorted(due, key=lambda x: x["review"]):
            out.append(
                f"| [{esc(e['title'])}]({e['rel']}) | {e['date']} | {e['tier']} | {e['review']} |"
            )
        out.append("")
    else:
        out += ["目前没有到期的条目。", ""]

    if missing:
        out += ["**core 条目缺复核日**：", ""]
        for e in missing:
            out.append(f"- [{esc(e['title'])}]({e['rel']})")
        out.append("")

    out += ["---", "", "## 知识在哪", ""]
    knowledge = knowledge_links(root)
    out += knowledge if knowledge else ["（`knowledge/`、`experience/` 还是空的）", ""]

    out += ["---", "", "## 主题", ""]
    if not topics:
        out += ["（`topics.txt` 里还没有启用的主题词）", ""]
    for topic in topics:
        records = hits.get(topic, [])
        if not records:
            continue
        out.append(f"### {topic}（{len(records)} 处）")
        by_file: dict[str, list[int]] = defaultdict(list)
        for name, line_no in records:
            by_file[name].append(line_no)
        ranked = sorted(by_file.items(), key=lambda kv: -len(kv[1]))
        for name, numbers in ranked[:3]:
            shown = ", ".join(str(n) for n in numbers[:12])
            more = " …" if len(numbers) > 12 else ""
            out.append(f"- `{name}` : {shown}{more}")
        if len(ranked) > 3:
            out.append(f"- （另有 {len(ranked) - 3} 个文件提到，按主题词自行搜索）")
        out.append("")

    out += ["---", "", "## 日期（正文里提到的日期，不等于事件发生日）", ""]
    if datehits:
        for day in sorted(datehits):
            out.append(f"- **{day}** : {'、'.join(sorted(datehits[day]))}")
    else:
        out.append("（没有找到日期）")
    out.append("")

    out += ["---", "", "## 引语（出现在 2 个以上文件的短句，谁说的须核原文）", ""]
    shared = [(q, fs) for q, fs in quotes.items() if len(fs) > 1]
    if shared:
        for quote, files in sorted(shared, key=lambda kv: -len(kv[1])):
            out.append(f"- 「{quote}」—— {'、'.join(sorted(files))}")
    else:
        out.append("（没有重复出现的短句）")
    out.append("")

    out += ["---", "", "## 最近 8 条", ""]
    recent = sorted(entries, key=lambda e: (e["date"], e["rel"]), reverse=True)[:8]
    if recent:
        for e in recent:
            out.append(f"- {e['date']} [{esc(e['title'])}]({e['rel']})")
        out += ["", "全部条目见 [entries/CATALOG.md](entries/CATALOG.md)。"]
    else:
        out.append("（`entries/` 还是空的）")
    out.append("")

    (root / "INDEX.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    build_catalog(root, entries)


def build_catalog(root: Path, entries: list[dict[str, str]]) -> None:
    out = [
        "# 日期条目",
        "",
        "[返回索引](../INDEX.md)",
        "",
        "> 自动生成。按日期倒序；只列原文，不复述内容。",
        "",
    ]
    current = None
    for e in sorted(entries, key=lambda x: (x["date"], x["rel"]), reverse=True):
        month = e["date"][:7] or "未知日期"
        if month != current:
            if current is not None:
                out.append("")
            out += [f"## {month}", ""]
            current = month
        out.append(f"- {e['date']} [{esc(e['title'])}]({e['rel'].split('/', 1)[-1]})")
    out.append("")
    folder = root / "entries"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "CATALOG.md").write_text("\n".join(out), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="给文件式记忆库建索引")
    parser.add_argument("--root", type=Path, default=Path("memory"), help="记忆库目录")
    parser.add_argument("--today", default=date.today().isoformat(), help="今天（YYYY-MM-DD）")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"找不到目录：{root}")
    build_index(root, args.today)
    print(f"index -> {root / 'INDEX.md'}")


if __name__ == "__main__":
    main()
