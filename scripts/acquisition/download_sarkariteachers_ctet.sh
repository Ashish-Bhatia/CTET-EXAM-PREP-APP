#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MANIFEST="$ROOT/docs/acquisition/sarkariteachers_ctet_manifest.csv"
BASE="$ROOT/data/acquisition/secondary/sarkariteachers"
PDF_DIR="$BASE/pdfs"
ARCHIVE="$BASE/ctet_sarkariteachers_papers.zip"

command -v python3 >/dev/null || { echo "ERROR: python3 is required" >&2; exit 1; }
command -v curl >/dev/null || { echo "ERROR: curl is required" >&2; exit 1; }

mkdir -p "$PDF_DIR"

python3 -m pip install --user -q gdown pypdf

python3 - "$MANIFEST" "$PDF_DIR" <<'PY'
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

manifest = Path(sys.argv[1])
out = Path(sys.argv[2])
rows = list(csv.DictReader(manifest.open(encoding="utf-8")))

if not rows:
    raise SystemExit("ERROR: manifest contains no records")


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._ -]+", "_", value).strip()

for i, row in enumerate(rows, 1):
    target = out / safe_name(row["filename"])
    if target.exists() and target.stat().st_size > 0:
        print(f"[{i}/{len(rows)}] EXISTS {target.name}")
        continue

    tmp = out / (target.name + ".download")
    if tmp.exists():
        tmp.unlink()

    print(f"[{i}/{len(rows)}] DOWNLOAD {row['filename']}")
    subprocess.run(
        [sys.executable, "-m", "gdown", "--id", row["google_drive_id"], "-O", str(tmp), "--fuzzy"],
        check=True,
    )

    if not tmp.exists() or tmp.stat().st_size == 0:
        raise SystemExit(f"ERROR: empty download for {row['filename']}")

    tmp.replace(target)

print("Validating PDF signatures, readability and SHA-256...")
from pypdf import PdfReader

hash_manifest = out / "sha256_manifest.csv"
with hash_manifest.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["filename", "size_bytes", "sha256", "pdf_pages"])

    for pdf in sorted(out.glob("*.pdf")):
        data = pdf.read_bytes()
        if not data.startswith(b"%PDF"):
            raise SystemExit(f"ERROR: invalid PDF signature: {pdf.name}")

        try:
            pages = len(PdfReader(str(pdf), strict=False).pages)
        except Exception as exc:
            raise SystemExit(f"ERROR: unreadable PDF {pdf.name}: {exc}")

        if pages < 1:
            raise SystemExit(f"ERROR: zero-page PDF: {pdf.name}")

        digest = hashlib.sha256(data).hexdigest()
        writer.writerow([pdf.name, len(data), digest, pages])
        print(f"OK {pdf.name} | pages={pages} | sha256={digest}")

actual = len(list(out.glob("*.pdf")))
expected = len(rows)
print(f"Downloaded PDF count: {actual}")
print(f"Manifest record count: {expected}")

if actual != expected:
    raise SystemExit(f"ERROR: expected {expected} PDFs, found {actual}")
PY

rm -f "$ARCHIVE"
(
    cd "$BASE"
    zip -q -r "$(basename "$ARCHIVE")" pdfs
)

printf '\nZIP integrity:\n'
unzip -t "$ARCHIVE"

printf '\nZIP SHA-256:\n'
sha256sum "$ARCHIVE"

printf '\nAcquisition complete.\n'
printf 'PDF directory: %s\n' "$PDF_DIR"
printf 'SHA-256 manifest: %s\n' "$PDF_DIR/sha256_manifest.csv"
printf 'ZIP archive: %s\n' "$ARCHIVE"
printf '\nIMPORTANT: Sarkari Teachers is a secondary source. These binaries do not satisfy OFFICIAL_BINARY_VERIFIED.\n'
