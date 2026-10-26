"""Apply the reviewed bilingual prose, preserving numbered mathematical displays."""
from pathlib import Path
import re, json, shutil
from datetime import datetime

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
path = HERE / 'manuscript.md'
original = path.read_text(encoding='utf-8')
assert 'Nonlinear long-wave equations provide a setting' in original, 'Reviewed revision already applied, or source has changed; do not rerun blindly.'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
out = HERE / 'discussion_revision_20261019' / stamp
out.mkdir(parents=True, exist_ok=False)
shutil.copy2(path, out / 'before_manuscript.md')
shutil.copy2(ROOT / 'report/dlw_paper_draft.html', out / 'before_draft.html')

def section(text, anchor):
    m = re.search(r'(?m)^#{2,3} .*\{#' + re.escape(anchor) + r'\}\s*\n', text)
    assert m, anchor
    end = re.search(r'(?m)^#{1,3} ', text[m.end():])
    return m.start(), m.end() + end.start() if end else len(text)

def replace_section(text, anchor, body):
    a,b = section(text, anchor)
    heading = text[a:text.index('\n',a)]
    return text[:a] + heading + '\n\n' + body.strip() + '\n\n' + text[b:]

def eq(lang, number):
    for m in re.finditer(r'<a id="' + lang + r'-eq-[^"]+"></a>\s*\n\s*\$\$[\s\S]*?\$\$', original):
        if rf'\tag{{{number}}}' in m[0]:
            return m[0]
    raise ValueError((lang,number))

