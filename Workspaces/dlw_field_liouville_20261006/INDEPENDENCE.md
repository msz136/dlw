# All-order functional independence on the periodic DLW field space

2026-10-06. This is an algebraic proof for general smooth periodic fields,
not a claim inferred from a finite determinant or a soliton family.

## Statement and conventions

Let N>=2, h>0, x in R/(ell Z), c!=0 and gamma be fixed. Set
G=hNc/4, T=hNgamma/4, g_j=hw_j/4, mu=T/G. Reduced coordinates are
p_j=U_j-mean_j U, with sum p_j=0, sum g_j=G, and

    U_j=p_j+m,       m=(T-sum p_j g_j)/G.

Fix arbitrary compatible sitewise x means of p_j and g_j. This defines an
affine Frechet space C of smooth reduced fields (one Casimir leaf).
Define Pmom=4 integral sum p_j g_j dx, and the monodromy integrals I_n
as in THEORY.md. For EVERY such C there is a point at which

    dPmom, dI_1, dI_2, ...

are linearly independent in the finite-subfamily sense, as covectors on C.
For each M, independence of Pmom,I_1,...,I_M holds on an open dense subset
of C. Simultaneous finite-subfamily independence holds on a dense residual
subset. We do not assert one common open set for all orders, a basis of
the cotangent space, or Liouville completeness.

## 1. Two active sites

Write g=G/2 (which can be negative). On an open x interval choose

    g_0=g+e,  g_1=g-e,  g_j=0 (j>=2),
    p_0=f,    p_1=-f,   p_j=0 (j>=2),
    m=mu-fe/g.

Then U_0=m+f, U_1=m-f and all other U_j=m. Factors with g_j=0 are
exactly (D-U_j/2)^(-1)(D-U_j/2)=1, even when U_j is variable.
The full N-site monodromy is the two-factor product S_1 S_0 on this
interval. This restriction is used to evaluate covectors; its invariance
under the DLW evolution is neither needed nor asserted.

Suppressing derivatives, replace D by a commuting variable z. Direct
rational multiplication and division give the complete symbol

    L_cl(z)=z+q/(z-b),
    q=(g^2-e^2)(g^2-f^2)/(4g^2),   b=mu/2-fe/g.

Therefore the derivative-free part R_n of rho_n=res L^n is

    R_n = sum_(t=1,...,floor((n+1)/2))
          binom(n,t) binom(n-t,n+1-2t) q^t b^(n+1-2t).

At e=0 define nonzero numbers

    C_k=(-1/4)^k binom(2k-1,k),
    D_k=-(k/g)(-1/4)^k binom(2k,k).

The highest degrees follow from the last summand t=k:

    [f^(2k)] R_(2k-1)(f,0)=C_k,
    deg_f partial_e R_(2k-1)(f,0) <=2k-1,
    deg_f R_(2k)(f,0) <=2k,
    [f^(2k+1)] partial_e R_(2k)(f,0)=D_k.

For the second identity, q_e(f,0)=0, while differentiating b introduces
one f and the remaining terms have t<=k-1. These formulas are valid for
all k, not just the twelve pairs checked by the accompanying script.

## 2. Derivative filtration: why the leading terms cannot cancel

Work in differential polynomials in f,e, allowing coefficients rational
in the fixed nonzero g and polynomial in mu. Give f^(r) weight 1+r and
e^(r) weight r. Constants have weight zero. Thus a monomial has weight
equal to its number of f factors plus its total derivative count.

The one-site expansion S_j=1+sum s_(j,k)D^(-k) obeys

    s_(j,1)=-g_j,
    s_(j,k+1)=B_j s_(j,k)-D s_(j,k),
    B_j=(U_j-g_j)/2.

Since B_j has weight at most 1, s_(j,k) has weight at most k-1 by
induction. The PDO multiplication formula then gives weight(p_k)<=k-1
for the coefficients of P. For products of t negative terms, the sharper
bound is k-t; each differentiation in the multiplication rule adds its
order to both sides. At the constrained two-site fields p_1=-G=a and
p_2=(G^2-T)/2=b_0 are constants.

The identity (P-1)L=a+(b_0/a)(P-1), by induction on the negative order,
gives weight(ell_k)<=k+1. In res L^n a term using t negative L terms
and total additional differentiation r has

    sum k_i+t+r=n+1.

Its weight is at most n+1. Hence weight(rho_n)<=n+1. Euler variation
in f reduces weight by 1; Euler variation in e does not increase weight:

    weight(E_f rho_n)<=n,       weight(E_e rho_n)<=n+1.

Integrating derivatives off a variation does not invalidate these bounds:
differentiation with respect to a jet removes that jet's derivative weight,
and the subsequent (-D)^r restores exactly r.

