# Exact match of the physical Poisson tensor with a compatible three-tensor hierarchy

2026-10-06. Constructive proof draft. All statements here concern the general two-site periodic field chart of the preceding notes. Field a below is alpha, not the original DLW constant. Use the normalized scalar bracket Jps=-[[0,D],[D,0]], corresponding to dividing the full two-site Hamiltonian by 2h.

## 1. Three explicit local operators

Let D=partial_x, and use right-normal form (coefficients to the left of D):

J1 = [[0,D],[D,0]],
J2 = [[2aD+a_x, -D²+dD],[D²+dD+d_x, -2D]].

Put w=2ad-a_x. Define
J3_11=2wD+w_x,
J3_12=D³-2dD²+(d²-d_x-4a)D-2a_x,
J3_21=D³+2dD²+(d²+3d_x-4a)D+d_xx+2d d_x-2a_x,
J3_22=-4dD-2d_x.
All three operators are skew-adjoint. J3 is the local formal expression associated with J2 J1^-1 J2; the proofs below do not replace the genuine periodic D inverse by a two-sided inverse.

## 2. Exact pushforward identity

For the Miura map from the previous note,
a=(p/2-eta)[-s_x/c+(1-s²/c²)(p/2+eta)],
d=B-ps/c+p_x/(p-2eta),
let F_* be its Frechet derivative. Then exactly

F_* Jps F_*^* = -(1/(2c)) [J3-2B J2+(B²-4eta²)J1].

poisson_pushforward_certificate.py computes every differential-operator coefficient in all four entries symbolically, including the variable-coefficient adjoints. Every residual is identically zero for arbitrary jets and c,eta,B. This is equality of the original pushed physical tensor, not a choice of an unrelated convenient bracket.

## 3. A direct proof of Jacobi and pairwise compatibility

For any fixed real c,eta!=0 and B, the map is locally invertible on an open periodic chart around p=P!=0, P!=±2eta, s=0. At that constant field its Frechet Fourier matrix is
[[P/2, -(P/2-eta) i k/c], [i k/(P-2eta), -P/c]],
with determinant -(P²+k²)/(2c), nonzero for every real Fourier wave number k. Its first-order elliptic inverse maps H^r to H^(r+1), including the zero mode because P!=0. Banach's inverse function theorem gives the chart (r>1/2).

Therefore the displayed pushforward is Poisson there. Its Jacobi residual is a differential-polynomial identity in a,d and their jets; validity on an open jet set makes it an identity everywhere. Vary B and eta over their open parameter ranges. Expanding the Schouten identity for
K(B,eta)=J3-2B J2+(B²-4eta²)J1
forces each [Ji,Jj] to vanish: eta^4 gives [J1,J1], B eta² gives [J1,J2], eta² gives [J1,J3], then the remaining B²,B,constant coefficients give [J2,J2],[J2,J3],[J3,J3]. Thus J1,J2,J3 are mutually compatible Poisson tensors. This proof uses the verified physical pushforward and polynomial dependence, rather than an unverified transfer of a named standard bracket.

## 4. All-order Lenard identities with the zero-mode term retained

Use the local Riccati generator y_x=y²+(d-lambda)y-a and C(lambda)=integral y=sum_{n>=1} C_n lambda^-n. Let v solve formally
(-D-2y-d+lambda)v=1.
Varying the Riccati equation and integrating by parts gives
g(lambda)=delta C(lambda)=(-v,yv).
A direct differential identity is
(J2-lambda J1)g=0,
(J3-lambda J2)g=(a_x,d_x).

The SECOND identity has a nonzero lambda^0 translation term. Dropping it would give a false generating identity. It contributes to no negative power, so coefficientwise for every n>=1:
J2 delta C_n=J1 delta C_(n+1),
J3 delta C_n=J2 delta C_(n+1)=J1 delta C_(n+2).

lenard_generating_certificate.py verifies the two full generating identities symbolically using arbitrary a,d jets and the exact y_x,v_x equations. local_density_certificate.py independently verifies the first four Lenard equations via Euler derivatives of the explicit densities, in addition to six conservation identities.

Because J1 delta C1=0, skew-adjointness and the Lenard shift give mutual involution of all C_n for J1, J2, J3, and hence for the exact physical pencil. Add C0=integral d if needed; J1 delta C0=J2 delta C0=0 and J3 delta C0=-2(a_x,d_x), so it commutes with all translation-invariant C_n as well.

## 5. The actual physical time flow belongs to this same hierarchy

The new PDE vector field X=(a_xx-2(ad)_x, -d_xx-(d²)_x+2a_x) obeys

X=J1 delta C3=J2 delta C2=J3 delta C1.

Here
C1=-integral a,
C2=-integral ad,
C3=integral(a²-ad²+d a_x).

The original normalized physical Hamiltonian has density
kappa=c p²/2-(gamma-ps)²/(2c)+beta c s²+s p_x,
beta=2eta²/c², gamma=2Bc.
It satisfies the exact functional identity

K_phys=2c integral a-2Bc integral d+2c eta² Lx,

because the density difference is
2c eta² + D[ps-2eta s+2Bc log|p/2-eta|].
Consequently X=J_phys delta K_phys for the very same pushed-forward physical pencil. The transformed time evolution and Poisson tensor have both been matched.

## 6. Why the marked inverse spectral values appear

The physical pencil polynomial is (lambda-B)²-4eta², with roots lambda_±=B±2eta, exactly the two marked values in the inverse Riccati reconstruction.
For an actual nonresonant periodic Riccati branch at either root (not merely substitution into an unproved convergent formal series), the generating calculation gives
J_phys delta C(lambda_±)=-(a_x,d_x)/(2c),
J_phys delta integral d=(a_x,d_x)/c.
Thus C(lambda_±)+(1/2)integral d is a Casimir. Its nonconstant part equals one half of integral(±p-2eta s/c), by the identities proved in the inverse note. This explains the original two mean Casimirs from the marked spectral data. At coincident-multiplier mean-zero leaves, use the original mean Casimirs and the restricted inverse chart rather than assuming differentiability of a simple-eigenvalue branch off the spectral constraint surface.

## 7. Scope reached

On this general two-site periodic field chart we now have: the physical Hamiltonian, its exact pushed Poisson tensor, a compatible three-tensor structure, an all-order Lenard chain, physical-time inclusion, mutually commuting conserved quantities, and the earlier arbitrarily long independent subsequences. These are substantive infinite-dimensional Hamiltonian-integrability structures, rather than a finite-soliton parameter Hamiltonization.

Full global periodic inverse spectral/action-angle completeness remains a different target. The known high-frequency Cauchy obstruction and the mixed-time analytic solution construction remain in force. General M>=3 still has the previously constructed trace/involution hierarchy, but the explicit three-tensor/Miura pencil above is proved here for M=2 only.
