from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".devcontainer/devcontainer.json",
    ".devcontainer/Dockerfile",
    ".github/workflows/ci.yml",
    ".gitignore",
    "README.md",
    "pyproject.toml",
    "requirements-dev.txt",
    "docs/FOUNDATION.md",
    "src/__init__.py",
]
FORBIDDEN_PATH_PARTS = {"acquisition", "ocr", "question_bank", "mocks"}
FORBIDDEN_BINARY_SUFFIXES = {".zip", ".pdf", ".docx", ".xlsx"}


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        print("Missing foundation files:")
        print(*missing, sep="\n")
        return 1

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.splitlines()

    for path in tracked:
        parts = set(Path(path).parts)
        if parts & FORBIDDEN_PATH_PARTS:
            print(f"Forbidden foundation path: {path}")
            return 1
        if Path(path).suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            print(f"Tracked binary artifact is forbidden in foundation: {path}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
