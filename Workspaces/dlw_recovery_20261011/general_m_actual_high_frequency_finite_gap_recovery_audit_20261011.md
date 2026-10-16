# Independent audit: real finite high-frequency gap independence for general M

2026-10-11. Read [the actual high-frequency Riesz-gap lemma, §8](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md), together with its §§6–7 and the [actual physical coefficient chart, §§4–6](all_m_physical_holonomy_state_inverse_20261011.md). The actual Riesz blocks, sequence analyticity and Born Hessian in §§1–7 are inputs already reviewed by the parent; this audit independently checks the new real Fourier witnesses, exact channel map, nonlinear minors and genericity scope. No checks were run, and no shared records or other author's proof were edited.

**Verdict: PASS for §8.** The correct count is \(2m\) real functions per positive high frequency. The residual conclusion is on the actual real mixed-low source ball; transfer to a thinner strong parameter phase requires the precise Fourier-range hypothesis in §8.3.

## 1. Exact real reflection and its independent channels

Let \(m=M-1\), \(K_n=2\pi in/L\), and \(p_\ell=-i\delta\cot(\pi\ell/M)\). For real \(\delta\),

\[
p_{M-\ell}=\bar p_\ell,
\qquad K_{-n}=\bar K_n.
\]

The original background matrix is real in its coefficients. Conjugation of its actual fast and slow eigenbranches therefore takes the channel \((\ell,n)\) to \((M-\ell,-n)\). Uniqueness of the high collision in its separated labeled window gives

\[
\lambda_{M-\ell,-n}=\overline{\lambda_{\ell n}},\qquad
\gamma_{M-\ell,-n}=\overline{\gamma_{\ell n}}.
\]

Choose each reflected right/left eigenbasis as the conjugate of the original basis. Then for actual real physical tangents the two Born couplings separately obey

\[
\Gamma^\pm_{M-\ell,-n}=\overline{\Gamma^\pm_{\ell n}},
\tag{A1}
\]

and the actual squared gaps obey \(g_{M-\ell,-n}=\overline{g_{\ell n}}\). No interchange of \(\Gamma^+\) and \(\Gamma^-\) is needed: fast remains fast under conjugation. A positive \(n\) is never fixed by this reflection, including the self-reflected slow branch \(\ell=M/2\) when \(M\) is even. Thus no extra reality constraint removes one of the two real components of a positive-frequency gap. Negative channels contribute no additional independent functions.

## 2. The actual physical derivative realizes all finite Fourier tests

At the fixed uniform mean leaf, the exact derivative has

\[
D\Pi_0:X_0^\mathbb R\longrightarrow
(L^2_0)^m_{a,\mathbb R}\times(L^2_0)^m_{b,\mathbb R}
\quad\text{bounded real isomorphism}.
\tag{A2}
\]

The source's real completion is \(X_0^\mathbb R=(L^2_0)^m\times(H^1_0)^m\). Its background Fourier coefficients are constant, and the only internal inverse is \((ik_n-\operatorname{ad}H_0)^{-1}\). Consequently \(D\Pi_0\) and its inverse act separately on each nonzero Fourier mode. Each finite Fourier target has a finite Fourier physical preimage. Since the coefficient derivative is real, the inverse preserves the usual negative-mode conjugation.

The complete mean identities are also exact:

\[
D\langle a\rangle=D\langle b\rangle=DH=0.
\tag{A3}
\]

They follow from the state-chart formula \(\dot a=u+q_0g\), \(\dot b=Z_1-Dv/S-gr_0\), with \(u,v,g,Z_1\) mean zero, and \(\dot H=\langle\dot V\rangle=0\). Thus the realized full potential tangent is precisely

\[
\widehat{\dot A}_n=\begin{pmatrix}0&A_n\\B_n&0\end{pmatrix},
\qquad \widehat{\dot A}_{-n}=\overline{\widehat{\dot A}_n},
\]

with no extra mean or constant-\(H\) channel. This is why the background diagonal Born terms vanish, and why the Fourier witnesses lie on the actual physical leaf rather than only in an unconstrained vector-potential model.

## 3. Exact complex linearity and a uniform high-frequency inverse

Choose a slow right/left basis \(s_\ell,t_\ell\) of \(H_0\), with \(t_js_\ell=\delta_{j\ell}\), respecting \(s_{M-\ell}=\bar s_\ell\) and \(t_{M-\ell}=\bar t_\ell\). At each actual collision the already recorded branch expansions give

\[
e_f=(1,O(n^{-1}))^{\mathsf T},\quad
\ell_f=(1+O(n^{-2}),O(n^{-1})),
\]

\[
e_\ell=(O(n^{-1}),s_\ell+O(n^{-1}))^{\mathsf T},\quad
\ell_\ell=(O(n^{-1}),t_\ell+O(n^{-1})).
\]

For positive \(n\), the exact map is

\[
T_n(A_n,B_n)=
\left(
\ell_f\widehat{\dot A}_ne_\ell,
\overline{\ell_\ell\widehat{\dot A}_{-n}e_f}
\right)_{\ell=1}^m.
\tag{A4}
\]

After substituting \(\widehat{\dot A}_{-n}=\overline{\widehat{\dot A}_n}\), its second component is \(\bar\ell_\ell\widehat{\dot A}_n\bar e_f\). It is therefore exactly complex linear in the freely chosen \((A_n,B_n)\). Its limit is

\[
T_\infty(A_n,B_n)=
(A_ns_\ell,t_{M-\ell}B_n)_{\ell=1}^m.
\tag{A5}
\]

