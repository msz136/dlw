## 2. Bilinear lattice construction and exact solutions

In this section, we develop a bilinear lattice description of the DLW system that connects the continuous equations, the arrangement of the τ functions and the construction of exact solutions. In Section 2.1, we recall the continuous system and its bilinear representation, fixing the parameters and the transformation to the physical fields. We then derive an unreduced bilinear lattice from the Hirota–Miwa equation in Section 2.2, making the origin of the discrete relations explicit. Building on these relations, Section 2.3 introduces a symmetric staggered formulation through a shift of the bilinear parameter. In Section 2.4, we construct the corresponding Gram determinant solutions and specify the conditions under which they yield regular physical fields. These results provide the basis for the nonlinear formulations and integrable structure developed in Section 3.

### 2.1 The continuous DLW system and its bilinear representation

We begin with the continuous DLW system and its bilinear representation. Specifically, we seek a description in which the physical fields and their explicit solutions can be obtained from a common pair of τ functions. With real parameters \(a\) and \(\lambda\), the continuous equations are
\[
u_{yt}+v_{xx}+[(u+2a)u_y]_x=0,\qquad
v_t+u_{xxy}+[(u+2a)v+2\lambda u]_x=0.\tag{1}
\]
For positive, sufficiently smooth functions \(f,g\), we use the transformation
\[
u=2\partial_x\log(f/g),\qquad v=2\partial_{xy}\log(fg).\tag{2}
\]
Hirota's bilinear derivatives are defined by
\[
D_x^mD_y^nD_t^\ell f\cdot g=
\left.(\partial_x-\partial_{x'})^m(\partial_y-\partial_{y'})^n
(\partial_t-\partial_{t'})^\ell f(x,y,t)g(x',y',t')\right|_{(x',y',t')=(x,y,t)}.\tag{3}
\]
Writing \(B_a=D_x^2+D_t+2aD_x\), the bilinear equations are
\[
B_af\cdot g=0,\qquad (D_yB_a+2\lambda D_x)f\cdot g=0.\tag{4}
\]
Their logarithmic expansion, followed by (2), gives the continuous field equations (1). We use the bilinear representation and continuous Gram construction of Sheng and Yu [1].

For the lattice construction, we fix \(\lambda=-2\). This replaces \(2\lambda u\) by \(-4u\) in the second field equation and \(2\lambda D_x\) by \(-4D_x\) in the second bilinear equation. Thus
\[
B_af\cdot g=0,\qquad (D_yB_a-4D_x)f\cdot g=0.\tag{5}
\]
The first relation describes the \(x,t\) dependence on each fixed-\(y\) slice, while the second connects these slices through the \(y\) derivative. We therefore consider a lattice in \(y\), keeping \(x\) and \(t\) continuous. When the operator parameter varies, we write \(B_s=D_x^2+D_t+2sD_x\).

The continuous Gram family can be written as
\[
\tau_n^{(0)}=\det_{1\le i,j\le N}\left[
\delta_{ij}+\frac{\rho_i}{p_i+q_j}
\left(-\frac{p_i-a}{q_j+a}\right)^n e^{\xi_i+\eta_j}\right],
\qquad f=\tau_1^{(0)},\quad g=\tau_0^{(0)},\tag{6}
\]
where
\[
\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad
\eta_j=q_jx+q_j^2t+\frac{y}{q_j+a}.\tag{7}
\]
The parameters are chosen so that the denominators are nonzero. On regions where \(\tau_1^{(0)}\) and \(\tau_0^{(0)}\) are positive, (2) gives smooth real physical fields. These τ functions solve the bilinear equations (5).

### 2.2 An unreduced bilinear lattice from the Hirota–Miwa equation

In this subsection, we introduce the endpoint-based semi-discretization (Endpoint-SD) of the DLW bilinear system. We retain two lattice directions in the Hirota–Miwa equation and use a Miwa expansion to introduce the continuous variables \(x,t\). We then examine the local consistency of the resulting lattice relations.

Let \(T_\alpha,T_\beta,T_\gamma\) denote commuting shifts, with subscripts indicating their action. The Hirota–Miwa equation is
\[
(\gamma-\beta)\tau_\alpha\tau_{\beta\gamma}
+(\alpha-\gamma)\tau_\beta\tau_{\alpha\gamma}
+(\beta-\alpha)\tau_\gamma\tau_{\alpha\beta}=0.\tag{8}
\]
We use the inverse-spacing convention and Gram construction in [2]. Set
\[
\alpha=\varepsilon_1^{-1},\qquad\beta=\varepsilon_2^{-1},
\qquad T_{\varepsilon_i^{-1}}:X_m\mapsto X_m+\frac{\varepsilon_i^m}{m}.\tag{9}
\]
After a common midpoint translation and multiplication by \(\varepsilon_1\varepsilon_2\), the first nonzero term has total degree three and is proportional to
\[
\frac{\varepsilon_1\varepsilon_2(\varepsilon_1-\varepsilon_2)}2
(D_{X_1}^2-D_{X_2}+2\gamma D_{X_1})\tau\cdot T_\gamma\tau.
\]
Its coefficient therefore gives
\[
(D_{X_1}^2-D_{X_2}+2\gamma D_{X_1})\tau\cdot T_\gamma\tau=0.\tag{10}
\]
Retain directions with inverse spacings \(0,d\), and denote their coordinates by \(s,r\). Introduce
\[
n=r+s,\qquad k=-r.\tag{11}
\]
The two shifts then act as
\[
T_0\tau_n(k)=\tau_{n+1}(k),\qquad
T_d\tau_n(k)=\tau_{n+1}(k-1).\tag{12}
\]
The zero inverse spacing is taken as a limit at the τ-function level. The two retained relations are
\[
\begin{aligned}
(D_{X_1}^2-D_{X_2})\tau_n(k)\cdot\tau_{n+1}(k)&=0,\\
(D_{X_1}^2-D_{X_2}+2dD_{X_1})\tau_n(k)\cdot\tau_{n+1}(k-1)&=0.
\end{aligned}\tag{13}
\]
Now set
\[
X_1=x-2bt,\qquad X_2=-t,\qquad
f_k=\tau_0(k),\quad g_k=\tau_1(k).\tag{14}
\]
Since \(D_x=D_{X_1}\) and \(D_t=-2bD_{X_1}-D_{X_2}\), the first operator becomes \(B_b\). Taking \(d=-h\), with \(h>0\), gives the following lattice.

**Definition 2.1 (Endpoint-SD).** We refer to
\[
B_bf_k\cdot g_k=0,\qquad B_{b-h}f_k\cdot g_{k-1}=0\tag{15}
\]
as the endpoint-based semi-discretization, abbreviated Endpoint-SD. For comparison with the continuous system at fixed parameter \(a\), we set \(b=a\) and associate both \(f_k\) and \(g_k\) with \(y_k=kh\). The auxiliary index \(n\) is not subjected to a pseudo two-reduction, so the \(x\) and \(t\) flows remain independent.

To examine consistency, define
\[
\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t).
\]
The endpoint pairings correspond to \(\Phi(0)\) and \(\Phi(-h)\).

**Proposition 2.1 (First-order bilinear consistency).** For sufficiently smooth \(f,g\),
\[
\frac{\Phi(0)-\Phi(-h)}h
=B_af\cdot g_y+2D_xf\cdot g
-\frac h2\left(B_af\cdot g_{yy}+4D_xf\cdot g_y\right)+O(h^2).\tag{16}
\]
**Proof.** Differentiation gives \(\Phi'(0)=B_af\cdot g_y+2D_xf\cdot g\) and \(\Phi''(0)=B_af\cdot g_{yy}+4D_xf\cdot g_y\). Taylor expansion proves (16). For solutions of (5), ordinary differentiation of the first relation gives \(B_af_y\cdot g+B_af\cdot g_y=0\), while the second gives \(B_af_y\cdot g-B_af\cdot g_y-4D_xf\cdot g=0\). Combining these identities yields \(\Phi'(0)=0\). ∎

The Endpoint-SD formulation therefore combines the lattice relations inherited from the Hirota–Miwa equation with a first-order approximation of the continuous bilinear system. Equation (16) makes the leading correction explicit and relates it to the endpoint placement of the τ functions and operator parameters.

### 2.3 A symmetric staggered formulation

We introduce the centered semi-discretization (Centered-SD) by examining the arrangement of the Endpoint-SD pairings. The first-order term in (16) arises from their one-sided placement relative to the continuous reference. To obtain a symmetric arrangement, we set
\[
b=a+\frac h2.\tag{17}
\]
The same lattice equations become
\[
B_{a-\frac h2}f_k\cdot g_{k-1}=0,\qquad
B_{a+\frac h2}f_k\cdot g_k=0.\tag{18}
\]
We associate \(g_k\) with \(y_k=kh\) and \(f_k\) with \(y_{k-\frac12}=(k-\frac12)h\). The two neighbouring \(g\) functions now lie symmetrically about \(f_k\), together with the two operator parameters about \(a\).

**Definition 2.2 (Centered-SD).** We refer to (18), with this staggered placement, as the centered semi-discretization, abbreviated Centered-SD.

At fixed \(h\), (18) follows exactly from (15) through (17). For the continuous comparison, \(a\) remains fixed. Using the function \(\Phi\) from Section 2.2 at the location of \(f_k\), the two pairings correspond to \(\Phi(-h/2)\) and \(\Phi(h/2)\).

**Proposition 2.2 (Second-order bilinear consistency).** For sufficiently smooth \(f,g\),
\[
\begin{aligned}
\frac{\Phi(h/2)+\Phi(-h/2)}2&=B_af\cdot g+O(h^2),\\
\frac{\Phi(h/2)-\Phi(-h/2)}h&=B_af\cdot g_y+2D_xf\cdot g+O(h^2).
\end{aligned}\tag{19}
\]
**Proof.** Taylor expansion gives \(\Phi(\pm h/2)=\Phi(0)\pm(h/2)\Phi'(0)+(h^2/8)\Phi''(0)+O(h^3)\). Taking the sum and difference proves (19). As shown in Section 2.2, the limiting relations are equivalent to the continuous bilinear pair (5). ∎

In the last two subsections, we have introduced Endpoint-SD and developed Centered-SD from it. The Miwa expansion and the reorganization of the remaining lattice directions lead naturally to the endpoint pairings of Endpoint-SD. Examining their approximation to the continuous system then draws attention to the first-order term associated with the one-sided arrangement. This observation motivates a symmetric placement of the same pairings, giving Centered-SD through a shift of the parameter reference and a staggered interpretation of the τ functions. The two formulations thus arise along a common construction, with first- and second-order bilinear consistency, respectively. With these relations established, we can examine how each choice enters the physical-field reconstruction and how the resulting formulations perform in numerical computation.

### 2.4 Gram determinant solutions and regularity

We now construct Gram determinant solutions for Endpoint-SD and Centered-SD. The retained lattice directions determine the discrete factors, while the Miwa expansion supplies the continuous dependence on \(x\) and \(t\). We present the two solution families separately and prove their bilinear identities within the same construction. We then identify a real parameter class that ensures positivity of the τ functions and permits smooth physical-field reconstruction.

Let \(N\ge1\), \(h>0\), and let \(a,c_{ij},\alpha_i,\beta_j,z_i,w_j\) be real, with
\[
z_iw_j(z_i+w_j)(z_i+h)(w_j-h)\ne0.
\]
Define
\[
L_{ij}(h)=\frac{1+h/z_i}{1-h/w_j},\qquad
\xi_i=z_i(x-2at)-z_i^2t,\qquad
\eta_j=w_j(x-2at)+w_j^2t.
\]
**Theorem 2.1 (Gram determinant solutions).**

(i) For Endpoint-SD, set
\[
\tau_n^{\mathrm E}(k)=\det_{1\le i,j\le N}\left[c_{ij}
+\frac{\alpha_i\beta_j}{z_i+w_j}
\left(-\frac{w_j}{z_i}\right)^n L_{ij}(h)^k e^{\xi_i+\eta_j}\right].\tag{20}
\]
Then \(f_k^{\mathrm E}=\tau_0^{\mathrm E}(k)\), \(g_k^{\mathrm E}=\tau_1^{\mathrm E}(k)\) satisfy
\[
B_af_k^{\mathrm E}\cdot g_k^{\mathrm E}=0,\qquad
B_{a-h}f_k^{\mathrm E}\cdot g_{k-1}^{\mathrm E}=0.\tag{21}
\]
(ii) For Centered-SD, set
\[
\tau_n^{\mathrm C}(k)=\det_{1\le i,j\le N}\left[c_{ij}
+\frac{\alpha_i\beta_j}{z_i+w_j}
\left(-\frac{w_j}{z_i}\right)^n L_{ij}(h)^k
e^{\xi_i+\eta_j-h(z_i+w_j)t}\right].\tag{22}
\]
Then \(f_k^{\mathrm C}=\tau_0^{\mathrm C}(k)\), \(g_k^{\mathrm C}=\tau_1^{\mathrm C}(k)\) satisfy
\[
B_{a-\frac h2}f_k^{\mathrm C}\cdot g_{k-1}^{\mathrm C}=0,\qquad
B_{a+\frac h2}f_k^{\mathrm C}\cdot g_k^{\mathrm C}=0.\tag{23}
\]
**Proof.** In the Hirota–Miwa Gram construction [2], the factor for a direction of inverse spacing \(\gamma\) is \(R_\gamma=(\gamma+w_j)/(\gamma-z_i)\). Hence
\[
R_0=-\frac{w_j}{z_i},\qquad
R_{-h}=R_0\frac{1-h/w_j}{1+h/z_i}.
\]
With \(n=r+s\), \(k=-r\), the two retained directions give
\[
R_{-h}^{\,r}R_0^{\,s}
=\left(-\frac{w_j}{z_i}\right)^nL_{ij}(h)^k.
\]
For a Miwa direction,
\[
\log\frac{1+\varepsilon w_j}{1-\varepsilon z_i}
=\sum_{m\ge1}\frac{z_i^m-(-w_j)^m}{m}\varepsilon^m.
\]
The first two continuous times therefore contribute \((z_i+w_j)X_1+(z_i^2-w_j^2)X_2\). Fixing the higher times and absorbing their factors into the amplitudes, the change \(X_1=x-2bt\), \(X_2=-t\) gives the phase
\[
(z_i+w_j)(x-2bt)+(w_j^2-z_i^2)t.
\]
The finite determinants are analytic in the Miwa parameters near zero, so the coefficient identities of Section 2.2 apply to this family. Taking \(b=a\) gives (20)–(21); taking \(b=a+h/2\) supplies the additional phase \(-h(z_i+w_j)t\) and gives (22)–(23). ∎

The superscripts distinguish the two families. They share the same determinant structure and lattice factors, while the extra phase in Centered-SD records the shifted parameter reference. To obtain regular real physical fields, we now choose a parameter class for which the determinants remain positive.

**Proposition 2.3 (A positive real solution class).** Set \(z_i=-P_i\), \(w_i=Q_i\), \(c_{ij}=\delta_{ij}\), \(\alpha_i=-e^{\xi_{i0}}\), and \(\beta_i=e^{\eta_{i0}}\), with real phase constants. If
\[
0<Q_N<\cdots<Q_1<P_1<\cdots<P_N,\qquad 0<h<Q_N,\tag{24}
\]
then both determinant families are positive for every integer \(n,k\) and finite real \(x,t\).

**Proof.** The nonconstant matrix in each determinant is a product of positive diagonal matrices and the Cauchy matrix \(H_{ij}=1/(P_i-Q_j)\). Indeed, \(Q_j/P_i>0\), and \(L_{ij}=(1-h/P_i)/(1-h/Q_j)>0\); all these factors separate into row and column factors. Every nonempty principal minor satisfies
\[
\det H_{I,I}=
\frac{\prod_{i<j,\ i,j\in I}(P_j-P_i)(Q_i-Q_j)}
{\prod_{i,j\in I}(P_i-Q_j)}>0.\tag{25}
\]
Positive diagonal multiplication preserves these signs. Expanding \(\det(I+A)\) as the sum of all principal minors, including the empty minor \(1\), proves positivity. The additional Centered-SD phase also consists of positive row and column factors. ∎

Starting from the Hirota–Miwa equation, we have introduced Endpoint-SD and developed its centered counterpart, Centered-SD, within the same bilinear construction. Endpoint-SD retains the endpoint arrangement that follows naturally from the Miwa expansion, whereas Centered-SD places the pairings symmetrically through a shift of the parameter reference and a staggered placement of the τ functions. These arrangements give first- and second-order bilinear consistency, respectively. Both admit explicit Gram determinant solutions, for which the positivity conditions established above ensure smooth logarithms for physical-field reconstruction. With these results in place, we next develop the corresponding nonlinear formulations and their Lax representations, then examine how the lattice solutions approach the continuous physical fields.

## 3. Nonlinear formulations and integrable structure

The bilinear construction gives Endpoint-SD and Centered-SD a common origin, while their different lattice arrangements enter the reconstruction of the physical fields. We now develop the corresponding nonlinear equations and examine how these choices shape their relation to the continuous DLW system. Alongside the field reconstruction, we establish compatible linear problems and use the determinant solutions to study the approximation of the continuous wave fields.

In Section 3.1, we introduce the nonlinear formulation of Endpoint-SD through its endpoint variables. Building on this reconstruction, Section 3.2 develops the formulation of Centered-SD using the staggered placement of the τ functions. We then establish their Darboux–Lax representations in Section 3.3. Section 3.4 brings the two formulations back to the continuous DLW system by examining their consistency and the convergence of the exact physical fields. For Centered-SD, we match the exact Gram fields to the continuous solution and identify the shared initial U-derivative coefficient that will guide the spatial comparisons.

### 3.1 The endpoint-based semi-discretization (Endpoint-SD)

We first introduce the physical fields associated with the endpoint bilinear lattice. Following the continuous transformation, we use the logarithmic ratio of the two τ functions to define the first field and replace the \(y\) derivative of their logarithmic product by a lattice difference to define the second. This reconstruction connects the two bilinear pairings to a nonlinear system for the physical fields.

For a lattice function \(q_k(x,t)\), write
\[
\Delta_hq_k=\frac{q_k-q_{k-1}}h,\qquad \overline q_k=\frac{q_k+q_{k-1}}2.
\]
The Endpoint-SD bilinear equations are
\[
B_af_k\cdot g_k=0,\qquad B_{a-h}f_k\cdot g_{k-1}=0,
\qquad B_a=D_x^2+D_t+2aD_x.
\]
We define
\[
U_k=2\partial_x\log\frac{f_k}{g_k},\qquad
V_k=\frac2h\partial_x\log\frac{f_kg_k}{f_{k-1}g_{k-1}}.\tag{26}
\]
The first expression uses the τ functions at a single site, so \(U_k\) is associated with \(y_k=kh\). The second takes a difference across two adjacent sites, placing \(V_k\) naturally on the edge with midpoint \(y_{k-\frac12}\). We retain these locations when comparing the lattice fields with their continuous counterparts.

**Proposition 3.1 (Nonlinear formulation of Endpoint-SD).** Let \(f_k,g_k\) be positive, sufficiently smooth solutions of the Endpoint-SD bilinear equations. Then the fields defined by (26) satisfy
\[
(\Delta_hU_k)_t+2a(\Delta_hU_k)_x
+\frac12\partial_x\Delta_h(U_k^2)+(V_k)_{xx}=0,\tag{27}
\]
and
\[
(V_k)_t+\partial_x\left[
(\overline U_k+2a-2h)V_k+\frac h4V_k^2-4\overline U_k
+(\Delta_hU_k)_x-\frac h4(\Delta_hU_k)^2\right]=0.\tag{28}
\]
**Proof.** Introduce the logarithmic variables
\[
r_k=\log(f_k/g_k),\qquad s_k=\log(f_kg_k),\qquad Z_k=\Delta_hs_k.
\]
Then \(U_k=2(r_k)_x\) and \(V_k=2(Z_k)_x\). Dividing the same-site bilinear equation by \(f_kg_k\) gives
\[
E_k:=(s_k)_{xx}+(r_k)_x^2+(r_k)_t+2a(r_k)_x=0.\tag{29}
\]
Applying \(2\partial_x\Delta_h\) to this relation yields (27): the logarithmic product supplies \((V_k)_{xx}\), while the remaining terms give the time derivative, drift and nonlinear flux of \(\Delta_hU_k\).

To obtain the second field equation, we use the pairing across the edge. Set
\[
R_k=\log f_k-\log g_{k-1}
=\frac{s_k-s_{k-1}+r_k+r_{k-1}}2,
\]
\[
Q_k=\log f_k+\log g_{k-1}
=\frac{s_k+s_{k-1}+r_k-r_{k-1}}2.
\]
The cross-site bilinear equation becomes
\[
E_k^{\mathrm c}:=(Q_k)_{xx}+(R_k)_x^2+(R_k)_t
+2(a-h)(R_k)_x=0.\tag{30}
\]
We now subtract the average of the two same-site relations, \((E_k+E_{k-1})/2\). This brings the cross-site pairing into expressions involving the edge field \(V_k\), the average \(\overline U_k\) and the difference \(\Delta_hU_k\). In particular,
\[
(R_k)_x=\frac{\overline U_k}{2}+\frac h4V_k,
\]
and hence
\[
(R_k)_x^2-\frac{U_k^2+U_{k-1}^2}{8}
=\frac h4\overline U_kV_k+\frac{h^2}{16}
\left[V_k^2-(\Delta_hU_k)^2\right].
\]
The second-derivative and time terms reduce to
\[
(Q_k)_{xx}-\frac{(s_k)_{xx}+(s_{k-1})_{xx}}2
=\frac h4(\Delta_hU_k)_x,
\]
\[
(R_k)_t-\frac{(r_k)_t+(r_{k-1})_t}2=\frac h2(Z_k)_t.
\]
Combining these expressions with the drift terms and multiplying by \(4/h\), we obtain
\[
2(Z_k)_t+(\Delta_hU_k)_x+(\overline U_k+2a-2h)V_k
+\frac h4V_k^2-4\overline U_k-\frac h4(\Delta_hU_k)^2=0.\tag{31}
\]
Differentiation in \(x\), together with \(V_k=2(Z_k)_x\), proves (28). ∎

We have thus obtained the nonlinear Endpoint-SD system by combining the endpoint field reconstruction with the two bilinear relations. Equations (27)–(28) involve only \(U_k\) and \(V_k\), with the logarithmic variables eliminated in the derivation. With the nonlinear equations established, we can now use the Endpoint-SD Gram determinants from Section 2.4 to obtain exact physical fields through (26). The positivity of these determinants ensures that the resulting fields remain smooth. These explicit fields also provide reference solutions for the subsequent analysis and numerical tests of Endpoint-SD.

### 3.2 The centered semi-discretization (Centered-SD)

We introduce the physical fields through the symmetric pairings of the centered bilinear lattice. As in the Endpoint-SD construction, taking logarithms turns the bilinear equations into relations that can be subtracted and added. The second field is then defined by a lattice difference of the logarithmic potential.

The centered pairings are
\[
B_{a+h/2}f_k\cdot g_k=0,\qquad B_{a-h/2}f_k\cdot g_{k-1}=0,\qquad B_c=D_x^2+D_t+2cD_x.\tag{32}
\]
Here \(f_k\) is located at \(y_k=(k-1/2)h\), between \(g_{k-1}\) and \(g_k\). Define
\[
u_k=\partial_x\log\frac{f_k^2}{g_{k-1}g_k},\qquad Z_k=\partial_x\log(f_k^2g_{k-1}g_k),\qquad v_k=\Delta_hZ_k.\tag{33}
\]
These definitions follow the continuous fields \(u=2\partial_x\log(f/g)\) and \(v=2\partial_{xy}\log(fg)\). The field \(u_k\) is nodal, while \(v_k\) lies at the edge midpoint \(y_k-h/2\). Write \(\Delta_hq_k=(q_k-q_{k-1})/h\) and \(H(u)=u^2/2+2au\).

For a specified lower trace \(b(x,t)\), define the reconstruction \(\Omega_k[u,v;b]\) by
\[
\Omega_0[u,v;b]=b,\qquad \Omega_k[u,v;b]=\frac h2(v_k-\Delta_hu_k)-\Omega_{k-1}[u,v;b],\quad k=1,\ldots,N.\tag{34}
\]
On a finite lattice, this recurrence uniquely determines the reconstruction from the fields and the lower trace. We suppress the dependence on b below and write \(\Omega_k[u,v]\).

**Proposition 3.2 (Natural physical-field formulation of Centered-SD).** Let \(f_k,g_k\) be positive, sufficiently smooth solutions of (32). For the fields defined in (33), choose the compatible lower trace \(b=\partial_x\log(g_0/g_{-1})\). Then, for \(k=1,\ldots,N\), the physical fields satisfy
\[
\begin{aligned}
\Delta_hu_{k,t}
&=-\partial_x\Delta_h\left[H(u_k)+\frac{\Omega_k[u,v]^2}{2}-h\Omega_k[u,v]\right]-v_{k,xx},\\[2mm]
v_{k,t}
&=-\partial_x^2\Delta_hu_k\\
&\quad-\partial_x\Bigg\{\Delta_h\left[H(u_k)+\frac{\Omega_k[u,v]^2}{2}-h\Omega_k[u,v]\right]\\
&\hspace{22mm}+\frac2h\left[(u_k+2a)\Omega_k[u,v]+(u_{k-1}+2a)\Omega_{k-1}[u,v]-h(u_k+u_{k-1})\right]\Bigg\}.
\end{aligned}\tag{35}
\]

**Proof.** Set \(r_k=\log(f_k/g_k)\), \(R_k=\log(f_k/g_{k-1})\), \(s_k=\log(f_kg_k)\), and \(Q_k=\log(f_kg_{k-1})\). The first equation in (32) pairs \(f_k\) with \(g_k\), whereas the second pairs \(f_k\) with \(g_{k-1}\). We refer to these as the same-site and cross-site relations, respectively; these names describe the lattice indices in each pairing. Dividing by the corresponding products, using \((D_x^2f\cdot g)/(fg)=(\log fg)_{xx}+[(\log(f/g))_x]^2\), gives
\[
\begin{aligned}
s_{k,xx}+r_{k,x}^2+r_{k,t}+(2a+h)r_{k,x}&=0,\\
Q_{k,xx}+R_{k,x}^2+R_{k,t}+(2a-h)R_{k,x}&=0.
\end{aligned}\tag{36}
\]
We have now rewritten the two bilinear equations as two logarithmic relations. Subtracting the first relation in (36) from the second gives
\[
0=(Q_k-s_k)_{xx}+(R_{k,x}^2-r_{k,x}^2)+(R_k-r_k)_t+2a(R_k-r_k)_x-h(R_k+r_k)_x.
\]
The definitions imply \(Q_k-s_k=-(R_k-r_k)\). Introduce \(\omega_k=(R_k-r_k)_x\). Since \(u_k=(R_k+r_k)_x\), the second-derivative term is \(-\omega_{k,x}\), while the difference of squares is \(u_k\omega_k\). The subtraction therefore reduces to
\[
(R_k-r_k)_t-\omega_{k,x}+(u_k+2a)\omega_k-hu_k=0.
\]
Differentiating in x gives
\[
\omega_{k,t}=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k].\tag{37}
\]
This is one evolution equation, for the difference between the two logarithmic derivatives. We next return to (36) and add its two relations:
\[
0=(s_k+Q_k)_{xx}+r_{k,x}^2+R_{k,x}^2+(r_k+R_k)_t+2a(r_k+R_k)_x-h(R_k-r_k)_x.
\]
From \(r_{k,x}=(u_k-\omega_k)/2\) and \(R_{k,x}=(u_k+\omega_k)/2\), the sum of squares is \((u_k^2+\omega_k^2)/2\). Substituting and differentiating in x yields
\[
u_{k,t}=-\partial_x\left[H(u_k)+\frac{\omega_k^2}{2}-h\omega_k\right]-Z_{k,xx}.\tag{38}
\]
At this stage, the two relations obtained from the bilinear system are
\[
\begin{aligned}
\omega_{k,t}&=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k],\\
u_{k,t}&=-\partial_x[H(u_k)+\omega_k^2/2-h\omega_k]-Z_{k,xx}.
\end{aligned}
\]
The first involves \(u_k,\omega_k\); the second also contains the logarithmic potential \(Z_k\). Taking a lattice difference of the second relation and using \(v_k=\Delta_hZ_k\), the pair becomes
\[
\begin{aligned}
\omega_{k,t}&=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k],\\
\Delta_hu_{k,t}&=-\partial_x\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]-v_{k,xx}.
\end{aligned}
\]
The potential has been replaced by v. The auxiliary quantity \(\omega\) remains, and we still need the evolution equation for v.

