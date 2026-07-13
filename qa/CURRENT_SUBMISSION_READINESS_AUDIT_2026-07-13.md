# Current Submission-Readiness Audit
Date: 2026-07-13

## Verdict

Confidence: HIGH for local file QA; MEDIUM for journal-acceptance probabilities.

Current folder status: **A / S-minus for the manuscript; B+ for the whole submission package; not yet S+ as a folder.**

The manuscript has materially improved since the earlier audit. The new GWR and spatial-error additions are present in the Markdown draft and final DOCX, and they make the paper more scientifically honest because they directly expose the regional-to-district granularity problem instead of hiding it. The scientific core is now defensible as an ecological spatial-pattern and methods-transparency paper.

It is **not yet S+ submission-ready as a complete package** because README, dashboard, and poster have not been updated to reflect the final GWR/spatial-error framing, and the DOCX does not show a verifiable page-number field in the file internals. Cambridge also expects strict manuscript preparation compliance and may return nonconforming files without review.

## Evidence Checked

- Manuscript draft: `manuscript/HIV_Spatial_Epidemiology_Ghana_Manuscript_DRAFT.md`
- Final DOCX/PDF: `manuscript/HIV_Spatial_Epidemiology_Ghana_Manuscript_FINAL.docx` and `.pdf`
- README: `README.md`
- Dashboard: `dashboard/HIV_Spatial_Ghana_Dashboard.html`
- Poster: `poster/HIV_Spatial_Ghana_Poster.html`
- New outputs: `outputs/data/gwr_spatial_error_metadata.txt`, `spatial_error_model_results.csv`, `gwr_coefficient_summary.csv`, `gwr_local_r2.csv`
- Test suite: `python -m pytest -q` -> **29 passed**

## Cambridge Compliance

Observed strengths:

- Title is short and specific: 9 words.
- Summary paragraph is 199 words, within Cambridge's 150-200 word requirement.
- Main text is approximately 3,101 words from Introduction through Conclusion, within the preferred 2,000-4,000 range for Original Papers.
- References: 19, below Cambridge's preferred ceiling of 40.
- Tables are placed after the main text, and figure legends are grouped after tables.
- DOCX internals show double spacing, line numbering, and 1-inch margins.
- Declarations cover data/code availability, funding, competing interests, ethics, and AI assistance.

Remaining Cambridge risks:

- Page numbers were not verifiably present as visible DOCX footer/page fields. The file contains page-number settings but no `PAGE` field or footer XML detected.
- Figures exist as PNG only. PNG is acceptable at initial submission, but Cambridge revised-submission production expects TIF/EPS at required resolution.
- The title page still contains working metadata (`Target journal`, `Reporting guideline`, approximate word count). This should be cleaned before upload.
- The final PDF/DOCX should receive a visual render check in Word or LibreOffice before submission.

Official Cambridge policy anchors: summary 150-200 words, Original Papers preferably 2,000-4,000 words with fewer than 40 references, line/page numbering, tables at the end, and figure-format rules are from Cambridge Epidemiology & Infection author instructions: https://www.cambridge.org/core/journals/epidemiology-and-infection/information/author-instructions/preparing-your-materials

## Scientific Soundness

Grade: **A-minus**

The current science is coherent if framed as regional DHS HIV estimates mapped onto district boundaries, not true independent district-level HIV surveillance. The strongest methodological improvement is the explicit GWR failure for regionally constant predictors, followed by a district-varying predictor GWR sensitivity model. This turns the main limitation into a transparent analytical finding.

Key verified results:

- Spatial error lambda = 0.9232; pseudo-R2 = 0.8077.
- Robust LM-error = 182.4, p < 0.001; robust LM-lag = 4.6, p = 0.032.
- District-varying GWR R2 = 0.9563; OLS R2 on same predictors = 0.8400.
- GWR local R2 range = -0.0879 to 0.8802, showing local instability in some areas.
- Test suite passed: 29/29.

Main scientific caution:

The outcome still has only nine distinct DHS regional HIV values across 261 district rows. This is not fatal because the manuscript now discloses it clearly, but it means all district-named conclusions must remain descriptive or hypothesis-generating. Any wording that implies confirmed district-level prevalence differences would weaken the paper.

## Cross-Artifact Sync

Grade: **B**

The manuscript is ahead of the public-facing materials.

Mismatch findings:

- README still uses the older title and subtitle: "Subnational Spatial Epidemiology..." and "Bivariate LISA, Spatial Lag Regression, and Random Forest - 261-District DHS Analysis."
- README does not include the new GWR/spatial-error results.
- Dashboard has 0 mentions of GWR and 0 mentions of spatial error.
- Poster has 0 mentions of GWR and 0 mentions of spatial error.
- Dashboard/poster still foreground Random Forest/SHAP and spatial lag. Those can remain, but they should no longer be the dominant final-method story.

Required S+ repair:

1. Rename README framing to match the manuscript: regional HIV spatial patterns mapped across district boundaries.
2. Add the spatial-error and GWR sensitivity results to README, dashboard, and poster.
3. Reduce dashboard/poster emphasis on district-level implication.
4. Export final figures as Cambridge-ready TIF/EPS if moving beyond initial submission.
5. Verify visible page numbers in the DOCX/PDF.

## Journal Ranking

1. **PLOS Global Public Health** - best fit if repository/data/code transparency is central. Estimated current odds: **45-55%**; after sync/format fixes: **55-65%**. PLOS explicitly prioritises original, technically sound research with conclusions supported by data and reporting/data availability standards: https://journals.plos.org/globalpublichealth/s/criteria-for-publication

2. **BMC Public Health** - strongest scope fit for public health, social determinants, infectious disease epidemiology, and methods-validity over perceived novelty. Estimated current odds: **45-55%**; after fixes: **55-65%**. BMC Public Health states that editorial decisions are based on scientific validity and suitable methods, not perceived impact: https://link.springer.com/journal/12889/aims-and-scope

3. **Cambridge Epidemiology & Infection** - plausible but more selective on infectious-disease epidemiology contribution and manuscript conformity. Estimated current odds: **35-45%**; after final sync/format fixes: **45-55%**. The paper is now within scope, but the novelty is methods-transparency and Ghana subnational mapping rather than new surveillance data.

## S+ Status

Not S+ today.

Current status: **S-minus manuscript, B+ package, submit-after-final-fix.**

The work is scientifically sound enough to submit after small but important production fixes. It is not yet a clean "send today" package because the live README/dashboard/poster lag behind the manuscript and the DOCX page-number/visual render check remains unresolved.
