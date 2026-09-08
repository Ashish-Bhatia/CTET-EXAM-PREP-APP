#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from ctet_binary.acquisition import acquire_with_gdown
from ctet_binary.manifest import load_packages, resolve_by_filename
from ctet_binary.validation import validate_binary, write_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire and verify an official CTET ZIP.")
    parser.add_argument("--manifest", default="docs/acquisition/ACQUISITION_MANIFEST.md")
    parser.add_argument("--filename", required=True)
    parser.add_argument("--set", dest="set_name")
    parser.add_argument("--output-dir", default="data/official/feb-2026")
    parser.add_argument("--evidence")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    package = resolve_by_filename(load_packages(args.manifest), args.filename, args.set_name)
    destination = Path(args.output_dir) / package.filename
    acquire_with_gdown(package, destination, dry_run=args.dry_run)
    if args.dry_run:
        print(f"DRY_RUN {destination}")
        return 0
    evidence = validate_binary(destination, package)
    output = Path(args.evidence or f"reports/binary/{destination.stem}.json")
    write_evidence(evidence, output)
    print(f"SHA256 {evidence.sha256}")
    print(f"LIFECYCLE {evidence.lifecycle.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
