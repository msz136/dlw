### 2.5 Continuum limits {#en-limits}

Having established the semi-discrete equations and their exact solutions, we now examine how they approach the continuous DLW system as the lattice spacing tends to zero. We wish to determine how the lattice modifies the exact wave fields and how the continuous equations emerge from the discrete relations. We first derive an expansion of the difference between the semi-discrete and continuous Gram solutions, including its leading coefficients. The second-order convergence of the reconstructed fields then follows directly. We subsequently examine the consistency of the nonlinear equations.

Throughout this subsection, $O_K(h^m)$ denotes a remainder bounded uniformly by $C_Kh^m$ on a compact set $K$, with $C_K$ independent of $h$. We assume sufficient smoothness on an open neighbourhood of $K$. Where derivatives of an expansion are used, the remainder estimate is understood to hold for those derivatives as well.

We begin by comparing corresponding members of the exact solution families. To make this comparison at a common physical position, we extend the lattice τ functions to continuous $y$ and retain the staggered reconstruction. For positive functions $f_h,g_h$, we define

<a id="en-eq-47"></a>

$$\begin{aligned}U_h(y)&=\partial_x[2\log f_h(y)-\log g_h(y-h/2)-\log g_h(y+h/2)],\\\Omega_h(y)&=\partial_x[\log g_h(y+h/2)-\log g_h(y-h/2)],\\V_h(y)&=\frac4h\Omega_h(y)+\frac{U_h(y+h)-U_h(y-h)}{2h}.\end{aligned}\tag{38}$$

Here and below, we suppress the common arguments $x,t$ when displaying shifts in $y$. At $y=(j+\tfrac12)h$, these expressions agree with the lattice reconstruction in (18).

**Theorem 2.7 (Leading error and convergence of the exact wave fields).** Fix the determinant order $N$ and real spectral parameters satisfying, for some $h_0>0$,

<a id="en-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{50}$$

Let $f,g$ be the continuous Gram τ functions in (5), and let $u,v$ be their physical fields defined by (2). For $0<h\le h_0$, extend the positive lattice factors to real powers and set

<a id="en-eq-60"></a>

$$g_h(x,y,t)=\tau_0(y/h),\qquad f_h(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{51}$$

Let $U_h,V_h$ be the staggered reconstruction defined above. Write $\alpha=\log f$, $\beta=\log g$, $z_i=p_i-a$ and $w_i=q_i+a$, and define

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,$$

$$\alpha_2=\sum_{i=1}^{N}(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_{i=1}^{N}c_i\rho_i\partial_{\rho_i}\beta.$$

Then, uniformly on every compact set $K$,

<a id="en-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{60}$$

Consequently, for sufficiently small $h>0$,

<a id="en-eq-61"></a>

$$\sup_K\bigl(|U_h-u|+|V_h-v|\bigr)\le C_Kh^2\tag{52}$$

The same expansion applies to the physical fields reconstructed through either PE or PF.

**Proof.** We first expand the lattice factors while keeping the spectral parameters fixed:

<a id="en-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{53}$$

For each determinant entry, the coefficient of $y$ in the lattice phase therefore satisfies

<a id="en-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{54}$$

In $f_h$, the half-grid displacement also combines with the shift of the auxiliary parameter. The resulting amplitude factor is

<a id="en-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}\left[1+\frac{h^2}{8}\left(\frac1{w_k^2}-\frac1{z_i^2}\right)+O(h^4)\right].\end{aligned}\tag{55}$$

Both the phase and the centred amplitude thus differ from their continuous counterparts first at order $h^2$.

To identify the coefficients in the determinants, we use their principal-minor expansions. Each minor uses the same index set $\mathcal I$ for its rows and columns. Its phase correction is $h^2y\sum_{i\in\mathcal I}c_i$, while the additional amplitude correction for $f_h$ is $h^2\sum_{i\in\mathcal I}d_i$. The operator $\rho_i\partial_{\rho_i}$ selects precisely the minors containing the index $i$. Expanding the determinants and then their logarithms gives

$$\log f_h=\alpha+h^2\alpha_2+O_K(h^4),\qquad \log g_h=\beta+h^2\beta_2+O_K(h^4).$$

The stated spectral conditions ensure positivity of the continuous τ functions and their real-exponent extensions. Since $N$ and the spectral parameters are fixed, these expansions hold uniformly on compact sets, together with the derivatives required below.

We next insert the logarithmic expansions into the staggered reconstruction. Symmetric Taylor expansion about the physical position $y$ gives

$$U_h=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4).$$

For the second field, the corresponding expansions are

$$\frac4h\Omega_h=4\beta_{xy}+h^2\left[4(\beta_2)_{xy}+\frac16\beta_{xyyy}\right]+O_K(h^4),$$

$$\begin{aligned}\frac{U_h(y+h)-U_h(y-h)}{2h}={}&u_y+h^2\left[2(\alpha_2-\beta_2)_{xy}-\frac14\beta_{xyyy}+\frac16u_{yyy}\right]+O_K(h^4).\end{aligned}$$

Adding these expressions, we obtain

$$V_h=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).$$

