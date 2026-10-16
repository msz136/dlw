# Vector AKNS: matched twisted kernels and a common-domain H¹ state inverse

2026-10-11. This continues the [actual framed L² inverse](vector_akns_framed_l2_state_inverse_recovery_proof_20261011.md). It proves a first high-order correction for every fixed finite m=M−1≥1 and general complex constant H, including nonnormal H. All state inverses are local near (a,b,H)=0. The complete argument passed the [independent audit](vector_akns_twisted_h1_state_inverse_independent_audit_20261011.md), including the actual endpoint jets below. No existing or new symbolic checks were run; shared logs were not edited.

## 1. Actual kernels and the correction

Use the same actual system

\[
X_\lambda'=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix}X_\lambda,
\quad X_\lambda(0)=I,\quad N_\lambda=X_\lambda(L),
\quad\lambda_n=2\pi in/L.
\]

The preceding proof constructs L²-valued actual kernels, by convergent odd Dyson paths,

\[
(N_\lambda)_{fs}=\int_0^Le^{\lambda\tau}K_u(\tau)\,d\tau,
\qquad
(N_\lambda)_{sf}=\int_0^Le^{\lambda\tau}K_l(\tau)\,d\tau.
\tag{1}
\]

Their r=0 terms are Kᵤ,₀(τ)=a(L−τ)eᴴ⁽ᴸ⁻τ⁾ and Kₗ,₀(τ)=eᴴ⁽ᴸ⁻τ⁾b(τ). The r≥1 terms have 2r+1 alternating inputs and duration-fiber volume τʳ(L−τ)ʳ/(r!)².

Define the matched kernels

\[
U(\tau)=K_u(\tau)e^{-H(L-\tau)},\qquad
V(\tau)=e^{-H(L-\tau)}K_l(\tau),
\tag{2}
\]

with the indicated right multiplication for the row and left multiplication for the column. Their zeroth paths are exactly a(L−τ) and b(τ), for every complex H. The higher paths are denoted Rᵤ,ᵣ and Rₗ,ᵣ, so

\[
U=a(L-\tau)+R_u,\qquad V=b(\tau)+R_l,
\quad R_u=\sum_{r\ge1}R_{u,r},\ R_l=\sum_{r\ge1}R_{l,r}.
\tag{3}
\]

The matrix exponentials in the original paths are retained in order. Equation (2) cancels the known endpoint twist; it does not commute H through the nonlinear matrix products.

Set C=(N₀)ss−Iₘ and define the matched sample coordinates

\[
\mathscr T(a,b,H)=
\left(\left(\int_0^Le^{\lambda_n\tau}U(\tau)d\tau\right)_n,
\left(\int_0^Le^{\lambda_n\tau}V(\tau)d\tau\right)_n,C\right).
\tag{4}
\]

These are actual framed-data coordinates. From the raw samples one recovers Kᵤ,Kₗ by inverse Fourier transform. The finite matrix H is recovered by the already proved low L² framed inverse; applying (2) then computes (4). Thus the coordinate change is an analytic local function of the complete calibrated raw data. H cannot in general be obtained from the single slow block C alone, because that block also contains coupled a,b paths. The corrected data are not claimed to be conjugacy-invariant spectral actions.

This reparametrization has an explicit sample-space expression. Define the entire matrix coefficients

\[
B_j(H)=\frac1L\int_0^Le^{\lambda_j\tau}e^{-H(L-\tau)}d\tau.
\tag{4a}
\]

If H+λⱼI is invertible, Bⱼ=L⁻¹(H+λⱼI)⁻¹(I−e⁻ᴴᴸ); (4a) supplies the value at every singular or resonant matrix without a resolvent assumption. If yᵤ,ₖ and yₗ,ₖ are the raw upper and lower samples, the corrected sequences are

\[
t_{u,n}=\sum_{k\in\mathbb Z}y_{u,k}B_{n-k}(H),
\qquad t_{l,n}=\sum_{k\in\mathbb Z}B_{n-k}(H)y_{l,k}.
\tag{4b}
\]

These sums mean limits of Fourier truncations in ℓ². They are the Fourier representation of the bounded L² multiplication operators in (2), so their convergence and norm bound follow directly from Parseval and ‖e⁻ᴴ⁽ᴸ⁻τ⁾‖≤eᴸ‖ᴴ‖. They require no ℓ¹ claim for the coefficients Bⱼ. Matrix order in the two convolutions is essential. At H=0, Bⱼ=δⱼ₀I, as expected.

