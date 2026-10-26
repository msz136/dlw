### 3.2 The centered semi-discretization (Centered-SD)

We develop the nonlinear formulation from the same-site and cross-site relations used for Endpoint-SD. Their symmetric arrangement determines the first physical field through the sum of two logarithmic ratios. We then identify the full potential in its evolution equation and define the second field by a lattice difference. This choice retains the midpoint form of the first Endpoint-SD equation while using the symmetric bilinear lattice.

As in Section 3.1, set \(r_k=\log(f_k/g_k)\), \(R_k=\log(f_k/g_{k-1})\), \(s_k=\log(f_kg_k)\) and \(Q_k=\log(f_kg_{k-1})\). The Centered-SD pairings are
\[
B_{a+h/2}f_k\cdot g_k=0,\qquad B_{a-h/2}f_k\cdot g_{k-1}=0.\tag{32}
\]
Here \(f_k\) lies at \(y_k=(k-1/2)h\), between \(g_{k-1}\) and \(g_k\). Define the nodal field and auxiliary logarithmic difference by
\[
U_k=(r_k+R_k)_x=\partial_x\log\frac{f_k^2}{g_{k-1}g_k},\qquad
w_k=\frac4h(R_k-r_k)_x=\frac4h\partial_x\log\frac{g_k}{g_{k-1}}.\tag{33}
\]
Write \(H(U)=U^2/2+2aU\), \(A(w)=w^2/32-w/4\), and \(Z_k=(s_k+Q_k)_x\). Fix a linear primitive \(J\), commuting with time differentiation and satisfying \(\partial_x^2J=\partial_x\); for example, \(J\phi(x)=\int_{x_*}^x\phi(\xi)\,d\xi\) with fixed \(x_*\). The second physical field is the difference of the full potential:
\[
\widehat Z_k=Z_k+h^2JA(w_k),\qquad V_k=\Delta_h\widehat Z_k.\tag{34}
\]
Thus \(V_k\) lies at the edge midpoint \(y_k-h/2\). Let \(\mathcal M_-w_k=(w_k+w_{k-1})/2\) and \(\mathcal F_k=w_{k,xx}-\partial_x[(U_k+2a)w_k-4U_k]\).

**Proposition 3.2 (Full-potential formulation of Centered-SD).** Positive, sufficiently smooth solutions of (32), reconstructed by (33)–(34), satisfy
\[
\begin{aligned}
\Delta_hU_{k,t}&=-\partial_x\Delta_hH(U_k)-V_{k,xx},\\
V_{k,t}&=\Delta_hU_{k,t}+\mathcal M_-\mathcal F_k+h^2J\Delta_h[A'(w_k)\mathcal F_k],\\
V_k&=\Delta_hU_k+\mathcal M_-w_k+h^2J\Delta_hA(w_k),\qquad w_{k,t}=\mathcal F_k.
\end{aligned}\tag{35}
\]

**Proof.** Dividing the two bilinear equations by their respective tau-function products gives
\[
\begin{aligned}
s_{k,xx}+r_{k,x}^2+r_{k,t}+(2a+h)r_{k,x}&=0,\\
Q_{k,xx}+R_{k,x}^2+R_{k,t}+(2a-h)R_{k,x}&=0.
\end{aligned}\tag{36}
\]
As in the Endpoint-SD derivation, subtract the same-site relation from the cross-site relation. Since \(Q_k-s_k=-(R_k-r_k)\), the second-derivative term is \(-hw_{k,x}/4\). The difference of squares is \(hU_kw_k/4\), and the parameter terms give \(h(2aw_k-4U_k)/4\). Hence
\[
(R_k-r_k)_t+\frac h4[-w_{k,x}+(U_k+2a)w_k-4U_k]=0.
\]
Differentiating in x and multiplying by \(4/h\) yields
\[
w_{k,t}=w_{k,xx}-\partial_x[(U_k+2a)w_k-4U_k]=\mathcal F_k.\tag{37}
\]
Next add the relations in (36) and differentiate in x. From \(r_{k,x}=U_k/2-hw_k/8\) and \(R_{k,x}=U_k/2+hw_k/8\), the quadratic terms sum to \(U_k^2/2+h^2w_k^2/32\), while the parameter terms sum to \(2aU_k-h^2w_k/4\). Consequently,
\[
U_{k,t}+\partial_xH(U_k)+Z_{k,xx}+h^2\partial_xA(w_k)=0.\tag{38}
\]
The additional flux comes from these symmetric quadratic and parameter contributions. The definition of \(\widehat Z_k\) incorporates it into the potential, so (38) becomes \(U_{k,t}+\partial_xH(U_k)+\widehat Z_{k,xx}=0\). Taking a lattice difference gives the first equation in (35).

To eliminate the remaining logarithmic potential, use \(Z_k-U_k=2\partial_x\log(g_{k-1}g_k)\). Its adjacent-site difference is \(h(w_k+w_{k-1})/2\), giving
\[
\Delta_hZ_k=\Delta_hU_k+\mathcal M_-w_k.\tag{39}
\]
This proves the reconstruction constraint in (35). Differentiating that constraint in time and using (37) gives the stated equation for \(V_{k,t}\). ∎

The reconstruction preserves the first Endpoint-SD equation exactly, with the same placement of its two physical fields. The second field now includes an x primitive, whose normalization is part of the definition. Given U and V, a selected inverse branch and a lower trace determine w through
\[
\frac12w_k+hJA(w_k)=V_k-\Delta_hU_k-\frac12w_{k-1}+hJA(w_{k-1}).
\]
This is a nonlocal two-field representation with an auxiliary reconstruction constraint. For the numerical experiments, we solve this constraint at initialization and evolve U and w using the equations above, reconstructing V from the same fixed map. In particular, the lower w trace evolves through (37). The Gram determinants therefore retain their role as exact solution sources, while the full potential specifies how their logarithms enter the two physical fields.
