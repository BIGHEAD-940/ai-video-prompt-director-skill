#!/usr/bin/env python3
"""Validate the public skill package using only the Python standard library."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SKILL_DIR = Path("skills/ai-video-prompt-director")
SKILL_REL = SKILL_DIR / "SKILL.md"
REQUIRED = (
    Path("README.md"), Path("SOURCES.md"), Path("LICENSE"), Path("LICENSE-CODE"),
    Path("CHANGELOG.md"), Path("CONTRIBUTING.md"), Path("SECURITY.md"),
    Path("scripts/validate_repo.py"), Path("tests/test_validate_repo.py"),
    Path("evals/README.md"), Path("evals/prompts.csv"),
    SKILL_REL, SKILL_DIR / "agents/openai.yaml",
    SKILL_DIR / "references/directing-methods.md",
    SKILL_DIR / "references/prompt-template.md",
    SKILL_DIR / "references/evaluation-cases.md",
    SKILL_DIR / "examples/single-shot.md",
    SKILL_DIR / "examples/dialogue-reaction.md",
)
LOCAL_PATH_PATTERN = re.compile(r"(?i)\b[CD]:" + re.escape("\\") + r"(?:codex|users)" + re.escape("\\"))
SCAFFOLD_MARKERS = ("[TODO:", "TODO: Add the task-specific guidance")
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".csv", ".txt", ".gitignore"}


def validate(root: Path) -> list[str]:
    root = root.resolve()
    problems: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            problems.append(f"缺少必需文件：{rel.as_posix()}")

    skill_path = root / SKILL_REL
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill, re.S)
        if not frontmatter:
            problems.append("SKILL.md 缺少有效 YAML frontmatter")
        else:
            block = frontmatter.group(1)
            name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", block)
            description = re.search(r"(?m)^description:\s*.+\S.*$", block)
            if not name:
                problems.append("SKILL.md 缺少有效 name")
            elif name.group(1) != SKILL_DIR.name:
                problems.append("frontmatter name 与 Skill 目录名不一致")
            if not description:
                problems.append("SKILL.md 缺少 description")
        for marker in SCAFFOLD_MARKERS:
            if marker in skill:
                problems.append(f"SKILL.md 仍包含脚手架占位文本：{marker}")

    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"无法按 UTF-8 读取：{path.relative_to(root).as_posix()}")
            continue
        rel = path.relative_to(root).as_posix()
        if LOCAL_PATH_PATTERN.search(content):
            problems.append(f"发现疑似本机绝对路径：{rel}")
        if path.suffix.lower() == ".md":
            for target in link_pattern.findall(content):
                target = target.strip().split()[0].strip("<>")
                if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                    continue
                local_target = target.split("#", 1)[0]
                if local_target and not (path.parent / local_target).resolve().is_file():
                    problems.append(f"失效的本地 Markdown 链接：{rel} -> {target}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="仓库根目录")
    args = parser.parse_args()
    problems = validate(Path(args.root))
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print("OK: package structure, Markdown links, and local-path scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