The field definitions provide the relation needed to continue. They give \(Z_k-u_k=2\partial_x\log(g_{k-1}g_k)\), and hence
\[
v_k-\Delta_hu_k=\frac2h\partial_x\log\frac{g_k}{g_{k-2}}=\frac2h(\omega_k+\omega_{k-1}).\tag{39}
\]
With \(\omega_0=b\), this is precisely the recurrence (34), so \(\omega_k=\Omega_k[u,v]\).

We now have equations for \(\omega_{k,t}\) and \(\Delta_hu_{k,t}\), together with a relation expressing v through u and \(\omega\). Differentiating (39) in time gives
\[
v_{k,t}=\Delta_hu_{k,t}+\frac2h(\omega_{k,t}+\omega_{k-1,t}).
\]
Both terms on the right are supplied by the preceding pair. Substituting them, the second x derivatives combine by (39) as
\[
-v_{k,xx}+\frac2h(\omega_{k,xx}+\omega_{k-1,xx})=-\partial_x^2\Delta_hu_k.
\]
The resulting physical-field equations are
\[
\begin{aligned}
\Delta_hu_{k,t}&=-\partial_x\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]-v_{k,xx},\\[2mm]
v_{k,t}&=-\partial_x^2\Delta_hu_k\\
&\quad-\partial_x\Bigg\{\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]\\
&\hspace{22mm}+\frac2h[(u_k+2a)\omega_k+(u_{k-1}+2a)\omega_{k-1}-h(u_k+u_{k-1})]\Bigg\}.
\end{aligned}
\]
Replacing \(\omega\) by the reconstruction (34) gives the two equations in (35). ∎


