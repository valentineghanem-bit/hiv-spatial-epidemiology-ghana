# Humanised Cambridge Final S+ Verdict
Date: 2026-07-13

## Short Verdict

**Current grade: S+ for submission readiness; A-minus for scientific novelty; A for Cambridge fit after the final 261-district correction.**

This is now a serious submission package. The manuscript, README, dashboard, and poster all lead with the correct frame: **261 census districts**, with one technical geometry caveat where needed. The analysis no longer reads like district-level HIV surveillance that the data cannot support. It reads like a careful ecological spatial epidemiology paper that uses public Ghana DHS/Census data honestly and shows both the signal and the limits.

That honesty is the strength.

## What Is Fixed

- README rebuilt into a numbered 14-section structure and synced with GWR/spatial-error results.
- Dashboard now reports the spatial-error diagnostic and district-only GWR sensitivity result.
- Poster now includes spatial error, GWR, and the 261-district frame.
- Manuscript draft, Cambridge front matter, final DOCX, and Cambridge submission DOCX were corrected away from 260-forward wording.
- Clean Cambridge submission DOCX created: `manuscript/HIV_Spatial_Epidemiology_Ghana_Manuscript_CAMBRIDGE_SUBMISSION.docx`.
- Matching PDF exported from Word: `manuscript/HIV_Spatial_Epidemiology_Ghana_Manuscript_CAMBRIDGE_SUBMISSION.pdf`.
- Cambridge figure exports created as TIFF files in `outputs/figures_cambridge/`.
- Tests pass: `29 passed`.

## Cambridge Guideline Fit

The package now matches the main Cambridge Epidemiology & Infection preparation requirements:

- short informative title;
- 150-200 word continuous Summary;
- Original Paper length inside the preferred 2,000-4,000 word range;
- references below 40;
- double spacing, line numbering, page-number field, and 1-inch margins in the DOCX;
- tables placed at the end of the manuscript;
- figure legends separated from main text;
- TIFF figure files exported for production readiness;
- competing-interest, funding, ethics, data/code availability, and AI-use declarations present.

Official Cambridge anchors:

- Cambridge requires double spacing, 1-inch margins, line numbering, consecutive page numbering, and warns that nonconforming manuscripts may be returned without review.
- Cambridge asks for a 150-200 word continuous Summary and prefers Original Papers at 2,000-4,000 words with fewer than 40 references.
- Cambridge requires tables at the manuscript end and allows PNG/TIF/JPG/GIF/EPS at initial submission, with TIF/EPS expected at revised production stage.
- Cambridge requires transparent AI-use declaration where AI tools were used.

Sources:
- https://www.cambridge.org/core/journals/epidemiology-and-infection/information/author-instructions/preparing-your-materials
- https://www.cambridge.org/core/journals/epidemiology-and-infection/information/author-instructions

## Scientific Soundness

Scientific grade: **A-minus**.

The paper is sound because it no longer overclaims. It says exactly what the data can support:

- regional DHS HIV prevalence is mapped across 261 district records;
- HIV prevalence, VCT uptake, and wife-beating acceptance are regional pass-through variables;
- spatial autocorrelation is real as a mapped regional pattern but anti-conservative if misread as 261 independent HIV outcomes;
- spatial error diagnostics favour residual regional structure;
- GWR fails where regional predictors are locally constant, which is not a failure of the paper but a useful demonstration of the granularity problem;
- district-only GWR retains strong spatial signal, but interpretation remains qualitative and ecological.

The novelty is not "we discovered district HIV determinants." The novelty is cleaner: **a Ghana-focused, reproducible, multi-method spatial epidemiology analysis that shows what public aggregate DHS/Census data can and cannot honestly say at district scale.**

That is publishable.

## Remaining Reviewer Risk

One risk remains and should be owned in the cover letter: the paper does not use cluster-level DHS microdata or small-area estimation. A reviewer may ask why the study maps regional HIV estimates at district scale. The answer is already in the manuscript: transparency, reproducibility, and a direct audit of the limits of public aggregate data.

Do not soften that. It is better to be exact than to sound more impressive and lose trust.

## Re-Ranked Journal Odds

1. **Cambridge Epidemiology & Infection**  
   Current fit: **A**. Estimated odds after these fixes: **55-65%**.  
   Best case if handled as an infectious-disease epidemiology/data-science methods paper with clear regional relevance and no district overclaim.

2. **BMC Public Health**  
   Current fit: **A**. Estimated odds: **55-65%**.  
   Slightly broader and more forgiving on public-health scope, but less targeted to infectious-disease epidemiology methods.

3. **PLOS Global Public Health**  
   Current fit: **A-minus**. Estimated odds: **50-60%**.  
   Strong for transparency and public-health relevance, but may push harder on why no cluster-level/small-area model was used.

## Final Human Verdict

Submit the Cambridge submission DOCX, not the older working manuscript file.

This is now S+ as a submission package. Not because it is flashy. Because it is controlled, honest, reproducible, and editor-readable. The claim is tight. The limitation is not hidden. The methods now defend the limitation rather than pretending it is not there.

That is the version with the best chance.
