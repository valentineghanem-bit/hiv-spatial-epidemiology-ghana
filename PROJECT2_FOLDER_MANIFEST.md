# Project 2 Folder Manifest
Date: 2026-07-12

## Canonical Root
`2. Spatial Epidemiology of HIV in Ghana`

## Current Canonical Structure
- `manuscript/` - active article files.
  - `HIV_Spatial_Epidemiology_Ghana_Manuscript_FINAL.docx`
  - `HIV_Spatial_Epidemiology_Ghana_Manuscript_DRAFT.md`
- `dashboard/` - live dashboard artifacts.
  - `HIV_Spatial_Ghana_Dashboard.html`
  - `app.py`
  - platform launcher scripts.
- `poster/` - live poster artifact.
  - `HIV_Spatial_Ghana_Poster.html`
- `data/raw/` - raw spatial geometry.
- `docs/` - crosswalk and documentation files.
- `Master/` - master analytical CSV copy.
- `outputs/data/` - analysis outputs used for manuscript and artifact checks.
- `outputs/figures/` - manuscript figure PNGs.
- `analysis/` - reproducible spatial/ML pipeline.
- `tests/` - executable QA tests.
- `qa/` - active QA reports and editorial review outputs.
- `submission_package/Q1_EDITORIAL_AUDIT_2026-07-12/` - rebuilt submission-readiness package for this audit.
  - `manuscript/`
  - `dashboard/`
  - `poster/`
  - `data/`
  - `figures/`
  - `qa/`
  - `README.md`
  - `CITATION.cff`

## Rebuild Notes
Original files were preserved. The rebuilt folder system creates one clear package for Q1 editorial review without deleting root artifacts needed by the repo.

## Submission Rule
Do not treat `QA_PASSED_2026-07-12.txt` as a manuscript-submission green light. It was repo-only QA. Use `qa/Q1_EDITORIAL_REVIEW_2026-07-12.md` and `qa/EPID_COUNCIL_VERDICT_2026-07-12.md` for submission decisions.
