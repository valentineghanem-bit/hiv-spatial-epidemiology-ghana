# Q1 Editorial Review - Project 2
Date: 2026-07-12

## Bottom Line
Do not submit today without one targeted revision round.

The project is scientifically interesting and much stronger than a routine dashboard manuscript because it openly documents the corrected spatial pipeline, the 261-district/260-polygon reconciliation, the region-level DHS granularity problem, and sensitivity analyses restricted to genuinely district-level covariates. That transparency is a real strength.

But the current article is not yet clean Q1 standard as framed. The main empirical object is not independent district-level HIV prevalence. HIV prevalence has only 9 distinct DHS regional values across 261 districts; VCT uptake and wife-beating acceptance are also regional DHS pass-through variables. Therefore the title, abstract, dashboard, and poster must stop letting "261 districts" read as independent district inference.

## Journal Fit
Epidemiology & Infection fits the infectious-disease epidemiology topic and welcomes applied surveillance, statistics, data science, and AI work when it has regional or global relevance. The weakness is that the study is not truly district-resolved surveillance; it is ecological regional evidence rendered on district geometry. Cambridge source: https://www.cambridge.org/core/journals/epidemiology-and-infection/information/author-instructions

PLOS Global Public Health is the better first target because it explicitly values public-health inequity, methodological rigor, open data/code, and research across regional boundaries. It screens for original research, technical standard, conclusions supported by data, ethics, reporting guidelines, and data availability. PLOS sources: https://journals.plos.org/globalpublichealth/s/journal-information and https://journals.plos.org/globalpublichealth/s/what-we-publish

## Grade
Current grade: B / borderline Q1.

After one focused revision round: B+ for PLOS Global Public Health; B for Epidemiology & Infection.

Not A-level yet because the empirical novelty is moderate and the main outcome granularity limits causal and district-level inference.

## Acceptance Odds
- PLOS Global Public Health, if submitted now: 30-45%.
- PLOS Global Public Health, after targeted reframing: 45-60%.
- Epidemiology & Infection, if submitted now: 15-25%.
- Epidemiology & Infection, after targeted reframing: 25-35%.

Ranked target recommendation:
1. PLOS Global Public Health.
2. Epidemiology & Infection.
3. BMC Public Health / PLOS ONE as safer fallbacks if Q1 speed matters less than acceptance probability.

## Major Scientific Verdict
Scientifically sound if framed as:
"A transparent ecological spatial mapping and sensitivity analysis of Ghana's regional DHS HIV estimates rendered across district boundaries."

Not scientifically sound if framed as:
"A district-level determinant discovery study identifying actionable district HIV hotspots."

Claims that survive:
- Ghana's HIV burden has a strong south-north regional gradient.
- LISA/Gi* maps are useful visual summaries of regional structure on district geometry.
- VCT uptake and wife-beating acceptance are strong full-model regional correlates, not district-level causes.
- Region-level VCT prioritisation in Eastern, Greater Accra, Western, and Western North is defensible.
- District-specific targeting should wait for district-resolved surveillance or small-area-estimation evidence.

## Submission Blockers
- Title and running claims still over-index on "261 districts."
- Dashboard/poster previously had stale source labels and SHAP/model labels; patched during this audit.
- The poster and dashboard must keep the caveat visible near the top, not only in discussion text.
- The cover letter must pre-emptively explain the ecological design instead of waiting for Reviewer 2 to discover it.
- The old repo-only `QA_PASSED_2026-07-12.txt` says "publication ready"; manuscript-readiness is more cautious and should be governed by this report.

## QA Notes
- Test suite: passed, 29/29.
- DOCX structural QA: 120 paragraphs, 6 tables, 9 inline shapes; visible question-mark artifacts not found in text extraction.
- DOCX render QA: not completed because `soffice`/LibreOffice was unavailable in this environment.
- In-app browser visual QA: blocked by browser URL policy for local `file://` pages. Static HTML checks were completed instead.
- Static artifact QA after patches: no Plotly/Chart.js/D3/CDN scripts, no DHIMS2/GHS/WorldPop source mismatch, stale dashboard SHAP labels removed, poster caveat present.

## One Priority Action
Rewrite the title, abstract opening, and first dashboard/poster subtitle so the limitation is title-level: "regional DHS HIV estimates mapped to Ghana's district boundaries." Then submit to PLOS Global Public Health first.
