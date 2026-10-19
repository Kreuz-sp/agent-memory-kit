"""Build INDEX.md and entries/CATALOG.md for a file-based memory.

Usage:
    python build_index.py --root memory
    python build_index.py --root memory --today 2026-01-01   # fixed "today", for tests

Outputs (inside --root):
    INDEX.md
    entries/CATALOG.md

Design rules:
    - Read source files; write only the two generated files.
    - Topics come from topics.txt, one regex per line. Never hard-code them.
    - Decisions (promote / demote / delete) belong to humans; the script only reports.
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
        "# Index",
        "",
        "> Generated by `python tools/build_index.py --root memory`. **Do not edit by hand.**",
        f"> Generated: {today} · lines: {total} · entries: {len(entries)}",
        "",
        "---",
        "",
        "## Due for review",
        "",
    ]

    due = [e for e in entries if e["status"] == "active" and e["review"] and e["review"] <= today]
    missing = [e for e in entries if e["status"] == "active" and e["tier"] == "core" and not e["review"]]

    if due:
        out += ["| Entry | Date | Tier | Review |", "|---|---|---|---|"]
        for e in sorted(due, key=lambda x: x["review"]):
            out.append(
                f"| [{esc(e['title'])}]({e['rel']}) | {e['date']} | {e['tier']} | {e['review']} |"
            )
        out.append("")
    else:
        out += ["Nothing is due right now.", ""]

    if missing:
        out += ["**core entries without a review date**:", ""]
        for e in missing:
            out.append(f"- [{esc(e['title'])}]({e['rel']})")
        out.append("")

    out += ["---", "", "## Where the knowledge is", ""]
    knowledge = knowledge_links(root)
    out += knowledge if knowledge else ["(`knowledge/` and `experience/` are still empty)", ""]

    out += ["---", "", "## Topics", ""]
    if not topics:
        out += ["(no active topics in `topics.txt` yet)", ""]
    for topic in topics:
        records = hits.get(topic, [])
        if not records:
            continue
        out.append(f"### {topic} ({len(records)} hits)")
        by_file: dict[str, list[int]] = defaultdict(list)
        for name, line_no in records:
            by_file[name].append(line_no)
        ranked = sorted(by_file.items(), key=lambda kv: -len(kv[1]))
        for name, numbers in ranked[:3]:
            shown = ", ".join(str(n) for n in numbers[:12])
            more = " …" if len(numbers) > 12 else ""
            out.append(f"- `{name}` : {shown}{more}")
        if len(ranked) > 3:
            out.append(f"- ({len(ranked) - 3} more files mention it; search by the topic word)")
        out.append("")

    out += ["---", "", "## Dates (dates mentioned in the body; not necessarily the event date)", ""]
    if datehits:
        for day in sorted(datehits):
            out.append(f"- **{day}** : {'、'.join(sorted(datehits[day]))}")
    else:
        out.append("(no dates found)")
    out.append("")

    out += ["---", "", "## Quotes (short lines appearing in 2+ files; check the source before attributing)", ""]
    shared = [(q, fs) for q, fs in quotes.items() if len(fs) > 1]
    if shared:
        for quote, files in sorted(shared, key=lambda kv: -len(kv[1])):
            out.append(f"- 「{quote}」—— {'、'.join(sorted(files))}")
    else:
        out.append("(no repeated short lines)")
    out.append("")

    out += ["---", "", "## Latest 8", ""]
    recent = sorted(entries, key=lambda e: (e["date"], e["rel"]), reverse=True)[:8]
    if recent:
        for e in recent:
            out.append(f"- {e['date']} [{esc(e['title'])}]({e['rel']})")
        out += ["", "All entries: [entries/CATALOG.md](entries/CATALOG.md)."]
    else:
        out.append("(`entries/` is still empty)")
    out.append("")

    (root / "INDEX.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    build_catalog(root, entries)


def build_catalog(root: Path, entries: list[dict[str, str]]) -> None:
    out = [
        "# Entries by date",
        "",
        "[Back to index](../INDEX.md)",
        "",
        "> Generated. Newest first. Links only; no summaries.",
        "",
    ]
    current = None
    for e in sorted(entries, key=lambda x: (x["date"], x["rel"]), reverse=True):
        month = e["date"][:7] or "Unknown date"
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
    parser = argparse.ArgumentParser(description="Build an index for a file-based memory")
    parser.add_argument("--root", type=Path, default=Path("memory"), help="memory folder")
    parser.add_argument("--today", default=date.today().isoformat(), help="today (YYYY-MM-DD)")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Directory not found: {root}")
    build_index(root, args.today)
    print(f"index -> {root / 'INDEX.md'}")


if __name__ == "__main__":
    main()