### 3.3 Darboux–Lax representations

We now examine the integrable structure of the nonlinear systems through their associated linear problems. For each formulation, we seek a lattice relation connecting neighbouring wave functions and a continuous equation governing their time dependence. Their compatibility connects these linear problems to the nonlinear field equations derived above.

We begin with Endpoint-SD, whose endpoint variables determine the coefficients of the lattice relation. The same construction extends to Centered-SD through the parameter shift and field reconstruction introduced in Sections 2.3 and 3.2. We therefore use a common operator form and specify its coefficients for each formulation.

Let \(D=\partial_x\), and let \(Y\) denote the backward lattice shift, \((Y\psi)_k=\psi_{k-1}\). The shift acts on variable coefficients according to \(Yq_k=q_{k-1}Y\). Consider the operators
\[
L=(D+A_k)Y-(D+C_k),\qquad
M=D^2-2bD+S_k,\qquad \widetilde M=M-2(C_k)_x.\tag{40}
\]
They define the linear problem
\[
(D+A_k)\psi_{k-1}=(D+C_k)\psi_k,\qquad
(\psi_k)_t=(\psi_k)_{xx}-2b(\psi_k)_x+S_k\psi_k.\tag{41}
\]
We express its compatibility through
\[
L_t+LM=\widetilde M L.\tag{42}
\]
Indeed, this identity gives \(\partial_t(L\psi)=(L_t+LM)\psi=\widetilde M(L\psi)\), so the time evolution preserves the lattice relation \(L\psi=0\).

