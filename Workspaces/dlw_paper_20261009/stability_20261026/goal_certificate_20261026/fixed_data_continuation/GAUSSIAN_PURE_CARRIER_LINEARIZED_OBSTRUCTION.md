# The actual Gaussian benchmark admits no classical first variation in either selected independent direction

2026-10-26. Analytic proof draft with exact symbolic checks. This result
concerns the actual Gaussian background and the actual fixed single-carrier
directions used in the experiments. It excludes a classical first variation
at perturbation amplitude zero. It does **not** prove nonexistence for the
single isolated amplitude epsilon=1e-6, and assigns no reference error eta.

## 1. Exact background and hypotheses

Use X=x-4t, z=y+2 in [0,4], period L=192, T=.01, alpha=pi/4. The known
unperturbed benchmark has initial fields

    u0=lambda f(z) F0(X), v0=4-3 u0,z,
    lambda=.05, f(z)=sin(alpha z),
    F0(X)=sum_j exp(-(X+192j)^2/36).

Its complete continuous solution is the certified heat/Laplace construction
in `../../../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md`
(path relative to this note; use the project entry for the
authoritative formula). The following equivalent quantities are used:

    s(z)=lambda f(z)/2,
    F_t=-F_XX, F(0)=F0,
    J0,X=F0, J0(X+L)=J0(X)+CL,
    C=sqrt(pi)/32>0,
    psi(X,z,0)=exp(-s(z)J0(X)).

The existing construction proves psi is nonzero on the closed physical
cylinder, and its explicit formula yields

    Phi=psi/F, Phi_t=Phi_XX+V Phi,
    V=2 partial_XX log F,
    Phi(X+L,z,t)=exp(-s(z)CL) Phi(X,z,t).                (G1)

The backward heat function F is strictly positive for all real X and
0<=t<=.01. Indeed, writing d=pi/96, its Fourier coefficients are

    F_n(t)=C exp(-(9-t)(nd)^2).

Poisson summation gives a positive constant times a periodic Gaussian sum
with positive width 9-t. There is therefore no real zero in the inverse
transform or gauge used below. For the chosen z*=1, s>0 and s_z>0. The
known denominator lower bounds for psi and D in the reference construction
also make the inverse Laplace invariant P1 nonzero on a neighborhood of
this entire real slice and time interval.

Assume, for contradiction, that an amplitude family of periodic continuous
DLW solutions exists near epsilon=0, equals this benchmark at zero, and has
a classical first variation (dot u,dot v). It suffices to require that
the variation has two z derivatives of u and one of v near z=1, and enough
continuous X/time derivatives for the differentiated equations below to
hold. For example C1 dependence on epsilon in a topology controlling these
z derivatives and all X derivatives with their PDE time derivatives is
sufficient. This is a deliberately explicit response class.

The initial variation is either

    (dot u0,dot v0)=(phi(z)Ck(X),0)
    or                         (0,phi(z)Ck(X)),
    phi=f^2=sin^2(alpha z), Ck=cos(kappa X), kappa=pi/2.

These are precisely the selected independent directions; no added tail or
replacement perturbation profile is introduced.

## 2. A transformed defect obeys a homogeneous linear equation

Put Q=-u/2, P=(v-4-u_z)/4. The exact BLP equations are

    Q_zt=(Q^2-Q_X)_Xz+2P_XX,
    P_t=P_XX+2(QP)_X.

One inverse Laplace step is

    P1=P-Q_z=(v-4+u_z)/4,
    Q1=Q-(log P1)_X.

For any such transformed solution, the defect R=P1-Q1,z satisfies the
EXACT identity

    R_t=-R_XX+2(Q1 R)_X.                                (G2)

At the certified benchmark R=0 and Q1=Phi_X/Phi. Consequently its first
variation obeys the homogeneous equation

    dot R_t=-dot R_XX+2[(Phi_X/Phi)dot R]_X.             (G3)

