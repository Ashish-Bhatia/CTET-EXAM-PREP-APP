# CTET Exam Prep App

A controlled, evidence-driven platform for CTET preparation.

## Branch policy

- `main`: stable, reviewed code only.
- `develop`: integration branch.
- `feature/*`: isolated implementation work.

No direct development occurs on `main` or `develop`.

## Foundation

The repository foundation establishes reproducible development, automated validation, package layout, and architecture checks. CTET source acquisition and exam-content processing are intentionally absent from this milestone.

## Development

Use the repository devcontainer. Install development dependencies with:

```bash
python -m pip install -r requirements-dev.txt
```

Run validation with:

```bash
python -m pip check
python -m compileall -q src scripts tests
python -m pytest
python scripts/check_architecture.py
python -m ruff check .
```