**Proposition 3.3 (Darboux–Lax representations).** Let \(f_k,g_k\) be positive, sufficiently smooth solutions of the corresponding bilinear lattice, and define
\[
S_k=2\partial_x^2\log f_k.\tag{43}
\]
Then the operators (40) satisfy (42) with the following coefficients. For Endpoint-SD, with the physical fields defined in (26),
\[
b=a,\qquad A_k=\frac{U_{k-1}}2,\qquad
C_k=\frac{U_k+U_{k-1}+hV_k}{4}-h.\tag{44}
\]
For Centered-SD, with U and w defined in (33),
\[
\begin{gathered}
b=a+\frac h2,\\
A_k=\frac{U_{k-1}}2-\frac h8(w_{k-1}),\qquad
C_k=\frac{U_k}2+\frac h8(w_k)-h.
\end{gathered}\tag{45}
\]
**Proof.** We first establish the operator identity for a general bilinear parameter \(b\). Both lattices have the form
\[
B_bf_k\cdot g_k=0,\qquad B_{b-h}f_k\cdot g_{k-1}=0,
\]
with \(b=a\) for Endpoint-SD and \(b=a+h/2\) for Centered-SD. Using the logarithmic variables from the preceding subsections, set
\[
A_k=(r_{k-1})_x,\qquad C_k=(R_k)_x-h.\tag{46}
\]
The relation between these coefficients follows from \(R_k-r_{k-1}=\log f_k-\log f_{k-1}\). Consequently,
\[
S_k-S_{k-1}=2(C_k-A_k)_x.\tag{47}
\]
We next obtain the time equations for \(A_k\) and \(C_k\). The same-site bilinear relation gives
\[
(s_k)_{xx}+(r_k)_x^2+(r_k)_t+2b(r_k)_x=0.
\]
Since \(s_k+r_k=2\log f_k\), differentiation in \(x\) yields
\[
(r_k)_{xt}=(r_k)_{xxx}-2\bigl(b+(r_k)_x\bigr)(r_k)_{xx}-(S_k)_x.
\]
Evaluating this equation at \(k-1\) gives
\[
(A_k)_t=(A_k)_{xx}-2(b+A_k)(A_k)_x-(S_{k-1})_x.\tag{48}
\]
Similarly, the cross-site relation reads
\[
(Q_k)_{xx}+(R_k)_x^2+(R_k)_t+2(b-h)(R_k)_x=0.
\]
Here \(Q_k+R_k=2\log f_k\). Differentiating in \(x\) and using \((R_k)_x=C_k+h\), we obtain
\[
(C_k)_t=(C_k)_{xx}-2(b+C_k)(C_k)_x-(S_k)_x.\tag{49}
\]
These three relations are precisely the coefficient equations of the operator compatibility condition. To see this, expand \(L_t+LM-\widetilde M L\) using \(Dq=qD+q_x\) and \(Yq_k=q_{k-1}Y\). The coefficient of \(DY\) vanishes by (47). After this substitution, the coefficient of \(Y\) vanishes by (48), and the term without a lattice shift vanishes by (49). Thus (42) holds.

