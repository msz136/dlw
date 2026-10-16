# All M: the actual original trace field is a weighted vector-AKNS field modulo constant frame

2026-10-11. This is an exact field bridge on the actual fixed-component-mean physical image near the nonalias uniform background. It derives the vector statement from the already proved all-M rational gauge generator, rather than extrapolating the scalar M=2 identity. No checks were run; no shared log or another author's proof was changed.

Dependencies: [actual all-M rational physical Hamiltonian gauge bridge, §§1–4](all_m_rational_physical_gauge_hamilton_bridge_20261011.md), [periodic physical holonomy/state chart, §§1–3, 6–8](all_m_physical_holonomy_state_inverse_20261011.md), and [actual normalized endpoint calibration](all_m_actual_framed_endpoint_recovery_20261011.md). The finite constant-frame correction below is determined in the actual state frame; it is not discarded from the original framed monodromy data.

## 1. Actual objects and trace normalization

Fix \(M\ge2\), \(m=M-1\), \(L>0\), nonzero \(S=M\delta\), and the original component means. Work at one current spatially constant \(B\) parameter section, with

\[
\lambda=\lambda_{\rm original}-B.
\]

Let \(L_\lambda\) be the actual original traceless connection in the all-M rational bridge. The established actual periodic source frame is

\[
E=T_z\operatorname{diag}(1,G),\qquad
\bar E=(\det G)^{-1/M}E,
\]

using the near-identity branch of \(\log\det G\). Since \(\det T_z\) is a state-independent constant, \(\det\bar E\) is that same constant. The exact transformed connection is

\[
\bar A_\lambda=\bar E^{-1}L_\lambda\bar E-\bar E^{-1}\bar E_x
=\begin{pmatrix}\lambda&a\\b&H\end{pmatrix}
-\frac{\lambda+\operatorname{tr}H}{M}I_M
=\lambda J_*+Q,
\quad J_*=E_{00}-I_M/M.
\tag{1}
\]

Here \(H\) is a complete constant \(m\times m\) matrix, not a scalar, and \(a,b\) are actual periodic vector potentials. The internal nonalias condition is

\[
\operatorname{spec}(\operatorname{ad}H)
\cap\frac{2\pi i}{L}(\mathbb Z\setminus\{0\})=\varnothing.
\tag{2}
\]

It holds on the established sufficiently small uniform physical neighborhood. Only this coefficient-state chart and its constant-frame transversality are required; no invariant action/norming inverse is assumed.

For each fixed \(\mu\) and \(r\ge1\), the original actual Hamiltonian is

\[
F_{\mu,r}=r^{-1}\operatorname{tr}N_\chi(\mu)^r.
\tag{3}
\]

Let \(\bar Y_\mu\) be the actual initial-value fundamental matrix of (1), \(\bar N_\mu=\bar Y_\mu(L)\), and

\[
\bar W_{\mu,r}=\bar Y_\mu\bar N_\mu^r\bar Y_\mu^{-1}
=\begin{pmatrix}h&e\\f&K_W\end{pmatrix}.
\tag{4}
\]

Periodicity of \(\bar E\) gives the exact calibrated relation

\[
N_\chi(\mu)=\bar E(0)\bar N_\mu\bar E(0)^{-1},\qquad
\bar W_{\mu,r}=\bar E^{-1}W_{\mu,r}\bar E.
\tag{5}
\]

Thus \(F_{\mu,r}\) is the trace function of this normalized vector connection. Let \(N_A\) be the actual monodromy of the untraced block system \(A_\lambda=\left(\begin{smallmatrix}\lambda&a\\b&H\end{smallmatrix}\right)\). Then, with

\[
c_\mu=(\mu+\operatorname{tr}H)/M,
\]

\[
\bar N_\mu=e^{-Lc_\mu}N_A(\mu),\qquad
\bar W_{\mu,r}=e^{-rLc_\mu}W^A_{\mu,r},\qquad
F_{\mu,r}=e^{-rLc_\mu}\,r^{-1}\operatorname{tr}N_A(\mu)^r.
\tag{6}
\]

The scalar factor in (6) is necessary. In particular the actual trace-gradient residue cannot be replaced by the residue of an unnormalized block monodromy without it.

## 2. The auxiliary canonical vector trace field

On the ambient vector-potential space use only the auxiliary canonical bracket

\[
Y_{\mathcal F}=(\nabla_b\mathcal F,-\nabla_a\mathcal F,0),
\tag{7}
\]

with ordinary complex bilinear spatial integral pairing and with every entry of \(H\) a Casimir of this auxiliary bracket. For the normalized trace \(\mathcal F_{\mu,r}\) in (3)–(6), actual Duhamel differentiation gives

