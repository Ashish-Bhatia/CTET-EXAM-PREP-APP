# Phase Gates

## Phase 1, Official Examination Research

### Milestone 1, Examination Specification

Status: IN PROGRESS

Entry condition:

- Repository foundation exists and is validated.
- Codespace synchronization is tracked separately from examination-specification acceptance. A historical synchronization record does not constitute current-HEAD synchronization evidence.

Required acceptance evidence:

A. Required examination specification

- Applicable current CTET/CBSE Information Bulletin identified by cycle, title, source and effective/research date.
- Paper I and Paper II purpose and target classes verified.
- Counts, marks, duration, MCQ format and marking rules verified.
- Section/subject structure verified for both papers.
- Language options, codes and Language I/II relationship verified.
- Main question-paper language/medium rule verified.
- Qualifying marks and certificate validity verified.
- Examination schedule and relevant conduct/reporting workflow verified.
- OMR/response mechanics and candidate-facing workflow researched from official sources where published.
- Official syllabus and appendix content inventoried at the specification level.
- Current-cycle notices checked for changes or superseding instructions.
- Historical versus current rules explicitly separated.
- Unverified items explicitly recorded and classified.

B. Deferred paper-presentation evidence, non-blocking for Phase 1

- Exact printed question-number ranges.
- Printed section boundaries and sequencing.
- Passage numbering.
- Question-set numbering.
- Set-specific visual layout.
- Pagination and other printed layout details.

Items in category B remain UNVERIFIED until authoritative current-cycle question-paper evidence is published. They are downstream paper-presentation attributes and must not be used as a reason to declare Milestone 1 incomplete.

Exit condition:

- All required specification areas in category A are documented with authoritative provenance.
- Category B paper-presentation evidence is explicitly classified as UNVERIFIED where unavailable and is NON-BLOCKING for Phase 1.
- No material rule is based solely on secondary sources where official evidence exists.
- Phase 2 acquisition gate is explicitly approved in the repository records.

### Phase 2 gate, Official Binary Acquisition and Verification

LOCKED until Phase 1 exit condition is satisfied and explicit approval is recorded.

Permitted only after explicit approval:

- Binary acquisition of official CTET packages.
- SHA-256 calculation from actual bytes.
- ZIP/package validation.
- Provenance and identity verification.
- Extraction and inventory.

Required binary state:

OFFICIAL_PAGE_ONLY -> BINARY_ACQUIRED -> HASHED -> ZIP_VALIDATED -> OFFICIAL_BINARY_VERIFIED -> EXTRACTED -> INVENTORIED -> READY_FOR_ANALYSIS

## Phase 3, Extraction, Inventory and Segmentation

LOCKED until Phase 2 binaries are verified.

## Phase 4, Answer-Key Mapping and Structural Validation

LOCKED until Phase 3 outputs exist and are validated.

## Phase 5, Historical Corpus and Statistical Analysis

LOCKED until official paper and answer-key corpus is validated.

Historical topic distributions must be classified as ANALYTICAL ESTIMATE unless officially published by CBSE.

## Phase 6, Question-Bank and Blueprint Engine

LOCKED until Phase 5 evidence supports its constraints.

## Phase 7, UX/UI and Examination Simulator

LOCKED from implementation until the examination specification and required workflow rules are accepted.

## Phase 8, Application Implementation

LOCKED until upstream specification, corpus and blueprint gates are passed.

## Phase 9, Automated Testing and Validation

LOCKED until implementation exists.

## Phase 10, Production Readiness

LOCKED until required application and validation evidence exists.

## Global prohibition

No gate may be bypassed by assumption, secondary-source convenience, metadata-only acquisition, guessed hashes, inferred binaries or generated examination content.