The variation of the coefficient Q1 multiplies the zero background defect,
so it drops out exactly. This is a derivative of the full nonlinear system,
not an independently substituted constant-background linearization.

The exact physical expression is

    R=(v-4+3u_z)/4+(log P1)_Xz.

At initial time P1=-lambda f'F0/2. Direct differentiation gives

    dot R0=a(z) Ck-b(z)(Ck/F0)_X,                       (G4)

    u-only: a=3phi'/4=(3/2)ff', b=f'/lambda;
    v-only: a=phi/4=f^2/4, b=(f^2/f')'/(2lambda).

At z=1, both a's are strictly positive: a_u=3pi/16 and a_v=1/8.
Every expression is regular in a real neighborhood of this slice.

## 3. Gauge and Darboux lift to free backward heat

Fix z=1 and set r=dot R/Phi, W=F_X/F. Equation G3 and G1 give

    r_t=-r_XX-2W_X r.                                   (G5)

Because F solves backward heat,

    W_t=-W_XX-2W W_X.

Thus the time-dependent Darboux operator T=partial_X-W intertwines free
backward heat with G5:

    (partial_t+partial_XX+2W_X)T h
         =T(partial_t+partial_XX)h.                    (G6)

The function r has Bloch multiplier exp(mu L), where mu=sC>0, while W
and F are periodic. For every time, solve

    (partial_X-W)h=r,
    h(X+L,t)=exp(mu L)h(X,t).                           (G7)

This has a unique smooth Bloch solution. Divide by the positive F and
integrate over a period; the homogeneous kernel is cF, whose multiplier is
one rather than exp(mu L). The multiplier exp(mu L)-1 is nonzero, fixing
the integration constant uniquely. The coefficients are smooth in time,
so the constructed h has the needed time regularity.

Combining G5-G7 yields T(h_t+h_XX)=0. The expression in parentheses has
the same nontrivial Bloch multiplier as h, whereas every element of the
kernel of T is periodic. Therefore

    h_t=-h_XX.                                         (G8)

No additional finite-dimensional kernel forcing survives in this sector.

## 4. A positive-time Bloch distribution forces Gaussian initial Fourier tails

Write h(X,t)=exp(mu X)p(X,t), with p periodic. Then

    p_t=-p_XX-2mu p_X-mu^2 p,
    p_n(t)=exp([(nd)^2-2i mu nd-mu^2]t)p_n(0).

If p at any positive time tau is a periodic distribution, its Fourier
coefficients have at most polynomial growth. Hence

    |p_n(0)| <= Ctau(1+|n|)^N exp(-tau(nd)^2+mu^2 tau).

The initial p, and therefore h0, extend to entire functions of complex X
of finite order at most two. This follows directly by completing the
square in the absolutely convergent Fourier series. A smooth first
variation supplies far more than the required positive-time distribution.

This step does not call h itself tempered on the whole real line: its real
Bloch factor exp(mu X) has exponential growth. The periodic factor p is
the distribution to which the Fourier argument applies.

## 5. Entire-function contradiction without asymptotic cancellation assumptions

At initial time 1/Phi=F0 exp(sJ0). Multiplying G7 by F0 and using G4 gives
the entire identity

    F0 h0'-F0' h0 = exp(sJ0) E,
    E=a F0^2 Ck-b(F0 Ck'-Ck F0').                      (G9)

The periodic Gaussian F0 is entire of finite order at most two, as follows
from its Gaussian Fourier coefficients. Its entire antiderivative J0 is
not a polynomial, because J0'=F0 is nonconstant periodic. The carrier Ck
is entire of order one. Thus E has finite order at most two and is not
identically zero: F0 is even, Ck is even, and

    E(0)=a F0(0)^2>0.                                  (G10)

If h0 had the Gaussian tails required by G8, the left-hand side of G9
would be an entire function of finite order at most two. Dividing by the
nonzero finite-order entire E makes exp(sJ0) a finite-order meromorphic
function. It is in fact entire and has no zeros. Hadamard factorization
then forces exp(sJ0)=exp(P) for a polynomial P, so sJ0-P is a constant
integer multiple of 2pi i, and J0 is a polynomial. This is a contradiction.

Equivalently, exp(sJ0) has infinite entire order; multiplication by a
nonzero finite-order entire E cannot lower it to finite order. The proof
therefore does not rely on a heuristic dominant term in an integral for
h0, and cannot be evaded by cancellation between its two explicit terms.

## 6. Precise theorem and relevance

**Theorem.** Around the actual certified Gaussian benchmark, neither of the
selected independent single-carrier physical-field directions admits a
periodic classical first variation on any positive time interval, in the
finite-z / smooth-X response class stated in Section 1. Consequently the
continuous solution map cannot be C1 at this benchmark in either selected
direction in any topology that supplies such a variation.

This is stronger and more data-specific than the previously established
nearby-high-frequency-tail obstruction: the direction itself is the exact
single cosine used by the experiment. Nonlinear coupling with the
nonzero Gaussian background creates the transformed infinite-order tail.

The theorem does not rule out a non-differentiable family of solutions, a
solution at one isolated nonzero epsilon, or weaker notions of response
without the derivatives needed by G2-G7. In particular it does not by
itself close the requested fixed-epsilon=1e-6 reference question. It does
exclude an ordinary classical linear-response certificate based on
differentiating the continuous solution in the actual perturbation size.

## 7. A finite classical norm cannot have a uniform O(epsilon) response bound

The no-first-variation theorem also gives a concrete, stronger conditional
instability statement without assuming differentiability of the family.
For definiteness use the tensor classical norm, on the full periodic
physical cylinder,

    ||(du,dv)||X = sup_t[||du(t)||_(C_X^4 C_z^3)
                        +||dv(t)||_(C_X^4 C_z^2)].

All mixed derivatives within each indicated rectangle are included. Suppose
epsilon_n ->0 are nonzero and there are classical exact solutions with
the specified initial fields and the same prescribed lower u trace. Then
it is impossible that

    sup_n ||(u^n-u^0,v^n-v^0)||X/|epsilon_n| < infinity. (G11)

Indeed, G11 bounds the normalized differences in these finite spatial
norms. The original PDE and the fixed lower u trace bound their time
derivatives in lower spatial norms: obtain u_t by integrating its z
equation from the fixed lower trace, and use the v equation directly.
Products are bounded in the stated classical norms. Arzela-Ascoli, with
the usual loss of at least one spatial derivative, gives a subsequence of
normalized differences converging uniformly with u's second and v's first
z derivatives, locally near z=1 and with the required finite X derivatives.
The PDE passes to its linearization in distributions; the quadratic
remainder divided by epsilon_n tends to zero. Initial and lower-boundary
variations remain exact. The resulting periodic distribution-valued
variation satisfies G3-G8, contradicting the entire-order argument.

Only a distribution solution of the final free backward heat equation was
used in Section 4, so the loss of derivatives in this compactness step does
not weaken the contradiction. One can increase the finite X orders in X
if a completely classical passage is preferred; no all-order transverse
Gevrey assumption is involved.

Thus, if solutions for arbitrarily small selected amplitudes exist, their
response cannot be uniformly bounded by a constant times epsilon in this
finite classical norm. This does not yet rule out a Lipschitz estimate for
the undifferentiated physical maximum norm alone, because G11 also controls
spatial derivatives. It does not rule out a single isolated nonzero datum.

Exact transformation, gauge, Darboux and initial-coefficient identities
are checked in `gaussian_linearized_gauge_check.py/json`. The Gaussian
positivity, Bloch inversion and entire-order argument are analytic proofs.
No claim of formal proof-assistant verification is made.
