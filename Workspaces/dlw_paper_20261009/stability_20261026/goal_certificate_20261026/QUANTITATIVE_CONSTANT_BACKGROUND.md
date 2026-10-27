# An explicit, arbitrarily large error with arbitrarily small full nonlinear residual

2026-10-26. Analytic proof and symbolic/Arb checks. The exact target in this note is the continuous solution `(u,v)=(0,4)`. The result supplies a quantitative instance of residual-only certification failure. The general nonzero-background theorem is a separate, conditional extension. This note does not certify or establish nonexistence of the independently perturbed four initial data.

## 1. Full physical equations

Let `X=x-4t`, `z∈[0,4]`, with period 192 in X. The residuals of the original continuous DLW equation are exactly

\[
R_1=u_{zt}+v_{XX}+(u u_z)_X,\qquad
R_2=v_t+u_{XXz}+(uv-4u)_X.
\]

These are full nonlinear PDE residuals on the whole space-time cylinder, not Fourier-projected residuals. At the exact target `(0,4)` they both vanish.

## 2. Explicit construction, valid in any interior observation interval

Fix any open interval `J⊂(0,4)`, any desired terminal error `M>0`, and `T=.01`. Put

\[
F(s)=\frac{25\sqrt5}{3}s^3(1-s)^3,\quad f(s)=F'(s),\quad 0\le s\le1,
\]

and extend both by zero. Then `F∈C²`, `f∈C¹`, `max|f|=1`, and

\[
\|Ff\|_\infty=C=\frac{9765625\sqrt{11}}{170069856}
=0.19044476622779319371\ldots.
\]

The product's extrema occur at `s=(1±1/√11)/2`. The maximum of `|F|` is `25√5/192<1`.

For any period-compatible `k=πn/96`, let

\[
h(t)=\frac{e^{k^2t}-1}{e^{k^2T}-1},\qquad q=e^{-k^2T},\qquad\delta=q.
\]

Choose `zstar` with `[zstar,zstar+δ]⊂J` and define

\[
u_{app}=M\delta F\left(\frac{z-z_*}{\delta}\right)h(t)\cos(kX),
\qquad
v_{app}=4+M f\left(\frac{z-z_*}{\delta}\right)h(t)\cos(kX).
\]

The complete initial functions are exactly `(0,4)`, because `h(0)=0`. The lower boundary and its neighbourhood are exactly unchanged. The pair is regular enough for every derivative in the physical equations to be continuous. At the terminal time,

\[
\|v_{app}(T)-4\|_\infty=M,\qquad
\|u_{app}\|_\infty\le M\delta\frac{25\sqrt5}{192}.
\]

The support can be placed inside the paper's interior observation region. Given finitely many transverse sampling nodes, choose J avoiding their union; all sampled fields at all times then coincide exactly with the exact target.

## 3. Exact nonlinear residual and finite parameter inequality

Here `vapp=4+∂z uapp`, so the two complete residuals coincide. Direct differentiation gives

\[
R_1=R_2=M f(h'-k^2h)\cos(kX)
-M^2\delta kFf h^2\sin(2kX).
\]

Since `h'-k²h=k²/(e^{k²T}−1)` and `0≤h≤1`,

\[
\max(\|R_1\|_\infty,\|R_2\|_\infty)
\le q\left[\frac{Mk^2}{1-q}+M^2kC\right].\tag{Q1}
\]

The quadratic term has been retained exactly. The bound tends to zero for each fixed M as n tends to infinity. Consequently, for **every** residual tolerance `r>0` and **every** target terminal discrepancy `M>0`, an explicit finite n supplies residual less than r and terminal error M. To place the strip in any specified J, increase n further until `q<|J|`.

The accompanying Python file chooses finite integers n and verifies Q1 using 256-bit Arb for `M∈{10^-6,1}` and `r∈{10^-12,10^-30}`. The machine-readable JSON contains interval enclosures for k, δ and the residual bound.

## 4. Exact scope of the impossibility

Suppose an error estimator uses only exact initial and lower-boundary data, a positive tolerance r for the full ordinary maximum-norm PDE residual, and finitely many sampled field values. Without an additional uniform constraint on unresolved frequencies or transverse derivatives, these inputs admit arbitrarily large terminal v error. Thus they cannot supply even a finite universal error bound.

The inputs do not include a bound on the full continuous candidate itself, its transverse derivatives, or its infinite Fourier tail. Such information would restrict this construction, and would constitute additional mathematical hypotheses requiring proof for the proposed reference. The result does not exclude a structure-based exact evaluation or an independently proved tail-aware certificate for a specific continuous solution.

The use of thin transverse strips is explicit: the full maximum norm sees their height, while the residual's nonlinear coupling is proportional to their width. This is why controlling only x resolution and pointwise residual is insufficient for full-field accuracy.

For a smooth nonzero target the same phenomenon can be constructed using backward transport-diffusion along a frozen transverse layer, as in the separate general-background proof. Its existence assumptions must be checked for each target; the constant-state example above requires no unknown reference existence hypothesis.
