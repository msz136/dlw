# Periodic field hierarchy: theorem and analytic obstruction

2026-10-06. This document integrates the existing MONODROMY_POISSON_PROOF.md
and the separately audited INDEPENDENCE.md. The new analytic obstruction is
proved below. All Hamilton vector fields are formal differential expressions
unless an actual solution space and local flow are explicitly constructed.

## Phase space

Fix N>=2, h>0, x in R/(ell Z), c!=0, gamma constant. Let Pi denote the
lattice mean and P0=1-Pi. Coordinates p,s are smooth real periodic fields
with Pi p=Pi s=0; w=c+s and U=p+(gamma-Pi(ps))/c. Also fix each x mean
of p_j,s_j. These are the Casimirs of Jred=-offdiag(P0 D), with pairing
h sum integral. This is an affine Frechet Casimir leaf in the p,s coordinates.
Its weak symplectic inverse is -offdiag(D^-1) on zero-x-mean variations.
Physical fields are u=U-2a, v=w+delta0 p+4. The inverse is p=P0u,
s=P0(v-delta0u-4); thus no soliton ansatz is imposed.

The equations and mean closure are exactly those of
../dlw_hamilton_20261004/phase_space/periodic_reduction.md.
N=1 has no reduced field degrees of freedom. c=0 needs a different reduction.

## Formal theorem

Put g_j=hw_j/4, G=sum g=hNc/4, T=sum Ug=hNgamma/4;
A_j=(U_j+g_j)/2, B_j=(U_j-g_j)/2, S_j=(D-B_j)^-1(D-A_j).
Let P=S_(N-1)...S_0, a0=-G, b0=(G^2-T)/2 and
L=a0(P-1)^-1+b0/a0=D+sum ell_k D^-k.
Define I_n=integral res L^n, n>=1, and Pmom=h sum integral p s.

The following statements hold on the smooth periodic differential-functional
algebra, with constants fixed as above:

1. Every coefficient and every I_n is defined by a finite differential
   polynomial divided by a power of G. The formal infinite PDO series need
   not converge in an operator norm for any one of these functionals to exist.
2. I_n and Pmom mutually Poisson commute under the same Jred.
3. Pmom,I_1,I_2,... are independent in the finite-subfamily sense at a
   single smooth point on each Casimir leaf, and on a dense residual subset
   of that leaf. Each finite initial family is independent on an open dense set.
4. The physical Hamiltonian satisfies
       K=-8G I_1+(T/G)Pmom+constant.
   Thus X_K=-8G X_(I_1)+(T/G)X_(Pmom), with X_(Pmom)=-D(p,s).
   In particular every I_n is conserved along every sufficiently regular
   solution, and these formal Hamiltonian vector fields commute.

Proof of (1),(2): the factor recursion, Adler product/inverse calculation,
constraint tangency and restriction argument in MONODROMY_POISSON_PROOF.md.
Proof of (3): INDEPENDENCE.md, including the weight filtration and local
affine witness. The localized two-site fields serve only as tests of
covectors; no invariant two-site dynamical reduction for N>2 is assumed.
Proof of (4): rho1=-K_density/(8G)+T Pmom_density/(8G^2)
+G^2/12-T^2/(4G^2) modulo an x derivative. This fixes all coefficients
and the sign of the translation term, not merely the monodromy evolution.

## An exact obstruction to a differentiable local physical flow

Take the constant equilibrium p=s=0, U=U0=gamma/c, w=c, on its fixed
Casimir leaf. The mean reconstruction has zero first derivative there.
The linearized reduced equations are

    p_t=-U0 Dp-2 beta c Ds-D^2p-RD^2s,
    s_t=-c Dp-U0 Ds+D^2s,           beta=h^2/32.

For lattice frequency theta=2pi m/N, 1<=m<N, write
R(theta)=-i rtheta, rtheta=(h/2)cot(theta/2).
For continuous wave number k=2pi l/ell, l!=0, the Fourier matrix is

    M(k,theta)=-i U0 k I +
       [[k^2, -i(2 beta c k+rtheta k^2)],[-i c k,-k^2]].

Its two eigenvalues satisfy the exact identity

    (lambda+i U0 k)^2
       = k^4-c rtheta k^3-(h^2 c^2/16) k^2 =: Delta(k,theta).

For fixed theta, Delta/k^4 -> 1. For all sufficiently large positive k,
sqrt(Delta)>=k^2/sqrt(2); the plus branch grows at least this fast. There
is no lattice mean or continuous mean in these modes, so fixing all
Casimirs and fixing gamma does not remove them. A complex eigenmode and
its conjugate at (-k,-theta) yield a real perturbation.

For any fixed t>0, normalize these real eigenfunctions to unit H^r norm.
Their images under the linearized solution operator have H^r norms
exp(t sqrt(Delta)). They are unbounded as k increases. The same conclusion
holds from H^r to H^(r-d) for any finite derivative loss d. Consequently
there is no local solution map differentiable at this equilibrium whose
derivative solves this linearized equation as a bounded map between these
Sobolev spaces. In particular, no C1 Hamiltonian local flow on an open
Sobolev neighborhood of this equilibrium can realize the physical equation.
This assertion does not use an unjustified inference from linear instability
to failure of all continuous nonlinear solution maps.

It also excludes a continuous linearized solution operator C-infinity to
C-infinity: coefficients exp(-k) times normalized growing eigenvectors
give smooth initial data, while at any t>0 the resulting coefficients
grow faster than every polynomial, hence do not define a distribution.
Analytic strip losses exp(-(rho-rho')|k|) cannot compensate exp(t k^2).

A Fourier Gaussian weight exp(rho k^2) could absorb the *linear* growth
by a loss of rho, but this is not a proved nonlinear phase space. For
example convolution of exp(-rho k^2) with itself decays like
exp(-rho k^2/2), so multiplication generally consumes Gaussian radius.
The existence, uniqueness, continuous dependence and common hierarchy
domains in any such scale require separate proof.

## Remaining exact mathematical tasks

Infinite independent commuting integrals prove isotropy, not completeness.
On the smooth symplectic leaf set V_z=span{X_Pmom(z),X_I_n(z):n>=1}.
In a specified topology, a Liouville-type completeness statement would
require a suitable closure of V_z to be maximal isotropic; equivalently
one must identify its symplectic orthogonal (or an appropriate spectral
replacement). Pairwise involution only gives V_z subset V_z^omega.
Countably many independent covectors on an infinite-dimensional space do
not imply equality. No such equality or spectral inverse theorem has
been proved for the present physical-field monodromy map.

The analytic no-go above is a concrete obstruction in the usual Sobolev
category near a compatible constant equilibrium. It does not refute
formal integrability, special finite-gap solution spaces, possible other
regular points, or a suitably constructed analytic scale. Nor does it
extend the theorem to c=0 or the infinite nonperiodic lattice. These are
separate problems, not conclusions supplied by the formal trace algebra.
