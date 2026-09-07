from __future__ import annotations

import subprocess
from pathlib import Path

from .models import PackageIdentity


class AcquisitionError(RuntimeError):
    pass


def acquire_with_gdown(
    package: PackageIdentity,
    destination: str | Path,
    *,
    dry_run: bool = False,
) -> Path:
    target = Path(destination)
    if target.name != package.filename:
        raise AcquisitionError(
            f"destination filename mismatch: expected {package.filename}, got {target.name}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "gdown",
        f"https://drive.google.com/uc?id={package.drive_file_id}",
        "-O",
        str(target),
    ]
    if dry_run:
        return target
    result = subprocess.run(command, check=False, capture_output=True, text=True, shell=False)
    if result.returncode != 0:
        raise AcquisitionError(
            f"gdown failed with exit code {result.returncode}: {result.stderr.strip()}"
        )
    if not target.is_file() or target.stat().st_size == 0:
        raise AcquisitionError("gdown completed without a non-empty output file")
    return target