## 2. Exact endpoint matching

Suppose a,b∈H¹(0,L). They have continuous representatives. For each r≥1, the path product is bounded on the compact duration simplex, and its conditional integral has norm at most a fixed product of sup norms times τʳ(L−τ)ʳ/(r!)². Therefore every higher path vanishes at τ=0,L. The series converges uniformly for H¹-bounded inputs, by these factorial bounds, so Rᵤ(0)=Rᵤ(L)=Rₗ(0)=Rₗ(L)=0.

Consequently the raw kernel endpoints are exactly

\[
K_u(0)=a(L)e^{HL},\quad K_u(L)=a(0),
\qquad K_l(0)=e^{HL}b(0),\quad K_l(L)=b(L).
\tag{5}
\]

Once the H¹ estimate below is established, integration by parts at n≠0 gives the exact leading raw sample tails

\[
(N_{\lambda_n})_{fs}
=\frac{a(0)-a(L)e^{HL}}{\lambda_n}+o(|n|^{-1}),
\qquad
(N_{\lambda_n})_{sf}
=\frac{b(L)-e^{HL}b(0)}{\lambda_n}+o(|n|^{-1}).
\tag{5a}
\]

The remainder is −λₙ⁻¹ times the corresponding Fourier coefficient of the L² kernel derivative, which tends to zero. For periodic inputs the numerators are a(0)(I−eᴴᴸ) and (I−eᴴᴸ)b(0). If either numerator is nonzero, the corresponding raw sequence is not in h¹. General complex H gives exactly this endpoint mismatch; no diagonalization is involved. A simple constant-potential upper example is b=0, a constant, for which the raw value is a(eᴴᴸ−I)(H−λₙI)⁻¹ whenever the resolvent exists. Equation (5a) also applies at resonant H where that resolvent expression must be interpreted by its entire integral.

After (2), U(0)=a(L), U(L)=a(0), V(0)=b(0), V(L)=b(L). Hence periodic H¹ potentials give exactly periodic H¹ corrected kernels once their H¹ regularity is proved below. Formula (5) uses actual path sums, not formal spectral asymptotics.

## 3. A tame H¹ estimate for the nonlinear kernel

Let R=‖a‖₂+‖b‖₂ and Z=‖a‖H¹+‖b‖H¹. For every fixed upper bound h* on ‖H‖, there is a constant depending on L,h* such that

\[
\boxed{\quad
\|(R_u,R_l)\|_{H^1\oplus H^1}
\le C_{L,h_*}R^2e^{C_LR^2}Z.
\quad}
\tag{6}
\]

No small H¹ norm is used in this estimate. The small coefficient is the squared low L² norm. Finite m only affects equivalent choices of the finite block norms.

Here is the actual kernel proof. Parameterize the r+1 fast interval lengths by τxⱼ and the r+1 slow lengths by (L−τ)yⱼ, where x and y lie in their unit r-simplexes and each group's fractions sum to 1. The path kernel is

\[
\tau^r(L-\tau)^r\int_{\Delta_r(1)\times\Delta_r(1)}
P_H(t(\tau,x,y))\,dx\,dy,
\tag{7}
\]

followed by the left or right exponential in (2). Every transition time is affine in τ with derivative in [−1,1]. The derivative of each slow interval is −yⱼ, and the sum of their absolute derivatives is 1.

Differentiating (7) for initially smooth inputs has three contributions:

1. A derivative of one input cⱼ, multiplied by a coefficient of modulus at most 1.
2. Derivatives of the slow H-exponentials and the final correction. Their sum is bounded by 2‖H‖ times e²ᴸ‖ᴴ‖ times the undifferentiated input product.
3. The Jacobian derivative r(1/τ−1/(L−τ))Rᵣ.

The coarea L² estimate from the preceding proof applies to the first two contributions, including bounded coefficients. It gives

\[
e^{2L\|H\|}\frac{(L/2)^r}{r!}
\left[\sum_j\|c_j'\|_2\prod_{k\ne j}\|c_k\|_2
+2\|H\|\prod_j\|c_j\|_2\right].
\tag{8}
\]

For r≥2, Cauchy–Schwarz on a duration fiber and its exact volume give

