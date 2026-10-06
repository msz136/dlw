# General periodic field: displayed conserved family and independence verdict

2026-10-06. Consolidated proof draft for fixed finite M>=2, x periodic, Pi w=c!=0 and Pi(Uw)=gamma, with the previously fixed Hamiltonian closure.

Let G=hMc/4,B=gamma/(2c), calM=T_(M-1)...T0, Tj=(D-Uj/2+h wj/8)^-1(D-Uj/2-h wj/8), and L=-G(calM-I)^-1+(B-G/2)I.
Define C_n=(1/n) integral res L^n.

Equivalently for L=D-q(DI-V)^-1r, let z1=r,
z_(n+1)=V z_n-D z_n-sum_(i+j=n)z_i(q z_j), rho_n=-q z_n.
Then C_n=integral rho_n modulo total derivatives. First three:
C1=-integral qr,
C2=integral(q r_x-qVr),
C3=integral[(qr)²-qV²r+qV_xr+2qVr_x-qr_xx].

Conservation follows from L_t=[-(L²)_+,L] and the periodic trace identity. Involution follows from the factor-field Adler calculation and gauge-invariant transfer to the physical reduced bracket: the gradients with respect to calM commute with calM, so the bracket is the trace of a commutator. Normalizing constants G,B remain fixed during the off-leaf extension used to compute these gradients.

Independent odd subsequence: on w_j=c, U0=2B+2f,U1=2B-2f,others2B, the quadratic top derivative part of C_(2k+1) is (2/M)(-1)^(k+1) integral(D^k f)². For f=epsilon sum_(i=1)^N a_i cos(k_i x), with distinct positive frequencies and a_i nonzero, the amplitude Jacobian of C1,C3,...,C_(2N-1) has a nonzero leading Vandermonde factor in k_i². Arbitrarily large finite blocks are therefore independent. Because fixed-order functionals are polynomial in the reduced fields and their derivatives, the nonvanishing of a witness determinant gives an open dense condition on the affine smooth field space (and on the zero-component-mean Casimir leaf containing the witnesses). The countable intersection gives simultaneous finite-block independence in the usual residual/generic sense, not independence at every field.

## Additional independent momentum and actual Hamiltonian

Let p=P0U,s=w-c. Define Pmom=h sum integral p_j s_j. It generates negative x translation and commutes with every C_n. On the witness s=0, its differential vanishes on all p-only Fourier-amplitude directions, whereas the Jacobian of the N odd charges on those N directions is invertible. Therefore dPmom cannot be in their span: choose delta s0=f,delta s1=-f,others0, giving dPmom=4h integral f² !=0. This variation has zero component x means when f does and stays within the reduced coordinate space; the reconstruction of U's common mean automatically preserves Pi(Uw)=gamma.

Thus Pmom,C1,C3,...,C_(2N-1) are independent at the same witness for every N. The physical Hamiltonian obeys
K=-8G C1+(gamma/c)Pmom+constant.
Since G!=0, replace C1 by K. The concrete family

K, Pmom, C3, C5, ...

has arbitrary finite prefixes generically independent, all members are conserved, and all pairwise physical Poisson brackets vanish. This includes the actual time evolution generator in the independent family and not merely an unrelated Hamiltonian.

## Verdict and scope

This supplies a positive infinite-dimensional Hamiltonian-integrability statement in the independent commuting-conservation-hierarchy sense for general periodic physical fields under the stated closure. These are not finite-soliton parameter charges. The draft does not supply a complete global action-angle/inverse spectral theorem; that is a stronger open problem rather than evidence of nonintegrability. High-frequency Cauchy instability likewise does not disprove the conserved hierarchy.