It remains to express (46) through the physical fields. For Endpoint-SD,
\[
(r_{k-1})_x=\frac{U_{k-1}}2,\qquad
(R_k)_x=\frac{U_k+U_{k-1}+hV_k}{4},
\]
which gives (44). For Centered-SD, the logarithmic identities following (33) give
\[
(r_{k-1})_x=\frac{U_{k-1}}2-\frac h8(w_{k-1}),\qquad
(R_k)_x=\frac{U_k}2+\frac h8(w_k),
\]
and hence (45). ∎

The coefficient equations also show how the linear compatibility recovers the nonlinear dynamics. For Endpoint-SD, shifting (48) forward by one site gives
\[
(U_k)_t=(U_k)_{xx}-(U_k+2a)(U_k)_x-2(S_k)_x,
\]
while (47) becomes
\[
\Delta_hS_k=\frac12\partial_x(V_k+\Delta_hU_k).
\]
Taking a lattice difference of the first relation and substituting the second yields the first Endpoint-SD equation. The second follows from (49) through
\[
h(V_k)_t=4(C_k)_t-(U_k)_t-(U_{k-1})_t.
\]
For Centered-SD, the corresponding combination is
\[
C_k-A_{k+1}=\frac h4(w_k)-h.
\]
Subtracting the forward-shifted equation (48) from (49) therefore gives
\[
(w_k)_t+\partial_x\left[(U_k+2a)(w_k)-4U_k\right]
-(w_k)_{xx}=0.
\]
The potential relation (47) takes the form
\[
\Delta_hS_k=\partial_x\left[\Delta_hU_k+\frac12\mathcal M_-(w_k)\right].
\]
Combining it with the forward-shifted equation (48) recovers (38). The full-potential reconstruction (34) then gives the first physical-field equation in (35); differentiating its reconstruction constraint gives the V equation. These coefficients are expressed through U and the auxiliary w. Their expression through U,V alone uses the selected inverse branch of that constraint.