intro_en = r'''
The propagation and interaction of waves in shallow water have long attracted interest in the study of nonlinear wave phenomena. As waves evolve, nonlinear effects and dispersion can influence their profiles in different ways, and their balance can support coherent waves that persist during propagation. Nonlinear long-wave equations describe these effects in a reduced form, allowing wave motion to be studied without retaining the full complexity of the underlying fluid equations. Within this class, integrable models have received sustained attention for the analytical insight they offer. Their exact solutions make it possible to follow the evolution of individual waves and examine their interactions, while bilinear formulations and Lax representations reveal mathematical structures underlying these solutions. These analytical results also provide useful reference points for numerical studies, in which wave profiles and their evolution are represented on a discrete mesh. Passing from a continuous model to such a representation introduces choices that affect both the approximation of the waves and the mathematical structure of the resulting equations. Integrable discretization seeks to retain this connection, bringing the construction of discrete equations together with the study of their exact solutions and continuum limits.

The (2+1)-dimensional dispersive long wave (DLW) system extends the dispersive long wave equation to two spatial dimensions [1] and has been studied in connection with wave motion in wide channels and open seas of finite depth [3,4]. Since its introduction by Boiti, Leon and Pempinelli, its wave solutions have been studied through several closely related analytical approaches. The inverse spectral transform, Bäcklund transformation and superposition formula established in the original work [1] were followed by nonlinear transformations [2] and bilinear methods [3], which offered further ways to generate solutions and understand their relations. Determinant representations give these relations a concrete form. Hu, Xu and Yu developed Grammian and Wronskian solutions [4], and Sheng and Yu used a KP-hierarchy reduction to obtain Gram determinant solutions describing solitons, line breathers and rational waves on constant and periodic backgrounds [5].

The bilinear relations underlying these solutions also offer a starting point for introducing a lattice [16]. In this approach, Bäcklund transformations relate neighbouring lattice values, allowing discrete equations to be constructed together with their solution structures. This idea has been developed for semi-discrete soliton equations [7] and extended to systems with two spatial dimensions [8]. For the DLW system, a further connection comes from its bilinear relation to the (2+1)-dimensional sinh-Gordon equation [5], whose integrable discretizations admit determinant solutions and Bäcklund–Lax structures [6]. Together with earlier studies of discrete DLW systems [12], these developments motivate a closer examination of how the continuous DLW solution family can be carried onto a spatial lattice, and how the resulting wave fields compare with their continuous counterparts.

With these advancements, there is potential to study the preservation of integrable structure and the approximation of continuous waves within the same construction. With this in mind, we ask how to introduce a spatial lattice that preserves the bilinear and determinant structure, supports a consistent reconstruction of the physical fields, and admits a quantitative comparison between its exact solutions and those of the continuous system.

To address this question, we seek a semi-discrete description of the DLW system in the $y$ direction, with $x$ and $t$ remaining continuous. First, we wish to retain the connection between explicit wave solutions and the integrable structure that supports their evolution. More specifically, we seek Gram determinant solutions that make the discrete wave fields accessible to analytical study. A corresponding Lax representation should describe the same nonlinear evolution through its compatibility conditions. Second, we wish to understand what changes when the continuous waves are represented on a lattice. This calls for a quantitative comparison of the reconstructed fields, beyond the recovery of the continuous equations in the limit. Such a comparison would reveal how the discrete waves approach their continuous counterparts. Numerical computation introduces further approximations through spatial differences and time stepping, so the accuracy of the computed fields also depends on how the semi-discrete equations are implemented. We therefore wish to use the exact solutions as references for examining how the nonlinear formulation, time integrator and mesh influence the resulting errors.

In Section 2, starting from the continuous bilinear formulation and Gram determinant solutions presented by Sheng and Yu [5], we introduce a semi-discrete bilinear system by combining a staggered lattice in $y$ with shifts of the bilinear operator parameter. We first prove that the proposed Gram determinants satisfy this system, using an identity between adjacent layers. We then derive two nonlinear formulations. The first, the potential-elimination formulation (PE), eliminates an auxiliary potential; the second, the potential formulation (PF), retains it. For both formulations, we establish the reconstruction of the physical fields and derive Darboux–Lax representations whose compatibility conditions yield the corresponding nonlinear equations. The continuum-limit analysis then connects this construction to the original DLW system. We prove second-order consistency of the equations and, for fixed regular spectral parameters and positive $\tau$ functions on the compact sets considered, second-order convergence of the reconstructed exact solutions. An explicit expression for their leading difference identifies how the lattice modifies the continuous wave fields.

In Section 3, we examine the numerical methods through four soliton tests: two single-soliton cases with opposite signs of the $u$ pulse, and two two-soliton cases covering interactions between waves of the same and opposite polarities in $u$. These cases provide exact references for examining the numerical methods across different wave profiles and interaction patterns. We formulate spatial discretizations for PE and PF, together with a direct finite-difference approximation of the continuous equations. To understand the contribution from the $x$ discretization, we derive the leading $O(\Delta x^2)$ truncation terms in the reconstructed $u$ evolution for PE and direct finite differences on a fixed grid. We also introduce a self-adaptive moving mesh method based on a conservation law of the semi-discrete system. The method evolves the physical fields and node positions together, using the transversely averaged conservation density to redistribute the shared $x$ nodes while retaining a uniform lattice in $y$. We then describe the time integration methods and specify the test problems and error measures. Finally, we discuss how the nonlinear formulation, time integration and mesh adaptation affect the errors in both physical fields, drawing on the analytical expansions to interpret the numerical results.
'''
intro_zh = r'''
浅水中波的传播与相互作用长期以来受到非线性波研究的关注。在波的演化过程中，非线性效应与色散以不同方式影响波形，而二者的平衡能够支持在传播中持续存在的相干波。非线性长波方程以约化形式描述这些效应，使我们能够研究波动，而不必保留底层流体方程的全部复杂性。在这类方程中，可积模型因其提供的解析认识而持续受到关注。其精确解使我们能够追踪单个波的演化并考察波间相互作用，双线性形式与 Lax 表示则揭示了这些解背后的数学结构。这些解析结果也为数值研究提供了有用参照，其中波形及其演化需要在离散网格上表示。从连续模型转向这一表示时，所作的选择既影响波的逼近，也影响所得方程的数学结构。可积离散化旨在保留这两方面的联系，将离散方程的构造与其精确解及连续极限的研究结合起来。

（2+1）维色散长波（DLW）系统将色散长波方程推广到两个空间维度 [1]，并被用于研究宽水道及有限深外海中的波动 [3,4]。自 Boiti、Leon 与 Pempinelli 提出这一系统以来，研究者通过若干相互关联的解析方法研究其波解。最初的工作建立了逆谱变换、Bäcklund 变换及叠加公式 [1]；随后发展的非线性变换 [2] 与双线性方法 [3]，为生成解和理解解之间的联系提供了进一步的途径。行列式表示使这些联系具有了具体的表达形式。Hu、Xu 与 Yu 构造了 Grammian 和 Wronskian 解 [4]，而 Sheng 与 Yu 通过 KP 层级约化，得到了描述常值与周期背景上孤子、线呼吸子及有理波的 Gram 行列式解 [5]。

这些解所满足的双线性关系，也为引入格点提供了出发点 [16]。在这一思路下，Bäcklund 变换将相邻格点上的取值联系起来，使离散方程能够与其解结构一同构造。这一方法已用于半离散孤子方程 [7]，并推广到具有两个空间维度的系统 [8]。对于 DLW 系统，它与（2+1）维 sinh-Gordon 方程之间的双线性关系 [5] 又提供了一条联系：后者的可积离散化具有行列式解及 Bäcklund–Lax 结构 [6]。结合已有的离散 DLW 系统研究 [12]，这些进展促使我们进一步考察，如何将连续 DLW 解族引入空间格点，以及由此得到的波场与连续波场之间有怎样的对应关系。

随着这些进展，我们有望在同一构造中研究可积结构的保留与连续波的逼近。带着这一考虑，我们提出如下问题：如何引入空间格点，使其保留双线性与行列式结构，支持一致的物理场重构，并允许对其精确解与连续系统精确解进行定量比较？

围绕这一问题，我们希望得到 DLW 系统沿 $y$ 方向的半离散描述，同时保持 $x$ 与 $t$ 连续。首先，我们希望保留显式波解与支持其演化的可积结构之间的联系。更具体而言，我们寻求能够显式表达离散波场、便于解析研究的 Gram 行列式解。相应的 Lax 表示则应通过其相容条件描述同一非线性演化。其次，我们希望理解将连续波表示在格点上时发生了什么变化。这需要定量比较重构物理场，而不止是在极限中恢复连续方程。这样的比较能够揭示离散波如何趋近其连续对应。数值计算还会通过空间差分与时间推进引入进一步的近似，因此计算场的精度也取决于半离散方程的实现方式。由此，我们希望以精确解为参照，考察非线性表示、时间积分器与网格如何影响所得误差。

在第 2 节，我们从 Sheng 与 Yu [5] 给出的连续双线性形式及 Gram 行列式解出发，将 $y$ 方向的交错格点与双线性算子参数的平移相结合，引入半离散双线性系统。我们首先利用相邻层之间的恒等式，证明所提出的 Gram 行列式满足这一系统。随后，我们导出两种非线性表示：第一种为消去辅助势的差分消势形式（PE），第二种为保留辅助势的势函数形式（PF）。对于两种表示，我们建立物理场重构，并导出相容条件给出相应非线性方程的 Darboux–Lax 表示。连续极限分析进一步将这一构造与原 DLW 系统联系起来。我们证明方程的二阶相容性，并在固定正则谱参数、所考察紧集上 $\tau$ 函数为正的条件下，证明重构精确解的二阶收敛。二者之差首项的显式表达说明了格点如何改变连续波场。

在第 3 节，我们通过四组孤子算例考察数值方法：两组单孤子算例中 $u$ 脉冲符号相反，两组双孤子算例则涵盖 $u$ 场中同极性与异极性波的相互作用。这些算例提供精确参照，使我们能够在不同波形及相互作用模式下考察数值方法。我们建立 PE、PF 的空间离散，以及连续方程的直接有限差分近似。为理解 $x$ 方向离散的影响，我们在固定网格上推导 PE 与直接差分的重构 $u$ 演化中首项为 $O(\Delta x^2)$ 的截断项。我们还基于半离散系统的守恒律引入自适应动网格方法。该方法联立演化物理场与节点位置，利用横向平均守恒密度重新分配共享的 $x$ 节点，同时保留 $y$ 方向的均匀格点。随后，我们介绍时间积分方法，并明确算例与误差度量。最后，我们讨论非线性表示、时间积分与网格自适应如何影响两个物理场的误差，并结合解析展开解释数值结果。
'''

