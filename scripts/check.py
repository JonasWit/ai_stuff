#!/usr/bin/env python3
"""One command that answers "is this repository still consistent?".

Everything here is deliberately dependency-free and stack-agnostic: the rules must be
executable in a fresh clone, before any project code exists. When a stack appears the
same command runs its test suite as the last step.

Run:  uv run python scripts/check.py
Exit: 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "docs/zasady-ai.md",
    "docs/jak-pisac-agents-md.md",
    "docs/wzorce.md",
    "docs/testy-instrukcji.md",
    "scripts/check.py",
)

EXCLUDED_DIRS = frozenset(
    {".git", "node_modules", ".opencode", ".venv", "__pycache__", ".pytest_cache", "bin", "obj"}
)

CODE_EXTENSIONS = frozenset(
    {
        ".py",
        ".kt",
        ".ps1",
        ".psm1",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".sh",
        ".go",
        ".rs",
        ".cs",
        ".java",
        ".rb",
    }
)

CODE_LINE_BUDGET = 300
DOC_LINE_BUDGET = 800

# Assembled at runtime so this file never flags itself.
MARKERS = ("TO" + "DO", "FIX" + "ME", "XX" + "X")

LINK_PATTERN = re.compile(r'\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+"[^"]*")?\)')
EXTERNAL_PREFIXES = ("http:", "https:", "mailto:", "tel:", "ftp:", "#", "/")


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    problems: tuple[str, ...] = ()

    @classmethod
    def from_problems(cls, name: str, problems: list[str]) -> "CheckResult":
        found = tuple(problems)
        return cls(name=name, status="FAIL" if found else "PASS", problems=found)

    @classmethod
    def skipped(cls, name: str) -> "CheckResult":
        return cls(name=name, status="SKIP")


def iter_files(root: Path, extensions: frozenset[str] | None = None):
    """Yield (path, relative posix path) for files that are part of the repository."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if extensions is not None and path.suffix.lower() not in extensions:
            continue
        yield path, relative.as_posix()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def check_required_files(root: Path) -> CheckResult:
    problems = [f"missing: {name}" for name in REQUIRED_FILES if not (root / name).exists()]
    return CheckResult.from_problems("required files", problems)


def check_markdown_links(root: Path) -> CheckResult:
    from urllib.parse import unquote

    problems: list[str] = []
    for path, relative in iter_files(root, frozenset({".md"})):
        in_fence = False
        for number, line in enumerate(read_lines(path), start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_PATTERN.finditer(line):
                target = match.group("target").strip("<>")
                if target.startswith(EXTERNAL_PREFIXES):
                    continue
                path_part = target.split("#", 1)[0]
                if not path_part:
                    continue
                resolved = path.parent / unquote(path_part)
                if not resolved.exists():
                    problems.append(f"{relative}:{number} dead link: {target}")
    return CheckResult.from_problems("markdown links", problems)


def check_forbidden_markers(root: Path) -> CheckResult:
    problems: list[str] = []
    for path, relative in iter_files(root, CODE_EXTENSIONS):
        for number, line in enumerate(read_lines(path), start=1):
            for marker in MARKERS:
                if marker in line:
                    problems.append(f"{relative}:{number} {marker}")
    return CheckResult.from_problems("forbidden markers", problems)


def check_file_size(root: Path) -> CheckResult:
    problems: list[str] = []
    for path, relative in iter_files(root, CODE_EXTENSIONS | {".md"}):
        budget = DOC_LINE_BUDGET if path.suffix.lower() == ".md" else CODE_LINE_BUDGET
        lines = len(read_lines(path))
        if lines > budget:
            problems.append(f"{relative} has {lines} lines (limit {budget})")
    return CheckResult.from_problems("file size", problems)


def stack_commands(root: Path) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = []
    if (root / "package.json").exists() and shutil.which("npm"):
        commands.append(("npm test", ["npm", "test", "--silent"]))
    if ((root / "pyproject.toml").exists() or (root / "pytest.ini").exists()) and shutil.which("uv"):
        commands.append(("uv run pytest", ["uv", "run", "pytest"]))
    if (root / "Cargo.toml").exists() and shutil.which("cargo"):
        commands.append(("cargo test", ["cargo", "test", "--quiet"]))
    if (root / "go.mod").exists() and shutil.which("go"):
        commands.append(("go test", ["go", "test", "./..."]))
    return commands


def check_stack(root: Path) -> CheckResult:
    # Nested invocations (the test suite running its own checks) must not recurse.
    if os.environ.get("CHECK_SKIP_STACK") == "1":
        return CheckResult.skipped("stack checks")

    commands = stack_commands(root)
    if not commands:
        return CheckResult.skipped("stack checks")

    environment = {**os.environ, "CHECK_SKIP_STACK": "1"}
    problems: list[str] = []
    for name, command in commands:
        completed = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
        if completed.returncode != 0:
            problems.append(f"{name} failed")
            tail = (completed.stdout + completed.stderr).strip().splitlines()[-15:]
            problems.extend(tail)
    return CheckResult.from_problems("stack checks", problems)


def render(root: Path, results: list[CheckResult]) -> str:
    lines = [f"check root: {root.as_posix()}"]
    for result in results:
        lines.append(f"{result.status} {result.name}")
        lines.extend(f"      {problem}" for problem in result.problems)
    failed = sum(1 for result in results if result.status == "FAIL")
    lines.append(f"summary: {len(results)} checks, {failed} failed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check repository consistency.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="repository root (defaults to the parent of scripts/)",
    )
    arguments = parser.parse_args(argv)
    root = Path(arguments.root)

    results = [
        check_required_files(root),
        check_markdown_links(root),
        check_forbidden_markers(root),
        check_file_size(root),
        check_stack(root),
    ]
    print(render(root, results))
    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
