# QA AUDIT REPORT — Project 2: HIV Spatial Epidemiology Ghana
**Date:** 2026-07-12 | **Protocol:** QA v2.0, adapted for a repo-only deliverable (no manuscript file present in this repository)
**Trigger:** Pre-publication epid-council + QA request. Supersedes QA_HIV_Spatial_Ghana_2026-04-30.md, which certified a spatial pipeline later found to be corrupted (see DATA_CORRECTION_NOTE.md).

## Panel Scores (1–5, adapted to available deliverables)

| Panel | Dimension | Score | Notes |
|-------|-----------|-------|-------|
| 1 | Structural Completeness | 5 | README/CITATION.cff/sync-manifest/Master CSV/dashboard/poster/tests/DATA_CORRECTION_NOTE.md all present and cross-consistent |
| 2 | Scientific Rigour | 5 | Full spatial pipeline (Moran's I, LISA, Bivariate LISA, Getis-Ord, spatial lag) + ML (LASSO, RF/SHAP) rebuilt from a validated 261-district join; fixed seed=42 |
| 3 | Statistical Accuracy | 5 | 261 districts confirmed unique (was 250 unique w/ 10 contradictory duplicates pre-fix); own-value sanity check passed (HH mean 2.73% vs LL mean 0.41%); regression-guard tests added for the pre-fix Getis-Ord null-result bug |
| 4 | Citation Quality | N/A | No manuscript/bibliography in this repo |
| 5 | Language Quality | 5 | Poster/README prose corrected for a backwards north/south burden-direction claim and a lowercase "hiv" formatting slip |
| 6 | Facts Verification | 5 | All headline stats cross-verified against source CSVs (Morans_I_Results.csv, LISA_Results.csv, Getis_Ord_Results.csv, model_comparison.csv, shap_summary.csv) — see numeric spot-check below |
| 7 | Logical Coherence | 4 | Region-level-granularity limitation for HIV/VCT/wife-beating variables now disclosed prominently (was previously buried in a data-source table only); flagged by 5-advisor council, COUNCIL-141 |
| 8 | Scholarly Citation Audit | N/A | No manuscript in this repo |
| 9 | Q1 Journal Alignment | N/A | This deliverable is the GitHub repo, not the manuscript |
| 10 | Open Science Integrity | 5 | Full reproducible pipeline (`analysis/spatial_analysis_pipeline.py`), raw geometry (`data/raw/`), and crosswalk (`docs/`) committed; DATA_CORRECTION_NOTE.md discloses the pre-publication fix transparently |
| 11 | STROBE Compliance | 4 | Ecological-design/MAUP limitation now explicit in README; recommend the eventual manuscript's Limitations section incorporate the same disclosure |
| 12 | Cross-Artefact Consistency | 5 | README, CITATION.cff, sync-manifest.json, dashboard, poster, Master CSV all report identical N=261, Moran's I=0.920, LISA 59 HH/51 LL/4 HL, RF R²=0.611, LASSO R²=0.933 |
| 13 | Test Suite Integrity | 5 | Rewrote `tests/test_hiv_spatial.py`: previous version's "canonical value" tests compared hardcoded constants to themselves and could never fail; now loads and asserts against real output CSVs (29/29 passing) |
| 14 | Editorial Decision | **PASS** | See verdict below |

## Numeric Spot-Check (source file -> deliverable)

| Statistic | Source file value | README | Dashboard | Poster | CITATION.cff |
|---|---|---|---|---|---|
| N districts | 261 (Master CSV rows) | 261 | 261 | 261 | 261 |
| Global Moran's I | 0.9201 (Morans_I_Results.csv) | 0.920 | 0.92 | 0.92 | 0.920 |
| LISA HH / LL / HL | 59 / 51 / 4 (LISA_Results.csv) | 59/51/4 | 59 (HH card) | 59 (HH) | — |
| Getis-Ord hot/cold | 53 / 53 (Getis_Ord_Results.csv) | 53/53 | — | — | — |
| LASSO R² | 0.9328 (model_comparison.csv) | 0.933 | — (poster: 93%) | 93% | — |
| RF R² | 0.6108 (model_comparison.csv) | 0.611 | 0.61 | 0.61 | — |
| Top SHAP feature | VCT_Women_pct, 0.639 (shap_summary.csv) | VCT uptake | VCT uptake | VCT uptake | VCT uptake (|SHAP|=0.639) |

All spot-checked figures trace correctly. No orphaned or contradictory numbers found across deliverables (contrast with the pre-fix state, where README/JSON/CSV each reported a different, mutually-inconsistent LISA significant-cluster count).

## Fixes Applied This Session

- [x] **Critical:** rebuilt the entire spatial statistics pipeline (Moran's I, LISA, Bivariate LISA, Getis-Ord Gi*, spatial lag regression) from a corrupted district-geometry join that had produced 10 duplicate districts with contradictory results and silently dropped 11 real districts. Root cause, before/after audit: `DATA_CORRECTION_NOTE.md`.
- [x] Deleted the superseded, broken `analysis/build_master_dataset.py`; replaced with `analysis/spatial_analysis_pipeline.py`, portable and self-contained (`docs/`, `data/raw/` added).
- [x] Regenerated `fig4_lisa_cluster_map.png` and `fig5_morans_scatterplot.png` from corrected data; other figures unaffected, left untouched.
- [x] Fixed a Plotly-CDN dependency violation in dashboard/poster (already partially fixed pre-session but uncommitted); both now vanilla-JS + inline-SVG, dashboard 60,336 bytes / poster 38,930 bytes (60 KB ceiling).
- [x] Replaced extensively fabricated placeholder data in the dashboard (`DDATA`, `REGION`, `GI_TIERS`, `SC_PTS` — flat placeholder values, a Getis-Ord panel mislabeled with LISA quadrant categories) and poster (a fictitious "Logistic Reg AUC 67%" / "Gi* accuracy 61%" model-performance panel, and a SHAP ranking with numbers that matched no actual model output) with values traced to the real corrected output files.
- [x] Corrected a factual error in the poster Discussion ("Northern regions bear disproportionate burden" — backwards; the corrected data shows the *southern* belt as the High-High/hotspot cluster).
- [x] 5-advisor epid-council review (COUNCIL-141) surfaced and fixed an undisclosed region-level-granularity limitation (HIV prevalence, VCT uptake, and wife-beating acceptance are DHS regional estimates, not independent district measurements) — added prominent disclosure to README/dashboard/poster and reframed the poster's policy recommendation from district-level to region-level targeting.
- [x] Rewrote `tests/test_hiv_spatial.py` to assert against real output files instead of comparing hardcoded constants to themselves (29/29 tests passing).
- [x] Updated CITATION.cff (version 1.0.1, date-released 2026-07-12) and sync-manifest.json to N=261 and the corrected scope description.

## Open Items (Low Priority, not blocking)

- [ ] `requirements.txt` uses exact `==` pins rather than `>=` minimums (a style deviation from newer sibling repos' CI-installability convention, not a known breakage — not verified against live CI since no `gh` CLI credential is configured in this environment).
- [ ] No manuscript file exists in this repository to audit (consistent with the "no manuscripts committed to any repo" rule — if/when a manuscript is drafted, it must incorporate the same region-level-granularity Limitations disclosure).
- [ ] Repo has not yet been pushed to GitHub; local commit only, pending user confirmation to push.

## Publication Readiness

**PASS — repo-only deliverable, pending user confirmation to commit/push.** All identified data-integrity and disclosure defects were fixed as executable artefacts (re-run analysis, corrected files) rather than deferred. This QA pass supersedes and invalidates QA_HIV_Spatial_Ghana_2026-04-30.md.
