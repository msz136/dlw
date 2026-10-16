# Actual vector AKNS framed monodromy: a local L² state inverse

2026-10-11. Independent proof for each fixed finite m=M−1≥1. The result concerns calibrated full monodromy in a fixed fast/slow frame. It gives a low-order L²↔ℓ² analytic state inverse near the zero potential. It does not give an inverse from conjugacy-invariant Floquet classes, spectral actions, or raw weighted high-order samples. No existing or new symbolic checks were executed.

## 1. Statement and normalization

Fix L>0. The independent unknowns are

\[
a\in L^2(0,L;\mathbb C^{1\times m}),\quad
b\in L^2(0,L;\mathbb C^{m\times1}),\quad
H\in\operatorname{Mat}_m(\mathbb C),
\]

with H constant in x. Put

\[
\mathcal A_\lambda(x)=
\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\quad X_\lambda'=\mathcal A_\lambda X_\lambda,
\quad X_\lambda(0)=I_{m+1},\quad
N_\lambda=X_\lambda(L).
\tag{1}
\]

This N is the actual full fundamental monodromy of (1), without determinant normalization. In particular det Nλ=exp(Lλ+L tr H). Periodic L² potentials can be identified with their restrictions to (0,L); no endpoint value of a or b is needed to define (1).

Let λₙ=2πin/L, n∈Z. In the prescribed frame define

\[
\mathscr D(a,b,H)=
\left(\bigl((N_{\lambda_n})_{fs}\bigr)_{n\in\mathbb Z},
\bigl((N_{\lambda_n})_{sf}\bigr)_{n\in\mathbb Z},
(N_0)_{ss}-I_m\right).
\tag{2}
\]

The letters f,s denote the one-dimensional fast block and m-dimensional slow block. The target is

\[
\mathcal Y=
\ell^2(\mathbb Z;\mathbb C^{1\times m})
\oplus\ell^2(\mathbb Z;\mathbb C^{m\times1})
\oplus\operatorname{Mat}_m(\mathbb C).
\]

Then D is an entire holomorphic map from the Banach space
X=L²(row)⊕L²(column)⊕Matₘ(C) to Y. There are neighborhoods U of (0,0,0) in X and V of 0 in Y such that D:U→V is biholomorphic. Thus these actual framed samples recover a,b and H uniquely and analytically on a full local L² state neighborhood.

Use Euclidean norms for rows and columns, the operator norm for H in exponential bounds, and any fixed matrix norm, for instance Frobenius, on the finite-dimensional third factor. The proof does not diagonalize H and includes nonnormal complex H. All assertions concern fixed finite m; no uniform M→∞ neighborhood is claimed.

## 2. The actual ODE and its Dyson expansion

Set Eλ,H(t)=diag(eλt,eHt) and B(x)=[[0,a(x)],[b(x),0]]. Since a,b∈L²⊂L¹, the matrix ODE has its unique absolutely continuous fundamental matrix. Variation of constants gives the actual convergent expansion

\[
N_\lambda=E_{\lambda,H}(L)
+\sum_{k\ge1}\int_{0<t_1<\cdots<t_k<L}
E(L-t_k)B(t_k)E(t_k-t_{k-1})\cdots B(t_1)E(t_1)
\,dt_1\cdots dt_k.
\tag{3}
\]

For λ,H in a fixed bounded set, a term has norm bounded by a fixed diagonal-exponential factor times (∫₀ᴸ‖B‖dx)ᵏ/k!. The product of diagonal-exponential norms is bounded by exp[L max(Re λ,‖H‖)] because all nonnegative interval lengths sum to L. Consequently (3) converges absolutely, uniformly in the endpoint and on bounded parameter sets. It is the Volterra solution, not a formal expansion.

Every offdiagonal block comes from an odd path k=2r+1. On an upper-row path, the odd transitions use a and the even transitions use b. On a lower-column path, the odd transitions use b and the even transitions use a. Keeping the ordered H-exponentials is essential; they need not commute with a,b or with their intervening products.

Nevertheless the fast propagation is scalar, so all its factors combine exactly to eλτ, where τ is the total time spent in the fast state. For the upper and lower paths respectively,

\[
\tau_u=L-t_{2r+1}+\sum_{j=1}^r(t_{2j}-t_{2j-1}),
\]
\[
\tau_l=t_1+\sum_{j=1}^r(t_{2j+1}-t_{2j}),
\qquad 0\le\tau_u,\tau_l\le L.
\tag{4}
\]

The remaining ordered matrix product P_H(t) has norm at most

\[
\|P_H(t)\|\le e^{(L-\tau)\|H\|}
\prod_{j=1}^{2r+1}\|c_j(t_j)\|
\le e^{L\|H\|}\prod_j\|c_j(t_j)\|,
\tag{5}
\]

where cⱼ alternates between the appropriate row and column inputs.

## 3. Exact duration disintegration and the L² kernel bound

