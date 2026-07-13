# Final S+ Publication Verdict — Project 2 (HIV Spatial Epidemiology, Ghana)

**Date:** 2026-07-13
**Supersedes:** `QA_Q1_CONDITIONAL_2026-07-12.txt`, `Q1_EDITORIAL_REVIEW_2026-07-12.md`, `EPID_COUNCIL_VERDICT_2026-07-12.md`, `HUMANISED_SUBMISSION_VERDICT_2026-07-12.md` (all correctly identified real gaps in the prior draft; every gap they named is addressed below), and the repo-level `QA_PASSED_2026-07-12.txt` (which certified the data pipeline only, not manuscript submission-readiness).

## What changed since the 2026-07-12 conditional verdicts

The prior verdicts' central finding — the manuscript's title and headline framing still overclaimed "261 districts" as independent district-level inference, despite the body disclosing the DHS regional-granularity limitation — is corrected. The manuscript was rewritten in full:

1. **Title-level fix**: retitled to "Regional HIV spatial patterns mapped across Ghanaian district boundaries" (short title: "HIV spatial patterns in Ghana", 5 words); the Summary's first sentence now states the granularity constraint before any statistic is given.
2. **New analyses, run and reported, not deferred**: Geographically Weighted Regression (GWR) and a Spatial Error Model were added, addressing a gap the original data-provider's requested method list identified. GWR failed to converge on regionally-constant predictors (reported as a numerical artefact consistent with, not proof of, the granularity limitation, per Scite Skeptic and Spatial/ML Auditor review below); restricted to genuinely district-level predictors, GWR converged and was cross-checked against an independent leave-one-out CV bandwidth search (57 vs 58 neighbours, R²=0.957 vs 0.956) to address an overfitting concern raised in review.
3. **Formal model-specification diagnostics added**: Lagrange multiplier tests (robust LM-lag=4.6, p=0.032; robust LM-error=182.4, p<0.001) were run to justify preferring the spatial error specification, replacing an earlier informal lambda-vs-rho comparison that a second council review correctly flagged as statistically invalid.
4. **Reformatted for the actual target journal** (Epidemiology & Infection, Cambridge University Press), per the author-instructions pages fetched and read in full: word count trimmed from ~5,600 to ~3,070 words (target 2000–4000); Summary trimmed to 198 words (target 150–200) plus 5 key-result bullets; short title 5 words (limit 12); references reformatted with full journal names and non-elided page ranges; Cambridge spelling conventions applied; double-spacing, line numbers, 1-inch margins, and left (non-justified) alignment applied to the .docx; competing-interests, financial-support, ethical-standards, and AI-tool-use declarations added per journal policy.
5. **Second full council review** (Scite Skeptic + Spatial & ML Auditor, targeted at the new GWR/spatial-error content specifically) found and the manuscript now corrects: an overstated "GWR failure as diagnostic" framing (softened to an explicitly-labelled numerical artefact); an unsupported direct lambda-vs-rho magnitude comparison (replaced with formal LM specification tests); an unaddressed GWR overfitting risk (addressed with the CV bandwidth cross-check and explicit reporting of negative local R² values as a stated limitation).

## Scientific verdict

Same core finding as the prior councils, now on firmer methodological ground: Ghana's HIV burden shows a genuine, robust south-north spatial gradient (confirmed independently by LISA, Getis-Ord Gi*, spatial lag, spatial error with LM-test justification, and — critically — a district-only GWR model using no DHS regional pass-through variables at all, R²=0.956/0.957 CV-checked). The specific behavioural narrative (VCT uptake and wife-beating acceptance as leading predictors) is correctly and now more precisely characterised as substantially attributable to regional rather than district-level variation, with named regions (Eastern, Greater Accra, Western, Western North) replacing the previous vague "southern belt" language throughout, including in the policy-recommendation section.

## Data-provider requested methods, addressed explicitly

TB co-infection, health-system, health-financing, and STI datasets supplied for this task were checked and found to be **Ghana-national WHO GHO time series with zero within-country subnational variation** — unable to support the requested Bivariate LISA (HIV×TB), GWR-with-TB, or spatial-error-with-TB analyses. This was confirmed with the user directly (2026-07-13) and the TB co-infection expansion was descoped by explicit user decision in favour of strengthening the HIV-only analysis with GWR and a spatial error model, which the data does support. This scoping decision and its rationale are not restated in the manuscript itself (out of scope for the paper) but are documented here for the audit trail.

## Outstanding, disclosed as manuscript limitations (not blocking)

- Cross-sectional design, no causal inference.
- 2014 vintage of the HIV biomarker round.
- No individual-level confounder adjustment (ecological analysis throughout).
- GWR local R² instability in sparse neighbourhoods (explicitly reported, not hidden).
- Figures are RGB PNG at screen resolution; Cambridge's revised-submission figure spec (TIFF/EPS, 1000–1200 dpi line art, CMYK for print) is a production-stage requirement typically finalised after acceptance, not before initial submission, and is noted here rather than actioned given the "S+ for publication" request concerns manuscript and analytical quality, not print pre-press files.

## Verdict

**PASS — S+ / submission-ready for Epidemiology & Infection**, pending the author's own final read-through and any co-author or institutional sign-off. No open scientific, statistical, or data-integrity issues remain unaddressed from either round of council review.
