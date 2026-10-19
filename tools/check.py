"""Read-only checks: front matter, duplicate ids, knowledge/experience metadata, broken links.

Usage:
    python check.py --root memory

Exit code:
    0 = no warnings
    1 = warnings (no files are modified either way)
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

    # 1) ids in facts must be unique
    seen: dict[str, list[str]] = {}
    for path in sorted((root / "facts").glob("*.yaml")):
        for ident in re.findall(r"^\s*-\s*id:\s*(\S+)", read_text(path), re.M):
            seen.setdefault(ident, []).append(path.name)
    for ident, files in seen.items():
        if len(files) > 1:
            warnings.append(f"duplicate id: {ident} ({', '.join(files)})")

    # 2) knowledge / experience need Status and Updated
    for folder in ("knowledge", "experience"):
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name.startswith("_"):
                continue
            text = read_text(path)
            if not re.search(r"^Status:\s*(active|deprecated)\b", text, re.M):
                warnings.append(f"{folder}/{path.name}: missing or invalid Status")
            if not re.search(r"^Updated:\s*\d{4}-\d{2}-\d{2}\b", text, re.M):
                warnings.append(f"{folder}/{path.name}: missing Updated")

    # 3) front matter of entries
    entries = root / "entries"
    if entries.is_dir():
        for path in sorted(entries.glob("*.md")):
            if path.name.startswith("_") or path.name == "CATALOG.md":
                continue
            fm = front_matter(read_text(path))
            if not fm:
                warnings.append(f"entries/{path.name}: missing front matter")
                continue
            if not DATE_RE.match(fm.get("date", "")):
                warnings.append(f"entries/{path.name}: date is not YYYY-MM-DD")
            if fm.get("tier", "") not in TIERS:
                warnings.append(f"entries/{path.name}: tier must be core / record / raw")
            if fm.get("status", "") not in STATUSES:
                warnings.append(f"entries/{path.name}: status must be active / superseded / archived")
            if fm.get("tier") == "core" and not fm.get("review"):
                warnings.append(f"entries/{path.name}: core entries must have a review date")
            if fm.get("review") and not DATE_RE.match(fm["review"]):
                warnings.append(f"entries/{path.name}: review is not YYYY-MM-DD")

    # 4) relative links in navigation pages
    for name in ("README.md", "decisions.md", "commitments.md", "open-threads.md"):
        page = root / name
        if not page.exists():
            warnings.append(f"missing navigation page: {name}")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", read_text(page)):
            target = target.split("#")[0].strip()
            if not target or re.match(r"^[a-z]+:", target, re.I):
                continue
            if not (page.parent / target).exists():
                warnings.append(f"{name}: broken link {target}")

    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only checks for a memory folder")
    parser.add_argument("--root", type=Path, default=Path("memory"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Directory not found: {root}")

    warnings = check(root)
    print(f"CHECK: {len(warnings)} warning(s); no files changed.")
    for warning in warnings:
        print("WARN:", warning)
    raise SystemExit(0 if not warnings else 1)


if __name__ == "__main__":
    main()