\[
d_{a,b}\mathcal F_{\mu,r}
=\int_0^L(f\,\delta a+e\,\delta b)dx,
\qquad Y_{\mathcal F_{\mu,r}}=(e,-f,0).
\tag{8}
\]

The transpose/row-column pairing in (8) is contraction of the compatible blocks; no extra factor \(r\) remains because of the \(r^{-1}\) normalization in (3). Equivalently,

\[
\delta_{Y_{\mathcal F}}\bar A_\lambda
=[J_*,\bar W_{\mu,r}]
=\begin{pmatrix}0&e\\-f&0\end{pmatrix}.
\tag{9}
\]

Here \(H\) being an auxiliary Casimir is not a claim about the original physical tensor. Indeed \(\operatorname{tr}H=-\delta^{-1}\langle u\cdot v\rangle\) on the physical graph and is generally not a physical Casimir. The original physical \(H\)-variation is determined below.

## 3. Transform the actual physical gauge generator, including its moving frame

The already audited original field has the full-spectral actual gauge representation

\[
\delta_{X_{F_{\mu,r}}}L_\lambda=g_\lambda'-[L_\lambda,g_\lambda],
\qquad
g_\lambda=-\frac{\omega_\mu W_{\mu,r}^0}{\lambda-\mu}+g_\infty,
\qquad
\omega_\mu=\frac{S^2-\mu^2}{16S}.
\tag{10}
\]

Here \(g_\infty(x)\) is independent of \(\lambda\), and \(W^0=W-\operatorname{tr}W I_M/M\). Both terms are actual smooth periodic matrices at a smooth physical state. Transformation of a source-dependent connection requires the moving-frame term:

\[
\bar g_\lambda=
\bar E^{-1}g_\lambda\bar E-\bar E^{-1}\delta_{X_F}\bar E
=-\frac{\omega_\mu\bar W_{\mu,r}^0}{\lambda-\mu}+k(x).
\tag{11}
\]

The exact transformed identity is

\[
\delta_{X_F}\bar A_\lambda=
\bar g_\lambda'-[\bar A_\lambda,\bar g_\lambda].
\tag{12}
\]

The matrix \(k\) is independent of \(\lambda\), smooth and periodic. It is trace-free: \(g_\infty\) is trace-free and \(\operatorname{tr}(\bar E^{-1}\delta\bar E)=\delta\log\det\bar E=0\). Dropping \(-\bar E^{-1}\delta\bar E\) would give an incorrect framed field identity.

