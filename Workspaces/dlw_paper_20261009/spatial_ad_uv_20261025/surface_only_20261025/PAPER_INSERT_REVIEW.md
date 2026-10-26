# Independent review of the transparent-surface insertion

2026-10-25. Status: **passed**.

Compared the saved main manuscript with `before_paper_insertion/dlw-paper.html`. The raw HTML outside Section 5.2 is byte-for-byte identical. All three tables are unchanged. Within Section 5.2, the fourth introductory paragraph is the only changed body paragraph; its revised final sentence relates planar error locations to surface heights on the componentwise common linear scale. The case analyses and numerical conclusions are unchanged.

All 20 pre-existing figures remain, with image paths, attributes and caption content identical after disregarding the necessary figure-number changes. Four transparent-surface figures were added in the A, D, Gaussian and Sinusoidal order as Figures 12, 16, 20 and 24. Each immediately follows the same case's existing wireframe overlay. Their image sources resolve to the requested `figures/plain_CASE.png` files. The manuscript and English mirror each contain 24 figures; the gallery contains 20. The main manuscript's figure captions run consecutively from 1 to 24.

The new captions identify the T = 0.01 absolute physical-field errors, left/right components, method colors and common coordinates/height scales. Gaussian and sinusoidal captions retain the displayed-window/full-table-region distinction. Section 5.2 contains no candidate, version, preview or figure-selection instructions. No numerical experiment was rerun and no manuscript content was changed during this independent review.

## Check record

```json
{
  "status": "passed",
  "manuscript_sha256": "e301dca88e9af1c5628bbf0bf7380027a37e20db4d6a1ccf5640aad0436d4868",
  "raw_outside_section_5_2_unchanged": true,
  "old_figures_preserved": 20,
  "new_surface_figure_numbers": [
    12,
    16,
    20,
    24
  ],
  "cases": [
    "A",
    "D",
    "Gaussian",
    "Sinusoidal"
  ],
  "new_figures_immediately_follow_existing_overlay": true,
  "table_html_unchanged": true,
  "changed_body_paragraphs": [
    4
  ],
  "figure_counts": {
    "dlw-paper.html": 24,
    "report/dlw_numerical_text_20261025.html": 24,
    "report/dlw_uv_figure_choices_20261025.html": 20
  },
  "figure_numbering": "1-24 consecutive",
  "figure_selection_language_absent": true
}
```
