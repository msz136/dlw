# The actual Gaussian benchmark has no physical maximum-norm Lipschitz response

2026-10-26. Analytic proof with independent audit and exact symbolic
checks. This strengthens the finite-classical-norm result: the response
norm below contains no spatial derivatives. A further conclusion
excludes a response family with any Holder exponent greater than one
half. It does not prove nonexistence at one isolated nonzero amplitude,
and does not provide a perturbed reference or reference error eta.

## 1. Problem, exact directions, and theorem

Use X=x-4t, z=y+2 in [0,4], period L=192, and any common positive
interval [0,T] with T<=.01. The moving-frame equations are

    u_zt=-v_XX-(u²/2)_Xz,
    v_t=-u_XXz-(uv-4u)_X.                              (H1)

The lower trace is u(X,0,t)=0. The exact unperturbed solution (u^b,v^b)
is the certified continuous construction in
`../../../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md`,
with initial fields

    u0^b=.05 sin(pi z/4) F0(X), v0^b=4-3u0,z^b,
    F0(X)=sum_j exp(-(X+192j)²/36).

Consider either one of the two exact independent perturbation directions

    (delta u0,delta v0)=(epsilon phi(z)K(X),0),
    (delta u0,delta v0)=(0,epsilon phi(z)K(X)),
    phi(z)=sin²(pi z/4), K(X)=cos(pi X/2).              (H2)

All solutions below are classical exact physical solutions, periodic in
X, with this initial condition and the same lower trace. Their physical
response norm is

    M(epsilon)=sup_(X,z,t) (|u^epsilon-u^b|+|v^epsilon-v^b|).

**Theorem.** For either direction in (H2):

1. There is no sequence of nonzero epsilon_j ->0 for which such
   solutions exist on one common positive interval and
   M(epsilon_j)<=C|epsilon_j| with one finite constant C.
2. There is no family defined for every sufficiently small positive
   epsilon on one common positive interval satisfying
   M(epsilon)<=C epsilon^alpha for any alpha>1/2.

The first statement concerns an arbitrary amplitude sequence. The second
uses existence and the bound at every sufficiently small amplitude.
It does not assert the same Holder conclusion for an arbitrary sparse
amplitude sequence. Neither statement excludes a single solution at
epsilon=1e-6 or assigns its distance from the base solution.

The theorem is an analytic result conditional on the specified certified
base construction. It is not a formal proof-assistant theorem.

## 2. Fixed base transform and an exact residual identity

Let s(z)=.05 sin(pi z/4)/2, C=sqrt(pi)/32, d=pi/96. The base construction
provides

    F_t=-F_XX, F(X,0)=F0(X),
    Phi=psi/F, Phi_t=Phi_XX+2W_X Phi, W=F_X/F,
    Phi(X+L,z,t)=exp(-s(z)CL)Phi(X,z,t).

The positivity identity

    F(X,t)=3/sqrt(9-t) sum_j exp(-(X+192j)²/[4(9-t)])

shows F>0 for real X and 0<=t<=.01. Fix a compact transverse interval
I around z=1 inside (0,2). The base construction and its nonzero
psi,D bounds give

    P1^b=(v^b-4+u_z^b)/4=s_z F D/psi² !=0,
    Q1^b=-u^b/2-(log|P1^b|)_X=Phi_X/Phi,
    R^b=P1^b-Q1,z^b=0.

These are smooth coefficients on the compact real cylinder. No inverse
transformation of any perturbed solution will be used.

For arbitrary smooth u,v define

    E_u=u_zt+v_XX+(u²/2)_Xz,
    E_v=v_t+u_XXz+(uv-4u)_X,
    P1=(v-4+u_z)/4, Q1=-u/2-(log|P1|)_X,
    R=(v-4+3u_z)/4+(log|P1|)_Xz.

Where P1 is nonzero, exact algebra gives

    R_t+R_XX-2(Q1 R)_X
      =(E_v+3E_u)/4+partial_Xz[(E_v+E_u)/(4P1)].       (H3)

Its linearization at the base is an identity of linear differential
operators with smooth coefficients. It therefore holds for arbitrary
distributions w,q, with

    rho=(q+3w_z)/4+partial_Xz[(q+w_z)/(4P1^b)]         (H4)

on the left, and the linearized E_u,E_v on the right. This is legitimate
even if the actual perturbed invariant P1 has zeros.

## 3. A fixed forced backward-heat lift

For one exact solution set

    w_epsilon=(u^epsilon-u^b)/epsilon,
    q_epsilon=(v^epsilon-v^b)/epsilon.

The exact physical equations imply that its linearized residuals are

    E_u^lin=-epsilon partial_Xz(w_epsilon²/2),
    E_v^lin=-epsilon partial_X(w_epsilon q_epsilon).   (H5)

If M(epsilon)<=C|epsilon|^alpha, these residuals have size
O(|epsilon|^(2alpha-1)) in one fixed spatial-distribution norm, uniformly
in time. The normalized fields have size O(|epsilon|^(alpha-1)).
The derivatives in (H3)-(H5) increase the distribution order by only a
fixed finite amount, independently of epsilon.