overview_en = r'''In this section, we develop a semi-discrete DLW system by bringing its bilinear equations, exact solutions and physical-field reconstruction into a consistent construction. In Section 2.1, we recall the continuous bilinear formulation and Gram determinant solutions of Sheng and Yu [5], together with the transformation relating the τ functions to the physical fields. Building on these relations, in Section 2.2, we introduce a staggered lattice in $y$ and couple lattice shifts to shifts of the bilinear parameter, while keeping $x$ and $t$ continuous. In Section 2.3, we construct the corresponding Gram determinant solutions and establish that they satisfy the semi-discrete bilinear equations. In Section 2.4, we turn to the physical fields and derive two nonlinear formulations by eliminating or retaining an auxiliary potential, making the reconstruction explicit in each case. In Section 2.5, we examine the continuum limit of both the equations and their exact solutions to determine how the lattice system recovers the continuous DLW dynamics and how its wave fields approach their continuous counterparts. Finally, in Section 2.6, we derive Darboux–Lax representations and verify that their compatibility conditions yield the corresponding nonlinear equations.'''
overview_zh = r'''本节中，我们将双线性方程、精确解与物理场重构纳入一致的构造，建立 DLW 系统的半离散形式。在第 2.1 节，我们回顾 Sheng 与 Yu [5] 给出的连续双线性形式及 Gram 行列式解，以及联系 τ 函数与物理场的变换。在这些关系的基础上，我们在第 2.2 节沿 $y$ 方向引入交错格点，将格点平移与双线性参数的平移相结合，同时保持 $x$ 与 $t$ 连续。在第 2.3 节，我们构造相应的 Gram 行列式解，并证明它们满足半离散双线性方程。在第 2.4 节，我们转向物理场，通过消去或保留辅助势导出两种非线性表示，并分别明确其重构关系。在第 2.5 节，我们考察方程及其精确解的连续极限，以确定格点系统如何恢复连续 DLW 动力学，以及其波场如何趋近相应的连续波场。最后，在第 2.6 节，我们导出 Darboux–Lax 表示，并验证其相容条件给出相应的非线性方程。'''

