# BMC Public Health Submission Verdict

Date: 2026-07-13
Project: Regional HIV spatial patterns mapped across Ghanaian district boundaries

## Bottom Line

This is now a BMC Public Health-ready submission package.

I would not sell it as a district-level HIV prevalence paper. That would invite rejection. The stronger and more defensible framing is the one now used in the manuscript: a national ecological spatial analysis showing the south-north HIV gradient across 261 Ghana census district records while explicitly testing the limits of regional DHS variables mapped onto district boundaries.

That honesty is the paper's strength. It turns a potential fatal limitation into the scientific contribution.

## Grade

Current grade: S / near-S+

Not full S+ until the exact submission repository is archived with a persistent DOI or equivalent identifier and the DOI is added to the Availability of data and materials section. BMC strongly values open, reusable, citable data. GitHub is good; a versioned archive is better.

## Acceptance Odds

Estimated BMC Public Health odds:

- Desk/editorial screening: 85-90%
- Sent for peer review: 75-85%
- Acceptance after revision: 60-70%
- Acceptance without revision: unlikely; expect reviewer requests around ecological inference, DHS granularity, and data archiving

These odds assume the final submission keeps the conservative wording and does not overclaim district-level HIV measurement.

## Scientific Readiness

Scientific soundness: strong

The paper uses a sensible multi-method spatial framework: Moran's I, LISA, Getis-Ord Gi*, spatial lag/error modelling, GWR sensitivity analysis, LASSO, Random Forest, SHAP, and spatially conservative validation. The methods now support the conclusion rather than outrunning it.

Logical coherence: strong

The manuscript now has a clean chain:

1. HIV prevalence appears spatially patterned across mapped district records.
2. That pattern is partly real at regional level and partly shaped by regional DHS granularity.
3. Spatial error is preferred over spatial lag by diagnostics.
4. GWR fails when regionally constant predictors are forced into local district models.
5. District-only predictors still show spatial structure, but not enough to justify named-district HIV targeting.

New knowledge: moderate to strong

The new contribution is not that Ghana has HIV spatial heterogeneity. That is expected. The contribution is the Ghana-specific, reproducible, 261-record audit of how public DHS/Census/GSS data behave under modern spatial and interpretable-ML workflows, with the granularity problem shown rather than merely mentioned.

## QA Status

PASS

- Manuscript follows BMC Research article structure.
- Abstract is structured and below 350 words.
- Keywords reduced to 10.
- BMC-required Declarations subheadings are present.
- LLM-use disclosure is included in Methods.
- Manuscript tables: 7.
- Blank manuscript table cells: 0.
- DOCX uses editable Word tables, double spacing, line numbering, and page numbering.
- Dashboard and poster render in Chrome with no page or console errors.
- Dashboard and poster both show 261 districts.
- Dashboard and poster both expose spatial error and GWR wording.
- Test suite: 29 passed.

## Remaining S+ Action

Before pressing submit, create a Zenodo release or equivalent archive for the exact repository state and add the DOI to the manuscript. That is the last high-value upgrade.
