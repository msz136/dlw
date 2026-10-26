# Minimal natural-form synchronization of Sections 3.3 and 3.4

2026-10-25. These replacement sections preserve (40)–(53) and the common
Darboux–Lax proof. They change only consequences of the already adopted
Section 3.2 field definition. `prepare.py` writes extracted replacement HTML;
it does not write the manuscript.

## Section 3.3

The adopted logarithmic definitions give `r_x=(u-omega)/2` and
`R_x=(u+omega)/2`. Substitution into the unchanged coefficient definition
(46) gives `A=(u_previous-omega_previous)/2` and
`C=(u+omega)/2-h`, with `b=a+h/2`.

The identities used in the recovery paragraph are:

- `C-A_next=omega-h`; (49) minus shifted (48) is exactly (37).
- (47) gives `Delta S = dx[Delta u+(omega+omega_previous)/h]`, which,
  by (39), is `dx(v+Delta u)/2`.
- Twice shifted (48) plus the omega equation gives
  `u_t=u_xx-dx[H(u)+omega^2/2-h*omega]-2*S_x`.
- Its lattice difference gives the first equation (35). The derivative of
  (39) then gives the second equation.

The third identity was independently simplified with SymPy to an exactly zero
residual, using `A=(u-omega)/2` and `b=a+h/2`.

## Section 3.4

Introduce the normalized auxiliary `W=4*omega/h` locally for Taylor expansion.
The physical reconstruction is exactly `v=Delta u+M_-W`. Its midpoint
expansion is (53), with no inverse derivative or primitive term. The smooth
family assumption requires `W=v-u_y+O(h^2)` including the derivatives in
the equations; its lower trace is part of that assumption. The proposition
does not infer smoothness from the recurrence for arbitrary data.

The extra first-equation flux equals `h^2*(W^2/32-W/4)`. Its spatial
derivatives stay O(h^2) under the stated smooth-family assumptions. The
unchanged scaled auxiliary evolution then proves second-order consistency
for v as well.

The matched-Gram phase/amplitude argument is retained. Natural fields are
the symmetric logarithmic derivative u and `v=Delta Z`; positivity and the
required derivative bounds give both fields O(h^2) approximation. The old
primitive correction is removed. The original shared initial-u coefficient
claim is replaced by the exact flux difference verified independently in
`../../report_refresh_20261024/natural_selection_20261025/SCIENTIFIC_REVIEW.md`.

## Validation

`validation.json`: 95 successfully rendered KaTeX expressions, unique tags
(40)–(53), and no obsolete full-potential terminology. The existing
Endpoint-SD operator proof is unchanged. These are local mathematical
substitutions and a consistency proof under the stated assumptions; they do
not introduce a convergence theorem for the fully discrete numerical method.
