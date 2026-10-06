# Exact all-period physical Poisson coordinates for the matrix Lax representation

2026-10-06. Constructive proof draft. This resolves the physical Poisson matching at the matrix/free-field level for every finite M>=2. A distinct three-Hamiltonian pencil in reduced scalar coefficients remains established only for M=2.

## 1. Explicit independent coordinates

Continue the preceding matrix Lax note, with m=M-1, S=sum d_j=hMc/8!=0, B=gamma/(2c), b_j=U_j/2 and d_j=h w_j/8. The first-row off-diagonal spectral fields are
q_j=b_j-b_m-d_j-2 sum_(k=j+1)^m d_k+d_m,
for j=0,...,m-1.
Take q_0,...,q_(m-1), d_0,...,d_(m-1) as the 2m independent field coordinates. All are functions of x. The final d and all b are recovered by

d_m=S-sum_(j<m)d_j,
b_m=B-sum_(j<m)d_j-(sum_(j<m)d_j q_j)/S,
b_j=b_m+q_j+d_j+2sum_(k=j+1)^(m-1)d_k+d_m.

Direct substitution recovers every q_j and sum b_j d_j=BS. Only the fixed nonzero S is divided by. Thus these coordinates globally parameterize the chosen mean-closed field branch; no individual W_j-4 or d_j needs to be nonzero. Recover physical U_j=2b_j,w_j=8d_j/h and then u,v by the original variable transformation.

Although U's common mean is nonlinear in these variables, the change from p=P0U,s=w-c to q,d_first is affine and invertible, since the common mean of b cancels from each q_j.

## 2. Constant canonical-pair derivative bracket

Use the same h-weighted pairing for source and target gradients. The source tensor is Jred=-[[0,P0 D],[P0 D,0]]. Let Z columns be e_j-e_m, E select the first m components, and define Kd_(j,k)=-delta_jk-2 1_(k>j)+delta_km. The Frechet matrix is constant:
F_*=[[Z^T/2, h Kd/8],[0,h E/8]].
Since Kd Z is skew, Z^T P0=Z^T, and Z^T E^T=I_m,

F_* Jred F_*^T=-(h/16)[[0,I_m D],[I_m D,0]].

Equivalently, if all functional derivatives use the ordinary unweighted integral, the pointwise bracket is
{q_i(x),q_j(y)}=0,
{d_i(x),d_j(y)}=0,
{q_i(x),d_j(y)}=-(1/16)delta_ij partial_x delta(x-y).

The h-weighted and unweighted versions are the same bracket with different gradient normalizations. The unweighted original p,s kernel contains 1/h. Overall normalization should not be mixed with the two-site convention using a Hamiltonian divided by 2h.

This is the exact original physical bracket in new coordinates. The transformed physical Hamiltonian is simply the old K expressed with the displayed inverse formulas. The all-period trace hierarchy and its previously proved involution therefore live on this genuine free-field Hamiltonian realization.

general_period_free_fields_certificate.py verifies the tensor identity and inverse reconstruction exactly for M=2,...,9. The three elementary matrix identities above supply the all-M proof.

## 3. Matrix V carries determined, not extra, degrees of freedom

In these coordinates the internal connection is
V_ij=delta_ij(b_i-d_i)-2d_i 1_(j<i)-(d_i/S)q_j,
for 0<=i,j<m.
The column r is likewise determined by
r_j=[d_j(b_j-d_j-2sum_(k<j)d_k-(B-S))-d_(j,x)]/S.
Thus q,r,V are constrained expressions in the 2m free fields, not an unconstrained array of additional state variables.

For M=3, in particular,
V_01=-d_0 q_1/S,
V_10=-d_1(2S+q_0)/S.
On the explicit open chart q_1(2S+q_0)!=0,
d_0=-S V_01/q_1,
d_1=-S V_10/(2S+q_0).
Therefore (q_0,q_1,V_01,V_10) are four independent coefficient coordinates and recover the full physical field. The two diagonal V entries and both r entries are then fixed formulas.

For any M>=3, one may select for each i an off-diagonal j!=i with q_j+2S 1_(j<i)!=0 and recover
d_i=-S V_ij/[q_j+2S 1_(j<i)].
Such charts exist near the uniform field: with all d_j=delta, b_j=B, q_j=-2delta(M-1-j), take j=i+1 except at i=m-1, where take j=0. All selected denominators are nonzero for delta!=0. Thus the matrix spectral representation retains all physical field information on these charts. This is a statement about its full matrix coefficients, not spectral eigenvalues alone.

## 4. The earlier holonomy issue is now located precisely

There is no need to gauge V to zero to define or match the physical Poisson bracket: keep its explicit expression in q,d and use the constant bracket above. Holonomy matters if one chooses to replace this periodic covariant representation by a standard vector-AKNS gauge in which V is removed. It is not an unaccounted independent field or an obstruction to the original bracket matching.

## 5. Progress and remaining stronger question

Established at the all-period matrix/free-field level: faithful physical state coordinates, original Hamiltonian and Poisson tensor, explicit matrix Lax representation, density recursion, and the existing commuting trace family with arbitrarily long independent subsequences.

The all-M analogue of the special M=2 compatible three-tensor formula in scalar Lax coefficient coordinates has not been proved by this constant-coordinate change. Nor does an infinite independent sequence, by itself, prove maximal spectral completeness. Those stronger structures require further work; the original-bracket matching itself is no longer missing at the matrix/free-field level.
