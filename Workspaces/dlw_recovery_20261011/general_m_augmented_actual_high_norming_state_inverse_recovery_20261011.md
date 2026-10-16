# General M: an actual real high-norming state inverse with finite coefficient supplements

2026-10-11. This note proves an augmented actual **state** inverse in one real balanced-low Banach neighborhood. Its high coordinates are the actual calibrated rank-two norming candidates of [the high-frequency Riesz lemma, §§6–8](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md). The finite low coordinates are explicitly nonspectral Fourier coefficient data. The result does not supply an invariant action inverse or canonical norming coordinates. No checks were run and no shared record was edited.

Inputs: the actual Riesz-compression and strong \(\ell^2\) norming functions of that lemma; the exact uniform high-channel inverse independently checked in [the finite-gap audit](general_m_actual_high_frequency_finite_gap_recovery_audit_20261011.md); and the actual [physical coefficient chart, §§4–9](all_m_physical_holonomy_state_inverse_20261011.md). Original component means, \(S=M\delta\ne0\), the nonalias background, current centered parameter and full matrix frame are retained.

## 1. Real source and data spaces

Let \(m=M-1\), and take the actual fixed-mean real source

\[
X_0^{\mathbb R}=(L^2_0(S^1;\mathbb R))^m_u
\times(H^1_0(S^1;\mathbb R))^m_v.
\tag{1}
\]

Its background is \(u=v=0\), with the already fixed uniform \(q_0,r_0,H_0\). The actual mean-normalized periodic coefficient frame has

\[
a=qG,\quad b=G^{-1}r,\quad G_x=VG-GH,\quad\langle G\rangle=I_m,
\]

and the actual source map satisfies

\[
\Pi(x)=(P_0a,P_0b),\qquad
D\Pi_0:X_0^{\mathbb R}\to (L^2_0)^{2m}_{\mathbb R}
\quad\text{bounded isomorphism},
\tag{2}
\]

\[
D\langle a\rangle_0=D\langle b\rangle_0=DH_0=0.
\tag{3}
\]

The target real Hilbert space, represented by independent positive complex Fourier modes, is

\[
\mathcal D_N^{\mathbb R}
=\mathbb C^{2m(N-1)}\oplus
\ell^2(\{(\ell,n):1\le\ell\le m,\ n\ge N\};\mathbb C^2),
\tag{4}
\]

with its underlying real structure. Each positive low frequency carries a row and column of \(m\) complex coordinates; each positive high frequency carries \(m\) pairs. There is no extra constraint among the positive channels. Negative channels reflect as \((\ell,n)\mapsto(M-\ell,-n)\), and are determined by the actual physical reality.

## 2. Actual calibrated high norming functions

Use the actual moving-grid Riesz block from the high-frequency lemma,

\[
B_{\ell n}(\zeta,x),\qquad
\lambda=K_n+h_\ell(H(x))+\zeta,
\quad K_n=2\pi in/L,
\]

and its actual half-sum of discriminant roots \(c_{\ell n}(x)\). The two roots are the actual repeated-multiplier positions in their isolated label window. All eigenvalues and eigenbases of the full constant matrix \(H(x)\), Riesz projections and matrix compressions here are part of the coefficient-frame/calibration definition; they are not replaced by only \(\operatorname{tr}H\) or by invariant class data.

Choose one source-independent, uniformly bounded background two-dimensional change \(C_{\ell n}=I+O(n^{-1})\), with uniformly bounded inverse, that identifies the Riesz-plane basis at the background collision with the actual generator eigenbasis used in its Born couplings. Let

\[
\chi_{\ell n}=\rho_{\ell n}/e^{Lp_\ell}=1+O(n^{-1}),
\]

where \(\rho_{\ell n}\) is the actual background common multiplier. Increase \(N\) once so that \(\chi\) and \(\chi^{-1}\) are uniformly bounded. Define

\[
\begin{split}
\nu^+_{\ell n}(x)&=\chi_{\ell n}^{-1}
\bigl(C_{\ell n}^{-1}B_{\ell n}(c_{\ell n}(x),x)C_{\ell n}\bigr)_{12},\\
\nu^-_{\ell n}(x)&=\chi_{\ell n}^{-1}
\bigl(C_{\ell n}^{-1}B_{\ell n}(c_{\ell n}(x),x)C_{\ell n}\bigr)_{21}.
\end{split}
\tag{5}
\]

These are actual full-frame norming functions. They are real analytic into the corresponding high \(\ell^2\) space on the same physical low ball. Indeed the original offdiagonal functions are strong \(\ell^2\) analytic; the uniformly bounded background basis change adds only \(O(n^{-1})(e^{Lc_{\ell n}}-1)\) template terms, also strong \(\ell^2\) analytic. The uniformly bounded scalar factors preserve that conclusion. None of these operations divides by the actual gap.

At the uniform state the actual two-dimensional collision is geometrically double, and the compressed monodromy at its exact root is scalar. Therefore

\[
\nu^+_{\ell n}(0)=\nu^-_{\ell n}(0)=0.
\tag{6}
\]

## 3. The complete first variation, including the source center

