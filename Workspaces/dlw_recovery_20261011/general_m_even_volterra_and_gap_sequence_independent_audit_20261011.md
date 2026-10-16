# General M full Volterra remainder and gap sequence: independent audit

2026-10-11. Independent hand audit by `all_m_holonomy_image_audit`. No machine checks were run. No shared source or progress records were changed.

The even-insertion kernel estimate, full monodromy sequence estimate, and local analytic center/half-gap extraction stated below pass. The distinction between an abstract perturbation at Q=0 and a physical source perturbation at its uniform state is recorded in §6.

## 1. Actual Volterra expansion and the even fibers

Fix \(L>0\), a constant \(H\in\mathbb C^{m\times m}\), and periodic coefficients

\[
a\in L^2(0,L;\mathbb C^{1\times m}),\qquad
b\in L^2(0,L;\mathbb C^{m\times1}).
\]

Consider the actual initial-value equation

\[
Y'=\left[\begin{pmatrix}\lambda&0\\0&H\end{pmatrix}
+\begin{pmatrix}0&a(x)\\b(x)&0\end{pmatrix}\right]Y,
\qquad Y(0)=I,
\qquad \mathsf M(\lambda)=Y(L).
\tag{1}
\]

The coefficient is integrable. Its actual monodromy has the convergent chronological Volterra expansion. For \(k\) insertions, use the ordered times

\[
0<t_1<\cdots<t_k<L,
\]

and the interval lengths

\[
g_0=t_1,\quad g_j=t_{j+1}-t_j\ (1\le j<k),
\quad g_k=L-t_k.
\]

All intervals are nonnegative and sum to L. Every nonzero path alternates between the one-dimensional fast channel and the m-dimensional slow channel. Let \(\tau\) be its total fast duration. Its spectral factor is exactly \(e^{\lambda\tau}\), and the remaining amplitude contains slow propagators \(e^{Hs}\) with total slow duration \(L-\tau\).

With \(2r\) insertions, a fast-to-fast path has \(r+1\) fast intervals and \(r\) slow intervals. The pushforward of ordered-simplex Lebesgue measure under the fast-duration map has fiber density

\[
V_{ff,r}(\tau)=
\frac{\tau^r(L-\tau)^{r-1}}{r!(r-1)!},
\qquad 0<\tau<L,\quad r\ge1.
\tag{2}
\]

A slow-to-slow path has r fast intervals and \(r+1\) slow intervals, giving

\[
V_{ss,r}(\tau)=
\frac{\tau^{r-1}(L-\tau)^r}{(r-1)!r!}.
\tag{3}
\]

These are products of the coordinate simplex volumes obtained by splitting \(\tau\) among the fast intervals and \(L-\tau\) among the slow intervals. The fiber measure is the measure in the Lebesgue disintegration formula

\[
\int_{0<t_1<\cdots<t_{2r}<L}F(t)\,dt
=\int_0^L\int_{\operatorname{fiber}(\tau)}F(t)\,d\mu_\tau(t)\,d\tau.
\tag{4}
\]

It is not the unweighted Euclidean Hausdorff measure on that affine fiber. For example, when r=1 in the fast-to-fast block, \(\tau=L-t_2+t_1\) and \(0<t_1<\tau\), so the fiber density is precisely \(\tau\), without a spurious \(\sqrt2\) factor.

## 2. Fiber Cauchy and the even L² kernel bound

Let \(f_j(t_j)\) denote the corresponding a or b insertion, and use its Euclidean row/column norm. The Hilbert–Schmidt norm of the matrix amplitude is bounded by

\[
e^{L\|H\|}\prod_{j=1}^{2r}\|f_j(t_j)\|.
\]

This holds for the scalar fast block and the slow block, whose inserted matrix product is built from rank-one row/column products and slow propagators. Thus, for the resulting even kernel \(K_r(\tau)\), Cauchy–Schwarz on the fiber gives

\[
\|K_r(\tau)\|_{\rm HS}^2
\le e^{2L\|H\|}V_r(\tau)
\int_{\operatorname{fiber}(\tau)}
\prod_{j=1}^{2r}\|f_j(t_j)\|^2\,d\mu_\tau(t).
\tag{5}
\]

For either (2) or (3),

\[
\sup_\tau V_r(\tau)
\le\frac{L^{2r-1}}{r!(r-1)!}.
\]

