from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def test_foundation_directories_exist():
    for name in ("src", "scripts", "tests", "docs", "data", ".devcontainer", ".github/workflows"):
        assert (ROOT / name).is_dir()


def test_python_version_constraint():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires-python = ">=3.12,<3.13"' in text
