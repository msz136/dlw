# Independent physical-field perturbations: certification route

2026-10-26. This note addresses the user's selected problem: perturb u and v independently. The structured evaluator in this directory is a separate exploratory construction and **does not solve this problem**. No certified reference error eta is assigned to independently perturbed trajectories.

## 1. Exact decomposition about the actual background v=4

The Gaussian and sinusoidal benchmarks currently in the manuscript have background v=4. In X=x-4t, put

    A=u_y+v-4,  B=v-u_y-4,  u=(1/2) integral_0^z(A-B) dz,
    z=y+2 in [0,4], u(X,0,t)=0.

The full nonlinear equations become exactly

    A_t=-A_XX-(u A)_X,
    B_t= B_XX-(u B)_X.                            (1)

Both constant-background coupling terms disappear. This is useful: the previous mixed-problem constants for the old zero-v-background data should not be reused as if they were current quantitative bounds. The backward-diffusive A branch is nevertheless still present.

For independent perturbations

    u0^eps=u0+eps_u g(z) cos(kX),
    v0^eps=v0+eps_v g(z) cos(kX),
    g(z)=sin^2(pi z/4),

the exact initial transformed changes are

    delta A0 = [eps_u g'(z)+eps_v g(z)] cos(kX),
    delta B0 = [-eps_u g'(z)+eps_v g(z)] cos(kX).    (2)

Setting either eps_u or eps_v to zero gives genuinely independent physical-field perturbations. Since g and g' vanish at both transverse endpoints, these changes preserve the lower prescribed u trace and the initial lower A,B traces. This avoids a new boundary-trace incompatibility, but does not imply interior existence or control of the unresolved x modes.

The current experimental carrier is k=pi/2 (period 4). `independent_constants.py/json` uses that value. An earlier exploratory k=pi/6 calculation has been superseded.

## 2. An improved mixed-time existence theorem

Let x be periodic with length 192 and rho=.1. For trajectories with continuous Fourier coefficients in (z,t), use

    ||f||_rho = sum_n exp(rho |xi_n|) sup_(z,t)|f_n(z,t)|,
    ||(A,B)||_rho = ||A||_rho+||B||_rho.

This norm is a Banach algebra and ||u||_rho <= 2 ||(A,B)||_rho. Write S(t)=exp(t partial_XX). Prescribe the terminal unstable component G=A(T*) and the initial stable component H=B(0). The integral equations are

    A(t)=S(T*-t)G + integral_t^T* S(s-t) partial_X(u A)(s) ds,
    B(t)=S(t)H - integral_0^t S(t-s) partial_X(u B)(s) ds.   (3)

For T*<=.02, each time-integrated differentiated heat operator has norm at most h=sqrt(T*/2)<=.1. The elementary inequality is

    sup_(r>0) (1-exp(-T*r^2))/r <= sqrt(T/2).

The nonlinear part of (3) maps the ball ||(A,B)||<=R into a ball of radius 2hR^2 and has Lipschitz constant at most 4hR. Therefore, for

    ||G||_rho+||H||_rho <= .3,  R=.4,  T*<=.02,

the image norm is at most .3+.2(.4)^2=.332<.4 and the contraction factor is at most .16. There is a unique real mixed-time solution in this ball. In any smaller x-analytic strip, the equations recover the required x,t derivatives; transverse continuity plus the integral relation gives u_y. This is a theorem for the explicitly specified mixed-time problem, not for arbitrary original initial data.

The corresponding constants at T=.01 are image radius .322628 and contraction factor .113138. They are substantially smaller than the old zero-background mixed-time constants. `independent_constants.py` verifies these outward-rounded inequalities and bounds the actual stable initial data in the stated analytic norm.

## 3. The remaining equation is exact initial matching

For fixed H=B0^eps and every allowed terminal G, let (A_G,B_G) be the mixed solution (3), and define

    F_H(G)=A_G(0).

The desired independently perturbed IVP requires solving the full infinite-dimensional equation

    F_H(G)=A0^eps.                                   (4)

Both implications are exact: a solution of (4) supplies a positive-time continuous solution with both prescribed initial fields; an IVP solution in this small ball supplies a terminal G satisfying (4). An arbitrary smooth terminal condition, a small finite-mode matching residual, or agreement after refinement does not establish (4).

At the zero solution the derivative of this matching map is

    D F_0(G)=S(T*)G,

whose nth Fourier multiplier is exp(-T* xi_n^2). Its inverse has multiplier exp(T* xi_n^2), so a bounded inverse in the same analytic Wiener norm does not exist. In particular, the ordinary inverse-function theorem cannot turn the small mixed-time contraction constant into an initial-value existence theorem. At the nonzero benchmark the derivative includes variable-coefficient terms; its exact range and a compatible weighted inverse must be proved rather than replaced by the zero-background formula.

The most focused constructive next step is to validate (4) around a candidate terminal state: solve the retained-mode initial matching equations, bound the inverse of the derivative in a tail-aware space, and enclose the infinite residual and nonlinear remainder in that same space. The range and tail compatibility needed for the unstable component must be shown for the prescribed (2), not assumed from its initial low Fourier support. Nonlinear products generate additional x harmonics.

`NONZERO_MATCHING_DERIVATIVE.md` now gives the exact variable-coefficient linearization, a conditional exponential x-tail smoothing theorem with a norm bound below 1.744115, and the explicit first sideband for the actual Gaussian/sine amplitude family. It also states the infinite-tail Newton conditions that still need verification. This advances the nonzero matching analysis; it does not close the IVP certificate.

## 4. What is and is not excluded

The previously derived full-nonlinear residual counterexample (`../../reference_certificate_20261024/RESIDUAL_NO_GO_CLOSURE.md`) still applies around any sufficiently regular exact solution of the new perturbed data, if such a solution exists. It preserves the complete initial functions and the lower boundary and can keep every finite sample unchanged while producing arbitrarily small ordinary PDE residual and a fixed terminal v discrepancy. Thus ordinary residuals and finite refinement cannot by themselves supply the requested maximum-norm error guarantee.

That result does not prove nonexistence for (2), does not show that a particular numerical candidate has a large actual error, and does not rule out the matching-and-tail route above. The older non-Gevrey-y proof used different physical data and a special highest-harmonic sign structure. It must not be transferred to the present v=4-3u0_y base plus independent sin^2 perturbations without a new proof.

For the A/D solitons, the same forward/backward decomposition is algebraically valid, but the shifted A,B are not small around zero. A mixed-time theorem should instead be centered on the known soliton, retaining its variable-coefficient linear evolution. The above .3/.4 bounds do not cover those solitons. No uniform continuum reference certificate for the four independent perturbation experiments has been obtained in this note.

## 5. Honest certificate status

- Established here: exact current-background decomposition, exact perturbation data, and a small-data mixed-time existence/contraction theorem with useful constants.
- Pending: exact initial matching for the independent perturbations, admissible infinite tails, and a quantitative full-field certificate.
- Reference status for the selected independent perturbations: `certified=false`, `eta_u=null`, `eta_v=null`.

This is a mathematical continuation toward the requested certificate; it must not be reported as completion of that certificate.
