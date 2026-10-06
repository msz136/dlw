# Two-site physical fields, invertible Miura data, and a local conservation recursion

2026-10-06. Constructive proof draft. Here a below is a new field coefficient, not the original constant DLW parameter a. The main report denotes this field coefficient by alpha.

## 1. A standard two-field PDE reached by an explicit map

Use the two-site chart of the previous notes. eta=hc/8 !=0, B=gamma/(2c), f=p/2-eta,
g=-s_x/c+(1-s²/c²)(p/2+eta), C=B-ps/c.
On the real chart where f is nowhere zero, put
a=fg,
d=C+f_x/f=B-ps/c+p_x/(p-2eta).
Then
L=D-f(D-C)^-1g = D-(D-d)^-1 a.
The physical time evolution pushes forward exactly to
a_t=a_xx-2(ad)_x,
d_t=-d_xx-(d²)_x+2a_x.
Both identities have been verified with arbitrary symbolic jets and c,gamma,eta in two_site_exact.py, using beta=2eta²/c².

This is a two-boson/Kaup--Broer-type representation. It has, independently, the elementary Hamilton representation
J1=[[0,D],[D,0]], H1=integral(a²-ad²-a d_x),
since H1_a=2a-d²-d_x and H1_d=a_x-2ad.
This does not identify J1 with the pushforward of our original field bracket; that separate bracket still supplies the involution result established earlier.

## 2. Full scalar L retains the physical fields, with the appropriate Casimirs

Assume in addition a is nowhere zero, so coefficients of L recover
a=-ell1,
d=(a_x-ell2)/a.
Define the marked spectral values lambda_low=B-2eta and lambda_high=B+2eta. The physical fields determine
Y_low=f(1+s/c),
Y_high=-f(1-s/c).
They solve independent Riccati equations
Y_x=Y²+(d-lambda)Y-a
at their respective marked values. Conversely, any smooth periodic Riccati pair with Y_low-Y_high nowhere zero reconstructs
p=2eta+Y_low-Y_high,
s=c(Y_low+Y_high)/(Y_low-Y_high).
Exact symbolic substitution in both directions recovers a and d identically. inverse_two_site_certificate.py certifies these statements.

The Riccati equation linearizes by Y=-phi_x/phi to
phi_xx+(lambda-d)phi_x-a phi=0.
This also follows from L psi=lambda psi with phi=exp(-lambda x)psi. A periodic real Y corresponds to a positive, nonvanishing Floquet solution phi, determined up to scale. Thus inverse reconstruction reduces to choosing Floquet eigenlines at TWO fixed spectral values, not choosing two arbitrary functions.

A 2x2 monodromy has at most two eigenlines unless it is scalar. For an actual real regular field in this chart, the scalar possibility is excluded: given its nodeless Floquet solution phi, reduction of order gives the second solution using the strictly positive integrand exp(integral(d-lambda))/phi². If the two multipliers coincide, its integral over a period is positive and the monodromy is a nontrivial Jordan matrix, not scalar. Thus the full scalar operator has at most four real regular physical preimages before fixing mean Casimirs.

There is a stronger fixed-leaf uniqueness statement. Let Lx be the spatial period. For each chosen Floquet eigenvalue mu1, the ratio mu2/mu1 of the other eigenvalue to it equals
exp integral(2Y+d-lambda).
Our exact identities give
2Y_low+d-lambda_low = p-(2eta/c)s+f_x/f,
2Y_high+d-lambda_high = -p-(2eta/c)s+f_x/f.
Since real f is nonzero and periodic, integral f_x/f=0. Therefore the two ratios are fixed by the two original mean Casimirs integral p and integral s. Distinct multipliers have their branch fixed by the ratio; at equal multipliers the eigenline is unique by the Jordan argument. Hence L uniquely determines p,s on each fixed-(integral p,integral s) real regular leaf in the image.

