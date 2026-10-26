# Balanced revision (2026-10-26)

Four blocks replaced with the balanced text: Abstract, §1 Introduction (6 paragraphs), the two
closing paragraphs of §5.2, and §6 Conclusions (4 paragraphs). The framing is now symmetric:
the two lattices are presented as complementary arrangements of one bilinear construction.

## What the new framing says

| | Endpoint-SD | Centered-SD |
|---|---|---|
| Structure | direct two-field system, no auxiliary variable | auxiliary logarithmic difference `ω_k` |
| Consistency | first-order bilinear, second-order in the first equation | second order in both equations |
| Strength | smallest initial `u_t` defect in all four tests; most accurate `u` in the Gaussian and sinusoidal tests | most accurate `v` in all four tests; smaller errors in **both** fields for the soliton tests |
| Extra structure | — | exact semi-discrete conservation law, used for the moving mesh |

Negative framing was removed from the document: `degrades`, `degraded`, `contaminated`,
`defective`, `fragile` no longer appear anywhere, and §5.2's closing paragraph no longer speaks of
"cross-component degradation".

## Citations

- ¶1: `[1–4]` added after "compatible linear Lax problems", so refs 1–4 stay cited.
- Sheng–Yu is `[5]`, not `[1]`.
- The Miwa/Hirota–Miwa sentence now cites `[15]` only. The supplied text had `[2,15]`, but `[2]` is
  Wang–Zhou–Li (a nonlinear-transformation paper), which does not contain the Miwa expansion.
- ¶2 keeps the related-work sentence with `[6–9]`, `[11]`, `[9,12,13]`, `[14]`, `[10]`.

All fifteen references remain cited.

## Conclusions

Four paragraphs: construction summary; the three insights (spatial arrangement — Endpoint-SD
direct/compact and best in `u` for smooth data, Centered-SD best in `v` everywhere and better in `u`
for solitons); time integrators (steady spatial rate, CN ≈ RK4, Euler's opposite-sign cancellation);
adaptive mesh (conservation density guides the nodes, static gain dominates over the short horizon).
No mention of 4.4, 5.5, linearized stability or perturbed data.

## Verification (`validation.json`)

- Changed sections: `abstract`, `section-1`, `section-5.2`, `section-5`, `section-6`; all others
  byte-identical.
- 28 figures, 6 tables.
- Formula accounting: 974 total before − 75 replaced + 49 new = 948; no `.katex-error`.
- §5.2 has 9 paragraphs; the last two are the supplied ones.
- §6 has 4 paragraphs, 458 words.
- Five literal phrases asserted present; no negative-framing words anywhere.

## Files

- `publish_balance.py`, `verify_balance.py`, `manifest.json`, `validation.json`, `shot_top.png`.
- `before/dlw-paper.html` — previous state, `f780b12a…9bf5d0c7`.

Current manuscript: `1d84f50a…e711cb`, 2,258,324 bytes.

## Still open

The headings `4.4` and `5.5` (and the phrase "and linear stability" in the §4 title) are the last
traces of the stability material. The conclusions no longer mention it; deleting the two headings and
the phrase would make the document internally consistent in one step.
