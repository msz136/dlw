# General M uniform actual resonances: independent audit

Date: 2026-10-11. Authoring agent: `all_m_holonomy_image_audit`.

This note independently checks the actual uniform finite matrix spectrum, identifies the high-frequency fast/slow branches, and proves uniform isolation of their two-dimensional monodromy collision blocks. It uses no numerical checks and changes no shared manuscript or progress record. The exact quadratic relation already appears in §3.1 of `刘维尔可积性/research/spectral_independent_review_20261011.md`; it is rederived here as an input, rather than presented as a new result. This note does not duplicate the parent's separate Sobolev source perturbation lemma.

## 1. Assumptions and actual spectral variables

Let \(M\geq2\), \(m=M-1\), \(L>0\), \(\delta\in\mathbb R\setminus\{0\}\), and \(S=M\delta\). Number the original \(\chi\) components \(0,\ldots,m\), and put

\[
A_\chi(\lambda)=\lambda P+C_0,
\qquad P=\frac{{\bf1}{\bf1}^{\mathsf T}}M,
\qquad (C_0)_{ij}=\delta\operatorname{sign}(j-i).
\tag{1}
\]

The actual uniform monodromy and its trace normalization are

\[
T_\chi(\lambda)=e^{LA_\chi(\lambda)},\qquad
N_\chi(\lambda)=e^{-\lambda L/M}T_\chi(\lambda)
=e^{L[\lambda(P-I/M)+C_0]}.
\tag{2}
\]

Write \(y_f(\lambda),y_1(\lambda),\ldots,y_m(\lambda)\) for **spatial characteristic exponents**, namely eigenvalues of \(A_\chi(\lambda)\). The corresponding actual Floquet multipliers are \(\nu_j=e^{Ly_j}\). Equality of the fast and slow multipliers is therefore the equation

\[
y_f(\lambda)-y_\ell(\lambda)=K_n,
\qquad K_n=i\kappa_n,\qquad \kappa_n=\frac{2\pi n}{L}.
\tag{3}
\]

The exponent difference in (3) is \(K_n\).

## 2. Exact dispersion from the original finite matrix

For an eigenvector \(v=(v_0,\ldots,v_m)^{\mathsf T}\), subtracting consecutive rows of \(A_\chi v=yv\) gives

\[
(y+\delta)v_{i+1}=(y-\delta)v_i.
\tag{4}
\]

For generic \(y\), put \(t=(y-\delta)/(y+\delta)\). Then \(v_i=t^iv_0\). The first row is

\[
(y+\delta)v_0=(\delta+\lambda/M)\sum_{i=0}^{m}v_i.
\]

Substituting the geometric sum and \(1-t=2\delta/(y+\delta)\) yields

\[
\lambda=S\frac{1+t^M}{1-t^M}
=\mathcal R(y)
\equiv S\frac{(y+\delta)^M+(y-\delta)^M}
{(y+\delta)^M-(y-\delta)^M}.
\tag{5}
\]

The corresponding monic characteristic polynomial identity is

\[
\det(yI-A_\chi(\lambda))=Q_M(y)-\lambda R_M(y),
\tag{6}
\]

\[
Q_M(y)=\frac{(y+\delta)^M+(y-\delta)^M}{2},
\qquad
R_M(y)=\frac{(y+\delta)^M-(y-\delta)^M}{2S}.
\]

Here \(Q_M\) is monic of degree \(M\), and \(R_M\) is monic of degree \(m\). Equation (6) follows first at generic values from (4)–(5), then everywhere by the polynomial identity principle. It also covers the exceptional values omitted when dividing in (4).

The roots of \(R_M\), with a fixed labeling convention, are

\[
\omega_\ell=e^{2\pi i\ell/M},\qquad
p_\ell=\delta\frac{\omega_\ell+1}{\omega_\ell-1}
=-i\delta\cot\frac{\pi\ell}{M},\qquad 1\leq\ell\leq m.
\tag{7}
\]

Thus \((p_\ell+\delta)/(p_\ell-\delta)=\omega_\ell\); the eigenvector ratio \(t\) in (4) tends to \(\omega_\ell^{-1}\). This reciprocal is needed to retain the sign in (7).

## 3. Residues, regular parts, and actual branches at infinity

