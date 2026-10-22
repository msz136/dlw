<nav>[English](#en-title) · [中文](#zh-title)</nav>

# Integrable semi-discretizations of the (2+1)-dimensional dispersive long wave system {#en-title}

**Abstract.** Recent advancements in the study of the $(2+1)$-dimensional dispersive long wave (DLW) system have led to explicit solution families and a deeper understanding of their underlying integrable structure. Extending these developments to discrete settings requires formulations that preserve this structure and allow the resulting changes in the wave fields to be understood. In this work, we introduce an integrable semi-discrete DLW system, with a discrete $y$ coordinate and continuous $x$ and $t$. The construction couples staggered lattice shifts with shifts of the bilinear parameter to obtain a semi-discrete bilinear system, allowing the continuous Gram determinant solutions to be extended to the lattice setting. This system yields two nonlinear formulations through the elimination or retention of an auxiliary potential, with a corresponding Darboux–Lax representation for each. We establish second-order consistency of the semi-discrete equations with the continuous DLW system. Under suitable regularity and positivity assumptions, we also prove that the exact semi-discrete physical fields converge to their continuous counterparts at second order and derive explicit leading coefficients for this field approximation error.

The exact solutions also provide benchmarks for examining how the semi-discrete formulations perform in numerical computation. We first show how the choice of nonlinear formulation affects accuracy under a common centered discretization in $x$. The spatial error analysis helps explain the differences observed between the two formulations and direct finite differences. Comparisons of time integrators further assess the influence of temporal discretization. Beyond these comparisons, we use a conservation law of the semi-discrete system to develop a self-adaptive moving mesh method, coupling the motion of shared $x$ nodes to the evolution of the physical fields. With the same node count and time integrator, this method reduces the maximum errors in both physical fields across all four one- and two-soliton tests. Overall, our work connects the integrable construction of the semi-discrete DLW system with an understanding of how its formulation and numerical implementation shape computational accuracy. By developing the semi-discrete model alongside its error analysis and adaptive numerical method, we show how the construction of discrete integrable systems can contribute to understanding and improving numerical approximations of nonlinear waves.

**Keywords:** dispersive long wave equation; semi-discretization; Gram determinant; Darboux–Lax representation; continuum limit; self-adaptive moving mesh

## 1. Introduction {#en-intro}

The propagation and interaction of waves in shallow water have long attracted interest in the study of nonlinear wave phenomena. As waves evolve, nonlinear effects and dispersion can influence their profiles in different ways, and their balance can support coherent waves that persist during propagation. Nonlinear long-wave equations describe these effects in a reduced form, allowing wave motion to be studied without retaining the full complexity of the underlying fluid equations. Within this class, integrable models have received sustained attention for the analytical insight they offer. Their exact solutions make it possible to follow the evolution of individual waves and examine their interactions, while bilinear formulations and Lax representations reveal mathematical structures underlying these solutions. These analytical results also provide useful reference points for numerical studies, in which wave profiles and their evolution are represented on a discrete mesh. Passing from a continuous model to such a representation introduces choices that affect both the approximation of the waves and the mathematical structure of the resulting equations. Integrable discretization seeks to retain this connection, bringing the construction of discrete equations together with the study of their exact solutions and continuum limits.

The (2+1)-dimensional dispersive long wave (DLW) system extends the dispersive long wave equation to two spatial dimensions [1] and has been studied in connection with wave motion in wide channels and open seas of finite depth [3,4]. Since its introduction by Boiti, Leon and Pempinelli, its wave solutions have been studied through several closely related analytical approaches. The inverse spectral transform, Bäcklund transformation and superposition formula established in the original work [1] were followed by nonlinear transformations [2] and bilinear methods [3], which offered further ways to generate solutions and understand their relations. Determinant representations give these relations a concrete form. Hu, Xu and Yu developed Grammian and Wronskian solutions [4], and Sheng and Yu used a KP-hierarchy reduction to obtain Gram determinant solutions describing solitons, line breathers and rational waves on constant and periodic backgrounds [5].

The bilinear relations underlying these solutions also offer a starting point for introducing a lattice [15]. In this approach, Bäcklund transformations relate neighbouring lattice values, allowing discrete equations to be constructed together with their solution structures. This idea has been developed for semi-discrete soliton equations [7] and extended to systems with two spatial dimensions [8]. For the DLW system, a further connection comes from its bilinear relation to the (2+1)-dimensional sinh-Gordon equation [5], whose integrable discretizations admit determinant solutions and Bäcklund–Lax structures [6]. Together with earlier studies of discrete DLW systems [11], these developments motivate a closer examination of how the continuous DLW solution family can be carried onto a spatial lattice, and how the resulting wave fields compare with their continuous counterparts.

With these advancements, there is potential to study the preservation of integrable structure and the approximation of continuous waves within the same construction. With this in mind, we ask how to introduce a spatial lattice that preserves the bilinear and determinant structure, supports a consistent reconstruction of the physical fields, and admits a quantitative comparison between its exact solutions and those of the continuous system.

To address this question, we seek a semi-discrete description of the DLW system. First, the construction should retain the connection between explicit wave solutions and the integrable structure governing their evolution. Gram determinant solutions make the discrete wave fields accessible to analytical study, while a corresponding Lax representation should recover the same nonlinear equations through its compatibility conditions. Second, we wish to understand how the lattice changes the continuous wave fields. This requires a quantitative comparison of the corresponding exact solutions, complementing the recovery of the continuous equations in the limit. The comparison of exact wave fields also provides a basis for studying numerical approximations. Once the semi-discrete system is used in computation, the choice of nonlinear formulation, time integrator and mesh can affect how accurately these waves are resolved. We therefore seek to understand these effects through comparisons with the exact solutions.

In Section 2, we construct the semi-discrete DLW system from the continuous bilinear formulation and Gram determinant solutions of Sheng and Yu [5]. A staggered lattice in $y$, coupled to shifts of the bilinear parameter, allows the determinant solutions to be carried into the semi-discrete setting. This construction leads to the PE and PF formulations and their Darboux–Lax representations. We then examine how the equations and exact physical fields approach their continuous counterparts, establishing second-order consistency and convergence under the stated assumptions and deriving explicit leading error coefficients for the fields. Building on these analytical results, Section 3 develops the spatial discretizations, a conservation-based self-adaptive moving mesh method and the time integration schemes. Using four one- and two-soliton tests, we compare the nonlinear formulations with direct finite differences and assess the effects of time integration and mesh adaptation. The spatial error analysis helps explain the accuracy differences among the spatial discretizations. For the adaptive mesh, comparisons at a fixed node count assess how redistributing the nodes affects the accuracy of the computed wave fields. Finally, Section 4 brings together the main findings and discusses the connections between the analytical and numerical results.

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

At the location of $F_j$, the neighbouring functions $G_j$ and $G_{j+1}$ lie symmetrically on either side. We therefore use the average of their logarithms to define $u_j$, and introduce $\omega_j$ to describe the change in the logarithmic $x$-derivative between these neighbouring sites. For positive τ functions, we set

<a id="en-eq-27"></a>

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad \omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad v_j=\frac4h\omega_j+\delta_0u_j,\qquad \delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h}.\tag{18}$$

We associate the reconstructed fields $u_j$ and $v_j$ with $y=(j+\tfrac12)h$. The definition of $v_j$ follows the continuous identity

$$v=4(\log g)_{xy}+u_y,$$

which is obtained directly from (2). In (18), $4\omega_j/h$ approximates $4(\log g)_{xy}$, while $\delta_0u_j$ approximates $u_y$. These relations give a discrete counterpart of the continuous field transformation; we establish their second-order consistency in Section 2.5. For the derivation below, we work with $u_j$ and $\omega_j$, recovering $v_j$ through (18).

To derive the field equations, we introduce the logarithmic variables $\alpha_j=\log F_j$ and $\beta_j=\log G_j$. These variables allow us to expand the bilinear equations in terms of the derivatives that enter the reconstruction formulas. Dividing the two equations in (9) by $F_jG_j$ and $F_jG_{j+1}$, respectively, we obtain

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

Their symmetric form suggests taking the sum and difference of the equations in (19). After differentiation in $x$, the sum produces $u_{j,t}$, while the difference produces $\omega_{j,t}$. We can express the quadratic and first-derivative terms through (20). The second-derivative terms in the sum, however, retain an additional combination of the logarithmic variables. We collect this contribution by defining

<a id="en-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{21}$$

Taking the $x$-derivatives of $A_j+C_j=0$ and $A_j-C_j=0$, and substituting (20)–(21), we arrive at

<a id="en-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{22}$$

The second equation is already expressed in $u_j$ and $\omega_j$, whereas the first still involves $Z_j$. To complete the nonlinear description, we use the reconstruction relations to handle this remaining term in two ways. We first eliminate $Z_j$ by taking a lattice difference. We then develop an alternative formulation that retains a potential through which $Z_j$ and $\omega_j$ can both be expressed.

For the first formulation, we seek equations involving only $u_j$ and $\omega_j$. Although $Z_j$ contains logarithmic derivatives that do not appear separately in these two variables, its difference between adjacent lattice sites can be expressed directly through them. We therefore introduce the backward difference and averaging operators

<a id="en-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{23}$$

From the definitions of $u_j$ and $Z_j$, we have $Z_j-u_j=2(\beta_j+\beta_{j+1})_x$. Taking a backward difference and using $\omega_j=(\beta_{j+1}-\beta_j)_x$, we obtain

<a id="en-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{24}$$

This identity allows us to remove $Z_j$ after applying $\delta_-$ to the first equation in (22). Keeping the second equation unchanged, we arrive at the potential-elimination formulation (PE):

<a id="en-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{25}$$

We have thus removed the auxiliary quantity $Z_j$ through an exact lattice identity, without introducing a further approximation. The resulting equations involve $u_j$ and $\omega_j$, from which we recover the physical field $v_j$ using (18). The elimination places a backward difference on $u_{j,t}$, so recovering the individual time derivatives requires a boundary value or an equivalent normalization in the lattice direction. This feature will enter the numerical implementation of PE.

We next develop a formulation that retains the potential information carried by the τ functions. In this representation, we seek to express both $Z_j$ and $\omega_j$ through a common variable, so that we can use the first equation in (22) without taking a lattice difference. For this purpose, we introduce $M_j=\beta_{j,x}$. The reconstruction relations then give

<a id="en-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{26}$$

Thus, the difference of neighbouring potential values determines $\omega_j$, while their sum supplies the additional term in $Z_j$.

After substituting (26) into the first equation in (22), we encounter the combination $u_{j,x}+u_j^2/2$ inside an $x$-derivative. This suggests introducing a variable whose logarithmic derivative gives $u_j$. Guided by the τ-function reconstruction, we define

<a id="en-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{27}$$

With this choice, the derivative and quadratic terms combine as

<a id="en-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{28}$$

To obtain the evolution equation for $Q_j$, we return to the relation $(A_j+C_j)/2=0$, before differentiation in $x$. This allows us to retain the normalization inherited from the τ functions without introducing an integration function. Substituting (26)–(27), we obtain

<a id="en-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{29}$$

We have now expressed the first evolution relation through $Q_j$, the neighbouring potential values, and their difference $\omega_j$. To complete the formulation, we turn to the equation for $\omega_j$. Substituting $u_j=2Q_{j,x}/Q_j$ into its flux gives

<a id="en-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{30}$$

The last term couples the logarithmic derivative of $Q_j$ to $\omega_j-h$. We absorb this combination into a companion variable by setting

<a id="en-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{31}$$

Since the positive τ functions give $Q_j>0$, this definition is well defined on the region under consideration. It also simplifies the quadratic term in (29), through the identities

<a id="en-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{32}$$

Using (31)–(32), we rewrite the $\omega_j$ equation as an evolution equation for the product $Q_jR_j$:

<a id="en-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{33}$$

The second-derivative terms satisfy

<a id="en-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{34}$$

We can therefore expand the time derivative in (33) and use (29) to eliminate $Q_{j,t}$. Dividing by $Q_j$ then gives the evolution equation for $R_j$. Meanwhile, the two expressions for $\omega_j$ in (26) and (31) impose a lattice constraint linking $M_j$ to $Q_jR_j$.

Collecting these relations, we obtain the potential formulation (PF):

<a id="en-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{35}$$

Here $Q_j$ and $R_j$ occupy the half-grid locations $y=(j+\tfrac12)h$, while $M_j$ lies at $y=jh$. The first two equations describe the evolution of $Q_j$ and $R_j$; the third relates their product to the difference of neighbouring potential values. We recover the physical fields through

<a id="en-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{36}$$

We have obtained two nonlinear formulations by treating the auxiliary potential in different ways. To make their relation precise, we compare the physical fields reconstructed from the same τ functions. The following proposition shows that the agreement holds at each fixed lattice spacing, before taking any continuum limit.