Integrating (5), using (4), and enlarging the ordered simplex to the full product cube yields

\[
\boxed{\displaystyle
\|K_r\|_{L^2(0,L;\rm HS)}
\le e^{L\|H\|}
\frac{L^{r-1/2}}{\sqrt{r!(r-1)!}}
\prod_{j=1}^{2r}\|f_j\|_{L^2}.}
\tag{6}
\]

The integral of the squared product over the cube factors exactly as the product of the squared L² norms. No L² multiplication algebra is used.

For comparison, \(2r+1\) insertions in either off-diagonal block have \(r+1\) fast and \(r+1\) slow intervals. Their density and estimate are

\[
V_{\mathrm{odd},r}(\tau)=
\frac{\tau^r(L-\tau)^r}{(r!)^2},
\qquad
\|K_{\mathrm{odd},r}\|_2
\le e^{L\|H\|}\frac{L^r}{r!}
\prod_{j=1}^{2r+1}\|f_j\|_2.
\tag{7}
\]

The r=0 odd estimate is the ordinary one-insertion kernel. The zero-insertion diagonal terms are endpoint atoms and must be retained separately; they are not L² kernels.

## 3. Full remainder and joint entire sequence map

Write \(\alpha=\|a\|_2\) and \(\beta=\|b\|_2\). The even kernel sums in the two diagonal blocks are bounded by

\[
e^{L\|H\|}L^{-1/2}
\sum_{r\ge1}\frac{(L\alpha\beta)^r}{\sqrt{r!(r-1)!}},
\tag{8}
\]

and the two odd sums are bounded by

\[
e^{L\|H\|}\alpha e^{L\alpha\beta},\qquad
e^{L\|H\|}\beta e^{L\alpha\beta}.
\tag{9}
\]

Since \(\sqrt{r!(r-1)!}=r!/\sqrt r\), all these sums converge locally uniformly on the coefficient space. Each term is a bounded multilinear expression in a,b, with entire dependence on the finite matrix H. Consequently the sum K is a joint entire map

\[
(a,b,H)\longmapsto K\in L^2(0,L;\mathbb C^{M\times M}),
\]

and the actual full monodromy has the representation

\[
\mathsf M(\lambda)
=\operatorname{diag}(e^{\lambda L},e^{HL})
+\int_0^L e^{\lambda\tau}K(\tau)\,d\tau.
\tag{10}
\]

This includes both diagonal even kernels and the off-diagonal odd kernels.

For \(\kappa_n=2\pi n/L\), Parseval applied entrywise gives

\[
\sum_{n\in\mathbb Z}
\left\|\int_0^L e^{i\kappa_n\tau+\sigma\tau}K(\tau)\,d\tau\right\|_{\rm HS}^2
=L\|e^{\sigma\tau}K\|_2^2
\le L e^{2L|\operatorname{Re}\sigma|}\|K\|_2^2.
\tag{11}
\]

Thus the full remainder

\[
\left(\mathsf M(i\kappa_n+\sigma)
-\operatorname{diag}(e^{\sigma L},e^{HL})\right)_{n\in\mathbb Z}
\tag{12}
\]

is in ℓ², jointly entire in the coefficients and holomorphic in \(\sigma\). The same holds upon restricting to a one-sided or high-frequency subsequence. The estimates are locally uniform on coefficient sets and compact spectral-parameter disks.

## 4. Correct upgrade to per-channel disk suprema

An estimate of \(\sup_\sigma\sum_n|F_n(\sigma)|^2\) alone does not permit exchanging the supremum and sum. The required upgrade follows from a larger disk.

Let \(0<R_1<R_2\), and suppose the functions \(F_n\) are holomorphic on a neighborhood of the closed disk of radius \(R_2\), with

\[
\sup_{|\sigma|\le R_2}\sum_n\|F_n(\sigma)\|^2\le C^2.
\]

Cauchy's formula and Cauchy–Schwarz on the outer circle give, for every \(|\sigma|\le R_1\),

\[
\|F_n(\sigma)\|^2
\le\left(\frac{R_2}{R_2-R_1}\right)^2
\frac1{2\pi}\int_0^{2\pi}\|F_n(R_2e^{it})\|^2\,dt.
\]

The right-hand side does not depend on \(\sigma\). Taking the inner supremum before summing therefore proves

