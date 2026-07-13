# Epid Council Verdict - Project 2
Date: 2026-07-12

## Council Verdict
Borderline Q1, salvageable with reframing.

## Where the Council Agrees
- The corrected pipeline and open correction note are strengths, not embarrassments, if presented as transparency.
- The paper must not claim independent district-level HIV inference.
- PLOS Global Public Health is the stronger target than Epidemiology & Infection.
- Current submission odds are not high enough for a clean "submit today" recommendation.

## Where the Council Clashes
- The Synthesis Lead sees a credible ecological mapping contribution: Ghana-wide workflow, corrected district-polygon reconciliation, sensitivity analysis, and open artifacts.
- The Skeptic and Spatial Auditor see the regional DHS pass-through as the core threat: Moran's I, LISA, Gi*, spatial lag, LASSO, RF, and SHAP all partly measure regional block structure.
- The Publishing Editor would consider PLOS review after tightening, but expects Cambridge to hesitate unless the infectious-disease surveillance novelty is sharpened.

## Blind Spots Caught
- Dashboard SHAP labels were stale and inconsistent with `shap_summary.csv`; patched.
- Dashboard/poster source labels included unsupported DHIMS2/GHS/WorldPop language; patched.
- The older repo-only QA badge overstated readiness for manuscript submission.
- The "261 districts" framing remains risky even when the caveat appears later.

## Dialectical Synthesis By Claim
### Claim 1: Ghana HIV prevalence is spatially clustered.
Buttressing evidence: Moran's I = 0.920, LISA 59 HH / 51 LL / 4 HL, Gi* 53 hotspots / 53 coldspots.
Counter-argument: HIV prevalence has only 9 unique regional values across 261 districts, so the p-values and cluster counts are anti-conservative at district scale.
Resolution: Keep the claim, but state it as regional clustering mapped to district boundaries.

### Claim 2: VCT uptake and wife-beating acceptance are leading predictors.
Buttressing evidence: SHAP ranks VCT uptake first and wife-beating acceptance second; LASSO also ranks wife-beating acceptance highly.
Counter-argument: both variables are DHS regional pass-throughs; the models cannot distinguish true district effects from regional structure.
Resolution: Present them as regional correlates and hypothesis-generating mechanisms, not district-level determinants or causal drivers.

### Claim 3: Findings can guide HIV program action.
Buttressing evidence: region-level prioritisation for VCT scale-up in southern high-burden regions is plausible and operationally aligned with NACP/GHS regional planning.
Counter-argument: named-district targeting would be unjustified without district-resolved surveillance or small-area estimation.
Resolution: Recommend region-level prioritisation only; explicitly defer district targeting.

## Recommended Manuscript Edits
- Current: "Across 261 districts" as the dominant title/abstract signal.
- Revised: "Regional DHS HIV estimates mapped across Ghana's district boundaries."

- Current: "determinants" and "drive the gradient."
- Revised: "regional correlates" and "are associated with the observed gradient."

- Current: district hotspot wording.
- Revised: "district-boundary visualization of regional hotspot structure."

## One Priority Action
Make the ecological granularity limitation impossible to miss in the title, abstract, dashboard header, poster background box, and cover letter.