**Proposition 2.6 (Common physical fields).** Let $h>0$, and let positive, sufficiently smooth τ functions $F_j,G_j$ satisfy the semi-discrete bilinear system [(9)](#en-eq-9). Define $u_j,\omega_j,v_j$ by (18), and define $Q_j,R_j,M_j$ by (27), (31), and $M_j=\partial_x\log G_j$, respectively. Then the PE reconstruction (18) and the PF reconstruction (36) yield identical physical fields $u_j,v_j$.

**Proof.** The definitions give

<a id="en-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{37}$$

Adding the same central difference of u to the second equality proves that the reconstructed v fields also coincide. □

This agreement allows us to use the same reconstructed exact fields as references for both formulations. It does not imply that their numerical approximations will coincide: further discretization in $x$ and $t$ acts on different dependent variables and different forms of the evolution equations. We examine these effects in Section 3. Before doing so, we establish how the semi-discrete equations and their exact wave fields approach the continuous DLW system as $h\to0$.

### 2.5 Continuum limits {#en-limits}

Having established the semi-discrete equations and their exact solutions, we now examine how they approach the continuous DLW system as the lattice spacing tends to zero. We wish to determine how the lattice modifies the exact wave fields and how the continuous equations emerge from the discrete relations. We first derive an expansion of the difference between the semi-discrete and continuous Gram solutions, including its leading coefficients. The second-order convergence of the reconstructed fields then follows directly. We subsequently examine the consistency of the nonlinear equations.

Throughout this subsection, $O_K(h^m)$ denotes a remainder bounded uniformly by $C_Kh^m$ on a compact set $K$, with $C_K$ independent of $h$. We assume sufficient smoothness on an open neighbourhood of $K$. Where derivatives of an expansion are used, the remainder estimate is understood to hold for those derivatives as well.

We begin by comparing corresponding members of the exact solution families. To make this comparison at a common physical position, we extend the lattice τ functions to continuous $y$ and retain the staggered reconstruction. For positive functions $f_h,g_h$, we define

<a id="en-eq-47"></a>

$$\begin{aligned}U_h(y)&=\partial_x[2\log f_h(y)-\log g_h(y-h/2)-\log g_h(y+h/2)],\\\Omega_h(y)&=\partial_x[\log g_h(y+h/2)-\log g_h(y-h/2)],\\V_h(y)&=\frac4h\Omega_h(y)+\frac{U_h(y+h)-U_h(y-h)}{2h}.\end{aligned}\tag{38}$$

Here and below, we suppress the common arguments $x,t$ when displaying shifts in $y$. At $y=(j+\tfrac12)h$, these expressions agree with the lattice reconstruction in (18).

**Theorem 2.7 (Leading error and convergence of the exact wave fields).** Fix the determinant order $N$ and real spectral parameters satisfying, for some $h_0>0$,

<a id="en-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{39}$$

Let $f,g$ be the continuous Gram τ functions in (5), and let $u,v$ be their physical fields defined by (2). For $0<h\le h_0$, extend the positive lattice factors to real powers and set

<a id="en-eq-60"></a>

$$g_h(x,y,t)=\tau_0(y/h),\qquad f_h(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{40}$$

Let $U_h,V_h$ be the staggered reconstruction defined above. Write $\alpha=\log f$, $\beta=\log g$, $z_i=p_i-a$ and $w_i=q_i+a$, and define

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,$$

$$\alpha_2=\sum_{i=1}^{N}(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_{i=1}^{N}c_i\rho_i\partial_{\rho_i}\beta.$$

Then, uniformly on every compact set $K$,

<a id="en-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{41}$$

Consequently, for sufficiently small $h>0$,

<a id="en-eq-61"></a>

$$\sup_K\bigl(|U_h-u|+|V_h-v|\bigr)\le C_Kh^2\tag{42}$$

The same expansion applies to the physical fields reconstructed through either PE or PF.

**Proof.** We first expand the lattice factors while keeping the spectral parameters fixed:

<a id="en-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{43}$$

For each determinant entry, the coefficient of $y$ in the lattice phase therefore satisfies

<a id="en-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{44}$$

In $f_h$, the half-grid displacement also combines with the shift of the auxiliary parameter. The resulting amplitude factor is

<a id="en-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}\left[1+\frac{h^2}{8}\left(\frac1{w_k^2}-\frac1{z_i^2}\right)+O(h^4)\right].\end{aligned}\tag{45}$$

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

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{46}$$

The PE equations then take the form

<a id="en-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{47}$$

With $\mathcal M_+z_j=(z_{j+1}+z_j)/2$, the identity $\mathcal M_+\delta_-=\delta_0$ shows that the time derivative in $\mathcal M_+E_{1,h,j}+E_{2,h,j}$ is $v_{j,t}$. We therefore compare this combination with the second continuous DLW equation.

**Proposition 2.8 (Consistency of the equations).** Sample sufficiently smooth fields $u,v$ at $y_j=(j+\tfrac12)h$, and define the continuous residuals

<a id="en-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{48}$$

Then, uniformly on compact sets,

<a id="en-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{49}$$

**Proof.** We set $m_j=y_j-h/2$. Expanding the difference and averaging operators about their respective centres gives

<a id="en-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{50}$$

Consequently,

<a id="en-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{51}$$

These expansions also hold after the required differentiation. Substitution into the first residual yields $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$.

For the second residual, we write $w=v-u_y$ and obtain

<a id="en-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{52}$$

Averaging the first residual about $y_j$ and adding the second gives

<a id="en-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{53}$$

Here all continuous fields are evaluated at $y_j$. This proves the second assertion. □

The continuum-limit analysis shows that the proposed lattice system retains a quantitative connection with the continuous DLW model. We recover the continuous equations with second-order consistency and, for the exact solution families considered here, obtain uniform second-order convergence of both physical fields on compact sets. At finite lattice spacing, the coefficients $C_U$ and $C_V$ give a more detailed account of this approximation: they describe the leading difference in each field and how that difference varies across the wave profile. We can thus assess the effect of discretizing $y$ directly in the reconstructed physical fields. Since PE and PF yield identical fields from the same τ functions, the error expansion and its coefficients apply to both formulations.

### 2.6 Darboux–Lax representation {#en-lax}

The preceding analysis establishes the connection between the semi-discrete system and the continuous DLW equations. We now return to the structure of the lattice system at finite spacing and seek an auxiliary linear problem whose compatibility reproduces the nonlinear evolution. This will allow us to relate the field equations to the consistency of two operations: transferring a wave function between neighbouring lattice sites and evolving it in time.

To develop this representation, we first write the PE equations in shifted field variables and introduce an auxiliary potential. We then construct the lattice and time equations for the wave function and establish their compatibility with the nonlinear system. For the τ-function solutions, we show how the required potential and Darboux relations follow from the bilinear equations. Finally, we express the same linear problem in the variables $Q_j,R_j,M_j$, making its connection with the PF formulation explicit.

We begin by absorbing the constant terms in the PE equations into shifted variables:

<a id="en-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{54}$$

With this choice, the flux in the second equation becomes proportional to $U_jw_j$, while the first equation takes a quadratic form in $U_j$ and $w_j$. Substituting (54) into (25), we obtain

<a id="en-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{55}$$

To construct the auxiliary linear problem, we introduce a potential $V_j$ through its $x$-derivative and its change between neighbouring lattice sites:

<a id="en-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{56}$$

These two relations must assign the same value to $V_{j+1,x}-V_{j,x}$. We check this by taking the difference of the first relation at adjacent sites and comparing it with the $x$-derivative of the second. Their agreement is exactly the first equation in (55), evaluated at the corresponding lattice index.

We can therefore construct $V_j$ locally whenever the nonlinear equations hold. We first integrate the prescribed $x$-derivative at one reference site, then use the lattice relation to determine $V_j$ at neighbouring sites. The compatibility just established ensures that these propagated values satisfy the prescribed $x$-derivative at every site. The remaining freedom is a function of $t$ common to all lattice sites.

With the auxiliary potential in place, we introduce a wave function $\psi_j(x,t)$ and consider the linear system

<a id="en-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{57}$$

The first equation relates the wave functions at neighbouring lattice sites through two first-order differential operators in $x$. The second prescribes their time evolution at each site. We require these relations to remain consistent as time evolves: transferring the wave function to the next site and then evolving it must agree with evolving it first and then applying the lattice relation.

To express this requirement, we write

$$\mathscr A_j=\partial_x-\frac{U_j}{2}-\frac{hw_j}{8},\qquad \mathscr B_j=\partial_x-\frac{U_j}{2}+\frac{hw_j}{8},$$

and introduce the formal transfer and time-evolution operators

$$T_j=\mathscr B_j^{-1}\mathscr A_j,\qquad H_j=-\partial_x^2-V_j.$$

The linear system then reads $\psi_{j+1}=T_j\psi_j$ and $\psi_{j,t}=H_j\psi_j$. Its compatibility is expressed by

$$T_{j,t}=H_{j+1}T_j-T_jH_j.$$

Here $\mathscr B_j^{-1}$ is understood as a formal pseudodifferential inverse. The following theorem relates this operator identity to the nonlinear field equations.

**Theorem 2.9 (Darboux–Lax compatibility).** Every smooth solution of [(55)](#en-eq-70), together with the auxiliary potential [(56)](#en-eq-71), makes [(57)](#en-eq-72) compatible in the formal operator sense. Conversely, on a region where $w_j\ne0$, compatibility together with the potential-difference relation implies [(55)](#en-eq-70).

**Proof.** Factor the lattice transfer as $T_j=\mathscr B_j^{-1}\mathscr A_j$, with $\mathscr A_j=\partial_x-U_j/2-hw_j/8$ and $\mathscr B_j=\partial_x-U_j/2+hw_j/8$. The field equations make both scalar Darboux residuals vanish and give a common intermediate potential, hence $T_{j,t}=H_{j+1}T_j-T_jH_j$. Conversely, the coefficients of orders zero and minus one imply vanishing of both residuals when $w_j\ne0$. Their sum and difference recover the field equations. The operator identities are recorded in [Appendix C](#en-app-c). □

For the solutions constructed from τ functions, we can express the auxiliary potential and the Darboux coefficients directly in terms of $F_j,G_j$. Using the reconstruction formulas, we obtain

<a id="en-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{58}$$

The expressions for $r_j$ and $s_j$ agree with $U_j/2+hw_j/8$ and $U_j/2-hw_j/8$, respectively. The potential also satisfies the required lattice relation, since

$$V_{j+1}-V_j=2\partial_x^2\log\frac{G_{j+1}}{G_j}=2\omega_{j,x}=\frac h2w_{j,x}.$$

We then return to the normalized bilinear equations in (19). Differentiating them in $x$ and substituting (58), we find that the first gives $\mathcal E_j^r=0$, while the second gives $\mathcal E_j^s=0$. Their sum also recovers the prescribed expression for $V_{j,x}$ in (56). Thus, the same bilinear equations used to construct the exact fields supply the relations needed for their Darboux–Lax representation. In particular, the Gram determinant solutions of Section 2.3 satisfy these compatibility relations wherever the τ functions are positive.

We finally express the linear system in the potential variables used in PF. From the reconstruction relations, we have

<a id="en-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{59}$$

Substituting these expressions into (57), we obtain

<a id="en-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{60}$$

Equation (60) gives the Darboux–Lax system in the PF variables. The potential relation used above is also contained in the PF lattice constraint, whose $x$-derivative gives

<a id="en-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{61}$$

Through the Darboux–Lax representation, we interpret the nonlinear field equations as the conditions that make lattice transfer consistent with time evolution. We describe these two operations through linear equations for an auxiliary wave function and, under the conditions of the compatibility theorem, recover the nonlinear system by requiring them to agree. This gives us a way to examine the integrable structure of the equations at finite lattice spacing. By expressing the same linear problem in PE and PF variables, we also show how the two formulations retain this structure despite their different treatment of the potential.

We have therefore connected the construction of the lattice equations with both their exact solutions and their Darboux–Lax representation. Starting from the continuous bilinear relations, we obtained a semi-discrete system whose wave fields can be reconstructed explicitly and compared quantitatively with the continuous DLW solutions. These exact fields also allow us to assess what happens when we use the nonlinear equations for computation. Although PE and PF reconstruct the same fields analytically, their numerical implementations evolve different variables and introduce further approximations in $x$ and $t$. With the exact solutions and the $y$-discretization error now available as references, we can investigate how these choices affect the accuracy of the computed physical fields.

## 3. Numerical methods and experiments {#en-numerics}

In this section, we develop numerical methods for the semi-discrete DLW system and examine how its nonlinear formulations and numerical implementation affect computational accuracy. In Section 3.1, we discretize the remaining $x$ derivatives in PE and PF and introduce a direct finite-difference approximation of the continuous system for comparison. We also derive the leading spatial error terms to help explain the accuracy of these approximations. In Section 3.2, we use the semi-discrete conservation law to construct a self-adaptive moving mesh method (SAMM), coupling the motion of shared $x$ nodes to the evolution of the physical fields. In Section 3.3, we describe the time integration of the resulting systems, including the coupled field and mesh equations. In Section 3.4, we introduce four one- and two-soliton test problems and define the error measures. In Section 3.5, we compare the numerical results and draw on the spatial error analysis to discuss how the nonlinear formulation, time integrator and mesh choice influence the accuracy of both physical fields.

### 3.1 Spatial discretization {#en-schemes}

For the numerical comparison, we apply the same centred differences in $x$ to PE, PF and a direct finite-difference approximation of the continuous DLW system, denoted by FD. This allows us to examine the different formulations under a common spatial discretization.

**Grid and difference operators.** On the fixed grid, let $x_i=-L/2+i\Delta x$, where $\Delta x=L/N_x$. In the y direction, $M_j$ is located at $y=jh$, while $u_j,v_j,Q_j,R_j$ are located at $y=(j+\tfrac12)h$. The indices j and i label the y layers and x nodes, respectively. Time remains continuous in the spatially discretized systems below.

We approximate the x derivatives by three-point centred differences

<a id="en-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{62}$$

For smooth functions, the centred differences satisfy

<a id="en-eq-202"></a>

$$D_1f=f_x+\frac{(\Delta x)^2}{6}f_{xxx}+O((\Delta x)^4),\qquad D_2f=f_{xx}+\frac{(\Delta x)^2}{12}f_{xxxx}+O((\Delta x)^4).\tag{63}$$

$D_2$ is the independent three-point second derivative, not $D_1^2$.

In the y direction, we use

<a id="en-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{64}$$

The operators $D_1,D_2$ act on the x-node index, whereas $\delta_-,\delta_0,\mathcal M_-$ act on the layer index. All products and quotients below are evaluated pointwise. We first construct the PE and PF schemes, followed by the direct finite-difference scheme, denoted by FD.

**PE scheme.** We evolve $P=\delta_-u$ and $W=v-\delta_0u$. The lower boundary value fixes u by cumulative summation of P, and $v=W+\delta_0u$; see [Appendix D](#en-app-d). The evolution equations are $\dot P=F_P$, $\dot W=F_W$, with

<a id="en-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{65}$$

Thus the right-hand side is evaluated by first recovering u from P, and then applying the spatial difference operators to u and W. The field v follows from the same reconstruction formula.

**PF scheme.** We evolve Q and R and reconstruct the physical fields through

<a id="en-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{66}$$

Here $m_j\simeq M_{j,x}$ is obtained from the lattice constraint and lower boundary data as detailed in Appendix D. The final rates are

<a id="en-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{67}$$

The lowest Q layer is prescribed, while the interior Q layers and all R layers are evolved. The physical fields are recovered from Q and R using (66).

**FD scheme.** For comparison, we discretize the continuous DLW equations directly, taking $P=\delta_-u$ and v as the evolution variables. The field u is recovered from P by the first relation in (106). The resulting system is $\dot P=F_P$ and $\dot v=F_v$, with

<a id="en-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{68}$$


**Leading x-discretization error.** We examine how centred differences in $x$ affect the approximation of $u_t$ in PE and FD. For the same smooth fields on a fixed finite $y$ interval, with the prescribed lower-boundary rate at $y=b$, both schemes have the leading contribution

<a id="en-eq-203"></a>

$$r^u_{x,m}=(\Delta x)^2B+O\!\left((\Delta x)^4+(\Delta x)^2h^2\right),\qquad m=\mathrm{PE},\mathrm{FD}.\tag{69}$$

The coefficient is

<a id="en-eq-204"></a>

$$\boxed{B=-\frac16\partial_x^3\left[\frac{u(x,y,t)^2-u(x,b,t)^2}{2}+2a\bigl(u(x,y,t)-u(x,b,t)\bigr)\right]-\frac1{12}\partial_x^4\int_b^y v(x,s,t)\,ds.}\tag{70}$$

Here $r^u_{x,m}$ compares centred $x$ differences with exact $x$ derivatives on the same $y$-discrete state at interior $x$ nodes. Thus, $B$ identifies the leading spatial distribution of the error introduced by the common $x$ stencil.

*Derivation.* We begin with the $P$ equations, namely $\dot P=F_P$ in (65) for PE and in (68) for FD. Since $P_r=(u_r-u_{r-1})/h$, summing these equations from the lower layer $\ell$ gives
$$F^u_{m,j}=u_t(x,b,t)+h\sum_{r=\ell+1}^{j}F_{P,m,r}.$$
For FD, the first term telescopes and the second forms a trapezoidal sum:
$$F^u_{\mathrm{FD},j}=u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)\right]
-D_2\left[\frac h2\sum_{r=\ell+1}^{j}(v_r+v_{r-1})\right].$$
Applying the centred-difference expansions (63), and replacing the trapezoidal sum by $\int_b^y v\,ds+O(h^2)$, gives the coefficient (70). The corresponding $x$ derivatives of the quadrature remainder are also $O(h^2)$ for the smooth fields considered.

For PE, the same summation gives
$$\begin{aligned}
F^u_{\mathrm{PE},j}={}&u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)
+h^2\left(\frac{W_j^2-W_\ell^2}{32}-\frac{W_j-W_\ell}{4}\right)\right]\\
&-D_2\left[u_j-u_\ell+\frac h2\sum_{r=\ell+1}^{j}(W_r+W_{r-1})\right].
\end{aligned}$$
Here $W=v-\delta_0u=v-u_y+O(h^2)$. The integral of $u_y$ cancels the endpoint difference $u_j-u_\ell$, leaving the same integral of $v$ to leading order. The additional flux term carries an explicit factor $h^2$. Applying (63) therefore gives

<a id="en-eq-205"></a>

$$\begin{gathered}
r^u_{x,\mathrm{PE}}=(\Delta x)^2B_{h,\mathrm{PE}}+O((\Delta x)^4),\qquad
r^u_{x,\mathrm{FD}}=(\Delta x)^2B_{h,\mathrm{FD}}+O((\Delta x)^4),\\
B_{h,\mathrm{PE}}=B+O(h^2),\qquad B_{h,\mathrm{FD}}=B+O(h^2),\qquad
B_{h,\mathrm{PE}}-B_{h,\mathrm{FD}}=O(h^2).
\end{gathered}\tag{71}$$

The $O(h^2)$ difference concerns the coefficients multiplying $(\Delta x)^2$, so the difference between these leading $x$-error contributions is $O((\Delta x)^2h^2)$. These expressions provide a common reference for comparing PE and FD when we interpret the numerical results.

These three spatial discretizations are combined with the time integrators in Section 3.3. Their initial and boundary data are specified in Section 3.4.

### 3.2 Self-adaptive moving mesh method {#en-samm}

A uniform grid may allocate many points to weakly varying regions while resolving a narrow wave band inadequately. Moving mesh methods address this imbalance by redistributing nodes through a solution-dependent density [14]. For integrable equations, conservation laws offer a direct connection between the solution and the mesh: examples include self-adaptive methods for the Camassa–Holm equation [12], short pulse equations [13] and a generalized sine-Gordon equation [9]. In the present two-dimensional setting, we retain a uniform $y$ lattice and use the same moving $x$ nodes on every transverse layer. We therefore average the conservation density and flux across the layers to determine a shared node distribution. This adapts the $x$ resolution while preserving the tensor-product representation of the fields.

To obtain a density that follows the field evolution, we use the conservation form of the $W$ equation,
$$W_t+\bigl[(u+2a)W-4u\bigr]_x-W_{xx}=0.$$
The choice $\rho=1-W/4$ rewrites its nonlinear flux as
$$ (u+2a)W-4u=8a-4(u+2a)\rho.$$
It therefore leads directly to a conservation law for $\rho$, with $\rho=1$ on the zero-field background. We choose the flux to vanish on this background and obtain

<a id="en-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{72}$$

Substituting $W_j=4(1-\rho_j)$ into its evolution equation gives

<a id="en-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{73}$$

In PF, $\rho_j=Q_jR_j$. Since all $y$ layers share the same $x$ nodes, we determine the mesh motion from the transversely averaged density and flux,

<a id="en-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{74}$$

The initial nodes are chosen so that the integral of $\bar\rho(x,0)$ is equal between adjacent nodes. This assigns more nodes to regions of larger density. During evolution, each node retains its cumulative density integral, linking its motion to the evolving field. With the left endpoint $x_L$ fixed, the conservation law [(73)](#en-eq-97) gives

<a id="en-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{75}$$

The resulting node velocity is

<a id="en-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{76}$$

For the numerical evaluation of the flux, we approximate $\partial_x\rho$ by $D_1\rho$. The mesh evolution is defined for $\bar\rho>0$, while a positive mapping Jacobian preserves the ordering of the nodes. On this moving mesh, spatial derivatives are evaluated using the mapped centred operators in [Appendix E](#en-app-e). We then couple the field equations
$$\dot z=F_z+\mathcal V D_1z$$
to the node equation (76). The additional term accounts for the motion of the evaluation points; setting $\mathcal V=0$ recovers the fixed-grid formulation. Section 3.3 describes the time integration of this coupled system.

### 3.3 Time integration {#en-time}


After spatial discretization, we advance the resulting systems in time. For the comparisons between PE, PF and FD, and between fixed and moving meshes, we use the classical fourth-order Runge–Kutta method (RK4) [10]. Keeping the time integrator common allows us to examine the effects of the spatial formulation and mesh choice under the same time-stepping procedure. We then assess the influence of time integration separately by comparing forward Euler, RK4 and Crank–Nicolson (C–N) for PE on a fixed grid.

Let $z$ collect the evolving variables, so that each spatial scheme takes the form $\dot z=\mathcal F(t,z)$. For PE, these variables are $P,W$; for PF, they are the evolving components of $Q,R$; and for FD, they are $P,v$. The physical fields and auxiliary quantities are recovered when evaluating $\mathcal F$, using the reconstruction and boundary relations described above.

For SAMM, we include the node coordinates in the state and advance them together with the field variables. The resulting right-hand side contains both the field equations, with their mesh transport terms, and the node velocities from Section 3.2. This coupling allows changes in the fields to affect the mesh within each time step, while the updated mesh determines where the spatial derivatives are evaluated.

Given $z^n$ at time $t_n$, we compute the RK4 stages as
$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),\\
K_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_2/2),\\
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t K_3),
\end{aligned}$$
and update
$$z^{n+1}=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).$$

At each stage, we reconstruct the physical fields and auxiliary quantities from the stage variables and evaluate the prescribed boundary data at the corresponding stage time. For SAMM, the stage node positions determine the mapped spatial operators. The density, flux and node velocity are then evaluated from the same stage fields and mesh. Each call to $\mathcal F$ therefore represents a consistent intermediate state of the coupled system.

To examine the role of the time integrator, we retain the fixed-grid PE spatial discretization and vary only the time-stepping method. Forward Euler uses the current right-hand side,
$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n),$$
whereas Crank–Nicolson averages the right-hand sides at the two ends of the step:
$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
These methods provide first- and second-order temporal approximations, respectively, alongside the fourth-order RK4 method.