We have thus obtained both Darboux–Lax representations from the same logarithmic relations used to derive the nonlinear systems. The endpoint and staggered reconstructions enter through the coefficients \(A_k,C_k\), together with the corresponding choice of \(b\). Their common operator form makes the connection between Endpoint-SD and Centered-SD explicit: each translates its bilinear lattice into a compatible linear problem governing the reconstructed physical fields.

### 3.4 Continuous limit and approximation of the physical fields

We examine the nonlinear equations at the physical locations of their fields. Write the continuous residuals as
\[
\mathcal R_u=u_{yt}+v_{xx}+\partial_x[(u+2a)u_y],\qquad
\mathcal R_v=v_t+u_{xxy}+\partial_x[(u+2a)v-4u].\tag{50}
\]
Both representations place U at nodes and V at edge midpoints. For Centered-SD, the nodes themselves occupy the staggered locations specified in Section 3.2.

**Proposition 3.4 (Consistency on smooth branches).** Let u and v be sufficiently smooth on a fixed compact region. Substituting their samples into Endpoint-SD gives
\[
\mathcal R_{\mathrm E,1}=\mathcal R_u+O(h^2),\qquad
\mathcal R_{\mathrm E,2}=\mathcal R_v+\frac h4\partial_x(v^2-u_y^2-8v)+O(h^2).\tag{51}
\]
For Centered-SD, assume the reconstruction constraint selects a smooth branch admitting an expansion \(w=v-u_y+O(h^2)\), with the required derivative bounds, and that J is uniformly bounded on the functions considered. The two physical-field evolution residuals satisfy
\[
\mathcal R_{\mathrm C,1}=\mathcal R_u+O(h^2),\qquad
\mathcal R_{\mathrm C,2}=\mathcal R_v+O(h^2).\tag{52}
\]
The residuals are evaluated at the corresponding edge midpoint.

