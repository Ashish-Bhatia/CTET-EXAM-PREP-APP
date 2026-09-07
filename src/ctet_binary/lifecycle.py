from enum import StrEnum


class LifecycleState(StrEnum):
    OFFICIAL_PAGE_ONLY = "OFFICIAL_PAGE_ONLY"
    BINARY_ACQUIRED = "BINARY_ACQUIRED"
    HASHED = "HASHED"
    ZIP_VALIDATED = "ZIP_VALIDATED"
    OFFICIAL_BINARY_VERIFIED = "OFFICIAL_BINARY_VERIFIED"
    EXTRACTED = "EXTRACTED"
    INVENTORIED = "INVENTORIED"
    READY_FOR_ANALYSIS = "READY_FOR_ANALYSIS"


ORDER = tuple(LifecycleState)


def advance(current: LifecycleState, target: LifecycleState) -> LifecycleState:
    if ORDER.index(target) < ORDER.index(current):
        raise ValueError(f"Lifecycle cannot move backwards: {current} -> {target}")
    return target
