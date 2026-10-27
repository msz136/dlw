# Analytic candidates with exact finite-grid zeros

2026-10-26. Extension of the independent residual audit. Analyticity of each approximate field, by itself, does not remove the counterexample. A **uniform quantitative analytic norm or tail restriction** would be additional information and is outside the statement proved here.

## 1. Entire transverse profiles and rigorous normalization

Fix the transverse interval `[0,Z]`, a finite set `S` containing every sampled transverse coordinate and both endpoints, and an interior point `z*∉S`. Choose any small observation interval `J` around `z*` avoiding `S`. Put

\[
P(z)=\prod_{a\in S}(z-a)^2,\quad
Q(z)=P(z)/P(z_*),\quad
F_\delta(z)=\delta Q(z)e^{-((z-z_*)/\delta)^2},\quad
C_\delta=\|F_\delta'\|_{L^\infty(0,Z)}.
\]

Every `Fδ` is entire in `z`. Both `Fδ` and `Fδ'` vanish exactly at every `a∈S`. Define the fixed finite constants `Q0=||Q||∞`, `Q1=||Q'||∞` on `[0,Z]`, and set `s=(z−z*)/δ`. Then

\[
F_\delta'(z)=\bigl[\delta Q'(z)-2sQ(z)\bigr]e^{-s^2}.
\]

The mean-value estimate `|Q(z)−1|≤δQ1|s|` implies the **uniform real-interval bound**

\[
\bigl|F_\delta'(z)+2s e^{-s^2}\bigr|
\le\delta Q_1(1+2s^2)e^{-s^2}
\le E\delta,\quad E=Q_1(1+2/e).
\]

Once `δ` is small enough that `z*±δ/√2∈[0,Z]`, the reference profile `−2s e^-s²` has maximum absolute value `C0=√(2/e)` on that interval. Hence

\[
|C_\delta-C_0|\le E\delta,
\qquad C_\delta\ge C_0/2>0
\]

for sufficiently small `δ`. In particular, `Cδ→√(2/e)` is a proved uniform limit, rather than only a fixed-`s` formal expansion.

Let `gδ=Fδ/Cδ`. Then

\[
\|g_\delta'\|_\infty=1,\quad
\|g_\delta\|_\infty\le c_1\delta,\quad
\|g_\delta g_\delta'\|_\infty\le c_1\delta,
\quad c_1=2Q_0/C_0.
\]

The corresponding weighted derivative estimate, needed for a nonzero background, is

\[
\|(z-z_*)g_\delta'\|_\infty\le c_2\delta,
\quad
c_2=\frac2{C_0}\left(\frac{Q_1}{\sqrt{2e}}+\frac{2Q_0}{e}\right)
\]

for `δ≤1` and `Cδ≥C0/2`. This follows from `sup|s|e^-s²=1/√(2e)` and `sup s²e^-s²=1/e`.

The maximum of `|gδ'|` lies in `J` for sufficiently small `δ`: outside `J`, `|s|≥dist(z*,Jᶜ)/δ`, so the displayed derivative expression tends uniformly to zero; inside `J` its supremum tends to `C0` before normalization. Consequently the normalized derivative has maximum exactly one within the requested observation interval.

## 2. Fully analytic constant-background construction

At the exact continuous target `(U,V)=(0,4)`, take a period-compatible `k=2πn/L` and

\[
h_k(t)=\frac{e^{k^2t}-1}{e^{k^2T}-1},\quad
u_{\rm app}=M g_\delta(z)h_k(t)\cos(kX),\quad
v_{\rm app}=4+M g_\delta'(z)h_k(t)\cos(kX).
\]

These fields are entire in `(X,z,t)`. Their complete initial functions are exactly `(0,4)`; both physical fields agree exactly with the target at every prescribed transverse sample coordinate and both boundaries, at every time. At `t=T`, the maximum `v` error is exactly `M`, including in `J` for small `δ`.

The full nonlinear residuals coincide exactly:

\[
\mathcal R_1=\mathcal R_2
=M g_\delta'(h_k'-k^2h_k)\cos(kX)
-M^2k g_\delta g_\delta' h_k^2\sin(2kX).
\]

Thus

\[
\max_i\|\mathcal R_i\|_\infty
\le\frac{Mk^2}{e^{k^2T}-1}+M^2kc_1\delta.
\]