def prelim(lang):
    en = lang == 'en'
    chunks = [
        r'''Our aim here is to identify the relations we will carry from the continuous DLW system into its semi-discrete counterpart. Specifically, we seek a description in which we can construct exact solutions and recover the physical wave fields from them, so that both remain connected when we introduce a lattice. For this purpose, we revisit the bilinear formulation and Gram determinant solutions of Sheng and Yu [5], paying particular attention to the transformation between the τ functions and the physical fields. Following their normalization, we set $\lambda=-2$ and write the continuous system as''' if en else r'''这里，我们希望明确连续 DLW 系统中哪些关系将被引入相应的半离散系统。具体而言，我们寻求一种既能构造精确解、又能由这些解恢复物理波场的表示，使二者在引入格点后仍保持联系。为此，我们回顾 Sheng 与 Yu [5] 的双线性形式及 Gram 行列式解，着重说明 τ 函数与物理场之间的变换。沿用其归一化形式，我们取 $\lambda=-2$，将连续系统写为''',
        eq(lang,1),
        r'''where $a\in\mathbb R$ is a constant. We work with two sufficiently smooth, positive τ functions $f$ and $g$ and recover the physical fields through''' if en else r'''其中 $a\in\mathbb R$ 为常数。我们采用两个充分光滑的正 τ 函数 $f$ 与 $g$，并通过以下变换恢复物理场：''',
        eq(lang,2),
        r'''This transformation allows us to construct the wave fields through relations between $f$ and $g$. In particular, we use the bilinear equations [5]''' if en else r'''这一变换使我们能够通过 $f$ 与 $g$ 之间的关系构造波场。具体而言，我们采用文献 [5] 中的双线性方程''',
        eq(lang,3),
        r'''where $B_s=D_x^2+D_t+2sD_x$. We retain the parameter $s$ in this notation because shifts of this parameter will enter the lattice construction in Section 2.2. To fix our notation, we define the Hirota bilinear operators by''' if en else r'''其中 $B_s=D_x^2+D_t+2sD_x$。我们在这一记号中保留参数 $s$，因为该参数的平移将参与第 2.2 节的格点构造。为明确记号，我们将 Hirota 双线性算子定义为''',
        eq(lang,4),
        r'''where $r,s,m$ are nonnegative integers. We first state how solutions of the bilinear equations yield solutions of the physical-field equations.

**Proposition 2.1 (Bilinear representation [5]).** If sufficiently smooth positive functions $f,g$ satisfy [(3)](#en-eq-3), the fields defined by [(2)](#en-eq-2) solve the DLW system [(1)](#en-eq-1).

**Proof.** We divide the bilinear equations by $fg$, expand the Hirota operators in logarithmic derivatives, and substitute [(2)](#en-eq-2). This gives the two equations in [(1)](#en-eq-1); see [5, Section 2]. □

Having established this connection, we recall the continuous Gram determinant solutions of [5]. We use this family both as a guide to the semi-discrete determinant construction and as a reference for comparing the reconstructed wave fields in the continuum limit. The τ functions take the form''' if en else r'''其中 $r,s,m$ 均为非负整数。下面，我们首先说明如何由双线性方程的解得到物理场方程的解。

**命题 2.1（双线性表示 [5]）。** 若充分光滑的正函数 $f,g$ 满足双线性方程 [(3)](#zh-eq-3)，则由变换 [(2)](#zh-eq-2) 定义的物理场满足 DLW 系统 [(1)](#zh-eq-1)。

**证明。** 我们将双线性方程除以 $fg$，用对数导数展开 Hirota 算子，再代入变换 [(2)](#zh-eq-2)，即可得到系统 [(1)](#zh-eq-1) 中的两个方程，参见 [5, Section 2]。□

在明确这一联系后，我们回顾文献 [5] 中的连续 Gram 行列式解。我们将以这一解族指导半离散行列式的构造，并以其作为连续极限中比较重构波场的参照。τ 函数具有如下形式：''',
        eq(lang,5), 'with phases' if en else '其中相位为', eq(lang,6),
        r'''Here $N$ is the determinant order, $n$ is an auxiliary integer index, and $\delta_{ik}$ is the Kronecker delta. We choose the real parameters so that all displayed denominators are nonzero and restrict the physical fields to regions where $f$ and $g$ are positive. The following proposition confirms that this determinant family satisfies the bilinear equations used in our reconstruction.

**Proposition NEWCONT (Continuous Gram determinant solutions [5]).** Let $\tau_n^{(0)}$ be defined by (5)–(6), with parameters chosen so that all displayed denominators are nonzero. Then $f=\tau_1^{(0)}$ and $g=\tau_0^{(0)}$ satisfy the bilinear equations [(3)](#en-eq-3). Consequently, on any region where $f$ and $g$ are positive, the fields reconstructed through [(2)](#en-eq-2) solve the continuous DLW system [(1)](#en-eq-1).

**Proof.** The bilinear identities for this Gram determinant family follow from the KP-hierarchy reduction established in [5]. With $f=\tau_1^{(0)}$ and $g=\tau_0^{(0)}$, these identities give [(3)](#en-eq-3). The statement for the reconstructed physical fields then follows from Proposition 2.1. □

We therefore have an explicit solution family in which the τ functions and the physical fields are linked by the bilinear equations and the reconstruction formulas. In the next subsection, we use the $y$-dependence of this family to guide the lattice construction, seeking to preserve these relations in the semi-discrete setting.''' if en else r'''这里，$N$ 为行列式阶数，$n$ 为辅助整数指标，$\delta_{ik}$ 为 Kronecker 符号。我们选取实参数，使上述各分母均不为零，并将物理场限制在 $f$ 与 $g$ 均为正的区域内。下面的命题说明，这一行列式解族满足物理场重构所依据的双线性方程。

**命题 NEWCONT（连续 Gram 行列式解 [5]）。** 设 $\tau_n^{(0)}$ 由公式 (5)–(6) 定义，且参数选取使上述各分母均不为零，则 $f=\tau_1^{(0)}$ 与 $g=\tau_0^{(0)}$ 满足双线性方程 [(3)](#zh-eq-3)。因此，在 $f$ 与 $g$ 均为正的任意区域内，通过变换 [(2)](#zh-eq-2) 重构的物理场满足连续 DLW 系统 [(1)](#zh-eq-1)。

**证明。** 这一 Gram 行列式解族所满足的双线性恒等式由文献 [5] 中的 KP 层级约化得到。取 $f=\tau_1^{(0)}$ 与 $g=\tau_0^{(0)}$，这些恒等式即给出方程 [(3)](#zh-eq-3)。随后，由命题 2.1 可知，重构出的物理场满足连续 DLW 系统。□

至此，我们得到了一族显式解，其中 τ 函数与物理场通过双线性方程及重构公式相联系。下一小节中，我们将利用这一解族对 $y$ 的依赖来指导格点构造，以期在半离散情形下保留这些关系。'''
    ]
    return '\n\n'.join(chunks)