\[
\boxed{\displaystyle
\sum_n\sup_{|\sigma|\le R_1}\|F_n(\sigma)\|^2
\le\left(\frac{R_2}{R_2-R_1}\right)^2 C^2.}
\tag{13}
\]

Applied to (11), this is a bounded linear restriction into \(\ell^2 H^\infty(D_{R_1})\); it preserves coefficient-space analyticity. Spectral-parameter derivatives on still smaller disks follow by the same Cauchy argument. One may use the equivalent Hardy boundary norm on the larger circle instead of the displayed outer supremum.

## 5. Actual two-root contour moments: c in ℓ² and g in ℓ¹

Fix \(0<\rho<2\pi/L\) and a larger disk \(D_R\) with \(R>\rho\). Suppose

\[
B_n(\zeta)=\operatorname{diag}(e^{L\zeta},1)+Q_n(\zeta),
\qquad Q\in\ell^2 H^\infty(D_R;\mathbb C^{2\times2}),
\tag{14}
\]

and \(\sup_n\|Q_n\|_{H^\infty}\) is sufficiently small. Put

\[
F(\zeta)=e^{L\zeta}-1,\qquad
h_n=Q_{n,11}-Q_{n,22},\qquad
D_n=(\operatorname{tr}B_n)^2-4\det B_n.
\]

Direct expansion gives the exact identity

\[
D_n=F^2+2Fh_n+h_n^2+4Q_{n,12}Q_{n,21}.
\tag{15}
\]

On \(|\zeta|=\rho\), F is bounded away from zero. Uniform smallness of Q permits Rouché's theorem against \(F^2\), so every disk contains exactly two zeros counted with multiplicity. No ordering or separate analyticity of those roots is needed.

For the power sums and the center/half-gap-squared, define