For Crank–Nicolson, the new state appears on both sides of the update. We solve the resulting nonlinear equation iteratively, reconstructing the fields and applying the boundary data whenever the right-hand side is evaluated. The iteration is monitored through the residual
$$\mathcal R(z^{n+1})=z^{n+1}-z^n-\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
The iteration procedure and stopping criterion are specified in [Appendix F](#en-app-f); the time-integrator comparison is presented in Section 3.5.2.

For all three integrators, we recover $u,v$ from the numerical state at the comparison time and evaluate their errors against the same exact solution. This keeps the assessment in the physical fields while allowing us to examine how the time-stepping method affects the accuracy of the chosen spatial scheme.

### 3.4 Test problems and error measures {#en-tests}

We use four soliton solutions of the continuous DLW system to examine how the numerical methods resolve different wave profiles. We begin with two one-soliton solutions whose $u$ pulses have opposite signs, and then consider two-soliton solutions with different wave orientations and combinations of polarity. This progression allows us to compare the methods on individual waves before examining the more varied spatial structure of interacting waves. In each case, the exact solution supplies the initial and boundary data and provides the reference for measuring errors in both physical fields. Throughout these tests, we take $a=2$, set the determinant coefficients to $\rho_i=1$, and choose zero initial phases.

We examine the solutions over regions containing the principal wave profiles and place the computational boundaries farther out. The regions for the four tests are $[-5,5]^2$, $[-10,10]^2$, $[-30,30]^2$, and $[-30,30]^2$, respectively, and are kept the same across the numerical methods.

**One-soliton solutions.** For the one-soliton tests, we set $N=1$ in the continuous Gram determinant and obtain

<a id="en-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{77}$$

where

<a id="en-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{78}$$

The physical fields then take the explicit form

<a id="en-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{79}$$

These expressions guide our choice of parameters. When $p+q>0$ and $c>0$, the signs of the two pulses are determined by $c-1$ and $\ell$, respectively. We therefore choose $(p,q)=(1,2)$ and $(4,-3)$, giving a negative $u$ pulse in the first test and a positive one in the second. The corresponding values are $(c,\ell)=(1/4,-3/4)$ and $(2,-1/2)$, so the $v$ pulse remains negative in both cases.

The first profile is shown below at $t=0$. Both $u_*$ and $v_*$ form a negative trough extending obliquely across the region. Their variation is concentrated across the wave band, giving us a simple setting in which to examine how the methods resolve a localized pulse in each field.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_1_2.png" alt="Exact profiles: One soliton (1,2); t=0. Left: u; right: v." loading="lazy"><figcaption>Exact profiles: One soliton (1,2); t=0. Left: u; right: v.</figcaption></figure>

With the second parameter choice, the $u_*$ trough is replaced by a positive ridge, while $v_*$ remains negative. The profiles also differ from the first case in amplitude and transverse width. We use this case to extend the comparison to a different pulse shape as well as the opposite polarity of $u_*$.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_4_m3.png" alt="Exact profiles: One soliton (4,−3); t=0. Left: u; right: v." loading="lazy"><figcaption>Exact profiles: One soliton (4,−3); t=0. Left: u; right: v.</figcaption></figure>

**Two-soliton solutions.** We next consider two-soliton solutions to examine how the methods resolve the spatial structure formed by two interacting waves. Setting $N=2$ and expanding the Gram determinant gives

<a id="en-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{80}$$

where

<a id="en-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{81}$$

We obtain the physical fields from $u_*=2\partial_x\log(f_*/g_*)$ and $v_*=2\partial_x\partial_y\log(f_*g_*)$. The mixed term $E_1E_2$ incorporates the interaction between the two waves, with its coefficient determined by their spectral parameters.

In the first test, we choose $(p_1,q_1)=(6,-5)$ and $(p_2,q_2)=(4,-3)$, which gives $c_1=4/3$, $c_2=2$, and $A_{12}=4/3$. The phases $\theta_1=x-11t-y/12$ and $\theta_2=x-7t-y/2$ describe waves with different spatial orientations and propagation rates.

The corresponding profiles are shown below. The two positive ridges in $u_*$ approach one another along different directions and form a higher crest in the interaction region. The accompanying $v_*$ field contains two negative troughs whose shape also changes near their meeting point. This spatial variation allows us to examine the resolution of both the individual wave bands and the region where they interact.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton.png" alt="Exact profiles: Two solitons (6,−5; 4,−3); t=0. Left: u; right: v." loading="lazy"><figcaption>Exact profiles: Two solitons (6,−5; 4,−3); t=0. Left: u; right: v.</figcaption></figure>

For the second test, we retain $(p_2,q_2)=(4,-3)$ and choose $(p_1,q_1)=(1,2)$, bringing together the two parameter pairs used in the one-soliton tests. Here $c_1=1/4$, $c_2=2$, and $A_{12}=5/4$, with $\theta_1=3x+3t-3y/4$ and $\theta_2=x-7t-y/2$.

In this case, a positive ridge and a deeper negative trough coexist in $u_*$, while the two wave bands in $v_*$ remain negative. The difference in their amplitudes and widths gives the profile a more uneven spatial structure. By including this case, we examine how the methods resolve a smaller positive feature alongside a stronger negative wave and represent their interaction in both physical fields.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton_mixed.png" alt="Exact profiles: Two solitons (1,2; 4,−3); t=0. Left: u; right: v." loading="lazy"><figcaption>Exact profiles: Two solitons (1,2; 4,−3); t=0. Left: u; right: v.</figcaption></figure>

**Initial and boundary data.** To compare the three formulations from the same physical initial state, we use the continuous exact fields $u_*,v_*$ to initialize their respective variables. For PE, we set $P^0=\delta_-u_*(0)$ and $W^0=v_*(0)-\delta_0u_*(0)$, while FD uses the same $P^0$, together with $v^0=v_*(0)$. For PF, we determine $Q^0,R^0$ from these physical data and fix the normalization of $Q$ at the leftmost $x$ node. The reconstruction and lower-boundary initialization are described in Appendix D.

During time integration, the continuous exact solution supplies the lower $y$-boundary data and the ghost values of $u$. In the $x$ direction, PE and FD use periodic continuation, whereas PF incorporates the prescribed additive jumps of $Q$ and $R$. These boundary relations are applied when evaluating the right-hand side at each stage of the time integrator.

**Computational settings.** The fixed grids have spacing $\Delta x=h=0.1$. In the SAMM calculations, we keep the same number of nodes and the uniform $y$ spacing $h=0.1$, while allowing the $x$ nodes to follow the transversely averaged conservation density defined in Section 3.2. This lets us examine how redistributing the available nodes affects the accuracy of the computed wave profiles.

All tests start at $t=0$ and advance to $T=0.01$ with $\Delta t=10^{-4}$, giving 100 time steps. We use RK4 for the comparisons of the spatial formulations and meshes; the separate time-integrator comparison retains the fixed-grid PE scheme and the same time step.

**Error measures.** We compare the numerical and exact physical fields at the same spatial locations, using cubic spline interpolation along $x$ for the numerical nodal values. Let $\mathcal G$ denote the common set of comparison points in the region under consideration. The maximum absolute errors at the final time are

<a id="en-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{82}$$

We report the errors in the two fields separately to examine how each responds to the formulation, time integrator, and mesh choice.

For PE and PF, we further interpret the total error through the corresponding semi-discrete exact solution. Writing $Z=(u_*,v_*)$ for the continuous exact field and $Z_h=(U_h,V_h)$ for the semi-discrete exact field with the same spectral parameters, we have

<a id="en-eq-206"></a>

$$Z_{\mathrm{num}}-Z=\underbrace{Z_h-Z}_{\text{lattice error}}+\underbrace{Z_{\mathrm{num}}-Z_h}_{\text{numerical error}}.\tag{83}$$

Under the assumptions of Section 2.5, the lattice error satisfies $Z_h-Z=h^2C+O(h^4)$, where $C=(C_U,C_V)$. The coefficients derived there describe the leading spatial distribution of the error introduced by discretizing $y$. The remaining contribution includes the effects of the $x$ and time discretizations, field recovery, and initial and boundary data. We use this decomposition in the numerical results below to discuss how the lattice and numerical contributions combine and to interpret the observed errors in both physical fields.

### 3.5 Numerical results {#en-results}

With these test problems, we examine how the nonlinear formulation, time integrator, and mesh choice affect the accuracy of the two physical fields. We begin by comparing PE, PF, and FD on fixed grids with RK4, using both the maximum errors and their spatial distributions to assess the differences between the formulations. We then retain the PE spatial scheme and compare Euler, RK4, and Crank–Nicolson to examine the influence of time integration. Finally, we compare fixed grids with SAMM under the same RK4 method and node count to assess the benefit of redistributing the mesh. Where relevant, we draw on the analytical error coefficients and the decomposition above to interpret the observed differences. In the tables, $e_u=E_u(T)$ and $e_v=E_v(T)$ denote the maximum absolute errors at the final time.

#### 3.5.1 Comparison of spatial discretizations {#en-spatial-results}

We first compare PE, PF, and FD under the same grid spacing and time-stepping procedure. Starting from the continuous exact physical fields, we advance all three schemes on fixed grids with RK4 to $T=0.01$. Table 1 reports the maximum absolute errors in $u$ and $v$, allowing us to assess how the choice of formulation affects each field.

**Table 1. Maximum absolute errors $e_u/e_v$ on fixed grids; RK4, $\Delta x=h=0.1$, $\Delta t=10^{-4}$, $T=0.01$. Bold values indicate the smallest error in each field.**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>PE: e<sub>u</sub> / e<sub>v</sub></th><th>PF: e<sub>u</sub> / e<sub>v</sub></th><th>FD: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td>3.061201e-03 / 3.067031e-03</td><td><strong>4.715088e-04</strong> / <strong>1.201923e-03</strong></td></tr><tr><th>One-soliton (4, −3)</th><td><strong>1.419616e-05</strong> / 2.745967e-05</td><td>8.067776e-05 / 4.377502e-04</td><td>1.718043e-05 / <strong>2.605300e-05</strong></td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td><strong>3.552455e-05</strong> / 5.359645e-05</td><td>7.501357e-05 / 5.394947e-05</td><td>3.989986e-05 / <strong>5.173628e-05</strong></td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td>4.102555e-03 / 3.252786e-03</td><td><strong>4.782980e-04</strong> / <strong>1.350627e-03</strong></td></tr></tbody></table></div>

PE and FD give errors of comparable magnitude across the four tests, with their relative performance depending on the field and wave profile. For the $(4,-3)$ one-soliton solution and the $(6,-5;\,4,-3)$ two-soliton solution, PE gives the smaller $u$ error, while FD gives the smaller $v$ error. In the remaining two tests, FD is more accurate in both fields. Thus, even within the same wave solution, the two physical fields can respond differently to the choice of formulation.

The PF results show a stronger variation between cases. Its errors exceed those of PE and FD in both fields throughout the table, but the size of the difference changes substantially. For the first two-soliton test, its $v$ error is close to those of the other two methods; for the $(4,-3)$ one-soliton test, it is more than an order of magnitude larger. Although PE and PF represent the same semi-discrete system, their different variables and the subsequent numerical operations lead to different error magnitudes after full discretization.

To see where these differences arise in space, we next examine the absolute-error surfaces in Figures 1–4. The columns show PE, PF, and FD from left to right, with the $u$ error in the upper row and the $v$ error in the lower row. For each field, the three methods share the same colour and height scales, so that both the magnitude and spatial distribution of the errors can be compared directly.

For the first one-soliton solution, we observe errors concentrated along the oblique wave band in both fields. Figure 1 shows similar error patterns for PE and FD, with several parallel ridges in the $u$ error and a more pronounced central band in the $v$ error. PF produces larger errors along the same wave structure. Its higher maximum errors in Table 1 therefore reflect an extended band of larger deviations rather than a single isolated peak.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png" alt="Figure 1. One soliton (1,2): absolute-error surfaces at T=0.01." loading="lazy"><figcaption>Figure 1. One soliton (1,2): absolute-error surfaces at T=0.01.</figcaption></figure>

The second one-soliton test reveals a more pronounced difference between the formulations. In Figure 2, the PE and FD errors remain concentrated near the wave band and have similar spatial shapes. The PF $v$ error extends over a broader portion of the region and remains visibly elevated away from the principal band. We thus see a difference in both the magnitude and spatial extent of the error, accompanying the larger separation between the PF and PE/FD maximum $v$ errors in Table 1.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png" alt="Figure 2. One soliton (4,−3): absolute-error surfaces at T=0.01." loading="lazy"><figcaption>Figure 2. One soliton (4,−3): absolute-error surfaces at T=0.01.</figcaption></figure>

For the first two-soliton solution, the error surfaces follow the two wave branches and develop a pronounced peak near their interaction region. In Figure 3, we find this structure in the $v$ errors of all three methods, whose maximum values are also close. The $u$ errors show a clearer distinction: PF produces a higher peak near the interaction, while PE and FD retain similar distributions with smaller amplitudes. Comparing the two rows makes the field dependence evident—the formulations give closely matched $v$ errors in this case, but differ more substantially in $u$.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png" alt="Figure 3. Two solitons (6,−5; 4,−3): absolute-error surfaces at T=0.01." loading="lazy"><figcaption>Figure 3. Two solitons (6,−5; 4,−3): absolute-error surfaces at T=0.01.</figcaption></figure>

In the mixed-polarity two-soliton test, the larger errors are concentrated near the stronger negative wave band, while the smaller positive feature is less prominent in the error surfaces. Figure 4 again shows similar distributions for PE and FD, with FD attaining smaller maximum errors in both fields. PF produces a substantially higher error band, particularly in $u$. Alongside the first one-soliton test, this case shows that the larger PF errors persist when the $(1,2)$ wave is incorporated into an interacting solution.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png" alt="Figure 4. Two solitons (1,2; 4,−3): absolute-error surfaces at T=0.01." loading="lazy"><figcaption>Figure 4. Two solitons (1,2; 4,−3): absolute-error surfaces at T=0.01.</figcaption></figure>

To interpret these spatial comparisons, we return to the two contributions identified in Section 3.4. For PE and PF, the exact semi-discrete fields differ from the continuous fields by $h^2C+O(h^4)$, where $C=(C_U,C_V)$ describes the leading spatial distribution of the lattice error. Since both formulations share the same exact semi-discrete physical fields, this contribution is common to them. Their different errors in Table 1 and Figures 1–4 therefore arise from the numerical contribution: the choice of evolved variables, their subsequent discretization, and the recovery of the physical fields lead to different approximations of the same semi-discrete solution.

To understand the relative performance of PE and FD more quantitatively, we evaluate their spatial truncation errors on the continuous exact fields at $t=0$. For the approximation of $u_t$, the leading error takes the form

$$r_m^u=\underbrace{(\Delta x)^2B}_{X}+\underbrace{h^2A_m}_{Y_m}
+O\!\left((\Delta x)^4+(\Delta x)^2h^2+h^4\right),\qquad m=\mathrm{PE},\mathrm{FD}.$$

Here $B$ is the common $x$-discretization coefficient discussed in Section 3.1, while $A_m$ describes the contribution from discretizing $y$. With $[f]_b^y=f(x,y,0)-f(x,b,0)$, the latter coefficients are

$$A_{\mathrm{FD}}=-\frac1{12}\partial_x^2[v_y]_b^y,\qquad
A_{\mathrm{PE}}=A_{\mathrm{FD}}-\partial_x\left[\frac{(v-u_y)^2}{32}-\frac{v-u_y}{4}\right]_b^y+\frac14\partial_x^2[u_{yy}]_b^y.$$

PE therefore changes both the magnitude of the $y$ contribution and its spatial relation to the common $x$ contribution. We measure this relation using the normalized spatial inner product

$$\gamma_m=\frac{\langle X,Y_m\rangle}{\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}},
\qquad \langle X,Y_m\rangle=\frac1{|\mathcal G|}\sum_{\mathcal G}XY_m.$$

For nonzero component norms, the resulting identity is

<a id="en-eq-207"></a>

$$\|X+Y_m\|_{\mathrm{RMS}}^2=\|X\|_{\mathrm{RMS}}^2+\|Y_m\|_{\mathrm{RMS}}^2+2\gamma_m\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}.\tag{84}$$

A negative $\gamma_m$ reduces the squared norm through cancellation, whereas a positive value increases it. Table 2 evaluates these leading contributions at $t=0$ with $\Delta x=h=0.1$, using RMS values and inner products on the grid points in the four test regions.

<div class="table-wrap error-budget-wrap"><table class="comparison error-budget"><caption>Table 2. Leading spatial truncation-error contributions to $u_t$ at $t=0$.</caption><colgroup><col style="width:23%"><col style="width:8%"><col style="width:18%"><col style="width:18%"><col style="width:13%"><col style="width:20%"></colgroup><thead><tr><th scope="col">Test</th><th scope="col">Method</th><th scope="col"><i>x</i> contribution<br>$\|X\|_{\mathrm{RMS}}$</th><th scope="col"><i>y</i> contribution<br>$\|Y_m\|_{\mathrm{RMS}}$</th><th scope="col">Correlation<br>$\gamma_m$</th><th scope="col">Combined error<br>$\|X+Y_m\|_{\mathrm{RMS}}$</th></tr></thead><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">One soliton<br>(1,2)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="1.01572e-02">1.016 × 10<sup>−2</sup></span></td><td><span class="budget-number" data-value="4.75387e-03">4.754 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="+0.3295">+0.3295</span></td><td><span class="budget-number" data-value="1.25535e-02">1.255 × 10<sup>−2</sup></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="1.38192e-03">1.382 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="-0.8512">−0.8512</span></td><td><span class="budget-number" data-value="9.01016e-03"><strong>9.010 × 10<sup>−3</sup></strong></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">One soliton<br>(4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="6.19698e-04">6.197 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="2.39752e-04">2.398 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.5367">−0.5367</span></td><td><span class="budget-number" data-value="5.31071e-04"><strong>5.311 × 10<sup>−4</sup></strong></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="3.58155e-05">3.582 × 10<sup>−5</sup></span></td><td><span class="budget-number" data-value="+0.9965">+0.9965</span></td><td><span class="budget-number" data-value="6.55395e-04">6.554 × 10<sup>−4</sup></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">Two solitons<br>(6,−5;<br> 4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="5.08691e-04">5.087 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="1.63056e-04">1.631 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.5780">−0.5780</span></td><td><span class="budget-number" data-value="4.35281e-04"><strong>4.353 × 10<sup>−4</sup></strong></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="2.46367e-05">2.464 × 10<sup>−5</sup></span></td><td><span class="budget-number" data-value="+0.8659">+0.8659</span></td><td><span class="budget-number" data-value="5.30168e-04">5.302 × 10<sup>−4</sup></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">Two solitons<br>(1,2;<br> 4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="4.39676e-03">4.397 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="1.93527e-03">1.935 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="+0.3044">+0.3044</span></td><td><span class="budget-number" data-value="5.31566e-03">5.316 × 10<sup>−3</sup></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="5.89777e-04">5.898 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.8643">−0.8643</span></td><td><span class="budget-number" data-value="3.89830e-03"><strong>3.898 × 10<sup>−3</sup></strong></span></td></tr></tbody></table><p class="budget-note">The <i>x</i> contribution is common to PE and FD within each test. Bold values indicate the smaller combined RMS residual in each pair.</p></div>

The leading expressions agree closely with the full spatial residuals, with relative RMS differences of $0.12\%$–$2.12\%$.

This analysis helps provide a quantitative explanation for the change in relative accuracy between PE and FD. The two methods share the leading $x$-discretization contribution, while their different treatments of $y$ produce different spatial error distributions. For the $(1,2)$ one-soliton and mixed-polarity two-soliton solutions, the FD $y$ contribution reduces the combined spatial residual, whereas the PE contribution increases it. For the other two solutions, this relation is reversed, and PE gives the smaller residual. The resulting ordering agrees with the final maximum $u$ errors in all four tests. We thus relate the observed differences between the two spatial schemes to their $y$-error coefficients evaluated on each wave profile, together with the common error introduced by the $x$ discretization.

Having compared the spatial formulations, we retain PE in the following experiments and examine how its accuracy changes with the time integrator and mesh placement.

#### 3.5.2 Time integration of PE {#en-time-results}

Having examined the spatial discretizations, we now retain the fixed-grid PE scheme and compare forward Euler, RK4, and Crank–Nicolson. All three methods start from the same initial data and advance to $T=0.01$, with $\Delta x=h=0.1$ and $\Delta t=10^{-4}$. We examine both the maximum errors and their spatial profiles to see how changing the time integrator affects the accuracy of each physical field.

The maximum absolute errors are listed in Table 3. Crank–Nicolson and RK4 give closely matched results in all four tests. Euler produces more noticeable differences: it gives a smaller maximum $u$ error for the $(1,2)$ one-soliton and mixed-polarity two-soliton solutions, whereas RK4 gives the smaller $u$ error in the other two tests. For $v$, RK4 gives the smallest maximum error in all four cases.

**Table 3. Maximum absolute errors $e_u/e_v$ for PE with Euler, RK4 and Crank–Nicolson. Fixed grids; $T=0.01$, $\Delta x=h=0.1$, $\Delta t=10^{-4}$.**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>Euler: e<sub>u</sub> / e<sub>v</sub></th><th>RK4: e<sub>u</sub> / e<sub>v</sub></th><th>C–N: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td><strong>6.396711e-04</strong> / 1.340634e-03</td><td>6.406395e-04 / <strong>1.339511e-03</strong></td><td>6.406384e-04 / 1.339513e-03</td></tr><tr><th>One-soliton (4, −3)</th><td>1.422394e-05 / 3.005484e-05</td><td><strong>1.419616e-05</strong> / <strong>2.745967e-05</strong></td><td>1.419664e-05 / 2.746028e-05</td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td>3.840649e-05 / 5.901085e-05</td><td><strong>3.552455e-05</strong> / <strong>5.359645e-05</strong></td><td>3.552653e-05 / 5.359819e-05</td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td><strong>6.188417e-04</strong> / 1.515498e-03</td><td>6.329588e-04 / <strong>1.511271e-03</strong></td><td>6.330018e-04 / 1.511273e-03</td></tr></tbody></table></div>

We next examine the spatial error profiles

$$\varepsilon_u^{(m)}(x)=\max_j|u_m(x,y_j,T)-u_*(x,y_j,T)|,\qquad
\varepsilon_v^{(m)}(x)=\max_j|v_m(x,y_j,T)-v_*(x,y_j,T)|.$$

Here $m$ denotes the time integrator. For each test, we show the two physical fields side by side and include local enlargements near the RK4 error peaks.

For the $(1,2)$ one-soliton solution, all three methods produce closely matched error profiles. The enlargements reveal a small difference near the peaks: Euler gives a slightly smaller $u$ error and a slightly larger $v$ error, while Crank–Nicolson and RK4 remain nearly indistinguishable.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1150"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="Figure 5. One soliton (1,2) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-2.35193500%);"></div><figcaption>Figure 5. One soliton (1,2) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods.</figcaption></figure>

The $(4,-3)$ one-soliton test shows a more visible response to the choice of integrator. Euler changes the shape of the $u$-error profile, although its maximum remains close to those of the other two methods. In $v$, the difference extends across a broad part of the wave profile, where Euler produces a higher error plateau.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1148"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="Figure 6. One soliton (4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-26.94034638%);"></div><figcaption>Figure 6. One soliton (4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods.</figcaption></figure>

For the $(6,-5;\,4,-3)$ two-soliton solution, we also observe a change in the location of the dominant $u$-error peak. Euler gives a smaller error near the RK4 peak shown in the inset, but develops a higher peak elsewhere. Its larger maximum in the table therefore reflects a redistribution of the error along the profile. In $v$, the main peak is higher for Euler, while the RK4 and Crank–Nicolson profiles remain closely matched.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1140"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="Figure 7. Two solitons (6,−5; 4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-51.48599530%);"></div><figcaption>Figure 7. Two solitons (6,−5; 4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods.</figcaption></figure>

The mixed-polarity two-soliton solution returns to the pattern observed in the first test. The three profiles are close over the region, with Euler giving a slightly lower $u$-error peak and a slightly higher $v$-error peak. The agreement between Crank–Nicolson and RK4 again holds throughout the profiles, including the enlarged regions.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1129"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="Figure 8. Two solitons (1,2; 4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-75.86059440%);"></div><figcaption>Figure 8. Two solitons (1,2; 4,−3) at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods.</figcaption></figure>

Across these tests, changing the time integrator affects both the size and location of errors within the spatially discretized solution. Crank–Nicolson and RK4 yield almost the same profiles at the chosen resolution, whereas Euler produces changes that depend on the wave and the physical field. We retain RK4 in the following experiments to examine the effect of mesh adaptation under a common time-stepping procedure.

#### 3.5.3 Numerical performance of the self-adaptive moving mesh method {#en-mesh-results}

We now examine whether the conservation-based mesh adaptation introduced in Section 3.2 improves the accuracy of PE with the same number of nodes. Both the fixed-grid and adaptive calculations use RK4, $\Delta t=10^{-4}$, and the uniform $y$ spacing $h=0.1$. For SAMM, the transversely averaged conservation density determines the initial distribution of the $x$ nodes, which subsequently evolve together with the physical fields.

We first illustrate this redistribution using the $(6,-5;\,4,-3)$ two-soliton solution. Figure 9 shows the local node spacing normalized by the uniform spacing $\Delta x=0.1$, plotted at the midpoint of each interval. Values below one indicate a higher concentration of nodes, while values above one indicate wider spacing.

<figure><img src="../Workspaces/dlw_paper_20261009/figures/SAMM_spacing_C.png" alt="Figure 9. Normalized local x spacing for the (6,−5; 4,−3) two-soliton solution. Grey dashed: adaptive initial mesh; blue: T=0.01; orange dotted: uniform mesh." loading="lazy"><figcaption>Figure 9. Normalized local x spacing for the (6,−5; 4,−3) two-soliton solution. Grey dashed: adaptive initial mesh; blue: T=0.01; orange dotted: uniform mesh.</figcaption></figure>

The adaptive mesh concentrates nodes in the central part of the region, with the smallest spacing near $x=0$, and compensates with slightly wider intervals farther away. At $T=0.01$, the minimum spacing is approximately $0.09834$, compared with $0.1$ on the uniform grid. The initial and final spacing curves nearly coincide over this short interval, so the displayed distribution is largely established by the initial adaptation and then adjusted during evolution.

To assess the effect on accuracy, we compare the maximum absolute errors in both physical fields. Table 4 also gives the percentage reduction relative to the fixed mesh,

$$\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{SAMM}}(T)}{E_f^{\mathrm{fixed}}(T)}\right)\%,\qquad f=u,v.$$