**Proof.** Midpoint expansion gives \(\Delta_hU=u_y+h^2u_{yyy}/24+O(h^4)\) and \(\mathcal M_-U=u+h^2u_{yy}/8+O(h^4)\). The first Endpoint-SD equation therefore gives \(\mathcal R_u+O(h^2)\). In its second equation, the flux becomes
\[
(u+2a)v-4u+u_{xy}+\frac h4(v^2-u_y^2-8v)+O(h^2),
\]
which yields (51). The first Centered-SD equation is identical to the Endpoint-SD first equation. For its second equation, the reconstruction constraint has the expansion
\[
v=u_y+w+h^2\left(\frac{u_{yyy}}{24}+\frac{w_{yy}}8+J\partial_yA(w)\right)+O(h^4).\tag{53}
\]
On the stated smooth branch, insert \(w=v-u_y+O(h^2)\) into \(\mathcal F\) and the equation for \(V_t\). Its right-hand side is
\[
-\partial_y\partial_xH(u)-v_{xx}
+(v-u_y)_{xx}-\partial_x[(u+2a)(v-u_y)-4u]+O(h^2)
=-u_{xxy}-\partial_x[(u+2a)v-4u]+O(h^2).
\]
This proves (52). ∎

The smooth-branch condition specifies the reconstruction used in this comparison; a lattice-alternating component of w is not controlled by midpoint averaging alone. For matched exact waves, the required smooth expansion can be obtained from the Gram formulas themselves.

