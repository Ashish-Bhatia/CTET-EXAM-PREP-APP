from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .lifecycle import LifecycleState
from .models import BinaryEvidence, PackageIdentity

ZIP_SIGNATURES = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")
DRIVE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class BinaryValidationError(ValueError):
    pass


def _safe_member_path(name: str) -> str:
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//"):
        raise BinaryValidationError(f"absolute archive member path: {name}")
    if re.match(r"^[A-Za-z]:/", normalized):
        raise BinaryValidationError(f"Windows absolute archive member path: {name}")
    parts = [part for part in normalized.split("/") if part]
    if ".." in parts:
        raise BinaryValidationError(f"path traversal archive member: {name}")
    return "/".join(parts) + ("/" if name.endswith(("/", "\\")) else "")


def _inventory(path: Path) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    logical_paths: set[str] = set()
    try:
        with zipfile.ZipFile(path, "r") as archive:
            bad = archive.testzip()
            if bad is not None:
                raise BinaryValidationError(f"CRC validation failed: {bad}")
            for info in archive.infolist():
                logical = _safe_member_path(info.filename)
                key = logical.rstrip("/")
                if not key:
                    raise BinaryValidationError(f"empty archive member path: {info.filename}")
                if key in logical_paths:
                    raise BinaryValidationError(
                        f"duplicate archive member path: {info.filename}"
                    )
                logical_paths.add(key)
                is_dir = info.is_dir() or info.filename.endswith(("/", "\\"))
                data = archive.read(info.filename)
                inventory.append(
                    {
                        "path": logical,
                        "type": "directory" if is_dir else "file",
                        "size": info.file_size,
                        "compressed_size": info.compress_size,
                        "crc": f"{info.CRC:08x}",
                        "read_bytes": len(data),
                    }
                )
    except zipfile.BadZipFile as exc:
        raise BinaryValidationError(f"invalid ZIP archive: {exc}") from exc
    except OSError as exc:
        raise BinaryValidationError(f"unable to read ZIP archive: {exc}") from exc
    return inventory


def _validate_provenance(package: PackageIdentity) -> None:
    page = urlparse(package.official_page_url)
    drive = urlparse(package.official_drive_url)
    if page.scheme != "https" or page.netloc != "ctet.nic.in":
        raise BinaryValidationError("official page URL is not the CTET official HTTPS host")
    if drive.scheme != "https" or drive.netloc != "drive.google.com":
        raise BinaryValidationError("official Drive URL is not the Google Drive HTTPS host")
    if not DRIVE_ID_RE.fullmatch(package.drive_file_id):
        raise BinaryValidationError("invalid Drive file ID")


def validate_binary(path: str | Path, package: PackageIdentity) -> BinaryEvidence:
    file_path = Path(path)
    if file_path.name != package.filename:
        raise BinaryValidationError(
            f"filename mismatch: expected {package.filename}, got {file_path.name}"
        )
    if not file_path.is_file():
        raise BinaryValidationError(f"binary does not exist: {file_path}")
    size = file_path.stat().st_size
    if size == 0:
        raise BinaryValidationError("binary is zero bytes")
    with file_path.open("rb") as handle:
        signature = handle.read(4)
        handle.seek(0)
        digest = hashlib.sha256(handle.read()).hexdigest()
    if signature not in ZIP_SIGNATURES:
        raise BinaryValidationError("file does not have a ZIP signature")
    if package.expected_package_type.upper() != "ZIP":
        raise BinaryValidationError("unsupported expected package type")
    _validate_provenance(package)

    inventory = _inventory(file_path)
    evidence = BinaryEvidence.acquired(package, str(file_path), size)
    evidence.sha256 = digest
    evidence.lifecycle = LifecycleState.HASHED
    evidence.zip_valid = True
    evidence.lifecycle = LifecycleState.ZIP_VALIDATED
    evidence.crc_valid = True
    evidence.member_inventory = inventory
    evidence.lifecycle = LifecycleState.OFFICIAL_BINARY_VERIFIED
    return evidence


def write_evidence(evidence: BinaryEvidence, output: str | Path) -> None:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(evidence.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
