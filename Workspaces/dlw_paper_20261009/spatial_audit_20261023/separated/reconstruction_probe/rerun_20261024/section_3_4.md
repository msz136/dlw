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