**Table 4. Maximum absolute errors $e_u/e_v$ of PE on fixed and adaptive meshes at $T=0.01$, with the same node count and RK4 integrator.**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>Test</th><th>Fixed mesh: e<sub>u</sub> / e<sub>v</sub></th><th>Moving mesh: e<sub>u</sub> / e<sub>v</sub></th><th>Reduction: u / v</th></tr></thead><tbody><tr><th>One-soliton (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td><strong>5.781845e-04</strong> / <strong>1.091714e-03</strong></td><td>9.75% / 18.50%</td></tr><tr><th>One-soliton (4, −3)</th><td>1.419616e-05 / 2.745967e-05</td><td><strong>1.334447e-05</strong> / <strong>2.621326e-05</strong></td><td>6.00% / 4.54%</td></tr><tr><th>Two-soliton (6, −5; 4, −3)</th><td>3.552455e-05 / 5.359645e-05</td><td><strong>3.304157e-05</strong> / <strong>5.060189e-05</strong></td><td>6.99% / 5.59%</td></tr><tr><th>Two-soliton (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td><strong>6.156957e-04</strong> / <strong>1.428010e-03</strong></td><td>2.73% / 5.51%</td></tr></tbody></table></div>

SAMM reduces the maximum errors in both fields for all four tests. The improvement ranges from $2.73\%$ to $9.75\%$ in $u$ and from $4.54\%$ to $18.50\%$ in $v$. To see where these gains occur, we examine the spatial error profiles defined in the preceding subsection.

For the $(1,2)$ one-soliton solution, the adaptive mesh lowers the dominant $u$-error peak and reduces the broad elevated portion of the $v$-error profile. The latter improvement extends across much of the wave region, accompanying the largest relative reduction in the table.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1020"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="Figure 10. Fixed-grid and SAMM error profiles for One soliton (1,2) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-2.60416667%);"></div><figcaption>Figure 10. Fixed-grid and SAMM error profiles for One soliton (1,2) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM.</figcaption></figure>

The $(4,-3)$ one-soliton solution shows a smaller but sustained improvement. SAMM lowers the broad central portions of both error profiles while preserving their overall shape. The reductions in the maximum errors therefore accompany a decrease over an extended part of the region.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1030"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="Figure 11. Fixed-grid and SAMM error profiles for One soliton (4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-26.75189394%);"></div><figcaption>Figure 11. Fixed-grid and SAMM error profiles for One soliton (4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM.</figcaption></figure>

For the $(6,-5;\,4,-3)$ two-soliton solution, we observe the clearest reductions near the principal error peaks around the interaction region. The profiles remain close along several of the separated wave branches. This case connects the node-spacing illustration above with the accuracy comparison: the modest redistribution of the shared $x$ mesh is accompanied by reductions of $6.99\%$ and $5.59\%$ in the maximum $u$ and $v$ errors, respectively.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1035"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="Figure 12. Fixed-grid and SAMM error profiles for Two solitons (6,−5; 4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-51.13636364%);"></div><figcaption>Figure 12. Fixed-grid and SAMM error profiles for Two solitons (6,−5; 4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM.</figcaption></figure>

In the mixed-polarity two-soliton test, SAMM lowers the broad central portions of both profiles. The narrow peak that determines the maximum $u$ error changes less, giving a reduction of $2.73\%$, while the maximum $v$ error decreases by $5.51\%$. The spatial profiles thus reveal improvements beyond those summarized by the single largest error.

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1029"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="Figure 13. Fixed-grid and SAMM error profiles for Two solitons (1,2; 4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM." loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-75.63920455%);"></div><figcaption>Figure 13. Fixed-grid and SAMM error profiles for Two solitons (1,2; 4,−3) at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM.</figcaption></figure>

Through these comparisons, we find that the conservation-based density provides a useful basis for allocating the shared $x$ nodes. Although the density is constructed from $W=v-\delta_0u$ and averaged over $y$, the resulting mesh reduces the maximum errors in both physical fields in every test considered. The degree and location of the improvement vary with the wave profile, while the node count and time integrator remain unchanged.

## 4. Conclusion {#en-conclusion}


In this work, we have connected the construction of an integrable semi-discrete DLW system with an analysis of its numerical approximation. Starting from the continuous bilinear equations, we introduced a staggered lattice in $y$, coupled to shifts of the bilinear operator parameter, while keeping $x$ and $t$ continuous. The resulting system retains Gram determinant solutions of arbitrary finite order. From this construction, eliminating or retaining the auxiliary potential leads to the PE and PF formulations, for which we established Darboux–Lax representations and their compatibility with the nonlinear equations.

The explicit solutions also allow us to follow how the discrete wave fields approach their continuous counterparts. Under the stated regularity and positivity assumptions, we proved second-order convergence of these fields, alongside second-order consistency of the equations. By deriving the leading error coefficients, we further identified the spatial changes introduced by the lattice. These coefficients give a concrete connection between the analytical construction and the errors examined in the numerical experiments.

When the remaining variables are discretized, the choice of nonlinear formulation becomes consequential. Although PE and PF describe the same exact semi-discrete physical fields, their numerical implementations give different error magnitudes and distributions, with PE attaining smaller maximum errors in both fields throughout the four tests. The comparison with FD presents a more varied picture: the relative accuracy changes with the wave profile and the physical field. For $u$, our analysis relates this variation to the different $y$-error coefficients acting together with a common leading $x$-discretization contribution. Evaluating these contributions at $t=0$ gives the same PE–FD ordering as the final maximum $u$ errors in all four cases. This agreement helps explain how the different spatial discretizations produce the observed accuracy, beyond a comparison of their formal orders.

With PE as the spatial formulation, we then examined how time integration and node placement affect the computation. At the tested resolution, Crank–Nicolson and RK4 give nearly coincident error profiles, while Euler produces changes that depend on the wave and the field. Mesh adaptation offers a further way to improve the approximation within the same formulation. Using the semi-discrete conservation law, we constructed a shared adaptive $x$ mesh that evolves with the fields while retaining a uniform $y$ lattice. With the node count and RK4 integrator unchanged, the adaptive mesh reduces the maximum errors in both fields across all four tests, by $2.73\%$–$9.75\%$ in $u$ and $4.54\%$–$18.50\%$ in $v$. In this way, the conservation law obtained from the semi-discrete system also guides the allocation of numerical resolution, improving the computed wave profiles with the available nodes.

Our work illustrates how the analytical structure of a semi-discrete system can inform both the interpretation and the design of its numerical approximation. The exact solutions let us follow the changes introduced by the lattice, while the error coefficients help explain why different discretizations perform differently on the same waves. The conservation law, in turn, provides a way to use this structure in allocating the computational nodes. By bringing these aspects together, we move from constructing a discrete equation with explicit solutions to understanding how its formulation and implementation shape the accuracy of the computed fields. This connection offers a basis for further developments in which analytical properties guide the choices made in numerical computation.

## Appendix A. Leading exact-family difference {#en-app-a}

We derive the leading difference between the exact semi-discrete and continuous fields by expanding the Gram determinants in the lattice spacing. With $z_i=p_i-a$ and $w_i=q_i+a$, the principal-minor expansion associates each term with a common row and column index set $I$. The lattice phase contributes $h^2y\sum_{i\in I}c_i$, while the centred $f$ amplitude in (45) contributes $h^2\sum_{i\in I}d_i$. These contributions give

<a id="en-eq-208"></a>

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,\qquad \alpha_2=\sum_i(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_i c_i\rho_i\partial_{\rho_i}\beta.\tag{85}$$

The operator $\rho_i\partial_{\rho_i}$ selects precisely the minors containing the index $i$. Expanding the determinant and then its logarithm therefore gives (85) for any fixed $N$. Substitution into the symmetric reconstruction at the physical midpoint yields

<a id="en-eq-209"></a>

$$\begin{aligned}U_h&=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4),\\V_h&=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).\end{aligned}\tag{86}$$

Substituting $4\beta_{xy}=v-u_y$ into (86) gives the coefficients in (41). For fixed regular spectral parameters and sufficiently small $h$, nonvanishing τ functions on a neighbourhood of $K$ ensure uniform bounds on the derivatives and remainders used in the expansion. The positive spectral domain in Theorem 2.7 satisfies these conditions. The same calculation applies to other regular real branches wherever these bounds hold.

## Appendix B. Adjacent-layer determinant identity {#en-app-b}

**Proof.** We prove the adjacent-layer identity (13) by expressing the shift in the Gram matrix as a rank-one update. The Gram matrix at layer $n$ is $M=I+(r_ic_k/(p_i+q_k))$, where

<a id="en-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{87}$$

Let $P=\operatorname{diag}(p_i)$, $Q=\operatorname{diag}(q_i)$ and $b=(Q+sI)^{-1}c$. The definitions give

<a id="en-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{88}$$

In particular, the rank-one update in (88) follows from

<a id="en-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{89}$$

We first work where $M$ is invertible and introduce

<a id="en-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{90}$$

The last equality follows from the matrix determinant lemma, while Jacobi’s formula gives $\kappa=\tau_{n,x}/\tau_n$. To collect the differentiated terms, set

<a id="en-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{91}$$

Using $H_x=-HM_xH$ and $H_t=-HM_tH$, direct differentiation yields

<a id="en-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{92}$$

For example, $z_x=HPr-\kappa z$, so that $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$. Differentiating this identity once more and eliminating $\eta_1,\eta_2$ gives

<a id="en-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{93}$$

Thus $\psi=1-\zeta$ satisfies

<a id="en-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{94}$$

For $f=\psi g$, expansion of the bilinear operator gives

<a id="en-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{95}$$

Taking $g=\tau_n$ and $f=\tau_{n+1}$ identifies (94) with the bilinear identity [(13)](#en-eq-13) wherever $M$ is invertible. The identity extends to singular matrices by polynomial continuation. To see this, we replace each $\rho_i$ by $\varepsilon\rho_i$. At fixed $x,t$, the matrix equals the identity when $\varepsilon=0$, so the bilinear residual vanishes for $\varepsilon$ near zero. Since this residual is a polynomial in $\varepsilon$, it vanishes identically. Evaluation at $\varepsilon=1$ completes the proof. □

## Appendix C. Darboux operator calculation {#en-app-c}

**Proof.** We express the lattice part of the linear system through two first-order Darboux operators and relate their compatibility to the nonlinear equations. For this purpose, we use

<a id="en-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{96}$$

<a id="en-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{97}$$

Here $\mathscr B_j^{-1}$ is defined in the algebra of formal pseudodifferential operators. The linear system reads $\psi_{j+1}=T_j\psi_j$ and $\psi_{j,t}=H_j\psi_j$. Differentiating the lattice relation in t and using both time equations gives

<a id="en-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{98}$$

To verify this identity, define the scalar residuals

<a id="en-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{99}$$

Using $V_{j+1}-V_j=(h/2)w_{j,x}$ gives

<a id="en-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{100}$$

The $w$ equation makes the difference in (100) vanish, while the definition of $V_{j,x}$ makes the sum vanish. Thus $\mathcal E_j^r=\mathcal E_j^s=0$. These scalar relations enter the operator calculation through the following Darboux identity, obtained by the product rule for a scalar function $r$:

<a id="en-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{101}$$

The potential-difference relation implies

<a id="en-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{102}$$

Writing

<a id="en-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{103}$$

and applying the Darboux identity to the two vanishing residuals yields

<a id="en-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{104}$$

Eliminating the common intermediate operator gives $L_{j+1}T_j=T_jL_j$, which is equivalent to [(98)](#en-eq-75).

For the converse, we assume compatibility together with the potential-difference relation. Repeating the operator calculation while retaining the scalar residuals gives

<a id="en-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{105}$$

Comparison of the coefficients of $\partial_x^0$ and $\partial_x^{-1}$ gives $\mathcal E_j^r=\mathcal E_j^s$ and $w_j\mathcal E_j^s=0$. Both residuals therefore vanish wherever $w_j\ne0$. Their difference recovers the $w$ equation. Applying $\delta_-$ to their sum and using the potential-difference relation then recovers the first nonlinear equation. □

## Appendix D. Reconstruction and boundary initialization {#en-app-d}

The numerical schemes require auxiliary initial values and boundary data consistent with the prescribed physical fields. For PF, we determine $Q$ from $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$, with the normalization $Q_{j,0}^0=1$, and then set $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$. The same relation determines the lower boundary value $Q_0(t)$ from $u_{*,0}(t)$.

The variables $P,W$ determine the physical fields through

<a id="en-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{106}$$

Here $j_L$ denotes the lowest layer, and the prescribed value $u_{j_L,i}(t)$ fixes the boundary contribution in the reconstruction.



To evaluate the potential term $(M_j+M_{j+1})_x$ in the evolution equations, we use $m_j\simeq M_{j,x}$ and $S_j=Q_jR_j$. Applying $D_1$ to the lattice constraint $M_{j+1}-M_j=h(1-S_j)$ gives

<a id="en-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{107}$$

Once the lower boundary value of $m$ is specified, (107) determines the remaining layers successively. Temporarily labelling the lowest layer as $0$, we obtain this value from its $Q$ equation:

<a id="en-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{108}$$

Here $Q_0(t)$ is prescribed by the lower boundary data, and $Q_{0,t}$ is its time derivative.

## Appendix E. Derivatives on moving nodes {#en-app-e}

As the mesh moves, the physical $x$ spacings become nonuniform. We evaluate spatial derivatives by mapping the moving nodes to fixed, uniformly spaced computational coordinates $\xi_i=-L/2+i\Delta\xi$, with $\Delta\xi=L/N_x$. Writing $x_i(t)=\xi_i+s_i(t)$, the displacement $s_i$ determines the discrete Jacobian $J_i=1+D_\xi s_i$, which approximates $J=x_\xi$.

The chain rule gives $\partial_x=J^{-1}\partial_\xi$ and hence

<a id="en-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{109}$$

Approximating the computational-coordinate derivatives by centred differences gives

<a id="en-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{110}$$

The operators $D_\xi,D_{\xi\xi}$ are the three-point formulas in [(62)](#en-eq-87), evaluated on the uniform computational grid. The time derivative at a moving node also includes the change in its position, giving $\dot z=F_z+\mathcal V D_1z$. Coupling this relation to the node equation [(76)](#en-eq-100) produces the field–mesh system advanced by the time integrators in Section 3.3. The fixed-grid calculation is recovered when $s=0$ and $\mathcal V=0$.

## Appendix F. Implicit time stepping {#en-app-f}

For the fixed-grid PE system, Crank–Nicolson time stepping requires a nonlinear solve at each step. The method averages the right-hand sides at the current and next time levels:

<a id="en-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{111}$$

For this calculation, $z$ collects the variables $P,W$. We initialize the nonlinear iteration with the forward Euler predictor $z^{(0)}=z^n+\Delta t\,\mathcal F(t_n,z^n)$ and apply the residual correction
$$z^{(r+1)}=z^{(r)}-\mathcal R(z^{(r)}),$$
Here $\mathcal R$ is the nonlinear residual defined in Section 3.3. Each residual evaluation includes recovery of the physical fields and application of the boundary data at the corresponding time. The stopping criterion is
$$\|\mathcal R(z^{(r)})\|_\infty\le 10^{-12}+10^{-11}\max(1,\|z^n\|_\infty).$$
An iterate satisfying this criterion is accepted, with at most 80 residual evaluations allowed per time step. [Section 3.5.2](#en-time-results) compares the resulting errors with those obtained using Euler and RK4.

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

**摘要。** 近年来，对 $(2+1)$ 维色散长波（DLW）系统的研究取得了一系列进展，既获得了显式解族，也加深了对其背后可积结构的理解。将这些进展延伸至离散情形，需要建立能够保留这一结构、并揭示波场相应变化的表述。本文引入一个可积的半离散 DLW 系统，其中 $y$ 坐标离散，$x$ 与 $t$ 连续。这一构造将交错格点平移与双线性参数的平移相耦合，得到半离散双线性系统，使连续系统的 Gram 行列式解能够推广至格点情形。通过消去或保留辅助势函数，该系统导出两种非线性表示，每种表示均具有相应的 Darboux–Lax 表示。我们建立半离散方程与连续 DLW 系统的二阶相容性。在适当的正则性与正性条件下，我们还证明半离散精确物理场以二阶精度收敛至相应的连续物理场，并推导这一物理场逼近误差的显式首项系数。

这些精确解也为考察半离散表示在数值计算中的表现提供了基准。我们首先展示，在 $x$ 方向采用统一中心差分的条件下，非线性表示的选择如何影响精度。空间误差分析帮助解释两种表示与直接有限差分方法之间观察到的差异。时间积分器的比较进一步考察时间离散的影响。在这些比较之外，我们利用半离散系统的一条守恒律构造自适应动网格方法，将共享的 $x$ 方向节点运动与物理场演化相耦合。在节点数与时间积分器相同的条件下，该方法在全部四组单孤子与二孤子测试中均降低了两个物理场的最大误差。总体而言，我们的工作将半离散 DLW 系统的可积构造，与对其表示方式和数值实现如何影响计算精度的理解联系起来。通过结合半离散模型的构造、误差分析与自适应数值方法，我们展示了离散可积系统的构造如何为理解和改进非线性波的数值逼近作出贡献。

**关键词：** 色散长波方程；半离散化；Gram 行列式；Darboux–Lax 表示；连续极限；自适应动网格

## 1. 引言 {#zh-intro}

浅水中波的传播与相互作用长期以来受到非线性波研究的关注。在波的演化过程中，非线性效应与色散以不同方式影响波形，而二者的平衡能够支持在传播中持续存在的相干波。非线性长波方程以约化形式描述这些效应，使我们能够研究波动，而不必保留底层流体方程的全部复杂性。在这类方程中，可积模型因其提供的解析认识而持续受到关注。其精确解使我们能够追踪单个波的演化并考察波间相互作用，双线性形式与 Lax 表示则揭示了这些解背后的数学结构。这些解析结果也为数值研究提供了有用参照，其中波形及其演化需要在离散网格上表示。从连续模型转向这一表示时，所作的选择既影响波的逼近，也影响所得方程的数学结构。可积离散化旨在保留这两方面的联系，将离散方程的构造与其精确解及连续极限的研究结合起来。

（2+1）维色散长波（DLW）系统将色散长波方程推广到两个空间维度 [1]，并被用于研究宽水道及有限深外海中的波动 [3,4]。自 Boiti、Leon 与 Pempinelli 提出这一系统以来，研究者通过若干相互关联的解析方法研究其波解。最初的工作建立了逆谱变换、Bäcklund 变换及叠加公式 [1]；随后发展的非线性变换 [2] 与双线性方法 [3]，为生成解和理解解之间的联系提供了进一步的途径。行列式表示使这些联系具有了具体的表达形式。Hu、Xu 与 Yu 构造了 Grammian 和 Wronskian 解 [4]，而 Sheng 与 Yu 通过 KP 层级约化，得到了描述常值与周期背景上孤子、线呼吸子及有理波的 Gram 行列式解 [5]。

这些解所满足的双线性关系，也为引入格点提供了出发点 [15]。在这一思路下，Bäcklund 变换将相邻格点上的取值联系起来，使离散方程能够与其解结构一同构造。这一方法已用于半离散孤子方程 [7]，并推广到具有两个空间维度的系统 [8]。对于 DLW 系统，它与（2+1）维 sinh-Gordon 方程之间的双线性关系 [5] 又提供了一条联系：后者的可积离散化具有行列式解及 Bäcklund–Lax 结构 [6]。结合已有的离散 DLW 系统研究 [11]，这些进展促使我们进一步考察，如何将连续 DLW 解族引入空间格点，以及由此得到的波场与连续波场之间有怎样的对应关系。

随着这些进展，我们有望在同一构造中研究可积结构的保留与连续波的逼近。带着这一考虑，我们提出如下问题：如何引入空间格点，使其保留双线性与行列式结构，支持一致的物理场重构，并允许对其精确解与连续系统精确解进行定量比较？

为回答这一问题，我们寻求 DLW 系统的一种半离散描述。首先，这一构造应保留显式波解与支配其演化的可积结构之间的联系。Gram 行列式解使离散波场便于解析研究，而相应的 Lax 表示应通过其相容条件恢复同一非线性方程。其次，我们希望理解格点如何改变连续波场。这需要对相应的精确解进行定量比较，从而补充极限下连续方程恢复所提供的信息。精确波场的比较也为研究数值逼近提供了基础。当半离散系统用于计算时，非线性表示、时间积分器及网格的选择都会影响波形的计算精度。因此，我们希望通过与精确解的比较，理解这些选择所产生的影响。

在第 2 节，我们从 Sheng 与 Yu [5] 的连续双线性形式及 Gram 行列式解出发，构造半离散 DLW 系统。通过将 $y$ 方向的交错格点与双线性参数的平移相耦合，行列式解得以推广至半离散情形。这一构造导出 PE 与 PF 两种表示及其 Darboux–Lax 表示。随后，我们考察方程及精确物理场如何趋于其连续对应形式，在所述假设下建立二阶相容性与收敛性，并推导物理场误差的显式首项系数。在这些解析结果的基础上，第 3 节介绍空间离散、基于守恒律的自适应动网格方法及时间积分格式。通过四组单孤子与二孤子算例，我们将两种非线性表示与直接有限差分方法进行比较，并考察时间积分与网格自适应的影响。空间误差分析帮助解释不同空间离散之间的精度差异。对于自适应网格，我们通过固定节点数下的比较，考察节点重新分配如何影响所计算波场的精度。最后，第 4 节汇总主要研究结果，并讨论解析结果与数值结果之间的联系。

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

为导出物理场方程，我们引入对数变量 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。通过这些变量，我们可以将双线性方程展开为重构公式中所涉及的导数。将方程组 (9) 的两式分别除以 $F_jG_j$ 和 $F_jG_{j+1}$，得到

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

这一对称形式启发我们对方程组 (19) 取和与差。在进一步关于 $x$ 求导后，和式产生 $u_{j,t}$，差式产生 $\omega_{j,t}$。其中，平方项与一阶导数项可以通过公式 (20) 写成 $u_j,\omega_j$ 的形式。不过，和式中的二阶导数项仍保留了对数变量的另一种组合。为集中表示这一部分，我们引入

<a id="zh-eq-30"></a>

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{21}$$

随后，对 $A_j+C_j=0$ 与 $A_j-C_j=0$ 分别关于 $x$ 求导，并代入公式 (20)–(21)，便得到

<a id="zh-eq-31"></a>

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{22}$$

第二条方程已经完全由 $u_j,\omega_j$ 表示，而第一条方程仍包含 $Z_j$。为得到完整的非线性表示，我们利用重构关系，以两种方式处理这一剩余项。首先，我们通过格点差分消去 $Z_j$；随后，再构造另一种保留势变量的表示，使 $Z_j$ 与 $\omega_j$ 均可由该势变量表达。

对于第一种表示，我们希望得到仅涉及 $u_j,\omega_j$ 的方程。虽然 $Z_j$ 包含无法在这两个变量中单独体现的对数导数，但它在相邻格点之间的差可以直接由二者表示。因此，我们引入后向差分算子与平均算子

<a id="zh-eq-32"></a>

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad \mathcal M_-z_j=\frac{z_j+z_{j-1}}2.\tag{23}$$

由 $u_j$ 与 $Z_j$ 的定义，我们有 $Z_j-u_j=2(\beta_j+\beta_{j+1})_x$。对此取后向差分，再利用 $\omega_j=(\beta_{j+1}-\beta_j)_x$，得到

<a id="zh-eq-33"></a>

$$\begin{aligned}\delta_-Z_j&=\delta_-u_j+\frac2h(\beta_{j+1}-\beta_{j-1})_x\\&=\delta_-u_j+\frac2h(\omega_j+\omega_{j-1})\\&=\delta_-u_j+\frac4h\mathcal M_-\omega_j.\end{aligned}\tag{24}$$

这一恒等式使我们能够在对方程组 (22) 的第一式施加 $\delta_-$ 后消去 $Z_j$。保持第二式不变，我们便得到势消去表示（PE）：

<a id="zh-eq-34"></a>

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4h\mathcal M_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{25}$$

这样，我们通过精确的格点恒等式消去了辅助量 $Z_j$，没有引入额外近似。所得方程涉及 $u_j,\omega_j$，物理场 $v_j$ 则通过公式 (18) 恢复。消去操作也使 $u_{j,t}$ 以其后向差分的形式出现，因此，要恢复各格点上的时间导数，需要给定格点方向上的一个边界值或等价的归一化条件。这一特点将在 PE 的数值实现中体现。

接下来，我们构造一种保留 τ 函数中势信息的表示。在这一表示中，我们希望用同一个变量表达 $Z_j$ 与 $\omega_j$，从而无需对方程组 (22) 的第一式取格点差分。为此，我们引入 $M_j=\beta_{j,x}$。由重构关系可得

<a id="zh-eq-35"></a>

$$\begin{aligned}\omega_j&=(\beta_{j+1}-\beta_j)_x=M_{j+1}-M_j,\\Z_j&=(2\alpha_j+\beta_j+\beta_{j+1})_x\\&=(2\alpha_j-\beta_j-\beta_{j+1})_x+2(\beta_j+\beta_{j+1})_x\\&=u_j+2(M_j+M_{j+1}).\end{aligned}\tag{26}$$

因此，相邻势值之差决定了 $\omega_j$，而它们的和则给出 $Z_j$ 中除 $u_j$ 之外的部分。

将公式 (26) 代入方程组 (22) 的第一式后，我们发现其 $x$ 导数内部包含组合 $u_{j,x}+u_j^2/2$。这启发我们引入一个变量，使其对数导数给出 $u_j$。根据 τ 函数重构关系，我们定义

<a id="zh-eq-36"></a>

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{27}$$

通过这一选取，导数项与平方项可合并为

<a id="zh-eq-37"></a>

$$u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{28}$$

为得到 $Q_j$ 的演化方程，我们回到尚未关于 $x$ 求导的关系 $(A_j+C_j)/2=0$。这样可以保留由 τ 函数确定的归一化，而不必引入积分函数。代入公式 (26)–(27)，便得到

<a id="zh-eq-38"></a>

$$\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j=0.\tag{29}$$

至此，我们已将第一条演化关系写成由 $Q_j$、相邻势值及其差 $\omega_j$ 表示的形式。为完成这一表示，我们转向 $\omega_j$ 的方程。将 $u_j=2Q_{j,x}/Q_j$ 代入其通量，得到

<a id="zh-eq-39"></a>

$$(u_j+2a)\omega_j-hu_j=2a\omega_j+2\frac{Q_{j,x}}{Q_j}(\omega_j-h).\tag{30}$$

其中最后一项将 $Q_j$ 的对数导数与 $\omega_j-h$ 联系起来。我们引入配对变量 $R_j$，将这一组合纳入新的变量表示：

<a id="zh-eq-40"></a>

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad \omega_j=h(1-Q_jR_j).\tag{31}$$

由于正 τ 函数保证 $Q_j>0$，这一定义在所考虑区域内是良好定义的。同时，它也通过以下恒等式简化了公式 (29) 中的二次项：

<a id="zh-eq-41"></a>

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{32}$$

利用公式 (31)–(32)，我们将 $\omega_j$ 方程改写为乘积 $Q_jR_j$ 的演化方程：

<a id="zh-eq-42"></a>

$$(Q_jR_j)_t-(Q_jR_j)_{xx}+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x=0.\tag{33}$$

其中的二阶导数项满足

<a id="zh-eq-43"></a>

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{34}$$

因此，我们可以展开公式 (33) 中的时间导数，并利用公式 (29) 消去 $Q_{j,t}$，再除以 $Q_j$，得到 $R_j$ 的演化方程。另一方面，公式 (26) 与 (31) 给出的两种 $\omega_j$ 表达共同确定了一个格点约束，将 $M_j$ 与 $Q_jR_j$ 联系起来。

汇集这些关系，我们便得到势表示（PF）：

<a id="zh-eq-44"></a>

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{35}$$

其中，$Q_j,R_j$ 位于半格点 $y=(j+\tfrac12)h$，而 $M_j$ 位于整数格点 $y=jh$。前两条方程描述 $Q_j,R_j$ 的演化，第三条则将二者的乘积与相邻势值之差联系起来。物理场通过下式恢复：

<a id="zh-eq-45"></a>

$$u_j=2\frac{Q_{j,x}}{Q_j},\qquad v_j=4(1-Q_jR_j)+\delta_0u_j.\tag{36}$$

通过对辅助势采取不同的处理方式，我们得到了两种非线性表示。为明确二者之间的关系，我们比较它们从同一组 τ 函数重构出的物理场。下面的命题说明，这种一致性在每个固定格距下就已经成立，无需先取连续极限。

**命题 2.6（共同物理场）。** 设 $h>0$，且充分光滑的正 τ 函数 $F_j,G_j$ 满足半离散双线性系统 [(9)](#zh-eq-9)。通过公式 (18) 定义 $u_j,\omega_j,v_j$，并分别通过公式 (27)、(31) 及 $M_j=\partial_x\log G_j$ 定义 $Q_j,R_j,M_j$。则 PE 重构公式 (18) 与 PF 重构公式 (36) 给出完全相同的物理场 $u_j,v_j$。

**证明。** 由定义有

<a id="zh-eq-46"></a>

$$2\frac{Q_{j,x}}{Q_j}=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}=u_j,\qquad 4(1-Q_jR_j)=\frac4h\omega_j.\tag{37}$$

在第二个等式两侧加上相同的 u 中心差分，即得两种重构的 v 也一致。□

这一一致性使我们能够采用同一组重构精确场，作为两种表示的共同参照。不过，它并不意味着二者的数值近似也会相同：后续的 $x$ 方向与时间离散作用于不同的因变量及不同形式的演化方程。我们将在第 3 节考察这些影响。在此之前，我们先建立半离散方程及其精确波场在 $h\to0$ 时与连续 DLW 系统之间的联系。

### 2.5 连续极限 {#zh-limits}

在建立半离散方程及其精确解之后，我们进一步考察它们在格点间距趋于零时如何逼近连续 DLW 系统。我们希望明确格点如何改变精确波场，以及连续方程如何从离散关系中恢复。首先，我们导出半离散与连续 Gram 解之差的展开，并给出其首项系数；重构物理场的二阶收敛由此直接得到。随后，我们考察非线性方程的相容性。

本小节中，$O_K(h^m)$ 表示在紧集 $K$ 上由 $C_Kh^m$ 一致控制的余项，其中 $C_K$ 与 $h$ 无关。我们假设函数在 $K$ 的一个开邻域内充分光滑。使用展开式的导数时，余项估计也适用于所需导数。

我们首先比较精确解族中相互对应的成员。为在同一物理位置进行比较，我们将格点 τ 函数延拓到连续坐标 $y$，并保留交错重构。对于正函数 $f_h,g_h$，定义

<a id="zh-eq-47"></a>

$$\begin{aligned}U_h(y)&=\partial_x[2\log f_h(y)-\log g_h(y-h/2)-\log g_h(y+h/2)],\\\Omega_h(y)&=\partial_x[\log g_h(y+h/2)-\log g_h(y-h/2)],\\V_h(y)&=\frac4h\Omega_h(y)+\frac{U_h(y+h)-U_h(y-h)}{2h}.\end{aligned}\tag{38}$$

这里及下文在表示 $y$ 方向平移时，省略共同的变量 $x,t$。在 $y=(j+\tfrac12)h$ 处，这些表达式与格点重构公式 (18) 一致。

**定理 2.7（精确波场的误差首项与收敛性）。** 固定行列式阶数 $N$，并选取满足下列条件的实谱参数，其中 $h_0>0$：

<a id="zh-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{39}$$

设 $f,g$ 为公式 (5) 中的连续 Gram τ 函数，$u,v$ 为通过公式 (2) 定义的物理场。对于 $0<h\le h_0$，将正格点因子延拓到实数次幂，并令

<a id="zh-eq-60"></a>

$$g_h(x,y,t)=\tau_0(y/h),\qquad f_h(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{40}$$

设 $U_h,V_h$ 为上述交错重构得到的物理场。记 $\alpha=\log f$、$\beta=\log g$、$z_i=p_i-a$、$w_i=q_i+a$，并定义

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,$$

$$\alpha_2=\sum_{i=1}^{N}(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_{i=1}^{N}c_i\rho_i\partial_{\rho_i}\beta.$$

则在任意紧集 $K$ 上，一致地有

<a id="zh-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{41}$$

因此，对于充分小的 $h>0$，有

<a id="zh-eq-61"></a>

$$\sup_K\bigl(|U_h-u|+|V_h-v|\bigr)\le C_Kh^2\tag{42}$$

这一展开同时适用于通过 PE 与 PF 重构的物理场。

**证明。** 我们保持谱参数固定，首先展开格点因子：

<a id="zh-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{43}$$

对于各行列式元素，格点相位中 $y$ 的系数因而满足

<a id="zh-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{44}$$

在 $f_h$ 中，半格点位移还与辅助参数的平移相结合，得到如下振幅因子：

<a id="zh-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}\left[1+\frac{h^2}{8}\left(\frac1{w_k^2}-\frac1{z_i^2}\right)+O(h^4)\right].\end{aligned}\tag{45}$$

因此，相位与中心化振幅相对于连续形式的差异均从 $h^2$ 阶开始。

为确定行列式中的系数，我们采用主子式展开。每个主子式的行与列使用同一个指标集 $\mathcal I$，其相位修正为 $h^2y\sum_{i\in\mathcal I}c_i$，而 $f_h$ 的额外振幅修正为 $h^2\sum_{i\in\mathcal I}d_i$。算子 $\rho_i\partial_{\rho_i}$ 恰好选出包含指标 $i$ 的主子式。先展开行列式，再展开其对数，得到

$$\log f_h=\alpha+h^2\alpha_2+O_K(h^4),\qquad \log g_h=\beta+h^2\beta_2+O_K(h^4).$$

所述谱条件保证连续 τ 函数及其实数次幂延拓为正。由于 $N$ 和谱参数保持固定，这些展开连同下面所需的导数在紧集上一致成立。

接下来，我们将对数展开代入交错重构。围绕物理位置 $y$ 作对称 Taylor 展开，得到

$$U_h=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4).$$

对于第二个物理场，相应的展开为

$$\frac4h\Omega_h=4\beta_{xy}+h^2\left[4(\beta_2)_{xy}+\frac16\beta_{xyyy}\right]+O_K(h^4),$$

$$\begin{aligned}\frac{U_h(y+h)-U_h(y-h)}{2h}={}&u_y+h^2\left[2(\alpha_2-\beta_2)_{xy}-\frac14\beta_{xyyy}+\frac16u_{yyy}\right]+O_K(h^4).\end{aligned}$$

将二者相加，得到

$$V_h=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).$$

最后，连续重构关系给出 $4\beta_{xy}=v-u_y$。在两个物理场展开中使用这一恒等式，即得所述系数 $C_U,C_V$。它们在 $K$ 上有界，因此得到二阶收敛估计。由于 PE 与 PF 从同一组 τ 函数重构出相同的物理场，结论对两种表示均成立。□

通过这一展开，我们可以描述格点间距较小但非零时，$y$ 方向离散如何改变重构波场。系数 $C_U,C_V$ 分别刻画两个物理场差异首项的空间分布。含 $\alpha_2,\beta_2$ 的项来自行列式解本身的变化，其余项则来自交错重构。在所述假设下，这些系数在紧集上有界。因此，这一展开直接蕴含：当 $h\to0$ 时，两个重构物理场均在紧集上以二阶精度一致收敛到相应的连续 DLW 物理场。

现在，我们转向非线性方程。为用物理变量表达其连续极限，我们引入

<a id="zh-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{46}$$

PE 方程于是写为

<a id="zh-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{47}$$

令 $\mathcal M_+z_j=(z_{j+1}+z_j)/2$。恒等式 $\mathcal M_+\delta_-=\delta_0$ 表明，$\mathcal M_+E_{1,h,j}+E_{2,h,j}$ 中的时间导数为 $v_{j,t}$。因此，我们将这一组合与连续 DLW 系统的第二式进行比较。

**命题 2.8（方程的相容性）。** 在 $y_j=(j+\tfrac12)h$ 处对充分光滑的物理场 $u,v$ 取样，并定义连续残差

<a id="zh-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{48}$$

则在紧集上一致地有

<a id="zh-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{49}$$

**证明。** 记 $m_j=y_j-h/2$。围绕差分与平均算子各自的中心展开，得到

<a id="zh-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{50}$$

因此，

<a id="zh-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{51}$$

这些展开在所需的求导后仍成立。代入第一条残差，得到 $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$。

对于第二条残差，记 $w=v-u_y$，可得

<a id="zh-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{52}$$

将第一条残差关于 $y_j$ 作平均，再与第二条相加，得到

<a id="zh-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{53}$$

这里，所有连续物理场均在 $y_j$ 处取值。第二个结论得证。□

连续极限分析表明，所构造的格点系统与连续 DLW 模型保持着可定量描述的联系。我们建立了格点方程对连续方程的二阶相容性，并对本节考察的精确解族，得到了两个物理场在紧集上的二阶一致收敛。在有限格距下，系数 $C_U,C_V$ 进一步刻画了这种逼近：它们描述各物理场差异的首项，以及这一差异在波形中的空间变化。因此，我们能够直接通过重构物理场评估 $y$ 方向离散的影响。由于 PE 与 PF 从同一组 τ 函数得到相同的物理场，上述误差展开及其系数同时适用于两种表示。

### 2.6 Darboux–Lax 表示 {#zh-lax}

前面的分析建立了半离散系统与连续 DLW 方程之间的联系。现在，我们回到有限格距下的格点系统本身，寻求一个辅助线性问题，使其相容条件能够恢复非线性演化。通过这一表示，我们可以将物理场方程与两种操作之间的一致性联系起来：波函数在相邻格点之间的传递，以及它随时间的演化。

为建立这一表示，我们首先用平移后的场变量改写 PE 方程，并引入辅助势。随后，我们构造波函数的格点关系与时间演化方程，建立它们与非线性系统之间的相容关系。对于 τ 函数解，我们进一步说明所需的辅助势及 Darboux 关系如何由双线性方程得到。最后，我们用 $Q_j,R_j,M_j$ 表达同一个线性问题，明确它与 PF 表示之间的联系。

我们首先通过以下变量平移，将 PE 方程中的常数项吸收到新变量中：

<a id="zh-eq-69"></a>

$$U_j=u_j+2a,\qquad w_j=\frac4h\omega_j-4.\tag{54}$$

这样，第二条方程的通量变为与 $U_jw_j$ 成正比的形式，而第一条方程则以 $U_j,w_j$ 的二次项表示。将公式 (54) 代入 (25)，便得到

<a id="zh-eq-70"></a>

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+\mathcal M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{55}$$

为构造辅助线性问题，我们通过辅助势 $V_j$ 的 $x$ 导数及其在相邻格点之间的变化来定义它：

<a id="zh-eq-71"></a>

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{56}$$

这两条关系必须给出相同的 $V_{j+1,x}-V_{j,x}$。为检验这一点，我们对第一条关系取相邻格点之差，再与第二条关系的 $x$ 导数进行比较。二者一致的条件，恰好是相应格点指标处的方程组 (55) 的第一式。

因此，当非线性方程成立时，我们可以局部构造 $V_j$。首先，在一个参考格点处对给定的 $x$ 导数积分；随后，利用格点关系确定相邻位置的 $V_j$。刚才建立的相容性保证了这些递推得到的值在每个格点处都满足规定的 $x$ 导数关系。剩余的自由度是一个所有格点共有的时间函数。

在确定辅助势之后，我们引入波函数 $\psi_j(x,t)$，并考虑线性系统

<a id="zh-eq-72"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{57}$$

第一条方程通过两个关于 $x$ 的一阶微分算子联系相邻格点上的波函数，第二条则规定各格点处波函数的时间演化。我们要求这两种关系在时间演化过程中保持一致：先将波函数传递到下一个格点，再进行时间演化，应与先演化、再应用格点关系得到相同的结果。

为表达这一要求，我们定义

$$\mathscr A_j=\partial_x-\frac{U_j}{2}-\frac{hw_j}{8},\qquad \mathscr B_j=\partial_x-\frac{U_j}{2}+\frac{hw_j}{8},$$

并引入形式格点传递算子与时间演化算子

$$T_j=\mathscr B_j^{-1}\mathscr A_j,\qquad H_j=-\partial_x^2-V_j.$$

线性系统于是写为 $\psi_{j+1}=T_j\psi_j$ 与 $\psi_{j,t}=H_j\psi_j$，其相容性由算子恒等式

$$T_{j,t}=H_{j+1}T_j-T_jH_j$$

表达。这里，$\mathscr B_j^{-1}$ 按形式伪微分逆算子理解。下面的定理建立这一算子恒等式与非线性场方程之间的联系。

**定理 2.9（Darboux–Lax 相容性）。** 系统 [(55)](#zh-eq-70) 的每个光滑解，连同 [(56)](#zh-eq-71) 确定的辅助势，都使 [(57)](#zh-eq-72) 在形式算子意义下相容。反之，在 $w_j\ne0$ 的区域内，相容条件与辅助势的格点差关系共同推出 [(55)](#zh-eq-70)。

**证明。** 将格点转移分解为 $T_j=\mathscr B_j^{-1}\mathscr A_j$，其中 $\mathscr A_j=\partial_x-U_j/2-hw_j/8$、$\mathscr B_j=\partial_x-U_j/2+hw_j/8$。场方程使两个标量 Darboux 残差均为零，并给出共同的中间势，从而 $T_{j,t}=H_{j+1}T_j-T_jH_j$。反之，零阶与负一阶系数在 $w_j\ne0$ 时迫使两残差为零，其和与差恢复场方程。算子恒等式见[附录 C](#zh-app-c)。□

对于由 τ 函数构造的解，我们可以直接用 $F_j,G_j$ 表达辅助势与 Darboux 系数。利用重构公式，便得到

<a id="zh-eq-83"></a>

$$V_j=2(\log G_j)_{xx},\qquad r_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad s_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{58}$$

其中，$r_j,s_j$ 的表达式分别与 $U_j/2+hw_j/8$、$U_j/2-hw_j/8$ 一致。辅助势也满足所需的格点关系，因为

$$V_{j+1}-V_j=2\partial_x^2\log\frac{G_{j+1}}{G_j}=2\omega_{j,x}=\frac h2w_{j,x}.$$

随后，我们回到公式 (19) 中归一化后的双线性方程。对它们关于 $x$ 求导，并代入公式 (58)，第一式给出 $\mathcal E_j^r=0$，第二式给出 $\mathcal E_j^s=0$。二者之和还恢复了公式 (56) 中规定的 $V_{j,x}$ 表达式。因此，用于构造精确物理场的双线性方程，同时提供了建立 Darboux–Lax 表示所需的关系。特别地，第 2.3 节的 Gram 行列式解在 τ 函数为正的区域内满足这些相容关系。

最后，我们用 PF 中的势变量表达这一线性系统。根据重构关系，有

<a id="zh-eq-84"></a>

$$U_j=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\qquad V_j=2M_{j,x}.\tag{59}$$

将这些表达式代入 (57)，便得到

<a id="zh-eq-85"></a>

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{60}$$

公式 (60) 给出了 PF 变量下的 Darboux–Lax 系统。前面使用的辅助势关系也包含在 PF 的格点约束中，对该约束关于 $x$ 求导，即得

<a id="zh-eq-86"></a>

$$V_{j+1}-V_j=2(M_{j+1}-M_j)_x=-2h(Q_jR_j)_x=\frac h2w_{j,x}.\tag{61}$$

通过 Darboux–Lax 表示，我们将非线性场方程理解为格点传递与时间演化保持一致所需的条件。我们用辅助波函数的线性方程描述这两种操作，并在相容性定理的条件下，通过要求二者一致来恢复非线性系统。这使我们能够在有限格距下考察方程的可积结构。通过分别用 PE 与 PF 变量表达同一个线性问题，我们也说明了两种表示虽然对势变量采取不同的处理方式，却保留了这一共同结构。

由此，我们将格点方程的构造与其精确解及 Darboux–Lax 表示联系起来。从连续双线性关系出发，我们得到了一个物理场可以显式重构、并能与连续 DLW 解进行定量比较的半离散系统。这些精确物理场也使我们能够评估将非线性方程用于实际计算时的情况。尽管 PE 与 PF 在解析层面重构出相同的物理场，它们的数值实现却推进不同的变量，并在 $x$ 与 $t$ 方向引入进一步的近似。有了精确解及 $y$ 方向离散误差作为参照，我们便可以考察这些选择如何影响计算所得物理场的精度。

## 3. 数值方法与实验 {#zh-numerics}

本节中，我们建立半离散 DLW 系统的数值方法，并考察其非线性表示与数值实现如何影响计算精度。在第 3.1 节，我们离散 PE 与 PF 中剩余的 $x$ 方向导数，并引入连续系统的直接有限差分近似作为比较。我们还推导空间误差首项，以帮助解释这些近似的精度。在第 3.2 节，我们利用半离散守恒律构造自适应动网格方法（SAMM），将共享的 $x$ 方向节点运动与物理场演化相耦合。在第 3.3 节，我们介绍所得系统的时间积分，包括物理场与网格的耦合方程。在第 3.4 节，我们引入四组单孤子与二孤子算例，并定义误差度量。在第 3.5 节，我们比较数值结果，并结合空间误差分析，讨论非线性表示、时间积分器与网格选择如何影响两个物理场的计算精度。

### 3.1 空间离散 {#zh-schemes}

为进行数值比较，我们对 PE、PF 及连续 DLW 系统的直接有限差分近似（记为 FD）统一采用相同的 $x$ 向中心差分。由此，我们在共同的空间离散下考察不同表示的计算表现。

**网格与差分算子。** 在固定网格上，取 $x_i=-L/2+i\Delta x$，其中 $\Delta x=L/N_x$。沿 y 方向，$M_j$ 位于 $y=jh$，而 $u_j,v_j,Q_j,R_j$ 位于 $y=(j+\tfrac12)h$。下标 j、i 分别表示 y 层与 x 节点。以下空间离散系统保留时间为连续变量。

对 x 导数采用三点中心差分

<a id="zh-eq-87"></a>

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{62}$$

对于光滑函数，中心差分满足

<a id="zh-eq-202"></a>

$$D_1f=f_x+\frac{(\Delta x)^2}{6}f_{xxx}+O((\Delta x)^4),\qquad D_2f=f_{xx}+\frac{(\Delta x)^2}{12}f_{xxxx}+O((\Delta x)^4).\tag{63}$$

$D_2$ 是独立的三点二阶导数模板，不等于 $D_1^2$。

沿 y 方向采用

<a id="zh-eq-88"></a>

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\quad \delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\quad \mathcal M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.\tag{64}$$

其中，$D_1,D_2$ 作用于 x 节点编号，$\delta_-,\delta_0,\mathcal M_-$ 作用于层编号。下文的乘积与商均按节点计算。我们先构造 PE 和 PF 格式，再给出作为比较对象的直接差分格式，记为 FD。

**PE 格式。** 取 $P=\delta_-u$ 和 $W=v-\delta_0u$ 为演化变量。由下边界值及 P 的累积和确定 u，再令 $v=W+\delta_0u$，见[附录 D](#zh-app-d)。演化方程为 $\dot P=F_P$、$\dot W=F_W$，其中

<a id="zh-eq-90"></a>

$$\begin{aligned}
F_P={}&-\delta_-D_1\left[\frac{u^2}{2}+2au
+h^2\left(\frac{W^2}{32}-\frac{W}{4}\right)\right]
-D_2(P+\mathcal M_-W),\\
F_W={}&-D_1[(u+2a)W-4u]+D_2W.
\end{aligned}\tag{65}$$

因此，计算演化右端时，先由 P 恢复 u，再对 u、W 施加相应的空间差分算子；物理场 v 由同一重构公式得到。

**PF 格式。** 取 Q、R 为演化变量，物理场由

<a id="zh-eq-91"></a>

$$u_j=2\frac{D_1Q_j}{Q_j},\qquad
v_j=4(1-Q_jR_j)+\delta_0u_j\tag{66}$$

恢复。其中 $m_j\simeq M_{j,x}$ 由格点约束和下边界数据确定，详见附录 D。最终演化右端为

<a id="zh-eq-94"></a>

$$\begin{aligned}
F_{Q,j}={}&-D_2Q_j-2aD_1Q_j
-\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]Q_j,\\
F_{R,j}={}&D_2R_j-2aD_1R_j
+\left[m_j+m_{j+1}+\frac{h^2}{4}\bigl((Q_jR_j)^2-1\bigr)\right]R_j.
\end{aligned}\tag{67}$$

Q 的最下层取给定边界值，内部各层 Q 和所有层 R 按上述方程演化。随后通过式 (66) 恢复物理场。

**FD 格式。** 作为比较，直接离散连续 DLW 方程，取 $P=\delta_-u$ 和 v 为演化变量。物理场 u 由式 (106) 的第一个关系从 P 恢复。所得系统为 $\dot P=F_P$、$\dot v=F_v$，其中

<a id="zh-eq-95"></a>

$$\begin{aligned}
F_P&=-\delta_-D_1\left[\frac{u^2}{2}+2au\right]-D_2\mathcal M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{68}$$


**x 向离散误差的首项。** 我们考察 $x$ 向中心差分如何影响 PE 和 FD 对 $u_t$ 的近似。在固定有限 $y$ 区间上的同一光滑场及给定的 $y=b$ 下边界变化率下，两种格式均具有首项贡献

<a id="zh-eq-203"></a>

$$r^u_{x,m}=(\Delta x)^2B+O\!\left((\Delta x)^4+(\Delta x)^2h^2\right),\qquad m=\mathrm{PE},\mathrm{FD}.\tag{69}$$

其系数为

<a id="zh-eq-204"></a>

$$\boxed{B=-\frac16\partial_x^3\left[\frac{u(x,y,t)^2-u(x,b,t)^2}{2}+2a\bigl(u(x,y,t)-u(x,b,t)\bigr)\right]-\frac1{12}\partial_x^4\int_b^y v(x,s,t)\,ds.}\tag{70}$$

这里，$r^u_{x,m}$ 比较同一 $y$ 离散状态上内部 $x$ 节点处的中心差分与精确 $x$ 导数。因此，$B$ 刻画了共同 $x$ 向差分模板所引入误差的首项空间分布。

*推导。* 我们从 $P$ 方程出发，即 PE 的 (65) 和 FD 的 (68) 中的 $\dot P=F_P$。由 $P_r=(u_r-u_{r-1})/h$，从下边界层 $\ell$ 起累加可得
$$F^u_{m,j}=u_t(x,b,t)+h\sum_{r=\ell+1}^{j}F_{P,m,r}.$$
对于 FD，第一项相消为端点差，第二项形成梯形求和：
$$F^u_{\mathrm{FD},j}=u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)\right]
-D_2\left[\frac h2\sum_{r=\ell+1}^{j}(v_r+v_{r-1})\right].$$
应用中心差分展开 (63)，并将梯形和写为 $\int_b^y v\,ds+O(h^2)$，即得到系数 (70)。对于所考虑的光滑场，求积余项相应的 $x$ 导数也为 $O(h^2)$。

对于 PE，同样的累加给出
$$\begin{aligned}
F^u_{\mathrm{PE},j}={}&u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)
+h^2\left(\frac{W_j^2-W_\ell^2}{32}-\frac{W_j-W_\ell}{4}\right)\right]\\
&-D_2\left[u_j-u_\ell+\frac h2\sum_{r=\ell+1}^{j}(W_r+W_{r-1})\right].
\end{aligned}$$
其中 $W=v-\delta_0u=v-u_y+O(h^2)$。$u_y$ 的积分抵消端点差 $u_j-u_\ell$，从而在首阶留下相同的 $v$ 积分；额外通量项则显式带有因子 $h^2$。再次应用 (63)，得到

<a id="zh-eq-205"></a>

$$\begin{gathered}
r^u_{x,\mathrm{PE}}=(\Delta x)^2B_{h,\mathrm{PE}}+O((\Delta x)^4),\qquad
r^u_{x,\mathrm{FD}}=(\Delta x)^2B_{h,\mathrm{FD}}+O((\Delta x)^4),\\
B_{h,\mathrm{PE}}=B+O(h^2),\qquad B_{h,\mathrm{FD}}=B+O(h^2),\qquad
B_{h,\mathrm{PE}}-B_{h,\mathrm{FD}}=O(h^2).
\end{gathered}\tag{71}$$

这里的 $O(h^2)$ 差异指乘在 $(\Delta x)^2$ 前的系数差，因此相应 $x$ 向首项误差的差异为 $O((\Delta x)^2h^2)$。这些表达式为后文解释 PE 与 FD 的数值结果提供了共同参照。

上述三种空间格式与第 3.3 节的时间积分器结合使用，初值和边界数据见第 3.4 节。

### 3.2 自适应动网格方法 {#zh-samm}

均匀网格可能在变化缓慢的区域分配较多节点，却难以充分分辨狭窄波带。动网格方法通过依赖于解的密度重新分配节点，以改善这种不均衡 [14]。对于可积方程，守恒律提供了解与网格之间的直接联系，相关实例包括 Camassa–Holm 方程 [12]、短脉冲方程 [13] 及广义 sine-Gordon 方程 [9] 的自适应方法。在当前二维情形下，我们保留均匀的 $y$ 格点，并在各横向层共享同一组移动的 $x$ 节点。因此，我们对守恒密度与通量作横向平均，以确定共享的节点分布。这一做法在保持物理场张量积表示的同时，调整 $x$ 方向的分辨率。

为了使密度随物理场演化，我们利用 $W$ 方程的守恒形式，
$$W_t+\bigl[(u+2a)W-4u\bigr]_x-W_{xx}=0.$$
取 $\rho=1-W/4$ 后，非线性通量写为
$$ (u+2a)W-4u=8a-4(u+2a)\rho.$$
这一选择直接产生 $\rho$ 的守恒律，且零场背景对应 $\rho=1$。我们将通量归一化为在该背景上为零，从而得到

<a id="zh-eq-96"></a>

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.\tag{72}$$

将 $W_j=4(1-\rho_j)$ 代入其演化方程，得到

<a id="zh-eq-97"></a>

$$\partial_t\rho_j+\partial_xq_j=0.\tag{73}$$

在 PF 中，$\rho_j=Q_jR_j$。由于所有 $y$ 层共享同一组 $x$ 节点，我们利用横向平均的密度与通量确定网格运动，即

<a id="zh-eq-98"></a>

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{74}$$

初始节点按 $\bar\rho(x,0)$ 的累积积分等分，使相邻节点之间的密度积分相同，从而在密度较大的区域分配更多节点。演化过程中，每个节点对应的累积密度积分保持不变，节点运动由此与物理场的演化相联系。固定左端点 $x_L$，由守恒律[(73)](#zh-eq-97)得到

<a id="zh-eq-99"></a>

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.\tag{75}$$

因此节点速度为

<a id="zh-eq-100"></a>

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{76}$$

数值计算通量时，我们以 $D_1\rho$ 近似 $\partial_x\rho$。网格演化要求 $\bar\rho>0$，而映射 Jacobian 为正则保证节点顺序不变。在这一动网格上，空间导数由[附录 E](#zh-app-e)中的映射中心差分算子计算。随后，我们将场方程
$$\dot z=F_z+\mathcal V D_1z$$
与节点方程 (76) 耦合。附加项计入了取值位置移动所产生的影响；取 $\mathcal V=0$ 即恢复固定网格形式。第 3.3 节介绍这一耦合系统的时间积分。

### 3.3 时间积分 {#zh-time}


完成空间离散后，我们对所得系统进行时间推进。在 PE、PF、FD 的比较以及固定网格与动网格的比较中，统一采用经典四阶 Runge–Kutta 方法（RK4）[10]。保持时间积分器一致，使我们能够在相同的时间推进方式下考察空间表示与网格选择的影响。随后，在固定网格 PE 格式上比较前向 Euler、RK4 与 Crank–Nicolson（C–N），单独考察时间积分的作用。

记 $z$ 为演化变量，则各空间格式写为 $\dot z=\mathcal F(t,z)$。PE 的变量为 $P,W$，PF 的变量为 $Q,R$ 中需要演化的分量，FD 的变量为 $P,v$。每次计算 $\mathcal F$ 时，按照前述重构和边界关系恢复物理场与辅助量。

对于 SAMM，我们将节点坐标纳入状态，与场变量共同推进。相应右端包含带网格输运项的场方程，以及第 3.2 节给出的节点速度。这一耦合使物理场的变化能够在每个时间步内影响网格，而更新后的网格决定空间导数的计算位置。

给定 $t_n$ 时刻的 $z^n$，RK4 各阶段为
$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),\\
K_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_2/2),\\
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t K_3),
\end{aligned}$$
并更新
$$z^{n+1}=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).$$

在每个阶段，我们由阶段变量恢复物理场与辅助量，并在对应的阶段时刻计算给定边界数据。对于 SAMM，阶段节点位置决定映射后的空间算子，密度、通量和节点速度则由同一阶段的场与网格计算。因此，每次调用 $\mathcal F$ 都对应耦合系统中一致的中间状态。

为考察时间积分器的作用，我们保持固定网格 PE 空间离散不变，仅改变时间推进方法。前向 Euler 使用当前右端，
$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n),$$
而 Crank–Nicolson 对时间步两端的右端取平均：
$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
这两种方法分别给出一阶和二阶时间近似，与四阶 RK4 一同用于比较。