Terms containing derivatives before Euler variation still contain at least
one derivative after a nonzero Euler variation. Integration by parts cannot
create a derivative-free term. Thus the top derivative-free coefficients
computed in section 1 are not affected by PDO derivative corrections.

At e=0 these facts imply the degree bounds, where degree counts f jets:

    E_f rho_(2k-1): degree <=2k-1, top term 2k C_k f^(2k-1);
    E_e rho_(2k-1): degree <=2k-1;
    E_f rho_(2k):   degree <=2k-1;
    E_e rho_(2k):   degree <=2k+1, top term D_k f^(2k+1).

The asserted top terms are the unique terms of those highest degrees in
the indicated components: any derivative correction has lower degree by
the weight bound. No assumption on a particular x wavelength is used.

## 3. Explicit periodic Fourier witness

For the Casimir means given by the globally defined two-site fields, take
e=0, f=A cos(2pi x/ell), A!=0. The Euler gradients are trigonometric
polynomials; a product of d f jets has Fourier frequency at most d.
Order the zero-mean tangent directions as

    delta e=cos x, delta f=cos x,
    delta e=cos 3x, delta f=cos 3x, ...

(replace x by 2pi x/ell). With x-mean normalization, the Jacobian of
Pmom,I_1,I_2,I_3,... is lower triangular. Its successive diagonal entries
are

    4A, -A/4,
    D_k A^(2k+1)/2^(2k+1),
    (2k+2) C_(k+1) A^(2k+1)/2^(2k+1),       k>=1.

All are nonzero. Terms of lower frequency pair to zero and
mean(cos^r x cos(rx))=2^(-r) for r>=1. The determinant of each finite
initial square block is their product. Restoring integral normalization
multiplies each row by ell and does not alter independence.

The exact PDO computation for Pmom,I_1,...,I_5 at g=3,mu=2,A=2/5 gives
det=-3/97656250000000, using x means. It checks derivative corrections
through order five; the preceding induction proves the all-order claim.

## 4. Every fixed Casimir leaf, with the same point for all orders

To avoid any restriction on the sitewise x means, choose a small open
interval J and a smooth periodic field equal on J to the two-site state

    e=0,   f=A y,   A!=0,

where y is a local x coordinate. Extend the reduced coordinates smoothly
outside J, keeping sum p=0 and sum g=G. Smooth corrections supported
outside J enforce ANY prescribed compatible sitewise x means. This is
possible because the mean corrections sum to zero for both coordinate
vectors; a single outside bump of nonzero integral suffices for each
vector of corrections. Thus the resulting field lies in the requested C.

On J all Euler gradients restricted to variations in f,e are polynomials
in y. A monomial with d f jets has degree in y at most d, with strict
inequality if at least one derivative occurs. In particular the unique
leading terms in section 2 retain exactly their stated coefficients.
The restricted momentum density is 8fe: its gradients at e=0 are
(E_f Pmom,E_e Pmom)=(0,8Ay).

Suppose a finite constant linear combination of the covectors vanishes
on the Casimir tangent space. Test against arbitrary delta f,delta e
smoothly supported in J and having zero integrals. Both restricted Euler
gradients of that combination must be CONSTANT on J. Let n be the largest
index with nonzero coefficient:

* If n=2k-1, its f gradient has nonzero y^(2k-1) coefficient
  2k C_k A^(2k-1); every preceding f gradient has smaller degree.
* If n=2k, its e gradient has nonzero y^(2k+1) coefficient
  D_k A^(2k+1); every preceding e gradient has smaller degree.

Both contradict constancy. Remove successive highest indices; finally
8Ay forces the momentum coefficient to vanish. This proves independence
of EVERY finite subfamily at this single smooth point of C, modulo all
Casimir covectors. It also proves independence for N=2 and arbitrary
ell,h,c!=0,gamma. N=1 has no reduced field degrees of freedom and is
excluded deliberately.

## 5. Genericity

For each M select M+1 fixed admissible tangent vectors giving a nonzero
minor at the point above. Such vectors exist by finite-dimensional linear
algebra applied to the independent covectors. Let Delta_M(z) be the minor.
It is a continuous polynomial functional of finitely many derivatives of
the reduced coordinates; denominators involve only fixed G. It is nonzero
at the witness.

For any other z in C, Delta_M(z+t(z_star-z)) is a polynomial in t and is
nonzero at t=1. Its zeros cannot accumulate at t=0. Points arbitrarily
near z therefore have Delta_M!=0. The nonvanishing set is open dense.
The countable intersection over M is dense by the Baire theorem for the
affine Frechet space C. This gives residual all-order finite-subfamily
independence, not the maximal-isotropic condition needed for a genuine
infinite-dimensional Liouville theorem.