Finally, the continuous reconstruction implies $4\beta_{xy}=v-u_y$. Using this identity in the two field expansions gives the stated coefficients $C_U,C_V$. Their boundedness on $K$ yields the second-order convergence estimate. Since PE and PF reconstruct identical fields from the same τ functions, the result holds for both formulations. □

Through this expansion, we can describe how discretization in $y$ changes the reconstructed wave fields at small but finite lattice spacing. The coefficients $C_U$ and $C_V$ determine the leading spatial distribution of the difference in each field. The terms involving $\alpha_2,\beta_2$ arise from changes in the determinant solutions, while the remaining terms come from the staggered reconstruction. Under the stated assumptions, these coefficients are bounded on compact sets. The expansion therefore gives, as a direct consequence, uniform second-order convergence of both reconstructed fields to their continuous DLW counterparts as $h\to0$.

We now turn to the nonlinear equations. To express their continuum limit in the physical variables, we introduce

<a id="en-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{42}$$

The PE equations then take the form

<a id="en-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{43}$$

With $\mathcal M_+z_j=(z_{j+1}+z_j)/2$, the identity $\mathcal M_+\delta_-=\delta_0$ shows that the time derivative in $\mathcal M_+E_{1,h,j}+E_{2,h,j}$ is $v_{j,t}$. We therefore compare this combination with the second continuous DLW equation.

**Proposition 2.8 (Consistency of the equations).** Sample sufficiently smooth fields $u,v$ at $y_j=(j+\tfrac12)h$, and define the continuous residuals

<a id="en-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{44}$$

Then, uniformly on compact sets,

<a id="en-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{45}$$

**Proof.** We set $m_j=y_j-h/2$. Expanding the difference and averaging operators about their respective centres gives

<a id="en-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{46}$$

Consequently,

<a id="en-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{47}$$

These expansions also hold after the required differentiation. Substitution into the first residual yields $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$.

For the second residual, we write $w=v-u_y$ and obtain

<a id="en-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{48}$$

Averaging the first residual about $y_j$ and adding the second gives

<a id="en-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{49}$$

Here all continuous fields are evaluated at $y_j$. This proves the second assertion. □

The continuum-limit analysis shows that the proposed lattice system retains a quantitative connection with the continuous DLW model. We recover the continuous equations with second-order consistency and, for the exact solution families considered here, obtain uniform second-order convergence of both physical fields on compact sets. At finite lattice spacing, the coefficients $C_U$ and $C_V$ give a more detailed account of this approximation: they describe the leading difference in each field and how that difference varies across the wave profile. We can thus assess the effect of discretizing $y$ directly in the reconstructed physical fields. Since PE and PF yield identical fields from the same τ functions, the error expansion and its coefficients apply to both formulations.
