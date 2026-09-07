from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_architecture_guard_passes():
    result = subprocess.run(
        ["python", "scripts/check_architecture.py"], cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
