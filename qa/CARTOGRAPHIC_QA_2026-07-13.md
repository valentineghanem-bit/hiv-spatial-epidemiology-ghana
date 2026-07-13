# Cartographic QA - Ghana Manuscript Maps
Date: 2026-07-13

## Scope
Figures 1-4 were regenerated for the BMC Public Health manuscript map set:

- `outputs/figures/fig1_study_area_map.png`
- `outputs/figures/fig2_hiv_poverty_choropleth.png`
- `outputs/figures/fig3_determinants_choropleth.png`
- `outputs/figures/fig4_lisa_cluster_map.png`
- matching 300 dpi TIFF exports in `outputs/figures_cambridge/`

## Cartographic Fixes Applied
- Added north arrow and true-north bearing label to each manuscript map.
- Added 0-100-200 km scale bars.
- Added projection/CRS note: WGS 84 / UTM zone 30N (EPSG:32630).
- Added source and boundary caveat text.
- Preserved the 261-district analytic frame while explicitly labelling the mapped display geometry as 260 unique polygons because Guan shares the Krachi East Municipal boundary.
- Updated active BMC manuscript DOCX captions for Figures 1-4 to state the cartographic elements and boundary caveat.
- Copied corrected figure PNG/TIFF files into `submission_package/BMC_PUBLIC_HEALTH_SUBMISSION_2026-07-13/figures/`.

## Export QA
All corrected PNG files are 300 dpi. All corrected TIFF files are RGB, 300 dpi, and LZW-compressed.

## Editorial Verdict
The Ghana map figures are now cartographically self-contained for journal review: orientation, bearing, scale, projection, source, and boundary limitations are visible either on the figure or in its caption.
