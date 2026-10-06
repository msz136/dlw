# Independent mathematical review of report.src.html

Reviewed 2026-10-04 against the current nonlinear closure, exact physical
conversion, and the independent periodic mean-mode notes. No change to the
report source was made by this reviewer.

## Finding requiring a small correction

Section 6 calls B(zeta) the coefficient of D^2, but equation (16) sets
B=+R. In the first U component for a w/v-direction perturbation that
coefficient is -R. Change the phrase to “the coefficient of -D^2”, or
explicitly define B as the negative of the D^2 coefficient. The
root-count obstruction and its N threshold are unchanged.

## Formulas and scopes checked

- Equations (1) and the shift U=u+2a, w=v-C0u-4 correctly follow from the
  existing SD equations. The physical second equation minus M* times the
  first recovers the full w equation without inverting M, hence retains
  the even-N alternating mode.
- The periodic compatibility argument correctly gives constant c and
  spatially constant gamma(t). Fixing gamma in time is identified as the
  selected autonomous mean closure. The time-dependent Galilean change
  U'(x,t)=U(x-A,t)+A' and gamma'=gamma+cA' is exact.
- The R kernel, Fourier sign, skew-adjointness, and even-N Nyquist zero
  are correct. RD is selfadjoint.
- The signs of H0, J0 and both variational derivatives in (6)-(7) match
  the vector field. The unrestricted closure is appropriately distinguished
  from the invariant constrained system.
- The subtraction of gamma times the mean U functional cancels the
  delta B variation; both directions of equivalence in (8)-(9) hold.
  The explicit reduced functional (10) is correct, including its global
  quartic term and derivative term Pi(sDp).
- The physical graph, constraints (12), A and A* in (13), and lifted
  Poisson operator (14) are correct. The smooth coordinate pushforward
  supplies Jacobi for general N; the Casimir-coordinate ambient extension
  is legitimate with fixed rho. Natural sector (15) is correct.
- Section 6's constant first-order candidate J=-BD has the correct sign:
  its inferred linear gradient is D B^-1 [[1,R],[0,-1]]. With
  B^-1=[[p,q],[q,r]], diagonal Helmholtz conditions force p=r=0.
  The zero-order symplectic Helmholtz test D M_w vs -M_w D is correct;
  it already fails at a constant nonzero c background. These statements
  apply to the explicitly stated narrow classes and do not classify every
  Poisson operator.
- The density-support example is correct: relative support [-1,1] gives
  variational-gradient radius at most 2, radius-1 J gives composite radius
  3, and exclusion begins at N>=9. A separate bond density supported at
  {0,1} gives gradient radius 1, composite radius 2, and exclusion at
  N>=7; adding this optional distinction would help readers avoid a
  support-convention misunderstanding.
- The Laurent root-count proof is correct after the sign wording fix.
  Every nonzero lattice Fourier tangent is available at the compatible
  constant background, so the proof applies to this actual constrained
  phase space. The stated small-N, nonlocal, singular, and special-reduction
  exceptions are necessary and correctly retained.
- The two-node open-chain counterexample is dimensionally and algebraically
  correct. Schwartz x perturbations require background subtraction, as
  stated. Infinite-lattice cotangent multiplier unboundedness and the
  absence of a well-posedness claim are correctly distinguished.
- Hamiltonian conservation, translation momentum, reduced x-mean Casimirs,
  and the remaining Liouville requirements are correctly stated. No Lax
  result is substituted for Poisson or Jacobi verification.

Overall: mathematically sound within the advertised formal functional
setting, fixed periodic N,h, and c!=0 constant-gamma mean closure. No
substantive correction beyond the Section 6 coefficient-sign wording
was identified.