Form rho_epsilon by (H4) and put r_epsilon=rho_epsilon/Phi. With
T=partial_X-W and mu(z)=s(z)C>0 on I, the gauge and Darboux identities are

    r_t+r_XX+2W_X r=(right side of linearized H3)/Phi,
    (partial_t+partial_XX+2W_X)T=T(partial_t+partial_XX).

There is a unique Bloch lift T h_epsilon=r_epsilon with multiplier
exp(mu(z)L). To see continuity on distributions, write h=exp(mu X)p
and r=exp(mu X)a, with p,a periodic. Then

    p=F (partial_X+mu)^(-1)(a/F).

The inverse has Fourier multiplier 1/(ind+mu), smooth in z and uniformly
defined since mu is bounded away from zero. It is a continuous operator
on distributions, with smooth time and z dependence. The homogeneous
kernel cF is periodic and cannot belong to the nontrivial Bloch sector.

Consequently

    h_epsilon,t+h_epsilon,XX=S_epsilon,               (H6)

where h_epsilon has size O(|epsilon|^(alpha-1)) and S_epsilon has size
O(|epsilon|^(2alpha-1)) in fixed spatial-distribution norms, uniformly
in time. All source operations are spatial; no time derivatives of the
bounded physical perturbations occur in these estimates. The initial
h_epsilon equals one fixed h0 for every epsilon because (H4) and the
lift are linear and (H2) is exactly linear in epsilon.

## 4. Fourier estimates and the amplitude quantifiers

Write h_epsilon=exp(mu(z)X)p_epsilon and let p_epsilon,n denote its
periodic Fourier coefficients. They satisfy

    partial_t p_epsilon,n=lambda_n(z)p_epsilon,n+g_epsilon,n,
    lambda_n(z)=(nd)²-2i mu(z)nd-mu(z)².

Every fixed-order spatial-distribution bound yields polynomial Fourier
growth in n in one fixed transverse distribution norm. Thus h and S
have the corresponding bounds with factors (1+|n|)^N, uniformly in
epsilon and time. Pairing the backward Duhamel formula at a fixed
0<tau<=T with a z test function gives, after increasing fixed N,m,

    |<p_n(0),g>| <= C(1+|n|)^N ||g||_(C^m)
      [|epsilon|^(alpha-1) exp(-tau(nd)²)
        +|epsilon|^(2alpha-1)].                       (H7)

Indeed, multiplication of the test function by exp(-lambda_n(z)t)
costs only polynomial powers of n in its z derivatives. Its modulus is
at most a fixed constant times exp(-t(nd)²); the time integral of the
forcing can be bounded by the latter's stated size times a polynomial.
The exact classical solution supplies all time slices here; their
distribution bounds use only its physical maximum norm.

For a Lipschitz bound alpha=1 along any sequence epsilon_j ->0, take the
limit in (H7) for each fixed n. This proves

    |<p_n(0),g>| <= C(1+|n|)^N exp(-tau(nd)²)||g||_(C^m). (H8)

For 1/2<alpha<1, use the assumed all-small-amplitude family to choose

    epsilon_n=exp(-(tau/alpha)(nd)²).

Both exponents on the right of (H7) then equal
tau(2alpha-1)(nd)²/alpha. Thus (H8) again holds with a possibly smaller
positive Gaussian exponent. For alpha>=1 the bound implies a Lipschitz
bound at small epsilon, already excluded by the first argument.

Gaussian Fourier decay in one fixed transverse distribution norm makes
h0 entire in complex X with values in distributions in z. Completing
the square in its Fourier series gives constants m,N,C_1,C_2 such that

    |<F0 h0'-F0' h0,g>|
       <=C_1(1+|X|)^N exp(C_2|X|²)||g||_(C^m).        (H9)

The smooth Bloch factor and its z derivatives cost only exponential
growth in |Re X| and polynomial factors in |X|. The entire F0,F0'
also have order at most two, so they preserve this bound.

## 5. The exact initial data violate the forced entire bound

At t=0 the defect in (H4) is

    rho0=a(z)K(X)-b(z)(K/F0)_X,