Crank–Nicolson 的更新式两侧均含有新状态。我们迭代求解所得非线性方程，并在每次计算右端时恢复物理场、施加边界数据。迭代通过残差
$$\mathcal R(z^{n+1})=z^{n+1}-z^n-\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right]$$
进行监测。迭代过程与停止条件见[附录 F](#zh-app-f)，时间积分器的比较结果见第 3.5.2 节。

对于三种积分器，我们均在比较时刻由数值状态恢复 $u,v$，并相对于同一精确解评价误差。这样便能直接在物理场上考察时间推进方法如何影响所选空间格式的精度。

### 3.4 算例与误差度量 {#zh-tests}

我们采用连续 DLW 系统的四组孤子解，考察数值方法对不同波形的分辨能力。首先考虑两组 $u$ 脉冲符号相反的单孤子解，再考察具有不同波传播取向与极性组合的二孤子解。这样的安排使我们能够先比较各方法对单个波的计算表现，再考察相互作用波中更为丰富的空间结构。各算例均由精确解提供初值和边界数据，并以其作为两个物理场的误差评价基准。以下统一取 $a=2$、行列式系数 $\rho_i=1$，初相位为零。

我们在包含主要波形的区域内考察这些解，并将计算边界设置在更外侧。四组算例的区域分别为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$ 和 $[-30,30]^2$，各数值方法均采用相同的区域。

**单孤子解。** 对于单孤子算例，我们在连续 Gram 行列式中取 $N=1$，得到

<a id="zh-eq-105"></a>

$$f_*=1+cE,\qquad g_*=1+E,\tag{77}$$

其中

<a id="zh-eq-106"></a>

$$\begin{gathered}E=\frac{e^\theta}{p+q},\qquad c=-\frac{p-a}{q+a},\\\theta=kx+(q^2-p^2)t+\ell y,\qquad k=p+q,\qquad \ell=\frac1{p-a}+\frac1{q+a}.\end{gathered}\tag{78}$$

相应的物理场具有显式形式

<a id="zh-eq-107"></a>

$$\begin{aligned}u_*&=\frac{2k(c-1)E}{(1+cE)(1+E)},\\v_*&=2k\ell\left[\frac{cE}{(1+cE)^2}+\frac{E}{(1+E)^2}\right].\end{aligned}\tag{79}$$

这些表达式为参数选择提供了依据。当 $p+q>0$、$c>0$ 时，两个脉冲的符号分别由 $c-1$ 和 $\ell$ 决定。因此，我们选取 $(p,q)=(1,2)$ 和 $(4,-3)$，使第一组算例具有负的 $u$ 脉冲，第二组具有正的 $u$ 脉冲。相应参数分别为 $(c,\ell)=(1/4,-3/4)$ 和 $(2,-1/2)$，因而两组算例的 $v$ 脉冲均为负。

下图展示第一组解在 $t=0$ 时的波形。$u_*$ 和 $v_*$ 均形成斜穿区域的负向波谷，场的变化主要集中在波带的横向。我们由此从较为简单的波形出发，考察各方法对两个物理场中局部脉冲的分辨能力。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_1_2.png" alt="精确波形：单孤子 (1,2)；t=0。左：u；右：v。" loading="lazy"><figcaption>精确波形：单孤子 (1,2)；t=0。左：u；右：v。</figcaption></figure>

采用第二组参数后，$u_*$ 由负向波谷变为正向波脊，而 $v_*$ 仍为负向波谷。与第一组相比，波形的幅值和横向宽度也有所变化。通过这一算例，我们将比较扩展到不同的脉冲形状及相反的 $u_*$ 极性。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_single_4_m3.png" alt="精确波形：单孤子 (4,−3)；t=0。左：u；右：v。" loading="lazy"><figcaption>精确波形：单孤子 (4,−3)；t=0。左：u；右：v。</figcaption></figure>

**二孤子解。** 接下来，我们考虑二孤子解，考察各方法对两个相互作用波所形成空间结构的分辨能力。取 $N=2$ 并展开 Gram 行列式，得到

<a id="zh-eq-108"></a>

$$\begin{aligned}f_*&=1+c_1E_1+c_2E_2+A_{12}c_1c_2E_1E_2,\\g_*&=1+E_1+E_2+A_{12}E_1E_2,\end{aligned}\tag{80}$$

其中

<a id="zh-eq-109"></a>

$$\begin{gathered}E_i=\frac{e^{\theta_i}}{p_i+q_i},\qquad c_i=-\frac{p_i-a}{q_i+a},\\\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+\left(\frac1{p_i-a}+\frac1{q_i+a}\right)y,\qquad i=1,2,\\A_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}.\end{gathered}\tag{81}$$

