# Plain-description revision (2026-10-26)

Third pass on the same four blocks. The framing is now descriptive rather than evaluative: no
"complementary", "strengths", "trade-offs", "defective", "degrades" or "outperform" anywhere in the
document (checked in `validation.json`).

## What changed

| Block | Change |
|---|---|
| Abstract | new opening sentence (the DLW system as an integrable model, and why preserving the structure matters) and a new closing sentence ("Together, these results show how bilinear lattice symmetry and semi-discrete conservation laws translate directly into improved physical-field accuracy…"); 325 words |
| §1 ¶3–5 | replaced by the three plain paragraphs; ¶1, ¶2 (with `[6–9]`, `[11]`, `[9,12,13]`, `[14]`, `[10]`) and ¶6 (roadmap) kept byte-identical |
| §5.2 last two ¶ | phenomenon-and-mechanism only: Table 2/Table 3 relation, why the `u` ordering persists in Gaussian/sinusoidal and flips in the soliton tests, and why `v` is best for Centered-SD in all four |
| §6 | three paragraphs; the last one steps back ("Viewed in a broader context…") to the general lesson about bilinear structure, cross-component accuracy and conservation-guided mesh adaptation |

## Verification (`validation.json`)

- Changed sections: `abstract`, `section-1`, `section-5.2`, `section-5`, `section-6`; nothing else.
- §1 still has 6 paragraphs; paragraphs 1, 2 and 6 compare equal to the previous file.
- 28 figures, 6 tables. Formula accounting: 948 − 45 + 51 = 954; no `.katex-error`.
- All fifteen references cited.
- §5.2 has 9 paragraphs, the last two being the supplied ones; §6 has 3 paragraphs, 398 words.
- Abstract starts with the new background sentence and ends with the new synthesis sentence.

## Files

- `publish_plain.py`, `verify_plain.py`, `manifest.json`, `validation.json`, `shot_top.png`.
- `before/dlw-paper.html` — previous state, `1d84f50a…e711cb`.

Current manuscript: `8b511834…92ad26`, 2,262,418 bytes.