The right-eigenvector matrix and left-eigenvector matrix are inverse matrices; the reflection is just a finite permutation. Hence \(T_\infty\) is a complex isomorphism. In finite dimension the recorded entry errors imply

\[
\|T_n-T_\infty\|\le C/n.
\]

Increase one fixed \(N\) until \(\|T_\infty^{-1}(T_n-T_\infty)\|<1/2\). A Neumann inverse gives uniformly bounded \(T_n\) and \(T_n^{-1}\) for every \(n\ge N\). All constants may depend on the fixed \(M,L,\delta\) and the nonalias distance. No small-\(\delta\) assumption or scalar M=2 canonical relation is inserted here.

## 4. The real nonlinear minor and its leading determinant

Fix any finite positive set \(F\subset\{n\ge N\}\), and put \(d=2m|F|\). Use the exact \(T_n^{-1}\), then (A2), to choose a real finite Fourier physical tangent \(f\) with

\[
\alpha_{\ell n}=\Gamma^+_{\ell n}(f)=1,\qquad
\beta_{\ell n}=\overline{\Gamma^-_{\ell n}(f)}=1
\quad(n\in F).
\]

For each selected complex coordinate choose two real finite Fourier tangents whose exact coupling outputs have \(\delta\alpha=0\) and whose \(\delta\beta\) is respectively \(1\) and \(i\) in that coordinate and zero in all other selected coordinates. The frequencies do not mix because the derivative is a Fourier multiplier and every Born coupling uses its own \(\pm n\) coefficients.

The actual Hessian from the Riesz proof gives

\[
g^{[2]}_{\ell n}(f)=-4\gamma_{\ell n}^{-2}
\alpha_{\ell n}\overline{\beta_{\ell n}},
\qquad
Dg^{[2]}_{\ell n}(f)[h]
=-4\gamma_{\ell n}^{-2}\overline{\delta\beta_{\ell n}}.
\tag{A6}
\]

For a nonzero complex \(c=-4\gamma_{\ell n}^{-2}\), the map \(z\mapsto c\bar z\) is a real two-dimensional isomorphism with determinant \(-|c|^2=-16|\gamma_{\ell n}|^{-4}\) in the displayed \(1,i\) coordinate basis. Thus the \(d\times d\) real Jacobian of all selected \((\operatorname{Re}g,\operatorname{Im}g)\), tested on these fixed directions, has a nonsingular leading block diagonal matrix.

Banach analyticity gives, for this fixed finite list,

\[
Dg(\varepsilon f)[h]
=\varepsilon D^2g(0)[f,h]+O(\varepsilon^2),
\]

so its minor is

\[
\varepsilon^d C_F+O(\varepsilon^{d+1}),\qquad C_F\ne0.
\tag{A7}
\]

For sufficiently small nonzero real \(\varepsilon\), the actual nonlinear differentials are independent. All witnesses can be made arbitrarily close to the background inside the fixed source ball. The derivative is zero at the background itself, in agreement with the double-root criticality; that point is not declared regular.

## 5. Low-domain genericity and the precise strong transfer

For every fixed finite \(F\), the minor in (A7) is one real-analytic scalar function on the connected actual source ball. Its arbitrarily near-zero nonzero witness shows it is not identically zero. The real-analytic identity theorem along Banach affine lines then makes its nonzero locus open dense. There are countably many finite subsets of the positive integers. Their intersection is a dense residual subset of that actual real \(X_0\) ball, and every finite high-gap block has independent real differentials there.

A valid extra consequence on this same low ball is that all individual high gaps can be required nonzero as well: the singleton witness above has \(g_{\ell n}(\varepsilon f)=-4\gamma_{\ell n}^{-2}\varepsilon^2+O(\varepsilon^3)\ne0\). Each individual nonzero-gap locus is open dense; intersecting their countable family with the finite-minor loci remains dense residual. This does not identify a norming inverse or any action coordinate, and it does not transfer the residual subset to another function phase by density alone.

For the separate strong parameter map \(F_H:O_H\to X_0\), the stated assumptions are sufficient: real analyticity, \(F_H(0)=0\), and range of \(DF_H(0)\) containing all required finite real physical Fourier tangents. Choose parameter preimages of \(f\) and all tests \(h\). Since \(Dg(0)=0\),

\[
D^2(g\circ F_H)(0)[u,v]
=D^2g(0)[DF_H(0)u,DF_H(0)v].
\]

The \(D^2F_H\) term vanishes. The same leading minor follows at \(\varepsilon f_H\), and Baire applies on one connected parameter ball after the actual map is known to land in the fixed low domain. This is exactly the conditional transfer in §8.3. An ambient low residual set, a smooth-density assertion, or an unspecified strong chart does not establish these hypotheses.

## 6. Coverage and remaining scope

This PASS verifies the real reflection, uniform exact physical coupling inverse, mean/holonomy derivative identities, finite Fourier witnesses, actual nonlinear minors and low residual statement of §8. It does not independently reprove §§1–7, nor prove canonical norming coordinates, an invariant action inverse, Hamiltonian gap-flow completeness, regular Lagrangian fibers, or general-M Liouville completeness.

The exact coupling inverse suggests a separate actual **state** inverse from calibrated high norming candidates plus finitely many low Fourier coefficient data. That implication is recorded in a separate note; the finite supplemental coefficients are not spectral invariants, and the norming candidates retain the full coefficient frame/calibration.
