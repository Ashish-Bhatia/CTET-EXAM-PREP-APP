from pathlib import Path
import hashlib
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ctet_binary.acquisition import acquire_with_gdown  # noqa: E402
from ctet_binary.lifecycle import LifecycleState, advance  # noqa: E402
from ctet_binary.manifest import (  # noqa: E402
    ManifestError,
    load_packages,
    resolve_by_filename,
)
from ctet_binary.models import PackageIdentity  # noqa: E402
from ctet_binary.validation import (  # noqa: E402
    BinaryValidationError,
    validate_binary,
    write_evidence,
)


PACKAGE = PackageIdentity(
    identity_key="test",
    exam_cycle="Test",
    exam_date="2026-01-01",
    paper="Paper I",
    set_name="S",
    filename="test.zip",
    drive_file_id="1Abc_-123",
    official_page_url="https://ctet.nic.in/question-paper-feb-2026/",
    official_drive_url="https://drive.google.com/file/d/1Abc_-123/view",
)


def make_zip(path: Path, depth: int = 3) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        prefix = "/".join(f"folder{i}" for i in range(depth))
        if prefix:
            archive.writestr(f"{prefix}/", b"")
            archive.writestr(f"{prefix}/question.pdf", b"question")
        else:
            archive.writestr("question.pdf", b"question")


@pytest.mark.parametrize("depth", [0, 1, 2, 3, 5])
def test_arbitrary_depth_and_member_reads(tmp_path, depth):
    target = tmp_path / "test.zip"
    make_zip(target, depth)
    evidence = validate_binary(target, PACKAGE)
    assert evidence.lifecycle == LifecycleState.OFFICIAL_BINARY_VERIFIED
    assert evidence.crc_valid
    assert any(item["path"].endswith("question.pdf") for item in evidence.member_inventory)


def test_sha256_uses_actual_bytes(tmp_path):
    target = tmp_path / "test.zip"
    make_zip(target)
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    assert validate_binary(target, PACKAGE).sha256 == expected


@pytest.mark.parametrize(
    "payload",
    [b"", b"<html>download warning</html>", b"PK\x00\x00not-a-zip"],
)
def test_rejects_invalid_binary(tmp_path, payload):
    target = tmp_path / "test.zip"
    target.write_bytes(payload)
    with pytest.raises(BinaryValidationError):
        validate_binary(target, PACKAGE)


def test_rejects_corrupt_zip(tmp_path):
    target = tmp_path / "test.zip"
    make_zip(target)
    target.write_bytes(target.read_bytes()[:-8])
    with pytest.raises(BinaryValidationError):
        validate_binary(target, PACKAGE)


@pytest.mark.parametrize(
    "member",
    [
        "../escape.txt",
        "..\\escape.txt",
        "/absolute.txt",
        "C:\\absolute.txt",
        "folder/../x.txt",
    ],
)
def test_rejects_unsafe_member_paths(tmp_path, member):
    target = tmp_path / "test.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr(member, b"x")
    with pytest.raises(BinaryValidationError):
        validate_binary(target, PACKAGE)


def test_duplicate_logical_paths_rejected(tmp_path):
    target = tmp_path / "test.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("folder/file.txt", b"a")
        archive.writestr("folder\\file.txt", b"b")
    with pytest.raises(BinaryValidationError):
        validate_binary(target, PACKAGE)


def test_lifecycle_is_monotonic():
    assert (
        advance(LifecycleState.OFFICIAL_PAGE_ONLY, LifecycleState.HASHED)
        == LifecycleState.HASHED
    )
    with pytest.raises(ValueError):
        advance(LifecycleState.HASHED, LifecycleState.BINARY_ACQUIRED)


def test_manifest_set_resolution_and_duplicates(tmp_path):
    manifest = tmp_path / "manifest.md"
    row = (
        "| Identity key | Exam cycle | Exam date | Paper | Set | Official filename | "
        "Official archive/page URL | Official Drive URL | Drive file ID | Expected package type |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| key | Feb | 2026-02-08 | Paper I | B | p.zip | page | drive | ID1 | ZIP |\n"
    )
    manifest.write_text(row, encoding="utf-8")
    packages = load_packages(manifest)
    assert resolve_by_filename(packages, "p.zip", "B").set_name == "B"
    with pytest.raises(ManifestError):
        resolve_by_filename(packages, "missing.zip")


def test_duplicate_manifest_identity_rejected(tmp_path):
    manifest = tmp_path / "manifest.md"
    row = (
        "| Identity key | Exam cycle | Exam date | Paper | Set | Official filename | "
        "Official archive/page URL | Official Drive URL | Drive file ID | Expected package type |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n"
        "| key | Feb | date | Paper I | S | a.zip | page | drive | ID1 | ZIP |\n"
        "| key | Feb | date | Paper I | T | b.zip | page | drive | ID2 | ZIP |\n"
    )
    manifest.write_text(row, encoding="utf-8")
    with pytest.raises(ManifestError):
        load_packages(manifest)


def test_dry_run_does_not_download(tmp_path):
    destination = tmp_path / PACKAGE.filename
    result = acquire_with_gdown(PACKAGE, destination, dry_run=True)
    assert result == destination
    assert not destination.exists()


def test_evidence_is_deterministic_for_same_evidence(tmp_path):
    target = tmp_path / "test.zip"
    make_zip(target)
    evidence = validate_binary(target, PACKAGE)
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    write_evidence(evidence, a)
    write_evidence(evidence, b)
    assert a.read_text() == b.read_text()