def bilinear(lang):
    en = lang == 'en'
    return '\n\n'.join([
        r'''Building on the continuous bilinear formulation, we now seek to introduce a spatial lattice while preserving its connection with the determinant solutions. Specifically, we aim to retain a structure that supports explicit wave solutions and a consistent reconstruction of the physical fields. The lattice equations should also recover the continuous bilinear system as the spacing tends to zero. With these requirements in mind, we begin by examining how the two equations in (3) are related, using this connection to guide our choice of discrete shifts.

In particular, we focus on how the $y$-dependence enters the bilinear system. The first equation involves only derivatives in $x$ and $t$, whereas the second connects variation in $y$ to the same operator $B_a$. This shared structure suggests a way to introduce a lattice in $y$ while keeping $x$ and $t$ continuous. To develop this idea, we first rewrite the equations so that the relation between differentiation in $y$ and variation of the operator parameter becomes explicit. Differentiating the first equation in (3) with respect to $y$ and combining it with the second, we obtain''' if en else r'''在连续双线性形式的基础上，我们希望引入空间格点，同时保留这一形式与行列式解之间的联系。具体而言，我们希望保留能够支持显式波解及一致物理场重构的结构。格点方程还应在间距趋于零时恢复连续双线性系统。带着这些要求，我们首先考察方程组 (3) 中两式之间的联系，并以此指导离散平移的选取。

具体而言，我们关注 $y$ 方向的依赖如何进入双线性系统。第一式仅涉及 $x$ 与 $t$ 的导数，第二式则通过同一个算子 $B_a$ 联系 $y$ 方向的变化。这一共同结构启发我们沿 $y$ 方向引入格点，同时保持 $x$ 与 $t$ 连续。为展开这一思路，我们首先改写方程，使 $y$ 方向求导与算子参数变化之间的关系显现出来。对 (3) 的第一式关于 $y$ 求导，再结合第二式，我们得到''',
        eq(lang,7),
        r'''Together with $B_af\cdot g=0$, this relation is equivalent to the continuous bilinear system (3). The two terms in (7) suggest shifting the second τ function and the operator parameter together. We therefore introduce''' if en else r'''将这一关系与 $B_af\cdot g=0$ 联立，即得到与连续双线性系统 (3) 等价的表示。公式 (7) 中的两项启发我们同时平移第二个 τ 函数与算子参数。因此，我们引入''',
        eq(lang,8),
        r'''Since $B_{a+s}=B_a+2sD_x$, we have

$$\Phi(0)=B_af\cdot g,\qquad \Phi'(0)=B_af\cdot g_y+2D_xf\cdot g.$$

We can thus express the continuous bilinear equations as the two conditions $\Phi(0)=0$ and $\Phi'(0)=0$. This observation motivates a symmetric lattice construction: we replace these conditions by two bilinear relations corresponding to the shifts $s=-h/2$ and $s=h/2$.

For $h>0$ and $j\in\mathbb Z$, we place $F_j(x,t)$ at $y=(j+\tfrac12)h$ and $G_j(x,t)$ at $y=jh$, keeping $x$ and $t$ continuous. Relative to $F_j$, the adjacent functions $G_j$ and $G_{j+1}$ then occupy the two symmetric positions. We pair these offsets with the parameter values $a-h/2$ and $a+h/2$, and propose the semi-discrete bilinear system''' if en else r'''由于 $B_{a+s}=B_a+2sD_x$，我们有

$$\Phi(0)=B_af\cdot g,\qquad \Phi'(0)=B_af\cdot g_y+2D_xf\cdot g.$$

这样，连续双线性方程便可表示为 $\Phi(0)=0$ 与 $\Phi'(0)=0$ 两个条件。这一观察启发我们采用对称的格点构造：用分别对应 $s=-h/2$ 与 $s=h/2$ 的两条双线性关系替代这两个条件。

对于 $h>0$ 和 $j\in\mathbb Z$，我们将 $F_j(x,t)$ 放置在 $y=(j+\tfrac12)h$，将 $G_j(x,t)$ 放置在 $y=jh$，并保持 $x,t$ 连续。相对于 $F_j$，相邻的 $G_j$ 与 $G_{j+1}$ 恰好位于两个对称位置。我们将这两个偏移分别与参数值 $a-h/2$、$a+h/2$ 配对，由此提出半离散双线性系统''',
        eq(lang,9),
        r'''Here $F_j$ and $G_j$ are unknown lattice τ functions. Their positions specify how we compare them with the continuous functions $f$ and $g$; they do not require the lattice functions to equal samples of a continuous solution. We construct exact Gram determinant solutions of (9) in Section 2.3 and establish their convergence under this staggered identification in Section 2.5.

To check the local consistency of the proposed relations, we return to (8) and expand about $s=0$. For sufficiently smooth $f$ and $g$, symmetric Taylor expansion gives''' if en else r'''这里，$F_j$ 与 $G_j$ 是待求的格点 τ 函数。它们的位置规定了与连续函数 $f,g$ 进行比较时的对应方式，并不要求格点函数等于连续解在相应位置的采样值。我们将在第 2.3 节构造系统 (9) 的精确 Gram 行列式解，并在第 2.5 节建立这一交错对应下的收敛性。

为检验所提出关系的局部相容精度，我们回到公式 (8)，在 $s=0$ 附近展开。当 $f,g$ 充分光滑时，对称 Taylor 展开给出''',
        eq(lang,10),
        r'''The symmetric average and difference quotient therefore recover the first equation in (3) and the equivalent relation (7) with second-order consistency. This establishes the connection with the continuous bilinear system. We next examine whether the proposed lattice relations also admit a corresponding determinant solution family.''' if en else r'''因此，对称平均与差商分别以二阶相容精度恢复 (3) 的第一式及等价关系 (7)，从而建立与连续双线性系统的联系。接下来，我们进一步考察所提出的格点关系是否也具有相应的行列式解族。'''
    ])