我们通过 $u_*=2\partial_x\log(f_*/g_*)$ 和 $v_*=2\partial_x\partial_y\log(f_*g_*)$ 恢复物理场。其中，混合项 $E_1E_2$ 纳入两个波之间的相互作用，其系数由谱参数确定。

第一组算例取 $(p_1,q_1)=(6,-5)$、$(p_2,q_2)=(4,-3)$，相应地有 $c_1=4/3$、$c_2=2$、$A_{12}=4/3$。两相位 $\theta_1=x-11t-y/12$ 和 $\theta_2=x-7t-y/2$ 描述具有不同空间取向和传播速率的两个波。

相应的二孤子波形如下图所示。$u_*$ 中的两条正向波脊沿不同方向接近，并在相互作用区域形成更高的波峰。伴随的 $v_*$ 场包含两条负向波谷，其形状在交汇处附近也发生变化。这种空间变化使我们能够同时考察独立波带及其相互作用区域的分辨情况。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton.png" alt="精确波形：二孤子 (6,−5; 4,−3)；t=0。左：u；右：v。" loading="lazy"><figcaption>精确波形：二孤子 (6,−5; 4,−3)；t=0。左：u；右：v。</figcaption></figure>

第二组算例保留 $(p_2,q_2)=(4,-3)$，并取 $(p_1,q_1)=(1,2)$，将前面两组单孤子算例采用的参数组合起来。此时 $c_1=1/4$、$c_2=2$、$A_{12}=5/4$，相位为 $\theta_1=3x+3t-3y/4$ 和 $\theta_2=x-7t-y/2$。