In the exact generator eigenbasis at the background collision, the projected spectral-parameter derivative of the monodromy is

\[
\rho_{\ell n}L\operatorname{diag}(y_f',y_\ell').
\tag{7}
\]

One can differentiate the actual background eigen-decomposition; all basis-derivative terms are commutators with the scalar collision block and hence vanish. The same reasoning removes derivatives of the Riesz intertwiner and source-dependent coefficient frame from the first-order collision compression.

For a physical source tangent, (3) gives \(\langle\dot A\rangle=0\), so the two diagonal Born entries at the exact collision are zero. In a fixed absolute coordinate \(\xi=\lambda-\lambda_{\ell n}\), the first-order discriminant has the form \(2F(\xi)(\dot B_{11}-\dot B_{22})\), where \(F\) has a simple zero and the diagonal difference vanishes at \(\xi=0\). Its ratio to the background discriminant \(F^2\) has no pole there. The root-moment formula therefore gives zero first variation of the absolute root center. Also \(Dh_\ell(H)_0=0\) by \(DH_0=0\). Thus

\[
Dc_{\ell n}(0)=0.
\tag{8}
\]

There is accordingly no omitted source-center term in differentiating (5). More generally, the offdiagonal entries of (7) are already zero, so such a center term would not contribute after this precise background calibration. The actual Duhamel offdiagonal Born entries are \(\rho_{\ell n}L\Gamma^\pm_{\ell n}\); division by the moving-template background factor and then by \(\chi\) gives exactly

\[
\boxed{D\nu^\pm_{\ell n}(0)[f]=L\Gamma^\pm_{\ell n}(f).}
\tag{9}
\]

This is a first variation of the actual evaluated monodromy block, not a formal Fourier ansatz.

## 4. One real Banach IFT gives the augmented actual state inverse

Using \(\widehat a_n=L^{-1}\int a(x)e^{-2\pi inx/L}dx\) and the same convention for \(b\), define the forward state data

\[
\Psi_N(x)=
\left(
(\widehat a_n,\widehat b_n)_{1\le n<N},
(\nu^+_{\ell n},\overline{\nu^-_{\ell n}})_{1\le\ell\le m,\ n\ge N}
\right).
\tag{10}
\]

The conjugation in the second component is on the actual real source domain and yields a real-analytic function. Its target is the underlying real Hilbert space (4); this is a real IFT, not a holomorphic IFT obtained by dropping independent negative modes of a complex source. Formula (6) and background zero nonconstant Fourier coefficients give \(\Psi_N(0)=0\).

Let \(\mathcal U\) be the bounded real Fourier isomorphism from the target of (2) to its positive-mode representation. For each positive high frequency the exact complex-linear map

\[
T_n:(A_n,B_n)\mapsto
(\Gamma^+_{\ell n},\overline{\Gamma^-_{\ell n}})_{\ell=1}^m
\]

is uniformly invertible, by the independently checked finite-gap lemma. Equations (2), (9) show

\[
\boxed{D\Psi_N(0)=
\operatorname{diag}\bigl(I_{\rm low},(LT_n)_{n\ge N}\bigr)
\mathcal U D\Pi_0.}
\tag{11}
\]

Both factors and their inverses are bounded on their real Hilbert spaces. In particular the infinite high-block inverse is the direct sum of the uniformly bounded \(L^{-1}T_n^{-1}\), and the finite low part supplies precisely the modes not covered by that high theorem. Thus \(D\Psi_N(0)\) is an actual bounded real Banach isomorphism.

The real-analytic inverse function theorem now gives neighborhoods \(U_N\subset X_0^{\mathbb R}\), \(V_N\subset\mathcal D_N^{\mathbb R}\), of the uniform state and zero data, such that

\[
\boxed{\Psi_N:U_N\longrightarrow V_N
\text{ is a real-analytic Banach diffeomorphism}.}
\tag{12}
\]

All high modes use the same actual physical source neighborhood. This proves a nonlinear augmented high-norming state inverse. It does not just prove independence of finitely many coordinates. Every data point in the resulting target neighborhood reconstructs a unique actual physical state on the fixed component-mean leaf. Full \(a,b,H\), original \(q,d\), and the actual source frame are then computed from that state by the already proved physical chart.

## 5. Exact status of the supplemental and calibration data

The finite positive low modes in (10) are Fourier coefficients of the actual vector potentials. They are **not** invariant spectral actions, Floquet classes or gap data. They are supplemental coefficient metadata. The theorem is deliberately augmented by them.

Likewise every high component in (5) is defined using the complete state-adapted coefficient matrix \(H\), its finite-dimensional eigenbasis, the actual full framed monodromy and the fixed background collision calibration. If these quantities are included as numerical metadata with the supplied norming values, they are constrained by the reconstructed state; they are not new free target coordinates appended to (4). The physical finite graph remains enforced by reconstruction on \(U_N\).

The forward map (10) is not determined by characteristic coefficients alone. A similarity changes norming entries while leaving the gap roots unchanged. The theorem therefore does not remove the distinction between full framed and class-only spectral data, or replace the recovered endpoint matrices by arbitrary constant gauges.

