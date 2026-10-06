# DLW: bounded locality and constant bracket calculations

Let E f_j=f_{j+1}, d=(1-E^-1)/h, M=(1+E^-1)/2, D=partial_x,
beta=h^2/32. On a cyclic N-lattice, Pi is the lattice average and P=I-Pi.
Define R=d^-1 M on Ran(P), extended by R Pi=0. The formal evolutionary closure is

    U_t = -D(U^2/2+beta w^2)-D^2 U-R D^2 w,
    w_t = -D(Uw)+D^2 w.

This closure reproduces the original implicit first equation iff D^2 Pi w=0.
Its second equation need not preserve that condition on an unconstrained function
space. Section 4 audits a genuine Hamiltonian closure on a periodic compatible
phase manifold, and makes the locality test directions admissible there. Results
are not blanket results for every constrained subspace or boundary condition.

## 1. Exact lattice inverse and locality obstruction

For z=e^(i theta), theta != 0,

    R(z) = h/2 * (z+1)/(z-1) = -i h/2 cot(theta/2).

Thus R*=-R with the real equal-weight pairing. On the fixed N cyclic lattice,

    R = h sum_{l=1}^{N-1} (l/N-1/2) E^l.

The coefficient pairs l,N-l are opposite. For even N the l=N/2 coefficient is
zero. The exact cyclic radius is floor((N-1)/2) for N>=3; R=0 for N=1,2.
In particular N=3,4 genuinely permits radius 1, and N=5,6 permits radius 2.
Calling a fixed finite N matrix “infinite range” would be inaccurate.

Suppose a Laurent polynomial B(z), supported in [-r,r], agrees with R(z) on
all N-1 nonzero cyclic Fourier modes. Then

    Q(z) = (z-1) z^r B(z) - h/2 z^r(z+1)

is a polynomial of degree <=2r+1 with N-1 distinct roots. If N>=2r+3 it
must vanish identically, but Q(1)=-h !=0. Hence such B does not exist. The
same pole excludes every finite Laurent polynomial on the infinite lattice.

At any constant background, the U_t derivative in a w direction and a nonzero
x Fourier mode contains k^2 R(z), plus a lattice-local term. Therefore a
smooth local evolutionary representation of cyclic radius r is impossible
for N>=2r+3, provided those nonzero lattice test directions belong to the
phase space. This excludes any local J and local Hamiltonian gradient whose
composition has that radius, including field-dependent J; no Jacobi test is
needed because matching the vector field already fails. Differential-order
limits are irrelevant to this particular lattice obstruction.

For a nearest-neighbor bond density H=sum H_j(z_j,z_{j+1},Dz_j,Dz_{j+1}),
the variational gradient has radius 1. J of radius 1 gives composite radius
<=2 and is excluded for N>=7. A density spanning j-1,j,j+1 can give gradient
radius 2, so radius-1 J gives radius <=3 and exclusion starts at N>=9.
These bounds should be stated with the exact density support convention.

The physical change v=w+C U, C=(E-E^-1)/(2h), is local invertible. For a
v-only tangent perturbation, w changes by the same amount; the nonlocal
U_t coefficient remains R, so this obstruction also holds in (u,v).

## 2. A constant bracket that does work for the explicit closure

With periodic x (or vanishing boundary terms), set

    J0 = [[0,D],[D,0]],
    H = h sum_j integral [-U^2 w/2-beta w^3/3+U D w-w R D w/2] dx.

Since D*=-D and R*=-R, and R commutes with D, (RD)*=RD. Consequently

    delta H/delta U = -Uw+Dw,
    delta H/delta w = -U^2/2-beta w^2-DU-RDw.

J0 times this gradient is exactly the explicit closure. J0 is skew and has
zero Schouten bracket because all coefficients are field-independent; its
bracket obeys Jacobi on the algebra of suitably smooth functionals. The
Hamiltonian is cubic, uses first x derivatives, and has the exact lattice
range of R. It is not a finite-range Hamiltonian uniformly in N.

For T=[[1,0],[C,1]], C*=-C, one gets T J0 T*=J0. Thus in the requested
coordinates z=(u,v), the same J0 works with H(u,v-Cu). Its density then
contains first x derivatives and nearest-neighbor local terms plus the
R term. This identity does not cure the nonlinear mean compatibility issue.

## 3. Narrow Helmholtz exclusions

For a constant algebraic symplectic bracket J=a[[0,1],[-1,0]], a!=0,
the inferred U gradient is -F_w/a. Its U Frechet derivative is

    a^-1 D circ w,    whose adjoint is -a^-1 w D.

These are unequal for general w. Therefore the inferred covector is not a
variational gradient, even if the Hamiltonian is allowed to be nonlocal.
This excludes only this zero-order algebraic bracket class.

For J=A D with a constant invertible real symmetric scalar matrix A, write
A^-1=[[a,b],[b,c]]. Since F=D G,

    G=(-U^2/2-beta w^2-DU-RDw, -Uw+Dw).