Set \(P_i=p_i-a\), \(Q_j=q_j+a\). In the Centered-SD Gram family, choose \(z_i=P_i-h/2\), \(w_j^{\rm spec}=Q_j+h/2\), \(c_{ij}=\delta_{ij}\) and \(\alpha_i\beta_j=-\rho_i z_i/w_j^{\rm spec}\), where the superscript distinguishes the spectral parameter from the auxiliary field. The x,t phase then agrees exactly with the continuous one, and the y phase rate is
\[
\frac1h\log\frac{(P_i+h/2)(Q_j+h/2)}{(P_i-h/2)(Q_j-h/2)}
=\frac1{P_i}+\frac1{Q_j}+O(h^2).
\]
At their respective staggered positions, the g amplitude agrees with the continuous amplitude, while the f amplitude differs by the factor \(\sqrt{(1-h^2/(4P_i^2))/(1-h^2/(4Q_j^2))}=1+O(h^2)\). For nonzero spectral denominators, sufficiently small h and positive tau functions bounded away from zero on the fixed region, the determinants and their required derivatives therefore differ from the continuous counterparts by \(O(h^2)\). Symmetric averaging in (33) gives \(U_h=u+O(h^2)\); the difference of Z in (39) gives \(\Delta_hZ_h=v+O(h^2)\). A bounded fixed primitive adds an \(O(h^2)\) correction, so \(V_h=v+O(h^2)\) as well.

The shared first equation gives a more specific conclusion for the initial derivative comparison. With common continuous samples and an exact lower value of \(U_t\), summation along y approximates \(\int v_{xx}\,dy\) by the midpoint rule. Thus both semi-discrete formulations have
\[
r_U=\frac{h^2}{24}[v_{xxy}]_{y_0}^{y}+O(h^4).
\]
This coefficient concerns the initial derivative defect. Together with the exact-field matching, it distinguishes the accuracy of the reconstructed waves from the error introduced when the nonlinear equations act on common continuous initial data.