\[
\|R_r/\tau\|_2,\ \|R_r/(L-\tau)\|_2
\le e^{2L\|H\|}\frac{L^{r-1}}{r!}\prod_j\|c_j\|_2.
\tag{9}
\]

Indeed the squared coefficient is bounded by sup τʳ⁻²(L−τ)ʳ/(r!)² or its reflection, at most L²ʳ⁻²/(r!)². Multiplying the two estimates by r bounds the Jacobian contribution by 2e²ᴸ‖ᴴ‖Lʳ⁻¹∏‖cⱼ‖₂/(r−1)!.

The remaining r=1 case cannot use (9), because a factor τ⁻¹ occurs. It instead has a direct two-variable estimate. Put σ=L−τ. The upper path is exactly

\[
K_{u,1}(\tau)=\int_0^\tau\int_0^\sigma
a(\sigma+s)e^{H(\sigma-t)}b(t+s)a(t)e^{Ht}\,dt\,ds.
\tag{10}
\]

The product of the original exponentials and the correction has norm at most e²ᴸ‖ᴴ‖. Dividing by τ, use |a(σ+s)|≤‖a‖∞ and Cauchy–Schwarz on the t-integral; dividing by σ, use |a(t)|≤‖a‖∞ and Cauchy–Schwarz on the s-integral. Both give the uniform pointwise bound e²ᴸ‖ᴴ‖‖a‖∞‖a‖₂‖b‖₂. Therefore

\[
\|R_{u,1}/\tau\|_2,\ \|R_{u,1}/\sigma\|_2
\le\sqrt L e^{2L\|H\|}\|a\|_\infty\|a\|_2\|b\|_2.
\tag{11}
\]

The lower path has the ordered formula

\[
K_{l,1}(\tau)=\int_0^\tau\int_0^\sigma
e^{H(\sigma-s)}b(\tau+s)a(t+s)e^{Hs}b(t)\,ds\,dt.
\]

The same argument gives (11) with ‖b‖∞ in place of ‖a‖∞. The one-dimensional trace embedding bounds these sup norms by C_LZ.

Combining (8)–(11) with the zeroth-derivative kernel bound and summing the factorial series proves (6): each differentiated-input term is at most (2r+1)R²ʳZ times its displayed factorial coefficient, and each undifferentiated product is at most R²ʳZ. The r=1 Jacobian term is at most C_LR²Z. All r≥2 Jacobian terms sum to at most C_LR²eᶜᴸᴿ²Z.

Approximate H¹ inputs by smooth inputs. The bounds apply to the multilinear differences as well; each finite path converges in H¹, and the factorial tails converge uniformly on H¹-bounded sets. The L² kernel limit is the already proved actual Dyson kernel, so these H¹ derivatives are its weak derivatives. This establishes (6) without assuming pointwise derivatives of L² potentials.

The same bounded multilinear construction and H-exponential dependence show that (3) is holomorphic H¹⊕H¹⊕Matₘ(C)→H¹⊕H¹ on all bounded H¹ sets. For periodic inputs the endpoint identities place its values in H¹per⊕H¹per, a closed complex subspace.

## 4. A single low domain and actual inverse regularity

Write X₀=L²per(row)⊕L²per(column)⊕Matₘ(C), and X₁=H¹per(row)⊕H¹per(column)⊕Matₘ(C). Temporarily use kernel targets Y₀=L²per(row)⊕L²per(column)⊕Matₘ(C) and Y₁=H¹per(row)⊕H¹per(column)⊕Matₘ(C); a low L² element needs no endpoint condition.

The kernel map Φ(a,b,H)=(U,V,C) is entire X₀→Y₀. Its vacuum derivative is the isomorphism

\[
L_0(\alpha,\beta,K)=(\alpha(L-\tau),\beta(\tau),LK).
\tag{12}
\]

Let N=Φ−L₀. The pair part of N is (Rᵤ,Rₗ). The finite matrix part C−LH has vanishing constant and linear terms, by the actual Volterra expansion, and obeys an ordinary low-norm quadratic estimate on a fixed small ball.

Choose one X₀ ball of radius ε inside the previously proved raw framed inverse neighborhood, with ‖L₀⁻¹DN‖X₀→X₀≤1/2 there. Shrink ε further once so that (6) and the finite matrix quadratic estimate give

