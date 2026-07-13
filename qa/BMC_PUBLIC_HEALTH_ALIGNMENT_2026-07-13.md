# BMC Public Health Alignment Audit

Date: 2026-07-13
Project: Regional HIV spatial patterns mapped across Ghanaian district boundaries
Target article type: BMC Public Health Research article

## Guideline Sources Checked

- BMC Public Health submission guidelines: https://link.springer.com/journal/12889/submission-guidelines
- BMC Public Health Research article guidelines: https://link.springer.com/journal/12889/submission-guidelines/research-article

## Journal Fit

The manuscript fits BMC Public Health better than the earlier Cambridge target. The journal explicitly covers epidemiology, infectious disease epidemiology, public health methods, social determinants of health, health behaviour, and public health informatics. The paper's strongest contribution is not a claim of district-resolved HIV prevalence. It is the transparent demonstration of what public Ghana DHS, Census, and boundary files can and cannot support when mapped across 261 district records.

BMC's stated editorial threshold is scientific validity, suitable methods, and adherence to field standards rather than perceived novelty alone. That is favourable for this paper because the manuscript is methodologically careful and openly states the ecological granularity constraint.

## Manuscript Structure

Status: PASS

- Title page includes article type, author, affiliation, ORCID, corresponding author, and reporting guideline.
- Abstract is structured as Background, Methods, Results, Conclusions.
- Abstract length: 255 words, below the 350-word BMC limit.
- Keywords: 10 listed, within the BMC range of 3 to 10.
- Main sections present: Background, Methods, Results, Discussion, Conclusions.
- List of abbreviations present.
- Declarations section present with all BMC-required subheadings.
- LLM-use disclosure is in Methods, matching BMC's instruction that LLM use should be documented and not treated as authorship.

## Tables And Figures

Status: PASS

- Seven manuscript tables detected.
- Blank table cells: 0.
- Tables are rebuilt as editable Word table objects in the BMC DOCX.
- Table titles are short and placed above the tables.
- Dashboard and poster now state 261 district records and name spatial error/GWR sensitivity checks.
- Figure files in `outputs/figures/` and `outputs/figures_cambridge/` are numbered Figure 1 to Figure 9 to match the manuscript legends and upload order.

## Submission Companion Materials

Status: PASS

- BMC-specific cover letter prepared in human editor-facing language: `submission_package/BMC_PUBLIC_HEALTH_SUBMISSION_2026-07-13/BMC_COVER_LETTER_TO_EDITOR_2026-07-13.md` and `.docx`.
- STROBE cross-sectional/ecological checklist completed and mapped to stable manuscript sections: `submission_package/BMC_PUBLIC_HEALTH_SUBMISSION_2026-07-13/STROBE_CROSS_SECTIONAL_CHECKLIST_2026-07-13.md` and `.docx`.
- BMC portal checklist prepared: `submission_package/BMC_PUBLIC_HEALTH_SUBMISSION_2026-07-13/BMC_PORTAL_SUBMISSION_CHECKLIST_2026-07-13.md` and `.docx`.
- Humanised BMC submission-readiness verdict prepared in the same folder.
- The companion files are BMC-specific and no longer rely on Cambridge-branded wording.

## Data Availability

Status: NEAR PASS

The manuscript and README point to the reproducible GitHub repository and machine-readable outputs. For full BMC strength, archive the exact submission version on Zenodo or another persistent repository and place the DOI/full HTTPS identifier in the manuscript Availability of data and materials section and reference list.

## Scientific Soundness

Status: STRONG

The paper is scientifically sound because it does three things reviewers usually ask for in ecological spatial work:

- It separates regional pass-through DHS variables from genuinely district-varying Census/geographic covariates.
- It reports spatial diagnostics and explains why spatial error is preferred over spatial lag.
- It avoids named-district targeting claims where the underlying HIV and behavioural estimates are regional.

The key inferential boundary is clear: this is a region-level HIV pattern displayed across district boundaries, with district-level socioeconomic sensitivity analyses. That honesty increases credibility.

## Final Fix Before Submission

Archive the exact submission repository state on Zenodo or another persistent repository and add the DOI/full HTTPS identifier to the Availability of data and materials section. This is the remaining improvement that would move the data-sharing layer from strong to exemplary.
