# An all-period rank-one matrix spectral representation

2026-10-06. Constructive proof draft. This extends the explicit two-site resolvent form to every finite lattice period M>=2. It does not yet prove an all-M version of the two-site three-tensor pencil.

## 1. Data and exact transfer problem

Set b_j=U_j/2,d_j=h w_j/8. Let S=sum_j d_j=hMc/8!=0 and B=(sum_j b_j d_j)/S=gamma/(2c), both constants by the chosen mean closure. Define nu=B-S. The scalar transfer equations are
(D-b_j+d_j)psi_(j+1)=(D-b_j-d_j)psi_j,
with psi_M=mu psi_0.
They are equivalent to the ordered monodromy eigenvalue equation calM psi0=mu psi0. Introduce lambda=nu-2S/(mu-1). This is the same spectral change used by normalized L=-2S(calM-I)^-1+nu I.

Let chi_j=psi_(j+1)-psi_j and phi=sum_j chi_j=(mu-1)psi0. Let H be the strict lower triangular matrix H_jk=1 for k<j, zero otherwise, and let d denote the column of d_j, 1 the all-ones column. Summing differences gives
psi=H chi + (1/(mu-1))1 1^T chi.
The transfer equation becomes
chi_x=(lambda P+C)chi,
P=d 1^T/S,
C=diag(b-d)-2 diag(d)H-(nu/S)d 1^T.
Since 1^T d=S, P²=P and rank P=1.

## 2. A global-in-the-chart spectral splitting without individual d_j divisions

Let Z have columns e_j-e_(M-1), j=0,...,M-2. Let E select the first M-1 components, and set
T=[d/S, Z],
K=E-(d_first/S)1^T,
T^-1=[1^T;K].
T is invertible whenever S!=0, even when one or many d_j vanish. Its determinant is a nonzero constant up to the chosen basis orientation.

The mean constraints give
1^T C d/S = (sum b_j d_j)/S-S-nu=0.
Also 1^T d_x=0. After chi=T(phi,xi)^T,

(phi,xi)_x = [[lambda,q],[r,V]] (phi,xi),
q=1^T C Z,
r=K(C d-d_x)/S,
V=K C Z.

The scalar spectral mode has no extra zero-order diagonal term. q is a 1 by (M-1) row, r an (M-1) by 1 column, V an (M-1)-square matrix. All their entries are explicit local differential expressions in physical fields, divided only by fixed S in this construction.

Eliminating xi yields the exact scalar resolvent representation

L=D-q(D I_(M-1)-V)^-1 r.

At M=2 the formulas reduce identically to q=2f,r=g/2,V=C_old, reproducing the previous scalar rank-one form. general_period_matrix_certificate.py verifies all matrix identities exactly for M=2,...,6 and this precise M=2 match. The sums and change-of-basis argument above supply the all-M proof.

## 3. A direct density recursion for every finite period

Let z=xi/phi. The matrix spectral system implies
z_x=r+V z-lambda z-z(q z).
There is a unique small formal branch z=sum_(n>=1) z_n lambda^-n, with
z1=r,
z_(n+1)=V z_n-D z_n-sum_(i+j=n; i,j>=1) z_i(q z_j).
The scalar logarithmic derivative is phi_x/phi=lambda+qz, so define rho_n=-q z_n. These coefficients agree, modulo total x derivatives and the standard trace normalization, with the existing scalar trace densities Tr L^n/n. In particular rho1=-qr=res L.

The physical Lax time equation has scalar wave evolution phi_t=-phi_xx+2(qr)phi, up to a spatially constant scalar normalization. For R=lambda-phi_x/phi=sum rho_n lambda^-n, logarithmic differentiation gives
R_t=D[-R_x-2lambda R+R²-2qr],
since the lambda^0 term -2rho1-2qr cancels. Therefore
(rho_n)_t+D[rho_(n,x)+2rho_(n+1)-sum_(i+j=n)rho_i rho_j]=0.
This supplies a finite-dimensional vector recursion at each order for arbitrary M; it avoids expanding an entire product of inverse differential factors by hand. It is still a formal generating series, with genuine finite differential expressions at each fixed order.

## 4. Relation to multicomponent constrained KP and a periodic caveat

Locally solve G_x=V G. Then
L=D-(qG)D^-1(G^-1 r),
a rank-(M-1) constrained-KP form. On a circle G generally has nontrivial holonomy, so qG and G^-1r need not be periodic individually. The displayed covariant representation with V kept is periodic and retains that information. No standard periodic vector-AKNS theorem can be imported by simply discarding this holonomy.

Primary relevant references: Huang--Shaw--Tu, Matrix Formulation of Hamiltonian Structures of Constrained KP Hierarchy, https://arxiv.org/abs/solv-int/9801019 ; Aratyn et al., Hamiltonian Structures of the Multi-Boson KP Hierarchies, Abelianization and Lattice Formulation, https://arxiv.org/abs/hep-th/9401058 . They identify a relevant Hamiltonian framework; this note establishes the DLW matrix realization directly.

## 5. Poisson matching status

The original reduced field bracket is retained and the previously proved all-M trace involution remains valid. The new matrix coefficients inherit a Poisson bracket by the Frechet pushforward F_* Jred F_*^*. However an explicit all-M identification of that bracket with the same kind of three-tensor polynomial proved at M=2 has NOT been completed here. The internal matrix connection, its holonomy, and the constraints on the q,r,V image must be included in such a matching.

Thus the result of this extension is a concrete all-M Lax realization and density recursion, with a verified M=2 reduction, not an unsupported assertion that the two-site three-tensor formula applies entrywise for every period.