\[
\|L_0^{-1}N(z)\|_{X_1}\le q_1(\varepsilon)\|z\|_{X_1},
\qquad q_1(\varepsilon)<1/2,
\quad z\in X_1,\ \|z\|_{X_0}\le\varepsilon.
\tag{13}
\]

For the pair the coefficient is O(ε²). For the finite part, its O(‖z‖X₀²) bound is at most Cε‖z‖X₁. Thus (13) uses one low ball and allows arbitrarily large finite H¹ norm.

Choose a sufficiently small open Y₀ ball V₀ so that the low fixed-point iteration

\[
z_0=0,\qquad z_{k+1}=L_0^{-1}\bigl(y-N(z_k)\bigr)
\tag{14}
\]

stays in that X₀ ball and is a contraction there. This is the actual low analytic inverse supplied by the Banach inverse theorem, restricted to a common ball. If y∈V₀∩Y₁, the exact endpoint matching and H¹ holomorphy imply that every iterate belongs to X₁. Equation (13) gives

\[
\|z_{k+1}\|_{X_1}
\le C_L\|y\|_{Y_1}+q_1\|z_k\|_{X_1},
\quad
\sup_k\|z_k\|_{X_1}\le\frac{C_L}{1-q_1}\|y\|_{Y_1}.
\tag{15}
\]

The X₀ limit is the unique low inverse z. Bounded H¹ sequences have weakly convergent subsequences; continuous inclusion into L² identifies any weak X₁ limit with z. Periodic H¹ is weakly closed. Therefore z∈X₁, with the same bound (15). This proves actual high inverse regularity on the entire intersection V₀∩Y₁, rather than only a second high-norm-small IFT neighborhood.

The inverse is also holomorphic Y₁→X₁ on that intersection. To see this directly, it is holomorphic into X₀, has range X₁, and is locally bounded in X₁ by (15). Along a complex line in Y₁, approximate any X₁-dual functional in dual norm by L² test functionals and finite matrix functionals. Uniform local X₁ bounds make the scalar approximations converge uniformly; the limit is holomorphic. Weak holomorphy and local boundedness give Banach-valued holomorphy. Equivalently the one-variable Cauchy coefficients lift into X₁ with the same Cauchy bounds, followed by the usual locally bounded line-holomorphy criterion.

Let κ:V₀→X₀ denote this unique inverse branch in the chosen low ball, and set U₀=κ(V₀). This is the local preimage inside that ball, without a claim about possible preimages outside it. It establishes restrictions of one actual low chart:

\[
\boxed{
\Phi:U_0\cap X_1\longleftrightarrow V_0\cap Y_1
\quad\text{is biholomorphic,}
}
\tag{16}
\]

as is Φ:U₀↔V₀ on the L² level. No H¹-dependent source radius was used in (16).

## 5. Weighted Fourier state coordinates and physical calibration

For a periodic H¹ vector function f, the sequence (∫₀ᴸeλₙτf(τ)dτ)ₙ lies in h¹, and conversely h¹ reconstructs exactly a periodic H¹ function by Fourier inversion. Parseval identifies the h¹ norm, up to fixed L-dependent constants, with the periodic H¹ norm. Combining this isomorphism with (16) proves

\[
\boxed{
\mathscr T:
U_0\cap(H^1_{\rm per}\oplus H^1_{\rm per}\oplus\operatorname{Mat}_m)
\longleftrightarrow
\mathscr V_0\cap(h^1\oplus h^1\oplus\operatorname{Mat}_m),
}
\tag{17}
\]

where 𝒱₀ is the image of the same low V₀ under the L² Fourier isomorphism. The vacuum sample derivative is ((Lα̂ₙ)ₙ,(Lβ̂₋ₙ)ₙ,LK), with the conventions of the preceding proof. General complex H remains a genuine finite variable; no diagonalization, real slice, commutativity, or spectral separation of its eigenvalues is assumed.

One may use the corrected kernels as an explicit analytic reparametrization of the raw calibrated data: raw inverse Fourier samples give Kᵤ,Kₗ, the actual low inverse gives H, and (2) followed by Fourier transform gives 𝒯. Both raw and corrected low maps are local analytic isomorphisms. The high result is the additional regularity statement (16)–(17), proved by the actual kernel estimate and iteration.

