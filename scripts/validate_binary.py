#!/usr/bin/env python3
from __future__ import annotations

import argparse

from ctet_binary.manifest import load_packages, resolve_by_filename
from ctet_binary.validation import validate_binary, write_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an acquired CTET ZIP.")
    parser.add_argument("--manifest", default="docs/acquisition/ACQUISITION_MANIFEST.md")
    parser.add_argument("--filename", required=True)
    parser.add_argument("--set", dest="set_name")
    parser.add_argument("--file", required=True)
    parser.add_argument("--evidence")
    args = parser.parse_args()

    package = resolve_by_filename(load_packages(args.manifest), args.filename, args.set_name)
    evidence = validate_binary(args.file, package)
    output = args.evidence or f"reports/acquisition/{args.filename}.json"
    write_evidence(evidence, output)
    print(f"SHA256 {evidence.sha256}")
    print(f"LIFECYCLE {evidence.lifecycle.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