def gram(lang):
    en = lang == 'en'
    return '\n\n'.join([
        r'''We now turn to the exact solutions of the semi-discrete bilinear system (9). To construct them, we adapt the continuous Gram determinants in (5), preserving their dependence on $x$ and $t$ while replacing the $y$-dependent exponential factors by lattice factors. The choice of these factors connects the determinant formula to the equations derived above: they must accommodate the coupled lattice and parameter shifts in (9), while approaching the continuous exponential factors as $h\to0$. We therefore look for a form that allows us to establish both the bilinear identities and the correspondence with the continuous solution family.

We choose the lattice factor

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad d=\frac h2.$$

For fixed nonzero $z$ and sufficiently small $h$, its expansion gives

$$\log\lambda_h(z)=\frac hz+O(h^3).$$

Consequently, $\lambda_h(z)^j$ approaches $e^{y/z}$ as $h\to0$ with $jh=y$ fixed. We can therefore replace the continuous $y$-dependent exponentials by powers of this factor. Its numerator and denominator also contain the same half-step offsets that appear in the operator parameters of (9), allowing us to relate the lattice shift to the parameter shift in the determinant identities below.

With this choice, we define''' if en else r'''现在，我们转向半离散双线性系统 (9) 的精确解。为构造这些解，我们调整公式 (5) 中的连续 Gram 行列式，保留其对 $x$ 与 $t$ 的依赖，同时将依赖于 $y$ 的指数因子替换为格点因子。这些因子的选取将行列式公式与前面导出的方程联系起来：它们既需要适应方程 (9) 中格点与参数的耦合平移，也应在 $h\to0$ 时趋于连续指数因子。因此，我们希望找到一种形式，使双线性恒等式的验证与连续解族之间对应关系的建立都能在其中展开。

我们选取格点因子

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad d=\frac h2.$$

对于固定的非零 $z$ 和充分小的 $h$，展开可得

$$\log\lambda_h(z)=\frac hz+O(h^3).$$

因此，当 $h\to0$ 且 $jh=y$ 保持固定时，$\lambda_h(z)^j$ 趋于 $e^{y/z}$。由此，我们可以用这一因子的整数次幂替换连续形式中依赖于 $y$ 的指数因子。它的分子与分母还包含与方程 (9) 中算子参数相同的半步偏移，使我们能够在下面的行列式恒等式中联系格点平移与参数平移。

据此，我们定义''',
        eq(lang,11),
        r'''Here $\delta_{ik}$ is the Kronecker delta. We retain the auxiliary index $n$ to establish bilinear identities between adjacent members of the sequence, and the parameter $s$ to accommodate the two operators in (9). For $n=0$, the determinant is independent of $s$, so we write $\tau_0(j;s)=\tau_0(j)$. The following theorem identifies the members that give the required lattice τ functions.

**Theorem 2.2 (Gram determinant solutions).** Let $h>0$, $N\ge1$, and let $p_i,q_i,\rho_i$ be real parameters satisfying $p_i+q_k\ne0$, $p_i-a\pm d\ne0$ and $q_k+a\pm d\ne0$ for all $i,k$. Then the functions''' if en else r'''其中，$\delta_{ik}$ 为 Kronecker 符号。我们保留辅助指标 $n$，以建立序列中相邻成员之间的双线性恒等式；同时保留参数 $s$，以处理方程 (9) 中的两个算子。当 $n=0$ 时，行列式与 $s$ 无关，因此记作 $\tau_0(j;s)=\tau_0(j)$。下面的定理明确了应选取哪些成员作为所需的格点 τ 函数。

**定理 2.2（Gram 行列式解）。** 设 $h>0$、$N\ge1$，实参数 $p_i,q_i,\rho_i$ 对所有 $i,k$ 满足 $p_i+q_k\ne0$、$p_i-a\pm d\ne0$ 及 $q_k+a\pm d\ne0$。则函数''',
        eq(lang,12),
        r'''satisfy the semi-discrete bilinear system [(9)](#en-eq-9) at every lattice site $j\in\mathbb Z$.

To prove this result, we first establish a bilinear identity between adjacent $n$-layers at a fixed lattice site. This identity gives the first equation in (9) directly. For the second, we show that shifting the lattice index from $j$ to $j+1$, together with the parameter from $a-d$ to $a+d$, leaves the determinant defining $F_j$ unchanged. We can then apply the same identity at the neighbouring site.

**Lemma 2.3 (Adjacent-layer identity).** Under the spectral conditions of Theorem 2.2, fix a lattice site $j$ and a parameter $s$ such that $p_i-s\ne0$ and $q_k+s\ne0$ for all $i,k$. Then, for every $n\in\mathbb Z$,''' if en else r'''在每个格点 $j\in\mathbb Z$ 上均满足半离散双线性系统 [(9)](#zh-eq-9)。

为证明这一结果，我们首先在固定格点处建立相邻 $n$ 层之间的双线性恒等式。该恒等式直接给出方程组 (9) 的第一式。对于第二式，我们将证明：当格点指标由 $j$ 移至 $j+1$，同时参数由 $a-d$ 变为 $a+d$ 时，定义 $F_j$ 的行列式保持不变。这样，我们便可以在相邻格点处应用同一恒等式。

**引理 2.3（相邻层恒等式）。** 在定理 2.2 的谱条件下，固定格点 $j$，并选取参数 $s$，使所有 $i,k$ 均满足 $p_i-s\ne0$ 与 $q_k+s\ne0$。则对每个 $n\in\mathbb Z$，均有''',
        eq(lang,13),
        r'''**Proof.** We use the matrix determinant lemma and the rank-one identities obtained by differentiating the determinant entries to establish (13). The detailed calculation is given in [Appendix B](#en-app-b), where we also extend the identity to points at which the matrices defining the τ functions are singular. □

**Proof of Theorem 2.2.** We first apply (13) at the lattice site $j$, with $n=0$ and $s=a-d$. Since $\tau_0(j;s)$ is independent of $s$, the definitions in (12) give

$$B_{a-d}F_j\cdot G_j=B_{a-d}\tau_1(j;a-d)\cdot\tau_0(j)=0.$$

This is the first equation in (9).

To obtain the second equation, we need to pair $F_j$ with $G_{j+1}$ under the operator $B_{a+d}$. The required connection follows from the choice of lattice factors:''' if en else r'''**证明。** 我们利用矩阵行列式引理，以及对行列式元素求导得到的秩一恒等式，建立公式 (13)。详细计算见[附录 B](#zh-app-b)，其中还将这一恒等式延拓到定义 τ 函数的矩阵为奇异矩阵的情形。□

**定理 2.2 的证明。** 首先，我们在格点 $j$ 处应用恒等式 (13)，取 $n=0$ 与 $s=a-d$。由于 $\tau_0(j;s)$ 与 $s$ 无关，根据定义 (12)，可得

$$B_{a-d}F_j\cdot G_j=B_{a-d}\tau_1(j;a-d)\cdot\tau_0(j)=0.$$

这就得到了方程组 (9) 的第一式。

为得到第二式，我们需要在算子 $B_{a+d}$ 下将 $F_j$ 与 $G_{j+1}$ 配对。所需的联系来自格点因子的选取：''',
        eq(lang,14),
        'Using this identity in each entry of the determinant, we find' if en else '将这一恒等式应用于行列式的各个元素，我们得到',
        eq(lang,15),
        r'''Thus, the same function $F_j$ can be represented at the neighbouring site $j+1$, provided that the parameter is shifted from $a-d$ to $a+d$. Applying (13) at that site with $n=0$ and $s=a+d$, we obtain''' if en else r'''因此，只要将参数从 $a-d$ 同步移至 $a+d$，同一个函数 $F_j$ 就可以用相邻格点 $j+1$ 处的行列式表示。在该格点处取 $n=0$、$s=a+d$，再次应用恒等式 (13)，便得到''',
        eq(lang,16),
        r'''This proves the second equation in (9) and completes the proof. □

The identity (15) explains how the determinant construction accommodates the two shifted operators in the bilinear system. We can now use these τ functions to reconstruct the physical fields. Before doing so, we give a sufficient condition for their positivity, ensuring that the logarithms in the reconstruction remain well defined.

The determinant identities above establish the bilinear equations without requiring the τ functions to be positive. To reconstruct real physical fields through logarithmic derivatives, however, we work on regions where both $F_j$ and $G_j$ are positive. We now give a sufficient parameter condition that ensures this property for all $x,t$ and every lattice site.

**Proposition 2.4 (Positive τ functions).** Suppose $0<p_1<\cdots<p_N<a-h/2$, $0<q_1<\cdots<q_N$ and $\rho_i>0$. Then the τ functions defined by (12) satisfy $F_j\ge1$ and $G_j\ge1$ for all $x,t\in\mathbb R$ and $j\in\mathbb Z$.

**Proof.** Under these conditions, the lattice factors $\lambda_h(p_i-a)$ and $\lambda_h(q_k+a)$ are positive. The additional factor in $F_j$ is also positive, since

$$-\frac{p_i-a+d}{q_k+a-d}>0.$$

We can therefore write each matrix defining $F_j$ or $G_j$ as $I+D_1CD_2$, where $C_{ik}=1/(p_i+q_k)$ and $D_1,D_2$ are positive diagonal matrices. For any nonempty index set $I\subseteq\{1,\ldots,N\}$, the Cauchy determinant formula gives''' if en else r'''这证明了方程组 (9) 的第二式，定理得证。□

恒等式 (15) 说明了行列式构造如何适应双线性系统中的两个移位算子。现在，我们可以利用这些 τ 函数重构物理场。在此之前，我们先给出保证其为正的一个充分条件，使重构中的对数保持良好定义。

上述行列式恒等式在不要求 τ 函数为正的情况下，就能保证双线性方程成立。不过，为通过对数导数重构实值物理场，我们将在 $F_j$ 与 $G_j$ 均为正的区域内进行讨论。下面，我们给出一个充分的参数条件，使这一性质对所有 $x,t$ 以及每个格点都成立。

**命题 2.4（正 τ 函数）。** 假设 $0<p_1<\cdots<p_N<a-h/2$、$0<q_1<\cdots<q_N$ 且 $\rho_i>0$。则由公式 (12) 定义的 τ 函数对所有 $x,t\in\mathbb R$ 和 $j\in\mathbb Z$ 均满足 $F_j\ge1$、$G_j\ge1$。

**证明。** 在这些条件下，格点因子 $\lambda_h(p_i-a)$ 与 $\lambda_h(q_k+a)$ 均为正。$F_j$ 中额外的因子也为正，因为

$$-\frac{p_i-a+d}{q_k+a-d}>0.$$

因此，我们可以将定义 $F_j$ 或 $G_j$ 的矩阵分别写成 $I+D_1CD_2$，其中 $C_{ik}=1/(p_i+q_k)$，$D_1,D_2$ 均为正对角矩阵。对于任意非空指标集 $I\subseteq\{1,\ldots,N\}$，Cauchy 行列式公式给出''',
        eq(lang,17),
        r'''Multiplication by the positive diagonal matrices preserves the positivity of these principal minors. We then expand $\det(I+D_1CD_2)$ as the sum of all principal minors of $D_1CD_2$, together with the empty minor $1$. Every nonempty contribution is positive, which proves the stated bounds. □

This condition gives a parameter range in which the τ functions remain positive throughout the lattice evolution. It is sufficient rather than necessary; outside this range, we may still reconstruct the physical fields wherever both τ functions are positive. With the determinant solutions and their regularity conditions established, we turn to the nonlinear equations governing the reconstructed fields.''' if en else r'''左右乘以正对角矩阵后，这些主子式仍保持为正。随后，我们将 $\det(I+D_1CD_2)$ 展开为 $D_1CD_2$ 的全部主子式之和，并计入取值为 $1$ 的空主子式。每个非空项均为正，因此得到所述下界。□

这一条件给出了 τ 函数在整个格点演化过程中保持为正的参数范围。它是充分条件，并非必要条件；在这一范围之外，只要两个 τ 函数在所考虑区域内均为正，我们仍可重构物理场。在建立行列式解及其正则性条件之后，我们接下来转向控制重构物理场演化的非线性方程。'''
    ])