## 6. The initial-value coefficient-frame variant and original chi data

There is also a genuine variant using \(G^f(0)=I_m\), which fits the original endpoint calibration directly. Put \(Q=G(0)\), with its actual dependence on the physical state, and

\[
a^f=aQ^{-1},\qquad b^f=Qb,\qquad H^f=QHQ^{-1}.
\]

The actual block monodromies satisfy

\[
M_A^f=D_QM_AD_Q^{-1},\qquad D_Q=\operatorname{diag}(1,Q).
\tag{13}
\]

At the background \(Q=I\). Its source derivative contributes \([\dot D_Q,M_0]\), whose compression to the scalar collision block is zero. The full constant \(H^f\) derivative is generally \([\dot Q,H_0]\), **not** zero, but its eigenvalue derivatives vanish. Also

\[
D(P_0a^f,P_0b^f)_0=D\Pi_0,
\]

because the difference consists of spatial constants. In the actual coefficient connection, the source-frame difference \([\dot D_Q,A_0]\) is constant in space, and hence has zero nonzero Fourier coefficients; it does not change either \(\Gamma^\pm_{\ell n}\). Its collision compression has zero diagonal Born terms as well. Thus (8)–(11) hold unchanged for this frame when all norming definitions and finite low data consistently use \(a^f,b^f,H^f\). The same real IFT gives an actual initial-value-frame augmented inverse, on its own sufficiently small neighborhood; both frames can be considered on a common smaller source ball.

The actual original fixed-\(\chi\) monodromy determines its endpoint \(T_d(0)\) by the already proved positive-parameter limit. Conjugation by this recovered endpoint gives the initial-value-frame normalized block monodromy. The full \(H^f\) can then be recovered directly from actual imaginary samples, without invoking the old small-potential ambient state inverse. Let

\[
\widehat N^f(\lambda)=T_d(0)^{-1}N_\chi(\lambda)T_d(0),\qquad
\alpha=\exp[-L\operatorname{tr}H^f/M].
\]

The exact normalization and the FULL \(\ell^2\) remainder of the Riesz lemma §3 give

\[
e^{K_nL/M}\widehat N^f(K_n)
=\alpha M_{A^f}(K_n)
=\alpha\operatorname{diag}(1,e^{LH^f})+\mathcal E_n,
\qquad(\mathcal E_n)\in\ell^2(\operatorname{Mat}_M).
\tag{14}
\]

In particular \(\mathcal E_n\to0\) as \(|n|\to\infty\). The actual limit's top-left entry recovers the nonzero scalar \(\alpha\), and its slow block divided by \(\alpha\) recovers the complete matrix \(e^{LH^f}\). The nonalias condition makes the derivative of \(H\mapsto e^{LH}\) invertible at \(H_0\); the finite-dimensional analytic IFT recovers the unique nearby full \(H^f\). This is matrix recovery, not just slow eigenvalues or trace.

For completeness, the full matrix derivative is \(K\mapsto e^{LH_0}\int_0^Le^{-tH_0}Ke^{tH_0}dt\). On a slow eigenmatrix with eigenvalue difference \(p_i-p_j\), the integral factor is \((1-e^{-L(p_i-p_j)})/(p_i-p_j)\), with value \(L\) when the difference is zero. Every factor is nonzero by (NR). Thus the derivative is an isomorphism on the complete matrix space, including all diagonal and offdiagonal entries. The exact scalar factor now reconstructs the untraced matrix:

\[
M_{A^f}(\lambda)=
e^{\lambda L/M+L\operatorname{tr}H^f/M}\widehat N^f(\lambda),
\tag{15}
\]

which is the actual full matrix used in the Riesz compression and its norming functions. Equations (14)–(15) require the fixed-\(\chi\) frame data and current centered parameter labels, but require no additional near-zero vector-potential radius. Thus the initial-value-frame variant is directly compatible with actual original full-frame data at any fixed uniform nonalias background allowed by the coefficient chart. No natural Banach norm on the whole original entire-function monodromy space is asserted: the open data IFT is (12), for the extracted augmented \(\ell^2\) coordinates and the declared finite low coefficient supplements.

For \(B=\Gamma/(2c)\), preserve the original labels and use \(\lambda=\lambda_{\rm original}-B\) on each current spatial section. The scalar normalized monodromy factor and endpoint frame are those already proved in the actual calibration theorem. This static state inverse adds no \(B_t=0\), \(\Gamma_t=0\) or new equation for the external labels.

## 7. What the theorem does not yet provide

Equation (12) closes the **augmented** state-inverse question for these actual multichannel high norming functions. It does not prove an inverse from the high functions alone, since finite low coefficient data remain. It does not give an inverse from class/gap/action data, a canonical Poisson identity, squared-eigenfunction Hamiltonian completeness, or ordinary invariant Liouville fibers. Nor does it prove a weighted \(h^s\) inverse or all-hierarchy strong-domain membership; nonlinear endpoint tails and the high Sobolev norming estimates remain separate questions. Those conclusions cannot be inferred merely from the \(L^2/\ell^2\) Banach IFT.