Let Δ₂ᵣ₊₁={0<t₁<⋯<t₂ᵣ₊₁<L}. Introduce the nonnegative interval lengths d₀=t₁, dⱼ=tⱼ₊₁−tⱼ for 1≤j≤2r, and d₂ᵣ₊₁=L−t₂ᵣ₊₁. Their sum is L; the t-to-free-d transformation has unit determinant. There are r+1 fast intervals and r+1 slow intervals, irrespective of which offdiagonal path is chosen.

Disintegration of ordinary Lebesgue dt by τ in (4) has conditional measures ντ with total mass

\[
V_r(\tau)=\frac{\tau^r(L-\tau)^r}{(r!)^2}.
\tag{6}
\]

An explicit check, avoiding normalization ambiguity in the coarea measure, is

\[
\int_{\Delta_{2r+1}} f(\tau(t))\,dt
=\int_0^L f(\tau)
\frac{\tau^r(L-\tau)^r}{(r!)^2}\,d\tau.
\tag{7}
\]

Indeed, fix the sum of the r+1 fast d's to τ and the sum of the r+1 slow d's to L−τ; eliminating one interval in each group leaves two ordinary r-simplexes of volumes τʳ/r! and (L−τ)ʳ/r!. Permuting the d-coordinates and choosing the eliminated interval does not change the unit Jacobian. Equivalently ντ is Hausdorff fiber measure divided by ‖∇τ‖=√(2r+1) in t-coordinates. The measure in (6) already includes this coarea factor.

Define the vector-valued path kernel, almost everywhere in τ, by

\[
K_r(\tau)=\int_{\tau(t)=\tau}P_H(t)\,d\nu_\tau(t).
\tag{8}
\]

Cauchy–Schwarz on the finite-measure fiber, followed by (5), gives

\[
\|K_r(\tau)\|^2
\le e^{2L\|H\|}V_r(\tau)
\int_{\tau(t)=\tau}\prod_j\|c_j(t_j)\|^2\,d\nu_\tau(t).
\]

Integrate in τ, use sup Vᵣ=(L/2)²ʳ/(r!)², and enlarge the ordered simplex to the full cube:

\[
\boxed{\quad
\|K_r\|_{L^2(0,L)}
\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\prod_{j=1}^{2r+1}\|c_j\|_{L^2(0,L)}.
\quad}
\tag{9}
\]

This argument is valid for independent L² row/column inputs before identifying repeated copies. It makes no pointwise boundedness assumption. For r=0, ντ has mass 1, and the kernels are explicitly

\[
K_{u,0}(\tau)=a(L-\tau)e^{H(L-\tau)},\qquad
K_{l,0}(\tau)=e^{H(L-\tau)}b(\tau).
\tag{10}
\]

The matrix product in (8) is retained in its true order. Estimate (9) uses only submultiplicativity of the Euclidean/operator norms; no commuting-H or scalar-slow assumption is present.

## 4. Holomorphic kernel sums equal the actual monodromy

Applying (9) to the repeated inputs yields

\[
\|K_{u,r}\|_2\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\|a\|_2^{r+1}\|b\|_2^r,
\]
\[
\|K_{l,r}\|_2\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\|b\|_2^{r+1}\|a\|_2^r.
\tag{11}
\]

Therefore Kᵤ=∑rKᵤ,ᵣ and Kₗ=∑rKₗ,ᵣ converge absolutely in L², uniformly on bounded subsets of X, with bounds

\[
\|K_u\|_2\le e^{L\|H\|+(L/2)\|a\|_2\|b\|_2}\|a\|_2,
\quad
\|K_l\|_2\le e^{L\|H\|+(L/2)\|a\|_2\|b\|_2}\|b\|_2.
\tag{12}
\]

For each r, the path-product map of its independent L² inputs is bounded multilinear into L²(Δ₂ᵣ₊₁). Its H dependence is entire: eHt is an entire matrix function uniformly for 0≤t≤L, and the finite ordered products are holomorphic as bounded multiplier maps on the simplex. The fiber integration operator L²(Δ₂ᵣ₊₁)→L²(0,L) is continuous with the norm estimate in §3. Thus Kᵤ,ᵣ and Kₗ,ᵣ are jointly holomorphic L²-valued maps. Normal convergence in (11) proves that their sums are entire holomorphic X→L².

For each fixed λ, disintegration and Fubini give the odd Dyson term as ∫₀ᴸeλτKᵣ(τ)dτ. This bounded functional of Kᵣ can be interchanged with the absolutely convergent L² sum. Comparing with the already convergent actual Dyson expansion (3) proves the exact identities

\[
\boxed{(N_\lambda)_{fs}=\int_0^L e^{\lambda\tau}K_u(\tau)\,d\tau,
\qquad
(N_\lambda)_{sf}=\int_0^L e^{\lambda\tau}K_l(\tau)\,d\tau.}
\tag{13}
\]

This proves both the series-to-kernel equality and its equality to actual ODE monodromy for every λ. It is not an identification based only on formal coefficients.

## 5. Fourier samples, derivative and the analytic inverse

