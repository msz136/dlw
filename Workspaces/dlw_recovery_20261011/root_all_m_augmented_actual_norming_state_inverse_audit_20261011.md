# Root audit: actual multichannel high norming, with finite low coefficient supplements

2026-10-11. Read the full final recovery proof `general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md`, §§1–7, against the independently checked actual Riesz/gap lemma and the uniform physical Fourier coupling inverse. This is a hand audit; no existing machine checks were rerun.

## Exact derivative and actual data topology

The real physical source is \(X_0=(L^2_0)^m\times(H^1_0)^m\), \(m=M-1\). The mean-normalized coefficient chart has \(D\Pi_0\) a real Banach isomorphism to \((L^2_0)^{2m}\), and its coefficient mean and full \(H\) derivatives vanish. The actual rank-two block is scalar at its exact background collision. Differentiating its source frame or Riesz intertwiner therefore adds no compressed commutator. In the background generator eigenbasis, the spectral-parameter derivative of that block is diagonal.

The diagonal Duhamel entries vanish because the source coefficient variation has zero mean. In the discriminant root-moment calculation, the first variation divided by the background discriminant then has no pole. Both the absolute center derivative and the mean-normalized slow eigenvalue derivative vanish. Thus evaluating the offdiagonal block at its actual source center introduces no omitted term. The exact derivative of the two calibrated norming coordinates is

\[
D\nu^\pm_{\ell n}(0)=L\Gamma^\pm_{\ell n}.
\]

The scalar calibration \(\chi_{\ell n}=\rho_{\mathrm{actual}}/\rho_{\mathrm{template}}\) is essential. The background basis changes and their inverses are uniformly bounded and differ from identity by \(O(1/n)\); the additional template terms remain strongly \(\ell^2\)-analytic. Evaluation at the center uses the previously proved function-valued \(\ell^2(A_r)\) map, rather than an unproved analytic map into a sequence of sup norms.

Use independent positive Fourier modes on the real source. The high outputs are \((\nu^+,\overline{\nu^-})\); negative channels are fixed by the actual reflected real structure. The exact high-channel map \(T_n\) is complex linear in these positive source coefficients, with uniform bounded inverse. Supplement the finitely many frequencies \(1\le n<N\) by the actual nonconstant coefficient modes \((\widehat a_n,\widehat b_n)\). The resulting real derivative is

\[
D\Psi_N(0)=\operatorname{diag}\bigl(I_{\mathrm{low}},(LT_n)_{n\ge N}\bigr)\mathcal U D\Pi_0,
\]

where \(\mathcal U\) is the real Fourier isomorphism. This operator and its inverse are bounded on the stated real Hilbert spaces. The real analytic Banach IFT gives an ordinary nonlinear local state diffeomorphism on one source neighborhood. It is not merely a finite-coordinate rank statement or a complex IFT that has dropped negative modes.

## Initial-value frame and genuine original-data calibration

The mean-normalized gauge has generally unknown \(G(0)\). The proof correctly removes it by using \(G^f(0)=I\): with \(Q=G(0)\),

\[
a^f=aQ^{-1},\quad b^f=Qb,\quad H^f=QHQ^{-1},\quad
M_A^f=D_QM_AD_Q^{-1}.
\]

Here \(\dot H^f=[\dot Q,H_0]\) need not vanish. Its eigenvalue derivatives do vanish. The new source connection variation differs by a spatially constant commutator; its nonzero Fourier couplings and projected low coefficient derivative are unchanged. At the scalar collision its compressed monodromy commutator vanishes. Hence the complete real IFT derivative remains the same, without falsely setting \(DH^f=0\).

The original positive-parameter endpoint limit recovers \(T_d(0)\). In that recovered based frame, the full imaginary-sample remainder theorem gives

\[
e^{K_nL/M}\widehat N^f(K_n)
=\alpha\operatorname{diag}(1,e^{LH^f})+\mathcal E_n,
\quad \alpha=e^{-L\operatorname{tr}H^f/M},\quad \mathcal E\in\ell^2.
\]

Thus the top-left limit gives the nonzero scalar \(\alpha\), and the slow block divided by it gives the complete matrix exponential. At the nonalias background, the derivative of the matrix exponential is invertible: its offdiagonal multipliers are the nonzero divided differences of \(e^{Lp_i}\), and its diagonal multipliers are nonzero. The finite-dimensional analytic IFT recovers the full nearby \(H^f\), not just its eigenvalues or trace. The exact scalar factor then recovers \(M_A^f(\lambda)\). This calibration needs no old near-zero ambient vector inverse and is valid at each fixed nonalias uniform background allowed by the physical coefficient chart.

**PASS:** an actual real multichannel high-norming state inverse exists after the declared finite low coefficient supplements. The initial-value-frame version is compatible with original full framed monodromy and its current centered parameter. The low supplements are nonspectral metadata; full-frame norming is not a characteristic-class function. No invariant action inverse, canonical Poisson formula, weighted all-order inverse, strong-domain membership, or all-M Hamiltonian completeness follows from this result. The original \(c\), external \(\Gamma(t)\), and current \(B=\Gamma/(2c)\) are retained.