The diagonal Frechet derivatives of q=A^-1G contain -aD and cD. Their
selfadjointness forces a=c=0; b!=0 follows from invertibility. The remaining
cross derivatives then match by adjunction. Hence J is a scalar multiple
of J0 in this subclass, and H is the corresponding scaled nonlocal H above.
Possible additions from the kernel of D do not affect these tests on nonzero
x modes. This is a classification only of A D with scalar constant A;
Laurent-valued A, higher-order brackets, singular brackets, nonconstant
coefficients, and Dirac reductions are outside this calculation.

## Evidence

`check_algebra.py` verifies the cyclic inverse and skew coefficients for
N=3,...,18, the physical-coordinate bracket conjugation, and the symbolic
Helmholtz coefficient constraints. These are supporting exact algebra
checks, not substitutes for the boundary and invariant-phase-space proof.

## 4. Audit of the constrained periodic Hamiltonian construction

Fix real constants c!=0 and C. Write q=PU, s=Pw and

    U=B+q, w=c+s, B=(C-Pi(qs))/c.

Then Pi(w)=c and Pi(Uw)=C pointwise in x. All meanzero q,s are free
coordinates, so this is a smooth graph phase manifold. A Hamiltonian with
the opposite sign to Section 2 is more convenient:

    Hfull = h sum integral [U^2 w/2+beta w^3/3-U Dw+w RDw/2] dx,
    HC = (Hfull-C h sum integral U dx) restricted to the graph,
    Jred = -[[0,PD],[PD,0]].

The U derivative of the unrestricted HC is Uw-Dw-C. Its lattice average
vanishes on this graph. Therefore every delta B term drops out of the
restricted variation. The reduced derivatives are exactly

    HC_q = P(Uw-Dw-C),
    HC_s = P(U^2/2+beta w^2+DU+RDw).

Jred times this gradient gives the projected U equation and the complete w
equation, because Pi(Uw)=C is constant. B_t is supplied by differentiating
the graph relation. Thus the original implicit SD holds identically, with
the chosen fixed c,C closure for the otherwise free mean mode. Fixing C
also in time is an additional specified closure, not a consequence of the
original first difference equation alone.

For S=Pi(qs), the reduced Hamiltonian can also be written as Nh times the
x integral of

    -(C-S)^2/(2c) + c Pi(q^2)/2 + Pi(q^2 s)/2
    + beta c^3/3 + beta c Pi(s^2) + beta Pi(s^3)/3
    - Pi(q Ds) + Pi(s RD s)/2.

Thus the unreduced trial density is cubic, while the exact elimination of
the mean adds a global quartic term -S^2/(2c). A final description should
not call this restricted Hamiltonian a local cubic polynomial density.

Let physical u=U-2a, v=w+4+C0 u, C0=(E-E^-1)/(2h). Put r=Pv=s+C0q.
Since Pi(q C0q)=0, B=(C-Pi(qr))/c. The shear (q,s)->(q,r) preserves Jred
because C0*=-C0. With rho=-1/c and b0=C/c-2a, the physical graph is

    u=b0+q+rho Pi(qr),   v=c+4+r.

Its derivative from meanzero coordinates is

    A = [[I+rho Pi M_r, rho Pi M_q],[0,I]],
    A* eta = (P eta_u+rho r Pi eta_u, P eta_v+rho q Pi eta_u).

Consequently Jphys=A Jred A* is skew and Poisson: this is a coordinate
pushforward of a constant Poisson bracket. Jacobi follows from the chain
rule for functionals, independently of a Lax pair. An ambient extension
uses coordinates (q,r,b=Pi u-rho Pi(qr),d=Pi v), assigns zero brackets to
b,d, and pushes the same constant bracket forward. Its c,C graph is a
Poisson leaf (possibly further degenerate due to x-constant Casimirs).

The pointwise constraints f=Pi v-c-4 and
g=c(Pi u+2a)+Pi[(Pu)(Pv)]-C have ambient gradient representatives (0,1)
and (c+r,q). A* annihilates both because 1+rho c=0. This independently
checks that the lifted operator is tangent to the intended constraints.

At q=r=0, the graph tangent has arbitrary nonzero lattice Fourier modes,
and A is the identity on these modes. Thus the bounded locality exclusion
in Section 1 applies to the genuinely constrained Hamiltonian vector field,
including in physical (u,v) coordinates. Jphys contains Pi and therefore
has full cyclic lattice dependence; HC contains R. This positive candidate
lies outside the uniformly finite-range J and H class that was excluded.

The proof assumes periodic x, equal lattice weights, sufficient x smoothness,
fixed N,h, c!=0, and a differentiable functional algebra on which variations,
adjoints, and the chain rule apply. For N finite, R is bounded and no lattice
inverse-domain issue remains. It is an algebraic Hamiltonian result, not a
well-posedness theorem for the mixed forward/backward x evolution.
