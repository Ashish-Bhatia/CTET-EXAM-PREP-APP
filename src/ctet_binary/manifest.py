from __future__ import annotations

from pathlib import Path

from .models import PackageIdentity


class ManifestError(ValueError):
    pass


def load_packages(path: str | Path) -> list[PackageIdentity]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    packages: list[PackageIdentity] = []
    seen: set[str] = set()
    header_seen = False
    for line in lines:
        if line.startswith("| Identity key | Exam cycle | Exam date | Paper | Set | Official filename |"):
            header_seen = True
            continue
        if not header_seen or not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 10:
            continue
        identity_key, cycle, date, paper, set_name, filename, page_url, drive_url, drive_id, package_type = cells[:10]
        if identity_key in seen:
            raise ManifestError(f"duplicate identity key: {identity_key}")
        seen.add(identity_key)
        packages.append(
            PackageIdentity(
                identity_key=identity_key,
                exam_cycle=cycle,
                exam_date=date,
                paper=paper,
                set_name=set_name,
                filename=filename,
                drive_file_id=drive_id,
                official_page_url=page_url,
                official_drive_url=drive_url,
                expected_package_type=package_type,
            )
        )
    return packages


def resolve_by_filename(
    packages: list[PackageIdentity], filename: str, set_name: str | None = None
) -> PackageIdentity:
    matches = [
        p for p in packages
        if p.filename == filename and (set_name is None or p.set_name == set_name)
    ]
    if len(matches) != 1:
        raise ManifestError(f"expected exactly one package, found {len(matches)}")
    return matches[0]


def expected_local_filename(package: PackageIdentity) -> str:
    return package.filename
