# Repository Foundation

## Scope

This milestone establishes the engineering foundation only.

Included:

- reproducible Codespaces environment
- pinned development dependencies
- Python package layout
- automated CI
- architecture guardrails
- baseline tests

Excluded:

- CTET package acquisition
- source-document processing
- OCR and extraction
- question or answer analysis
- analytics and blueprinting
- mock generation
- application features

## Branching

`main` is the stable branch. `develop` is the integration branch. Work is performed on `feature/*` branches and merged through pull requests.

## Data boundary

Raw exam artifacts and derived datasets are not committed by default. Their future lifecycle requires an explicit provenance and storage design before acquisition begins.
