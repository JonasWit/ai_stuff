"""Tests for scripts/check.py.

Run with: uv run pytest
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

CHECK_SCRIPT = Path(__file__).resolve().parents[1] / "check.py"


def load_check_module():
    spec = importlib.util.spec_from_file_location("check", CHECK_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["check"] = module
    spec.loader.exec_module(module)
    return module


check = load_check_module()


@pytest.fixture()
def make_repo(tmp_path: Path):
    """Build a minimal repository that satisfies every required file."""

    def build(files: dict[str, str] | None = None, missing: tuple[str, ...] = ()) -> Path:
        root = tmp_path / "repo"
        root.mkdir()
        for name in check.REQUIRED_FILES:
            if name in missing:
                continue
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# placeholder\n", encoding="utf-8")
        for name, content in (files or {}).items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root

    return build


def run(root: Path, capsys) -> tuple[int, str]:
    code = check.main(["--root", str(root)])
    return code, capsys.readouterr().out


def test_clean_repository_passes(make_repo, capsys):
    root = make_repo()
    code, out = run(root, capsys)
    assert code == 0
    assert "PASS required files" in out


def test_missing_required_document_fails(make_repo, capsys):
    root = make_repo(missing=("docs/wzorce.md",))
    code, out = run(root, capsys)
    assert code == 1
    assert "docs/wzorce.md" in out


def test_dead_relative_link_fails(make_repo, capsys):
    root = make_repo({"README.md": "[missing](docs/nie-ma.md)\n"})
    code, out = run(root, capsys)
    assert code == 1
    assert "docs/nie-ma.md" in out


def test_working_relative_link_passes(make_repo, capsys):
    root = make_repo({"README.md": "[rules](docs/zasady-ai.md)\n"})
    code, _ = run(root, capsys)
    assert code == 0


def test_external_link_is_not_checked(make_repo, capsys):
    root = make_repo({"README.md": "[site](https://example.com/page)\n"})
    code, _ = run(root, capsys)
    assert code == 0


def test_link_inside_code_fence_is_ignored(make_repo, capsys):
    root = make_repo({"README.md": "```\n[sample](docs/nie-ma.md)\n```\n"})
    code, _ = run(root, capsys)
    assert code == 0


def test_anchor_only_link_is_ignored(make_repo, capsys):
    root = make_repo({"README.md": "[section](#usage)\n"})
    code, _ = run(root, capsys)
    assert code == 0


def test_forbidden_marker_in_code_fails(make_repo, capsys):
    root = make_repo({"src/app.py": "# TO" + "DO fix this\n"})
    code, out = run(root, capsys)
    assert code == 1
    assert "src/app.py" in out


def test_forbidden_marker_in_docs_is_allowed(make_repo, capsys):
    root = make_repo({"docs/notes.md": "# TO" + "DO is discussed here\n"})
    code, _ = run(root, capsys)
    assert code == 0


def test_forbidden_marker_in_kotlin_fails(make_repo, capsys):
    root = make_repo({"examples/app.kt": "// TO" + "DO later\n"})
    code, out = run(root, capsys)
    assert code == 1
    assert "examples/app.kt" in out


def test_paths_are_reported_with_forward_slashes(make_repo, capsys):
    root = make_repo({"src/app.py": "# TO" + "DO fix this\n"})
    _, out = run(root, capsys)
    assert "src/app.py:1" in out
    assert "src\\app.py" not in out


def test_oversized_code_file_fails(make_repo, capsys):
    body = "\n".join(f"# line {i}" for i in range(check.CODE_LINE_BUDGET + 20))
    root = make_repo({"src/big.py": body})
    code, out = run(root, capsys)
    assert code == 1
    assert "src/big.py" in out


def test_absent_stack_is_skipped_not_failed(make_repo, capsys):
    root = make_repo()
    code, out = run(root, capsys)
    assert code == 0
    assert "SKIP stack checks" in out


def test_nested_run_does_not_execute_stack_checks(make_repo, capsys, monkeypatch):
    monkeypatch.setenv("CHECK_SKIP_STACK", "1")
    root = make_repo({"pyproject.toml": "[project]\nname = 'x'\n"})
    code, out = run(root, capsys)
    assert code == 0
    assert "SKIP stack checks" in out