If the vector AKNS frame comes from original DLW through T(x),G(x), the endpoint relation still includes G(0)⁻¹T(0)⁻¹NχT(0)G(0), together with its specified determinant normalization. This correction does not supply an absent endpoint calibration and does not turn conjugacy classes into full framed samples. It is a weighted full-potential state-coordinate result; transferring it to an original physical image and proving action/norming completeness remain separate.

## 6. The correction stops at H¹ without additional jet subtraction

Even H=0 does not make all higher endpoint derivatives periodic. For m=1 and nonzero constant a,b, the actual duration kernels have the exact series

\[
K_u(\tau)=a\sum_{r\ge0}
\frac{(ab)^r\tau^r(L-\tau)^r}{(r!)^2}.
\tag{18}
\]

At H=0 the correction (2) does nothing. The r=1 term, and only that term, contributes to the endpoint derivative:

\[
K_u'(0)=La^2b,\qquad K_u'(L)=-La^2b.
\tag{19}
\]

Thus the corrected kernel has equal values but a nonzero derivative jump. Integrating its Fourier coefficient twice by parts gives a nonzero 1/n² leading tail; the smooth remainder is of higher order. Such a sequence belongs to h¹ and fails to belong to h². Hence (17) cannot be promoted to all Hᴺ/hᴺ by the same twist alone.

The first nonlinear derivative jump can also be computed explicitly for general complex H. Take C² periodic a,b, put a₀=a(0)=a(L), b₀=b(0)=b(L), and define the actual integrals

\[
c=\int_0^L a(t)b(t)\,dt\in\mathbb C,
\qquad Q_H=\int_0^L e^{-Ht}b(t)a(t)e^{Ht}\,dt
\in\operatorname{Mat}_m(\mathbb C).
\tag{20}
\]

The r≥2 paths have zero first derivative at both endpoints: their factors τʳ(L−τ)ʳ and the uniformly convergent differentiated duration formulas show this directly. The r=0 terms are reflection a and b, with equal endpoint derivatives because the source is periodic. From the two ordered r=1 formulas in §3 one obtains

\[
R_{u,1}'(0)=a_0e^{HL}Q_He^{-HL},
\quad R_{u,1}'(L)=-ca_0,
\qquad
R_{l,1}'(0)=Q_Hb_0,
\quad R_{l,1}'(L)=-cb_0.
\tag{21}
\]

For example, divide (10) by τ and let τ↓0; its s-average fixes the first row input at a(L), while the t-integral remains, yielding the first formula after the right correction. Dividing by σ and letting σ↓0 gives (∫ab)a(0). The lower formulas follow from its displayed ordered integral in exactly the two analogous limits. Multiplying by the correction contributes no endpoint term because Rᵣ itself vanishes there. Consequently

\[
D_u:=U'(L)-U'(0)=-ca_0-a_0e^{HL}Q_He^{-HL},
\qquad
D_v:=V'(L)-V'(0)=-cb_0-Q_Hb_0.
\tag{22}
\]

These identities retain general matrix conjugation and do not replace Qᴴ by a commuting scalar. For C² inputs, differentiation of the smooth affine-duration formulas twice gives C² kernels by uniform factorial bounds; a second integration by parts yields corrected leading tails −Dᵤ/λₙ²+o(n⁻²) and −Dᵥ/λₙ²+o(n⁻²).

There is therefore an explicit first jet subtraction on smooth inputs. Let B₂(s)=s²−s+1/6, whose endpoint values agree and whose derivative difference on [0,L] is 2/L, and put

\[
U^{[2]}(\tau)=U(\tau)-\frac L2D_uB_2(\tau/L),
\qquad
V^{[2]}(\tau)=V(\tau)-\frac L2D_vB_2(\tau/L).
\tag{23}
\]

Their values and first derivatives match at both endpoints; C² inputs thus give periodic H² kernels and h² samples after this true jet subtraction. This is a forward smooth-input statement. It is not yet an H² state inverse on the same low L² domain: the coefficients (22) involve point traces a₀,b₀, which are not defined as continuous functionals on L², so (23) is not a demonstrated low-L² analytic reparametrization. An inverse/compatibility argument and higher actual jet subtractions would still have to be supplied. No all-N endpoint-jet construction or inverse theorem is asserted here.

The completed result is a general finite-M actual H¹/h¹ framed state inverse on restrictions of one low domain. The next high-order step is the computation and subtraction of actual endpoint jets; the original general-M class/action Hamilton completeness problem remains open.