The mean-zero leaf deserves special care: both marked multipliers coincide throughout it. One must NOT impose 'simple marked eigenvalues' as a generic condition on that leaf. They are Jordan rather than scalar, and the preceding argument still works. At the uniform background this follows explicitly: the marked companion matrices have a nonzero nilpotent part N with N²=0, so exp(Lx A)=exp(Lx trace(A)/2)(I+Lx N).

## 3. Local differentiable reconstruction near the uniform field

At p=s=0, a=-eta² and d=B. For variations preserving both x means,
delta a=(eta/c)D delta s,
delta d=-(1/(2eta))D delta p.
Let r>1/2. The map
(p,s) in H^(r+1)_0 × H^(r+1)_0 -> (P_x a,P_x d) in H^r_0 × H^r_0
is analytic near zero, and its displayed derivative is an isomorphism because D is invertible on zero-mean periodic functions. Banach's inverse function theorem gives a local analytic inverse. The two coefficient means are then analytic functions of these zero-mean coordinates; the image is a codimension-two graph.

Thus the physical-field-to-Lax-coefficient map loses no continuous state information on this local fixed-Casimir leaf. This is coefficient-level reconstruction, not a proof that eigenvalues or conserved traces alone determine the state. The physical and two-field PDEs are locally equivalent on this image chart, since the differential map is invertible there and the vector-field pushforward was checked exactly.

## 4. A simple all-order local density recursion

Take the small formal Riccati branch Y(lambda)=sum_{n>=1} rho_n lambda^-n. Coefficient matching gives
rho1=-a,
rho_(n+1)=d rho_n-D rho_n+sum_{i=1}^{n-1}rho_i rho_(n-i).

The time equation from psi_t=-(D²-2a)psi is
Y_t=-D((lambda+d)Y+a),
hence for every n>=1,
(rho_n)_t+D(rho_(n+1)+d rho_n)=0.
Compatibility of the Riccati and time equations follows from the two-field PDE above; equivalently it is the scalar Lax identity. Formal uniqueness of the small branch supplies the all-order argument. Each coefficient is a finite differential polynomial, so each local identity has an ordinary meaning on sufficiently smooth fields.

First examples:
rho1=-a,
rho2=a_x-ad,
rho3=-a_xx+2d a_x+a d_x-ad²+a².
After integration over x:
C1=-integral a,
C2=-integral ad,
C3=integral(a²-ad²+d a_x).
These are the normalized trace quantities integral res L^n/n modulo total derivatives. local_density_certificate.py verifies the first six full density/flux identities exactly on arbitrary jets. No tau ansatz is used.

## 5. What this resolves, and what remains

It resolves a concrete question left open by a forward-only Lax construction: in the regular two-site field chart, the full operator carries enough information to recover the physical fields, and the recovery can be made locally analytic on a fixed mean leaf. We now have explicit forward and inverse descriptions and a short local density recursion.

The next genuinely spectral step is an inverse problem from appropriate periodic spectral data (Floquet multipliers together with eigenfunction/norming or divisor information) to a,d. Spectral invariants alone should leave the evolving angle data free. One must then match the relevant Poisson structure and establish completeness/maximality in a specified sense. This note does not silently equate Lax coefficients with completed action-angle spectral coordinates.

Literature anchors checked: Aratyn et al., Generalized Miura Transformations, Two-Boson KP Hierarchies and their Reduction to KdV Hierarchies, https://arxiv.org/abs/hep-th/9302125; Nabelek--Zakharov, Solutions to the Kaup--Broer system and its (2+1) dimensional integrable generalization via the dressing method, Physica D 409 (2020) 132478, https://doi.org/10.1016/j.physd.2020.132478 . The latter explicitly discusses the coexistence of integrability and Sobolev ill-posedness. The formulas and inverse reconstruction in this note are direct calculations for the current DLW period-two reduction, not a theorem claimed from those references.