text = original
for lang,intro,overview in [('en',intro_en,overview_en),('zh',intro_zh,overview_zh)]:
    text = replace_section(text,lang+'-intro',intro)
    # The Section 2 overview ends at its first subsection.
    text = replace_section(text,lang+'-continuous',overview)
    text = replace_section(text,lang+'-preliminaries',prelim(lang))
    text = replace_section(text,lang+'-bilinear',bilinear(lang))
    text = replace_section(text,lang+'-gram',gram(lang))
    a,b=section(text,lang+'-nonlinear')
    old=text[a:b]
    cut=old.index('Let $\\alpha_j') if lang=='en' else old.index('令 $\\alpha_j')
    heading=old[:old.index('\n')]
    opening = r'''We now turn from the bilinear equations to the evolution of the physical fields. Our aim is to express the semi-discrete system in variables that can be compared with the continuous fields $u$ and $v$, while retaining the exact solutions constructed above. This requires a reconstruction that accounts for the staggered positions of $F_j$ and $G_j$. We first define the fields on this lattice and derive their evolution from the two bilinear equations. The resulting relations then lead to two nonlinear formulations, according to whether we eliminate an auxiliary potential or retain it.

At the location of $F_j$, the neighbouring functions $G_j$ and $G_{j+1}$ lie symmetrically on either side. We therefore use their average logarithm to define $u_j$, and introduce $\omega_j$ to describe the change in the logarithmic $x$-derivative between these neighbouring sites. For positive τ functions, we set''' if lang=='en' else r'''现在，我们从双线性方程转向物理场的演化。我们希望用能够与连续物理场 $u,v$ 进行比较的变量表示半离散系统，同时保留前面构造的精确解。为此，物理场重构需要考虑 $F_j$ 与 $G_j$ 的交错位置。我们首先在这一格点上定义物理场，再从两条双线性方程导出其演化关系。随后，根据辅助势的消去或保留，这些关系将引出两种非线性表示。

在 $F_j$ 所在位置的两侧，相邻函数 $G_j$ 与 $G_{j+1}$ 对称分布。因此，我们利用二者对数的平均值定义 $u_j$，并引入 $\omega_j$，描述相邻格点之间对数 $x$ 导数的变化。对于正 τ 函数，我们采用如下定义：'''
    after = r'''We associate the reconstructed fields $u_j$ and $v_j$ with $y=(j+\tfrac12)h$. The definition of $v_j$ follows the continuous identity

$$v=4(\log g)_{xy}+u_y,$$

which is obtained directly from (2). In (18), $4\omega_j/h$ approximates $4(\log g)_{xy}$, while $\delta_0u_j$ approximates $u_y$. These relations give a discrete counterpart of the continuous field transformation; we establish their second-order consistency in Section 2.5. For the derivation below, we work with $u_j$ and $\omega_j$, recovering $v_j$ through (18).''' if lang=='en' else r'''我们将重构出的物理场 $u_j,v_j$ 对应于 $y=(j+\tfrac12)h$。其中，$v_j$ 的定义依据连续恒等式

$$v=4(\log g)_{xy}+u_y,$$

它可由变换 (2) 直接得到。在公式 (18) 中，$4\omega_j/h$ 逼近 $4(\log g)_{xy}$，而 $\delta_0u_j$ 逼近 $u_y$。这些关系构成了连续物理场变换的离散对应，其二阶相容性将在第 2.5 节建立。在下面的推导中，我们采用 $u_j,\omega_j$ 作为变量，再通过公式 (18) 恢复 $v_j$。'''
    text=text[:a]+heading+'\n\n'+opening+'\n\n'+eq(lang,18)+'\n\n'+after+'\n\n'+old[cut:]+text[b:]