For any `r>0,M>0`, first choose `n` sufficiently large that the first term is less than `r/2`, and then choose `δ` small enough to satisfy the normalization/interior conditions and `M²kc1δ<r/2`. Alternatively, `δ=e^-k²T` works for all sufficiently large `n`. No compactly supported nonanalytic bump is used.

This proves the same arbitrary-error/small-full-residual obstruction even among candidates individually analytic in every variable.

## 3. Extension of the conditional nonzero-background theorem

Use the scalar terminal transport-diffusion profile `φ_n(X,t)` and smooth time cutoff `χ` from `INDEPENDENT_NO_GO_AUDIT.md`, and set

\[
d_n=M g_\delta(z)\chi(t)\phi_n(X,t),\qquad
e_n=M g_\delta'(z)\chi(t)\phi_n(X,t).
\]

The perturbations are entire in `z`, preserve the exact initial fields, and vanish in both physical components at every finite sample coordinate and endpoint. They are not zero in an open neighborhood of those transverse lines, so that stronger support claim from the compact-bump version is deliberately omitted.

Writing `α_n=sup_{t≤T/2}||φ_n(t)||∞→0`, `C=||φ_n||∞` uniformly bounded and `W_n=||φ_{n,X}||∞<∞`, the exact nonlinear subtraction gives

\[
\max_i\|\Delta\mathcal R_i\|_\infty
\le M\|\chi'\|_\infty\alpha_n+M\delta\widetilde K_n(M),
\]

\[
\widetilde K_n(M)
=c_2(QC+PW_n)
+\frac{c_1}{2}\bigl[(N_a+N_b)C+(M_a+M_b+8)W_n\bigr]
+2Mc_1CW_n.
\]

Here `P,Q,Ma,Mb,Na,Nb` denote the background constants in the independent audit; the polynomial `Q(z)` is unrelated to that scalar background constant `Q=||U_Xz||∞`. The first term in `K̃` uses the new weighted estimate `||(z−z*)gδ'||≤c2δ`, replacing compact support. The final term retains the entire quadratic product.

Choose `n` first so that the cutoff term is less than `r/2`, then choose `δ<r/[2M(1+K̃_n(M))]`, as well as the earlier profile conditions. This proves the full residual bound. If the target itself is analytic in `z`, so is the resulting candidate. For a merely smooth target, it is the added perturbation that is entire; the candidate inherits the target's regularity.

The time cutoff in this general-background version is smooth, not analytic. The all-variable analytic claim belongs to the explicit constant-background construction above. No analyticity in time of a general background has been assumed.

## 4. Finite derivative observations and the exact limitation

If a validator observes transverse derivatives through some finite order `m`, replace the factors `(z−a)^2` by `(z−a)^(m+2)`. Then `gδ` and `gδ'` have the required zero multiplicities, preserving those finitely many derivatives too. Mixed derivatives in `X,t` retain the same polynomial zeros. Since the new `Q` is still a fixed polynomial with `Q(z*)=1`, the uniform normalization proof is unchanged.

The all-variable analytic constant-background example can also preserve any prescribed finite initial time jet. Replace `h_k` by

\[
h_{k,m}(t)=\frac{e^{k^2t}-\sum_{j=0}^{m}(k^2t)^j/j!}
{e^{k^2T}-\sum_{j=0}^{m}(k^2T)^j/j!}.
\]

It satisfies `0≤h≤1`, `h(T)=1`, and its derivatives through order `m` vanish at zero. Its cancellation defect is

\[
h_{k,m}'-k^2h_{k,m}
=\frac{k^2(k^2t)^m/m!}{e^{k^2T}-\sum_{j=0}^{m}(k^2T)^j/j!},
\]

whose maximum tends to zero for every fixed finite `m` as `k→∞`. Thus finite initial derivative checks do not remove this analytic counterexample either.

The construction cannot preserve all derivatives of an analytic perturbation at one interior point: analyticity would then force it to vanish identically. It preserves every specified **finite** collection by choosing a sufficiently high finite multiplicity.

Although each candidate is entire, its norms on any fixed complex strip become unbounded as `δ→0`, and high transverse derivatives also grow without a common bound. Therefore the result does not defeat a certificate that first proves membership in a fixed quantitative analytic/Gevrey/tail ball. It shows why merely declaring the reference or candidate “analytic” supplies insufficient numerical information.

For the current independently perturbed sine data, no existence assertion is added: the separate transverse-jet obstruction makes the regularity of a potential target itself a substantive issue. This extension is a statement about the information needed by a residual-based verifier, not a proof that every structural construction of those exact data is impossible.
