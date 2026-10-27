# Independent audit of the A/D finite-Laplace-chain extension

2026-10-26. Reviewed Section 4 of `constructive_laplace_chain.md`. The extension is correct for the specific finite chain stated there. This note does not certify a perturbed trajectory or rule out general dressing constructions.

## Actual initial data

The production `time_samm_20261025/time/run_time.py:setup` samples continuous exact u and v separately at their native sites, then recovers w through the current Centered-SD recurrence. The `Exact` evaluator imported from `paper_comparison_20261022/solver_snapshot.py` uses continuous phases with transverse rates `1/(p-2)+1/(q+2)`; the apparent lattice index in its interface merely converts to physical y. No discrete exponential dispersion is substituted into these initial profiles.

Independent extraction of the actual parameters gives:

| Case | p | q | Continuous y exponents | g coefficients | f coefficients |
|---|---|---|---|---|---|
| A | 1 | 2 | -3/4 | 1, 1/3 | 1, 1/12 |
| D | 1, 4 | 2, -3 | -3/4, -1/2 | 1, 1/3, 1, 5/12 | 1, 1/12, 2, 5/24 |

All tau coefficients are positive. Thus both tau functions are strictly positive at real x,y and their reconstructed physical fields are regular there. Each exponent is an integer multiple of 1/4, and `exp(8 pi i gamma)=1` for each elementary exponent. Both tau functions, the physical fields, and all their derivatives consequently have the common imaginary y period `8 pi i`.

The saved experiment uses A's transverse interval `[-9.95,9.95]`, length19.9, and D's interval `[-39.95,39.95]`, length79.9. Its perturbation envelope is `sin^2(b(y-yL))` with `b=pi/L` in each case. This b is distinct from the common x-carrier frequency `pi/2`.

`audit_soliton_laplace_checks.py` independently reconstructs the continuous Gram profiles and compares them to the baseline initial u and reconstructed v in the stored perturbation NPZ files. The largest difference is `7.11e-14`, consistent with the ordinary floating-point evaluation order. These numerical comparisons supplement the exact source/parameter check; they are not interval enclosures.

## Uniform complex-neighborhood argument

Choose any real regular point `(X0,y0)` with `C(X0)=cos(pi X0/2)` nonzero. On a sufficiently small complex neighborhood, both tau denominators remain bounded away from zero. Translate this neighborhood by `y -> y+8 pi i n`. The unperturbed analytic germs and every fixed-order derivative are identical on every translate.

Let `R_n=8 pi n`, `E_n=exp(2bR_n)`, and write points in the translated neighborhood as `y=y0+iR_n+zeta`. The perturbation has

\[
 \phi(y)=-\tfrac14 E_n e^{-2ib(y_0+\zeta-y_L)}+O(1),
\quad
 \phi_y(y)=\tfrac{ib}{2}E_n e^{-2ib(y_0+\zeta-y_L)}+O(E_n^{-1}).
\]

The bounds hold uniformly with all finitely many derivatives needed for any fixed chain index. The initial invariants therefore have the leading coefficients in the certificate note. Suppose at a finite integer index

\[
 P_j=E_n c_j(X)e^{-2ib(y_0+\zeta-y_L)}+O(1),
\quad
 c_j=C(X)\left[-\frac{\epsilon_v}{16}
                +\frac{(2j-1)ib\epsilon_u}{8}\right].
\]

The leading factor separates into an X function and a y exponential. Its mixed logarithmic derivative vanishes exactly. The uniformly differentiable relative remainder is `O(E_n^{-1})`, so

\[
 (\log P_j)_{Xy}=O(E_n^{-1}).
\]

Consequently the recurrence `P_(j+1)=2P_j-P_(j-1)+(log P_j)_Xy` preserves the leading coefficient recurrence and the `O(1)` remainder. It works in both integer directions. For real perturbation amplitudes not both zero and integer j, `c_j` never vanishes on this X neighborhood. Every finite invariant is thus nonzero as a meromorphic function. No assumption about a future solution at complex y enters this initial-data argument.

The uniform translated germs are essential: a bound only on isolated points would not justify differentiating the asymptotic expression. Section 4 correctly supplies those neighborhoods.

## Scope

The result excludes finite termination of the stated Laplace chain on the current perturbed A/D initial data, complementing the separate Gaussian/sine proof. It does not exclude arbitrary transformations called Darboux, an infinite chain, a general inverse-scattering representation, or a weaker-regularity PDE solution. The numerical Fourier treatment of the finite x interval is not used in this local initial-data theorem.

Evidence: `audit_soliton_laplace_checks.py` and `audit_soliton_laplace_checks.json`.