Since \(\bar W'=[\bar A_\mu,\bar W]\), the pole part has the exact pole-free variation

\[
\left(-\frac{\omega_\mu\bar W^0}{\lambda-\mu}\right)'
-\left[\bar A_\lambda,-\frac{\omega_\mu\bar W^0}{\lambda-\mu}\right]
=\omega_\mu[J_*,\bar W].
\tag{13}
\]

This is precisely \(\omega_\mu\) times (9). It uses \(\bar A_\lambda-\bar A_\mu=(\lambda-\mu)J_*\) and the actual adjoint equation, so it holds without simplicity or cyclicity of \(N_\mu\).

## 4. The remaining correction is a constant finite frame direction

Subtract (13) from (12). The exact remainder is

\[
\delta_{X_F}\bar A_\lambda-
\omega_\mu\delta_{Y_{\mathcal F}}\bar A_\lambda
=k'-[\bar A_\lambda,k].
\tag{14}
\]

The left side is independent of \(\lambda\), since the coefficient \(J_*\) in (1) is state-independent. The \(\lambda\) coefficient on the right forces \([J_*,k]=0\). Consequently

\[
k(x)=\operatorname{diag}(t(x),K(x)),\qquad t+\operatorname{tr}K=0.
\tag{15}
\]

The upper diagonal block of (14) is

\[
-\delta\operatorname{tr}H/M=t'.
\]

Its left side is spatially constant. Integrating over the period proves

\[
\delta\operatorname{tr}H=0,\qquad t'=0.
\tag{16}
\]

The slow diagonal block is then

\[
\delta H=K'-[H,K].
\tag{17}
\]

Both \(H\) and \(\delta H\) are spatially constant by construction of the actual periodic holonomy chart. At each nonzero spatial Fourier mode, (17) gives

\[
(ik_n-\operatorname{ad}H)K_n=0.
\]

The nonalias condition (2) implies \(K_n=0\) for every \(n\ne0\). Thus \(K\) and \(t\) are constant matrices/scalars. Put

\[
X=tI_m-K\in\operatorname{Mat}_m(\mathbb C).
\]

The complete block equations from (14) become

\[
\boxed{
\delta_{X_{F_{\mu,r}}}a=\omega_\mu e+aX,\qquad
\delta_{X_{F_{\mu,r}}}b=-\omega_\mu f-Xb,\qquad
\delta_{X_{F_{\mu,r}}}H=[H,X].
}
\tag{18}
\]

Indeed \(ta-aK=aX\), \(Kb-bt=-Xb\), and \(-[H,K]=[H,X]\). Conversely any \(X\) uniquely corresponds to the trace-free block constant \(k\): \(t=\operatorname{tr}X/M\), \(K=tI_m-X\). Hence the correction has exactly the constant \(GL_m\) frame form

\[
\mathcal V_X=(aX,-Xb,[H,X]),
\tag{19}
\]

the tangent of \((a,b,H)\mapsto(aQ,Q^{-1}b,Q^{-1}HQ)\). In particular the slow holonomy eigenvalues, not just its trace, are constant along every actual trace-power field in this neighborhood, since its actual \(H\)-variation is a commutator.

## 5. Precise quotient statement and the finite physical constraints

The constant-frame action is free near the uniform point: the established observability/controllability condition and simple \(H\) make \(\mathcal V_X=0\) imply \(X=0\). The physical finite graph is transverse to this \(m^2\)-dimensional orbit; the corresponding full-rank minor remains full rank on the common small neighborhood. A finite analytic slice therefore supplies a local quotient by this exact constant-frame group.

Let \(p\) denote its local quotient projection, and let \(\mathcal P\) be the actual physical coefficient map into triples. The normalized trace is frame invariant; its auxiliary vector field (8) is frame equivariant, so it descends through \(p\). Equation (18) proves

\[
\boxed{D(p\circ\mathcal P)X_{F_{\mu,r}}
=\omega_\mu\,Dp\,Y_{\mathcal F_{\mu,r}}.}
\tag{20}
\]

For \(\mu\ne\pm S\), division by \(\omega_\mu\) is valid in this tangent identity. This supplies the requested exact actual vector-AKNS trace bridge modulo finite frame for all \(M\). At \(\mu=\pm S\), the original trace powers are fixed by the component means and their physical fields vanish. Equation (18) is consistent with this because \(\omega_\mu=0\), and freeness forces the correction \(X=0\). Values at these parameters can be approached by the actual continuous trace family if a closed-span statement later requires them.

The quotient retains the other physical finite constraints. The physical graph has \(2m+m^2\) scalar constraints before the frame quotient; dividing by the \(m^2\) frame directions does not identify the entire ambient vector-potential quotient with the physical image. Equation (20) instead says that the descended trace field is tangent to the actual physical subimage there. On the physical graph the correction \(X\) is unique: the difference of two allowed corrections would be a constant-frame vector tangent to the physical graph, which the audited transversality excludes.

It follows that (20) is more than a bare pole-residue match: it keeps the moving source frame, trace normalization, actual holonomy, and finite graph constraints. It does not declare the physical Poisson tensor equal to the auxiliary canonical tensor on arbitrary functions. Only this full actual normalized trace family and its exact transformed fields have been identified.

### 5.1 An actual balanced-low extension by the finite graph minor

The exact smooth identity also gives an analytic balanced-low physical field without differentiating a rough moving frame in an unproved direction. Let the actual low coefficient graph be defined by

\[
\mathcal C(a,b,H)=
\bigl(\langle a\rangle-\alpha(P_0a,P_0b),
\langle b\rangle-\beta(P_0a,P_0b),
H-\mathcal H(P_0a,P_0b)\bigr)=0.
\tag{21}
\]

It is an analytic map from an ambient \(L^2\times L^2\times\operatorname{Mat}_m\) neighborhood to \(\mathbb C^{2m+m^2}\). Let \(\mathcal V_X\) be (19). Select the same \(m^2\) scalar-output minor \(P\) supplied by the physical constant-frame transversality, and define

\[
T_zX=P\,D\mathcal C_z[\mathcal V_X].
\]

At the uniform point \(T_z:\operatorname{Mat}_m\to\mathbb C^{m^2}\) is an isomorphism; it remains one on a common sufficiently small low neighborhood. For a fixed actual normalized trace define

\[
X(z,\mu,r)=-T_z^{-1}P\,D\mathcal C_z
\bigl[\omega_\mu Y_{\mathcal F_{\mu,r}}(z)\bigr],
\qquad
V(z)=\omega_\mu Y_{\mathcal F_{\mu,r}}(z)+\mathcal V_{X(z,\mu,r)}.
\tag{22}
\]

The actual fundamental matrix of the \(L^2\) connection (1), its inverse and its adjoint (4) are \(H^1\) and analytic in the low coefficients. This follows from the convergent actual Volterra solution in \(C^0\), followed by \(Y'=\bar A Y\in L^2\), and the analogous inverse equation. Hence (8) is an analytic ambient-low field, with uniform bounds for compact \(\mu\) sets and each fixed finite \(r\). Matrix inverse, the finite graph differential and the constant-frame action make (22) analytic as well.

On smooth physical states, the already proved (18) forces (22) to equal its exact correction: both solve the selected minor equations, which have a unique solution. Therefore the **full**, unselected constraint satisfies \(D\mathcal C_z[V(z)]=0\) there. Smooth mean-zero physical states are dense in the actual low source chart. Continuity extends this full identity to every low physical state; the unused \(2m\) constraints have not been silently dropped.

Now use the established actual low inverse

\[
\Pi:(L^2_0)^m\times(H^1_0)^m
\longleftrightarrow (L^2_0)^{2m},\qquad
\Pi(x)=(P_0a,P_0b).
\]

The field

\[
\widehat X(x)=(D\Pi_x)^{-1}
\bigl(P_0V_a(\mathcal P(x)),P_0V_b(\mathcal P(x))\bigr)
\tag{23}
\]

is an actual analytic map of the balanced low source into itself. Since \(V\) is tangent to the complete graph (21), its full coefficient push is \(V\), not just the projected offdiagonal part. Thus the exact coefficient identity (18) extends to this low field.

It remains to identify (23) with the original differential Poisson field at rough states. In the original free \((\Delta_{\rm first},d_{\rm first})\) coordinates, \(L_\mu\) is affine in all fields with fixed matrix coefficients. Its actual Duhamel trace gradients are therefore constant-matrix contractions of the original periodic \(H^1\) adjoint and belong to \(H^1\), continuously and analytically in the low source. First apply the original \(J_{\Delta,d}=-(1/16)\operatorname{offdiag}(I_mD)\) in those coordinates; then transform its velocity to the state chart's \((q,d)\) coordinates by the constant derivative of \(q_i=\Delta_i-S-\sum_{j<m}\operatorname{sgn}(j-i)d_j\). This sum is over the free \(m\) components; its matrix \(A_f\) satisfies \(A_f+A_f^{\mathsf T}=0\), so the constant change also preserves this offdiagonal tensor. Both operations are continuous into \((L^2_0)^{2m}\). On dense smooth physical states the resulting actual original field equals (23). Both sides are continuous into this larger \(L^2\) space, so they remain equal at every low state. In particular its \(d\) component gains the asserted \(H^1\) regularity from (23); this has been proved by the finite graph cancellation, not assumed from the raw gradient budget.

Therefore each fixed actual all-M trace-power field analytically preserves

\[
\boxed{(L^2_0)^m_q\times(H^1_0)^m_d.}
\tag{24}
\]

It has a genuine local Banach flow there, and (18)–(20) hold on that low domain. This gives no invariant action coordinates or common class-kernel completeness. The finite minor procedure is only the actual state-graph correction required by the exact trace field.

## 6. Original frame and external labels remain present

The original full fixed-\(\chi\) monodromy remains the matrix in (5); neither \(\bar E(0)\) nor its source variation is erased from the calibrated data. If an initial-value internal frame \(G^f(0)=I\) is used, its constant transition changes the representative \(X\) but not the quotient identity (20). All these are actual recovered frame functions, not additional arbitrary norming parameters.

For the original prescribed \(B(t)=\Gamma(t)/(2c)\), keep the original nonzero \(c\), \(\Gamma\), \(S\), component-mean labels and the parameter relation \(\mu=\mu_{\rm original}-B\). Raw unnormalized monodromy has the additional scalar \(e^{BL}\); determinant normalization and the centered relation give (5)–(6) exactly. The present proof concerns each current \(B\) section's original physical \(J\)-Hamiltonian tangent. Externally prescribed \(B_t\) is a separate derivative of that section. No \(B_t=0\), \(\Gamma_t=0\), or new autonomous equation for these labels is imposed or inferred.

## 7. What is closed and what remains

The exact all-M field comparison modulo finite constant frame is proved. It needs neither scalar M=2 Birkhoff coordinates nor a high-frequency gap assumption. It uses the actual ODE adjoints and the audited all-M rational generator for every trace power; cyclicity is not an assumption of (18)–(20).

The remaining general-M problem is now the actual vector-AKNS invariant action/divisor/norming state inverse and squared-eigenfunction completeness on the constrained physical quotient. A framed low \(L^2/\ell^2\) inverse does not supply those invariant coordinates. The finite frame quotient, trace normalization and pole weight are no longer missing steps, but this proof alone does not give common class-kernel maximality, ordinary invariant fibers, or the full general-field all-M Liouville theorem.