# Preserve the reviewed moving-mesh background in its agreed location.
mesh_en = r'''A uniform grid may allocate many points to weakly varying regions while resolving a narrow wave band inadequately. Moving mesh methods address this imbalance by redistributing nodes through a solution-dependent density [15]. For integrable equations, conservation laws offer a direct connection between the solution and the mesh: examples include self-adaptive methods for the Camassa–Holm equation [13], short pulse equations [14] and a generalized sine-Gordon equation [9]. In the present two-dimensional setting, we retain a uniform $y$ lattice and use the same moving $x$ nodes on every transverse layer. We therefore average the conservation density and flux across the layers to determine a shared node distribution. This adapts the $x$ resolution while preserving the tensor-product representation of the fields.'''
mesh_zh = r'''均匀网格可能在变化缓慢的区域分配较多节点，却难以充分分辨狭窄波带。动网格方法通过依赖于解的密度重新分配节点，以改善这种不均衡 [15]。对于可积方程，守恒律提供了解与网格之间的直接联系，相关实例包括 Camassa–Holm 方程 [13]、短脉冲方程 [14] 及广义 sine-Gordon 方程 [9] 的自适应方法。在当前二维情形下，我们保留均匀的 $y$ 格点，并在各横向层共享同一组移动的 $x$ 节点。因此，我们对守恒密度与通量作横向平均，以确定共享的节点分布。这一做法在保持物理场张量积表示的同时，调整 $x$ 方向的分辨率。'''
for lang,mesh in [('en',mesh_en),('zh',mesh_zh)]:
    a,b=section(text,lang+'-samm')
    e=text.index('\n',a)
    text=text[:e+1]+'\n'+mesh+'\n'+text[e+1:]

# Make room for the new continuous-solution proposition; update only result labels,
# never subsection numbers or equation numbers.
text=re.sub(r'((?:Proposition|Theorem|Lemma|命题|定理|引理)\s+)2\.(\d+)\b',lambda m:m[1]+f'2.{int(m[2])+1}' if int(m[2])>=2 else m[0],text)
text=text.replace('NEWCONT','2.2')

# The compressed introduction no longer cites [11]. Remove that bibliography item
# and close the numbering gap while preserving the reference order.
text=re.sub(r'(?m)^\[11\] [^\n]+\n\n','',text)
def cite_shift(m):
    return '['+','.join(str(int(n)-1 if int(n)>=12 else int(n)) for n in m[1].split(','))+']'
text=re.sub(r'\[(\d+(?:,\d+)*)\](?!\()',cite_shift,text)

old_math=[m for m in re.findall(r'\$\$[\s\S]*?\$\$',original) if re.search(r'\\tag\{\d+\}',m)]
new_math=[m for m in re.findall(r'\$\$[\s\S]*?\$\$',text) if re.search(r'\\tag\{\d+\}',m)]
assert old_math==new_math, 'Numbered mathematical displays changed'
assert len(re.findall(r'\*\*(?:Proposition|Theorem|Lemma) 2\.\d+ \(',text))==11
assert len(re.findall(r'\*\*(?:命题|定理|引理) 2\.\d+（',text))==11
assert 'NEWCONT' not in text
path.write_text(text,encoding='utf-8')
(out/'scope_validation.json').write_text(json.dumps({'numbered_equations_unchanged':True,'numbered_displays':len(new_math),'scope':['Introduction','Section 2 overview','2.1–2.3','2.4 opening through reconstruction','3.2 relocated mesh context','result numbering and bibliography references'],'section_3_roadmap_aligned_to_existing_order':True,'bibliography_entries_per_language':15,'backup':str(out)},ensure_ascii=False,indent=2),encoding='utf-8')
print(str(out))
