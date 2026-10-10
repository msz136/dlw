<nav>[English](#en-title) · [中文](#zh-title)</nav>

# Semi-discretization, Darboux–Lax representation and numerical simulations of the (2+1)-dimensional DLW system {#en-title}

**Abstract.** We construct a staggered semi-discrete bilinear system for the (2+1)-dimensional dispersive long wave (DLW) equation and derive its Gram determinant solutions. A rank-one update between adjacent auxiliary layers establishes the bilinear identities for determinants of arbitrary finite order. Two nonlinear formulations follow by eliminating a common logarithmic potential through lattice differences or retaining it through potential variables. They reconstruct identical physical fields from a common positive τ-function pair and admit a Darboux–Lax representation. We establish second-order consistency and the uniform second-order continuum limit of the exact Gram solutions for fixed regular spectral parameters. Numerical experiments compare the nonlinear formulations, time integrators and self-adaptive moving mesh methods against a direct finite-difference discretization. In the fixed-grid tests, the potential-elimination formulation gives smaller errors in u than the potential formulation. RK4 and Crank–Nicolson differ by less than 0.003% in terminal error, while the moving mesh reduces the errors in both physical fields by 16.2%–66.8% across the reported comparisons.

**Keywords:** dispersive long wave equation; semi-discretization; Gram determinant; Darboux–Lax representation; continuum limit; self-adaptive moving mesh

## 1. Introduction {#en-intro}

The (2+1)-dimensional dispersive long wave (DLW) system describes long-wave motion and has been studied through inverse scattering, exact-solution transformations and bilinear methods. Early work developed a spectral-transform approach [1], while subsequent studies constructed exact-solution transformations [2] and bilinear Bäcklund transformations [3]. Determinant representations of its solutions were obtained within the Sato and Hirota frameworks [4]. More recently, a reduction of the KP hierarchy yielded Gram determinant solutions describing solitons, breathers and rational waves [5]. These results connect the nonlinear physical fields with a common τ-function structure.

Previous studies have shown that the bilinear representation of the DLW system is connected with the modified KP hierarchy and, under suitable parameter choices and an interchange of variables, with a (2+1)-dimensional sinh-Gordon system [5]. Semi-discrete and fully discrete versions of the latter bilinear system have been constructed, together with their Bäcklund transformations and Lax pairs [6]. The integrable discretization of soliton equations has received considerable attention, with Hirota’s bilinear method providing a framework for constructing discrete counterparts of continuous systems [6–8]. Within this framework, the compatibility between bilinear equations and Bäcklund transformations has been used to derive semi-discrete analogues of several soliton equations, including extended KdV and KP equations [7]. In (2+1) dimensions, bilinear constructions have also yielded a semi-discrete system related to the KP and Zakharov equations, admitting N-soliton solutions and soliton resonance [8]. These developments suggest exploring a semi-discrete counterpart of the DLW system within the bilinear framework.

In this paper, we construct a semi-discrete bilinear system for the (2+1)-dimensional DLW equation by discretizing the y variable and derive its Gram determinant solutions. Through two dependent-variable transformations, we obtain two nonlinear formulations that recover the same physical fields from a common pair of τ functions, and establish the associated Darboux–Lax representation and second-order continuum limits. We then develop numerical schemes based on these formulations and investigate the effects of the nonlinear formulation, time integration and self-adaptive moving mesh (SAMM) methods through one- and two-soliton computations. The numerical comparison follows the use of semi-discrete soliton systems in self-adaptive computation [9].

The paper is organized as follows. Starting from the continuous DLW system and its bilinear representation, Section 2 constructs the semi-discrete bilinear equations and their Gram determinant solutions, derives two nonlinear formulations, and establishes the continuum limits and the Darboux–Lax representation. Section 3 presents the numerical schemes and one- and two-soliton experiments, examining the effects of the nonlinear formulation, time integration and SAMM methods. Section 4 concludes the paper.

## 2. Semi-discrete DLW system and exact solutions {#en-continuous}

We begin with the continuous DLW system and its bilinear representation, which provide the starting point for the semi-discrete construction. We then derive the Gram determinant solutions and two nonlinear formulations, followed by their continuum limits and Darboux–Lax representation.

### 2.1 Continuous DLW system and bilinear formulation {#en-preliminaries}

Consider the (2+1)-dimensional DLW system in the normalization of [5] with $\lambda=-2$,

<a id="en-eq-1"></a>

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

where $a\in\mathbb R$ is constant. With positive τ functions f and g, introduce the dependent-variable transformation

<a id="en-eq-2"></a>

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

The corresponding bilinear representation is [5]

<a id="en-eq-3"></a>

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

where $B_s=D_x^2+D_t+2sD_x$ and the Hirota operators are defined by

<a id="en-eq-4"></a>

$$D_x^rD_y^sD_t^m f\cdot g=\left.(\partial_x-\partial_{x\prime})^r(\partial_y-\partial_{y\prime})^s(\partial_t-\partial_{t\prime})^m f(x,y,t)g(x\prime,y\prime,t\prime)\right|_{(x\prime,y\prime,t\prime)=(x,y,t)}.\tag{4}$$

Here r,s,m are nonnegative integers. The following proposition states the relation between the bilinear equations and the physical fields.

**Proposition 2.1 (Bilinear representation [5]).** If sufficiently smooth positive functions f,g satisfy [(3)](#en-eq-3), the fields defined by [(2)](#en-eq-2) solve the DLW system [(1)](#en-eq-1).

**Proof.** Divide the bilinear equations by fg, expand the Hirota operators in logarithmic derivatives, and substitute [(2)](#en-eq-2). This gives the two equations in [(1)](#en-eq-1); see [5, Section 2]. □

The continuous Gram determinant solutions are given by [5]

<a id="en-eq-5"></a>

$$\tau_n^{(0)}=\det_{1\le i,k\le N}\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\left(-\frac{p_i-a}{q_k+a}\right)^n e^{\xi_i+\eta_k}\right],\quad f=\tau_1^{(0)},\quad g=\tau_0^{(0)},\tag{5}$$

<a id="en-eq-6"></a>

$$\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad \eta_k=q_kx+q_k^2t+\frac{y}{q_k+a}.\tag{6}$$

Here N is the determinant order, n is an auxiliary integer index, and the real parameters are chosen so that all displayed denominators are nonzero. The physical fields are defined on regions where f and g are positive.

### 2.2 Semi-discrete bilinear equations {#en-bilinear}

Based on the bilinear formulation presented above, we construct a semi-discretization of the DLW system in the y-direction, keeping x and t continuous. We start from the continuous bilinear equations. Differentiating the first equation in [(3)](#en-eq-3) with respect to y and combining it with the second gives

<a id="en-eq-7"></a>

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{7}$$

To combine the shift of the second factor with a shift of the operator parameter, set

<a id="en-eq-8"></a>

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t).\tag{8}$$

Then $\Phi(0)=B_af\cdot g$ and $\Phi\prime(0)=B_af\cdot g_y+2D_xf\cdot g$. Taking the symmetric shifts $s=\pm h/2$ leads to

<a id="en-eq-9"></a>

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{9}$$

The τ functions $F_j$ and $G_j$ are associated with $f(x,(j+\tfrac12)h,t)$ and $g(x,jh,t)$, respectively. The convergence of the Gram determinant solutions under this identification is established in Section 2.5.

Symmetric Taylor expansion gives

<a id="en-eq-10"></a>

$$\frac{\Phi(h/2)+\Phi(-h/2)}2=B_af\cdot g+O(h^2),\qquad \frac{\Phi(h/2)-\Phi(-h/2)}h=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{10}$$

Thus the average and the difference quotient recover the continuous bilinear equations with second-order accuracy.

### 2.3 Gram determinant solutions {#en-gram}

Let $d=h/2$ and $\lambda_h(z)=(z+d)/(z-d)$. Define the determinant sequence

<a id="en-eq-11"></a>

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{11}$$

Here $\delta_{ik}$ is the Kronecker symbol. The member $\tau_0(j;s)$ is independent of s and is denoted by $\tau_0(j)$.

**Theorem 2.2 (Gram determinant solutions).** Let $h>0$, $N\ge1$, and let $p_i,q_i,\rho_i$ be real parameters satisfying $p_i+q_k\ne0$, $p_i-a\pm d\ne0$ and $q_k+a\pm d\ne0$ for all i,k. Then

<a id="en-eq-12"></a>

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{12}$$

satisfy the semi-discrete bilinear system [(9)](#en-eq-9) for all lattice sites j.

Next, we verify that these Gram determinants satisfy the semi-discrete bilinear equations. For this purpose, we first establish an identity between adjacent members of the determinant sequence.

**Lemma 2.3 (Adjacent-layer identity).** Under the spectral conditions of Theorem 2.2, fix j and s such that $p_i-s\ne0$ and $q_k+s\ne0$. For every $n\in\mathbb Z$,

<a id="en-eq-13"></a>

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{13}$$

**Proof.** Write the nth Gram matrix as $M=I+(r_ic_k/(p_i+q_k))$, with

<a id="en-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{14}$$

Let $P=\operatorname{diag}(p_i)$, $Q=\operatorname{diag}(q_i)$ and $b=(Q+sI)^{-1}c$. The definitions give

<a id="en-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{15}$$

The layer shift follows from

<a id="en-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{16}$$

Where M is invertible, define

<a id="en-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{17}$$

The last equality follows from the matrix determinant lemma, while Jacobi’s formula gives $\kappa=\tau_{n,x}/\tau_n$. To collect the differentiated terms, set

<a id="en-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{18}$$

Using $H_x=-HM_xH$ and $H_t=-HM_tH$, direct differentiation yields

<a id="en-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{19}$$

For example, $z_x=HPr-\kappa z$, so that $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$. Differentiating this identity once more and eliminating $\eta_1,\eta_2$ gives

<a id="en-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{20}$$

Thus $\psi=1-\zeta$ satisfies

<a id="en-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{21}$$

For $f=\psi g$, expansion of the bilinear operator gives

<a id="en-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{22}$$

Taking $g=\tau_n$ and $f=\tau_{n+1}$ proves [(13)](#en-eq-13) wherever M is invertible. To extend the result to singular matrices, replace all $\rho_i$ by $\varepsilon\rho_i$. At any fixed x,t, M is the identity at $\varepsilon=0$, and the bilinear residual vanishes for ε near zero. Since the residual is a polynomial in ε, it vanishes identically. Setting $\varepsilon=1$ completes the proof. □

**Proof of Theorem 2.2.** The first equation follows from Lemma 2.3 with $n=0$ and $s=a-d$. For the second, the entrywise identity

<a id="en-eq-23"></a>

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{23}$$

implies

<a id="en-eq-24"></a>

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{24}$$

Applying the lemma at $j+1$ with $n=0$ and $s=a+d$ gives

<a id="en-eq-25"></a>

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{25}$$

This proves the second bilinear equation. □

Before introducing the nonlinear variables, we give a sufficient condition for the positivity of the τ functions.

**Proposition 2.4 (Positive τ functions).** If $0<p_1<\cdots<p_N<a-h/2$, $0<q_1<\cdots<q_N$ and $\rho_i>0$, then $F_j\ge1$ and $G_j\ge1$ for all x,t,j.

**Proof.** Both matrices have the form $I+D_1CD_2$, where $D_1,D_2$ are positive diagonal matrices and $C_{ik}=1/(p_i+q_k)$. Every nonempty principal minor is positive, since

<a id="en-eq-26"></a>

$$\det C_{I,I}=\frac{\prod_{i<k,\ i,k\in I}(p_k-p_i)(q_k-q_i)}{\prod_{i,k\in I}(p_i+q_k)}>0.\tag{26}$$

Positive diagonal scaling preserves this property. Expanding $\det(I+D_1CD_2)$ as the sum of its principal minors, including the empty minor 1, proves the assertion. □

### 2.4 Nonlinear formulations {#en-nonlinear}

We now derive two nonlinear formulations of the semi-discrete bilinear system. Both formulations use the following physical-field reconstruction from positive τ functions:

<a id="en-eq-27"></a>

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad \omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad v_j=\frac4h\omega_j+\delta_0u_j,\qquad \delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h}.\tag{27}$$

The physical fields are associated with $y=(j+\tfrac12)h$. These definitions provide a discrete counterpart of [(2)](#en-eq-2); their second-order consistency is established in Section 2.5.

Let $\alpha_j=\log F_j$ and $\beta_j=\log G_j$. Dividing the two bilinear equations by $F_jG_j$ and $F_jG_{j+1}$, respectively, gives

<a id="en-eq-28"></a>

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{28}$$

The physical-field definitions imply

<a id="en-eq-29"></a>

$$(\alpha_j-\beta_j)_x=\frac{u_j+\omega_j}{2},\qquad (\alpha_j-\beta_{j+1})_x=\frac{u_j-\omega_j}{2}.\tag{29}$$

In $A_j+C_j$, the second-derivative terms combine into $(2\alpha_j+\beta_j+\beta_{j+1})_{xx}$. We therefore introduce

<a id="en-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{30}$$

Taking the x-derivatives of $A_j+C_j=0$ and $A_j-C_j=0$ yields

<a id="en-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{31}$$

Next, we derive two nonlinear formulations from these evolution equations. The first eliminates $Z_j$ through a lattice difference, while the second expresses $Z_j$ in terms of a potential variable. For the first formulation, we introduce the backward difference and averaging operators

<a id="en-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{32}$$

The definitions of $u_j,\omega_j,Z_j$ give

<a id="en-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{33}$$

Applying $\delta_-$ to the first evolution equation and substituting this identity, we obtain the potential-elimination formulation (PE)

<a id="en-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{34}$$

For the second formulation, introduce the potential variable $M_j=\beta_{j,x}$. The definitions give

<a id="en-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{35}$$

With this substitution, the first evolution equation contains $u_{j,x}+u_j^2/2$. We therefore introduce

<a id="en-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{36}$$

so that

<a id="en-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{37}$$

The undifferentiated relation $(A_j+C_j)/2=0$ then gives

<a id="en-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{38}$$

In the second evolution equation, the flux can be written as

<a id="en-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{39}$$

To remove the quotient, define

<a id="en-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{40}$$

Using the identities

<a id="en-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{41}$$

the ω equation becomes

<a id="en-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{42}$$

Since

<a id="en-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{43}$$

substitution of the Q equation yields the equation for R. Together with the lattice constraint, this gives the potential formulation (PF)

<a id="en-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{44}$$

Here $Q_j,R_j$ are associated with $y=(j+\tfrac12)h$, and $M_j$ with $y=jh$. The physical fields are recovered by

<a id="en-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{45}$$

The following proposition shows that the two nonlinear formulations recover identical physical fields from the same pair of positive τ functions.

**Proposition 2.5 (Common physical fields).** Let positive F,G satisfy [(9)](#en-eq-9). The two nonlinear formulations constructed above yield identical physical fields u,v at every finite positive lattice spacing h.

**Proof.** The definitions give

<a id="en-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{46}$$

Adding the same central difference of u to the second equality proves that the reconstructed v fields also coincide. □

### 2.5 Continuum limits {#en-limits}

Having obtained the two nonlinear formulations, we now examine their continuum limits as $h\to0$. We first establish the second-order consistency of the physical-field reconstruction and the semi-discrete equations with their continuous counterparts. We then show that, for fixed regular spectral parameters, the Gram determinant solutions converge to the continuous DLW solutions with an error of order $h^2$, uniformly on compact sets.

Throughout this subsection, $O_K(h^m)$ denotes a remainder uniformly bounded by $C_Kh^m$ on a compact set K. Functions are assumed smooth on an open neighbourhood of K. The following proposition relates the staggered reconstruction to the continuous dependent-variable transformation.

**Proposition 2.6 (Consistency of reconstruction).** Let f,g be positive smooth functions, and let u,v be given by [(2)](#en-eq-2). At a physical location y, define

<a id="en-eq-47"></a>

$$\begin{aligned}u^{[h]}(y)&=\partial_x[2\log f(y)-\log g(y-h/2)-\log g(y+h/2)],\\\omega^{[h]}(y)&=\partial_x[\log g(y+h/2)-\log g(y-h/2)],\\v^{[h]}(y)&=\frac4h\omega^{[h]}(y)+\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}.\end{aligned}\tag{47}$$

The arguments x,t are suppressed. Then

<a id="en-eq-48"></a>

$$u^{[h]}=u+O_K(h^2),\qquad v^{[h]}=v+O_K(h^2).\tag{48}$$

**Proof.** Write $\alpha=\log f$, $\beta=\log g$. Symmetric Taylor expansion gives

<a id="en-eq-49"></a>

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad \frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).\tag{49}$$

The first expansion also holds after differentiation, so

<a id="en-eq-50"></a>

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2),\qquad v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2).\tag{50}$$

This proves the assertion. □

We next examine the nonlinear equations. Set

<a id="en-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{51}$$

The first formulation becomes

<a id="en-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{52}$$

With $\mathcal M_+z_j=(z_{j+1}+z_j)/2$, the identity $\mathcal M_+\delta_-=\delta_0$ shows that $\mathcal M_+E_{1,h,j}+E_{2,h,j}=0$ is the evolution equation for v.

**Proposition 2.7 (Consistency of the equations).** Sample smooth u,v at $y_j=(j+\tfrac12)h$, and denote the continuous DLW residuals by

<a id="en-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{53}$$

Then, uniformly on compact sets,

<a id="en-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{54}$$

**Proof.** Write $m_j=y_j-h/2$. Taylor expansion gives

<a id="en-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{55}$$

Consequently,

<a id="en-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{56}$$

The expansions hold after the required derivatives and give $E_{1,h,j}=\mathcal C_1(m_j)+O_K(h^2)$. Setting $w=v-u_y$, the second residual becomes

<a id="en-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{57}$$

Averaging the first residual about y_j and adding the second yields

<a id="en-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{58}$$

All continuous fields in this display are evaluated at y_j. This proves the second assertion. □

Finally, we establish the continuum limit of the exact Gram solutions. Here the τ functions depend on h through both the lattice factors and the shifted auxiliary parameter.

**Theorem 2.8 (Continuum limit of the Gram solutions).** Fix N and spectral parameters such that, for some $h_0>0$,

<a id="en-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{59}$$

For $0<h\le h_0$, extend the positive lattice factors to real exponents and define

<a id="en-eq-60"></a>

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{60}$$

Thus $g^{(h)}(x,jh,t)=G_j$ and $f^{(h)}(x,(j+\tfrac12)h,t)=F_j$. Let $u^{(h)},v^{(h)}$ be their staggered reconstruction, and let $f^{(0)},g^{(0)}$ be the continuous Gram functions in [(5)](#en-eq-5). The corresponding fields $u^{(0)},v^{(0)}$ solve the continuous DLW system, and for every compact K,

<a id="en-eq-61"></a>

$$\sup_K\bigl(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\bigr)\le C_Kh^2\tag{61}$$

for sufficiently small positive h. This estimate holds for both nonlinear formulations.

**Proof.** Write $z_i=p_i-a$ and $w_k=q_k+a$. For fixed spectral parameters,

<a id="en-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{62}$$

so the coefficient of y in the exponential satisfies

<a id="en-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{63}$$

For $f^{(h)}$, the auxiliary-parameter shift and the half-grid shift combine into the amplitude factor

<a id="en-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}+O(h^2).\end{aligned}\tag{64}$$

The phase and amplitude therefore differ from their continuous counterparts by $O(h^2)$. Since N is fixed, for every fixed mixed derivative $\partial^\nu$,

<a id="en-eq-65"></a>

$$\partial^\nu(f^{(h)}-f^{(0)})=O_K(h^2),\qquad \partial^\nu(g^{(h)}-g^{(0)})=O_K(h^2).\tag{65}$$

The positivity argument in Proposition 2.4 also applies to the real-exponent extension and its limit. All four τ functions are bounded below by 1, so their logarithmic derivatives satisfy the same second-order estimates.

The adjacent-layer identity and the lattice-shift relation remain valid for the extension, giving

<a id="en-eq-66"></a>

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.\tag{66}$$

Taking their symmetric average and difference quotient, with the uniform derivative bounds above, yields

<a id="en-eq-67"></a>

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.\tag{67}$$

These are the continuous bilinear equations in the equivalent form of Section 2.1, so Proposition 2.1 gives a continuous DLW solution. Finally, applying Proposition 2.6 uniformly to the h-dependent family gives

<a id="en-eq-68"></a>

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).\tag{68}$$

Combining these relations with [(65)](#en-eq-65) proves the estimate. Proposition 2.5 transfers the result to both nonlinear formulations. □

### 2.6 Darboux–Lax representation {#en-lax}

We next construct a Darboux–Lax representation of the semi-discrete DLW system. We first express the linear problem in terms of the physical fields and then give its potential form in the variables Q,R,M.

Introduce the shifted variables

<a id="en-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{69}$$

The first nonlinear formulation becomes

<a id="en-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{70}$$

To formulate the linear problem, introduce an auxiliary potential V satisfying

<a id="en-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{71}$$

The compatibility of these relations is precisely the first nonlinear equation. On a local x-interval and a lattice chain, V can therefore be constructed by integration at one reference site followed by lattice propagation, up to a common function of t.

Consider the auxiliary linear equations

<a id="en-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{72}$$

The first equation relates wave functions at adjacent lattice sites, while the second determines their time evolution. The following theorem establishes their compatibility with the nonlinear system.

**Theorem 2.9 (Darboux–Lax compatibility).** Every smooth solution of [(70)](#en-eq-70), together with the auxiliary potential [(71)](#en-eq-71), makes [(72)](#en-eq-72) compatible in the formal operator sense. Conversely, on a region where $w_j\ne0$, compatibility together with the potential-difference relation implies [(70)](#en-eq-70).

**Proof.** Set

<a id="en-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{73}$$

<a id="en-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{74}$$

Here $\mathscr B_j^{-1}$ is defined in the algebra of formal pseudodifferential operators. The linear system reads $\psi_{j+1}=T_j\psi_j$ and $\psi_{j,t}=H_j\psi_j$. Differentiating the lattice relation in t and using both time equations gives

<a id="en-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{75}$$

To verify this identity, define the scalar residuals

<a id="en-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{76}$$

Using $V_{j+1}-V_j=(h/2)w_{j,x}$ gives

<a id="en-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{77}$$

The w equation makes the difference vanish, and the definition of $V_{j,x}$ makes the sum vanish. Hence $\mathcal E_j^r=\mathcal E_j^s=0$. For a scalar function r, the product rule gives the Darboux identity

<a id="en-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{78}$$

The potential-difference relation implies

<a id="en-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{79}$$

Writing

<a id="en-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{80}$$

and applying the Darboux identity to the two vanishing residuals yields

<a id="en-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{81}$$

Eliminating the common intermediate operator gives $L_{j+1}T_j=T_jL_j$, which is equivalent to [(75)](#en-eq-75).

Conversely, assume compatibility and the potential-difference relation. The same operator calculation gives

<a id="en-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{82}$$

Comparing the coefficients of $\partial_x^0$ and $\partial_x^{-1}$ yields $\mathcal E_j^r=\mathcal E_j^s$ and $w_j\mathcal E_j^s=0$. Thus both residuals vanish wherever $w_j\ne0$. Their difference gives the w equation; their sum, after applying $\delta_-$ and using the potential-difference relation, gives the first nonlinear equation. □

For τ-function solutions, take

<a id="en-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{83}$$

Differentiating the normalized bilinear equations in x gives $\mathcal E_j^r=\mathcal E_j^s=0$. Thus the Gram determinant solutions satisfy the Darboux–Lax compatibility relations.

Finally, substitute the potential variables

<a id="en-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{84}$$

The linear system becomes

<a id="en-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{85}$$

Differentiating the lattice constraint gives

<a id="en-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{86}$$

The Q and R equations make both scalar residuals vanish, establishing compatibility. Conversely, when $Q_jR_j\ne0$, compatibility together with this potential-difference relation recovers the physical-field equations of the first formulation.

The above construction provides a common Darboux–Lax representation for the two nonlinear formulations. The lattice shift is realized through two first-order Darboux operators sharing an intermediate potential, and its compatibility with the time evolution follows from the semi-discrete field equations.

## 3. Numerical methods and experiments {#en-numerics}

We construct numerical schemes from the two nonlinear formulations and compare them with a direct finite-difference discretization of the continuous DLW system. Using the continuous exact solutions as a reference, we examine the effects of the nonlinear formulation and its discrete implementation, time integration, and self-adaptive moving mesh (SAMM) methods on the physical-field errors.

### 3.1 Spatial discretization {#en-schemes}

**Grid and difference operators.** On the fixed grid, let $x_i=-L/2+i\Delta x$, where $\Delta x=L/N_x$. In the y direction, $M_j$ is located at $y=jh$, while $u_j,v_j,Q_j,R_j$ are located at $y=(j+\tfrac12)h$. The indices j and i label the y layers and x nodes, respectively. Time remains continuous in the spatially discretized systems below.

We approximate the x derivatives by three-point centred differences

<a id="en-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{87}$$

In the y direction, we use

<a id="en-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{88}$$

The operators $D_1,D_2$ act on the x-node index, whereas $\delta_-,\delta_0,\mathcal M_-$ act on the layer index. All products and quotients below are evaluated pointwise. We first construct the PE and PF schemes, followed by the direct finite-difference scheme, denoted by FD.

**PE scheme.** We evolve $P=\delta_-u$ and $W=v-\delta_0u$. At each time, the physical fields are reconstructed by

<a id="en-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{89}$$

where $j_L$ denotes the lowest layer and $u_{j_L,i}(t)$ is prescribed by the lower boundary data. Substituting these fields into the PE equations gives $\dot P=F_P$ and $\dot W=F_W$, with

<a id="en-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{90}$$

Thus the right-hand side is evaluated by first recovering u from P, and then applying the spatial difference operators to u and W. The field v follows from the same reconstruction formula.

**PF scheme.** We evolve Q and R and reconstruct the physical fields through

<a id="en-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{91}$$

The evolution equations also contain $(M_j+M_{j+1})_x$. To evaluate this term, introduce $m_j\simeq M_{j,x}$ and $S_j=Q_jR_j$. Applying $D_1$ to the lattice constraint $M_{j+1}-M_j=h(1-S_j)$ yields

<a id="en-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{92}$$

This relation determines the m layers successively once their lower boundary value is known. Temporarily labelling the lowest layer as 0, we obtain that value from the Q equation:

<a id="en-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{93}$$

Here $Q_0(t)$ is prescribed by the lower boundary data, and $Q_{0,t}$ is its time derivative. With m determined, the evolution equations are $\dot Q_j=F_{Q,j}$ and $\dot R_j=F_{R,j}$, where

<a id="en-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{94}$$

The lowest Q layer is prescribed, while the interior Q layers and all R layers are evolved. The physical fields are recovered from Q and R using (91).

**FD scheme.** For comparison, we discretize the continuous DLW equations directly, taking $P=\delta_-u$ and v as the evolution variables. The field u is recovered from P by the first relation in (89). The resulting system is $\dot P=F_P$ and $\dot v=F_v$, with

<a id="en-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{95}$$

These three spatial discretizations are combined with the time integrators in Section 3.3. Their initial and boundary data are specified in Section 3.4.

### 3.2 Self-adaptive moving mesh method {#en-samm}

Based on the two semi-discrete DLW formulations, we construct the following self-adaptive moving mesh method using their common conservation law. Only the x nodes move, while the y spacing h remains fixed; all y layers share the same x nodes. Introduce the density and flux

<a id="en-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{96}$$

Substituting $W_j=4(1-\rho_j)$ into its evolution equation gives

<a id="en-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{97}$$

In PF, $\rho_j=Q_jR_j$. Since all y layers share the same x nodes, average over the layers:

<a id="en-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{98}$$

The initial mesh equidistributes the cumulative integral of $\bar\rho(x,0)$, assigning more nodes to regions of larger density. Fixing the left endpoint $x_L$ and keeping the cumulative integral at each moving node constant, [(97)](#en-eq-97) gives

<a id="en-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{99}$$

The resulting node velocity is

<a id="en-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{100}$$

In the computation, replace $\partial_x\rho$ by $D_1\rho$ and require $\bar\rho>0$. The FD moving-mesh comparison uses the same density, averaging and velocity formulas [(96)](#en-eq-96), [(98)](#en-eq-98) and [(100)](#en-eq-100).

The physical x spacings become nonuniform as the nodes move. Introduce fixed uniform computational coordinates $\xi_i=-L/2+i\Delta\xi$, with $\Delta\xi=L/N_x$, and write $x_i(t)=\xi_i+s_i(t)$. The node displacement is $s_i$, and $J_i=1+D_\xi s_i$ approximates the mapping Jacobian $J=x_\xi$.

The chain rule gives $\partial_x=J^{-1}\partial_\xi$ and hence

<a id="en-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{101}$$

Approximating the computational-coordinate derivatives by centred differences gives

<a id="en-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{102}$$

Here $D_\xi,D_{\xi\xi}$ are the three-point formulas in [(87)](#en-eq-87) on the uniform computational grid. For each evolving variable z, the chain rule gives $\dot z=F_z+\mathcal V D_1z$. Add this transport term to the rates above and advance the node equation [(100)](#en-eq-100) together with the fields. The fixed grid corresponds to $s=0$ and $\mathcal V=0$.

### 3.3 Time integration {#en-time}

We use the forward Euler, classical fourth-order Runge–Kutta (RK4), and Crank–Nicolson (C–N) methods to integrate the spatially discretized systems on both fixed and moving meshes. Let $z$ collect the evolving variables and write the resulting system as $\dot z=\mathcal F(t,z)$. For SAMM, $z$ also includes the node coordinates, and $\mathcal F$ includes the mesh transport terms and node velocities.

With $t_n=n\Delta t$, the forward Euler method is

<a id="en-eq-103"></a>

$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n).\tag{103}$$

We also use the classical four-stage, fourth-order Runge–Kutta method (RK4). At each stage, the reconstruction, auxiliary variables, spatial differences and boundary values are evaluated from the stage fields and mesh.

The Crank–Nicolson (C–N) method averages the rates at adjacent time levels:

<a id="en-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{104}$$

For FD, the v update is $v^{n+1}=v^n+\Delta t(F_v^n+F_v^{n+1})/2$. Since the final rate depends on the unknown next-level fields, it is solved jointly with the P update. The coupled implicit equations are solved iteratively, using the forward Euler approximation as the initial guess.

### 3.4 Test problems and error measures {#en-tests}

We consider one- and two-soliton solutions of the continuous DLW system. The exact solutions provide the initial and boundary data and serve as the reference for evaluating the numerical errors. Throughout the tests, we set $a=2$, take the determinant coefficients $\rho_i=1$, and set the initial phases to zero.

**One-soliton solutions.** For $N=1$, the continuous Gram determinant reduces to

<a id="en-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{105}$$

where

<a id="en-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{106}$$

The corresponding physical fields are

<a id="en-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{107}$$

For $p+q>0$ and $c>0$, the sign of the u pulse is determined by $c-1$, while that of v is determined by $\ell$. We choose $(p,q)=(1,2)$ and $(4,-3)$ to obtain a negative and a positive u pulse, respectively. In the first case, $c=1/4$ and $\ell=-3/4$; in the second, $c=2$ and $\ell=-1/2$. Both choices give a negative v pulse.

**Two-soliton solution.** For $N=2$, expanding the Gram determinant gives

<a id="en-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{108}$$

where

<a id="en-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{109}$$

The physical fields are obtained from $u_*=2\partial_x\log(f_*/g_*)$ and $v_*=2\partial_x\partial_y\log(f_*g_*)$. For the two-soliton solution, we take $p_1=6$, $q_1=-5$, $p_2=4$, and $q_2=-3$, giving $c_1=4/3$, $c_2=2$ and $A_{12}=4/3$. The phases are $\theta_1=x-11t-y/12$ and $\theta_2=x-7t-y/2$, so the two constituent waves have different spatial orientations and propagation rates. This case extends the comparison to a two-wave interaction.

**Initial and boundary data.** PE is initialized with $P^0=\delta_-u_*(0)$ and $W^0=v_*(0)-\delta_0u_*(0)$; FD uses the same $P^0$ and $v^0=v_*(0)$. For PF, Q is determined by $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ with normalization $Q_{j,0}^0=1$, and $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$. The lower boundary $Q_0(t)$ is obtained from $u_{*,0}(t)$ by the same relation. The three schemes therefore use common initial physical fields.

The computational boundaries are placed where the soliton tails approach their backgrounds. PE and FD use periodic x differences; PF uses the left and right background values of Q,R. In y, the lower boundary is exact and the difference between the numerical solution and the exact background is quadratically extrapolated at the upper boundary.

**Computational settings and error measures.**

For Tables 1–3, the computational domain is $x\in[-20,20)$ and $y\in[-1.5,1.5]$. Use $N_x=256$, fixed-grid spacing $\Delta x=0.15625$, and 24 cells in y with $h=0.125$. The time step is $\Delta t=1.25\times10^{-4}$ and the final time is $T=0.01$.

The evaluation grid $\mathcal G$ consists of 4001 equally spaced x points on $[-10,10]$ and all y layers. Cubic splines interpolate each numerical physical field from its actual x nodes. Define

<a id="en-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{110}$$

### 3.5 Numerical results {#en-results}

Table 1 compares the maximum absolute errors of the three spatial schemes, using common initial physical fields, the same fixed grid and RK4 time integration. The difference between PE and PF is most pronounced in u: the PF errors are approximately 7.61, 1.91 and 2.02 times the PE errors for the one-soliton solution with p=1 and q=2, the one-soliton solution with p=4 and q=−3 and the two-soliton case, respectively. The corresponding ratios for v are 2.25, 0.929 and 1.11. Thus PE gives smaller u errors in all three tests, while the relative v errors depend on the soliton parameters.

**Table 1. Maximum absolute errors on the fixed grid with RK4. The smallest entry in each row is bold.**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">Case</th><th scope="col">Field</th><th scope="col">PE</th><th scope="col">PF</th><th scope="col">FD</th></tr></thead>
<tbody>
<tr>
<th rowspan="2" scope="rowgroup">One-soliton (p=1, q=2)</th>
<th scope="row">u</th>
<td>1.560308e-03</td>
<td>1.187746e-02</td>
<td><strong>1.161402e-03</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>3.229398e-03</td>
<td>7.254773e-03</td>
<td><strong>3.008503e-03</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">One-soliton (p=4, q=−3)</th>
<th scope="row">u</th>
<td><strong>6.639277e-05</strong></td>
<td>1.266358e-04</td>
<td>7.809306e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.664598e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.429802e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">Two-soliton</th>
<th scope="row">u</th>
<td><strong>1.299876e-04</strong></td>
<td>2.620490e-04</td>
<td>1.442262e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.267185e-04</td>
<td>1.405303e-04</td>
<td><strong>1.242170e-04</strong></td>
</tr>
</tbody>
</table></div>

Relative to FD, PE reduces the u error by about 15.0% and 9.87% for the one-soliton solution with p=4 and q=−3 and the two-soliton case, while increasing the v error by about 3.65% and 2.01%. For the one-soliton solution with p=1 and q=2, its u and v errors exceed FD by about 34.3% and 7.34%. PF gives the smallest v error for the one-soliton solution with p=4 and q=−3, approximately 3.66% below FD. The differences between PE and FD are smaller in the latter two cases than in the one-soliton solution with p=1 and q=2, with different trends in the two physical fields. We next compare time integration and mesh selection for each scheme.

**Time-integrator comparison.**

Table 2 compares the terminal errors of Euler, RK4 and C–N on the fixed spatial grid with the same time step. Error reductions are relative to Euler, while differences between RK4 and C–N are relative to RK4.

**Table 2. Maximum absolute errors of the time integrators on the fixed grid. The smallest entry in each row is bold.**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">Case</th><th scope="col">Method</th><th scope="col">Field</th><th scope="col">Euler</th><th scope="col">RK4</th><th scope="col">C–N</th></tr></thead>
<tbody>
<tr>
<th rowspan="6" scope="rowgroup">One-soliton (p=1, q=2)</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td><strong>1.559149e-03</strong></td>
<td>1.560308e-03</td>
<td>1.560309e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.228608e-03</strong></td>
<td>3.229398e-03</td>
<td>3.229404e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td><strong>1.186363e-02</strong></td>
<td>1.187746e-02</td>
<td>1.187746e-02</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>7.210650e-03</strong></td>
<td>7.254773e-03</td>
<td>7.254804e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td><strong>1.160637e-03</strong></td>
<td>1.161402e-03</td>
<td>1.161404e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.008253e-03</strong></td>
<td>3.008503e-03</td>
<td>3.008508e-03</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">One-soliton (p=4, q=−3)</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>6.674179e-05</td>
<td><strong>6.639277e-05</strong></td>
<td>6.639418e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.968001e-05</td>
<td><strong>6.664598e-05</strong></td>
<td>6.664697e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>1.302977e-04</td>
<td>1.266358e-04</td>
<td><strong>1.266346e-04</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>8.322184e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.194314e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>7.824931e-05</td>
<td><strong>7.809306e-05</strong></td>
<td>7.809446e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.738482e-05</td>
<td><strong>6.429802e-05</strong></td>
<td>6.429896e-05</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">Two-soliton</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>1.306127e-04</td>
<td><strong>1.299876e-04</strong></td>
<td>1.299912e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.332472e-04</td>
<td><strong>1.267185e-04</strong></td>
<td>1.267211e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>2.745545e-04</td>
<td><strong>2.620490e-04</strong></td>
<td>2.620512e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.986149e-04</td>
<td><strong>1.405303e-04</strong></td>
<td>1.405323e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>1.447371e-04</td>
<td><strong>1.442262e-04</strong></td>
<td>1.442298e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.300531e-04</td>
<td><strong>1.242170e-04</strong></td>
<td>1.242195e-04</td>
</tr>
</tbody>
</table></div>

Across all eighteen comparisons, the relative difference between RK4 and C–N is below 0.003%. At the tested spatial resolution and time step, the two methods give nearly identical terminal errors.

Replacing Euler by RK4 reduces the PE and FD errors for the one-soliton solution with p=4 and q=−3 and the two-soliton case by 0.20%–0.52% in u and 4.35%–4.90% in v. PF is more sensitive: its u errors decrease by 2.81% and 4.55%, and its v errors by 25.6% and 29.2%, respectively. The trend reverses for the one-soliton solution with p=1 and q=2, where RK4 errors exceed Euler errors by 0.0083%–0.612%. Under these settings, the largest effect of time integration occurs in the PF v field; the RK4–C–N difference is much smaller than the change from Euler. RK4 is used for the remaining mesh comparisons and field plots.

**Fixed and moving meshes.**

Table 3 compares fixed and moving meshes for each spatial scheme, with identical node counts, RK4, time step and final time. Each cell lists $E_u$ followed by $E_v$. Reductions are relative to the corresponding fixed-grid errors.

**Table 3. Maximum absolute errors on fixed and moving meshes with RK4. Each cell gives $E_u/E_v$; the smaller error for each field is bold.**

<div class="table-wrap"><table class="comparison paired-errors"><thead><tr><th>Case</th><th>Method</th><th>Fixed mesh: u / v</th><th>Moving mesh: u / v</th></tr></thead><tbody><tr><th>One-soliton (p=1, q=2)</th><th>PE</th><td>1.560308e-03 / 3.229398e-03</td><td><strong>1.198143e-03 / 2.172159e-03</strong></td></tr><tr><th>One-soliton (p=1, q=2)</th><th>PF</th><td>1.187746e-02 / 7.254773e-03</td><td><strong>3.940103e-03 / 3.703664e-03</strong></td></tr><tr><th>One-soliton (p=1, q=2)</th><th>FD</th><td>1.161402e-03 / 3.008503e-03</td><td><strong>8.878667e-04 / 1.960738e-03</strong></td></tr><tr><th>One-soliton (p=4, q=−3)</th><th>PE</th><td>6.639277e-05 / 6.664598e-05</td><td><strong>4.533361e-05 / 5.568003e-05</strong></td></tr><tr><th>One-soliton (p=4, q=−3)</th><th>PF</th><td>1.266358e-04 / 6.194167e-05</td><td><strong>8.467373e-05 / 4.606240e-05</strong></td></tr><tr><th>One-soliton (p=4, q=−3)</th><th>FD</th><td>7.809306e-05 / 6.429802e-05</td><td><strong>5.709006e-05 / 5.387754e-05</strong></td></tr><tr><th>Two-soliton</th><th>PE</th><td>1.299876e-04 / 1.267185e-04</td><td><strong>8.193645e-05 / 8.860848e-05</strong></td></tr><tr><th>Two-soliton</th><th>PF</th><td>2.620490e-04 / 1.405303e-04</td><td><strong>1.626438e-04 / 8.423511e-05</strong></td></tr><tr><th>Two-soliton</th><th>FD</th><td>1.442262e-04 / 1.242170e-04</td><td><strong>9.643247e-05 / 8.548888e-05</strong></td></tr></tbody></table></div>

Moving-mesh errors are lower in all eighteen field comparisons, with reductions of 16.2%–66.8%. The ranges are 16.5%–37.0% for PE, 25.6%–66.8% for PF and 16.2%–34.8% for FD. PF improves most for the one-soliton solution with p=1 and q=2, with reductions of 66.8% in u and 48.9% in v. In the two-soliton case, both fields improve by approximately 30%–40% across the three schemes.

At the same node count, conserved-density-based placement and motion consistently improve both physical fields for all three schemes. The response to mesh allocation and motion is substantially larger than the below-0.003% difference between RK4 and C–N in Table 2.

**One-soliton (p=1, q=2): fields and errors.**

The field plots compare PE, PF and FD throughout. To display the spatial wave profiles, all three schemes are computed on $x\in[-40,40)$ and $y\in[-30,30)$ using a fixed grid, RK4, $\Delta x=0.15625$, $h=0.125$, $\Delta t=1.25\times10^{-4}$ and $T=0.01$. Tables 1–3 use the smaller domain and common evaluation grid specified above; Figures 1–6 show the expanded-domain fields and pointwise errors.

Each figure has three columns, ordered PE, PF and FD, and four rows showing the u surface, u contours, v surface and v contours. Error figures use the same arrangement for $|u_{\rm num}-u_*|$ and $|v_{\rm num}-v_*|$. Colour scales and height ranges are shared across methods for the same quantity.

Both physical fields of the one-soliton solution with p=1 and q=2 are negative pulses along an oblique line. Figure 1 shows the local profiles on $x\in[-3,4]$, $y\in[-3,3]$, and Figure 2 shows the errors on the same region, comparing the profiles and locations of deviations across methods.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_fields.png" alt="One-soliton (p=1, q=2): numerical physical fields comparison" loading="lazy"></a><figcaption>Figure 1. One-soliton (p=1, q=2): numerical physical fields. Columns: PE, PF, FD. Rows: u surface, u contours, v surface and v contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_errors.png" alt="One-soliton (p=1, q=2): absolute errors comparison" loading="lazy"></a><figcaption>Figure 2. One-soliton (p=1, q=2): absolute errors. Columns: PE, PF, FD. Rows: u error surface, u error contours, v error surface and v error contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

**One-soliton (p=4, q=−3): fields and errors.**

For the one-soliton solution with p=4 and q=−3, u is a positive pulse and v a negative pulse. Figures 3 and 4 show the fields and absolute errors on $x,y\in[-30,30]$, with the method order, panel arrangement and numerical parameters of Figures 1 and 2. The surfaces and contours compare the wave locations and errors along the wave bands.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_fields.png" alt="One-soliton (p=4, q=−3): numerical physical fields comparison" loading="lazy"></a><figcaption>Figure 3. One-soliton (p=4, q=−3): numerical physical fields. Columns: PE, PF, FD. Rows: u surface, u contours, v surface and v contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_errors.png" alt="One-soliton (p=4, q=−3): absolute errors comparison" loading="lazy"></a><figcaption>Figure 4. One-soliton (p=4, q=−3): absolute errors. Columns: PE, PF, FD. Rows: u error surface, u error contours, v error surface and v error contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

**Two-soliton fields and errors.**

The two-soliton solution contains two sets of spectral parameters. Figure 5 shows the two wave bands and their interaction on $x,y\in[-30,30]$. Relative to the one-soliton profiles, the contours bend and develop local extrema near the intersection. Figure 6 compares the errors near the interaction and along the distant wave bands.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_fields.png" alt="Two-soliton: numerical physical fields comparison" loading="lazy"></a><figcaption>Figure 5. Two-soliton: numerical physical fields. Columns: PE, PF, FD. Rows: u surface, u contours, v surface and v contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_errors.png" alt="Two-soliton: absolute errors comparison" loading="lazy"></a><figcaption>Figure 6. Two-soliton: absolute errors. Columns: PE, PF, FD. Rows: u error surface, u error contours, v error surface and v error contours. RK4, fixed mesh, T = 0.01. Each quantity uses a common colour scale across methods.</figcaption></figure>

## 4. Conclusion {#en-conclusion}

The combination of a staggered lattice and a shifted operator parameter generates both semi-discrete DLW bilinear relations from a common Gram determinant sequence. Rank-one updates yield exact solutions of arbitrary finite order, and logarithmic transformations lead to the PE and PF formulations. Both recover the same physical fields on positive τ-function solutions and are linked to the Darboux–Lax compatibility relations and second-order continuum limits.

In numerical computation, the choice of formulation affects the errors in the physical fields. On the fixed grid with RK4, PF u errors are approximately 1.91–7.61 times the PE errors. PE reduces u errors relative to FD by about 15.0% and 9.87% for the one-soliton solution with p=4 and q=−3 and the two-soliton case, while v comparisons depend on the spectral parameters. RK4 and C–N terminal errors differ by less than 0.003%; replacing Euler by RK4 has its largest effect on PF v, reducing errors by 25.6% and 29.2% in these two cases. Conserved-density-based node placement and motion reduce all eighteen field errors by 16.2%–66.8%. The common semi-discrete structure therefore leads to distinct numerical behaviour: the nonlinear representation changes the distribution of error between fields, the influence of time integration depends on the evolved variables, and SAMM improves both fields in all three tests.

## Data and code availability {#en-data}

The theoretical derivations and numerical materials are provided in [DLW theory](../notebook/DLW理论.ipynb) and [DLW numerical analysis](../notebook/DLW数值分析report.ipynb). The numerical notebook contains parameters, executable code and saved results; the tables use these recorded data. The expanded-domain comparisons additionally use the [field preparation script](../Workspaces/dlw_paper_20261009/prepare_comparison_fields.py) and [plotting script](../Workspaces/dlw_paper_20261009/plot_comparison_fields.py).

## References {#en-references}

[1] M. Boiti, J.J.-P. Leon, F. Pempinelli. Spectral transform for a two spatial dimension extension of the dispersive long wave equation. *Inverse Problems* **3** (1987), 371–387. [DOI](https://doi.org/10.1088/0266-5611/3/3/007).

[2] M. Wang, Y. Zhou, Z. Li. A nonlinear transformation of the dispersive long wave equations in (2+1) dimensions and its applications. *Journal of Nonlinear Mathematical Physics* **5** (1998), 120–125. [DOI](https://doi.org/10.2991/jnmp.1998.5.2.2).

[3] K. Sun, B. Tian, W.-J. Liu, M. Li, Q.-X. Qu, Y. Jiang. Symbolic-computation study on the (2+1)-dimensional dispersive long wave system. *SIAM Journal on Applied Mathematics* **70** (2010), 2259–2272. [DOI](https://doi.org/10.1137/090774847).

[4] J. Hu, Z.-W. Xu, G.-F. Yu. Determinant structure for the (2+1)-dimensional dispersive long wave system. *Applied Mathematics Letters* **62** (2016), 76–83. [DOI](https://doi.org/10.1016/j.aml.2016.07.003).

[5] H.-H. Sheng, G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. *Physica D* **432** (2022), 133140. [DOI](https://doi.org/10.1016/j.physd.2021.133140).

[6] X.-B. Hu, G.-F. Yu. Integrable discretizations of the (2+1)-dimensional sinh-Gordon equation. *Journal of Physics A: Mathematical and Theoretical* **40** (2007), 12645–12659. [DOI](https://doi.org/10.1088/1751-8113/40/42/S10).

[7] Y. Zhang, X. Chang, J. Hu, X. Hu, H.-W. Tam. Integrable discretization of soliton equations via bilinear method and Bäcklund transformation. *Science China Mathematics* **58** (2015), 279–296. [DOI](https://doi.org/10.1007/s11425-014-4952-6). [Preprint](https://arxiv.org/abs/1411.0476).

[8] G.-F. Yu, Z.-W. Xu. Dynamics of a differential-difference integrable (2+1)-dimensional system. *Physical Review E* **91** (2015), 062902. [DOI](https://doi.org/10.1103/PhysRevE.91.062902).

[9] B.-F. Feng, H.-H. Sheng, G.-F. Yu. Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation. *Numerical Algorithms* **94** (2023), 351–370. [DOI](https://doi.org/10.1007/s11075-023-01504-1).

# （2+1）维 DLW 系统的半离散化、Darboux–Lax 表示与数值模拟 {#zh-title}

 **摘要。** 本文构造（2+1）维色散长波（DLW）方程的交错半离散双线性系统，并给出其 Gram 行列式解。通过相邻辅助层之间的秩一更新，建立任意有限阶行列式满足的双线性恒等式。对共同的对数势作格点差分消元或引入势变量，得到两种非线性表示；它们由同一正 τ 函数对恢复相同的物理场，并具有相应的 Darboux–Lax 表示。进一步建立二阶一致性，以及固定正则谱参数下精确 Gram 解族在紧集上的一致二阶连续极限。数值实验以连续方程的直接差分为参照，比较非线性表示、时间算法及自适应动网格方法的影响。在固定网格算例中，差分消势形式的 u 误差均小于势函数形式；RK4 与 Crank–Nicolson 的终止误差相对差异小于 0.003%；动网格使所报告比较中的两个物理场误差降低 16.2%—66.8%。

**关键词：** 色散长波方程；半离散化；Gram 行列式；Darboux–Lax 表示；连续极限；自适应动网格

## 1. 引言 {#zh-intro}

（2+1）维色散长波（DLW）系统描述长波运动，其逆散射、精确解变换与双线性结构已得到研究。早期工作建立了谱变换方法 [1]，随后研究给出了精确解变换 [2] 与双线性 Bäcklund 变换 [3]。在 Sato 理论及 Hirota 方法框架下，已有研究获得了行列式解 [4]。进一步通过 KP 层级约化，得到了描述孤子、呼吸子和有理波的 Gram 行列式解 [5]。这些结果将非线性物理场与共同的 τ 函数结构联系起来。

已有研究表明，DLW 的双线性表示与修正 KP 层级相联系，并可通过适当的参数选取和变量互换联系到（2+1）维 sinh-Gordon 系统 [5]。后者的双线性系统已有半离散与全离散版本，以及相应的 Bäcklund 变换和 Lax 对 [6]。孤子方程的可积离散化受到广泛关注，Hirota 双线性方法为构造连续系统的离散对应提供了框架 [6–8]。在这一框架下，双线性方程与 Bäcklund 变换的相容性已用于导出包括扩展 KdV 和 KP 方程在内的半离散系统 [7]。在（2+1）维情形，双线性构造还给出了与 KP、Zakharov 方程相关的半离散系统，并得到其 N 孤子解与孤子共振现象 [8]。这些进展为在双线性框架下研究 DLW 系统的半离散对应提供了途径。

本文沿 y 方向构造（2+1）维 DLW 方程的半离散双线性系统，并给出其 Gram 行列式解。通过两种因变量变换，得到由同一对 τ 函数恢复相同物理场的两种非线性表示，并建立相应的 Darboux–Lax 表示和二阶连续极限。随后构造数值格式，通过单孤子和二孤子计算研究非线性表示、时间积分与自适应动网格（SAMM）方法对误差的影响。数值比较沿用半离散孤子系统用于自适应计算的研究思路 [9]。

本文安排如下。第 2 节从连续 DLW 系统及其双线性表示出发，构造半离散双线性方程与 Gram 行列式解，导出两种非线性表示，并建立连续极限与 Darboux–Lax 表示。第 3 节介绍数值格式及单孤子、二孤子实验，考察非线性表示、时间积分和 SAMM 方法的影响。第 4 节给出结论。

## 2. 半离散 DLW 系统与精确解 {#zh-continuous}

本节先介绍连续 DLW 系统及其双线性表示，作为半离散构造的起点。随后给出 Gram 行列式解与两种非线性表示，并建立相应的连续极限和 Darboux–Lax 表示。

### 2.1 连续 DLW 系统与双线性形式 {#zh-preliminaries}

考虑文献 [5] 中取 $\lambda=-2$ 后的（2+1）维 DLW 系统，

<a id="zh-eq-1"></a>

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

其中 $a\in\mathbb R$ 为常数。对于正 τ 函数 f、g，引入因变量变换

<a id="zh-eq-2"></a>

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

相应的双线性表示为 [5]

<a id="zh-eq-3"></a>

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

其中 $B_s=D_x^2+D_t+2sD_x$，Hirota 双线性算子定义为

<a id="zh-eq-4"></a>

$$D_x^rD_y^sD_t^m f\cdot g=\left.(\partial_x-\partial_{x\prime})^r(\partial_y-\partial_{y\prime})^s(\partial_t-\partial_{t\prime})^m f(x,y,t)g(x\prime,y\prime,t\prime)\right|_{(x\prime,y\prime,t\prime)=(x,y,t)}.\tag{4}$$

这里 r、s、m 为非负整数。下面的命题说明双线性方程与物理场之间的关系。

**命题 2.1（双线性表示 [5]）。** 设充分光滑的正函数 f、g 满足 [(3)](#zh-eq-3)，则由 [(2)](#zh-eq-2) 定义的物理场满足 DLW 系统 [(1)](#zh-eq-1)。

**证明。** 将双线性方程除以 fg，将 Hirota 算子展开为对数导数，再代入 [(2)](#zh-eq-2)，即得 [(1)](#zh-eq-1) 中的两条方程，参见 [5，第 2 节]。□

连续 Gram 行列式解由下式给出 [5]：

<a id="zh-eq-5"></a>

$$\tau_n^{(0)}=\det_{1\le i,k\le N}\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\left(-\frac{p_i-a}{q_k+a}\right)^n e^{\xi_i+\eta_k}\right],\quad f=\tau_1^{(0)},\quad g=\tau_0^{(0)},\tag{5}$$

<a id="zh-eq-6"></a>

$$\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad \eta_k=q_kx+q_k^2t+\frac{y}{q_k+a}.\tag{6}$$

其中 N 为行列式阶数，n 为辅助整数指标，实参数应使所有分母非零。物理场定义在 f、g 为正的区域内。

### 2.2 半离散双线性方程 {#zh-bilinear}

基于上述双线性表示，我们沿 y 方向构造 DLW 系统的半离散化，并保留 x、t 为连续变量。从连续双线性方程出发，对 [(3)](#zh-eq-3) 的第一式关于 y 求导，再结合第二式，得到

<a id="zh-eq-7"></a>

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{7}$$

将第二因子的平移与算子参数的平移结合起来，令

<a id="zh-eq-8"></a>

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t).\tag{8}$$

此时 $\Phi(0)=B_af\cdot g$，$\Phi\prime(0)=B_af\cdot g_y+2D_xf\cdot g$。取对称位移 $s=\pm h/2$，得到

<a id="zh-eq-9"></a>

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{9}$$

τ 函数 $F_j$、$G_j$ 分别对应半格点 $y=(j+\tfrac12)h$ 上的 f 与整数格点 $y=jh$ 上的 g。这一对应下 Gram 行列式解的收敛性将在第 2.5 节建立。

对称 Taylor 展开给出

<a id="zh-eq-10"></a>

$$\frac{\Phi(h/2)+\Phi(-h/2)}2=B_af\cdot g+O(h^2),\qquad \frac{\Phi(h/2)-\Phi(-h/2)}h=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{10}$$

因此，两条格点关系的平均与差商以二阶精度恢复连续双线性方程。

### 2.3 Gram 行列式解 {#zh-gram}

记 $d=h/2$、$\lambda_h(z)=(z+d)/(z-d)$，定义行列式序列

<a id="zh-eq-11"></a>

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{11}$$

其中 $\delta_{ik}$ 为 Kronecker 符号。零层行列式与 s 无关，记为 $\tau_0(j)$。

**定理 2.2（Gram 行列式解）。** 设 $h>0$、$N\ge1$，实参数 $p_i,q_i,\rho_i$ 对所有 i、k 满足 $p_i+q_k\ne0$、$p_i-a\pm d\ne0$、$q_k+a\pm d\ne0$。则

<a id="zh-eq-12"></a>

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{12}$$

对所有格点 j 满足半离散双线性系统 [(9)](#zh-eq-9)。

下面验证这些 Gram 行列式确实满足半离散双线性方程。为此，先建立行列式序列相邻辅助层之间的恒等式。

**引理 2.3（相邻层恒等式）。** 在定理 2.2 的谱参数条件下，固定 j 和 s，并设 $p_i-s\ne0$、$q_k+s\ne0$。则对任意 $n\in\mathbb Z$，有

<a id="zh-eq-13"></a>

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{13}$$

**证明。** 将第 n 层 Gram 矩阵写成 $M=I+(r_ic_k/(p_i+q_k))$，其中

<a id="zh-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{14}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义可得

<a id="zh-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{15}$$

其中的辅助层移位关系来自恒等式

<a id="zh-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{16}$$

在 M 可逆处，记

<a id="zh-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{17}$$

最后一个等式由矩阵行列式引理得到，而 Jacobi 微分公式给出 $\kappa=\tau_{n,x}/\tau_n$。为收集求导产生的项，记

<a id="zh-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{18}$$

利用 $H_x=-HM_xH$、$H_t=-HM_tH$，逐项求导得到

<a id="zh-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{19}$$

例如 $z_x=HPr-\kappa z$，故 $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$。对其再求一次导数，并消去 $\eta_1,\eta_2$，得到

<a id="zh-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{20}$$

因此 $\psi=1-\zeta$ 满足

<a id="zh-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{21}$$

对于 $f=\psi g$，展开双线性算子可得

<a id="zh-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{22}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，即在 M 可逆处得到 [(13)](#zh-eq-13)。为将结论延伸至奇异矩阵，将所有 $\rho_i$ 替换为 $\varepsilon\rho_i$。在固定 x、t 处，$\varepsilon=0$ 时 M 为单位矩阵，双线性残差在 ε 的零点邻域内为零。该残差是 ε 的多项式，故恒等于零。令 $\varepsilon=1$ 即完成证明。□

**定理 2.2 的证明。** 在引理 2.3 中取 $n=0$、$s=a-d$，即得第一条方程。对于第二条，逐矩阵元的恒等式

<a id="zh-eq-23"></a>

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{23}$$

给出

<a id="zh-eq-24"></a>

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{24}$$

在格点 $j+1$ 处应用引理，并取 $n=0$、$s=a+d$，得到

<a id="zh-eq-25"></a>

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{25}$$

即得第二条双线性方程。□

在引入非线性变量之前，先给出保证 τ 函数为正的充分条件。

**命题 2.4（正 τ 函数）。** 若 $0<p_1<\cdots<p_N<a-h/2$、$0<q_1<\cdots<q_N$、$\rho_i>0$，则对所有 x、t、j 有 $F_j\ge1$、$G_j\ge1$。

**证明。** 两个矩阵均可写成 $I+D_1CD_2$，其中 $D_1,D_2$ 为正对角矩阵，$C_{ik}=1/(p_i+q_k)$。每个非空主子式均为正，因为

<a id="zh-eq-26"></a>

$$\det C_{I,I}=\frac{\prod_{i<k,\ i,k\in I}(p_k-p_i)(q_k-q_i)}{\prod_{i,k\in I}(p_i+q_k)}>0.\tag{26}$$

正对角缩放保持这一性质。将 $\det(I+D_1CD_2)$ 展开为包括空主子式 1 在内的所有主子式之和，即得结论。□

### 2.4 非线性表示 {#zh-nonlinear}

下面导出半离散双线性系统的两种非线性表示。两种表示均采用如下由正 τ 函数恢复物理场的变换：

<a id="zh-eq-27"></a>

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad \omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad v_j=\frac4h\omega_j+\delta_0u_j,\qquad \delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h}.\tag{27}$$

物理场位于 $y=(j+\tfrac12)h$。上述定义给出连续变换 [(2)](#zh-eq-2) 的离散对应，其二阶一致性将在第 2.5 节建立。

令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。将两条双线性方程分别除以 $F_jG_j$ 和 $F_jG_{j+1}$，得到

<a id="zh-eq-28"></a>

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{28}$$

由物理场定义可得

<a id="zh-eq-29"></a>

$$(\alpha_j-\beta_j)_x=\frac{u_j+\omega_j}{2},\qquad (\alpha_j-\beta_{j+1})_x=\frac{u_j-\omega_j}{2}.\tag{29}$$

在 $A_j+C_j$ 中，二阶导数项合并为 $(2\alpha_j+\beta_j+\beta_{j+1})_{xx}$。因此引入

<a id="zh-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{30}$$

分别对 $A_j+C_j=0$ 和 $A_j-C_j=0$ 关于 x 求导，得到

<a id="zh-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{31}$$

下面从这些演化方程出发，导出两种非线性表示。第一种通过格点差分消去 $Z_j$，第二种则利用势变量表示 $Z_j$。对于第一种表示，引入后向差分算子与平均算子

<a id="zh-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{32}$$

由 $u_j,\omega_j,Z_j$ 的定义可得

<a id="zh-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{33}$$

对第一条演化方程施加 $\delta_-$，并代入上述恒等式，得到差分消势形式（PE）

<a id="zh-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{34}$$

对于第二种表示，引入势变量 $M_j=\beta_{j,x}$。由定义可得

<a id="zh-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{35}$$

代入后，第一条演化方程中出现组合 $u_{j,x}+u_j^2/2$。因此引入

<a id="zh-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{36}$$

从而

<a id="zh-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{37}$$

由求导前的关系 $(A_j+C_j)/2=0$，得到

<a id="zh-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{38}$$

第二条演化方程中的通量可写为

<a id="zh-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{39}$$

为消去其中的商，定义

<a id="zh-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{40}$$

利用恒等式

<a id="zh-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{41}$$

ω 的方程化为

<a id="zh-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{42}$$

由于

<a id="zh-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{43}$$

代入 Q 的方程即得 R 的演化方程。结合格点约束，得到势函数形式（PF）

<a id="zh-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{44}$$

其中 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。物理场由下式恢复：

<a id="zh-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{45}$$

下面的命题说明，两种非线性表示由同一对正 τ 函数恢复完全相同的物理场。

**命题 2.5（共同物理场）。** 设正函数 F、G 满足 [(9)](#zh-eq-9)。由它们构造的两种非线性表示在每个有限正格距 h 下给出完全相同的物理场 u、v。

**证明。** 由定义有

<a id="zh-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{46}$$

在第二个等式两侧加上相同的 u 中心差分，即得两种重构的 v 也一致。□

### 2.5 连续极限 {#zh-limits}

在得到两种非线性表示后，下面考察它们在 $h\to0$ 时的连续极限。首先建立物理场重构及半离散方程与相应连续表达之间的二阶一致性。随后证明，在固定正则谱参数下，Gram 行列式解以 $h^2$ 阶误差在紧集上一致收敛到连续 DLW 解。

本小节中，$O_K(h^m)$ 表示在紧集 K 上由 $C_Kh^m$ 一致控制的余项，所涉及函数在 K 的开邻域内光滑。下面的命题联系交错重构与连续因变量变换。

**命题 2.6（重构的一致性）。** 设 f、g 为正光滑函数，u、v 由 [(2)](#zh-eq-2) 给出。在物理位置 y 处定义

<a id="zh-eq-47"></a>

$$\begin{aligned}u^{[h]}(y)&=\partial_x[2\log f(y)-\log g(y-h/2)-\log g(y+h/2)],\\\omega^{[h]}(y)&=\partial_x[\log g(y+h/2)-\log g(y-h/2)],\\v^{[h]}(y)&=\frac4h\omega^{[h]}(y)+\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}.\end{aligned}\tag{47}$$

上式省略了 x、t 变量。则

<a id="zh-eq-48"></a>

$$u^{[h]}=u+O_K(h^2),\qquad v^{[h]}=v+O_K(h^2).\tag{48}$$

**证明。** 记 $\alpha=\log f$、$\beta=\log g$。对称 Taylor 展开给出

<a id="zh-eq-49"></a>

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad \frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).\tag{49}$$

第一个展开式求导后仍成立，因此

<a id="zh-eq-50"></a>

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2),\qquad v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2).\tag{50}$$

即得结论。□

下面考察非线性方程。令

<a id="zh-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{51}$$

第一种表示可写为

<a id="zh-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{52}$$

记 $\mathcal M_+z_j=(z_{j+1}+z_j)/2$。由 $\mathcal M_+\delta_-=\delta_0$ 可知，$\mathcal M_+E_{1,h,j}+E_{2,h,j}=0$ 给出 v 的演化方程。

**命题 2.7（方程的一致性）。** 将光滑场 u、v 采样于 $y_j=(j+\tfrac12)h$，并记连续 DLW 方程的残差为

<a id="zh-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{53}$$

则在紧集上一致有

<a id="zh-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{54}$$

**证明。** 记 $m_j=y_j-h/2$。Taylor 展开给出

<a id="zh-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{55}$$

从而

<a id="zh-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{56}$$

上述展开在所需导数下仍成立，由此得到 $E_{1,h,j}=\mathcal C_1(m_j)+O_K(h^2)$。令 $w=v-u_y$，第二个残差为

<a id="zh-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{57}$$

将第一个残差在 y_j 两侧取平均，再加上第二个残差，得到

<a id="zh-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{58}$$

上式所有连续场均在 y_j 处取值，即得第二个结论。□

最后建立精确 Gram 解的连续极限。此时 τ 函数通过格点乘子和辅助参数的平移依赖于 h。

**定理 2.8（Gram 解的连续极限）。** 固定 N 和谱参数，并设存在 $h_0>0$ 使

<a id="zh-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{59}$$

对于 $0<h\le h_0$，将正格点乘子延拓到实数指数，并定义

<a id="zh-eq-60"></a>

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{60}$$

因此 $g^{(h)}(x,jh,t)=G_j$，$f^{(h)}(x,(j+\tfrac12)h,t)=F_j$。记其交错重构为 $u^{(h)},v^{(h)}$，并令 $f^{(0)},g^{(0)}$ 为 [(5)](#zh-eq-5) 中的连续 Gram 函数。相应物理场 $u^{(0)},v^{(0)}$ 满足连续 DLW 系统，且对任意紧集 K 有

<a id="zh-eq-61"></a>

$$\sup_K\bigl(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\bigr)\le C_Kh^2\tag{61}$$

其中 h 为充分小的正数。该估计对两种非线性表示均成立。

**证明。** 记 $z_i=p_i-a$、$w_k=q_k+a$。对于固定谱参数，

<a id="zh-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{62}$$

因此指数项中 y 的系数满足

<a id="zh-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{63}$$

对于 $f^{(h)}$，辅助参数平移与半格点平移共同给出振幅因子

<a id="zh-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}+O(h^2).\end{aligned}\tag{64}$$

因此相位和振幅与相应连续表达均相差 $O(h^2)$。由于 N 固定，对任意固定混合导数 $\partial^\nu$ 有

<a id="zh-eq-65"></a>

$$\partial^\nu(f^{(h)}-f^{(0)})=O_K(h^2),\qquad \partial^\nu(g^{(h)}-g^{(0)})=O_K(h^2).\tag{65}$$

命题 2.4 的正性论证同样适用于实数指数延拓及其极限。四个 τ 函数均不小于 1，因此相应对数导数也满足一致二阶估计。

相邻层恒等式和格点移位关系在延拓后仍成立，因此

<a id="zh-eq-66"></a>

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.\tag{66}$$

利用上述一致导数界，对两式取对称平均与差商，再令 h 趋于零，得到

<a id="zh-eq-67"></a>

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.\tag{67}$$

这正是第 2.2 节中的连续双线性方程等价形式，故由命题 2.1 得到连续 DLW 解。最后，将命题 2.6 一致地应用于依赖 h 的解族，得到

<a id="zh-eq-68"></a>

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).\tag{68}$$

结合 [(65)](#zh-eq-65) 即得所需估计。由命题 2.5，该结论同时适用于两种非线性表示。□

### 2.6 Darboux–Lax 表示 {#zh-lax}

下面构造半离散 DLW 系统的 Darboux–Lax 表示。首先以物理场写出线性问题，再给出它在势变量 Q、R、M 下的形式。

引入平移后的变量

<a id="zh-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{69}$$

第一种非线性表示可写为

<a id="zh-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{70}$$

为构造线性问题，引入辅助势 V，满足

<a id="zh-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{71}$$

这两条关系的相容条件恰为第一条非线性方程。在局部 x 区间和格点链上，可以先在一个参考格点积分，再沿格点递推，构造辅助势 V；其自由度为所有格点共有的时间函数。

考虑如下辅助线性方程：

<a id="zh-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{72}$$

第一条方程联系相邻格点上的波函数，第二条给出它们的时间演化。下面的定理建立该线性系统与非线性方程之间的相容关系。

**定理 2.9（Darboux–Lax 相容性）。** 系统 [(70)](#zh-eq-70) 的每个光滑解，连同 [(71)](#zh-eq-71) 确定的辅助势，都使 [(72)](#zh-eq-72) 在形式算子意义下相容。反之，在 $w_j\ne0$ 的区域内，相容条件与辅助势的格点差关系共同推出 [(70)](#zh-eq-70)。

**证明。** 令

<a id="zh-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{73}$$

<a id="zh-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{74}$$

其中 $\mathscr B_j^{-1}$ 在形式伪微分算子代数中定义。线性系统写为 $\psi_{j+1}=T_j\psi_j$、$\psi_{j,t}=H_j\psi_j$。对格点关系关于 t 求导，并代入相邻两层的时间方程，得到

<a id="zh-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{75}$$

为验证该恒等式，定义标量残差

<a id="zh-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{76}$$

利用 $V_{j+1}-V_j=(h/2)w_{j,x}$，可得

<a id="zh-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{77}$$

由 w 的演化方程，两项残差之差为零；由 $V_{j,x}$ 的定义，两项残差之和也为零。因此 $\mathcal E_j^r=\mathcal E_j^s=0$。对于标量函数 r，乘积法则给出 Darboux 恒等式

<a id="zh-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{78}$$

由辅助势差关系，有

<a id="zh-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{79}$$

记

<a id="zh-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{80}$$

分别将 Darboux 恒等式用于两个为零的残差，得到

<a id="zh-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{81}$$

消去共同的中间算子，得到 $L_{j+1}T_j=T_jL_j$，即相容条件 [(75)](#zh-eq-75)。

反之，设相容条件与辅助势差关系成立。同样的算子计算给出

<a id="zh-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{82}$$

比较 $\partial_x^0$ 和 $\partial_x^{-1}$ 的系数，得到 $\mathcal E_j^r=\mathcal E_j^s$、$w_j\mathcal E_j^s=0$。因此在 $w_j\ne0$ 的区域内，两项残差均为零。两者之差给出 w 方程；两者之和经后向差分，并结合辅助势差关系，给出第一条非线性方程。□

对于 τ 函数解，可取

<a id="zh-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{83}$$

将双线性方程分别除以相应 τ 函数乘积，再对 x 求导，即得 $\mathcal E_j^r=\mathcal E_j^s=0$。因此 Gram 行列式解满足上述 Darboux–Lax 相容关系。

最后代入势变量关系

<a id="zh-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{84}$$

线性系统化为

<a id="zh-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{85}$$

对格点约束求 x 导数可得

<a id="zh-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{86}$$

Q、R 的演化方程使两项标量残差为零，从而保证线性系统相容。反之，当 $Q_jR_j\ne0$ 时，相容条件与该辅助势差关系共同恢复第一种表示的物理场方程。

上述构造给出了两种非线性表示共同的 Darboux–Lax 表示。格点平移通过共享中间势的两个一阶 Darboux 算子实现，其与时间演化的相容性由半离散场方程保证。

## 3. 数值方法与实验 {#zh-numerics}

本节基于两种非线性表示构造数值格式，并与连续 DLW 系统的直接差分方法进行比较。以连续精确解为参照，考察非线性表示及其离散实现、时间积分和自适应动网格（SAMM）方法对物理场误差的影响。

### 3.1 空间离散 {#zh-schemes}

**网格与差分算子。** 在固定网格上，取 $x_i=-L/2+i\Delta x$，其中 $\Delta x=L/N_x$。沿 y 方向，$M_j$ 位于 $y=jh$，而 $u_j,v_j,Q_j,R_j$ 位于 $y=(j+\tfrac12)h$。下标 j、i 分别表示 y 层与 x 节点。以下空间离散系统保留时间为连续变量。

对 x 导数采用三点中心差分

<a id="zh-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{87}$$

沿 y 方向采用

<a id="zh-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{88}$$

其中，$D_1,D_2$ 作用于 x 节点编号，$\delta_-,\delta_0,\mathcal M_-$ 作用于层编号。下文的乘积与商均按节点计算。我们先构造 PE 和 PF 格式，再给出作为比较对象的直接差分格式，记为 FD。

**PE 格式。** 取 $P=\delta_-u$ 和 $W=v-\delta_0u$ 为演化变量。在每个时刻，通过

<a id="zh-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{89}$$

恢复物理场。其中，$j_L$ 为最下层编号，$u_{j_L,i}(t)$ 由下边界数据给定。将重构的物理场代入 PE 方程，得到 $\dot P=F_P$、$\dot W=F_W$，其中

<a id="zh-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{90}$$

因此，计算演化右端时，先由 P 恢复 u，再对 u、W 施加相应的空间差分算子；物理场 v 由同一重构公式得到。

**PF 格式。** 取 Q、R 为演化变量，物理场由

<a id="zh-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{91}$$

恢复。演化方程还包含 $(M_j+M_{j+1})_x$。为计算这一项，引入 $m_j\simeq M_{j,x}$ 和 $S_j=Q_jR_j$。对格点约束 $M_{j+1}-M_j=h(1-S_j)$ 施加 $D_1$，得到

<a id="zh-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{92}$$

给定下边界的 m 后，即可利用这一关系逐层求出其余各层。将最下层临时编号为 0，由该层的 Q 方程确定起始值：

<a id="zh-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{93}$$

其中，$Q_0(t)$ 由下边界数据给定，$Q_{0,t}$ 为其时间导数。确定 m 后，演化方程为 $\dot Q_j=F_{Q,j}$、$\dot R_j=F_{R,j}$，其中

<a id="zh-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{94}$$

Q 的最下层取给定边界值，内部各层 Q 和所有层 R 按上述方程演化。随后通过式 (91) 恢复物理场。

**FD 格式。** 作为比较，直接离散连续 DLW 方程，取 $P=\delta_-u$ 和 v 为演化变量。物理场 u 由式 (89) 的第一个关系从 P 恢复。所得系统为 $\dot P=F_P$、$\dot v=F_v$，其中

<a id="zh-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{95}$$

上述三种空间离散分别与第 3.3 节的时间积分方法结合，初值及边界数据在第 3.4 节给出。

### 3.2 自适应动网格方法 {#zh-samm}

基于上述两种半离散 DLW 表示，我们利用其共同的守恒律构造以下自适应动网格方法。仅调整 x 节点的位置，y 方向格距 h 保持不变，所有 y 层共用一组 x 节点。引入密度与通量

<a id="zh-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{96}$$

将 $W_j=4(1-\rho_j)$ 代入其演化方程，得到

<a id="zh-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{97}$$

在 PF 形式中，$\rho_j=Q_jR_j$。由于所有 $y$ 层共用一组 $x$ 节点，对各层取平均作为网格密度和通量：

<a id="zh-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{98}$$

初始网格按 $\bar\rho(x,0)$ 的累积积分等分，即令相邻节点之间的密度积分相同。密度较大的区域因此分配更多节点。令左端节点 $x_L$ 固定，并保持每个移动节点对应的累积积分不变，利用[(97)](#zh-eq-97)得

<a id="zh-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{99}$$

因此节点速度为

<a id="zh-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{100}$$

计算时以 $D_1\rho$ 代替通量中的 $\partial_x\rho$，并要求 $\bar\rho>0$。FD 的动网格比较也采用[(96)](#zh-eq-96)、[(98)](#zh-eq-98)和[(100)](#zh-eq-100)确定节点速度。

物理节点移动后，相邻 $x$ 间距不再相等。为在同一节点编号上计算导数，引入固定均匀的计算坐标 $\xi_i=-L/2+i\Delta\xi$，其中 $\Delta\xi=L/N_x$。写 $x_i(t)=\xi_i+s_i(t)$，$s_i$ 是节点位移，$J_i=1+D_\xi s_i$ 近似坐标映射的伸缩率 $J=x_\xi$。

对于定义在移动节点上的场，链式法则给出 $\partial_x=J^{-1}\partial_\xi$。再作用一次该算子，就会对 $J^{-1}$ 求导，因而

<a id="zh-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{101}$$

分别以均匀 $\xi$ 网格上的中心差分近似这些导数，得到

<a id="zh-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{102}$$

$D_\xi,D_{\xi\xi}$ 为[(87)](#zh-eq-87)在均匀计算坐标上的三点差分。对随节点移动的任一演化变量 $z$，链式法则给出 $\dot z=F_z+\mathcal V D_1z$。因此，在第 3.1 节各时间变化率上加入 $\mathcal V D_1z$，并将节点方程[(100)](#zh-eq-100)与场变量同步推进。固定网格对应 $s=0,\mathcal V=0$。

### 3.3 时间积分 {#zh-time}

我们采用向前 Euler、经典四阶 Runge–Kutta（RK4）和 Crank–Nicolson（C–N）方法，对固定网格与动网格上的空间离散系统进行时间积分。将全部演化变量记为 $z$，所得系统统一写为 $\dot z=\mathcal F(t,z)$。对于 SAMM，$z$ 还包含节点坐标，$\mathcal F$ 包含网格输运项及节点速度。

取 $t_n=n\Delta t$，向前 Euler 方法为

<a id="zh-eq-103"></a>

$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n).\tag{103}$$

我们同时采用经典四级四阶 Runge–Kutta 方法（RK4）。每一级均根据该级的场变量与网格，重新计算物理场重构、辅助变量、空间差分及边界值。

Crank–Nicolson（C–N）方法取相邻两个时间层变化率的平均：

<a id="zh-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{104}$$

FD 方法中的 $v$ 方程写为 $v^{n+1}=v^n+\Delta t(F_v^n+F_v^{n+1})/2$。由于 $F_v^{n+1}$ 依赖未知的下一层解，需与 $P$ 的更新联立求解。以向前 Euler 格式给出的近似作为初值，迭代求解耦合的隐式方程。

### 3.4 算例与误差度量 {#zh-tests}

我们考虑连续 DLW 系统的单孤子与二孤子解。精确解用于给定初值和边界数据，并作为数值误差的评价基准。各算例统一取 $a=2$、行列式系数 $\rho_i=1$，初相位为零。

**单孤子解。** 当 $N=1$ 时，连续 Gram 行列式化为

<a id="zh-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{105}$$

其中

<a id="zh-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{106}$$

相应的物理场为

<a id="zh-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{107}$$

当 $p+q>0$、$c>0$ 时，u 脉冲的正负由 $c-1$ 决定，而 v 脉冲的正负由 $\ell$ 决定。我们选取 $(p,q)=(1,2)$ 和 $(4,-3)$，分别得到负的和正的 u 脉冲。第一组参数对应 $c=1/4$、$\ell=-3/4$；第二组对应 $c=2$、$\ell=-1/2$。两组参数的 v 场均为负脉冲。

**二孤子解。** 当 $N=2$ 时，展开 Gram 行列式可得

<a id="zh-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{108}$$

其中

<a id="zh-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{109}$$

物理场由 $u_*=2\partial_x\log(f_*/g_*)$ 和 $v_*=2\partial_x\partial_y\log(f_*g_*)$ 得到。对于二孤子解，取 $p_1=6$、$q_1=-5$、$p_2=4$、$q_2=-3$，相应地有 $c_1=4/3$、$c_2=2$、$A_{12}=4/3$。此时两相位分别为 $\theta_1=x-11t-y/12$ 和 $\theta_2=x-7t-y/2$，对应两个空间取向及传播速率不同的波。该算例将数值比较扩展到双波相互作用的情形。

**初值与边界数据。** PE 的初值取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$；FD 采用相同的 $P^0$，并取 $v^0=v_*(0)$。对于 PF，由 $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ 及归一化 $Q_{j,0}^0=1$ 确定 Q，再取 $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$。下边界的 $Q_0(t)$ 按同一关系由 $u_{*,0}(t)$ 确定。因此，三种格式采用共同的初始物理场。

计算域边界选在孤子尾部接近背景的位置。PE、FD 的 x 向差分采用周期边界，PF 按 Q、R 的左右端背景值处理边界。沿 y 方向，下侧取解析边界，上侧对数值解与解析背景之差作二次外推。

**计算设置与误差度量。**

表 1—3 的计算域为 $x\in[-20,20)$、$y\in[-1.5,1.5]$。取 $N_x=256$、固定网格间距 $\Delta x=0.15625$，沿 $y$ 方向取 24 个单元，格距 $h=0.125$。时间步长为 $\Delta t=1.25\times10^{-4}$，计算至 $T=0.01$。

在 $x\in[-10,10]$ 上取 4001 个等距点，并取全部 $y$ 层组成评价网格 $\mathcal G$。将各方法的数值物理场沿实际 $x$ 节点作三次样条插值，定义

<a id="zh-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{110}$$

### 3.5 数值结果 {#zh-results}

表 1 比较三种空间格式在共同初始物理场、相同固定网格和 RK4 时间推进下的最大绝对误差。PE 与 PF 的差别在 $u$ 场中较为突出：单孤子（p=1，q=2）、单孤子（p=4，q=−3） 和二孤子的 PF 误差分别为 PE 的约 7.61、1.91 和 2.02 倍。对于 $v$ 场，相应比值为 2.25、0.929 和 1.11。因而在这组三个算例中，PE 的 $u$ 误差均小于 PF，而两者的 $v$ 误差关系随孤子参数变化。

**表 1　固定网格、RK4 下的最大绝对误差。每行最小值加粗。**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">算例</th><th scope="col">场</th><th scope="col">PE</th><th scope="col">PF</th><th scope="col">FD</th></tr></thead>
<tbody>
<tr>
<th rowspan="2" scope="rowgroup">单孤子（p=1，q=2）</th>
<th scope="row">u</th>
<td>1.560308e-03</td>
<td>1.187746e-02</td>
<td><strong>1.161402e-03</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>3.229398e-03</td>
<td>7.254773e-03</td>
<td><strong>3.008503e-03</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">单孤子（p=4，q=−3）</th>
<th scope="row">u</th>
<td><strong>6.639277e-05</strong></td>
<td>1.266358e-04</td>
<td>7.809306e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.664598e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.429802e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">二孤子</th>
<th scope="row">u</th>
<td><strong>1.299876e-04</strong></td>
<td>2.620490e-04</td>
<td>1.442262e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.267185e-04</td>
<td>1.405303e-04</td>
<td><strong>1.242170e-04</strong></td>
</tr>
</tbody>
</table></div>

与 FD 相比，PE 在单孤子（p=4，q=−3） 和二孤子中的 $u$ 误差分别降低约 15.0% 和 9.87%，对应的 $v$ 误差则分别增加约 3.65% 和 2.01%；在单孤子（p=1，q=2） 中，PE 的 $u,v$ 误差分别高出约 34.3% 和 7.34%。PF 在单孤子（p=4，q=−3） 的 $v$ 场中取得表内最小误差，比 FD 低约 3.66%。相较于单孤子（p=1，q=2），PE 与 FD 在单孤子（p=4，q=−3） 及二孤子中的差异较小，且两个物理场的变化方向不同。以下对三种空间格式分别比较时间算法和网格选择。

**时间算法比较。**

在固定网格上保持空间分辨率与时间步长不变，表 2 比较 Euler、RK4 和 C–N 的终止时刻误差。以下相对降幅以 Euler 的误差为基准，RK4 与 C–N 的相对差异以 RK4 的误差为基准。

**表 2　固定网格上不同时间算法的最大绝对误差。每行最小值加粗。**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">算例</th><th scope="col">方法</th><th scope="col">场</th><th scope="col">Euler</th><th scope="col">RK4</th><th scope="col">C–N</th></tr></thead>
<tbody>
<tr>
<th rowspan="6" scope="rowgroup">单孤子（p=1，q=2）</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td><strong>1.559149e-03</strong></td>
<td>1.560308e-03</td>
<td>1.560309e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.228608e-03</strong></td>
<td>3.229398e-03</td>
<td>3.229404e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td><strong>1.186363e-02</strong></td>
<td>1.187746e-02</td>
<td>1.187746e-02</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>7.210650e-03</strong></td>
<td>7.254773e-03</td>
<td>7.254804e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td><strong>1.160637e-03</strong></td>
<td>1.161402e-03</td>
<td>1.161404e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.008253e-03</strong></td>
<td>3.008503e-03</td>
<td>3.008508e-03</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">单孤子（p=4，q=−3）</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>6.674179e-05</td>
<td><strong>6.639277e-05</strong></td>
<td>6.639418e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.968001e-05</td>
<td><strong>6.664598e-05</strong></td>
<td>6.664697e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>1.302977e-04</td>
<td>1.266358e-04</td>
<td><strong>1.266346e-04</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>8.322184e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.194314e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>7.824931e-05</td>
<td><strong>7.809306e-05</strong></td>
<td>7.809446e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.738482e-05</td>
<td><strong>6.429802e-05</strong></td>
<td>6.429896e-05</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">二孤子</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>1.306127e-04</td>
<td><strong>1.299876e-04</strong></td>
<td>1.299912e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.332472e-04</td>
<td><strong>1.267185e-04</strong></td>
<td>1.267211e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>2.745545e-04</td>
<td><strong>2.620490e-04</strong></td>
<td>2.620512e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.986149e-04</td>
<td><strong>1.405303e-04</strong></td>
<td>1.405323e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>1.447371e-04</td>
<td><strong>1.442262e-04</strong></td>
<td>1.442298e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.300531e-04</td>
<td><strong>1.242170e-04</strong></td>
<td>1.242195e-04</td>
</tr>
</tbody>
</table></div>

在全部十八组比较中，RK4 与 C–N 的误差相对差异均小于 0.003%。在本组空间分辨率与时间步长下，两种时间算法给出近乎相同的终止时刻误差。

从 Euler 改为 RK4 时，单孤子（p=4，q=−3） 与二孤子的 PE、FD 两种格式在 $u$ 场上的误差降幅为 0.20%—0.52%，在 $v$ 场上的降幅为 4.35%—4.90%。PF 对这一更换更为敏感：两组算例的 $u$ 误差分别降低 2.81% 和 4.55%，$v$ 误差分别降低 25.6% 和 29.2%。单孤子（p=1，q=2） 的变化方向相反，RK4 的误差比 Euler 高 0.0083%—0.612%。因此，在当前计算设置中，PF 的 $v$ 场是时间积分选择影响最明显的部分；RK4 与 C–N 之间的选择带来的误差变化远小于从 Euler 改为这两种方法的变化。后续网格比较及场图统一采用 RK4。

**固定网格与动网格。**

表 3 比较同一空间格式在固定网格与动网格上的误差，采用相同节点数、RK4 时间推进及相同时间步长与终止时刻。各单元格依次列出 $E_u$ 和 $E_v$；以下降幅均以对应的固定网格误差为基准。

**表 3　固定网格与动网格的最大绝对误差（RK4）。各单元格依次为 $E_u/E_v$；每个物理场较小的误差加粗。**

<div class="table-wrap"><table class="comparison paired-errors"><thead><tr><th>算例</th><th>方法</th><th>固定网格：u / v</th><th>动网格：u / v</th></tr></thead><tbody><tr><th>单孤子（p=1，q=2）</th><th>PE</th><td>1.560308e-03 / 3.229398e-03</td><td><strong>1.198143e-03 / 2.172159e-03</strong></td></tr><tr><th>单孤子（p=1，q=2）</th><th>PF</th><td>1.187746e-02 / 7.254773e-03</td><td><strong>3.940103e-03 / 3.703664e-03</strong></td></tr><tr><th>单孤子（p=1，q=2）</th><th>FD</th><td>1.161402e-03 / 3.008503e-03</td><td><strong>8.878667e-04 / 1.960738e-03</strong></td></tr><tr><th>单孤子（p=4，q=−3）</th><th>PE</th><td>6.639277e-05 / 6.664598e-05</td><td><strong>4.533361e-05 / 5.568003e-05</strong></td></tr><tr><th>单孤子（p=4，q=−3）</th><th>PF</th><td>1.266358e-04 / 6.194167e-05</td><td><strong>8.467373e-05 / 4.606240e-05</strong></td></tr><tr><th>单孤子（p=4，q=−3）</th><th>FD</th><td>7.809306e-05 / 6.429802e-05</td><td><strong>5.709006e-05 / 5.387754e-05</strong></td></tr><tr><th>二孤子</th><th>PE</th><td>1.299876e-04 / 1.267185e-04</td><td><strong>8.193645e-05 / 8.860848e-05</strong></td></tr><tr><th>二孤子</th><th>PF</th><td>2.620490e-04 / 1.405303e-04</td><td><strong>1.626438e-04 / 8.423511e-05</strong></td></tr><tr><th>二孤子</th><th>FD</th><td>1.442262e-04 / 1.242170e-04</td><td><strong>9.643247e-05 / 8.548888e-05</strong></td></tr></tbody></table></div>

在全部十八组物理场比较中，动网格的误差均低于固定网格，降幅为 16.2%—66.8%。按空间格式分别计算，PE 的降幅为 16.5%—37.0%，PF 为 25.6%—66.8%，FD 为 16.2%—34.8%。单孤子（p=1，q=2） 的 PF 改善最明显，其 $u,v$ 误差分别降低 66.8% 和 48.9%；二孤子中三种格式的两个场均降低约 30%—40%。

在相同节点数下，按守恒密度布点并推进节点，对三种格式和两个物理场均带来一致的误差改善。与表 2 中 RK4、C–N 小于 0.003% 的误差差异相比，这组算例对网格分配与运动的响应明显得多。

**单孤子（p=1，q=2）：物理场与误差。**

以下场图统一比较 PE、PF 和 FD，不再单独选择某一种方法。为展示波形的空间分布，三种方法均在 $x\in[-40,40)$、$y\in[-30,30)$ 上计算，采用固定网格、RK4、$\Delta x=0.15625$、$h=0.125$、$\Delta t=1.25\times10^{-4}$ 和 $T=0.01$。表 1—3 使用前述较小计算域和统一评价网格；图 1—6 展示扩域计算得到的物理场及其逐点误差。

每幅图均按三列四行排列：列从左至右为 PE、PF、FD；行依次为 $u$ 曲面、$u$ 等高线、$v$ 曲面、$v$ 等高线。误差图采用相同排列，绘制 $|u_{\rm num}-u_*|$ 和 $|v_{\rm num}-v_*|$。同一物理量在三列中使用共同色阶和高度范围，以便比较幅值。

单孤子（p=1，q=2） 的两个物理场均为沿斜直线分布的负脉冲。图 1 展示 $x\in[-3,4]$、$y\in[-3,3]$ 的局部波形，图 2 给出同一区域的误差。两幅图分别比较三种方法得到的波形和偏差位置。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_fields.png" alt="单孤子（p=1，q=2），PE/PF/FD三列四行数值物理场对照" loading="lazy"></a><figcaption>图 1　单孤子（p=1，q=2）的数值物理场。左、中、右列依次为 PE、PF、FD；第一、二行为 u 的曲面和等高线，第三、四行为 v 的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_errors.png" alt="单孤子（p=1，q=2），PE/PF/FD三列四行绝对误差对照" loading="lazy"></a><figcaption>图 2　单孤子（p=1，q=2）的绝对误差。左、中、右列依次为 PE、PF、FD；第一、二行为 u 误差的曲面和等高线，第三、四行为 v 误差的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

**单孤子（p=4，q=−3）：物理场与误差。**

单孤子（p=4，q=−3） 的 $u$ 为正脉冲，$v$ 为负脉冲。图 3、4 展示 $x,y\in[-30,30]$ 内的物理场与绝对误差，方法顺序、行排列和计算参数与图 1、2 相同。通过两场的曲面及等高线，可以同时比较波带的位置和误差沿波带的分布。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_fields.png" alt="单孤子（p=4，q=−3），PE/PF/FD三列四行数值物理场对照" loading="lazy"></a><figcaption>图 3　单孤子（p=4，q=−3）的数值物理场。左、中、右列依次为 PE、PF、FD；第一、二行为 u 的曲面和等高线，第三、四行为 v 的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_errors.png" alt="单孤子（p=4，q=−3），PE/PF/FD三列四行绝对误差对照" loading="lazy"></a><figcaption>图 4　单孤子（p=4，q=−3）的绝对误差。左、中、右列依次为 PE、PF、FD；第一、二行为 u 误差的曲面和等高线，第三、四行为 v 误差的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

**二孤子物理场与误差。**

二孤子包含两组谱参数。图 5 展示 $x,y\in[-30,30]$ 内的两条波带及其交汇结构；与单孤子相比，等高线在交汇区域发生弯曲，并形成局部极值。图 6 给出三种方法在该区域及远端波带上的误差分布，用于比较它们对同一二孤子结构的数值再现。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_fields.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_fields.png" alt="二孤子，PE/PF/FD三列四行数值物理场对照" loading="lazy"></a><figcaption>图 5　二孤子的数值物理场。左、中、右列依次为 PE、PF、FD；第一、二行为 u 的曲面和等高线，第三、四行为 v 的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_errors.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_errors.png" alt="二孤子，PE/PF/FD三列四行绝对误差对照" loading="lazy"></a><figcaption>图 6　二孤子的绝对误差。左、中、右列依次为 PE、PF、FD；第一、二行为 u 误差的曲面和等高线，第三、四行为 v 误差的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。</figcaption></figure>

## 4. 结论 {#zh-conclusion}

交错格点与算子参数的配合，使 DLW 的两条半离散双线性关系由同一 Gram 行列式链产生。其秩一更新给出任意有限阶精确解，对数变换则把这一构造传递到 PE 与 PF 两种非线性表示。两种表示在正 τ 函数解上恢复相同的物理场，并与 Darboux–Lax 相容关系及二阶连续极限相联系。

进一步用于计算时，表示方式影响各物理场的误差。固定网格、RK4 下，PF 的 $u$ 误差为 PE 的约 1.91—7.61 倍；PE 在单孤子（p=4，q=−3） 与二孤子中的 $u$ 误差又分别比 FD 低约 15.0% 和 9.87%，而 $v$ 场的比较随谱参数变化。时间方向，RK4 与 C–N 的终止误差相对差异小于 0.003%；从 Euler 改为 RK4 的影响以 PF 的 $v$ 场最为明显，在单孤子（p=4，q=−3） 与二孤子中分别降低 25.6% 和 29.2%。网格方向，守恒密度驱动的初始布点与节点运动使全部十八组误差降低 16.2%—66.8%。这些结果将共同的半离散结构与具体计算表现联系起来：非线性表示改变误差在两场中的分布，时间积分的影响依赖演化变量，而动网格在本组三个算例中对两场均有改善。

## 数据与代码说明 {#zh-data}

本文的理论推导与数值计算材料分别收录于随稿文件 [DLW理论.ipynb](../notebook/DLW理论.ipynb) 和 [DLW数值分析report.ipynb](../notebook/DLW数值分析report.ipynb)。数值文件包含算例参数、可执行计算代码及保存的图表输出；正文中的误差表使用这些既有结果。三种方法的宽域场图另附[场数据准备程序](../Workspaces/dlw_paper_20261009/prepare_comparison_fields.py)与[绘图程序](../Workspaces/dlw_paper_20261009/plot_comparison_fields.py)。

## 参考文献 {#zh-references}

[1] M. Boiti, J.J.-P. Leon, F. Pempinelli. Spectral transform for a two spatial dimension extension of the dispersive long wave equation. *Inverse Problems* **3** (1987), 371–387. [DOI](https://doi.org/10.1088/0266-5611/3/3/007).

[2] M. Wang, Y. Zhou, Z. Li. A nonlinear transformation of the dispersive long wave equations in (2+1) dimensions and its applications. *Journal of Nonlinear Mathematical Physics* **5** (1998), 120–125. [DOI](https://doi.org/10.2991/jnmp.1998.5.2.2).

[3] K. Sun, B. Tian, W.-J. Liu, M. Li, Q.-X. Qu, Y. Jiang. Symbolic-computation study on the (2+1)-dimensional dispersive long wave system. *SIAM Journal on Applied Mathematics* **70** (2010), 2259–2272. [DOI](https://doi.org/10.1137/090774847).

[4] J. Hu, Z.-W. Xu, G.-F. Yu. Determinant structure for the (2+1)-dimensional dispersive long wave system. *Applied Mathematics Letters* **62** (2016), 76–83. [DOI](https://doi.org/10.1016/j.aml.2016.07.003).

[5] H.-H. Sheng, G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. *Physica D* **432** (2022), 133140. [DOI](https://doi.org/10.1016/j.physd.2021.133140).

[6] X.-B. Hu, G.-F. Yu. Integrable discretizations of the (2+1)-dimensional sinh-Gordon equation. *Journal of Physics A: Mathematical and Theoretical* **40** (2007), 12645–12659. [DOI](https://doi.org/10.1088/1751-8113/40/42/S10).

[7] Y. Zhang, X. Chang, J. Hu, X. Hu, H.-W. Tam. Integrable discretization of soliton equations via bilinear method and Bäcklund transformation. *Science China Mathematics* **58** (2015), 279–296. [DOI](https://doi.org/10.1007/s11425-014-4952-6). [Preprint](https://arxiv.org/abs/1411.0476).

[8] G.-F. Yu, Z.-W. Xu. Dynamics of a differential-difference integrable (2+1)-dimensional system. *Physical Review E* **91** (2015), 062902. [DOI](https://doi.org/10.1103/PhysRevE.91.062902).

[9] B.-F. Feng, H.-H. Sheng, G.-F. Yu. Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation. *Numerical Algorithms* **94** (2023), 351–370. [DOI](https://doi.org/10.1007/s11075-023-01504-1).