\[
s_{j,n}=\frac1{2\pi i}\oint_{|\zeta|=\rho}
\zeta^j\frac{D_n'}{D_n}\,d\zeta,\qquad
c_n=\frac{s_{1,n}}2,\qquad
g_n=\frac{s_{2,n}}2-c_n^2.
\tag{16}
\]

If the two roots are \(\zeta_{n,1},\zeta_{n,2}\), then

\[
c_n=\frac{\zeta_{n,1}+\zeta_{n,2}}2,\qquad
g_n=\frac{(\zeta_{n,1}-\zeta_{n,2})^2}4.
\]

Thus g is the half-gap squared. The full gap squared is 4g.

On the contour let

\[
U_n=\frac{D_n-F^2}{F^2}
=\frac{2h_n}{F}
+\frac{h_n^2+4Q_{n,12}Q_{n,21}}{F^2}.
\]

The smallness condition ensures \(\|U_n\|<1\) uniformly. The branch \(\log(1+U_n)\) near zero is single-valued on a neighborhood of the contour. Integration by parts, with the background moments equal to zero, yields

\[
c_n=-\frac12\frac1{2\pi i}\oint\log(1+U_n)\,d\zeta,
\tag{17}
\]

\[
g_n=-\frac1{2\pi i}\oint\zeta\log(1+U_n)\,d\zeta-c_n^2.
\tag{18}
\]

Uniformly on the contour,

\[
\log(1+U_n)=\frac{2h_n}{F}+R_n,
\qquad
\|R_n\|_\infty\le C\|Q_n\|_{H^\infty}^2.
\tag{19}
\]

At the abstract base point Q=0, (17) gives

\[
Dc_n(0)[Q_n]=-
\frac1{2\pi i}\oint\frac{h_n}{F}\,d\zeta
=-\frac{h_n(0)}L.
\tag{20}
\]

The linear term in (18) vanishes because \(\zeta h_n/F\) is holomorphic inside the contour, including at zero. Therefore

\[
Dg_n(0)=0,\qquad
|c_n|\le C\eta_n,\qquad
|g_n|\le C\eta_n^2,
\qquad \eta_n=\|Q_n\|_{H^\infty}.
\tag{21}
\]

It follows that c belongs to ℓ² and g belongs to ℓ¹, with

\[
\|c\|_{\ell^2}\le C\|Q\|_{\ell^2H^\infty},\qquad
\|g\|_{\ell^1}\le C\|Q\|_{\ell^2H^\infty}^2.
\tag{22}
\]

These are Banach analytic maps, not just coordinatewise analytic maps. One direct verification uses the common scalar Taylor series of the contour functionals. The c-series starts in degree one and the g-series starts in degree two. For a degree j term with j≥2,

\[
\sum_n\eta_n^j
\le\|\eta\|_\infty^{j-2}\|\eta\|_2^2,
\]

while the c-series satisfies

\[
\|(\eta_n^j)_n\|_2
\le\|\eta\|_\infty^{j-1}\|\eta\|_2.
\]

The uniform scalar Cauchy bounds make both series locally normally convergent on the ℓ² domain with sufficiently small ℓ∞ norm. The associated polarized multilinear maps into ℓ¹ are bounded: use Cauchy–Schwarz on two sequence factors and ℓ∞ on the remaining ones. This proves the claimed complex analyticity into \(\ell^2\times\ell^1\).

## 6. Precise interpretation at the physical uniform state

The statement \(Dg(0)=0\) in (21) is an assertion at the abstract perturbation Q=0. If a chosen physical chart has \(Q(z_0)\ne0\) at its uniform source state, it does not follow from (21) alone that \(D_zg(z_0)=0\).

The actual uniform resonance branches provide the needed separate check. In an analytic uniform eigenframe and after dividing by the nonzero slow multiplier, write the exact background block as

\[
B_n^0(\zeta)=\operatorname{diag}(E_n(\zeta),1),\qquad
F_n=E_n-1,
\]

where

\[
E_n(\zeta)=
\exp\{L[y_f(\lambda_{\ell n}+\zeta)-y_\ell(\lambda_{\ell n}+\zeta)-K_n]\}.
\tag{23}
\]

Then \(F_n(0)=0\), \(F_n'(0)=L\gamma_{\ell n}\ne0\), and the earlier uniform resonance audit gives \(\gamma_{\ell n}=1+O(\kappa_n^{-2})\). For high n, \(F_n\) has only the simple zero at zero in the chosen disk and is uniformly bounded away from zero on its circle.

For an actual source variation expressed as a perturbation of this exact background block, the same algebra yields the linear discriminant variation \(2F_n h_n\). Replacing F by \(F_n\) in (17)–(20), one obtains

\[
Dc_n(z_0)[\dot Q_n]=-
\frac{\dot h_n(0)}{F_n'(0)},\qquad
D_zg_n(z_0)=0,
\tag{24}
\]

since \(\zeta\dot h_n/F_n\) remains holomorphic. These constants are uniform at high frequency. This verifies physical first-order vanishing when the exact uniform branch normalization is used. It does not require replacing an exact exponent difference by its leading linear approximation.

## 7. Conclusion

The proposed even fiber formula and kernel estimate are correct. Combined with the odd estimates, they give an actual full monodromy remainder that is jointly entire into ℓ² and, after a larger-disk Cauchy restriction, into the required per-channel disk supremum space. The two-root contour construction then gives analytic centers in ℓ² and half-gap-squared in ℓ¹. The abstract linear cancellation and its separate exact-uniform physical version are both valid. No source inverse, spectral completeness, Poisson or action-angle claim follows solely from these estimates.

## 8. Finite high-frequency actual gap independence

This additional independent audit concerns finite blocks of actual gap functions. It uses the already established mean-normalized physical state inverse; it adds no kernel estimates and performs no machine checks.

### 8.1 Required physical tangent chart

Use the real balanced source space

\[
X_0=L^2_{0,\mathrm{per}}(q)\times H^1_{0,\mathrm{per}}(d),
\]

at its uniform state z=0. Assume the previously proved analytic physical chart

\[
\Pi(z)=(P_0a(z),P_0b(z))
\]

has a bounded real derivative isomorphism

\[
D\Pi(0):X_0\longrightarrow
L^2_{0,\mathrm{per}}(\mathbb R^{1\times m})
\times L^2_{0,\mathrm{per}}(\mathbb R^{m\times1}),
\tag{25}
\]

and that its physical graph satisfies

\[
D\langle a\rangle(0)=D\langle b\rangle(0)=DH(0)=0.
\tag{26}
\]

Mean-normalized periodic gauge uniqueness makes this chart translation-equivariant. Consequently DΠ(0), and its inverse, commute with Fourier projections. Every finite Fourier pair in the target therefore has a finite Fourier source preimage in X₀, with the same frequency support. This is stronger than an abstract existence claim for a preimage and supplies the witnesses below.

For a positive frequency n, arbitrary complex Fourier coefficients \(A_n,B_n\) determine a real tangent pair by

\[
\dot a(x)=A_ne^{i\kappa_nx}+\overline{A_n}e^{-i\kappa_nx},\qquad
\dot b(x)=B_ne^{i\kappa_nx}+\overline{B_n}e^{-i\kappa_nx}.
\]

Its actual coefficient variation has

\[
\dot A_n=\begin{pmatrix}0&A_n\\B_n&0\end{pmatrix},
\qquad\dot A_{-n}=\overline{\dot A_n},\qquad
\dot A_0=0.
\tag{27}
\]

The final equality uses (26), including the constant slow-block variation.

### 8.2 Exact Born selector and the coefficient isomorphism

The uniform constant slow matrix H₀ is real, has the simple eigenvalues \(p_\ell\), and admits right and left eigenbases \(s_\ell,t_\ell\), normalized by \(t_\ell s_j=\delta_{\ell j}\). Choose conjugate phases so that

\[
s_{M-\ell}=\overline{s_\ell},\qquad
t_{M-\ell}=\overline{t_\ell}.
\]

The self-conjugate channel, when present, uses real eigenvectors.

At the actual center \(\lambda_{\ell n}\), choose analytic generator eigenvectors and their algebraic left duals in the fixed split frame. For large n their normalized estimates are

\[
e_f=\binom{1}{O(n^{-1})},\quad
\ell_f=(1+O(n^{-2}),O(n^{-1})),
\]

\[
e_\ell=\binom{O(n^{-1})}{s_\ell+O(n^{-1})},\quad
\ell_\ell=(O(n^{-1}),t_\ell+O(n^{-1})).
\tag{28}
\]

The constants are uniform over the finite number of channels. These follow by solving the fast resolvent equation and the simple slow-root Schur-complement equation at infinity. The generator roots are simple even though their monodromy multipliers collide.

Let \(\nu=e^{Ly_f}=e^{Ly_\ell}\) at the collision. The actual Born formula in this eigenframe is

\[
\dot T_{ij}=e^{Ly_i}
\int_0^L e^{(y_j-y_i)x}\ell_i\dot A(x)e_j\,dx.
\tag{29}
\]

Since \(y_f-y_\ell=i\kappa_n\) holds exactly, it gives

\[
\frac{\dot T_{f\ell}}{L\nu}
=\Gamma^+_{\ell n}\equiv\ell_f\dot A_ne_\ell,
\qquad
\frac{\dot T_{\ell f}}{L\nu}
=\Gamma^-_{\ell n}\equiv\ell_\ell\dot A_{-n}e_f.
\tag{30}
\]

All other Fourier coefficients are annihilated in these two entries. The diagonal Born entries vanish by \(\dot A_0=0\). This is an exact Fourier selector at the corrected actual centers, not a replacement of the centers by their leading asymptotic values.

Put \(\alpha_\ell=\Gamma^+_{\ell n}\) and \(\beta_\ell=\overline{\Gamma^-_{\ell n}}\). Because (27) imposes reality,

\[
\beta_\ell=\overline{\ell_\ell}\dot A_n\overline{e_f}.
\]

Thus

\[
\mathcal T_n:(A_n,B_n)\longmapsto(\alpha_\ell,\beta_\ell)_{\ell=1}^{m}
\tag{31}
\]

is complex-linear on the arbitrary positive Fourier coefficients. By (28), its leading blocks are

\[
\alpha_\ell=A_ns_\ell+O(n^{-1})\|A_n\|+O(n^{-2})\|B_n\|,
\]

\[
\beta_\ell=t_{M-\ell}B_n+O(n^{-1})\|B_n\|+O(n^{-2})\|A_n\|.
\tag{32}
\]

The map \(A\mapsto(As_\ell)_\ell\) is invertible because the s vectors form a basis. The map \(B\mapsto(t_{M-\ell}B)_\ell\) is invertible because its rows are a permutation of the dual basis. A Neumann-series argument therefore makes \(\mathcal T_n\) an isomorphism for every n>N, with uniformly bounded inverse. Conjugating the negative Born coefficient is essential for this complex-linear statement.

### 8.3 The quadratic actual half-gap and its finite witness

Let \(\gamma_{\ell n}=\partial_\lambda(y_f-y_\ell)(\lambda_{\ell n})\). The exact background block in (23) has \(F_n'(0)=L\gamma_{\ell n}\). The first source off-diagonal block entries at ζ=0 are \(L\Gamma^+\) and \(L\Gamma^-\); the first diagonal entries are zero. Formula (18), or its version with Fₙ, then gives the homogeneous quadratic coefficient of the actual half-gap-squared:

\[
\boxed{\displaystyle
g^{[2]}_{\ell n}(w)=
-\frac{4\Gamma^+_{\ell n}(w)\Gamma^-_{\ell n}(w)}{\gamma_{\ell n}^2}
=-\frac{4\alpha_\ell(w)\overline{\beta_\ell(w)}}{\gamma_{\ell n}^2}.}
\tag{33}
\]

Here Γ denotes the generator coefficients in (30). If Γ instead includes the monodromy Born factor Lν, that factor must be divided out before using (33). The minus sign and the factor four are those of half-gap-squared in the spectral parameter: the leading discriminant equation is \(\gamma^2\zeta^2+4\varepsilon^2\Gamma^+\Gamma^-=0\).

For each selected positive frequency n>N, invert \(\mathcal T_n\) to choose a real tangent witness with \(\alpha_\ell=\beta_\ell=1\) in every slow channel. Also choose real tangent directions with \(\delta\alpha=0\) and \(\delta\beta\) equal to a real or imaginary coordinate unit. Their source preimages are finite Fourier by (25). At the witness,

\[
Dg^{[2]}_{\ell n}(w)[h]
=-\frac4{\gamma_{\ell n}^2}\overline{\delta\beta_\ell}.
\tag{34}
\]

Multiplication by the nonzero complex coefficient in (34), followed by conjugation, is an invertible real two-dimensional map. Hence the real and imaginary parts of the m gap functions have differential rank 2m at this quadratic witness.

For any finite set F of positive frequencies above N, sum the corresponding witnesses and use the selected directions at each frequency. The exact selector (30) makes the quadratic Jacobian block diagonal in n. Its real rank is

\[
d=2m|F|.
\tag{35}
\]

The actual gap map is analytic and starts at degree two at the uniform state. Consequently, for the same fixed directions,

\[
Dg(\varepsilon w)=\varepsilon Dg^{[2]}(w)+O(\varepsilon^2),
\]

and the selected nonlinear real minor satisfies

\[
\Delta_F(\varepsilon w)=
\varepsilon^d\left(C_F+O(\varepsilon)\right),\qquad C_F\ne0.
\tag{36}
\]

Thus every finite high-frequency gap block is independent at some source state arbitrarily close to the uniform state. Source nonlinearities and second-order mean/holonomy corrections do not alter this quadratic coefficient.

### 8.4 Residual independence and the strong-chart qualification

Choose one connected real source ball on which the analytic physical state chart and all the high-frequency two-root extractions are defined. For each finite F, the fixed-direction minor ΔF is a real analytic scalar function on this ball, and (36) shows that it is not identically zero. Its nonzero set is open and dense. The identity principle here can be proved by restricting to real analytic lines in the convex ball: vanishing on an open subset would force vanishing along every line to any other point.

There are countably many finite sets F. Baire's theorem therefore gives a dense residual set of source states on which every finite high-frequency gap block has independent real differentials. Every smaller finite selection of individual channels inherits independence from the full blocks above.

This statement is proved in X₀. To transfer it to a different proposed strong chart \(F_{\rm strong}:U\to X_0\), one needs Fstrong to be analytic at its uniform origin and the range of \(DF_{\rm strong}(0)\) to **contain every finite Fourier source direction used for the witnesses and variations above**. It is not enough to say that the range consists of finite Fourier fields, or to infer this from weak density. Under the stated inclusion, the composite has the same quadratic witnesses; the vanishing of the first gap derivative prevents the second derivative of Fstrong from contributing at quadratic order. The same countable analytic-minor proof then applies on a connected strong-chart ball.

The conclusion concerns independence of finite blocks of real and imaginary gap functions. It does not provide an inverse infinite sequence chart, an action normalization, Poisson commutativity, or spectral completeness.
