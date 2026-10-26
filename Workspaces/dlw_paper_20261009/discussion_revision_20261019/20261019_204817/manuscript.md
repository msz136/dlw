<nav>[English](#en-title) · [中文](#zh-title)</nav>

# Integrable semi-discretizations of the (2+1)-dimensional dispersive long wave system {#en-title}

**Abstract.** We construct an integrable semi-discrete system for the (2+1)-dimensional dispersive long wave (DLW) equation by discretizing the y direction. Starting from the continuous bilinear equations, we introduce a staggered lattice in the y direction and obtain Gram determinant solutions of arbitrary order that satisfy the semi-discrete bilinear system. Eliminating or retaining an auxiliary potential yields two nonlinear formulations, the potential-elimination formulation (PE) and the potential formulation (PF), for which we establish corresponding Darboux–Lax representations. We prove that, as the lattice spacing tends to zero, the semi-discrete equations recover the continuous DLW equation with second-order accuracy, and the physical fields reconstructed from their exact solutions converge to the continuous exact solutions with second-order accuracy, and we give the leading difference between the two exact solution families in closed form. Furthermore, we construct a mesh density from a conservation law of the equation and propose a self-adaptive moving mesh method in which the physical fields and node positions evolve together. Using exact one- and two-soliton solutions as benchmarks, we compare the numerical errors of PE, PF and direct finite differences, and examine the effects of different time integrators and self-adaptive moving meshes. The numerical results show that the proposed moving mesh method reduces the maximum absolute errors in both physical fields in all four tests considered.

**Keywords:** dispersive long wave equation; semi-discretization; Gram determinant; Darboux–Lax representation; continuum limit; self-adaptive moving mesh

## 1. Introduction {#en-intro}

The propagation and interaction of waves in shallow water have long attracted interest in the study of nonlinear wave phenomena. As waves evolve, nonlinear effects and dispersion can influence their profiles in different ways, and their balance can support coherent waves that persist during propagation. Nonlinear long-wave equations describe these effects in a reduced form, allowing wave motion to be studied without retaining the full complexity of the underlying fluid equations. Within this class, integrable models have received sustained attention for the analytical insight they offer. Their exact solutions make it possible to follow the evolution of individual waves and examine their interactions, while bilinear formulations and Lax representations reveal mathematical structures underlying these solutions. These analytical results also provide useful reference points for numerical studies, in which wave profiles and their evolution are represented on a discrete mesh. Passing from a continuous model to such a representation introduces choices that affect both the approximation of the waves and the mathematical structure of the resulting equations. Integrable discretization seeks to retain this connection, bringing the construction of discrete equations together with the study of their exact solutions and continuum limits.

The (2+1)-dimensional dispersive long wave (DLW) system extends the dispersive long wave equation to two spatial dimensions [1] and has been studied in connection with wave motion in wide channels and open seas of finite depth [3,4]. Since its introduction by Boiti, Leon and Pempinelli, its wave solutions have been studied through several closely related analytical approaches. The inverse spectral transform, Bäcklund transformation and superposition formula established in the original work [1] were followed by nonlinear transformations [2] and bilinear methods [3], which offered further ways to generate solutions and understand their relations. Determinant representations give these relations a concrete form. Hu, Xu and Yu developed Grammian and Wronskian solutions [4], and Sheng and Yu used a KP-hierarchy reduction to obtain Gram determinant solutions describing solitons, line breathers and rational waves on constant and periodic backgrounds [5].

The bilinear relations underlying these solutions also offer a starting point for introducing a lattice [15]. In this approach, Bäcklund transformations relate neighbouring lattice values, allowing discrete equations to be constructed together with their solution structures. This idea has been developed for semi-discrete soliton equations [7] and extended to systems with two spatial dimensions [8]. For the DLW system, a further connection comes from its bilinear relation to the (2+1)-dimensional sinh-Gordon equation [5], whose integrable discretizations admit determinant solutions and Bäcklund–Lax structures [6]. Together with earlier studies of discrete DLW systems [11], these developments motivate a closer examination of how the continuous DLW solution family can be carried onto a spatial lattice, and how the resulting wave fields compare with their continuous counterparts.

With these advancements, there is potential to study the preservation of integrable structure and the approximation of continuous waves within the same construction. With this in mind, we ask how to introduce a spatial lattice that preserves the bilinear and determinant structure, supports a consistent reconstruction of the physical fields, and admits a quantitative comparison between its exact solutions and those of the continuous system.

To address this question, we seek a semi-discrete description of the DLW system in the $y$ direction, with $x$ and $t$ remaining continuous. First, we wish to retain the connection between explicit wave solutions and the integrable structure that supports their evolution. More specifically, we seek Gram determinant solutions that make the discrete wave fields accessible to analytical study. A corresponding Lax representation should describe the same nonlinear evolution through its compatibility conditions. Second, we wish to understand what changes when the continuous waves are represented on a lattice. This calls for a quantitative comparison of the reconstructed fields, beyond the recovery of the continuous equations in the limit. Such a comparison would reveal how the discrete waves approach their continuous counterparts. Numerical computation introduces further approximations through spatial differences and time stepping, so the accuracy of the computed fields also depends on how the semi-discrete equations are implemented. We therefore wish to use the exact solutions as references for examining how the nonlinear formulation, time integrator and mesh influence the resulting errors.

In Section 2, starting from the continuous bilinear formulation and Gram determinant solutions presented by Sheng and Yu [5], we introduce a semi-discrete bilinear system by combining a staggered lattice in $y$ with shifts of the bilinear operator parameter. We first prove that the proposed Gram determinants satisfy this system, using an identity between adjacent layers. We then derive two nonlinear formulations. The first, the potential-elimination formulation (PE), eliminates an auxiliary potential; the second, the potential formulation (PF), retains it. For both formulations, we establish the reconstruction of the physical fields and derive Darboux–Lax representations whose compatibility conditions yield the corresponding nonlinear equations. The continuum-limit analysis then connects this construction to the original DLW system. We prove second-order consistency of the equations and, for fixed regular spectral parameters and positive $\tau$ functions on the compact sets considered, second-order convergence of the reconstructed exact solutions. An explicit expression for their leading difference identifies how the lattice modifies the continuous wave fields.

In Section 3, we examine the numerical methods through four soliton tests: two single-soliton cases with opposite signs of the $u$ pulse, and two two-soliton cases covering interactions between waves of the same and opposite polarities in $u$. These cases provide exact references for examining the numerical methods across different wave profiles and interaction patterns. We formulate spatial discretizations for PE and PF, together with a direct finite-difference approximation of the continuous equations. To understand the contribution from the $x$ discretization, we derive the leading $O(\Delta x^2)$ truncation terms in the reconstructed $u$ evolution for PE and direct finite differences on a fixed grid. We also introduce a self-adaptive moving mesh method based on a conservation law of the semi-discrete system. The method evolves the physical fields and node positions together, using the transversely averaged conservation density to redistribute the shared $x$ nodes while retaining a uniform lattice in $y$. We then describe the time integration methods and specify the test problems and error measures. Finally, we discuss how the nonlinear formulation, time integration and mesh adaptation affect the errors in both physical fields, drawing on the analytical expansions to interpret the numerical results.

## 2. Semi-discrete DLW system and exact solutions {#en-continuous}

In this section, we develop a semi-discrete DLW system by bringing its bilinear equations, exact solutions and physical-field reconstruction into a consistent construction. In Section 2.1, we recall the continuous bilinear formulation and Gram determinant solutions of Sheng and Yu [5], together with the transformation relating the τ functions to the physical fields. Building on these relations, in Section 2.2, we introduce a staggered lattice in $y$ and couple lattice shifts to shifts of the bilinear parameter, while keeping $x$ and $t$ continuous. In Section 2.3, we construct the corresponding Gram determinant solutions and establish that they satisfy the semi-discrete bilinear equations. In Section 2.4, we turn to the physical fields and derive two nonlinear formulations by eliminating or retaining an auxiliary potential, making the reconstruction explicit in each case. In Section 2.5, we examine the continuum limit of both the equations and their exact solutions to determine how the lattice system recovers the continuous DLW dynamics and how its wave fields approach their continuous counterparts. Finally, in Section 2.6, we derive Darboux–Lax representations and verify that their compatibility conditions yield the corresponding nonlinear equations.

### 2.1 Continuous DLW system and bilinear formulation {#en-preliminaries}

Our aim here is to identify the relations we will carry from the continuous DLW system into its semi-discrete counterpart. Specifically, we seek a description in which we can construct exact solutions and recover the physical wave fields from them, so that both remain connected when we introduce a lattice. For this purpose, we revisit the bilinear formulation and Gram determinant solutions of Sheng and Yu [5], paying particular attention to the transformation between the τ functions and the physical fields. Following their normalization, we set $\lambda=-2$ and write the continuous system as

<a id="en-eq-1"></a>

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

where $a\in\mathbb R$ is a constant. We work with two sufficiently smooth, positive τ functions $f$ and $g$ and recover the physical fields through

<a id="en-eq-2"></a>

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

This transformation allows us to construct the wave fields through relations between $f$ and $g$. In particular, we use the bilinear equations [5]

<a id="en-eq-3"></a>

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

where $B_s=D_x^2+D_t+2sD_x$. We retain the parameter $s$ in this notation because shifts of this parameter will enter the lattice construction in Section 2.2. To fix our notation, we define the Hirota bilinear operators by

<a id="en-eq-4"></a>

$$D_x^rD_y^sD_t^m f\cdot g=\left.(\partial_x-\partial_{x\prime})^r(\partial_y-\partial_{y\prime})^s(\partial_t-\partial_{t\prime})^m f(x,y,t)g(x\prime,y\prime,t\prime)\right|_{(x\prime,y\prime,t\prime)=(x,y,t)}.\tag{4}$$

where $r,s,m$ are nonnegative integers. We first state how solutions of the bilinear equations yield solutions of the physical-field equations.

**Proposition 2.1 (Bilinear representation [5]).** If sufficiently smooth positive functions $f,g$ satisfy [(3)](#en-eq-3), the fields defined by [(2)](#en-eq-2) solve the DLW system [(1)](#en-eq-1).

**Proof.** We divide the bilinear equations by $fg$, expand the Hirota operators in logarithmic derivatives, and substitute [(2)](#en-eq-2). This gives the two equations in [(1)](#en-eq-1); see [5, Section 2]. □

Having established this connection, we recall the continuous Gram determinant solutions of [5]. We use this family both as a guide to the semi-discrete determinant construction and as a reference for comparing the reconstructed wave fields in the continuum limit. The τ functions take the form

<a id="en-eq-5"></a>

$$\tau_n^{(0)}=\det_{1\le i,k\le N}\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\left(-\frac{p_i-a}{q_k+a}\right)^n e^{\xi_i+\eta_k}\right],\quad f=\tau_1^{(0)},\quad g=\tau_0^{(0)},\tag{5}$$

with phases

<a id="en-eq-6"></a>

$$\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad \eta_k=q_kx+q_k^2t+\frac{y}{q_k+a}.\tag{6}$$

Here $N$ is the determinant order, $n$ is an auxiliary integer index, and $\delta_{ik}$ is the Kronecker delta. We choose the real parameters so that all displayed denominators are nonzero and restrict the physical fields to regions where $f$ and $g$ are positive. The following proposition confirms that this determinant family satisfies the bilinear equations used in our reconstruction.

**Proposition 2.2 (Continuous Gram determinant solutions [5]).** Let $\tau_n^{(0)}$ be defined by (5)–(6), with parameters chosen so that all displayed denominators are nonzero. Then $f=\tau_1^{(0)}$ and $g=\tau_0^{(0)}$ satisfy the bilinear equations [(3)](#en-eq-3). Consequently, on any region where $f$ and $g$ are positive, the fields reconstructed through [(2)](#en-eq-2) solve the continuous DLW system [(1)](#en-eq-1).

**Proof.** The bilinear identities for this Gram determinant family follow from the KP-hierarchy reduction established in [5]. With $f=\tau_1^{(0)}$ and $g=\tau_0^{(0)}$, these identities give [(3)](#en-eq-3). The statement for the reconstructed physical fields then follows from Proposition 2.1. □

We therefore have an explicit solution family in which the τ functions and the physical fields are linked by the bilinear equations and the reconstruction formulas. In the next subsection, we use the $y$-dependence of this family to guide the lattice construction, seeking to preserve these relations in the semi-discrete setting.

### 2.2 Semi-discrete bilinear equations {#en-bilinear}

Building on the continuous bilinear formulation, we now seek to introduce a spatial lattice while preserving its connection with the determinant solutions. Specifically, we aim to retain a structure that supports explicit wave solutions and a consistent reconstruction of the physical fields. The lattice equations should also recover the continuous bilinear system as the spacing tends to zero. With these requirements in mind, we begin by examining how the two equations in (3) are related, using this connection to guide our choice of discrete shifts.

In particular, we focus on how the $y$-dependence enters the bilinear system. The first equation involves only derivatives in $x$ and $t$, whereas the second connects variation in $y$ to the same operator $B_a$. This shared structure suggests a way to introduce a lattice in $y$ while keeping $x$ and $t$ continuous. To develop this idea, we first rewrite the equations so that the relation between differentiation in $y$ and variation of the operator parameter becomes explicit. Differentiating the first equation in (3) with respect to $y$ and combining it with the second, we obtain

<a id="en-eq-7"></a>

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{7}$$

Together with $B_af\cdot g=0$, this relation is equivalent to the continuous bilinear system (3). The two terms in (7) suggest shifting the second τ function and the operator parameter together. We therefore introduce

<a id="en-eq-8"></a>

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t).\tag{8}$$

Since $B_{a+s}=B_a+2sD_x$, we have

$$\Phi(0)=B_af\cdot g,\qquad \Phi'(0)=B_af\cdot g_y+2D_xf\cdot g.$$

We can thus express the continuous bilinear equations as the two conditions $\Phi(0)=0$ and $\Phi'(0)=0$. This observation motivates a symmetric lattice construction: we replace these conditions by two bilinear relations corresponding to the shifts $s=-h/2$ and $s=h/2$.

For $h>0$ and $j\in\mathbb Z$, we place $F_j(x,t)$ at $y=(j+\tfrac12)h$ and $G_j(x,t)$ at $y=jh$, keeping $x$ and $t$ continuous. Relative to $F_j$, the adjacent functions $G_j$ and $G_{j+1}$ then occupy the two symmetric positions. We pair these offsets with the parameter values $a-h/2$ and $a+h/2$, and propose the semi-discrete bilinear system

<a id="en-eq-9"></a>

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{9}$$

Here $F_j$ and $G_j$ are unknown lattice τ functions. Their positions specify how we compare them with the continuous functions $f$ and $g$; they do not require the lattice functions to equal samples of a continuous solution. We construct exact Gram determinant solutions of (9) in Section 2.3 and establish their convergence under this staggered identification in Section 2.5.

To check the local consistency of the proposed relations, we return to (8) and expand about $s=0$. For sufficiently smooth $f$ and $g$, symmetric Taylor expansion gives

<a id="en-eq-10"></a>

$$\frac{\Phi(h/2)+\Phi(-h/2)}2=B_af\cdot g+O(h^2),\qquad \frac{\Phi(h/2)-\Phi(-h/2)}h=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{10}$$

The symmetric average and difference quotient therefore recover the first equation in (3) and the equivalent relation (7) with second-order consistency. This establishes the connection with the continuous bilinear system. We next examine whether the proposed lattice relations also admit a corresponding determinant solution family.

### 2.3 Gram determinant solutions {#en-gram}

We now turn to the exact solutions of the semi-discrete bilinear system (9). To construct them, we adapt the continuous Gram determinants in (5), preserving their dependence on $x$ and $t$ while replacing the $y$-dependent exponential factors by lattice factors. The choice of these factors connects the determinant formula to the equations derived above: they must accommodate the coupled lattice and parameter shifts in (9), while approaching the continuous exponential factors as $h\to0$. We therefore look for a form that allows us to establish both the bilinear identities and the correspondence with the continuous solution family.

We choose the lattice factor

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad d=\frac h2.$$

For fixed nonzero $z$ and sufficiently small $h$, its expansion gives

$$\log\lambda_h(z)=\frac hz+O(h^3).$$

Consequently, $\lambda_h(z)^j$ approaches $e^{y/z}$ as $h\to0$ with $jh=y$ fixed. We can therefore replace the continuous $y$-dependent exponentials by powers of this factor. Its numerator and denominator also contain the same half-step offsets that appear in the operator parameters of (9), allowing us to relate the lattice shift to the parameter shift in the determinant identities below.

With this choice, we define

<a id="en-eq-11"></a>

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{11}$$

Here $\delta_{ik}$ is the Kronecker delta. We retain the auxiliary index $n$ to establish bilinear identities between adjacent members of the sequence, and the parameter $s$ to accommodate the two operators in (9). For $n=0$, the determinant is independent of $s$, so we write $\tau_0(j;s)=\tau_0(j)$. The following theorem identifies the members that give the required lattice τ functions.

**Theorem 2.3 (Gram determinant solutions).** Let $h>0$, $N\ge1$, and let $p_i,q_i,\rho_i$ be real parameters satisfying $p_i+q_k\ne0$, $p_i-a\pm d\ne0$ and $q_k+a\pm d\ne0$ for all $i,k$. Then the functions

<a id="en-eq-12"></a>

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{12}$$

satisfy the semi-discrete bilinear system [(9)](#en-eq-9) at every lattice site $j\in\mathbb Z$.

To prove this result, we first establish a bilinear identity between adjacent $n$-layers at a fixed lattice site. This identity gives the first equation in (9) directly. For the second, we show that shifting the lattice index from $j$ to $j+1$, together with the parameter from $a-d$ to $a+d$, leaves the determinant defining $F_j$ unchanged. We can then apply the same identity at the neighbouring site.

**Lemma 2.4 (Adjacent-layer identity).** Under the spectral conditions of Theorem 2.3, fix a lattice site $j$ and a parameter $s$ such that $p_i-s\ne0$ and $q_k+s\ne0$ for all $i,k$. Then, for every $n\in\mathbb Z$,

<a id="en-eq-13"></a>

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{13}$$

**Proof.** We use the matrix determinant lemma and the rank-one identities obtained by differentiating the determinant entries to establish (13). The detailed calculation is given in [Appendix B](#en-app-b), where we also extend the identity to points at which the matrices defining the τ functions are singular. □

**Proof of Theorem 2.3.** We first apply (13) at the lattice site $j$, with $n=0$ and $s=a-d$. Since $\tau_0(j;s)$ is independent of $s$, the definitions in (12) give

$$B_{a-d}F_j\cdot G_j=B_{a-d}\tau_1(j;a-d)\cdot\tau_0(j)=0.$$

This is the first equation in (9).

To obtain the second equation, we need to pair $F_j$ with $G_{j+1}$ under the operator $B_{a+d}$. The required connection follows from the choice of lattice factors:

<a id="en-eq-23"></a>

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{14}$$

Using this identity in each entry of the determinant, we find

<a id="en-eq-24"></a>

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{15}$$

Thus, the same function $F_j$ can be represented at the neighbouring site $j+1$, provided that the parameter is shifted from $a-d$ to $a+d$. Applying (13) at that site with $n=0$ and $s=a+d$, we obtain

<a id="en-eq-25"></a>

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{16}$$

This proves the second equation in (9) and completes the proof. □

The identity (15) explains how the determinant construction accommodates the two shifted operators in the bilinear system. We can now use these τ functions to reconstruct the physical fields. Before doing so, we give a sufficient condition for their positivity, ensuring that the logarithms in the reconstruction remain well defined.

The determinant identities above establish the bilinear equations without requiring the τ functions to be positive. To reconstruct real physical fields through logarithmic derivatives, however, we work on regions where both $F_j$ and $G_j$ are positive. We now give a sufficient parameter condition that ensures this property for all $x,t$ and every lattice site.

**Proposition 2.5 (Positive τ functions).** Suppose $0<p_1<\cdots<p_N<a-h/2$, $0<q_1<\cdots<q_N$ and $\rho_i>0$. Then the τ functions defined by (12) satisfy $F_j\ge1$ and $G_j\ge1$ for all $x,t\in\mathbb R$ and $j\in\mathbb Z$.

**Proof.** Under these conditions, the lattice factors $\lambda_h(p_i-a)$ and $\lambda_h(q_k+a)$ are positive. The additional factor in $F_j$ is also positive, since

$$-\frac{p_i-a+d}{q_k+a-d}>0.$$

We can therefore write each matrix defining $F_j$ or $G_j$ as $I+D_1CD_2$, where $C_{ik}=1/(p_i+q_k)$ and $D_1,D_2$ are positive diagonal matrices. For any nonempty index set $I\subseteq\{1,\ldots,N\}$, the Cauchy determinant formula gives

<a id="en-eq-26"></a>

$$\det C_{I,I}=\frac{\prod_{i<k,\ i,k\in I}(p_k-p_i)(q_k-q_i)}{\prod_{i,k\in I}(p_i+q_k)}>0.\tag{17}$$

Multiplication by the positive diagonal matrices preserves the positivity of these principal minors. We then expand $\det(I+D_1CD_2)$ as the sum of all principal minors of $D_1CD_2$, together with the empty minor $1$. Every nonempty contribution is positive, which proves the stated bounds. □

This condition gives a parameter range in which the τ functions remain positive throughout the lattice evolution. It is sufficient rather than necessary; outside this range, we may still reconstruct the physical fields wherever both τ functions are positive. With the determinant solutions and their regularity conditions established, we turn to the nonlinear equations governing the reconstructed fields.

### 2.4 Nonlinear formulations {#en-nonlinear}

We now turn from the bilinear equations to the evolution of the physical fields. Our aim is to express the semi-discrete system in variables that can be compared with the continuous fields $u$ and $v$, while retaining the exact solutions constructed above. This requires a reconstruction that accounts for the staggered positions of $F_j$ and $G_j$. We first define the fields on this lattice and derive their evolution from the two bilinear equations. The resulting relations then lead to two nonlinear formulations, according to whether we eliminate an auxiliary potential or retain it.

At the location of $F_j$, the neighbouring functions $G_j$ and $G_{j+1}$ lie symmetrically on either side. We therefore use their average logarithm to define $u_j$, and introduce $\omega_j$ to describe the change in the logarithmic $x$-derivative between these neighbouring sites. For positive τ functions, we set

<a id="en-eq-27"></a>

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad \omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad v_j=\frac4h\omega_j+\delta_0u_j,\qquad \delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h}.\tag{18}$$

We associate the reconstructed fields $u_j$ and $v_j$ with $y=(j+\tfrac12)h$. The definition of $v_j$ follows the continuous identity

$$v=4(\log g)_{xy}+u_y,$$

which is obtained directly from (2). In (18), $4\omega_j/h$ approximates $4(\log g)_{xy}$, while $\delta_0u_j$ approximates $u_y$. These relations give a discrete counterpart of the continuous field transformation; we establish their second-order consistency in Section 2.5. For the derivation below, we work with $u_j$ and $\omega_j$, recovering $v_j$ through (18).

Let $\alpha_j=\log F_j$ and $\beta_j=\log G_j$. Dividing the two bilinear equations by $F_jG_j$ and $F_jG_{j+1}$, respectively, gives

<a id="en-eq-28"></a>

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{19}$$

The physical-field definitions imply

<a id="en-eq-29"></a>

$$(\alpha_j-\beta_j)_x=\frac{u_j+\omega_j}{2},\qquad (\alpha_j-\beta_{j+1})_x=\frac{u_j-\omega_j}{2}.\tag{20}$$

In $A_j+C_j$, the second-derivative terms combine into $(2\alpha_j+\beta_j+\beta_{j+1})_{xx}$. We therefore introduce

<a id="en-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{21}$$

Taking the x-derivatives of $A_j+C_j=0$ and $A_j-C_j=0$ yields

<a id="en-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{22}$$

Next, we derive two nonlinear formulations from these evolution equations. The first eliminates $Z_j$ through a lattice difference, while the second expresses $Z_j$ in terms of a potential variable. For the first formulation, we introduce the backward difference and averaging operators

<a id="en-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{23}$$

The definitions of $u_j,\omega_j,Z_j$ give

<a id="en-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{24}$$

Applying $\delta_-$ to the first evolution equation and substituting this identity, we obtain the potential-elimination formulation (PE)

<a id="en-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{25}$$

For the second formulation, introduce the potential variable $M_j=\beta_{j,x}$. The definitions give

<a id="en-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{26}$$

With this substitution, the first evolution equation contains $u_{j,x}+u_j^2/2$. We therefore introduce

<a id="en-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{27}$$

so that

<a id="en-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{28}$$

The undifferentiated relation $(A_j+C_j)/2=0$ then gives

<a id="en-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{29}$$

In the second evolution equation, the flux can be written as

<a id="en-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{30}$$

To remove the quotient, define

<a id="en-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{31}$$

Using the identities

<a id="en-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{32}$$

the ω equation becomes

<a id="en-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{33}$$

Since

<a id="en-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{34}$$

substitution of the Q equation yields the equation for R. Together with the lattice constraint, this gives the potential formulation (PF)

<a id="en-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{35}$$

Here $Q_j,R_j$ are associated with $y=(j+\tfrac12)h$, and $M_j$ with $y=jh$. The physical fields are recovered by

<a id="en-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{36}$$

The following proposition shows that the two nonlinear formulations recover identical physical fields from the same pair of positive τ functions.

**Proposition 2.6 (Common physical fields).** Let positive F,G satisfy [(9)](#en-eq-9). The two nonlinear formulations constructed above yield identical physical fields u,v at every finite positive lattice spacing h.

**Proof.** The definitions give

<a id="en-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{37}$$

Adding the same central difference of u to the second equality proves that the reconstructed v fields also coincide. □

### 2.5 Continuum limits {#en-limits}

Having obtained the two nonlinear formulations, we now examine their continuum limits as $h\to0$. We first establish the second-order consistency of the physical-field reconstruction and the semi-discrete equations with their continuous counterparts. We then show that, for fixed regular spectral parameters, the Gram determinant solutions converge to the continuous DLW solutions with an error of order $h^2$, uniformly on compact sets.

Throughout this subsection, $O_K(h^m)$ denotes a remainder uniformly bounded by $C_Kh^m$ on a compact set K. Functions are assumed smooth on an open neighbourhood of K. The following proposition relates the staggered reconstruction to the continuous dependent-variable transformation.

**Proposition 2.7 (Consistency of reconstruction).** Let f,g be positive smooth functions, and let u,v be given by [(2)](#en-eq-2). At a physical location y, define

<a id="en-eq-47"></a>

$$\begin{aligned}u^{[h]}(y)&=\partial_x[2\log f(y)-\log g(y-h/2)-\log g(y+h/2)],\\\omega^{[h]}(y)&=\partial_x[\log g(y+h/2)-\log g(y-h/2)],\\v^{[h]}(y)&=\frac4h\omega^{[h]}(y)+\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}.\end{aligned}\tag{38}$$

The arguments x,t are suppressed. Then

<a id="en-eq-48"></a>

$$u^{[h]}=u+O_K(h^2),\qquad v^{[h]}=v+O_K(h^2).\tag{39}$$

**Proof.** Write $\alpha=\log f$, $\beta=\log g$. Symmetric Taylor expansion gives

<a id="en-eq-49"></a>

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad \frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).\tag{40}$$

The first expansion also holds after differentiation, so

<a id="en-eq-50"></a>

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2),\qquad v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2).\tag{41}$$

This proves the assertion. □

We next examine the nonlinear equations. Set

<a id="en-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{42}$$

The first formulation becomes

<a id="en-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{43}$$

With $\mathcal M_+z_j=(z_{j+1}+z_j)/2$, the identity $\mathcal M_+\delta_-=\delta_0$ shows that $\mathcal M_+E_{1,h,j}+E_{2,h,j}=0$ is the evolution equation for v.

**Proposition 2.8 (Consistency of the equations).** Sample smooth u,v at $y_j=(j+\tfrac12)h$, and denote the continuous DLW residuals by

<a id="en-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{44}$$

Then, uniformly on compact sets,

<a id="en-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{45}$$

**Proof.** Write $m_j=y_j-h/2$. Taylor expansion gives

<a id="en-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{46}$$

Consequently,

<a id="en-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{47}$$

The expansions hold after the required derivatives and give $E_{1,h,j}=\mathcal C_1(m_j)+O_K(h^2)$. Setting $w=v-u_y$, the second residual becomes

<a id="en-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{48}$$

Averaging the first residual about y_j and adding the second yields

<a id="en-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{49}$$

All continuous fields in this display are evaluated at y_j. This proves the second assertion. □

Finally, we establish the continuum limit of the exact Gram solutions. Here the τ functions depend on h through both the lattice factors and the shifted auxiliary parameter.

**Theorem 2.9 (Continuum limit of the Gram solutions).** Fix N and spectral parameters such that, for some $h_0>0$,

<a id="en-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{50}$$

For $0<h\le h_0$, extend the positive lattice factors to real exponents and define

<a id="en-eq-60"></a>

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{51}$$

Thus $g^{(h)}(x,jh,t)=G_j$ and $f^{(h)}(x,(j+\tfrac12)h,t)=F_j$. Let $u^{(h)},v^{(h)}$ be their staggered reconstruction, and let $f^{(0)},g^{(0)}$ be the continuous Gram functions in [(5)](#en-eq-5). The corresponding fields $u^{(0)},v^{(0)}$ solve the continuous DLW system, and for every compact K,

<a id="en-eq-61"></a>

$$\sup_K\bigl(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\bigr)\le C_Kh^2\tag{52}$$

for sufficiently small positive h. This estimate holds for both nonlinear formulations.

**Proof.** Write $z_i=p_i-a$ and $w_k=q_k+a$. For fixed spectral parameters,

<a id="en-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{53}$$

so the coefficient of y in the exponential satisfies

<a id="en-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{54}$$

For $f^{(h)}$, the auxiliary-parameter shift and the half-grid shift combine into the amplitude factor

<a id="en-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}+O(h^2).\end{aligned}\tag{55}$$

The phase and amplitude therefore differ from their continuous counterparts by $O(h^2)$. Since N is fixed, for every fixed mixed derivative $\partial^\nu$,

<a id="en-eq-65"></a>

$$\partial^\nu(f^{(h)}-f^{(0)})=O_K(h^2),\qquad \partial^\nu(g^{(h)}-g^{(0)})=O_K(h^2).\tag{56}$$

The positivity argument in Proposition 2.5 also applies to the real-exponent extension and its limit. All four τ functions are bounded below by 1, so their logarithmic derivatives satisfy the same second-order estimates.

The adjacent-layer identity and the lattice-shift relation remain valid for the extension, giving

<a id="en-eq-66"></a>

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.\tag{57}$$

Taking their symmetric average and difference quotient, with the uniform derivative bounds above, yields

<a id="en-eq-67"></a>

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.\tag{58}$$

These are the continuous bilinear equations in the equivalent form of Section 2.1, so Proposition 2.1 gives a continuous DLW solution. Finally, applying Proposition 2.7 uniformly to the h-dependent family gives

<a id="en-eq-68"></a>

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).\tag{59}$$

Combining these relations with [(56)](#en-eq-65) proves the estimate. Proposition 2.6 transfers the result to both nonlinear formulations. □

**Proposition 2.10 (Leading difference of the exact families).** Fix N and the same regular spectral parameters in the continuous and semi-discrete Gram determinants. On a compact set where the τ functions stay away from zero, choose smooth logarithms and write $\alpha=\log f$, $\beta=\log g$, $\log f_h=\alpha+h^2\alpha_2+O_K(h^4)$ and $\log g_h=\beta+h^2\beta_2+O_K(h^4)$, using the extensions (51). At the common physical position $y=(j+\tfrac12)h$, the reconstructed exact fields satisfy

<a id="en-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{60}$$

The expansions hold with the derivatives used in reconstruction. Their coefficients and proof are given in [Appendix A](#en-app-a). This is an asymptotic comparison of exact solution families; the two families already differ at the initial time.

### 2.6 Darboux–Lax representation {#en-lax}

We next construct a Darboux–Lax representation of the semi-discrete DLW system. We first express the linear problem in terms of the physical fields and then give its potential form in the variables Q,R,M.

Introduce the shifted variables

<a id="en-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{61}$$

The first nonlinear formulation becomes

<a id="en-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{62}$$

To formulate the linear problem, introduce an auxiliary potential V satisfying

<a id="en-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{63}$$

The compatibility of these relations is precisely the first nonlinear equation. On a local x-interval and a lattice chain, V can therefore be constructed by integration at one reference site followed by lattice propagation, up to a common function of t.

Consider the auxiliary linear equations

<a id="en-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{64}$$

The first equation relates wave functions at adjacent lattice sites, while the second determines their time evolution. The following theorem establishes their compatibility with the nonlinear system.

**Theorem 2.11 (Darboux–Lax compatibility).** Every smooth solution of [(62)](#en-eq-70), together with the auxiliary potential [(63)](#en-eq-71), makes [(64)](#en-eq-72) compatible in the formal operator sense. Conversely, on a region where $w_j\ne0$, compatibility together with the potential-difference relation implies [(62)](#en-eq-70).

**Proof.** Factor the lattice transfer as $T_j=\mathscr B_j^{-1}\mathscr A_j$, with $\mathscr A_j=\partial_x-U_j/2-hw_j/8$ and $\mathscr B_j=\partial_x-U_j/2+hw_j/8$. The field equations make both scalar Darboux residuals vanish and give a common intermediate potential, hence $T_{j,t}=H_{j+1}T_j-T_jH_j$. Conversely, the coefficients of orders zero and minus one imply vanishing of both residuals when $w_j\ne0$. Their sum and difference recover the field equations. The operator identities are recorded in [Appendix C](#en-app-c). □

For τ-function solutions, take

<a id="en-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{65}$$

Differentiating the normalized bilinear equations in x gives $\mathcal E_j^r=\mathcal E_j^s=0$. Thus the Gram determinant solutions satisfy the Darboux–Lax compatibility relations.

Finally, substitute the potential variables

<a id="en-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{66}$$

The linear system becomes

<a id="en-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{67}$$

Differentiating the lattice constraint gives

<a id="en-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{68}$$

The Q and R equations make both scalar residuals vanish, establishing compatibility. Conversely, when $Q_jR_j\ne0$, compatibility together with this potential-difference relation recovers the physical-field equations of the first formulation.

The above construction provides a common Darboux–Lax representation for the two nonlinear formulations. The lattice shift is realized through two first-order Darboux operators sharing an intermediate potential, and its compatibility with the time evolution follows from the semi-discrete field equations.

## 3. Numerical methods and experiments {#en-numerics}

In this section, we develop numerical algorithms based on PE and PF and compare them with direct finite differences applied to the continuous DLW system. We first discretize the remaining x derivatives and combine the resulting spatial discretizations with time integration methods. We then use the conservation law derived above to construct a mesh density and a self-adaptive moving mesh (SAMM) method in which the physical fields and node positions evolve together, allowing the x-node distribution to adjust as the solution evolves. Using exact one- and two-soliton solutions as references, we examine the effects of spatial discretization, time integration, and the choice between fixed and self-adaptive moving meshes on the physical-field errors.

### 3.1 Spatial discretization {#en-schemes}

We discretize the remaining x derivatives to obtain evolution systems for numerical computation. PE and PF retain their respective nonlinear variables, while direct finite differences applied to the continuous DLW equations provide a reference method. All three implementations use the same physical grid and boundary data.

**Grid and difference operators.** On the fixed grid, let $x_i=-L/2+i\Delta x$, where $\Delta x=L/N_x$. In the y direction, $M_j$ is located at $y=jh$, while $u_j,v_j,Q_j,R_j$ are located at $y=(j+\tfrac12)h$. The indices j and i label the y layers and x nodes, respectively. Time remains continuous in the spatially discretized systems below.

We approximate the x derivatives by three-point centred differences

<a id="en-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{69}$$

Writing $k=\Delta x$, smooth functions satisfy

<a id="en-eq-202"></a>

$$D_1f=f_x+\frac{k^2}{6}f_{xxx}+O(k^4),\qquad D_2f=f_{xx}+\frac{k^2}{12}f_{xxxx}+O(k^4).\tag{70}$$

$D_2$ is the independent three-point second derivative, not $D_1^2$.

In the y direction, we use

<a id="en-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{71}$$

The operators $D_1,D_2$ act on the x-node index, whereas $\delta_-,\delta_0,\mathcal M_-$ act on the layer index. All products and quotients below are evaluated pointwise. We first construct the PE and PF schemes, followed by the direct finite-difference scheme, denoted by FD.

**PE scheme.** We evolve $P=\delta_-u$ and $W=v-\delta_0u$. The lower boundary value fixes u by cumulative summation of P, and $v=W+\delta_0u$; see [Appendix D](#en-app-d). The evolution equations are $\dot P=F_P$, $\dot W=F_W$, with

<a id="en-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{72}$$

Thus the right-hand side is evaluated by first recovering u from P, and then applying the spatial difference operators to u and W. The field v follows from the same reconstruction formula.

**PF scheme.** We evolve Q and R and reconstruct the physical fields through

<a id="en-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{73}$$

Here $m_j\simeq M_{j,x}$ is obtained from the lattice constraint and lower boundary data as detailed in Appendix D. The final rates are

<a id="en-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{74}$$

The lowest Q layer is prescribed, while the interior Q layers and all R layers are evolved. The physical fields are recovered from Q and R using (73).

**FD scheme.** For comparison, we discretize the continuous DLW equations directly, taking $P=\delta_-u$ and v as the evolution variables. The field u is recovered from P by the first relation in (113). The resulting system is $\dot P=F_P$ and $\dot v=F_v$, with

<a id="en-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{75}$$

**Leading x contribution to the reconstructed u rate.** Let b be the lowest physical y layer, $\Delta_bF=F(y)-F(b)$, and $T_h$ the composite trapezoidal sum from b to y. On a fixed grid define $H=u^2/2+2au$, $W=v-\delta_0u$ and $K(W)=W^2/32-W/4$. Summing the P equation with the prescribed $u_t(b)$ gives

<a id="en-eq-203"></a>

$$\begin{aligned}F^u_{\rm PE}&=u_t(b)-D_1\Delta_b[H+h^2K(W)]-D_2[\Delta_bu+T_hW],\\F^u_{\rm FD}&=u_t(b)-D_1\Delta_bH-D_2T_hv.\end{aligned}\tag{76}$$

Relative to the same y-discrete rates with exact x derivatives, $r^u_{x,m}=k^2B_{h,m}+O(k^4)$ at fixed h, where

<a id="en-eq-204"></a>

$$\begin{aligned}B_{h,\rm PE}&=-\frac16\partial_{xxx}\Delta_b[H+h^2K(W)]-\frac1{12}\partial_{xxxx}[\Delta_bu+T_hW],\\B_{h,\rm FD}&=-\frac16\partial_{xxx}\Delta_bH-\frac1{12}\partial_{xxxx}T_hv.\end{aligned}\tag{77}$$

For smooth fields, as h also tends to zero, both coefficients approach

<a id="en-eq-205"></a>

$$B=-\frac16\partial_{xxx}\Delta_bH(u)-\frac1{12}\partial_{xxxx}\int_b^y v(x,s,t)\,ds,\qquad r_x^u=k^2B+O(k^4+k^2h^2).\tag{78}$$

These are interior right-hand-side truncation errors with a matched x extension and the prescribed lower boundary. Periodic wrap-around mismatches contribute separately. The calculation concerns u for PE and FD on a fixed grid; PF, v and moving nodes require their own expansions.

These three spatial discretizations are combined with the time integrators in Section 3.3. Their initial and boundary data are specified in Section 3.4.

### 3.2 Self-adaptive moving mesh method {#en-samm}

A uniform grid may allocate many points to weakly varying regions while resolving a narrow wave band inadequately. Moving mesh methods address this imbalance by redistributing nodes through a solution-dependent density [14]. For integrable equations, conservation laws offer a direct connection between the solution and the mesh: examples include self-adaptive methods for the Camassa–Holm equation [12], short pulse equations [13] and a generalized sine-Gordon equation [9]. In the present two-dimensional setting, we retain a uniform $y$ lattice and use the same moving $x$ nodes on every transverse layer. We therefore average the conservation density and flux across the layers to determine a shared node distribution. This adapts the $x$ resolution while preserving the tensor-product representation of the fields.

The conservation law of the semi-discrete DLW system provides a density with which to construct a self-adaptive moving mesh method (SAMM). In this method, the physical fields and the node positions evolve together, and the node distribution is determined by the solution. We retain the uniform semi-discrete y lattice and allow the x nodes to move, with the same x nodes shared by all y layers. We choose the following conservation density and flux:

<a id="en-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{79}$$

Substituting $W_j=4(1-\rho_j)$ into its evolution equation gives

<a id="en-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{80}$$

In PF, $\rho_j=Q_jR_j$. Since all y layers share the same x nodes, average over the layers:

<a id="en-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{81}$$

The initial nodes are chosen so that the integral of $\bar\rho(x,0)$ is equal between adjacent nodes. This assigns more nodes to regions of larger density. During evolution, each node retains its cumulative density integral, linking its motion to the evolving field. With the left endpoint $x_L$ fixed, the conservation law [(80)](#en-eq-97) gives

<a id="en-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{82}$$

The resulting node velocity is

<a id="en-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{83}$$

In the computation, replace $\partial_x\rho$ by $D_1\rho$ and require $\bar\rho>0$. The FD moving-mesh comparison uses the same density, averaging and velocity formulas [(79)](#en-eq-96), [(81)](#en-eq-98) and [(83)](#en-eq-100).

On moving nodes, use the mapped centred operators in [Appendix E](#en-app-e) and evolve $\dot z=F_z+\mathcal V D_1z$ together with (83). The mapping Jacobian must remain positive. The fixed grid has $\mathcal V=0$.

### 3.3 Time integration {#en-time}

We use classical fourth-order Runge–Kutta (RK4) for the spatial-method and mesh comparisons. To assess sensitivity to time integration, we also apply forward Euler and Crank–Nicolson (C–N) to PE on the fixed grid. Let $z$ collect the evolving variables and write the resulting system as $\dot z=\mathcal F(t,z)$. For SAMM, $z$ also includes the node coordinates, and $\mathcal F$ includes the mesh transport terms and node velocities.

We use the standard Euler and RK4 methods [10]. At every RK4 stage, the fields, auxiliary variables, mesh and boundary values are evaluated at that stage. The C–N iteration and complete time-integrator comparison are given in [Appendix F](#en-app-f).

### 3.4 Test problems and error measures {#en-tests}

We consider one- and two-soliton solutions of the continuous DLW system. The exact solutions provide the initial and boundary data and serve as the reference for evaluating the numerical errors. Throughout the tests, we set $a=2$, take the determinant coefficients $\rho_i=1$, and set the initial phases to zero.

**One-soliton solutions.** For $N=1$, the continuous Gram determinant reduces to

<a id="en-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{84}$$

where

<a id="en-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{85}$$

The corresponding physical fields are

<a id="en-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{86}$$

For $p+q>0$ and $c>0$, the sign of the u pulse is determined by $c-1$, while that of v is determined by $\ell$. We choose $(p,q)=(1,2)$ and $(4,-3)$ to obtain a negative and a positive u pulse, respectively. In the first case, $c=1/4$ and $\ell=-3/4$; in the second, $c=2$ and $\ell=-1/2$. Both choices give a negative v pulse.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_1_2.png" alt="Exact one-soliton solution with (p,q)=(1,2) at t=0. Left: u; right: v. Display window: x ∈ [−5,5], y ∈ [−5,5]." loading="lazy"><figcaption>Exact one-soliton solution with (p,q)=(1,2) at t=0. Left: u; right: v. Display window: x ∈ [−5,5], y ∈ [−5,5].</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_4_m3.png" alt="Exact one-soliton solution with (p,q)=(4,−3) at t=0. Left: u; right: v. Display window: x ∈ [−10,10], y ∈ [−10,10]." loading="lazy"><figcaption>Exact one-soliton solution with (p,q)=(4,−3) at t=0. Left: u; right: v. Display window: x ∈ [−10,10], y ∈ [−10,10].</figcaption></figure>

**Two-soliton solutions.** For $N=2$, expanding the Gram determinant gives

<a id="en-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{87}$$

where

<a id="en-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{88}$$

The physical fields are obtained from $u_*=2\partial_x\log(f_*/g_*)$ and $v_*=2\partial_x\partial_y\log(f_*g_*)$. For the first two-soliton test, we take $p_1=6$, $q_1=-5$, $p_2=4$, and $q_2=-3$, giving $c_1=4/3$, $c_2=2$ and $A_{12}=4/3$. The phases are $\theta_1=x-11t-y/12$ and $\theta_2=x-7t-y/2$, corresponding to two waves with different spatial orientations and propagation rates, which allow us to examine numerical performance in a two-wave interaction.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton.png" alt="Exact two-soliton solution with (p₁,q₁)=(6,−5), (p₂,q₂)=(4,−3) at t=0. Left: u; right: v. Display window: x ∈ [−30,30], y ∈ [−30,30]." loading="lazy"><figcaption>Exact two-soliton solution with (p₁,q₁)=(6,−5), (p₂,q₂)=(4,−3) at t=0. Left: u; right: v. Display window: x ∈ [−30,30], y ∈ [−30,30].</figcaption></figure>

The second two-soliton test takes $(p_1,q_1)=(1,2)$ and $(p_2,q_2)=(4,-3)$, with $c_1=1/4$, $c_2=2$ and $A_{12}=5/4$. Its phases are $\theta_1=3x+3t-3y/4$ and $\theta_2=x-7t-y/2$, producing positive and negative wave bands in u.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton_mixed.png" alt="Exact two-soliton solution: (1,2; 4,-3), t=0; u / v; [-30,30]²." loading="lazy"><figcaption>Exact two-soliton solution: (1,2; 4,-3), t=0; u / v; [-30,30]².</figcaption></figure>

**Initial and boundary data.** PE, PF and FD use the same initial physical fields. PE is initialized with $P^0=\delta_-u_*(0)$ and $W^0=v_*(0)-\delta_0u_*(0)$; FD uses the same $P^0$ and $v^0=v_*(0)$. PF uses the same continuous physical data, with Q normalized at the left x node; its reconstruction and lower-boundary initialization are specified in Appendix D.

**Computational settings and error measures.**

We next specify the regions and discretization parameters used in the numerical tests. To include the principal soliton profiles, we consider $[-5,5]^2$, $[-10,10]^2$, $[-30,30]^2$ and $[-30,30]^2$ for the four tests, respectively.

The corresponding computational domains are $[-10,10]^2$, $[-20,20]^2$, $[-40,40]^2$ and $[-40,40]^2$. PE and FD use periodic x continuation; PF uses the prescribed additive jumps of Q and R. Lower y data and u ghost values are supplied by the continuous exact solution. All methods use the same computational and evaluation regions.

The experiments use fixed grids and self-adaptive moving meshes (SAMM). On fixed grids, we take $\Delta x=h=0.1$. For SAMM, the y nodes remain uniformly spaced with $h=0.1$, while the x nodes are redistributed according to the conservation density introduced above, averaged over y.

Each test is advanced through 100 time steps. Specifically, starting at $t=0$, we use $\Delta t=10^{-4}$ and compute the solution up to $T=0.01$.

For error evaluation, cubic spline interpolation of the nodal fields along x provides a continuous representation in that direction, so that the numerical and exact solutions can be compared at the same spatial locations. We use the maximum absolute error over the evaluation points $\mathcal G$ in the region under consideration to measure the largest deviation from the exact solution at the final time:

<a id="en-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{89}$$

To interpret PE and PF errors, let $Z=(u,v)$ be the continuous exact field and $Z_h=(U_h,V_h)$ the semi-discrete exact field with the same spectral parameters, evaluated at the same positions as $Z_{\rm num}$. Then

<a id="en-eq-206"></a>

$$e_{\rm model}=Z_h-Z,\qquad e_{\rm num}=Z_{\rm num}-Z_h,\qquad e_{\rm total}=e_{\rm model}+e_{\rm num}.\tag{90}$$

Here $e_{\rm num}$ is the numerical deviation from the semi-discrete exact solution. It includes spatial and time discretization, reconstruction, and initial and boundary mismatches. With the continuous-field initialization used here, $e_{\rm num}(0)=-h^2C(0)+O(h^4)$, $C=(C_U,C_V)$, at points where the physical initialization is exact; any initialization reconstruction residual is additional. The continuous lower boundary likewise differs from that of the exact semi-discrete family. For a common discrete L² or RMS inner product, without subtracting means,

<a id="en-eq-207"></a>

$$\rho=\frac{\langle e_{\rm model},e_{\rm num}\rangle}{\|e_{\rm model}\|\,\|e_{\rm num}\|},\qquad \|e_{\rm total}\|^2=\|e_{\rm model}\|^2+\|e_{\rm num}\|^2+2\rho\|e_{\rm model}\|\,\|e_{\rm num}\|.\tag{91}$$

The direction cosine ρ is defined when both norms are nonzero and is not a Pearson correlation. A negative cross term describes cancellation in this inner-product norm. The maximum errors reported below remain total errors and do not obey this squared-norm identity. Right-hand-side truncation coefficients describe instantaneous forcing; their effect on final errors also depends on propagation and the initial and boundary data.

### 3.5 Numerical results {#en-results}

This subsection presents the results of the numerical experiments. We first compare the errors of PE, PF and FD on fixed grids, using RK4 for time evolution. We then hold the PE spatial discretization fixed and compare Euler, RK4 and C–N, followed by a comparison of fixed grids and SAMM. In the tables, $e_u=E_u(T)$ and $e_v=E_v(T)$ denote the maximum absolute errors in the two physical fields.

#### 3.5.1 Comparison of spatial discretizations {#en-spatial-results}

We compare the numerical errors of the different spatial discretizations. For each test, the initial data are prescribed by the exact solution, and PE, PF and FD are evolved on fixed grids by RK4 to $T=0.01$. The maximum absolute errors are computed by comparing the resulting physical fields U and V with the exact solution, as reported in Table 1.

**Table 1. Maximum absolute errors in e<sub>u</sub> / e<sub>v</sub> at T=0.01 for PE, PF and FD on fixed grids; RK4, Δx=h=0.1, Δt=10⁻⁴.**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>PE: e<sub>u</sub> / e<sub>v</sub></th><th>PF: e<sub>u</sub> / e<sub>v</sub></th><th>FD: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td>3.061201e-03 / 3.067031e-03</td><td><strong>4.715088e-04</strong> / <strong>1.201923e-03</strong></td></tr><tr><th>One-soliton (4, −3)</th><td><strong>1.419616e-05</strong> / 2.745967e-05</td><td>8.067776e-05 / 4.377502e-04</td><td>1.718043e-05 / <strong>2.605300e-05</strong></td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td><strong>3.552455e-05</strong> / 5.359645e-05</td><td>7.501357e-05 / 5.394947e-05</td><td>3.989986e-05 / <strong>5.173628e-05</strong></td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td>4.102555e-03 / 3.252786e-03</td><td><strong>4.782980e-04</strong> / <strong>1.350627e-03</strong></td></tr></tbody></table></div>

Across the four tests in Table 1, PE achieves the smallest maximum absolute error in U in two cases, while FD attains the smallest error in the largest number of comparisons. PF gives larger errors than both PE and FD in all four tests.

Figures 1–4 show the absolute-error surfaces at T=0.01, computed on fixed grids using RK4. The three columns correspond to the spatial discretization methods PE, PF and FD, from left to right. The first row shows the absolute error in U and the second row shows the absolute error in V. For each field, all three methods use the same colour and height scales.

**One-soliton (1, 2)**

Both fields in the first one-soliton test are negative oblique pulses. Figure 1 shows the absolute errors near the wave band.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png" alt="One-soliton (p=1, q=2): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>Figure 1. One-soliton (p=1, q=2): absolute-error surfaces.</figcaption></figure>

**One-soliton (4, −3)**

The second one-soliton test has a positive U pulse and a negative V pulse. In Figure 2, PF gives a larger V error than the other two methods.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png" alt="One-soliton (p=4, q=−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>Figure 2. One-soliton (p=4, q=−3): absolute-error surfaces.</figcaption></figure>

**Two-soliton (6, −5; 4, −3)**

The first two-soliton test contains two differently oriented wave bands. Figure 3 covers their interaction region and separated branches, comparing the error distributions in different parts of the domain.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png" alt="Two-soliton (6,−5; 4,−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>Figure 3. Two-soliton (6,−5; 4,−3): absolute-error surfaces.</figcaption></figure>

**Two-soliton (1, 2; 4, −3)**

The second two-soliton test combines positive and negative U wave bands. Figure 4 shows the absolute errors for this structure.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png" alt="Two-soliton (1,2; 4,−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>Figure 4. Two-soliton (1,2; 4,−3): absolute-error surfaces.</figcaption></figure>

In the following time-integration and mesh comparisons, we use PE throughout to keep the spatial discretization fixed and examine the effects of the time integrator and mesh placement separately.

#### 3.5.2 Time integration of PE {#en-time-results}

The fixed-grid PE comparison in Appendix F shows that the C–N and RK4 error profiles nearly coincide at the reported step size. Euler has a smaller u maximum error in some cases; such a ranking concerns total error, which also contains spatial and initial-data effects. RK4 is used throughout the mesh comparison.

#### 3.5.3 Numerical performance of the self-adaptive moving mesh method {#en-mesh-results}

We apply the SAMM constructed in [Section 3.2](#en-samm) to the four one- and two-soliton tests and compare its accuracy with that of fixed grids. The PE discretization and RK4 time integrator are used in both calculations. The node counts are kept the same, and the y spacing is $h=0.1$. In SAMM, the conservation density determines the moving x nodes, which evolve together with the fields up to $T=0.01$. Table 2 reports the maximum absolute errors obtained on the fixed and moving meshes.

**Table 2. Maximum absolute errors (e<sub>u</sub> / e<sub>v</sub>) of PE on fixed and moving meshes at T=0.01, using RK4.**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>Fixed mesh: e<sub>u</sub> / e<sub>v</sub></th><th>Moving mesh: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td><strong>5.781845e-04</strong> / <strong>1.091714e-03</strong></td></tr><tr><th>One-soliton (4, −3)</th><td>1.419616e-05 / 2.745967e-05</td><td><strong>1.334447e-05</strong> / <strong>2.621326e-05</strong></td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td>3.552455e-05 / 5.359645e-05</td><td><strong>3.304157e-05</strong> / <strong>5.060189e-05</strong></td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td><strong>6.156957e-04</strong> / <strong>1.428010e-03</strong></td></tr></tbody></table></div>

Figure 5 shows the error profiles $\max_j|U_{\rm num}-U_*|$ and $\max_j|V_{\rm num}-V_*|$ for the four tests, comparing the error distributions of the two mesh methods. Orange-red dashed lines and hollow circles denote fixed meshes; blue solid lines denote SAMM.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="PE_mesh_profiles" loading="lazy"></a><figcaption>Figure 5. PE absolute-error profiles on fixed and moving meshes at T=0.01.</figcaption></figure>

In all four tests, SAMM gives smaller maximum absolute errors in both U and V than the fixed-grid method. Thus, the self-adaptive mesh improves the accuracy of PE for the one- and two-soliton solutions considered here, with the degree of improvement depending on the soliton parameters and the physical field.

## 4. Conclusion {#en-conclusion}

We have studied the construction, exact solutions and numerical implementation of an integrable semi-discretization of the (2+1)-dimensional DLW equation. Starting from the continuous bilinear equations, we introduced a lattice in the y direction while retaining continuous x and t variables, and derived nonlinear formulations and numerical algorithms for the resulting semi-discrete system.

By combining a staggered lattice with shifted operator parameters, we constructed Gram determinant solutions of arbitrary finite order and used determinant identities to prove that the corresponding τ functions satisfy the proposed semi-discrete bilinear equations. Eliminating or retaining the auxiliary potential yields the PE and PF nonlinear formulations, respectively. Both recover the same physical fields from the corresponding positive τ-function solutions. We also obtained their Darboux–Lax representations and proved that the compatibility conditions yield the associated nonlinear equations.

We further established the relation between the semi-discrete system and the continuous DLW equation. As the lattice spacing tends to zero, the semi-discrete equations recover the continuous equations with second-order accuracy. Within the stated regular parameter range, the physical fields reconstructed from the exact semi-discrete solutions also converge to their continuous counterparts with second-order accuracy. These results identify the continuum limits of both the equations and their exact solutions.

We developed numerical algorithms based on PE and PF and compared them with direct finite differences applied to the continuous DLW equation, using exact one- and two-soliton solutions as benchmarks. Comparisons of spatial discretizations, time integrators and mesh configurations examined how these choices affect the numerical errors in the two physical fields.

We established a conservation law for the semi-discrete DLW equation and used it to select a mesh density, from which we constructed a self-adaptive moving mesh method that evolves the physical fields and node positions together. The method retains uniform nodes in the y direction and adjusts the x-node positions as the density evolves. With the same node counts and time integration method, the self-adaptive moving mesh reduced the maximum absolute errors in both physical fields in all four soliton tests, achieving higher accuracy with a given number of nodes.



## Appendix A. Leading exact-family difference {#en-app-a}

Set $z_i=p_i-a$, $w_i=q_i+a$. The principal-minor expansion pairs every selected row and column with the same index set I. The lattice phase contributes $h^2y\sum_{i\in I}c_i$, and the centred f amplitude in (55) contributes $h^2\sum_{i\in I}d_i$, where

<a id="en-eq-208"></a>

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,\qquad \alpha_2=\sum_i(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_i c_i\rho_i\partial_{\rho_i}\beta.\tag{92}$$

Indeed, $\rho_i\partial_{\rho_i}$ selects precisely those minors containing i. Expanding the determinant and then its logarithm therefore gives (92) for every fixed N. Symmetric reconstruction at the physical midpoint yields

<a id="en-eq-209"></a>

$$\begin{aligned}U_h&=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4),\\V_h&=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).\end{aligned}\tag{93}$$

Using $4\beta_{xy}=v-u_y$ gives (60). Fixed regular spectral parameters, nonvanishing τ functions on a neighbourhood of K, and sufficiently small h ensure uniform bounds for the required derivatives and remainders. The positive spectral domain in Theorem 2.9 supplies these conditions; other regular real branches may be used wherever the same bounds hold. No stability estimate for a general initial-value problem is asserted.

## Appendix B. Adjacent-layer determinant identity {#en-app-b}

**Proof.** Write the nth Gram matrix as $M=I+(r_ic_k/(p_i+q_k))$, with

<a id="en-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{94}$$

Let $P=\operatorname{diag}(p_i)$, $Q=\operatorname{diag}(q_i)$ and $b=(Q+sI)^{-1}c$. The definitions give

<a id="en-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{95}$$

The layer shift follows from

<a id="en-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{96}$$

Where M is invertible, define

<a id="en-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{97}$$

The last equality follows from the matrix determinant lemma, while Jacobi’s formula gives $\kappa=\tau_{n,x}/\tau_n$. To collect the differentiated terms, set

<a id="en-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{98}$$

Using $H_x=-HM_xH$ and $H_t=-HM_tH$, direct differentiation yields

<a id="en-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{99}$$

For example, $z_x=HPr-\kappa z$, so that $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$. Differentiating this identity once more and eliminating $\eta_1,\eta_2$ gives

<a id="en-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{100}$$

Thus $\psi=1-\zeta$ satisfies

<a id="en-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{101}$$

For $f=\psi g$, expansion of the bilinear operator gives

<a id="en-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{102}$$

Taking $g=\tau_n$ and $f=\tau_{n+1}$ proves [(13)](#en-eq-13) wherever M is invertible. To extend the result to singular matrices, replace all $\rho_i$ by $\varepsilon\rho_i$. At any fixed x,t, M is the identity at $\varepsilon=0$, and the bilinear residual vanishes for ε near zero. Since the residual is a polynomial in ε, it vanishes identically. Setting $\varepsilon=1$ completes the proof. □

## Appendix C. Darboux operator calculation {#en-app-c}

**Proof.** Set

<a id="en-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{103}$$

<a id="en-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{104}$$

Here $\mathscr B_j^{-1}$ is defined in the algebra of formal pseudodifferential operators. The linear system reads $\psi_{j+1}=T_j\psi_j$ and $\psi_{j,t}=H_j\psi_j$. Differentiating the lattice relation in t and using both time equations gives

<a id="en-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{105}$$

To verify this identity, define the scalar residuals

<a id="en-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{106}$$

Using $V_{j+1}-V_j=(h/2)w_{j,x}$ gives

<a id="en-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{107}$$

The w equation makes the difference vanish, and the definition of $V_{j,x}$ makes the sum vanish. Hence $\mathcal E_j^r=\mathcal E_j^s=0$. For a scalar function r, the product rule gives the Darboux identity

<a id="en-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{108}$$

The potential-difference relation implies

<a id="en-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{109}$$

Writing

<a id="en-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{110}$$

and applying the Darboux identity to the two vanishing residuals yields

<a id="en-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{111}$$

Eliminating the common intermediate operator gives $L_{j+1}T_j=T_jL_j$, which is equivalent to [(105)](#en-eq-75).

Conversely, assume compatibility and the potential-difference relation. The same operator calculation gives

<a id="en-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{112}$$

Comparing the coefficients of $\partial_x^0$ and $\partial_x^{-1}$ yields $\mathcal E_j^r=\mathcal E_j^s$ and $w_j\mathcal E_j^s=0$. Thus both residuals vanish wherever $w_j\ne0$. Their difference gives the w equation; their sum, after applying $\delta_-$ and using the potential-difference relation, gives the first nonlinear equation. □

## Appendix D. Reconstruction and boundary initialization {#en-app-d}

For PF, Q is determined by $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ with normalization $Q_{j,0}^0=1$, and $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$. The lower boundary $Q_0(t)$ is obtained from $u_{*,0}(t)$ by the same relation.

At each time, the physical fields are reconstructed by

<a id="en-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{113}$$

where $j_L$ denotes the lowest layer and $u_{j_L,i}(t)$ is prescribed by the lower boundary data.



The evolution equations also contain $(M_j+M_{j+1})_x$. To evaluate this term, introduce $m_j\simeq M_{j,x}$ and $S_j=Q_jR_j$. Applying $D_1$ to the lattice constraint $M_{j+1}-M_j=h(1-S_j)$ yields

<a id="en-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{114}$$

This relation determines the m layers successively once their lower boundary value is known. Temporarily labelling the lowest layer as 0, we obtain that value from the Q equation:

<a id="en-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{115}$$

Here $Q_0(t)$ is prescribed by the lower boundary data, and $Q_{0,t}$ is its time derivative.

## Appendix E. Derivatives on moving nodes {#en-app-e}

The physical x spacings become nonuniform as the nodes move. Introduce fixed uniform computational coordinates $\xi_i=-L/2+i\Delta\xi$, with $\Delta\xi=L/N_x$, and write $x_i(t)=\xi_i+s_i(t)$. The node displacement is $s_i$, and $J_i=1+D_\xi s_i$ approximates the mapping Jacobian $J=x_\xi$.

The chain rule gives $\partial_x=J^{-1}\partial_\xi$ and hence

<a id="en-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{116}$$

Approximating the computational-coordinate derivatives by centred differences gives

<a id="en-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{117}$$

Here $D_\xi,D_{\xi\xi}$ are the three-point formulas in [(69)](#en-eq-87) on the uniform computational grid. At moving nodes, each field variable satisfies $\dot z=F_z+\mathcal V D_1z$. Together with the node equation [(83)](#en-eq-100), this gives the coupled evolution system for the fields and the mesh. We advance this system using the time integrators in Section 3.3. The fixed-grid calculation corresponds to $s=0$ and $\mathcal V=0$.

## Appendix F. Implicit time stepping and comparison {#en-app-f}

The Crank–Nicolson (C–N) method averages the rates at adjacent time levels:

<a id="en-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{118}$$

For FD, the v update is $v^{n+1}=v^n+\Delta t(F_v^n+F_v^{n+1})/2$. Since the final rate depends on the unknown next-level fields, it is solved jointly with the P update. The coupled implicit equations are solved iteratively, using the forward Euler approximation as the initial guess.



We compare Euler, RK4 and C–N for all four soliton tests using the PE spatial discretization on fixed grids. Each test uses $\Delta x=h=0.1$, $\Delta t=10^{-4}$ and $T=0.01$. Table F1 lists the maximum absolute errors.

**Table F1. Time-integrator comparison for PE: maximum absolute errors (e<sub>u</sub> / e<sub>v</sub>).**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>Euler: e<sub>u</sub> / e<sub>v</sub></th><th>RK4: e<sub>u</sub> / e<sub>v</sub></th><th>C–N: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td><strong>6.396711e-04</strong> / 1.340634e-03</td><td>6.406395e-04 / <strong>1.339511e-03</strong></td><td>6.406384e-04 / 1.339513e-03</td></tr><tr><th>One-soliton (4, −3)</th><td>1.422394e-05 / 3.005484e-05</td><td><strong>1.419616e-05</strong> / <strong>2.745967e-05</strong></td><td>1.419664e-05 / 2.746028e-05</td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td>3.840649e-05 / 5.901085e-05</td><td><strong>3.552455e-05</strong> / <strong>5.359645e-05</strong></td><td>3.552653e-05 / 5.359819e-05</td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td><strong>6.188417e-04</strong> / 1.515498e-03</td><td>6.329588e-04 / <strong>1.511271e-03</strong></td><td>6.330018e-04 / 1.511273e-03</td></tr></tbody></table></div>

For each time integrator m, we consider the maximum absolute errors over the y index j, $\max_j|U_m(x,y_j,T)-U_*(x,y_j,T)|$ and $\max_j|V_m(x,y_j,T)-V_*(x,y_j,T)|$. Figure F1 plots these profiles, with insets near the RK4 error peaks.

<figure><a href="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="PE_time_profiles" loading="lazy"></a><figcaption>Figure F1. PE absolute-error profiles at T=0.01 with local enlargements.</figcaption></figure>

The C–N and RK4 error profiles nearly coincide in all four tests. Euler gives a smaller maximum absolute error in U for some tests, whereas RK4 gives smaller errors in the remaining comparisons. In the subsequent mesh experiments, we use RK4 throughout to examine the effect of node redistribution.

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


[10] E. Hairer, S. P. Nørsett, G. Wanner. *Solving Ordinary Differential Equations I: Nonstiff Problems*. 2nd revised ed., Springer, 1993. [Publisher](https://link.springer.com/book/10.1007/978-3-540-78862-1).

[11] S.-F. Tian, T.-T. Zhang, P.-L. Ma, X.-Y. Zhang. Lie symmetries and nonlocally related systems of the continuous and discrete dispersive long waves system by geometric approach. *Journal of Nonlinear Mathematical Physics* **22** (2015), 180–193. [DOI](https://doi.org/10.1080/14029251.2015.1023562).

[12] B.-F. Feng, K. Maruno, Y. Ohta. A self-adaptive moving mesh method for the Camassa–Holm equation. *Journal of Computational and Applied Mathematics* **235** (2010), 229–243. [DOI](https://doi.org/10.1016/j.cam.2010.05.044). [Preprint](https://arxiv.org/abs/0905.2693).

[13] B.-F. Feng, K. Maruno, Y. Ohta. Self-adaptive moving mesh schemes for short pulse type equations and their Lax pairs. *Pacific Journal of Mathematics for Industry* **6** (2014), 8. [DOI](https://doi.org/10.1186/s40736-014-0008-7). [Preprint](https://arxiv.org/abs/1403.6191).

[14] W. Huang, R. D. Russell. *Adaptive Moving Mesh Methods*. Applied Mathematical Sciences, vol. 174, Springer, 2011. [DOI](https://doi.org/10.1007/978-1-4419-7916-2).

[15] R. Hirota. *The Direct Method in Soliton Theory*. Cambridge Tracts in Mathematics, vol. 155, Cambridge University Press, 2004. [DOI](https://doi.org/10.1017/CBO9780511543043).

# （2+1）维色散长波系统的可积半离散化 {#zh-title}

**摘要。** 本文沿 y 方向构造（2+1）维色散长波（DLW）方程的可积半离散系统。该构造从连续双线性方程出发，沿 y 方向引入交错格点，并给出满足半离散双线性系统的任意阶 Gram 行列式解。通过消去或保留辅助势，得到差分消势形式（PE）与势函数形式（PF）两种非线性表示，并建立相应的 Darboux–Lax 表示。我们证明，当格距趋于零时，半离散方程以二阶精度恢复连续 DLW 方程，相应精确解所重构的物理场以二阶精度收敛到连续精确解，并给出两个精确解族之差首项的封闭形式。进一步，基于方程的守恒律构造网格密度，提出物理场与节点位置联立演化的自适应动网格方法。以单孤子和二孤子精确解为基准，比较 PE、PF 与直接差分方法的数值误差，并考察不同时间积分算法及自适应动网格的影响。数值结果表明，在所考察的四组算例中，所提出的自适应动网格方法均降低了两个物理场的最大绝对误差。

**关键词：** 色散长波方程；半离散化；Gram 行列式；Darboux–Lax 表示；连续极限；自适应动网格

## 1. 引言 {#zh-intro}

浅水中波的传播与相互作用长期以来受到非线性波研究的关注。在波的演化过程中，非线性效应与色散以不同方式影响波形，而二者的平衡能够支持在传播中持续存在的相干波。非线性长波方程以约化形式描述这些效应，使我们能够研究波动，而不必保留底层流体方程的全部复杂性。在这类方程中，可积模型因其提供的解析认识而持续受到关注。其精确解使我们能够追踪单个波的演化并考察波间相互作用，双线性形式与 Lax 表示则揭示了这些解背后的数学结构。这些解析结果也为数值研究提供了有用参照，其中波形及其演化需要在离散网格上表示。从连续模型转向这一表示时，所作的选择既影响波的逼近，也影响所得方程的数学结构。可积离散化旨在保留这两方面的联系，将离散方程的构造与其精确解及连续极限的研究结合起来。

（2+1）维色散长波（DLW）系统将色散长波方程推广到两个空间维度 [1]，并被用于研究宽水道及有限深外海中的波动 [3,4]。自 Boiti、Leon 与 Pempinelli 提出这一系统以来，研究者通过若干相互关联的解析方法研究其波解。最初的工作建立了逆谱变换、Bäcklund 变换及叠加公式 [1]；随后发展的非线性变换 [2] 与双线性方法 [3]，为生成解和理解解之间的联系提供了进一步的途径。行列式表示使这些联系具有了具体的表达形式。Hu、Xu 与 Yu 构造了 Grammian 和 Wronskian 解 [4]，而 Sheng 与 Yu 通过 KP 层级约化，得到了描述常值与周期背景上孤子、线呼吸子及有理波的 Gram 行列式解 [5]。

这些解所满足的双线性关系，也为引入格点提供了出发点 [15]。在这一思路下，Bäcklund 变换将相邻格点上的取值联系起来，使离散方程能够与其解结构一同构造。这一方法已用于半离散孤子方程 [7]，并推广到具有两个空间维度的系统 [8]。对于 DLW 系统，它与（2+1）维 sinh-Gordon 方程之间的双线性关系 [5] 又提供了一条联系：后者的可积离散化具有行列式解及 Bäcklund–Lax 结构 [6]。结合已有的离散 DLW 系统研究 [11]，这些进展促使我们进一步考察，如何将连续 DLW 解族引入空间格点，以及由此得到的波场与连续波场之间有怎样的对应关系。

随着这些进展，我们有望在同一构造中研究可积结构的保留与连续波的逼近。带着这一考虑，我们提出如下问题：如何引入空间格点，使其保留双线性与行列式结构，支持一致的物理场重构，并允许对其精确解与连续系统精确解进行定量比较？

围绕这一问题，我们希望得到 DLW 系统沿 $y$ 方向的半离散描述，同时保持 $x$ 与 $t$ 连续。首先，我们希望保留显式波解与支持其演化的可积结构之间的联系。更具体而言，我们寻求能够显式表达离散波场、便于解析研究的 Gram 行列式解。相应的 Lax 表示则应通过其相容条件描述同一非线性演化。其次，我们希望理解将连续波表示在格点上时发生了什么变化。这需要定量比较重构物理场，而不止是在极限中恢复连续方程。这样的比较能够揭示离散波如何趋近其连续对应。数值计算还会通过空间差分与时间推进引入进一步的近似，因此计算场的精度也取决于半离散方程的实现方式。由此，我们希望以精确解为参照，考察非线性表示、时间积分器与网格如何影响所得误差。

在第 2 节，我们从 Sheng 与 Yu [5] 给出的连续双线性形式及 Gram 行列式解出发，将 $y$ 方向的交错格点与双线性算子参数的平移相结合，引入半离散双线性系统。我们首先利用相邻层之间的恒等式，证明所提出的 Gram 行列式满足这一系统。随后，我们导出两种非线性表示：第一种为消去辅助势的差分消势形式（PE），第二种为保留辅助势的势函数形式（PF）。对于两种表示，我们建立物理场重构，并导出相容条件给出相应非线性方程的 Darboux–Lax 表示。连续极限分析进一步将这一构造与原 DLW 系统联系起来。我们证明方程的二阶相容性，并在固定正则谱参数、所考察紧集上 $\tau$ 函数为正的条件下，证明重构精确解的二阶收敛。二者之差首项的显式表达说明了格点如何改变连续波场。

在第 3 节，我们通过四组孤子算例考察数值方法：两组单孤子算例中 $u$ 脉冲符号相反，两组双孤子算例则涵盖 $u$ 场中同极性与异极性波的相互作用。这些算例提供精确参照，使我们能够在不同波形及相互作用模式下考察数值方法。我们建立 PE、PF 的空间离散，以及连续方程的直接有限差分近似。为理解 $x$ 方向离散的影响，我们在固定网格上推导 PE 与直接差分的重构 $u$ 演化中首项为 $O(\Delta x^2)$ 的截断项。我们还基于半离散系统的守恒律引入自适应动网格方法。该方法联立演化物理场与节点位置，利用横向平均守恒密度重新分配共享的 $x$ 节点，同时保留 $y$ 方向的均匀格点。随后，我们介绍时间积分方法，并明确算例与误差度量。最后，我们讨论非线性表示、时间积分与网格自适应如何影响两个物理场的误差，并结合解析展开解释数值结果。

## 2. 半离散 DLW 系统与精确解 {#zh-continuous}

本节中，我们将双线性方程、精确解与物理场重构纳入一致的构造，建立 DLW 系统的半离散形式。在第 2.1 节，我们回顾 Sheng 与 Yu [5] 给出的连续双线性形式及 Gram 行列式解，以及联系 τ 函数与物理场的变换。在这些关系的基础上，我们在第 2.2 节沿 $y$ 方向引入交错格点，将格点平移与双线性参数的平移相结合，同时保持 $x$ 与 $t$ 连续。在第 2.3 节，我们构造相应的 Gram 行列式解，并证明它们满足半离散双线性方程。在第 2.4 节，我们转向物理场，通过消去或保留辅助势导出两种非线性表示，并分别明确其重构关系。在第 2.5 节，我们考察方程及其精确解的连续极限，以确定格点系统如何恢复连续 DLW 动力学，以及其波场如何趋近相应的连续波场。最后，在第 2.6 节，我们导出 Darboux–Lax 表示，并验证其相容条件给出相应的非线性方程。

### 2.1 连续 DLW 系统与双线性形式 {#zh-preliminaries}

这里，我们希望明确连续 DLW 系统中哪些关系将被引入相应的半离散系统。具体而言，我们寻求一种既能构造精确解、又能由这些解恢复物理波场的表示，使二者在引入格点后仍保持联系。为此，我们回顾 Sheng 与 Yu [5] 的双线性形式及 Gram 行列式解，着重说明 τ 函数与物理场之间的变换。沿用其归一化形式，我们取 $\lambda=-2$，将连续系统写为

<a id="zh-eq-1"></a>

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

其中 $a\in\mathbb R$ 为常数。我们采用两个充分光滑的正 τ 函数 $f$ 与 $g$，并通过以下变换恢复物理场：

<a id="zh-eq-2"></a>

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

这一变换使我们能够通过 $f$ 与 $g$ 之间的关系构造波场。具体而言，我们采用文献 [5] 中的双线性方程

<a id="zh-eq-3"></a>

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

其中 $B_s=D_x^2+D_t+2sD_x$。我们在这一记号中保留参数 $s$，因为该参数的平移将参与第 2.2 节的格点构造。为明确记号，我们将 Hirota 双线性算子定义为

<a id="zh-eq-4"></a>

$$D_x^rD_y^sD_t^m f\cdot g=\left.(\partial_x-\partial_{x\prime})^r(\partial_y-\partial_{y\prime})^s(\partial_t-\partial_{t\prime})^m f(x,y,t)g(x\prime,y\prime,t\prime)\right|_{(x\prime,y\prime,t\prime)=(x,y,t)}.\tag{4}$$

其中 $r,s,m$ 均为非负整数。下面，我们首先说明如何由双线性方程的解得到物理场方程的解。

**命题 2.1（双线性表示 [5]）。** 若充分光滑的正函数 $f,g$ 满足双线性方程 [(3)](#zh-eq-3)，则由变换 [(2)](#zh-eq-2) 定义的物理场满足 DLW 系统 [(1)](#zh-eq-1)。

**证明。** 我们将双线性方程除以 $fg$，用对数导数展开 Hirota 算子，再代入变换 [(2)](#zh-eq-2)，即可得到系统 [(1)](#zh-eq-1) 中的两个方程，参见 [5, Section 2]。□

在明确这一联系后，我们回顾文献 [5] 中的连续 Gram 行列式解。我们将以这一解族指导半离散行列式的构造，并以其作为连续极限中比较重构波场的参照。τ 函数具有如下形式：

<a id="zh-eq-5"></a>

$$\tau_n^{(0)}=\det_{1\le i,k\le N}\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\left(-\frac{p_i-a}{q_k+a}\right)^n e^{\xi_i+\eta_k}\right],\quad f=\tau_1^{(0)},\quad g=\tau_0^{(0)},\tag{5}$$

其中相位为

<a id="zh-eq-6"></a>

$$\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad \eta_k=q_kx+q_k^2t+\frac{y}{q_k+a}.\tag{6}$$

这里，$N$ 为行列式阶数，$n$ 为辅助整数指标，$\delta_{ik}$ 为 Kronecker 符号。我们选取实参数，使上述各分母均不为零，并将物理场限制在 $f$ 与 $g$ 均为正的区域内。下面的命题说明，这一行列式解族满足物理场重构所依据的双线性方程。

**命题 2.2（连续 Gram 行列式解 [5]）。** 设 $\tau_n^{(0)}$ 由公式 (5)–(6) 定义，且参数选取使上述各分母均不为零，则 $f=\tau_1^{(0)}$ 与 $g=\tau_0^{(0)}$ 满足双线性方程 [(3)](#zh-eq-3)。因此，在 $f$ 与 $g$ 均为正的任意区域内，通过变换 [(2)](#zh-eq-2) 重构的物理场满足连续 DLW 系统 [(1)](#zh-eq-1)。

**证明。** 这一 Gram 行列式解族所满足的双线性恒等式由文献 [5] 中的 KP 层级约化得到。取 $f=\tau_1^{(0)}$ 与 $g=\tau_0^{(0)}$，这些恒等式即给出方程 [(3)](#zh-eq-3)。随后，由命题 2.1 可知，重构出的物理场满足连续 DLW 系统。□

至此，我们得到了一族显式解，其中 τ 函数与物理场通过双线性方程及重构公式相联系。下一小节中，我们将利用这一解族对 $y$ 的依赖来指导格点构造，以期在半离散情形下保留这些关系。

### 2.2 半离散双线性方程 {#zh-bilinear}

在连续双线性形式的基础上，我们希望引入空间格点，同时保留这一形式与行列式解之间的联系。具体而言，我们希望保留能够支持显式波解及一致物理场重构的结构。格点方程还应在间距趋于零时恢复连续双线性系统。带着这些要求，我们首先考察方程组 (3) 中两式之间的联系，并以此指导离散平移的选取。

具体而言，我们关注 $y$ 方向的依赖如何进入双线性系统。第一式仅涉及 $x$ 与 $t$ 的导数，第二式则通过同一个算子 $B_a$ 联系 $y$ 方向的变化。这一共同结构启发我们沿 $y$ 方向引入格点，同时保持 $x$ 与 $t$ 连续。为展开这一思路，我们首先改写方程，使 $y$ 方向求导与算子参数变化之间的关系显现出来。对 (3) 的第一式关于 $y$ 求导，再结合第二式，我们得到

<a id="zh-eq-7"></a>

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{7}$$

将这一关系与 $B_af\cdot g=0$ 联立，即得到与连续双线性系统 (3) 等价的表示。公式 (7) 中的两项启发我们同时平移第二个 τ 函数与算子参数。因此，我们引入

<a id="zh-eq-8"></a>

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t).\tag{8}$$

由于 $B_{a+s}=B_a+2sD_x$，我们有

$$\Phi(0)=B_af\cdot g,\qquad \Phi'(0)=B_af\cdot g_y+2D_xf\cdot g.$$

这样，连续双线性方程便可表示为 $\Phi(0)=0$ 与 $\Phi'(0)=0$ 两个条件。这一观察启发我们采用对称的格点构造：用分别对应 $s=-h/2$ 与 $s=h/2$ 的两条双线性关系替代这两个条件。

对于 $h>0$ 和 $j\in\mathbb Z$，我们将 $F_j(x,t)$ 放置在 $y=(j+\tfrac12)h$，将 $G_j(x,t)$ 放置在 $y=jh$，并保持 $x,t$ 连续。相对于 $F_j$，相邻的 $G_j$ 与 $G_{j+1}$ 恰好位于两个对称位置。我们将这两个偏移分别与参数值 $a-h/2$、$a+h/2$ 配对，由此提出半离散双线性系统

<a id="zh-eq-9"></a>

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{9}$$

这里，$F_j$ 与 $G_j$ 是待求的格点 τ 函数。它们的位置规定了与连续函数 $f,g$ 进行比较时的对应方式，并不要求格点函数等于连续解在相应位置的采样值。我们将在第 2.3 节构造系统 (9) 的精确 Gram 行列式解，并在第 2.5 节建立这一交错对应下的收敛性。

为检验所提出关系的局部相容精度，我们回到公式 (8)，在 $s=0$ 附近展开。当 $f,g$ 充分光滑时，对称 Taylor 展开给出

<a id="zh-eq-10"></a>

$$\frac{\Phi(h/2)+\Phi(-h/2)}2=B_af\cdot g+O(h^2),\qquad \frac{\Phi(h/2)-\Phi(-h/2)}h=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{10}$$

因此，对称平均与差商分别以二阶相容精度恢复 (3) 的第一式及等价关系 (7)，从而建立与连续双线性系统的联系。接下来，我们进一步考察所提出的格点关系是否也具有相应的行列式解族。

### 2.3 Gram 行列式解 {#zh-gram}

现在，我们转向半离散双线性系统 (9) 的精确解。为构造这些解，我们调整公式 (5) 中的连续 Gram 行列式，保留其对 $x$ 与 $t$ 的依赖，同时将依赖于 $y$ 的指数因子替换为格点因子。这些因子的选取将行列式公式与前面导出的方程联系起来：它们既需要适应方程 (9) 中格点与参数的耦合平移，也应在 $h\to0$ 时趋于连续指数因子。因此，我们希望找到一种形式，使双线性恒等式的验证与连续解族之间对应关系的建立都能在其中展开。

我们选取格点因子

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad d=\frac h2.$$

对于固定的非零 $z$ 和充分小的 $h$，展开可得

$$\log\lambda_h(z)=\frac hz+O(h^3).$$

因此，当 $h\to0$ 且 $jh=y$ 保持固定时，$\lambda_h(z)^j$ 趋于 $e^{y/z}$。由此，我们可以用这一因子的整数次幂替换连续形式中依赖于 $y$ 的指数因子。它的分子与分母还包含与方程 (9) 中算子参数相同的半步偏移，使我们能够在下面的行列式恒等式中联系格点平移与参数平移。

据此，我们定义

<a id="zh-eq-11"></a>

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{11}$$

其中，$\delta_{ik}$ 为 Kronecker 符号。我们保留辅助指标 $n$，以建立序列中相邻成员之间的双线性恒等式；同时保留参数 $s$，以处理方程 (9) 中的两个算子。当 $n=0$ 时，行列式与 $s$ 无关，因此记作 $\tau_0(j;s)=\tau_0(j)$。下面的定理明确了应选取哪些成员作为所需的格点 τ 函数。

**定理 2.3（Gram 行列式解）。** 设 $h>0$、$N\ge1$，实参数 $p_i,q_i,\rho_i$ 对所有 $i,k$ 满足 $p_i+q_k\ne0$、$p_i-a\pm d\ne0$ 及 $q_k+a\pm d\ne0$。则函数

<a id="zh-eq-12"></a>

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{12}$$

在每个格点 $j\in\mathbb Z$ 上均满足半离散双线性系统 [(9)](#zh-eq-9)。

为证明这一结果，我们首先在固定格点处建立相邻 $n$ 层之间的双线性恒等式。该恒等式直接给出方程组 (9) 的第一式。对于第二式，我们将证明：当格点指标由 $j$ 移至 $j+1$，同时参数由 $a-d$ 变为 $a+d$ 时，定义 $F_j$ 的行列式保持不变。这样，我们便可以在相邻格点处应用同一恒等式。

**引理 2.4（相邻层恒等式）。** 在定理 2.3 的谱条件下，固定格点 $j$，并选取参数 $s$，使所有 $i,k$ 均满足 $p_i-s\ne0$ 与 $q_k+s\ne0$。则对每个 $n\in\mathbb Z$，均有

<a id="zh-eq-13"></a>

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{13}$$

**证明。** 我们利用矩阵行列式引理，以及对行列式元素求导得到的秩一恒等式，建立公式 (13)。详细计算见[附录 B](#zh-app-b)，其中还将这一恒等式延拓到定义 τ 函数的矩阵为奇异矩阵的情形。□

**定理 2.3 的证明。** 首先，我们在格点 $j$ 处应用恒等式 (13)，取 $n=0$ 与 $s=a-d$。由于 $\tau_0(j;s)$ 与 $s$ 无关，根据定义 (12)，可得

$$B_{a-d}F_j\cdot G_j=B_{a-d}\tau_1(j;a-d)\cdot\tau_0(j)=0.$$

这就得到了方程组 (9) 的第一式。

为得到第二式，我们需要在算子 $B_{a+d}$ 下将 $F_j$ 与 $G_{j+1}$ 配对。所需的联系来自格点因子的选取：

<a id="zh-eq-23"></a>

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{14}$$

将这一恒等式应用于行列式的各个元素，我们得到

<a id="zh-eq-24"></a>

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{15}$$

因此，只要将参数从 $a-d$ 同步移至 $a+d$，同一个函数 $F_j$ 就可以用相邻格点 $j+1$ 处的行列式表示。在该格点处取 $n=0$、$s=a+d$，再次应用恒等式 (13)，便得到

<a id="zh-eq-25"></a>

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{16}$$

这证明了方程组 (9) 的第二式，定理得证。□

恒等式 (15) 说明了行列式构造如何适应双线性系统中的两个移位算子。现在，我们可以利用这些 τ 函数重构物理场。在此之前，我们先给出保证其为正的一个充分条件，使重构中的对数保持良好定义。

上述行列式恒等式在不要求 τ 函数为正的情况下，就能保证双线性方程成立。不过，为通过对数导数重构实值物理场，我们将在 $F_j$ 与 $G_j$ 均为正的区域内进行讨论。下面，我们给出一个充分的参数条件，使这一性质对所有 $x,t$ 以及每个格点都成立。

**命题 2.5（正 τ 函数）。** 假设 $0<p_1<\cdots<p_N<a-h/2$、$0<q_1<\cdots<q_N$ 且 $\rho_i>0$。则由公式 (12) 定义的 τ 函数对所有 $x,t\in\mathbb R$ 和 $j\in\mathbb Z$ 均满足 $F_j\ge1$、$G_j\ge1$。

**证明。** 在这些条件下，格点因子 $\lambda_h(p_i-a)$ 与 $\lambda_h(q_k+a)$ 均为正。$F_j$ 中额外的因子也为正，因为

$$-\frac{p_i-a+d}{q_k+a-d}>0.$$

因此，我们可以将定义 $F_j$ 或 $G_j$ 的矩阵分别写成 $I+D_1CD_2$，其中 $C_{ik}=1/(p_i+q_k)$，$D_1,D_2$ 均为正对角矩阵。对于任意非空指标集 $I\subseteq\{1,\ldots,N\}$，Cauchy 行列式公式给出

<a id="zh-eq-26"></a>

$$\det C_{I,I}=\frac{\prod_{i<k,\ i,k\in I}(p_k-p_i)(q_k-q_i)}{\prod_{i,k\in I}(p_i+q_k)}>0.\tag{17}$$

左右乘以正对角矩阵后，这些主子式仍保持为正。随后，我们将 $\det(I+D_1CD_2)$ 展开为 $D_1CD_2$ 的全部主子式之和，并计入取值为 $1$ 的空主子式。每个非空项均为正，因此得到所述下界。□

这一条件给出了 τ 函数在整个格点演化过程中保持为正的参数范围。它是充分条件，并非必要条件；在这一范围之外，只要两个 τ 函数在所考虑区域内均为正，我们仍可重构物理场。在建立行列式解及其正则性条件之后，我们接下来转向控制重构物理场演化的非线性方程。

### 2.4 非线性表示 {#zh-nonlinear}

现在，我们从双线性方程转向物理场的演化。我们希望用能够与连续物理场 $u,v$ 进行比较的变量表示半离散系统，同时保留前面构造的精确解。为此，物理场重构需要考虑 $F_j$ 与 $G_j$ 的交错位置。我们首先在这一格点上定义物理场，再从两条双线性方程导出其演化关系。随后，根据辅助势的消去或保留，这些关系将引出两种非线性表示。

在 $F_j$ 所在位置的两侧，相邻函数 $G_j$ 与 $G_{j+1}$ 对称分布。因此，我们利用二者对数的平均值定义 $u_j$，并引入 $\omega_j$，描述相邻格点之间对数 $x$ 导数的变化。对于正 τ 函数，我们采用如下定义：

<a id="zh-eq-27"></a>

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad \omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad v_j=\frac4h\omega_j+\delta_0u_j,\qquad \delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h}.\tag{18}$$

我们将重构出的物理场 $u_j,v_j$ 对应于 $y=(j+\tfrac12)h$。其中，$v_j$ 的定义依据连续恒等式

$$v=4(\log g)_{xy}+u_y,$$

它可由变换 (2) 直接得到。在公式 (18) 中，$4\omega_j/h$ 逼近 $4(\log g)_{xy}$，而 $\delta_0u_j$ 逼近 $u_y$。这些关系构成了连续物理场变换的离散对应，其二阶相容性将在第 2.5 节建立。在下面的推导中，我们采用 $u_j,\omega_j$ 作为变量，再通过公式 (18) 恢复 $v_j$。

令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。将两条双线性方程分别除以 $F_jG_j$ 和 $F_jG_{j+1}$，得到

<a id="zh-eq-28"></a>

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{19}$$

由物理场定义可得

<a id="zh-eq-29"></a>

$$(\alpha_j-\beta_j)_x=\frac{u_j+\omega_j}{2},\qquad (\alpha_j-\beta_{j+1})_x=\frac{u_j-\omega_j}{2}.\tag{20}$$

在 $A_j+C_j$ 中，二阶导数项合并为 $(2\alpha_j+\beta_j+\beta_{j+1})_{xx}$。因此引入

<a id="zh-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{21}$$

分别对 $A_j+C_j=0$ 和 $A_j-C_j=0$ 关于 x 求导，得到

<a id="zh-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{22}$$

下面从这些演化方程出发，导出两种非线性表示。第一种通过格点差分消去 $Z_j$，第二种则利用势变量表示 $Z_j$。对于第一种表示，引入后向差分算子与平均算子

<a id="zh-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{23}$$

由 $u_j,\omega_j,Z_j$ 的定义可得

<a id="zh-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{24}$$

对第一条演化方程施加 $\delta_-$，并代入上述恒等式，得到差分消势形式（PE）

<a id="zh-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{25}$$

对于第二种表示，引入势变量 $M_j=\beta_{j,x}$。由定义可得

<a id="zh-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{26}$$

代入后，第一条演化方程中出现组合 $u_{j,x}+u_j^2/2$。因此引入

<a id="zh-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{27}$$

从而

<a id="zh-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{28}$$

由求导前的关系 $(A_j+C_j)/2=0$，得到

<a id="zh-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{29}$$

第二条演化方程中的通量可写为

<a id="zh-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{30}$$

为消去其中的商，定义

<a id="zh-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{31}$$

利用恒等式

<a id="zh-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{32}$$

ω 的方程化为

<a id="zh-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{33}$$

由于

<a id="zh-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{34}$$

代入 Q 的方程即得 R 的演化方程。结合格点约束，得到势函数形式（PF）

<a id="zh-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{35}$$

其中 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。物理场由下式恢复：

<a id="zh-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{36}$$

下面的命题说明，两种非线性表示由同一对正 τ 函数恢复完全相同的物理场。

**命题 2.6（共同物理场）。** 设正函数 F、G 满足 [(9)](#zh-eq-9)。由它们构造的两种非线性表示在每个有限正格距 h 下给出完全相同的物理场 u、v。

**证明。** 由定义有

<a id="zh-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{37}$$

在第二个等式两侧加上相同的 u 中心差分，即得两种重构的 v 也一致。□

### 2.5 连续极限 {#zh-limits}

在得到两种非线性表示后，下面考察它们在 $h\to0$ 时的连续极限。首先建立物理场重构及半离散方程与相应连续表达之间的二阶一致性。随后证明，在固定正则谱参数下，Gram 行列式解以 $h^2$ 阶误差在紧集上一致收敛到连续 DLW 解。

本小节中，$O_K(h^m)$ 表示在紧集 K 上由 $C_Kh^m$ 一致控制的余项，所涉及函数在 K 的开邻域内光滑。下面的命题联系交错重构与连续因变量变换。

**命题 2.7（重构的一致性）。** 设 f、g 为正光滑函数，u、v 由 [(2)](#zh-eq-2) 给出。在物理位置 y 处定义

<a id="zh-eq-47"></a>

$$\begin{aligned}u^{[h]}(y)&=\partial_x[2\log f(y)-\log g(y-h/2)-\log g(y+h/2)],\\\omega^{[h]}(y)&=\partial_x[\log g(y+h/2)-\log g(y-h/2)],\\v^{[h]}(y)&=\frac4h\omega^{[h]}(y)+\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}.\end{aligned}\tag{38}$$

上式省略了 x、t 变量。则

<a id="zh-eq-48"></a>

$$u^{[h]}=u+O_K(h^2),\qquad v^{[h]}=v+O_K(h^2).\tag{39}$$

**证明。** 记 $\alpha=\log f$、$\beta=\log g$。对称 Taylor 展开给出

<a id="zh-eq-49"></a>

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad \frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).\tag{40}$$

第一个展开式求导后仍成立，因此

<a id="zh-eq-50"></a>

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2),\qquad v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2).\tag{41}$$

即得结论。□

下面考察非线性方程。令

<a id="zh-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{42}$$

第一种表示可写为

<a id="zh-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{43}$$

记 $\mathcal M_+z_j=(z_{j+1}+z_j)/2$。由 $\mathcal M_+\delta_-=\delta_0$ 可知，$\mathcal M_+E_{1,h,j}+E_{2,h,j}=0$ 给出 v 的演化方程。

**命题 2.8（方程的一致性）。** 将光滑场 u、v 采样于 $y_j=(j+\tfrac12)h$，并记连续 DLW 方程的残差为

<a id="zh-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{44}$$

则在紧集上一致有

<a id="zh-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{45}$$

**证明。** 记 $m_j=y_j-h/2$。Taylor 展开给出

<a id="zh-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{46}$$

从而

<a id="zh-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{47}$$

上述展开在所需导数下仍成立，由此得到 $E_{1,h,j}=\mathcal C_1(m_j)+O_K(h^2)$。令 $w=v-u_y$，第二个残差为

<a id="zh-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{48}$$

将第一个残差在 y_j 两侧取平均，再加上第二个残差，得到

<a id="zh-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{49}$$

上式所有连续场均在 y_j 处取值，即得第二个结论。□

最后建立精确 Gram 解的连续极限。此时 τ 函数通过格点乘子和辅助参数的平移依赖于 h。

**定理 2.9（Gram 解的连续极限）。** 固定 N 和谱参数，并设存在 $h_0>0$ 使

<a id="zh-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{50}$$

对于 $0<h\le h_0$，将正格点乘子延拓到实数指数，并定义

<a id="zh-eq-60"></a>

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{51}$$

因此 $g^{(h)}(x,jh,t)=G_j$，$f^{(h)}(x,(j+\tfrac12)h,t)=F_j$。记其交错重构为 $u^{(h)},v^{(h)}$，并令 $f^{(0)},g^{(0)}$ 为 [(5)](#zh-eq-5) 中的连续 Gram 函数。相应物理场 $u^{(0)},v^{(0)}$ 满足连续 DLW 系统，且对任意紧集 K 有

<a id="zh-eq-61"></a>

$$\sup_K\bigl(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\bigr)\le C_Kh^2\tag{52}$$

其中 h 为充分小的正数。该估计对两种非线性表示均成立。

**证明。** 记 $z_i=p_i-a$、$w_k=q_k+a$。对于固定谱参数，

<a id="zh-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{53}$$

因此指数项中 y 的系数满足

<a id="zh-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{54}$$

对于 $f^{(h)}$，辅助参数平移与半格点平移共同给出振幅因子

<a id="zh-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}+O(h^2).\end{aligned}\tag{55}$$

因此相位和振幅与相应连续表达均相差 $O(h^2)$。由于 N 固定，对任意固定混合导数 $\partial^\nu$ 有

<a id="zh-eq-65"></a>

$$\partial^\nu(f^{(h)}-f^{(0)})=O_K(h^2),\qquad \partial^\nu(g^{(h)}-g^{(0)})=O_K(h^2).\tag{56}$$

命题 2.5 的正性论证同样适用于实数指数延拓及其极限。四个 τ 函数均不小于 1，因此相应对数导数也满足一致二阶估计。

相邻层恒等式和格点移位关系在延拓后仍成立，因此

<a id="zh-eq-66"></a>

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.\tag{57}$$

利用上述一致导数界，对两式取对称平均与差商，再令 h 趋于零，得到

<a id="zh-eq-67"></a>

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.\tag{58}$$

这正是第 2.2 节中的连续双线性方程等价形式，故由命题 2.1 得到连续 DLW 解。最后，将命题 2.7 一致地应用于依赖 h 的解族，得到

<a id="zh-eq-68"></a>

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).\tag{59}$$

结合 [(56)](#zh-eq-65) 即得所需估计。由命题 2.6，该结论同时适用于两种非线性表示。□

**命题 2.10（精确解族之差的首项）。** 固定 N，并在连续与半离散 Gram 行列式中取同一组正则谱参数。在 τ 函数远离零的紧区域上选取光滑对数，记 $\alpha=\log f$、$\beta=\log g$，并按 (51) 的延拓写成 $\log f_h=\alpha+h^2\alpha_2+O_K(h^4)$、$\log g_h=\beta+h^2\beta_2+O_K(h^4)$。在共同物理位置 $y=(j+\tfrac12)h$，重构的精确场满足

<a id="zh-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{60}$$

上述展开连同重构所需导数一致成立，系数及证明见[附录 A](#zh-app-a)。这是精确解族的渐近比较；两族在初始时刻已经存在差异。

### 2.6 Darboux–Lax 表示 {#zh-lax}

下面构造半离散 DLW 系统的 Darboux–Lax 表示。首先以物理场写出线性问题，再给出它在势变量 Q、R、M 下的形式。

引入平移后的变量

<a id="zh-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{61}$$

第一种非线性表示可写为

<a id="zh-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{62}$$

为构造线性问题，引入辅助势 V，满足

<a id="zh-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{63}$$

这两条关系的相容条件恰为第一条非线性方程。在局部 x 区间和格点链上，可以先在一个参考格点积分，再沿格点递推，构造辅助势 V；其自由度为所有格点共有的时间函数。

考虑如下辅助线性方程：

<a id="zh-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{64}$$

第一条方程联系相邻格点上的波函数，第二条给出它们的时间演化。下面的定理建立该线性系统与非线性方程之间的相容关系。

**定理 2.11（Darboux–Lax 相容性）。** 系统 [(62)](#zh-eq-70) 的每个光滑解，连同 [(63)](#zh-eq-71) 确定的辅助势，都使 [(64)](#zh-eq-72) 在形式算子意义下相容。反之，在 $w_j\ne0$ 的区域内，相容条件与辅助势的格点差关系共同推出 [(62)](#zh-eq-70)。

**证明。** 将格点转移分解为 $T_j=\mathscr B_j^{-1}\mathscr A_j$，其中 $\mathscr A_j=\partial_x-U_j/2-hw_j/8$、$\mathscr B_j=\partial_x-U_j/2+hw_j/8$。场方程使两个标量 Darboux 残差均为零，并给出共同的中间势，从而 $T_{j,t}=H_{j+1}T_j-T_jH_j$。反之，零阶与负一阶系数在 $w_j\ne0$ 时迫使两残差为零，其和与差恢复场方程。算子恒等式见[附录 C](#zh-app-c)。□

对于 τ 函数解，可取

<a id="zh-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{65}$$

将双线性方程分别除以相应 τ 函数乘积，再对 x 求导，即得 $\mathcal E_j^r=\mathcal E_j^s=0$。因此 Gram 行列式解满足上述 Darboux–Lax 相容关系。

最后代入势变量关系

<a id="zh-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{66}$$

线性系统化为

<a id="zh-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{67}$$

对格点约束求 x 导数可得

<a id="zh-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{68}$$

Q、R 的演化方程使两项标量残差为零，从而保证线性系统相容。反之，当 $Q_jR_j\ne0$ 时，相容条件与该辅助势差关系共同恢复第一种表示的物理场方程。

上述构造给出了两种非线性表示共同的 Darboux–Lax 表示。格点平移通过共享中间势的两个一阶 Darboux 算子实现，其与时间演化的相容性由半离散场方程保证。

## 3. 数值方法与实验 {#zh-numerics}

本节基于 PE 与 PF 两种非线性表示开展数值计算，并与连续 DLW 系统的直接差分方法进行比较。首先，对半离散系统中保留的 x 导数进行空间离散，并结合时间积分方法，得到相应的数值算法。进一步，利用前述守恒律构造网格密度，建立物理场与节点位置联立演化的自适应动网格（SAMM）方法，使 x 方向的节点分布随解的演化而调整。在此基础上，以单孤子和二孤子精确解为参照，考察空间离散化方法、时间积分算法及固定网格与自适应动网格的选择对物理场数值误差的影响。

### 3.1 空间离散 {#zh-schemes}

本节对尚未离散的 x 导数作近似，得到可用于计算的演化系统。PE 与 PF 分别沿用各自的非线性变量，连续 DLW 方程的直接差分作为参照。三种实现采用相同的物理网格与边界数据。

**网格与差分算子。** 在固定网格上，取 $x_i=-L/2+i\Delta x$，其中 $\Delta x=L/N_x$。沿 y 方向，$M_j$ 位于 $y=jh$，而 $u_j,v_j,Q_j,R_j$ 位于 $y=(j+\tfrac12)h$。下标 j、i 分别表示 y 层与 x 节点。以下空间离散系统保留时间为连续变量。

对 x 导数采用三点中心差分

<a id="zh-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{69}$$

记 $k=\Delta x$，对光滑函数有

<a id="zh-eq-202"></a>

$$D_1f=f_x+\frac{k^2}{6}f_{xxx}+O(k^4),\qquad D_2f=f_{xx}+\frac{k^2}{12}f_{xxxx}+O(k^4).\tag{70}$$

$D_2$ 是独立的三点二阶导数模板，不等于 $D_1^2$。

沿 y 方向采用

<a id="zh-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{71}$$

其中，$D_1,D_2$ 作用于 x 节点编号，$\delta_-,\delta_0,\mathcal M_-$ 作用于层编号。下文的乘积与商均按节点计算。我们先构造 PE 和 PF 格式，再给出作为比较对象的直接差分格式，记为 FD。

**PE 格式。** 取 $P=\delta_-u$ 和 $W=v-\delta_0u$ 为演化变量。由下边界值及 P 的累积和确定 u，再令 $v=W+\delta_0u$，见[附录 D](#zh-app-d)。演化方程为 $\dot P=F_P$、$\dot W=F_W$，其中

<a id="zh-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{72}$$

因此，计算演化右端时，先由 P 恢复 u，再对 u、W 施加相应的空间差分算子；物理场 v 由同一重构公式得到。

**PF 格式。** 取 Q、R 为演化变量，物理场由

<a id="zh-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{73}$$

恢复。其中 $m_j\simeq M_{j,x}$ 由格点约束和下边界数据确定，详见附录 D。最终演化右端为

<a id="zh-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{74}$$

Q 的最下层取给定边界值，内部各层 Q 和所有层 R 按上述方程演化。随后通过式 (73) 恢复物理场。

**FD 格式。** 作为比较，直接离散连续 DLW 方程，取 $P=\delta_-u$ 和 v 为演化变量。物理场 u 由式 (113) 的第一个关系从 P 恢复。所得系统为 $\dot P=F_P$、$\dot v=F_v$，其中

<a id="zh-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{75}$$

**重构 u 变化率的 x 方向首项。** 设 b 为最下物理 y 层，$\Delta_bF=F(y)-F(b)$，$T_h$ 为从 b 到 y 的复合梯形和。在固定网格上记 $H=u^2/2+2au$、$W=v-\delta_0u$、$K(W)=W^2/32-W/4$。将 P 方程累加并使用给定的 $u_t(b)$，得到

<a id="zh-eq-203"></a>

$$\begin{aligned}F^u_{\rm PE}&=u_t(b)-D_1\Delta_b[H+h^2K(W)]-D_2[\Delta_bu+T_hW],\\F^u_{\rm FD}&=u_t(b)-D_1\Delta_bH-D_2T_hv.\end{aligned}\tag{76}$$

相对于保留同一 y 离散而对 x 精确求导的变化率，固定 h 时有 $r^u_{x,m}=k^2B_{h,m}+O(k^4)$，其中

<a id="zh-eq-204"></a>

$$\begin{aligned}B_{h,\rm PE}&=-\frac16\partial_{xxx}\Delta_b[H+h^2K(W)]-\frac1{12}\partial_{xxxx}[\Delta_bu+T_hW],\\B_{h,\rm FD}&=-\frac16\partial_{xxx}\Delta_bH-\frac1{12}\partial_{xxxx}T_hv.\end{aligned}\tag{77}$$

对光滑场，当 h 也趋于零时，二者均趋于

<a id="zh-eq-205"></a>

$$B=-\frac16\partial_{xxx}\Delta_bH(u)-\frac1{12}\partial_{xxxx}\int_b^y v(x,s,t)\,ds,\qquad r_x^u=k^2B+O(k^4+k^2h^2).\tag{78}$$

以上为匹配 x 延拓并保留给定下边界时的内部右端截断误差；周期回绕不匹配另有边界贡献。此处只计算固定网格上 PE 与 FD 的 u 变化率，PF、v 及移动节点需另行展开。

上述三种空间离散分别与第 3.3 节的时间积分方法结合，初值及边界数据在第 3.4 节给出。

### 3.2 自适应动网格方法 {#zh-samm}

均匀网格可能在变化缓慢的区域分配较多节点，却难以充分分辨狭窄波带。动网格方法通过依赖于解的密度重新分配节点，以改善这种不均衡 [14]。对于可积方程，守恒律提供了解与网格之间的直接联系，相关实例包括 Camassa–Holm 方程 [12]、短脉冲方程 [13] 及广义 sine-Gordon 方程 [9] 的自适应方法。在当前二维情形下，我们保留均匀的 $y$ 格点，并在各横向层共享同一组移动的 $x$ 节点。因此，我们对守恒密度与通量作横向平均，以确定共享的节点分布。这一做法在保持物理场张量积表示的同时，调整 $x$ 方向的分辨率。

半离散 DLW 系统的守恒律为自适应动网格方法（SAMM）提供了网格密度。利用这一密度，可将物理场与节点位置联立演化，使节点分布随解的变化而调整。我们保留 y 方向的均匀半离散格点，仅令 x 节点移动，各 y 层共用同一组 x 节点。为此，选取以下守恒密度与通量：

<a id="zh-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{79}$$

将 $W_j=4(1-\rho_j)$ 代入其演化方程，得到

<a id="zh-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{80}$$

在 PF 形式中，$\rho_j=Q_jR_j$。由于所有 $y$ 层共用一组 $x$ 节点，对各层取平均作为网格密度和通量：

<a id="zh-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{81}$$

初始节点按 $\bar\rho(x,0)$ 的累积积分等分，使相邻节点之间的密度积分相同，从而在密度较大的区域分配更多节点。演化过程中，每个节点对应的累积密度积分保持不变，节点运动由此与物理场的演化相联系。固定左端点 $x_L$，由守恒律[(80)](#zh-eq-97)得到

<a id="zh-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{82}$$

因此节点速度为

<a id="zh-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{83}$$

计算时以 $D_1\rho$ 代替通量中的 $\partial_x\rho$，并要求 $\bar\rho>0$。FD 的动网格比较也采用[(79)](#zh-eq-96)、[(81)](#zh-eq-98)和[(83)](#zh-eq-100)确定节点速度。

移动节点上采用[附录 E](#zh-app-e)的映射中心差分，将 $\dot z=F_z+\mathcal V D_1z$ 与 (83) 联立推进，并要求映射 Jacobian 保持正值。固定网格对应 $\mathcal V=0$。

### 3.3 时间积分 {#zh-time}

空间方法与网格比较统一采用经典四阶 Runge–Kutta（RK4）推进。为考察结果对时间积分的敏感程度，我们另在固定网格上对 PE 使用向前 Euler 和 Crank–Nicolson（C–N）方法。将全部演化变量记为 $z$，所得系统统一写为 $\dot z=\mathcal F(t,z)$。对于 SAMM，$z$ 还包含节点坐标，$\mathcal F$ 包含网格输运项及节点速度。

采用标准 Euler 与 RK4 方法 [10]；RK4 每一级均按该级的场、辅助变量、网格及边界数据计算。C–N 迭代及完整的时间积分器比较见[附录 F](#zh-app-f)。

### 3.4 算例与误差度量 {#zh-tests}

我们考虑连续 DLW 系统的单孤子与二孤子解。精确解用于给定初值和边界数据，并作为数值误差的评价基准。各算例统一取 $a=2$、行列式系数 $\rho_i=1$，初相位为零。

**单孤子解。** 当 $N=1$ 时，连续 Gram 行列式化为

<a id="zh-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{84}$$

其中

<a id="zh-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{85}$$

相应的物理场为

<a id="zh-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{86}$$

当 $p+q>0$、$c>0$ 时，u 脉冲的正负由 $c-1$ 决定，而 v 脉冲的正负由 $\ell$ 决定。我们选取 $(p,q)=(1,2)$ 和 $(4,-3)$，分别得到负的和正的 u 脉冲。第一组参数对应 $c=1/4$、$\ell=-3/4$；第二组对应 $c=2$、$\ell=-1/2$。两组参数的 v 场均为负脉冲。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_1_2.png" alt="单孤子精确解：(p,q)=(1,2)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−5,5]、y ∈ [−5,5]。" loading="lazy"><figcaption>单孤子精确解：(p,q)=(1,2)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−5,5]、y ∈ [−5,5]。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_4_m3.png" alt="单孤子精确解：(p,q)=(4,−3)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−10,10], y ∈ [−10,10]。" loading="lazy"><figcaption>单孤子精确解：(p,q)=(4,−3)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−10,10], y ∈ [−10,10]。</figcaption></figure>

**二孤子解。** 当 $N=2$ 时，展开 Gram 行列式可得

<a id="zh-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{87}$$

其中

<a id="zh-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{88}$$

物理场由 $u_*=2\partial_x\log(f_*/g_*)$ 和 $v_*=2\partial_x\partial_y\log(f_*g_*)$ 得到。对于二孤子解，取 $p_1=6$、$q_1=-5$、$p_2=4$、$q_2=-3$，相应地有 $c_1=4/3$、$c_2=2$、$A_{12}=4/3$。此时两相位分别为 $\theta_1=x-11t-y/12$ 和 $\theta_2=x-7t-y/2$，对应两个空间取向及传播速率不同的波，从而可用于考察双波相互作用情形下的数值表现。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton.png" alt="二孤子精确解：(p₁,q₁)=(6,−5)、(p₂,q₂)=(4,−3)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−30,30], y ∈ [−30,30]。" loading="lazy"><figcaption>二孤子精确解：(p₁,q₁)=(6,−5)、(p₂,q₂)=(4,−3)，t=0。左图为 u，右图为 v；展示范围为 x ∈ [−30,30], y ∈ [−30,30]。</figcaption></figure>

第二组二孤子取 $(p_1,q_1)=(1,2)$、$(p_2,q_2)=(4,-3)$，此时 $c_1=1/4$、$c_2=2$、$A_{12}=5/4$，相位为 $\theta_1=3x+3t-3y/4$ 和 $\theta_2=x-7t-y/2$，其 $u$ 场包含正、负两条波带。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton_mixed.png" alt="二孤子精确解: (1,2; 4,-3), t=0; u / v; [-30,30]²." loading="lazy"><figcaption>二孤子精确解: (1,2; 4,-3), t=0; u / v; [-30,30]².</figcaption></figure>

**初值与边界数据。** PE、PF 和 FD 采用相同的初始物理场。PE 的初值取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$；FD 采用相同的 $P^0$，并取 $v^0=v_*(0)$。PF 采用同一连续物理初边值，并在最左 x 节点归一化 Q；重构及下边界初始化见附录 D。

**计算设置与误差度量。**

下面给出数值实验所考察的区域及离散参数。为包含孤子的主要波形结构，四组算例所考察的区域依次取为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$ 和 $[-30,30]^2$。

相应计算域依次为 $[-10,10]^2$、$[-20,20]^2$、$[-40,40]^2$ 和 $[-40,40]^2$。PE 与 FD 在 x 方向周期延拓，PF 对 Q、R 采用给定的加性跳跃；y 下边界数据和 u 的幽灵层值由连续精确解给定。各方法使用相同的计算域和评价区域。

实验中分别设置固定网格与自适应动网格（SAMM）。固定网格取 $\Delta x=h=0.1$；对于 SAMM，y 方向采用间距 $h=0.1$ 的均匀格点，x 节点则依据前述守恒密度的 y 平均值重新分配。

每组算例均推进 100 个时间步。具体地，从 $t=0$ 出发，取时间步长 $\Delta t=10^{-4}$，计算至终止时刻 $T=0.01$。

误差评价时，沿 x 方向对节点上的数值物理场作三次样条插值，得到该方向上的连续表示，以便在相同空间位置与精确解比较。我们考察所选区域内评价点集 $\mathcal G$ 上的最大绝对误差，用以衡量终止时刻数值解对精确解的最大偏离：

<a id="zh-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{89}$$

为解释 PE 与 PF 的误差，记连续精确场为 $Z=(u,v)$，同谱参数的半离散精确场为 $Z_h=(U_h,V_h)$，并与 $Z_{\rm num}$ 在相同位置取值。于是

<a id="zh-eq-206"></a>

$$e_{\rm model}=Z_h-Z,\qquad e_{\rm num}=Z_{\rm num}-Z_h,\qquad e_{\rm total}=e_{\rm model}+e_{\rm num}.\tag{90}$$

其中 $e_{\rm num}$ 为相对于半离散精确解的数值偏差，包含空间与时间离散、重构以及初值和边界不匹配的影响。本文采用连续场初始化，因此在物理初值精确恢复的点上，$e_{\rm num}(0)=-h^2C(0)+O(h^4)$，$C=(C_U,C_V)$；初始化中的重构残差需另计。连续下边界与该半离散精确族的边界也存在差异。对同一个离散 L² 或 RMS 内积，不减去均值，有

<a id="zh-eq-207"></a>

$$\rho=\frac{\langle e_{\rm model},e_{\rm num}\rangle}{\|e_{\rm model}\|\,\|e_{\rm num}\|},\qquad \|e_{\rm total}\|^2=\|e_{\rm model}\|^2+\|e_{\rm num}\|^2+2\rho\|e_{\rm model}\|\,\|e_{\rm num}\|.\tag{91}$$

两范数均非零时方向余弦 ρ 有定义，它不是 Pearson 相关系数。负交叉项说明该内积范数中的抵消。下文保留的最大误差均为总误差，不适用上述平方范数恒等式。右端截断系数描述瞬时误差源，其对终态误差的影响还取决于传播及初边值数据。

### 3.5 数值结果 {#zh-results}

本小节展示数值实验的结果。首先，在固定网格上使用 PE、PF 和 FD，并基于 RK4 算法推进时间演化，比较三种方法的误差。随后固定采用 PE 离散化，分别比较 Euler、RK4、C–N 三种时间算法，以及固定网格与 SAMM 的计算误差。表中，$e_u=E_u(T)$、$e_v=E_v(T)$ 表示两个物理场的最大绝对误差。

#### 3.5.1 空间离散的比较 {#zh-spatial-results}

我们比较不同空间离散化方法的数值误差。每组实验的初值由精确解给定，分别使用 PE、PF 和 FD，在固定网格上基于 RK4 演化至 $T=0.01$，并将所得物理场 U、V 与精确解比较，计算最大绝对误差，结果列于表 1。

**表 1　PE、PF 和 FD 在 T=0.01 时的最大绝对误差（e<sub>u</sub> / e<sub>v</sub>）。固定网格，RK4，Δx=h=0.1，Δt=10⁻⁴。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>PE: e<sub>u</sub> / e<sub>v</sub></th><th>PF: e<sub>u</sub> / e<sub>v</sub></th><th>FD: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td>3.061201e-03 / 3.067031e-03</td><td><strong>4.715088e-04</strong> / <strong>1.201923e-03</strong></td></tr><tr><th>单孤子 (4, −3)</th><td><strong>1.419616e-05</strong> / 2.745967e-05</td><td>8.067776e-05 / 4.377502e-04</td><td>1.718043e-05 / <strong>2.605300e-05</strong></td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td><strong>3.552455e-05</strong> / 5.359645e-05</td><td>7.501357e-05 / 5.394947e-05</td><td>3.989986e-05 / <strong>5.173628e-05</strong></td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td>4.102555e-03 / 3.252786e-03</td><td><strong>4.782980e-04</strong> / <strong>1.350627e-03</strong></td></tr></tbody></table></div>

在表 1 的四组算例中，PE 在两个算例的 U 场上取得最小的最大绝对误差，而 FD 在最多的比较项中取得最小误差。在这四组算例中，PF 的误差均大于 PE 和 FD。

图 1—4 给出固定网格上采用 RK4 推进至 T=0.01 时的绝对误差曲面。不同列对应不同的空间离散方法，从左到右依次为 PE、PF、FD；第一行为 U 的绝对误差，第二行为 V 的绝对误差。同一物理场在三种方法间采用共同色阶和高度范围。

**单孤子 (1, 2)**

第一组单孤子的两个场均为斜向负脉冲。图 1 展示三种空间离散在波带附近的绝对误差。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png" alt="One-soliton (p=1, q=2): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>图 1　单孤子 (p=1, q=2)的绝对误差曲面。</figcaption></figure>

**单孤子 (4, −3)**

第二组单孤子的 U 为正脉冲、V 为负脉冲。图 2 中 PF 的 V 误差高于另外两种方法。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png" alt="One-soliton (p=4, q=−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>图 2　单孤子 (p=4, q=−3)的绝对误差曲面。</figcaption></figure>

**二孤子 (6, −5; 4, −3)**

第一组二孤子包含两条不同取向的波带。图 3 覆盖相互作用区和分离分支，用于比较三种方法在不同区域的误差分布。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png" alt="Two-soliton (6,−5; 4,−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>图 3　二孤子 (6,−5; 4,−3)的绝对误差曲面。</figcaption></figure>

**二孤子 (1, 2; 4, −3)**

第二组二孤子组合了一正一负的 U 波带。图 4 展示该结构的绝对误差。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png"><img src="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png" alt="Two-soliton (1,2; 4,−3): PE/PF/FD absolute-error surfaces" loading="lazy"></a><figcaption>图 4　二孤子 (1,2; 4,−3)的绝对误差曲面。</figcaption></figure>

在接下来的时间推进与网格配置比较中，我们统一采用 PE，以保持空间离散化方法不变，分别考察时间算法和网格配置对误差的影响。

#### 3.5.2 PE 的时间推进比较 {#zh-time-results}

附录 F 的固定网格 PE 对照表明，在所用步长下，C–N 与 RK4 的误差剖面几乎重合。部分算例中 Euler 的 u 最大误差较小；这一排序针对包含空间及初始数据影响的总误差。网格比较统一采用 RK4。

#### 3.5.3 自适应动网格方法的数值表现 {#zh-mesh-results}

我们将[第 3.2 节](#zh-samm)构造的 SAMM 用于上述四组单孤子与二孤子算例，并与固定网格计算比较精度。两者均采用 PE 离散化和 RK4 时间算法，保持相同节点数，y 间距为 $h=0.1$。SAMM 的 x 节点由守恒密度确定，并与物理场共同演化至 $T=0.01$。表 2 列出固定网格与动网格计算所得的最大绝对误差。

**表 2　PE 在 T=0.01 时固定网格与动网格上的最大绝对误差（e<sub>u</sub> / e<sub>v</sub>），RK4。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>固定网格: e<sub>u</sub> / e<sub>v</sub></th><th>动网格: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td><strong>5.781845e-04</strong> / <strong>1.091714e-03</strong></td></tr><tr><th>单孤子 (4, −3)</th><td>1.419616e-05 / 2.745967e-05</td><td><strong>1.334447e-05</strong> / <strong>2.621326e-05</strong></td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td>3.552455e-05 / 5.359645e-05</td><td><strong>3.304157e-05</strong> / <strong>5.060189e-05</strong></td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td><strong>6.156957e-04</strong> / <strong>1.428010e-03</strong></td></tr></tbody></table></div>

图 5 给出四组算例的误差剖面 $\max_j|U_{\rm num}-U_*|$ 和 $\max_j|V_{\rm num}-V_*|$，用于比较两种网格方法的误差分布。橙红虚线与空心圆表示固定网格，蓝色实线表示 SAMM。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="PE_mesh_profiles" loading="lazy"></a><figcaption>图 5　PE 在 T=0.01 时固定网格与动网格的绝对误差剖面。</figcaption></figure>

四组算例中，SAMM 的 U、V 最大绝对误差均小于固定网格方法。这表明自适应网格能够改善 PE 对所考察单孤子和二孤子解的计算精度，改善幅度随孤子参数和物理场而变化。

## 4. 结论 {#zh-conclusion}

本文围绕（2+1）维 DLW 方程的可积半离散化，研究了半离散系统的构造、精确解及其数值计算。我们从连续双线性方程出发，沿 y 方向引入离散格点，得到保留 x 与 t 连续性的半离散双线性系统，并据此建立非线性表示和数值算法。

通过交错格点与算子参数的配合，我们构造了任意有限阶 Gram 行列式解，并利用行列式恒等式证明相应的 τ 函数满足所提出的半离散双线性方程。在非线性化过程中，消去或保留辅助势分别得到 PE 与 PF 两种表示。对于相应的正 τ 函数解，两种表示恢复相同的物理场。我们还给出了它们的 Darboux–Lax 表示，并证明其相容条件产生相应的非线性方程。

我们进一步考察了半离散系统与连续 DLW 方程之间的关系，证明当格距趋于零时，半离散方程以二阶精度恢复连续方程。对于所构造的精确解，在给定的正则参数范围内，重构的物理场也以二阶精度收敛到相应的连续精确解，从而明确了方程及其解在连续极限下的对应关系。

我们基于 PE 与 PF 两种非线性表示构造了数值算法，并以单孤子和二孤子精确解为基准，与连续 DLW 方程的直接差分方法进行比较。通过空间离散化、时间积分和网格配置的对照实验，我们考察了这些选择对两个物理场数值误差的影响。

我们建立了半离散 DLW 方程的一条守恒律，并据此选取网格密度，构造物理场与节点位置联立演化的自适应动网格方法。该方法保持 y 方向的均匀格点，通过密度的演化调整 x 方向的节点位置。在相同节点数和时间积分方法下，自适应动网格降低了全部四组孤子算例中两个物理场的最大绝对误差，使既定数量的节点获得了更高的计算精度。



## 附录 A. 精确解族差的首项 {#zh-app-a}

记 $z_i=p_i-a$、$w_i=q_i+a$。主子式展开中，选取的行、列对应同一指标集 I。格点相位贡献 $h^2y\sum_{i\in I}c_i$，(55) 的居中 f 振幅贡献 $h^2\sum_{i\in I}d_i$，其中

<a id="zh-eq-208"></a>

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,\qquad \alpha_2=\sum_i(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_i c_i\rho_i\partial_{\rho_i}\beta.\tag{92}$$

算子 $\rho_i\partial_{\rho_i}$ 恰好选出含 i 的主子式，故先展开行列式再取对数，即对任意固定 N 得到 (92)。在物理中点作对称重构，得到

<a id="zh-eq-209"></a>

$$\begin{aligned}U_h&=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4),\\V_h&=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).\end{aligned}\tag{93}$$

代入 $4\beta_{xy}=v-u_y$ 即得 (60)。固定正则谱参数、K 邻域上 τ 函数不为零以及充分小的 h，保证所需导数及余项的一致界。定理 2.9 的正谱域提供这些条件；其他正则实分支在具有同样界的区域内也适用。此处未断言一般初值问题的稳定性估计。

## 附录 B. 相邻层行列式恒等式 {#zh-app-b}

**证明。** 将第 n 层 Gram 矩阵写成 $M=I+(r_ic_k/(p_i+q_k))$，其中

<a id="zh-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{94}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义可得

<a id="zh-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{95}$$

其中的辅助层移位关系来自恒等式

<a id="zh-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{96}$$

在 M 可逆处，记

<a id="zh-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{97}$$

最后一个等式由矩阵行列式引理得到，而 Jacobi 微分公式给出 $\kappa=\tau_{n,x}/\tau_n$。为收集求导产生的项，记

<a id="zh-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{98}$$

利用 $H_x=-HM_xH$、$H_t=-HM_tH$，逐项求导得到

<a id="zh-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{99}$$

例如 $z_x=HPr-\kappa z$，故 $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$。对其再求一次导数，并消去 $\eta_1,\eta_2$，得到

<a id="zh-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{100}$$

因此 $\psi=1-\zeta$ 满足

<a id="zh-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{101}$$

对于 $f=\psi g$，展开双线性算子可得

<a id="zh-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{102}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，即在 M 可逆处得到 [(13)](#zh-eq-13)。为将结论延伸至奇异矩阵，将所有 $\rho_i$ 替换为 $\varepsilon\rho_i$。在固定 x、t 处，$\varepsilon=0$ 时 M 为单位矩阵，双线性残差在 ε 的零点邻域内为零。该残差是 ε 的多项式，故恒等于零。令 $\varepsilon=1$ 即完成证明。□

## 附录 C. Darboux 算子计算 {#zh-app-c}

**证明。** 令

<a id="zh-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{103}$$

<a id="zh-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{104}$$

其中 $\mathscr B_j^{-1}$ 在形式伪微分算子代数中定义。线性系统写为 $\psi_{j+1}=T_j\psi_j$、$\psi_{j,t}=H_j\psi_j$。对格点关系关于 t 求导，并代入相邻两层的时间方程，得到

<a id="zh-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{105}$$

为验证该恒等式，定义标量残差

<a id="zh-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{106}$$

利用 $V_{j+1}-V_j=(h/2)w_{j,x}$，可得

<a id="zh-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{107}$$

由 w 的演化方程，两项残差之差为零；由 $V_{j,x}$ 的定义，两项残差之和也为零。因此 $\mathcal E_j^r=\mathcal E_j^s=0$。对于标量函数 r，乘积法则给出 Darboux 恒等式

<a id="zh-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{108}$$

由辅助势差关系，有

<a id="zh-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{109}$$

记

<a id="zh-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{110}$$

分别将 Darboux 恒等式用于两个为零的残差，得到

<a id="zh-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{111}$$

消去共同的中间算子，得到 $L_{j+1}T_j=T_jL_j$，即相容条件 [(105)](#zh-eq-75)。

反之，设相容条件与辅助势差关系成立。同样的算子计算给出

<a id="zh-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{112}$$

比较 $\partial_x^0$ 和 $\partial_x^{-1}$ 的系数，得到 $\mathcal E_j^r=\mathcal E_j^s$、$w_j\mathcal E_j^s=0$。因此在 $w_j\ne0$ 的区域内，两项残差均为零。两者之差给出 w 方程；两者之和经后向差分，并结合辅助势差关系，给出第一条非线性方程。□

## 附录 D. 重构与边界初始化 {#zh-app-d}

对于 PF，由 $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ 及归一化 $Q_{j,0}^0=1$ 确定 Q，再取 $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$。下边界的 $Q_0(t)$ 按同一关系由 $u_{*,0}(t)$ 确定。

在每个时刻，通过

<a id="zh-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{113}$$

恢复物理场。其中，$j_L$ 为最下层编号，$u_{j_L,i}(t)$ 由下边界数据给定。



恢复。演化方程还包含 $(M_j+M_{j+1})_x$。为计算这一项，引入 $m_j\simeq M_{j,x}$ 和 $S_j=Q_jR_j$。对格点约束 $M_{j+1}-M_j=h(1-S_j)$ 施加 $D_1$，得到

<a id="zh-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{114}$$

给定下边界的 m 后，即可利用这一关系逐层求出其余各层。将最下层临时编号为 0，由该层的 Q 方程确定起始值：

<a id="zh-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{115}$$

其中，$Q_0(t)$ 由下边界数据给定，$Q_{0,t}$ 为其时间导数。

## 附录 E. 移动节点上的导数 {#zh-app-e}

物理节点移动后，相邻 $x$ 间距不再相等。为在同一节点编号上计算导数，引入固定均匀的计算坐标 $\xi_i=-L/2+i\Delta\xi$，其中 $\Delta\xi=L/N_x$。写 $x_i(t)=\xi_i+s_i(t)$，$s_i$ 是节点位移，$J_i=1+D_\xi s_i$ 近似坐标映射的伸缩率 $J=x_\xi$。

对于定义在移动节点上的场，链式法则给出 $\partial_x=J^{-1}\partial_\xi$。再作用一次该算子，就会对 $J^{-1}$ 求导，因而

<a id="zh-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{116}$$

分别以均匀 $\xi$ 网格上的中心差分近似这些导数，得到

<a id="zh-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{117}$$

$D_\xi,D_{\xi\xi}$ 为[(69)](#zh-eq-87)在均匀计算坐标上的三点差分。在移动节点上，场变量满足 $\dot z=F_z+\mathcal V D_1z$。它与节点方程[(83)](#zh-eq-100)共同构成物理场和网格的联立演化系统，再采用第 3.3 节的时间算法推进。固定网格计算对应 $s=0,\mathcal V=0$。

## 附录 F. 隐式时间推进及对照 {#zh-app-f}

Crank–Nicolson（C–N）方法取相邻两个时间层变化率的平均：

<a id="zh-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{118}$$

FD 方法中的 $v$ 方程写为 $v^{n+1}=v^n+\Delta t(F_v^n+F_v^{n+1})/2$。由于 $F_v^{n+1}$ 依赖未知的下一层解，需与 $P$ 的更新联立求解。以向前 Euler 格式给出的近似作为初值，迭代求解耦合的隐式方程。



对上述四组孤子算例，固定采用 PE 空间离散，在固定网格上比较 Euler、RK4 与 C–N。各算例均取 $\Delta x=h=0.1$、$\Delta t=10^{-4}$、$T=0.01$，最大绝对误差列于表 F1。

**表 F1　PE 的时间算法比较：最大绝对误差（e<sub>u</sub> / e<sub>v</sub>）。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>Euler: e<sub>u</sub> / e<sub>v</sub></th><th>RK4: e<sub>u</sub> / e<sub>v</sub></th><th>C–N: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td><strong>6.396711e-04</strong> / 1.340634e-03</td><td>6.406395e-04 / <strong>1.339511e-03</strong></td><td>6.406384e-04 / 1.339513e-03</td></tr><tr><th>单孤子 (4, −3)</th><td>1.422394e-05 / 3.005484e-05</td><td><strong>1.419616e-05</strong> / <strong>2.745967e-05</strong></td><td>1.419664e-05 / 2.746028e-05</td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td>3.840649e-05 / 5.901085e-05</td><td><strong>3.552455e-05</strong> / <strong>5.359645e-05</strong></td><td>3.552653e-05 / 5.359819e-05</td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td><strong>6.188417e-04</strong> / 1.515498e-03</td><td>6.329588e-04 / <strong>1.511271e-03</strong></td><td>6.330018e-04 / 1.511273e-03</td></tr></tbody></table></div>

对每种时间算法 m，我们考察数值解与精确解之差沿 y 方向索引 j 的最大绝对值，即 $\max_j|U_m(x,y_j,T)-U_*(x,y_j,T)|$ 和 $\max_j|V_m(x,y_j,T)-V_*(x,y_j,T)|$。图 F1 给出相应误差剖面及 RK4 误差峰值附近的局部放大图。

<figure><a href="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="PE_time_profiles" loading="lazy"></a><figcaption>图 F1　PE 在 T=0.01 时的绝对误差剖面及局部放大图。</figcaption></figure>

四组算例中，C–N 与 RK4 的误差剖面均几乎重合。在部分算例的 U 场上，Euler 取得较小的最大绝对误差，其余比较中则以 RK4 的误差较小。后续网格实验统一采用 RK4 进行时间演化，考察节点重分布的影响。

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

[10] E. Hairer, S. P. Nørsett, G. Wanner. *Solving Ordinary Differential Equations I: Nonstiff Problems*. 2nd revised ed., Springer, 1993. [Publisher](https://link.springer.com/book/10.1007/978-3-540-78862-1).

[11] S.-F. Tian, T.-T. Zhang, P.-L. Ma, X.-Y. Zhang. Lie symmetries and nonlocally related systems of the continuous and discrete dispersive long waves system by geometric approach. *Journal of Nonlinear Mathematical Physics* **22** (2015), 180–193. [DOI](https://doi.org/10.1080/14029251.2015.1023562).

[12] B.-F. Feng, K. Maruno, Y. Ohta. A self-adaptive moving mesh method for the Camassa–Holm equation. *Journal of Computational and Applied Mathematics* **235** (2010), 229–243. [DOI](https://doi.org/10.1016/j.cam.2010.05.044). [Preprint](https://arxiv.org/abs/0905.2693).

[13] B.-F. Feng, K. Maruno, Y. Ohta. Self-adaptive moving mesh schemes for short pulse type equations and their Lax pairs. *Pacific Journal of Mathematics for Industry* **6** (2014), 8. [DOI](https://doi.org/10.1186/s40736-014-0008-7). [Preprint](https://arxiv.org/abs/1403.6191).

[14] W. Huang, R. D. Russell. *Adaptive Moving Mesh Methods*. Applied Mathematical Sciences, vol. 174, Springer, 2011. [DOI](https://doi.org/10.1007/978-1-4419-7916-2).

[15] R. Hirota. *The Direct Method in Soliton Theory*. Cambridge Tracts in Mathematics, vol. 155, Cambridge University Press, 2004. [DOI](https://doi.org/10.1017/CBO9780511543043).