where, writing f=sin(pi z/4),

    u-only: a=3ff'/2, b=f'/.05,
    v-only: a=f²/4, b=(f²/f')'/(2*.05).

The gauge Phi0=exp(-sJ0)/F0 and the initial lift give

    F0 h0'-F0' h0
      =exp(s(z)J0(X))[a(z)F0²K-b(z)(F0K'-F0'K)].      (H10)

Both sides extend as entire distribution-valued functions if (H9)
holds; equality on real X therefore gives equality at complex X.
The companion `GAUSSIAN_COMPLEX_GROWTH_LEMMA.md` proves that the right
side of (H10) cannot satisfy (H9). Its decisive estimates, for
X_Y=9pi/Y+iY, are

    Re J0(X_Y)>=c exp(Y²/36)/Y,
    |J0(X_Y)|<=C exp(Y²/36)/Y,
    |F0(X_Y)|>=c exp(Y²/36), F0'/F0=O(Y),
    (F0K'-F0'K)/(F0²K)=O(Y exp(-Y²/36)).

Since s and a are strictly positive on a small I, test (H10) against
g_Y(z)=g(z)exp(-i s(z)Im J0(X_Y)), where g is a fixed nonnegative cutoff
of integral one in I. The resulting magnitude is at least

    c |F0(X_Y)²K(X_Y)| exp(s_* Re J0(X_Y)).

Its logarithm grows at least as c exp(Y²/36)/Y+O(Y²), whereas the
logarithm permitted by (H9), including the cost
||g_Y||_(C^m)<=C(1+|J0(X_Y)|)^m, is O(Y²). This contradiction proves
both theorem statements.

## 6. Weak-limit interpretation of the Lipschitz case

There is an independent route for the first statement. A hypothetical
uniform physical Lipschitz sequence has bounded normalized w_j,q_j.
Weak-star compactness, the conservative form of (H1), and (H5) give a
distributional physical first variation with the exact initial traces.
The fixed linear transform then gives free backward heat. Applying its
Fourier ODE with a compactly supported positive-time test proves (H8)
without requiring pointwise z traces or a positive-time slice theorem.
The same complex contradiction applies.

The residual/Duhamel proof above has the advantage that it works
directly on each actual exact solution and also yields the Holder
statement. Neither argument needs any uniform physical derivative bound.

More generally, a spacetime-distribution solution of the linearized
physical PDE with these exact initial traces would be impossible. Its
fixed transform gives a free backward-heat distribution. For its
n-th periodic Fourier coefficient p_n, the identity
exp(-lambda_n t)p_n=p_n(0), tested against a smooth time cutoff supported
inside a positive interval, gives Gaussian decay in n with one finite
transverse distribution order. Time derivatives of the cutoff times
exp(-lambda_n t) cost only polynomial n factors. This proves (H8) and
the same contradiction without assuming bounded physical variations.

## 7. Verification and limits

The original gauge and initial-coefficient identities pass
`gaussian_linearized_gauge_check.py/json`. The additional exact checks in
`gaussian_linf_holder_check.py/json` pass the full physical inverse-defect
residual identity, both quadratic source formulas, the Holder exponent
balance, and the constants in the complex Gaussian split. The constants
648, 162pi and the tail exponent Y²/288 in the companion complex lemma
were independently audited. Compactness, distributional operator bounds,
Fourier estimates and complex growth remain analytic proofs rather than
machine-formalized claims.

The theorem concerns uniform response as amplitudes tend to zero. It
does not establish whether the isolated data epsilon=1e-6 possess a
continuous exact solution, and it assigns no eta for a numerical
reference at that amplitude. It does not exclude response exponents at
or below one half, or families without any such power-law response bound.

## 8. Corollary for exact spectral Galerkin linear responses

There is also a grid-refinement obstruction for a precisely specified
linearized approximation. Keep z continuous and use exact Fourier
Galerkin projection P_N in X, retaining |n|<=N about the exact continuous
Gaussian base. Define

    A_b=v^b-4+u_z^b, B_b=v^b-4-u_z^b,
    a_N=s_N+r_N,z, b_N=s_N-r_N,z,
    r_N=integral_0^z (a_N-b_N)/2, s_N=(a_N+b_N)/2.

The projected linear system is

    a_N,t=-a_N,XX-P_N partial_X(u^b a_N+A_b r_N),
    b_N,t= b_N,XX-P_N partial_X(u^b b_N+B_b r_N).      (H11)

For fixed N this is a bounded linear time-dependent ODE on the Banach
space of continuous z-dependent Fourier coefficients. The Volterra
integral defining r_N is bounded. The exact base coefficients are
smooth on the common compact time interval, so (H11) is well posed
there. Smooth z data stay smooth. Set its initial fields to either
(r_N,s_N)=(phi K,0) or (0,phi K), with a_N,b_N determined above. The
actual carrier index is kappa/d=48, so these initial conditions are
represented exactly whenever N>=48.

Because P_N commutes with X derivatives and the transverse integral,
(H11) is equivalent to the projected conservative physical system

    r_N,t=-partial_XX integral_0^z s_N-P_N partial_X(u^b r_N),
    s_N,t=-r_N,XXz-P_N partial_X(u^b s_N+(v^b-4)r_N).  (H12)

Suppose the physical responses r_N,s_N were uniformly bounded in
spacetime maximum norm for N>=48 on any common [0,T], T>0. A weak-star
subsequence would converge. In the weak formulation of (H12), move
P_N onto the smooth test function; P_N of that test converges in every
smooth norm. The limit therefore solves the complete continuous
linearized physical PDE and preserves the exact initial traces. The
distributional impossibility in Section 6 excludes this limit.

Consequently

    sup_(N>=48) sup_(X,z,0<=t<=T)(|r_N|+|s_N|)=infinity

for every 0<T<=.01. At least one physical field has unbounded response
along a subsequence of Fourier cutoffs. This concerns continuous-z,
exact spectral Galerkin linearization about the exact base. Applying it
to a fully discrete Centered-SD or Endpoint-SD experiment would require
a separate consistency and compactness argument. It is not a statement
that a nonlinear solution at the single target epsilon is absent.
