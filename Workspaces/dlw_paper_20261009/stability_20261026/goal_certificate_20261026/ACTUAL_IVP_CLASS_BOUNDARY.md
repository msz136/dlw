# Actual sine IVP: quantitative regularity obstruction and the remaining class

2026-10-26. Independent reasoning from the exact boundary-jet recurrence in
`../certificate_continuation/audit_sine_jet_obstruction.md`. This note sharpens
the necessary regularity bound and identifies why it does not prove general
nonexistence. It supplies no certified continuous reference.

## 1. Actual data and hypotheses

Use `X=x-4t`, `z=y+2 in [0,4]`, period 192 in X,

    alpha=pi/4, q=pi/12, kappa=pi/2=6q,
    u0=.03 sin(alpha z) cos(qX), v0=4-3u0_z.

Independently add `epsilon sin²(alpha z) cos(kappa X)` to exactly one physical
field, with the other unchanged; epsilon is any fixed nonzero real number,
including the current 1e-6. Retain the lower trace u(X,0,t)=0.

Put A=u_z+v-4, B=v-u_z-4, u=(1/2) integral_0^z(A-B). The PDE is

    A_t=-A_XX-(uA)_X, B_t=B_XX-(uB)_X.

Assume the boundary jets exist to every transverse order, are C1 in time and
C2 in periodic X, and commute with the PDE differentiations. These are the
same explicit hypotheses as the existing actual-sine theorem. No analytic
dependence on epsilon or z is assumed.

The independently audited weight/frequency isolation gives actual Fourier
coefficients of a_j=partial_z^j A(X,0,t)/j!:

    [a_(rn-1)]_(n kappa) = (-i kappa)^(n-1) epsilon^n C_n(t),

where r=2 for u input and r=3 for v input. The nonzero .03 background cannot
contribute to these selected coefficients. The positive recurrences imply,
for every 0<s<=t,

    C_n(t) >= alpha² n (alpha² s/2)^(n-1)
                    exp(n² kappa² (t-s))                    (u input),

    C_n(t) >= (alpha²/2) n (alpha² kappa² s²/12)^(n-1)
                    exp(n² kappa² (t-s))                    (v input).

## 2. Sharpened necessary quadratic growth rate

Choose s_n=(n-1)/(n² kappa²) for u input and
s_n=2(n-1)/(n² kappa²) for v input. For every fixed t>0 these satisfy
s_n<=t for all sufficiently large n. Taking logarithms gives

    log |[a_(rn-1)]_(n kappa)|
        >= n² kappa² t - O(n log n).

The constants in O(n log n) can depend on fixed t, epsilon, alpha and kappa.
They do not change the quadratic coefficient. Multiplying by (rn-1)! to
recover the derivative changes the logarithm by O(n log n) only. A Fourier
coefficient is bounded by the supremum norm. Consequently

    limsup_(j->infinity) j^(-2)
      log(1+||partial_z^j A(.,0,t)||_infinity)
       >= kappa² t/r².                                    (Q1)

The same necessary lower limit holds for

    M_j(t)=max(||partial_z^j u(.,0,t)||_infinity,
               ||partial_z^j v(.,0,t)||_infinity).

Indeed, if limsup j^-2 log(1+M_j) were less than the right hand side,
A=u_z+v-4 would satisfy the same smaller quadratic rate, because shifting
j to j+1 adds only O(j) to a quadratic exponent. This contradicts (Q1).

At T=.01 and kappa=pi/2, the necessary coefficients are approximately

    u-only input: pi²/1600 = .006168502750680849,
    v-only input: pi²/3600 = .002741556778080377.

Thus every weight with log M_j=o(j²), including all finite-order Gevrey
weights C R^j (j!)^s, is excluded. A quadratic derivative-weight certificate
must at least permit the corresponding coefficient in (Q1). This is a
necessary condition, not an existence or sufficiency statement.

## 3. Why uniform x analyticity does not remove the gap

Fix any finite x-strip weight rho and let X_rho be the periodic Wiener
space with norm sum_n exp(rho |xi_n|)|f_n|. Each prescribed boundary jet
a_j(X,t), b_j(X,t) is a finite Fourier polynomial with smooth time
coefficients. It therefore belongs to X_rho at every j, even though its
norm grows arbitrarily fast with j.

A Banach-valued Borel construction shows that arbitrary such jets can be
realized by functions smooth in z and t with values in X_rho. This directly
demonstrates that the boundary-jet lower bounds are compatible with a
uniform x-analytic norm and unrestricted smooth transverse behavior.

For completeness, choose a smooth cutoff chi equal to 1 near 0 and compactly
supported. Write c_j(t)=a_j(t)-a_j(0), so c_j(0)=0, and set

    F(X,z,t)=A0(X,z)+sum_(j>=0) z^j chi(lambda_j z)c_j(X,t).

Treat finitely many initial j separately. For the remaining j, choose
lambda_j so large that the j-th summand and all its z/time derivatives of
combined order <=j/2 have X_rho norm at most 2^-j. This is possible because,
for z derivative order m<j, its norm scales as lambda_j^(m-j) times a finite
constant involving chi and finitely many time derivatives of c_j. The sum
then converges in every finite C^m_z,t(X_rho) topology. At z=0, its normalized
jets are exactly a_j(t); at t=0, it equals the complete prescribed A0(X,z).
Repeat for B.

Reconstructing u=(1/2) integral(A-B), v=4+(A+B)/2 gives smooth physical
fields with the exact initial functions, lower u trace, and all the forced
boundary jets. The PDE residual is flat to every z order at the boundary.
There is no assertion that this extension solves the PDE in the interior.

This construction is a logical countercheck: neither the existence of all
jets nor a uniform analytic-x norm yields a transverse Gevrey bound. Hence
the actual-sine jet theorem alone cannot rule out C-infinity-z solutions,
continuous-z mixed solutions, or every possible initial-matching solution.

## 4. Consequences for the renewed goal

- A reference proof relying on finite-order analytic/Gevrey transverse tails
  is impossible for the actual perturbed sine datum under the stated PDE
  regularity assumptions, at every positive time.
- Increasing the polynomial order or arithmetic precision cannot repair that
  particular class assumption: the target itself would leave the class.
- No nonexistence theorem in the unrestricted smooth transverse class follows
  from this argument. No complete actual-data matching or finite full-field
  eta was obtained in this independent audit.
- Constant-background amplitude-series divergence remains a separate result.
  It is not a substitute for the fixed-epsilon actual-data jet argument.
- Gaussian and soliton actual-data nonexistence cannot be inferred from this
  sine frequency-isolation proof. Their initial frequency structures differ.

For the goal's impossibility branch, the full-nonlinear residual obstruction
audited separately is the most direct general statement about what ordinary
residuals, exact initial/boundary data and finite observations cannot certify.
That theorem should state its information assumptions explicitly. It does
not rule out integrable exact formulas or a future certificate using additional
quantitative infinite-tail restrictions.
