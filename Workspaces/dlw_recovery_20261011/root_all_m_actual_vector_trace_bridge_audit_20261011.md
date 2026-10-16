# Root audit: exact all-M original trace/vector-AKNS bridge

Read the main proof `all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md` §§1–7, including its low-domain §5.1, against the earlier audited original rational gauge representation and physical graph inverse. The independent audit supplies a second derivation. No symbolic check or numerical computation was rerun.

## Normalization and moving frame

The actual trace-normalized transformed connection is
\[
\bar A_\lambda=\begin{pmatrix}\lambda&a\\b&H\end{pmatrix}
 -(\lambda+\operatorname{tr}H)I_M/M
 =\lambda J_*+Q.
\]
With \(\bar E=(\det G)^{-1/M}T_z\operatorname{diag}(1,G)\), its determinant is state independent. The actual normalized adjoint \(\bar W=\bar Y\bar N^r\bar Y^{-1}\) is \(e^{-rL(\mu+\operatorname{tr}H)/M}\) times the untraced vector adjoint. This scalar must be included in its offdiagonal blocks \(e,f\).

The original generator has pole part \(-\omega_\mu W^0/(\lambda-\mu)\), \(\omega_\mu=(S^2-\mu^2)/(16S)\). Its transformed generator is
\[
\bar g=\bar E^{-1}g\bar E-\bar E^{-1}\delta\bar E
       =-\omega_\mu\bar W^0/(\lambda-\mu)+k(x).
\]
Thus the source-dependent frame derivative is retained. The actual adjoint equation gives the exact pole-free contribution \(\omega_\mu[J_*,\bar W]\), namely \(\omega_\mu(e,-f,0)\), the auxiliary canonical normalized trace field.

## The residual frame is genuinely finite and constant

The fixed leading \(\lambda J_*\) forces \([J_*,k]=0\), so \(k=\operatorname{diag}(t,K)\). The top diagonal equation \(-\delta\operatorname{tr}H/M=t'\) and periodicity force \(\delta\operatorname{tr}H=0\), \(t'=0\). Since \(H\) and \(\delta H\) are constant, \(\delta H=K'-[H,K]\). Nonzero Fourier modes vanish under the proved nonalias condition \(ik_n-\operatorname{ad}H\) invertible. Hence \(K,t\) are constant. Setting \(X=tI-K\) yields
\[
\delta a=\omega_\mu e+aX,\quad
\delta b=-\omega_\mu f-Xb,\quad
\delta H=[H,X].
\]
The exact correction is the constant \(GL_{M-1}\) frame direction. Actual trace fields therefore preserve all slow-holonomy eigenvalues. No monodromy simplicity or cyclicity is needed for this field identity.

The audited physical graph/frame transversality makes the correction unique and permits a local finite quotient. The remaining \(2(M-1)\) physical constraints remain there. This does not identify the entire original Poisson tensor with the auxiliary tensor on arbitrary ambient functions.

## Balanced-low identification has no regularity circle

Let \(\mathcal C=0\) be the full finite physical coefficient graph. A full-rank \((M-1)^2\) minor of \(D\mathcal C\mathcal V_X\) determines the finite correction analytically for each low actual adjoint. At \(L^2\) coefficients the actual fundamental matrix and adjoint are \(H^1\), by the Volterra equation and its differential equation, so all these operations are genuinely low-domain analytic.

On smooth physical states this constructed field equals the exact transformed original field. The full unselected graph constraints then vanish by continuity and density; solving the minor has not discarded the remaining constraints. The established state inverse pulls it back to an analytic \(L^2_q\times H^1_d\) field.

Independently the original affine connection's Duhamel gradients are \(H^1\), and applying the original differential Poisson tensor gives an analytic \(L^2\times L^2\) field. The free-coordinate change uses only the skew matrix on the first \(M-1\) components and preserves the offdiagonal tensor. Both fields agree densely and continuously in this larger space. Therefore the actual original second component is indeed \(H^1\); this is a consequence of the constructed field, not an assumption in differentiating a rough moving frame. Banach Picard gives an actual local flow.

**PASS:** the all-M actual normalized trace bridge modulo constant frame, full finite physical constraints and balanced-low original Hamilton flow are established on the audited small nonalias state neighborhood. Current \(B\), external \(\Gamma(t)\), nonzero \(c\) and actual original endpoint frame remain present. It is a state/field bridge, not an invariant action/divisor inverse or general-M Liouville theorem; infinite-spectrum Hamilton completeness remains open.
