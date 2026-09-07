from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from .lifecycle import LifecycleState


@dataclass(frozen=True)
class PackageIdentity:
    identity_key: str
    exam_cycle: str
    exam_date: str
    paper: str
    set_name: str
    filename: str
    drive_file_id: str
    official_page_url: str
    official_drive_url: str
    expected_package_type: str = "ZIP"


@dataclass(frozen=True)
class SourceProvenance:
    official_page_url: str
    official_drive_url: str
    drive_file_id: str
    source_verified: bool = True


@dataclass
class BinaryEvidence:
    package: PackageIdentity
    lifecycle: LifecycleState
    local_file: str | None = None
    acquisition_timestamp: str | None = None
    byte_size: int | None = None
    sha256: str | None = None
    zip_valid: bool = False
    crc_valid: bool = False
    member_inventory: list[dict[str, Any]] = field(default_factory=list)
    provenance: SourceProvenance | None = None
    diagnostics: list[str] = field(default_factory=list)

    @classmethod
    def acquired(
        cls, package: PackageIdentity, local_file: str, byte_size: int
    ) -> "BinaryEvidence":
        return cls(
            package=package,
            lifecycle=LifecycleState.BINARY_ACQUIRED,
            local_file=local_file,
            acquisition_timestamp=datetime.now(timezone.utc).isoformat(),
            byte_size=byte_size,
            provenance=SourceProvenance(
                package.official_page_url, package.official_drive_url, package.drive_file_id
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["lifecycle"] = self.lifecycle.value
        return value
