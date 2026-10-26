# Appendices A–D and removal of the editorial guide (2026-10-26)

The four appendix placeholders are now written, and the in-manuscript editorial guide
(formerly Appendix G) is removed. Sections 1–6 and the front matter are untouched except
for four forward references.

## What each appendix does

| Appendix | Content | Equations |
|---|---|---|
| A. Determinant identities and alternative solution representations | rank-one determinant identity; **shift identity** `τ^C_n(k;h) = τ^E_n(k;h)|_{a→a+h/2}`; logarithmic fields as ratios of neighbouring determinants; positivity of first minors; N = 1 member | (A1)–(A3) |
| B. Field transformations and reconstruction conditions | field relation `v_k − Δ_h u_k = (2/h)(ω_k+ω_{k−1})`; closed-form recurrence and its affine solution; conditions on the lower trace; consistency of initial data | (B1)–(B3) |
| C. Operator compatibility and continuum expansions | coefficient form of (42); midpoint expansions; flux expansion giving the O(h) coefficient of (51); Centered reconstruction (53) and residual (52) | (C1)–(C3) |
| D. Numerical implementation and supplementary experiments | Fourier multipliers and Nyquist convention; closures; Crank–Nicolson iteration and stopping rule; mapped centred differences; Table 6 of control runs | Table 6 |

Forward references were added at four points so the appendices are not orphaned:
§2.4 → A, §3.2 → B, §3.4 (end) → C, §4.2 → D.

## Verification

The shift identity (A2) was checked numerically before publication: with random complex
parameters, `det τ^C(a)` and `det τ^E(a+h/2)` agree to 9.0e−15 for N = 1…4 and several
(n, k). `validation.json` records:

- 26 sections; `appendix-G` gone; changed = A–D, the four anchor sections and their parents.
- 28 figures, 6 tables with captions 1–6 in order.
- 947 KaTeX spans (+125), zero `.katex-error`; no leftover tokens.
- Word counts: A 1019, B 761, C 840, D 1047.
- No "Editorial guide" text remains in the document.

Appendix D carries `class="numerical-section"` so that Table 6 receives the three-line
table style used by Tables 1–5.

## Files

- `publish_appendices.py` — publisher (replays from `before/dlw-paper.html`).
- `verify_appendices.py` — independent check.
- `manifest.json`, `validation.json`, `appendix_G_archive.txt` (text of the removed guide).
- `before/dlw-paper.html` — pre-edit manuscript, `65cf4aa7…b43af`.
- `_preview2.html`, `shot_appendix_CD.png`, `shot_table6_crop.png` — render checks.
- `fix_escapes.py`, `fix_raw.py` — one-off repair scripts used while building the publisher.

Current manuscript: `a8f88298…c22421f`, 2,261,236 bytes.

## Notes for the polish pass

- Appendix A's last sentence attributes the Casoratian reduction to [15] without proof;
  the equivalence is stated, not derived.
- Appendix C keeps the main text's wording that the coefficients of `DY`, `Y`, `D^0`
  vanish by (47)–(49); the full operator expansion is not printed.
- Appendix D's Table 6 summarises numbers already quoted in §§5.3–5.4; no new runs.