The poles \(p_\ell\) are distinct and simple. Their residues are

\[
r_\ell=\operatorname{Res}_{y=p_\ell}\mathcal R(y)
=\delta^2-p_\ell^2
=\delta^2\csc^2\frac{\pi\ell}{M}>0.
\tag{8}
\]

For a direct derivation, put \(U=(y+\delta)^M\), \(V=(y-\delta)^M\), \(D=U-V\), and \(F=S(U+V)\). At \(p=p_\ell\), \(U=V\ne0\), and

\[
D'(p)=-\frac{2S U(p)}{p^2-\delta^2},\quad
\frac{F'(p)}{D'(p)}=-Mp,\quad
\frac{D''(p)}{2D'(p)}=\frac{(M-1)p}{p^2-\delta^2}.
\]

Consequently the regular part at this pole is exactly

\[
h_\ell\equiv\lim_{y\to p_\ell}
\left(\mathcal R(y)-\frac{r_\ell}{y-p_\ell}\right)
=\frac{F'(p_\ell)}{D'(p_\ell)}
-r_\ell\frac{D''(p_\ell)}{2D'(p_\ell)}
=-p_\ell.
\tag{9}
\]

The polynomial part of \(\mathcal R\) is \(y\), with zero constant term. Hence the exact partial fraction identity is

\[
\mathcal R(y)=y+\sum_{\ell=1}^{m}\frac{r_\ell}{y-p_\ell}.
\tag{10}
\]

Expanding the two binomials in (5) at infinity gives

\[
\mathcal R(y)=y+\frac{A}{y}+O(y^{-3}),\qquad
A=\delta^2\left[\binom M2-\frac1M\binom M3\right]
=\frac{\delta^2(M^2-1)}3
=\sum_\ell r_\ell.
\tag{11}
\]

The absence of even inverse powers follows from \(\mathcal R(-y)=-\mathcal R(y)\).

For sufficiently large \(|\lambda|\), (6) has one actual analytic fast branch and \(m\) actual analytic slow branches, analytic in \(1/\lambda\) after removing the fast pole. The ordinary finite-dimensional analytic implicit function theorem at each simple root of \(R_M\), and the corresponding equation for \(y_f/\lambda\) near \(1\), give

\[
y_f(\lambda)=\lambda-\frac A\lambda+O(\lambda^{-3}),
\tag{12}
\]

\[
y_\ell(\lambda)=p_\ell+\frac{r_\ell}{\lambda}
-\frac{r_\ell p_\ell}{\lambda^2}+O(\lambda^{-3}).
\tag{13}
\]

The slow second coefficient follows from \(\lambda=r_\ell/(y-p_\ell)-p_\ell+O(y-p_\ell)\), using (9). All bounds and differentiated expansions are uniform over the finitely many channels for fixed \(M,\delta,L\).

## 4. Actual resonance centers and their first corrections

Let \(D_\ell(\lambda)=y_f(\lambda)-y_\ell(\lambda)\). Equations (12)–(13) give

\[
D_\ell(\lambda)=\lambda-p_\ell-\frac{A+r_\ell}{\lambda}
+\frac{r_\ell p_\ell}{\lambda^2}+O(\lambda^{-3}),
\qquad D_\ell'(\lambda)=1+O(\lambda^{-2}).
\tag{14}
\]

An analytic implicit function theorem at \(1/K=0\), after writing \(\lambda=K+p_\ell+o(1)\), solves the actual equation \(D_\ell(\lambda)=K\). Thus, for every sufficiently large \(|n|\), there is a unique root on the designated high-frequency branch,

\[
\boxed{\displaystyle
\lambda_{\ell n}=K_n+p_\ell
+\frac{A+r_\ell}{K_n}
-\frac{p_\ell(A+2r_\ell)}{K_n^2}
+O(|K_n|^{-3}).}
\tag{15}
\]

In particular, the first correction to \(i\kappa_n+p_\ell\) is

\[
\frac{\delta^2[(M^2-1)/3+\csc^2(\pi\ell/M)]}{i\kappa_n}.
\tag{16}
\]

These are exact multiplier collision points obtained by solving (3). The uncorrected \(i\kappa_n+p_\ell\) are only asymptotic centers.

The exact quadratic from the existing §3.1 provides an independent way to identify the same branches. At finite nonpole points,

\[
\mathcal R(y+K)=\mathcal R(y)
\iff\left(\frac{W+K\delta}{W-K\delta}\right)^M=1,
\qquad W=y^2+Ky-\delta^2.
\]

For channel \(\ell\), choose the root of unity \(\omega_\ell\). This gives \(W=Kp_\ell\), and therefore

\[
y_s(K)=-\frac K2+\sqrt{\frac{K^2}4+Kp_\ell+\delta^2},
\qquad y_f(K)=y_s(K)+K,
\tag{17}
\]

where the square root is defined by

\[
\sqrt{\frac{K^2}4+Kp_\ell+\delta^2}
=\frac K2\left(1+\frac{4p_\ell}K+\frac{4\delta^2}{K^2}\right)^{1/2},
\qquad (1+z)^{1/2}\to1.
\tag{18}
\]

This is an analytic branch at infinity; an unspecified principal square root would give the wrong labeling for one sign of \(n\). Equations (17)–(18) imply

\[
y_s(K)=p_\ell+\frac{r_\ell}{K}-\frac{2p_\ell r_\ell}{K^2}+O(K^{-3}),
\qquad
\lambda_{\ell n}=\mathcal R(y_s(K_n)+K_n)=\mathcal R(y_s(K_n)).
\tag{19}
\]

For large \(|n|\), these values are finite, the fast argument tends to infinity, and the slow argument tends to the specified pole without equaling it. Hence they are precisely the spatial branches in (12)–(13), rather than other solutions of the algebraic relation.

For \(M=2\), \(p_1=0\), \(A=r_1=\delta^2\), and the exact high-frequency solution is

\[
\lambda_{1n}=K_n\left(1+\frac{4\delta^2}{K_n^2}\right)^{1/2}
=i\kappa_n\left(1-\frac{4\delta^2}{\kappa_n^2}\right)^{1/2}
=i\kappa_n-\frac{2i\delta^2}{\kappa_n}+O(\kappa_n^{-3}).
\tag{20}
\]

This verifies directly that the leading center is not the exact collision.

## 5. Imaginary centers and absence of triple collisions

For real \(\delta\), \(K_n=i\kappa_n\) and \(p_\ell=-i\delta\cot(\pi\ell/M)\). The square-root radicand in (17) is real and negative for sufficiently large \(|n|\). The branch (18) is imaginary, so \(y_s(K_n)\), \(y_f(K_n)\), and \(\lambda_{\ell n}\) are all purely imaginary. The last conclusion also follows from the real odd rational function (5), or from (10).

Consequently \(A_\chi(\lambda_{\ell n})\) and its trace-normalized version are anti-Hermitian. The corresponding \(T_\chi\) and \(N_\chi\) are unitary. Their spatial characteristic exponents are still distinct and simple: the fast root is unbounded and the slow roots approach the distinct \(p_j\). The repeated Floquet multiplier arises only after exponentiation, and has geometric as well as algebraic multiplicity two if it is separated from the other multipliers.

Assume the no-adjoint-alias condition

\[
p_j-p_\ell\notin i\frac{2\pi}{L}\mathbb Z
\quad (j\ne\ell),
\qquad\text{equivalently}\qquad
\rho_j=e^{Lp_j}\ne\rho_\ell=e^{Lp_\ell}.
\tag{21}
\]

For \(m\ge2\), define \(\Delta=\min_{j\ne\ell}|\rho_j-\rho_\ell|>0\). At \(\lambda_{\ell n}\), (13) gives

\[
\nu_j(\lambda_{\ell n})=\rho_j+O(|\kappa_n|^{-1}),
\qquad
\nu_f(\lambda_{\ell n})=\nu_\ell(\lambda_{\ell n}).
\tag{22}
\]

Thus all slow multipliers remain pairwise separated, and the collision multiplier has distance at least \(\Delta/2\) from every other multiplier for sufficiently large \(|n|\). There are no triple or simultaneous additional collisions at these points. For \(m=1\), there are no other multipliers and the conclusion about separation is vacuous.

The trace-normalized multipliers acquire the common factor \(e^{-\lambda_{\ell n}L/M}\), of modulus one. All separation distances in (22) remain unchanged. The raw slow multipliers tend to \(\rho_j\); the normalized slow multipliers have this common rotating phase and should not be asserted to have the same limit.

The transverse exponent slope is

\[
\gamma_{\ell n}=D_\ell'(\lambda_{\ell n})=1+O(\kappa_n^{-2}).
\tag{23}
\]

In particular

\[
\left.\partial_\lambda(\nu_f-\nu_\ell)\right|_{\lambda_{\ell n}}
=L\nu_\ell(\lambda_{\ell n})\gamma_{\ell n}\ne0.
\tag{24}
\]

The derivative has modulus at least \(L/2\) for sufficiently large \(|n|\). The same bound holds after trace normalization, since the derivative of the common normalization factor multiplies a difference that vanishes at the collision.

## 6. Uniform actual Riesz blocks in the spectral parameter

Set \(g=\min(1,\Delta)\) if \(m\ge2\), and \(g=1\) if \(m=1\). Increasing the high-frequency threshold if necessary, every noncolliding multiplier is at distance at least \(3g/4\) from the collision multiplier. Take the circle centered at the collision multiplier with radius \(g/4\). At the imaginary center \(\lambda_* =\lambda_{\ell n}\), the monodromy is unitary, so its resolvent on this circle has norm at most \(4/g\). Its Riesz projection is an orthogonal rank-two projection.

This circle remains valid for a spectral-parameter neighborhood whose radius is independent of \(\ell,n\). Indeed, \(P\) and \(P-I/M\) have norm at most one. For either monodromy in (2), the anti-Hermitian reference at \(\lambda_*\) and Duhamel's formula give

\[
\|T_\chi(\lambda)-T_\chi(\lambda_*)\|
\le L|\lambda-\lambda_*|e^{L|\lambda-\lambda_*|},
\qquad
\|N_\chi(\lambda)-N_\chi(\lambda_*)\|
\le L|\lambda-\lambda_*|e^{L|\lambda-\lambda_*|}.
\tag{25}
\]

Choose \(r>0\) so that \(Lr e^{Lr}<g/16\). The resolvent identity and a Neumann series on the fixed circle then imply a uniform bound, for example \(8/g\), on the perturbed resolvent for \(|\lambda-\lambda_*|<r\). The contour remains free of spectrum, and the corresponding Riesz projection is analytic and has constant rank two throughout that neighborhood. The constants depend on \(M,\delta,L\) and the no-alias gap, but not on \(n\).

The same conclusion holds in any fixed uniformly invertible finite-dimensional split frame by similarity, with the resolvent constants multiplied by that frame's condition number. No uniform bound is inferred by perturbing the original variable-principal \(\chi\) system in the physical source. That separate issue requires the state-adapted fixed-principal frame used in the parent's source-space argument.

For completeness, the resonance chains themselves have a uniform separation in the \(\lambda\)-plane. With \(k_0=2\pi/L\), put

\[
d_* =\min\left(k_0,\min_{j\ne\ell}\operatorname{dist}(p_j-p_\ell,ik_0\mathbb Z)\right)>0,
\tag{26}
\]

where the second minimum is omitted for \(m=1\). Positivity follows from (21) and the finite number of channel pairs. Distinct leading centers \(ik_0n+p_\ell\) have distance at least \(d_*\). Equation (15) therefore gives distance at least \(d_*/2\) between any two distinct sufficiently high-frequency actual resonance centers. If useful, the radius \(r\) in (25) can also be chosen below \(d_*/8\).

## 7. Audit conclusion

PASS for the following uniform-background claims: exact finite matrix dispersion (5)–(6); slow pole labels (7); the regular-part identity \(h_\ell=-p_\ell\); actual high-frequency branch assignment; the corrected resonance centers (15)–(16); imaginary high-frequency centers; uniformly isolated, semisimple rank-two actual monodromy collision blocks under (21); and the nonzero uniform slope (23)–(24).

The established exact quadratic is reused with an explicit analytic branch convention. The argument neither treats the leading centers as exact nor substitutes a formal scalar resolvent for the actual monodromy. A physical source-to-spectral-data inverse, source-dependent moving gaps, and their Banach-space bounds remain separate lemmas and are not claimed here.
