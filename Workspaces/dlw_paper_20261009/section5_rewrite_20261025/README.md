# Section 5 rewritten from the supplied narrative

2026-10-25. The user supplied a rewritten narrative for Section 5 (a Gemini draft, `share.gemini.google/2BfuldnrN3lB`)
and asked for it to replace the current narrative.

## What changed

* `section-5` (the introduction) and Sections 5.1–5.4 are replaced by the supplied text.
  Section 5.5, all earlier sections, the appendices and the navigation are byte-identical to
  `before/dlw-paper.html`.
* Tables 1–5 and Figures 1–28 are taken verbatim from the previous manuscript, with their captions and
  PDF links, and placed where the new text marks them. No figure, table or number was regenerated.
* Table 4 now bolds every entry that attains the smallest displayed value, so that a tie (RK4 and
  Crank–Nicolson in three rows) is marked on both cells. This matches the sentence in Section 5.1,
  "bold entries indicate the smallest error among the compared methods for each case and field".

## Checks performed

* Every number quoted in the new text was matched against the recorded runs and the tables:
  factors 72, 2.8, 70, 1.7, 87, 60, 3.2, 3.5 (Table 3); 7.3e-3 and the Euler factors 0.8/21/82/38 %,
  3.8/8.0 %, 8.2/9.0 (Table 4 and the step-halving controls); 11.7/17.4/6.0/5.6 %, the frozen control
  12.8/16.3/5.3/5.8 %, spacing 0.90/1.04 and 0.97/1.02 Δx, displacements 9.5e-4 and 5.2e-4, mass 1e-7,
  the profile drops 6.74→5.95e-4 and 1.40→1.16e-3 (Table 5 and Figures 27–28).
* Cross-references exist: Proposition 3.4, the Gram determinant formulas (6)–(7) in Section 2.1,
  Sections 3.4 and 4.3.
* 774 KaTeX spans, no rendering errors; 28 figures and 5 tables with consecutive captions; no placeholder
  text left in the file.

## Section 5.2 summary expanded (second pass)

The concluding paragraph of 5.2 was replaced by the two paragraphs supplied by the user: the first follows the
Table 2 → Table 3 evolution and explains why Endpoint-SD's initial advantage in `u_t` does not survive the
nonlinear soliton tests, the second summarises the Centered-SD/FD comparison and hands over to Sections 5.3–5.4.
`patch_52_summary.py` performs the replacement and checks that Centered-SD gives the smallest terminal `v` error
in all four tests, that the quoted factors 60–87 (Endpoint) and 1.7–3.5 (FD) bracket the values computed from
Table 3 (60.2–86.6 and 1.68–3.48), and that the figure and table counts are unchanged. The pre-patch manuscript is
kept in `before/summary_expansion/dlw-paper.html`; `manifest_summary_expansion.json` records both hashes. Only
`section-5.2` changed (nine paragraphs now, 16 new formulas).

## Files

| Path | Content |
| --- | --- |
| `publish_section5.py` | bounded replacement of Section 5 and its subsections, with the tie-aware bold pass |
| `before/dlw-paper.html` | the manuscript before this rewrite (hash `7c8537…`) |
| `section-5*.html` | the published section sources |
| `manifest.json` | before/after hashes, replaced sections, kept blocks, formula count |
| `update_guide.py` | appends the rewrite note to the manuscript's editorial guide |
| `render.py`, `shot_*.png` | standalone render pages and screenshots used for the visual check |

`publish_section5.py` refuses to run once the manuscript differs from `before/dlw-paper.html`; the
rewrite is a one-shot publication. The earlier publisher in `../time_samm_20261025/` must not be re-run,
since Section 5 no longer carries its text.