Use the Fourier convention

\[
\widehat f_n=\frac1L\int_0^L e^{-2\pi inx/L}f(x)\,dx.
\tag{14}
\]

For any finite-vector-valued K∈L², Parseval gives

\[
\left(\int_0^L e^{\lambda_n\tau}K(\tau)\,d\tau\right)_n
=(L\widehat K_{-n})_n,\qquad
\sum_n\left\|\int_0^L e^{\lambda_n\tau}K\right\|^2
=L\|K\|_2^2.
\tag{15}
\]

Hence the two offdiagonal sequences in (2) are genuinely ℓ², and are entire holomorphic by (12)–(15). The finite third component (N₀)ss−I is entire holomorphic by the actual Volterra expansion at λ=0, or by the L¹ Banach ODE dependence. Thus D:X→Y is entire.

At a=b=H=0 the first terms of (13) give, using eλₙL=1,

\[
D\mathscr D(0)[\alpha,\beta,K]
=\left((L\widehat\alpha_n)_n,
(L\widehat\beta_{-n})_n,LK\right).
\tag{16}
\]

There is no first-order offdiagonal contribution of K, and no first-order a or b contribution to the slow diagonal block. Formula (16) is a bounded complex Banach-space isomorphism: its inverse takes upper Fourier coefficients yᵤ,ₙ/L, lower Fourier coefficients yₗ,₋ₙ/L, and H=C/L. In L² notation,

\[
\alpha(x)=\frac1L\sum_{n\in\mathbb Z}y_{u,n}e^{2\pi inx/L},
\quad
\beta(x)=\frac1L\sum_{n\in\mathbb Z}y_{l,n}e^{-2\pi inx/L},
\quad K=C/L.
\tag{17}
\]

These Fourier series converge in L². Their norms are controlled by the ℓ² data with factor L⁻¹/², and the matrix inverse has factor L⁻¹. The complex analytic Banach inverse function theorem applied to (16) proves the local biholomorphic inverse stated in §1. The target neighborhood is an actual open product neighborhood in Y, not a conjectural image determined by formal compatibility constraints.

For real a,b,H, conjugation gives N̄λ=Nbarλ and λbarₙ=λ₋ₙ. Thus the real data satisfy yᵤ,₋ₙ=overline(yᵤ,ₙ), yₗ,₋ₙ=overline(yₗ,ₙ), and C real. Uniqueness of the inverse shows that this real fixed set recovers exactly the real source locally. This statement uses the fixed prescribed frame.

## 6. Determinant normalization and endpoint calibration

If one replaces (1) by its trace-free normalized monodromy

\[
\widetilde N_\lambda=e^{-L(\lambda+\operatorname{tr}H)/(m+1)}N_\lambda,
\]

then the data and their vacuum derivative must also change. The offdiagonal derivative acquires the fixed nonzero phase e⁻²πⁱⁿ⁄⁽ᵐ⁺¹⁾. The slow-zero derivative is

\[
L\left(K-\frac{\operatorname{tr}K}{m+1}I_m\right),
\tag{18}
\]

not LK. It is still an isomorphism on Matₘ(C), since its trace is L tr K/(m+1), and its inverse is explicit. Consequently an analogous normalized framed inverse also follows, after this precise adjustment. One must not identify the raw and normalized derivative formulas.

When a vector AKNS connection is obtained from original DLW variables by a periodic split T(x) and periodic gauge G(x), the actual original monodromy is related by the endpoint factors. Schematically, with the scalar normalization specified separately,

\[
N_{\rm AKNS}=G(0)^{-1}T(0)^{-1}N_\chi T(0)G(0).
\tag{19}
\]

The data (2) are the entries in that calibrated AKNS frame. Conjugacy-invariant traces or branch points discard (19) and do not supply them. The inverse theorem does not remove or determine an unknown endpoint calibration by itself. Passing from this full potential inverse to the original physical source requires an independently proved physical-image constraint and inverse; that is outside this note.

## 7. Why raw high-order weights and Liouville conclusions remain separate

Raw samples need not preserve high Sobolev weights even for smooth periodic coefficients. Already for m=1, a(x)=a₀≠0, b=0, H=h₀≠0 small and constant,

\[
(N_{\lambda_n})_{fs}
=a_0\frac{e^{h_0L}-1}{h_0-\lambda_n}.
\tag{20}
\]

When eʰ⁰ᴸ≠1 this has a nonzero 1/n tail. It belongs to ℓ² but not h¹, although a,b are C∞ periodic. Thus the low theorem cannot be upgraded by the same raw sample map to Hᴺ↔hᴺ for N≥1. Endpoint/asymptotic subtraction or a different spectral coordinate construction would have to be proved first.

The established new result is the actual framed low-L² state inverse for every fixed finite M. It does not prove action-only discrimination, class-function state coordinates, action/norming Poisson formulas, weighted physical inverse coordinates, or general-M Hamilton closed-span maximality. Those remain additional dependencies of the original general-field DLW Liouville goal.