最后一组算例中，$u_*$ 同时包含一条正向波脊和一条更深的负向波谷，而 $v_*$ 中的两条波带仍均为负。两者幅值与宽度的差异使波形呈现出更不均匀的空间结构。引入这一算例后，我们可以考察各方法如何在较强负向波的同时分辨较小的正向结构，并在两个物理场中刻画它们的相互作用。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton_mixed.png" alt="精确波形：二孤子 (1,2; 4,−3)；t=0。左：u；右：v。" loading="lazy"><figcaption>精确波形：二孤子 (1,2; 4,−3)；t=0。左：u；右：v。</figcaption></figure>

**初值与边界数据。** 为使三种表示从相同的物理初态出发进行比较，我们利用连续精确场 $u_*,v_*$ 初始化各自的变量。PE 取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$，而 FD 使用相同的 $P^0$，并取 $v^0=v_*(0)$。对于 PF，我们由这些物理数据确定 $Q^0,R^0$，并在最左侧 $x$ 节点固定 $Q$ 的归一化。具体重构与下边界初始化见附录 D。

时间推进过程中，连续精确解提供 $y$ 下边界数据和 $u$ 的幽灵层值。在 $x$ 方向，PE 与 FD 采用周期延拓，PF 则纳入 $Q,R$ 的给定加性跳跃。在时间积分器的各阶段计算右端项时，均施加相应边界关系。

**计算设置。** 固定网格的间距为 $\Delta x=h=0.1$。在 SAMM 计算中，我们保持相同节点数及均匀的 $y$ 向间距 $h=0.1$，同时让 $x$ 节点按照第 3.2 节定义的横向平均守恒密度调整位置。由此，我们考察在既定节点数下，节点重新分配如何影响波形的计算精度。

所有算例均从 $t=0$ 开始，以 $\Delta t=10^{-4}$ 推进至 $T=0.01$，共计 100 个时间步。空间表示与网格的比较统一采用 RK4；单独的时间积分器比较保持固定网格 PE 格式及相同时间步长。

**误差度量。** 我们在相同空间位置比较数值物理场与精确物理场，并沿 $x$ 方向对数值节点值进行三次样条插值。记 $\mathcal G$ 为所考察区域内的共同取样点集，终止时刻的最大绝对误差为

<a id="zh-eq-110"></a>

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{82}$$

我们分别报告两个物理场的误差，以考察它们对非线性表示、时间积分器及网格选择的不同响应。

对于 PE 和 PF，我们进一步借助对应的半离散精确解理解总误差的组成。记连续精确场为 $Z=(u_*,v_*)$，具有相同谱参数的半离散精确场为 $Z_h=(U_h,V_h)$，则

<a id="zh-eq-206"></a>

$$Z_{\mathrm{num}}-Z=\underbrace{Z_h-Z}_{\text{lattice error}}+\underbrace{Z_{\mathrm{num}}-Z_h}_{\text{numerical error}}.\tag{83}$$

在第 2.5 节的假设下，格点误差满足 $Z_h-Z=h^2C+O(h^4)$，其中 $C=(C_U,C_V)$。该节导出的系数刻画了离散化 $y$ 所引入误差的首项空间分布。其余贡献包括 $x$ 方向和时间离散、物理场恢复以及初值与边界数据的影响。我们将在下文数值结果中利用这一分解，讨论格点误差与数值误差如何共同作用，并解释两个物理场中观察到的误差表现。

### 3.5 数值结果 {#zh-results}

通过上述算例，我们考察非线性表示、时间积分器和网格选择如何影响两个物理场的计算精度。首先，在固定网格上统一采用 RK4，对比 PE、PF 和 FD，并结合最大误差及其空间分布分析不同表示之间的差异。随后保持 PE 空间格式不变，比较 Euler、RK4 和 Crank–Nicolson，以考察时间积分的影响。最后，在采用相同 RK4 方法和节点数的条件下，对比固定网格与 SAMM，评价节点重新分配带来的精度改善。在相关结果的讨论中，我们结合解析误差系数与上述误差分解，解释观察到的差异。表中，$e_u=E_u(T)$ 和 $e_v=E_v(T)$ 表示终止时刻的最大绝对误差。

#### 3.5.1 空间离散的比较 {#zh-spatial-results}

我们首先在相同网格间距和时间推进方法下比较 PE、PF 和 FD。从连续精确物理场出发，三种格式均在固定网格上采用 RK4 推进至 $T=0.01$。表 1 列出 $u$ 和 $v$ 的最大绝对误差，以考察表示方式的选择如何影响各物理场。

**表 1　固定网格的最大绝对误差 $e_u/e_v$；RK4，$\Delta x=h=0.1$，$\Delta t=10^{-4}$，$T=0.01$。粗体标出各物理场的最小误差。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>PE: e<sub>u</sub> / e<sub>v</sub></th><th>PF: e<sub>u</sub> / e<sub>v</sub></th><th>FD: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td>3.061201e-03 / 3.067031e-03</td><td><strong>4.715088e-04</strong> / <strong>1.201923e-03</strong></td></tr><tr><th>单孤子 (4, −3)</th><td><strong>1.419616e-05</strong> / 2.745967e-05</td><td>8.067776e-05 / 4.377502e-04</td><td>1.718043e-05 / <strong>2.605300e-05</strong></td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td><strong>3.552455e-05</strong> / 5.359645e-05</td><td>7.501357e-05 / 5.394947e-05</td><td>3.989986e-05 / <strong>5.173628e-05</strong></td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td>4.102555e-03 / 3.252786e-03</td><td><strong>4.782980e-04</strong> / <strong>1.350627e-03</strong></td></tr></tbody></table></div>

四组算例中，PE 与 FD 的误差处于相近量级，两者的相对表现随物理场和波形变化。对于 $(4,-3)$ 单孤子和 $(6,-5;\,4,-3)$ 二孤子，PE 的 $u$ 误差更小，而 FD 的 $v$ 误差更小。另外两组算例中，FD 对两个物理场均具有更高精度。因此，即使对于同一个波解，两个物理场对表示方式的选择也可能呈现不同响应。

PF 的结果表现出更明显的算例差异。各组算例的两个物理场误差均大于 PE 和 FD，但差距大小变化显著。第一组二孤子中，其 $v$ 误差与另外两种方法接近；而在 $(4,-3)$ 单孤子中，其 $v$ 误差高出一个数量级以上。尽管 PE 和 PF 表示同一个半离散系统，两者采用的变量及后续数值运算不同，使其在完全离散后产生不同的误差大小。

为了观察这些差异在空间中的分布，我们接下来考察图 1—4 的绝对误差曲面。各列从左至右依次对应 PE、PF 和 FD，上行为 $u$ 误差，下行为 $v$ 误差。同一物理场采用共同色阶和高度范围，以便直接比较误差大小及空间分布。

对于第一组单孤子解，我们观察到两个物理场的误差均集中在斜向波带附近。图 1 中，PE 与 FD 呈现相近的误差形态：$u$ 误差形成数条平行的脊线，$v$ 误差则表现为更突出的中央波带。PF 沿同一波形结构产生更大的误差。因此，表 1 中 PF 较大的最大误差对应着一段持续分布的较大偏差，而非单个孤立峰值。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/A_errors3d.png" alt="图 1　单孤子 (1,2)：T=0.01 时的绝对误差曲面。" loading="lazy"><figcaption>图 1　单孤子 (1,2)：T=0.01 时的绝对误差曲面。</figcaption></figure>

第二组单孤子更清楚地呈现了不同表示之间的差异。图 2 中，PE 与 FD 的误差仍集中在波带附近，并具有相近的空间形态。PF 的 $v$ 误差则延伸至区域内更广的范围，在远离主要波带的位置仍明显偏高。因此，差异同时体现在误差大小和空间分布范围上，与表 1 中 PF 和 PE、FD 之间更大的 $v$ 最大误差差距相对应。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/B_errors3d.png" alt="图 2　单孤子 (4,−3)：T=0.01 时的绝对误差曲面。" loading="lazy"><figcaption>图 2　单孤子 (4,−3)：T=0.01 时的绝对误差曲面。</figcaption></figure>

对于第一组二孤子解，误差曲面沿两条波支分布，并在相互作用区域附近形成突出的峰值。图 3 中，三种方法的 $v$ 误差均呈现这一结构，其最大值也彼此接近。$u$ 误差则表现出更明显的区别：PF 在相互作用附近产生更高峰值，而 PE 和 FD 保持相似的分布，幅值较小。对比上下两行可以清楚地看到这种物理场依赖性：各表示的 $v$ 误差较为接近，但在 $u$ 场上存在更明显的差异。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/C_errors3d.png" alt="图 3　二孤子 (6,−5; 4,−3)：T=0.01 时的绝对误差曲面。" loading="lazy"><figcaption>图 3　二孤子 (6,−5; 4,−3)：T=0.01 时的绝对误差曲面。</figcaption></figure>

在混合极性二孤子算例中，较大误差集中在较强的负向波带附近，较小的正向结构在误差曲面中并不突出。图 4 再次呈现出 PE 与 FD 相近的误差分布，其中 FD 在两个物理场上均取得较小的最大误差。PF 则形成明显更高的误差带，尤其在 $u$ 场中。结合第一组单孤子算例可见，当 $(1,2)$ 波被纳入相互作用解后，PF 误差较大的现象仍然存在。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/D_errors3d.png" alt="图 4　二孤子 (1,2; 4,−3)：T=0.01 时的绝对误差曲面。" loading="lazy"><figcaption>图 4　二孤子 (1,2; 4,−3)：T=0.01 时的绝对误差曲面。</figcaption></figure>

为解释上述空间离散的比较结果，我们回到第 3.4 节区分的两项误差贡献。对于 PE 和 PF，半离散精确场与连续精确场之差为 $h^2C+O(h^4)$，其中 $C=(C_U,C_V)$ 刻画格点误差的首项空间分布。由于两种表示具有相同的半离散精确物理场，这部分贡献也是共同的。因此，表 1 和图 1—4 中两者的误差差异来自数值误差部分：演化变量的选择、后续离散及物理场恢复，使它们对同一半离散解形成不同的数值近似。

为更定量地理解 PE 与 FD 的相对表现，我们将 $t=0$ 的连续精确场代入两种格式，计算其空间截断误差。对于 $u_t$ 的近似，误差首项为

$$r_m^u=\underbrace{(\Delta x)^2B}_{X}+\underbrace{h^2A_m}_{Y_m}
+O\!\left((\Delta x)^4+(\Delta x)^2h^2+h^4\right),\qquad m=\mathrm{PE},\mathrm{FD}.$$

其中 $B$ 是第 3.1 节讨论的共同 $x$ 向离散误差系数，$A_m$ 描述离散化 $y$ 的贡献。记 $[f]_b^y=f(x,y,0)-f(x,b,0)$，则

$$A_{\mathrm{FD}}=-\frac1{12}\partial_x^2[v_y]_b^y,\qquad
A_{\mathrm{PE}}=A_{\mathrm{FD}}-\partial_x\left[\frac{(v-u_y)^2}{32}-\frac{v-u_y}{4}\right]_b^y+\frac14\partial_x^2[u_{yy}]_b^y.$$

因此，PE 不仅改变了 $y$ 向贡献的大小，也改变了它与共同 $x$ 向贡献之间的空间关系。我们利用归一化空间内积衡量这种关系：

$$\gamma_m=\frac{\langle X,Y_m\rangle}{\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}},
\qquad \langle X,Y_m\rangle=\frac1{|\mathcal G|}\sum_{\mathcal G}XY_m.$$

当分项范数非零时，相应恒等式为

<a id="zh-eq-207"></a>

$$\|X+Y_m\|_{\mathrm{RMS}}^2=\|X\|_{\mathrm{RMS}}^2+\|Y_m\|_{\mathrm{RMS}}^2+2\gamma_m\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}.\tag{84}$$

$\gamma_m<0$ 时，交叉项通过抵消降低合成误差的平方范数；正值则增大这一范数。表 2 给出 $\Delta x=h=0.1$、$t=0$ 时四组算例的首项贡献，RMS 与内积均在相应区域的格点上计算。

<div class="table-wrap error-budget-wrap"><table class="comparison error-budget"><caption>表 2　$t=0$ 时 $u_t$ 的空间截断误差首项贡献。</caption><colgroup><col style="width:23%"><col style="width:8%"><col style="width:18%"><col style="width:18%"><col style="width:13%"><col style="width:20%"></colgroup><thead><tr><th scope="col">算例</th><th scope="col">方法</th><th scope="col"><i>x</i> 向贡献<br>$\|X\|_{\mathrm{RMS}}$</th><th scope="col"><i>y</i> 向贡献<br>$\|Y_m\|_{\mathrm{RMS}}$</th><th scope="col">相关性<br>$\gamma_m$</th><th scope="col">合成误差<br>$\|X+Y_m\|_{\mathrm{RMS}}$</th></tr></thead><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">单孤子<br>(1,2)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="1.01572e-02">1.016 × 10<sup>−2</sup></span></td><td><span class="budget-number" data-value="4.75387e-03">4.754 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="+0.3295">+0.3295</span></td><td><span class="budget-number" data-value="1.25535e-02">1.255 × 10<sup>−2</sup></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="1.38192e-03">1.382 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="-0.8512">−0.8512</span></td><td><span class="budget-number" data-value="9.01016e-03"><strong>9.010 × 10<sup>−3</sup></strong></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">单孤子<br>(4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="6.19698e-04">6.197 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="2.39752e-04">2.398 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.5367">−0.5367</span></td><td><span class="budget-number" data-value="5.31071e-04"><strong>5.311 × 10<sup>−4</sup></strong></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="3.58155e-05">3.582 × 10<sup>−5</sup></span></td><td><span class="budget-number" data-value="+0.9965">+0.9965</span></td><td><span class="budget-number" data-value="6.55395e-04">6.554 × 10<sup>−4</sup></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">二孤子<br>(6,−5;<br> 4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="5.08691e-04">5.087 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="1.63056e-04">1.631 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.5780">−0.5780</span></td><td><span class="budget-number" data-value="4.35281e-04"><strong>4.353 × 10<sup>−4</sup></strong></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="2.46367e-05">2.464 × 10<sup>−5</sup></span></td><td><span class="budget-number" data-value="+0.8659">+0.8659</span></td><td><span class="budget-number" data-value="5.30168e-04">5.302 × 10<sup>−4</sup></span></td></tr></tbody><tbody class="case-group"><tr><th rowspan="2" scope="rowgroup" class="case-name">二孤子<br>(1,2;<br> 4,−3)</th><th scope="row" class="method">PE</th><td rowspan="2"><span class="budget-number" data-value="4.39676e-03">4.397 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="1.93527e-03">1.935 × 10<sup>−3</sup></span></td><td><span class="budget-number" data-value="+0.3044">+0.3044</span></td><td><span class="budget-number" data-value="5.31566e-03">5.316 × 10<sup>−3</sup></span></td></tr><tr><th scope="row" class="method">FD</th><td><span class="budget-number" data-value="5.89777e-04">5.898 × 10<sup>−4</sup></span></td><td><span class="budget-number" data-value="-0.8643">−0.8643</span></td><td><span class="budget-number" data-value="3.89830e-03"><strong>3.898 × 10<sup>−3</sup></strong></span></td></tr></tbody></table><p class="budget-note">每组算例中，PE 与 FD 具有相同的 <i>x</i> 向贡献。粗体表示每对比较中较小的合成 RMS 残差。</p></div>

首项表达式与完整空间残差吻合良好，相对 RMS 差异为 $0.12\%$–$2.12\%$。

这一分析有助于为 PE 与 FD 相对精度的变化提供定量解释。两种方法具有共同的 $x$ 向离散误差首项，而它们对 $y$ 方向的不同处理产生不同的空间误差分布。对于 $(1,2)$ 单孤子和混合极性二孤子，FD 的 $y$ 向贡献减小了合成空间残差，而 PE 的贡献增大残差。另外两组解中，这一关系反转，PE 得到较小残差。由此得到的排序与四组算例中终止时刻的 $u$ 最大误差一致。因此，我们将两种空间格式所呈现的精度差异，具体联系到各自的 $y$ 向误差系数在不同波形上的取值，以及它们与共同 $x$ 向离散误差的叠加结果。

在完成空间表示的比较后，下面的实验保持 PE 不变，考察其精度如何随时间积分器和网格布置而变化。

#### 3.5.2 PE 的时间推进比较 {#zh-time-results}

在考察空间离散之后，我们保持固定网格 PE 格式不变，比较前向 Euler、RK4 和 Crank–Nicolson。三种方法均从相同初值出发，以 $\Delta x=h=0.1$、$\Delta t=10^{-4}$ 推进至 $T=0.01$。我们同时考察最大误差及其空间剖面，观察改变时间积分器如何影响各物理场的精度。

最大绝对误差列于表 3。四组算例中 Crank–Nicolson 与 RK4 的结果十分接近。Euler 带来的差异更明显：在 $(1,2)$ 单孤子和混合极性二孤子中，它给出较小的 $u$ 最大误差；另外两组中，RK4 的 $u$ 误差更小。对于 $v$，四组算例均由 RK4 取得最小的最大误差。

**表 3　PE 采用 Euler、RK4 与 Crank–Nicolson 的最大绝对误差 $e_u/e_v$。固定网格；$T=0.01$、$\Delta x=h=0.1$、$\Delta t=10^{-4}$。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>Euler: e<sub>u</sub> / e<sub>v</sub></th><th>RK4: e<sub>u</sub> / e<sub>v</sub></th><th>C–N: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td><strong>6.396711e-04</strong> / 1.340634e-03</td><td>6.406395e-04 / <strong>1.339511e-03</strong></td><td>6.406384e-04 / 1.339513e-03</td></tr><tr><th>单孤子 (4, −3)</th><td>1.422394e-05 / 3.005484e-05</td><td><strong>1.419616e-05</strong> / <strong>2.745967e-05</strong></td><td>1.419664e-05 / 2.746028e-05</td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td>3.840649e-05 / 5.901085e-05</td><td><strong>3.552455e-05</strong> / <strong>5.359645e-05</strong></td><td>3.552653e-05 / 5.359819e-05</td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td><strong>6.188417e-04</strong> / 1.515498e-03</td><td>6.329588e-04 / <strong>1.511271e-03</strong></td><td>6.330018e-04 / 1.511273e-03</td></tr></tbody></table></div>

接下来考察空间误差剖面

$$\varepsilon_u^{(m)}(x)=\max_j|u_m(x,y_j,T)-u_*(x,y_j,T)|,\qquad
\varepsilon_v^{(m)}(x)=\max_j|v_m(x,y_j,T)-v_*(x,y_j,T)|.$$

其中 $m$ 表示时间积分器。每组算例均将两个物理场并排展示，并在 RK4 误差峰值附近给出局部放大。

对于 $(1,2)$ 单孤子，三种方法的误差剖面十分接近。局部放大显示了峰值附近的细微差异：Euler 的 $u$ 误差略小，$v$ 误差略大，而 Crank–Nicolson 与 RK4 几乎无法区分。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1150"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="图 5　单孤子 (1,2)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-2.35193500%);"></div><figcaption>图 5　单孤子 (1,2)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。</figcaption></figure>

$(4,-3)$ 单孤子对积分器选择的响应更明显。Euler 改变了 $u$ 误差剖面的形状，但最大值仍与另外两种方法接近。在 $v$ 场中，差异延伸至波形较宽的部分，Euler 产生了更高的误差平台。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1148"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="图 6　单孤子 (4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-26.94034638%);"></div><figcaption>图 6　单孤子 (4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。</figcaption></figure>

对于 $(6,-5;\,4,-3)$ 二孤子，我们还观察到主导 $u$ 误差峰值位置的变化。Euler 在放大图所示的 RK4 峰值附近给出较小误差，却在其他位置形成更高峰值。因此，表中更大的最大误差体现了误差沿剖面的重新分布。在 $v$ 场中，Euler 的主峰更高，RK4 与 Crank–Nicolson 的剖面则仍十分接近。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1140"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="图 7　二孤子 (6,−5; 4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-51.48599530%);"></div><figcaption>图 7　二孤子 (6,−5; 4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。</figcaption></figure>

混合极性二孤子再次呈现第一组算例中的模式。三种剖面在区域内较为接近，Euler 的 $u$ 误差峰值略低，$v$ 误差峰值略高。Crank–Nicolson 与 RK4 在整个剖面中再次保持吻合，包括局部放大的区域。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3196/1129"><img src="../Workspaces/dlw_paper_20261009/figures/PE_time_profiles.png" alt="图 8　二孤子 (1,2; 4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-75.86059440%);"></div><figcaption>图 8　二孤子 (1,2; 4,−3)，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。</figcaption></figure>

这些算例表明，改变时间积分器会影响空间离散解中误差的大小和位置。在所选分辨率下，Crank–Nicolson 与 RK4 给出几乎相同的剖面，而 Euler 引起的变化依赖于波形和物理场。接下来的实验继续采用 RK4，在共同的时间推进方法下考察网格自适应的作用。

#### 3.5.3 自适应动网格方法的数值表现 {#zh-mesh-results}

下面，我们考察第 3.2 节基于守恒律构造的网格自适应，能否在相同节点数下提高 PE 的计算精度。固定网格与自适应计算均采用 RK4、$\Delta t=10^{-4}$ 及均匀的 $y$ 向间距 $h=0.1$。对于 SAMM，横向平均守恒密度确定 $x$ 节点的初始分布，随后节点与物理场共同演化。

我们首先以 $(6,-5;\,4,-3)$ 二孤子说明这种重新分配。图 9 将各区间局部节点间距除以均匀间距 $\Delta x=0.1$，并在区间中点绘制。小于 1 的值表示节点更集中，大于 1 的值表示间距更宽。

<figure><img src="../Workspaces/dlw_paper_20261009/figures/SAMM_spacing_C.png" alt="图 9　(6,−5; 4,−3) 二孤子的归一化局部 x 间距。灰色虚线：自适应初始网格；蓝色：T=0.01；橙色点线：均匀网格。" loading="lazy"><figcaption>图 9　(6,−5; 4,−3) 二孤子的归一化局部 x 间距。灰色虚线：自适应初始网格；蓝色：T=0.01；橙色点线：均匀网格。</figcaption></figure>

自适应网格将节点集中在区域中央，最小间距出现在 $x=0$ 附近，并以远处略宽的区间进行补偿。在 $T=0.01$ 时，最小间距约为 $0.09834$，均匀网格间距则为 $0.1$。在这一短时间区间内，初始与最终间距曲线几乎重合，因此所示分布主要由初始自适应建立，并在演化中继续调整。

为评价精度变化，我们比较两个物理场的最大绝对误差。表 4 还给出相对于固定网格的误差下降百分比：

$$\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{SAMM}}(T)}{E_f^{\mathrm{fixed}}(T)}\right)\%,\qquad f=u,v.$$

**表 4　PE 在 $T=0.01$ 时固定网格与自适应网格的最大绝对误差 $e_u/e_v$；节点数及 RK4 积分器相同。**

<div class="table-wrap"><table class="comparison compact-results"><thead><tr><th>算例</th><th>固定网格: e<sub>u</sub> / e<sub>v</sub></th><th>动网格: e<sub>u</sub> / e<sub>v</sub></th><th>降幅：u / v</th></tr></thead><tbody><tr><th>单孤子 (1, 2)</th><td>6.406395e-04 / 1.339511e-03</td><td><strong>5.781845e-04</strong> / <strong>1.091714e-03</strong></td><td>9.75% / 18.50%</td></tr><tr><th>单孤子 (4, −3)</th><td>1.419616e-05 / 2.745967e-05</td><td><strong>1.334447e-05</strong> / <strong>2.621326e-05</strong></td><td>6.00% / 4.54%</td></tr><tr><th>二孤子 (6, −5; 4, −3)</th><td>3.552455e-05 / 5.359645e-05</td><td><strong>3.304157e-05</strong> / <strong>5.060189e-05</strong></td><td>6.99% / 5.59%</td></tr><tr><th>二孤子 (1, 2; 4, −3)</th><td>6.329588e-04 / 1.511271e-03</td><td><strong>6.156957e-04</strong> / <strong>1.428010e-03</strong></td><td>2.73% / 5.51%</td></tr></tbody></table></div>

SAMM 降低了四组算例中两个物理场的最大误差。$u$ 的改善范围为 $2.73\%$–$9.75\%$，$v$ 为 $4.54\%$–$18.50\%$。为了观察改善出现的位置，我们考察上一小节定义的空间误差剖面。

对于 $(1,2)$ 单孤子，自适应网格降低了主导的 $u$ 误差峰值，并减小了 $v$ 误差剖面中较宽的高值区域。后者的改善延伸至波形区域的大部分位置，对应表中最大的相对降幅。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1020"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="图 10　单孤子 (1,2) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-2.60416667%);"></div><figcaption>图 10　单孤子 (1,2) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。</figcaption></figure>

$(4,-3)$ 单孤子的改善幅度较小，但分布持续。SAMM 降低了两个误差剖面较宽的中央部分，同时保持整体形态。因此，最大误差的下降也伴随着区域内较大范围的误差减小。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1030"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="图 11　单孤子 (4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-26.75189394%);"></div><figcaption>图 11　单孤子 (4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。</figcaption></figure>

对于 $(6,-5;\,4,-3)$ 二孤子，最明显的下降出现在相互作用区域附近的主要误差峰值处，而若干分离波支上的剖面仍较接近。这将前面的节点间距图与精度比较联系起来：共享 $x$ 网格的适度重新分配，伴随着 $u$、$v$ 最大误差分别下降 $6.99\%$ 和 $5.59\%$。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1035"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="图 12　二孤子 (6,−5; 4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-51.13636364%);"></div><figcaption>图 12　二孤子 (6,−5; 4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。</figcaption></figure>

混合极性二孤子中，SAMM 降低了两个剖面较宽的中央部分。决定 $u$ 最大误差的窄峰变化较小，降幅为 $2.73\%$，而 $v$ 最大误差下降 $5.51\%$。因此，空间剖面展示了单个最大误差指标之外的改善。

<figure class="profile-pair"><div style="position:relative;overflow:hidden;aspect-ratio:3334/1029"><img src="../Workspaces/dlw_paper_20261009/figures/PE_mesh_profiles.png" alt="图 13　二孤子 (1,2; 4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;height:auto;margin:0;transform:translateY(-75.63920455%);"></div><figcaption>图 13　二孤子 (1,2; 4,−3) 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。</figcaption></figure>

通过这些比较，我们看到基于守恒律的密度为共享 $x$ 节点的配置提供了有效依据。尽管密度由 $W=v-\delta_0u$ 构造并在 $y$ 方向平均，所得网格仍降低了全部算例中两个物理场的最大误差。改善幅度及位置随波形变化，而节点数与时间积分器保持不变。

## 4. 结论 {#zh-conclusion}


本文将可积半离散 DLW 系统的构造与其数值近似分析联系起来。我们从连续双线性方程出发，在 $y$ 方向引入交错格点，并将其与双线性算子参数的平移结合，同时保持 $x$ 和 $t$ 连续。所得系统保留了任意有限阶的 Gram 行列式解。在这一构造的基础上，消去或保留辅助势分别得到 PE 和 PF 表示，我们进一步建立了它们的 Darboux–Lax 表示及其与非线性方程的相容性。

显式解也使我们能够具体考察离散波场如何趋近于相应的连续波场。在所述正则性和正性假设下，我们证明了这些物理场的二阶收敛性，以及方程的二阶相容性。通过推导误差首项系数，我们进一步刻画了格点引入的空间变化。这些系数在解析构造与数值实验所考察的误差之间建立了具体联系。

当其余变量进一步离散化时，非线性表示的选择开始影响计算结果。尽管 PE 和 PF 描述相同的半离散精确物理场，它们的数值实现仍产生不同的误差大小和分布，且四组算例中 PE 在两个物理场上均取得较小的最大误差。与 FD 的比较则呈现出更丰富的情况：相对精度随波形和物理场而改变。对于 $u$，我们的分析将这种变化联系到不同的 $y$ 向误差系数，以及它们与共同的 $x$ 向离散误差首项的作用。在 $t=0$ 处计算这些贡献，得到的 PE–FD 排序与四组算例终止时刻的 $u$ 最大误差排序一致。这种吻合使我们能够超出形式误差阶的比较，进一步解释不同空间离散为何呈现出所观察到的精度。

在采用 PE 空间表示的基础上，我们随后考察了时间积分和节点配置对计算的影响。在所测试的分辨率下，Crank–Nicolson 与 RK4 给出几乎重合的误差剖面，而 Euler 引起的变化则依赖于波形和物理场。网格自适应为同一表示下的精度改善提供了另一条途径。利用半离散系统的守恒律，我们构造了与物理场共同演化的共享自适应 $x$ 网格，同时保持 $y$ 向格点均匀。在节点数和 RK4 积分器均不变的条件下，自适应网格降低了四组算例中两个物理场的最大误差，其中 $u$ 的降幅为 $2.73\%$–$9.75\%$，$v$ 的降幅为 $4.54\%$–$18.50\%$。由此，从半离散系统得到的守恒律也用于指导数值分辨率的分配，使既有节点能够更准确地描述波形。

我们的工作展示了半离散系统的解析结构如何同时参与数值近似的解释与设计。精确解使我们能够追踪格点引入的变化，误差系数帮助解释不同离散方法为何在同一波形上表现不同，而守恒律则提供了利用这些结构配置计算节点的途径。通过将这些方面联系起来，我们的研究从构造具有显式解的离散方程，进一步走向理解其表示方式与数值实现如何影响物理场的计算精度。这种联系也为后续研究提供了基础，使解析性质能够具体地指导数值计算中的方法选择。

## 附录 A. 精确解族差的首项 {#zh-app-a}

我们通过对 Gram 行列式作关于格距的展开，推导半离散与连续精确物理场之差的首项。记 $z_i=p_i-a$、$w_i=q_i+a$，主子式展开中的每一项对应相同的行、列指标集 $I$。格点相位贡献 $h^2y\sum_{i\in I}c_i$，而 (45) 中居中的 $f$ 振幅贡献 $h^2\sum_{i\in I}d_i$。由此得到

<a id="zh-eq-208"></a>

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,\qquad \alpha_2=\sum_i(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_i c_i\rho_i\partial_{\rho_i}\beta.\tag{85}$$

算子 $\rho_i\partial_{\rho_i}$ 恰好选出含指标 $i$ 的主子式。因此，先展开行列式再展开其对数，即可对任意固定的 $N$ 得到 (85)。将其代入物理中点处的对称重构关系，得到

<a id="zh-eq-209"></a>

$$\begin{aligned}U_h&=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4),\\V_h&=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).\end{aligned}\tag{86}$$

将 $4\beta_{xy}=v-u_y$ 代入 (86)，即得到 (41) 中的系数。对于固定的正则谱参数及充分小的 $h$，$K$ 邻域内 τ 函数不为零，保证展开所需的导数和余项具有一致界。定理 2.7 的正谱域满足这些条件；在具有相同界的区域内，这一计算也适用于其他正则实分支。

## 附录 B. 相邻层行列式恒等式 {#zh-app-b}

**证明。** 我们将 Gram 矩阵的层移位表示为秩一更新，以证明相邻层恒等式 (13)。第 $n$ 层的 Gram 矩阵为 $M=I+(r_ic_k/(p_i+q_k))$，其中

<a id="zh-eq-14"></a>

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{87}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义可得

<a id="zh-eq-15"></a>

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{88}$$

特别地，(88) 中的秩一更新来自恒等式

<a id="zh-eq-16"></a>

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.\tag{89}$$

我们先在 $M$ 可逆的区域内引入

<a id="zh-eq-17"></a>

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{90}$$

最后一个等式由矩阵行列式引理得到，而 Jacobi 微分公式给出 $\kappa=\tau_{n,x}/\tau_n$。为收集求导产生的项，记

<a id="zh-eq-18"></a>

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{91}$$

利用 $H_x=-HM_xH$、$H_t=-HM_tH$，逐项求导得到

<a id="zh-eq-19"></a>

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{92}$$

例如 $z_x=HPr-\kappa z$，故 $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$。对其再求一次导数，并消去 $\eta_1,\eta_2$，得到

<a id="zh-eq-20"></a>

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{93}$$

因此 $\psi=1-\zeta$ 满足

<a id="zh-eq-21"></a>

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{94}$$

对于 $f=\psi g$，展开双线性算子可得

<a id="zh-eq-22"></a>

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{95}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，即可将 (94) 识别为 $M$ 可逆处的双线性恒等式 [(13)](#zh-eq-13)。这一恒等式通过多项式延拓适用于奇异矩阵。具体地，将每个 $\rho_i$ 替换为 $\varepsilon\rho_i$。在固定 $x,t$ 下，$\varepsilon=0$ 时矩阵为单位矩阵，因此双线性残差在 $\varepsilon$ 的零点邻域内消失。由于该残差是 $\varepsilon$ 的多项式，它恒等于零。取 $\varepsilon=1$ 即完成证明。□

## 附录 C. Darboux 算子计算 {#zh-app-c}

**证明。** 我们用两个一阶 Darboux 算子表示线性系统的格点关系，并将其相容性与非线性方程联系起来。为此，采用

<a id="zh-eq-73"></a>

$$r_j=\frac{U_j}{2}+\frac{hw_j}{8},\qquad s_j=\frac{U_j}{2}-\frac{hw_j}{8},\tag{96}$$

<a id="zh-eq-74"></a>

$$\mathscr A_j=\partial_x-r_j,\quad \mathscr B_j=\partial_x-s_j,\quad T_j=\mathscr B_j^{-1}\mathscr A_j,\quad H_j=-\partial_x^2-V_j.\tag{97}$$

其中 $\mathscr B_j^{-1}$ 在形式伪微分算子代数中定义。线性系统写为 $\psi_{j+1}=T_j\psi_j$、$\psi_{j,t}=H_j\psi_j$。对格点关系关于 t 求导，并代入相邻两层的时间方程，得到

<a id="zh-eq-75"></a>

$$T_{j,t}=H_{j+1}T_j-T_jH_j.\tag{98}$$

为验证该恒等式，定义标量残差

<a id="zh-eq-76"></a>

$$\begin{aligned}
\mathcal E_j^r&=r_{j,t}+r_{j,xx}+2r_jr_{j,x}+V_{j,x},\\
\mathcal E_j^s&=s_{j,t}+s_{j,xx}+2s_js_{j,x}+V_{j+1,x}.
\end{aligned}\tag{99}$$

利用 $V_{j+1}-V_j=(h/2)w_{j,x}$，可得

<a id="zh-eq-77"></a>

$$\begin{aligned}
\mathcal E_j^r-\mathcal E_j^s&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^r+\mathcal E_j^s&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{100}$$

$w$ 方程使 (100) 中的残差之差为零，而 $V_{j,x}$ 的定义使残差之和为零。因此，$\mathcal E_j^r=\mathcal E_j^s=0$。这些标量关系通过以下 Darboux 恒等式进入算子计算；该恒等式由标量函数 $r$ 的乘积法则得到：

<a id="zh-eq-78"></a>

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{101}$$

由辅助势差关系，有

<a id="zh-eq-79"></a>

$$\widetilde V_j:=V_j+2r_{j,x}=V_{j+1}+2s_{j,x}.\tag{102}$$

记

<a id="zh-eq-80"></a>

$$L_j=\partial_t+\partial_x^2+V_j,\qquad \widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j,\tag{103}$$

分别将 Darboux 恒等式用于两个为零的残差，得到

<a id="zh-eq-81"></a>

$$\widetilde L_j\mathscr A_j=\mathscr A_jL_j,\qquad \widetilde L_j\mathscr B_j=\mathscr B_jL_{j+1}.\tag{104}$$

消去共同的中间算子，得到 $L_{j+1}T_j=T_jL_j$，即相容条件 [(98)](#zh-eq-75)。

反过来，我们假设相容条件及辅助势差关系成立。在保留标量残差的情况下重复上述算子计算，得到

<a id="zh-eq-82"></a>

$$\mathscr B_j(T_{j,t}-H_{j+1}T_j+T_jH_j)=-\mathcal E_j^r+\mathcal E_j^sT_j,\qquad T_j=I-\mathscr B_j^{-1}\frac{hw_j}{4}.\tag{105}$$

比较 $\partial_x^0$ 和 $\partial_x^{-1}$ 的系数，得到 $\mathcal E_j^r=\mathcal E_j^s$ 及 $w_j\mathcal E_j^s=0$。因此，在 $w_j\ne0$ 的区域内，两项残差均为零。两者之差恢复 $w$ 方程；对两者之和施加 $\delta_-$，再利用辅助势差关系，即恢复第一条非线性方程。□

## 附录 D. 重构与边界初始化 {#zh-app-d}

数值格式需要与给定物理场一致的辅助变量初值和边界数据。对于 PF，我们由 $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ 及归一化条件 $Q_{j,0}^0=1$ 确定 $Q$，再取 $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$。同一关系由 $u_{*,0}(t)$ 确定下边界值 $Q_0(t)$。

变量 $P,W$ 通过以下关系确定物理场：

<a id="zh-eq-89"></a>

$$u_{j,i}=u_{j_L,i}+h\sum_{k=j_L+1}^{j}P_{k,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i}.\tag{106}$$

其中，$j_L$ 表示最下层，给定值 $u_{j_L,i}(t)$ 确定重构中的边界贡献。



为计算演化方程中的势函数项 $(M_j+M_{j+1})_x$，我们采用 $m_j\simeq M_{j,x}$ 及 $S_j=Q_jR_j$。对格点约束 $M_{j+1}-M_j=h(1-S_j)$ 施加 $D_1$，得到

<a id="zh-eq-92"></a>

$$m_{j+1}=m_j-hD_1S_j.\tag{107}$$

给定 $m$ 的下边界值后，(107) 依次确定其余各层。将最下层临时编号为 $0$，由该层的 $Q$ 方程得到这一边界值：

<a id="zh-eq-93"></a>

$$m_0=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{h^2}{8}\bigl[S_0^2-1\bigr]+\frac h2D_1S_0.\tag{108}$$

其中，$Q_0(t)$ 由下边界数据给定，$Q_{0,t}$ 为其时间导数。

## 附录 E. 移动节点上的导数 {#zh-app-e}

随着网格运动，物理空间中的 $x$ 节点间距不再均匀。我们将移动节点映射至固定、均匀的计算坐标 $\xi_i=-L/2+i\Delta\xi$，其中 $\Delta\xi=L/N_x$，以计算空间导数。写成 $x_i(t)=\xi_i+s_i(t)$ 后，位移 $s_i$ 确定离散 Jacobian $J_i=1+D_\xi s_i$，用于近似 $J=x_\xi$。

对于定义在移动节点上的场，链式法则给出 $\partial_x=J^{-1}\partial_\xi$。再作用一次该算子，就会对 $J^{-1}$ 求导，因而

<a id="zh-eq-101"></a>

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.\tag{109}$$

分别以均匀 $\xi$ 网格上的中心差分近似这些导数，得到

<a id="zh-eq-102"></a>

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{110}$$

算子 $D_\xi,D_{\xi\xi}$ 是在均匀计算网格上应用的三点差分公式 [(62)](#zh-eq-87)。移动节点处的时间导数还包含位置变化的贡献，因此 $\dot z=F_z+\mathcal V D_1z$。将这一关系与节点方程 [(76)](#zh-eq-100) 耦合，得到由第 3.3 节时间积分器推进的场与网格系统。取 $s=0$ 和 $\mathcal V=0$ 即恢复固定网格计算。

## 附录 F. 隐式时间推进 {#zh-app-f}

对于固定网格 PE 系统，Crank–Nicolson 时间推进需要在每一步求解非线性方程。该方法对当前与下一时间层的右端取平均：

<a id="zh-eq-104"></a>

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.\tag{111}$$

在这一计算中，$z$ 包含变量 $P,W$。我们以向前 Euler 预测值 $z^{(0)}=z^n+\Delta t\,\mathcal F(t_n,z^n)$ 初始化非线性迭代，并采用残差修正
$$z^{(r+1)}=z^{(r)}-\mathcal R(z^{(r)}),$$
其中，$\mathcal R$ 为第 3.3 节定义的非线性残差。每次残差求值均包括物理场恢复，以及相应时刻边界数据的施加。停止准则为
$$\|\mathcal R(z^{(r)})\|_\infty\le 10^{-12}+10^{-11}\max(1,\|z^n\|_\infty)$$
满足这一准则的迭代值被接受，每个时间步最多允许 80 次残差求值。[第 3.5.2 节](#zh-time-results) 比较了所得误差与 Euler、RK4 的计算结果。

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
