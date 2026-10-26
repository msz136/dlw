from pathlib import Path
import re, shutil, datetime, json

P=Path(__file__).resolve().parent
root=P.parents[1]
src=P/'manuscript.md'
s=src.read_text(encoding='utf-8')
original=s
backup=P/'discussion_revision_20261019'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
shutil.copy2(src,backup/'manuscript.md')
shutil.copy2(root/'report/dlw_paper_draft.html',backup/'dlw_paper_draft.html')

def replace(old,new):
 global s
 assert s.count(old)==1,(old[:100],s.count(old))
 s=s.replace(old,new)

def gap(lang, left, right, text):
 global s
 # Replace prose between two numbered equation blocks, preserving both equations.
 pat=rf'(<a id="{lang}-eq-{left}"></a>\s*\$\$[\s\S]*?\$\$)[\s\S]*?(?=<a id="{lang}-eq-{right}"></a>)'
 s,n=re.subn(pat,lambda m:m[1]+'\n\n'+text.strip()+'\n\n',s,count=1)
 assert n==1

replace('Let $\\alpha_j=\\log F_j$ and $\\beta_j=\\log G_j$. Dividing the two bilinear equations by $F_jG_j$ and $F_jG_{j+1}$, respectively, gives',r'''To derive the field equations, we introduce the logarithmic variables $\alpha_j=\log F_j$ and $\beta_j=\log G_j$. These variables allow us to expand the bilinear equations in terms of the derivatives that enter the reconstruction formulas. Dividing the two equations in (9) by $F_jG_j$ and $F_jG_{j+1}$, respectively, we obtain''')
replace('令 $\\alpha_j=\\log F_j$、$\\beta_j=\\log G_j$。将两条双线性方程分别除以 $F_jG_j$ 和 $F_jG_{j+1}$，得到',r'''为导出物理场方程，我们引入对数变量 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。通过这些变量，我们可以将双线性方程展开为重构公式中所涉及的导数。将方程组 (9) 的两式分别除以 $F_jG_j$ 和 $F_jG_{j+1}$，得到''')

pairs=[(29,30,r'''Their symmetric form suggests taking the sum and difference of the equations in (19). After differentiation in $x$, the sum produces $u_{j,t}$, while the difference produces $\omega_{j,t}$. We can express the quadratic and first-derivative terms through (20). The second-derivative terms in the sum, however, retain an additional combination of the logarithmic variables. We collect this contribution by defining''',r'''这一对称形式启发我们对方程组 (19) 取和与差。在进一步关于 $x$ 求导后，和式产生 $u_{j,t}$，差式产生 $\omega_{j,t}$。其中，平方项与一阶导数项可以通过公式 (20) 写成 $u_j,\omega_j$ 的形式。不过，和式中的二阶导数项仍保留了对数变量的另一种组合。为集中表示这一部分，我们引入'''),
(30,31,r'''Taking the $x$-derivatives of $A_j+C_j=0$ and $A_j-C_j=0$, and substituting (20)–(21), we arrive at''',r'''随后，对 $A_j+C_j=0$ 与 $A_j-C_j=0$ 分别关于 $x$ 求导，并代入公式 (20)–(21)，便得到'''),
(31,32,r'''The second equation is already expressed in $u_j$ and $\omega_j$, whereas the first still involves $Z_j$. To complete the nonlinear description, we use the reconstruction relations to handle this remaining term in two ways. We first eliminate $Z_j$ by taking a lattice difference. We then develop an alternative formulation that retains a potential through which $Z_j$ and $\omega_j$ can both be expressed.

For the first formulation, we seek equations involving only $u_j$ and $\omega_j$. Although $Z_j$ contains logarithmic derivatives that do not appear separately in these two variables, its difference between adjacent lattice sites can be expressed directly through them. We therefore introduce the backward difference and averaging operators''',r'''第二条方程已经完全由 $u_j,\omega_j$ 表示，而第一条方程仍包含 $Z_j$。为得到完整的非线性表示，我们利用重构关系，以两种方式处理这一剩余项。首先，我们通过格点差分消去 $Z_j$；随后，再构造另一种保留势变量的表示，使 $Z_j$ 与 $\omega_j$ 均可由该势变量表达。

对于第一种表示，我们希望得到仅涉及 $u_j,\omega_j$ 的方程。虽然 $Z_j$ 包含无法在这两个变量中单独体现的对数导数，但它在相邻格点之间的差可以直接由二者表示。因此，我们引入后向差分算子与平均算子'''),
(32,33,r'''From the definitions of $u_j$ and $Z_j$, we have $Z_j-u_j=2(\beta_j+\beta_{j+1})_x$. Taking a backward difference and using $\omega_j=(\beta_{j+1}-\beta_j)_x$, we obtain''',r'''由 $u_j$ 与 $Z_j$ 的定义，我们有 $Z_j-u_j=2(\beta_j+\beta_{j+1})_x$。对此取后向差分，再利用 $\omega_j=(\beta_{j+1}-\beta_j)_x$，得到'''),
(33,34,r'''This identity allows us to remove $Z_j$ after applying $\delta_-$ to the first equation in (22). Keeping the second equation unchanged, we arrive at the potential-elimination formulation (PE):''',r'''这一恒等式使我们能够在对方程组 (22) 的第一式施加 $\delta_-$ 后消去 $Z_j$。保持第二式不变，我们便得到势消去表示（PE）：'''),
(34,35,r'''We have thus removed the auxiliary quantity $Z_j$ through an exact lattice identity, without introducing a further approximation. The resulting equations involve $u_j$ and $\omega_j$, from which we recover the physical field $v_j$ using (18). The elimination places a backward difference on $u_{j,t}$, so recovering the individual time derivatives requires a boundary value or an equivalent normalization in the lattice direction. This feature will enter the numerical implementation of PE.

We next develop a formulation that retains the potential information carried by the τ functions. In this representation, we seek to express both $Z_j$ and $\omega_j$ through a common variable, so that we can use the first equation in (22) without taking a lattice difference. For this purpose, we introduce $M_j=\beta_{j,x}$. The reconstruction relations then give''',r'''这样，我们通过精确的格点恒等式消去了辅助量 $Z_j$，没有引入额外近似。所得方程涉及 $u_j,\omega_j$，物理场 $v_j$ 则通过公式 (18) 恢复。消去操作也使 $u_{j,t}$ 以其后向差分的形式出现，因此，要恢复各格点上的时间导数，需要给定格点方向上的一个边界值或等价的归一化条件。这一特点将在 PE 的数值实现中体现。

接下来，我们构造一种保留 τ 函数中势信息的表示。在这一表示中，我们希望用同一个变量表达 $Z_j$ 与 $\omega_j$，从而无需对方程组 (22) 的第一式取格点差分。为此，我们引入 $M_j=\beta_{j,x}$。由重构关系可得'''),
(35,36,r'''Thus, the difference of neighbouring potential values determines $\omega_j$, while their sum supplies the additional term in $Z_j$.

After substituting (26) into the first equation in (22), we encounter the combination $u_{j,x}+u_j^2/2$ inside an $x$-derivative. This suggests introducing a variable whose logarithmic derivative gives $u_j$. Guided by the τ-function reconstruction, we define''',r'''因此，相邻势值之差决定了 $\omega_j$，而它们的和则给出 $Z_j$ 中除 $u_j$ 之外的部分。

将公式 (26) 代入方程组 (22) 的第一式后，我们发现其 $x$ 导数内部包含组合 $u_{j,x}+u_j^2/2$。这启发我们引入一个变量，使其对数导数给出 $u_j$。根据 τ 函数重构关系，我们定义'''),
(36,37,'With this choice, the derivative and quadratic terms combine as','通过这一选取，导数项与平方项可合并为'),
(37,38,r'''To obtain the evolution equation for $Q_j$, we return to the relation $(A_j+C_j)/2=0$, before differentiation in $x$. This allows us to retain the normalization inherited from the τ functions without introducing an integration function. Substituting (26)–(27), we obtain''',r'''为得到 $Q_j$ 的演化方程，我们回到尚未关于 $x$ 求导的关系 $(A_j+C_j)/2=0$。这样可以保留由 τ 函数确定的归一化，而不必引入积分函数。代入公式 (26)–(27)，便得到'''),
(38,39,r'''We have now expressed the first evolution relation through $Q_j$, the neighbouring potential values, and their difference $\omega_j$. To complete the formulation, we turn to the equation for $\omega_j$. Substituting $u_j=2Q_{j,x}/Q_j$ into its flux gives''',r'''至此，我们已将第一条演化关系写成由 $Q_j$、相邻势值及其差 $\omega_j$ 表示的形式。为完成这一表示，我们转向 $\omega_j$ 的方程。将 $u_j=2Q_{j,x}/Q_j$ 代入其通量，得到'''),
(39,40,r'''The last term couples the logarithmic derivative of $Q_j$ to $\omega_j-h$. We absorb this combination into a companion variable by setting''',r'''其中最后一项将 $Q_j$ 的对数导数与 $\omega_j-h$ 联系起来。我们引入配对变量 $R_j$，将这一组合纳入新的变量表示：'''),
(40,41,r'''Since the positive τ functions give $Q_j>0$, this definition is well defined on the region under consideration. It also simplifies the quadratic term in (29), through the identities''',r'''由于正 τ 函数保证 $Q_j>0$，这一定义在所考虑区域内是良好定义的。同时，它也通过以下恒等式简化了公式 (29) 中的二次项：'''),
(41,42,r'''Using (31)–(32), we rewrite the $\omega_j$ equation as an evolution equation for the product $Q_jR_j$:''',r'''利用公式 (31)–(32)，我们将 $\omega_j$ 方程改写为乘积 $Q_jR_j$ 的演化方程：'''),
(42,43,'The second-derivative terms satisfy','其中的二阶导数项满足'),
(43,44,r'''We can therefore expand the time derivative in (33) and use (29) to eliminate $Q_{j,t}$. Dividing by $Q_j$ then gives the evolution equation for $R_j$. Meanwhile, the two expressions for $\omega_j$ in (26) and (31) impose a lattice constraint linking $M_j$ to $Q_jR_j$.

Collecting these relations, we obtain the potential formulation (PF):''',r'''因此，我们可以展开公式 (33) 中的时间导数，并利用公式 (29) 消去 $Q_{j,t}$，再除以 $Q_j$，得到 $R_j$ 的演化方程。另一方面，公式 (26) 与 (31) 给出的两种 $\omega_j$ 表达共同确定了一个格点约束，将 $M_j$ 与 $Q_jR_j$ 联系起来。

汇集这些关系，我们便得到势表示（PF）：'''),
(44,45,r'''Here $Q_j$ and $R_j$ occupy the half-grid locations $y=(j+\tfrac12)h$, while $M_j$ lies at $y=jh$. The first two equations describe the evolution of $Q_j$ and $R_j$; the third relates their product to the difference of neighbouring potential values. We recover the physical fields through''',r'''其中，$Q_j,R_j$ 位于半格点 $y=(j+\tfrac12)h$，而 $M_j$ 位于整数格点 $y=jh$。前两条方程描述 $Q_j,R_j$ 的演化，第三条则将二者的乘积与相邻势值之差联系起来。物理场通过下式恢复：''')]
for l,r,en,zh in pairs:
 gap('en',l,r,en); gap('zh',l,r,zh)

replace('The following proposition shows that the two nonlinear formulations recover identical physical fields from the same pair of positive τ functions.', 'We have obtained two nonlinear formulations by treating the auxiliary potential in different ways. To make their relation precise, we compare the physical fields reconstructed from the same τ functions. The following proposition shows that the agreement holds at each fixed lattice spacing, before taking any continuum limit.')
replace('下面的命题说明，两种非线性表示由同一对正 τ 函数恢复完全相同的物理场。','通过对辅助势采取不同的处理方式，我们得到了两种非线性表示。为明确二者之间的关系，我们比较它们从同一组 τ 函数重构出的物理场。下面的命题说明，这种一致性在每个固定格距下就已经成立，无需先取连续极限。')
for lang,txt in [('en',r'''This agreement allows us to use the same reconstructed exact fields as references for both formulations. It does not imply that their numerical approximations will coincide: further discretization in $x$ and $t$ acts on different dependent variables and different forms of the evolution equations. We examine these effects in Section 3. Before doing so, we establish how the semi-discrete equations and their exact wave fields approach the continuous DLW system as $h\to0$.'''),('zh',r'''这一一致性使我们能够采用同一组重构精确场，作为两种表示的共同参照。不过，它并不意味着二者的数值近似也会相同：后续的 $x$ 方向与时间离散作用于不同的因变量及不同形式的演化方程。我们将在第 3 节考察这些影响。在此之前，我们先建立半离散方程及其精确波场在 $h\to0$ 时与连续 DLW 系统之间的联系。''')]:
 marker=f'### 2.5 '+('Continuum limits' if lang=='en' else '连续极限')
 s=s.replace(marker,txt+'\n\n'+marker,1)

# The next file contains the fully reorganized, approved continuum-limit subsection.
for lang in ('en','zh'):
 new=(P/f'section25_sync_{lang}.md').read_text(encoding='utf-8')
 pattern=rf'### 2\.5 [^\n]*\{{#{lang}-limits\}}[\s\S]*?(?=### 2\.6 )'
 s,n=re.subn(pattern,lambda m:new.strip()+'\n\n',s,count=1)
 assert n==1

# Darboux–Lax exposition. Keep the original short proof, pending author review.
replace('We next construct a Darboux–Lax representation of the semi-discrete DLW system. We first express the linear problem in terms of the physical fields and then give its potential form in the variables Q,R,M.',r'''The preceding analysis establishes the connection between the semi-discrete system and the continuous DLW equations. We now return to the structure of the lattice system at finite spacing and seek an auxiliary linear problem whose compatibility reproduces the nonlinear evolution. This will allow us to relate the field equations to the consistency of two operations: transferring a wave function between neighbouring lattice sites and evolving it in time.

To develop this representation, we first write the PE equations in shifted field variables and introduce an auxiliary potential. We then construct the lattice and time equations for the wave function and establish their compatibility with the nonlinear system. For the τ-function solutions, we show how the required potential and Darboux relations follow from the bilinear equations. Finally, we express the same linear problem in the variables $Q_j,R_j,M_j$, making its connection with the PF formulation explicit.''')
replace('下面构造半离散 DLW 系统的 Darboux–Lax 表示。首先以物理场写出线性问题，再给出它在势变量 Q、R、M 下的形式。',r'''前面的分析建立了半离散系统与连续 DLW 方程之间的联系。现在，我们回到有限格距下的格点系统本身，寻求一个辅助线性问题，使其相容条件能够恢复非线性演化。通过这一表示，我们可以将物理场方程与两种操作之间的一致性联系起来：波函数在相邻格点之间的传递，以及它随时间的演化。

为建立这一表示，我们首先用平移后的场变量改写 PE 方程，并引入辅助势。随后，我们构造波函数的格点关系与时间演化方程，建立它们与非线性系统之间的相容关系。对于 τ 函数解，我们进一步说明所需的辅助势及 Darboux 关系如何由双线性方程得到。最后，我们用 $Q_j,R_j,M_j$ 表达同一个线性问题，明确它与 PF 表示之间的联系。''')
replace('Introduce the shifted variables','We begin by absorbing the constant terms in the PE equations into shifted variables:')
replace('引入平移后的变量','我们首先通过以下变量平移，将 PE 方程中的常数项吸收到新变量中：')
for l,r,en,zh in [(69,70,r'''With this choice, the flux in the second equation becomes proportional to $U_jw_j$, while the first equation takes a quadratic form in $U_j$ and $w_j$. Substituting (61) into (25), we obtain''',r'''这样，第二条方程的通量变为与 $U_jw_j$ 成正比的形式，而第一条方程则以 $U_j,w_j$ 的二次项表示。将公式 (61) 代入 (25)，便得到'''),(70,71,r'''To construct the auxiliary linear problem, we introduce a potential $V_j$ through its $x$-derivative and its change between neighbouring lattice sites:''',r'''为构造辅助线性问题，我们通过辅助势 $V_j$ 的 $x$ 导数及其在相邻格点之间的变化来定义它：'''),(71,72,r'''These two relations must assign the same value to $V_{j+1,x}-V_{j,x}$. We check this by taking the difference of the first relation at adjacent sites and comparing it with the $x$-derivative of the second. Their agreement is exactly the first equation in (62), evaluated at the corresponding lattice index.

We can therefore construct $V_j$ locally whenever the nonlinear equations hold. We first integrate the prescribed $x$-derivative at one reference site, then use the lattice relation to determine $V_j$ at neighbouring sites. The compatibility just established ensures that these propagated values satisfy the prescribed $x$-derivative at every site. The remaining freedom is a function of $t$ common to all lattice sites.

With the auxiliary potential in place, we introduce a wave function $\psi_j(x,t)$ and consider the linear system''',r'''这两条关系必须给出相同的 $V_{j+1,x}-V_{j,x}$。为检验这一点，我们对第一条关系取相邻格点之差，再与第二条关系的 $x$ 导数进行比较。二者一致的条件，恰好是相应格点指标处的方程组 (62) 的第一式。

因此，当非线性方程成立时，我们可以局部构造 $V_j$。首先，在一个参考格点处对给定的 $x$ 导数积分；随后，利用格点关系确定相邻位置的 $V_j$。刚才建立的相容性保证了这些递推得到的值在每个格点处都满足规定的 $x$ 导数关系。剩余的自由度是一个所有格点共有的时间函数。

在确定辅助势之后，我们引入波函数 $\psi_j(x,t)$，并考虑线性系统''')]:
 gap('en',l,r,en);gap('zh',l,r,zh)
replace('The first equation relates wave functions at adjacent lattice sites, while the second determines their time evolution. The following theorem establishes their compatibility with the nonlinear system.',r'''The first equation relates the wave functions at neighbouring lattice sites through two first-order differential operators in $x$. The second prescribes their time evolution at each site. We require these relations to remain consistent as time evolves: transferring the wave function to the next site and then evolving it must agree with evolving it first and then applying the lattice relation.

To express this requirement, we write

$$\mathscr A_j=\partial_x-\frac{U_j}{2}-\frac{hw_j}{8},\qquad \mathscr B_j=\partial_x-\frac{U_j}{2}+\frac{hw_j}{8},$$

and introduce the formal transfer and time-evolution operators

$$T_j=\mathscr B_j^{-1}\mathscr A_j,\qquad H_j=-\partial_x^2-V_j.$$

The linear system then reads $\psi_{j+1}=T_j\psi_j$ and $\psi_{j,t}=H_j\psi_j$. Its compatibility is expressed by

$$T_{j,t}=H_{j+1}T_j-T_jH_j.$$

Here $\mathscr B_j^{-1}$ is understood as a formal pseudodifferential inverse. The following theorem relates this operator identity to the nonlinear field equations.''')
replace('第一条方程联系相邻格点上的波函数，第二条给出它们的时间演化。下面的定理建立该线性系统与非线性方程之间的相容关系。',r'''第一条方程通过两个关于 $x$ 的一阶微分算子联系相邻格点上的波函数，第二条则规定各格点处波函数的时间演化。我们要求这两种关系在时间演化过程中保持一致：先将波函数传递到下一个格点，再进行时间演化，应与先演化、再应用格点关系得到相同的结果。

为表达这一要求，我们定义

$$\mathscr A_j=\partial_x-\frac{U_j}{2}-\frac{hw_j}{8},\qquad \mathscr B_j=\partial_x-\frac{U_j}{2}+\frac{hw_j}{8},$$

并引入形式格点传递算子与时间演化算子

$$T_j=\mathscr B_j^{-1}\mathscr A_j,\qquad H_j=-\partial_x^2-V_j.$$

线性系统于是写为 $\psi_{j+1}=T_j\psi_j$ 与 $\psi_{j,t}=H_j\psi_j$，其相容性由算子恒等式

$$T_{j,t}=H_{j+1}T_j-T_jH_j$$

表达。这里，$\mathscr B_j^{-1}$ 按形式伪微分逆算子理解。下面的定理建立这一算子恒等式与非线性场方程之间的联系。''')
replace('For τ-function solutions, take',r'''For the solutions constructed from τ functions, we can express the auxiliary potential and the Darboux coefficients directly in terms of $F_j,G_j$. Using the reconstruction formulas, we obtain''')
replace('对于 τ 函数解，可取',r'''对于由 τ 函数构造的解，我们可以直接用 $F_j,G_j$ 表达辅助势与 Darboux 系数。利用重构公式，便得到''')
gap('en',83,84,r'''The expressions for $r_j$ and $s_j$ agree with $U_j/2+hw_j/8$ and $U_j/2-hw_j/8$, respectively. The potential also satisfies the required lattice relation, since

$$V_{j+1}-V_j=2\partial_x^2\log\frac{G_{j+1}}{G_j}=2\omega_{j,x}=\frac h2w_{j,x}.$$

We then return to the normalized bilinear equations in (19). Differentiating them in $x$ and substituting (65), we find that the first gives $\mathcal E_j^r=0$, while the second gives $\mathcal E_j^s=0$. Their sum also recovers the prescribed expression for $V_{j,x}$ in (63). Thus, the same bilinear equations used to construct the exact fields supply the relations needed for their Darboux–Lax representation. In particular, the Gram determinant solutions of Section 2.3 satisfy these compatibility relations wherever the τ functions are positive.

We finally express the linear system in the potential variables used in PF. From the reconstruction relations, we have''')
gap('zh',83,84,r'''其中，$r_j,s_j$ 的表达式分别与 $U_j/2+hw_j/8$、$U_j/2-hw_j/8$ 一致。辅助势也满足所需的格点关系，因为

$$V_{j+1}-V_j=2\partial_x^2\log\frac{G_{j+1}}{G_j}=2\omega_{j,x}=\frac h2w_{j,x}.$$

随后，我们回到公式 (19) 中归一化后的双线性方程。对它们关于 $x$ 求导，并代入公式 (65)，第一式给出 $\mathcal E_j^r=0$，第二式给出 $\mathcal E_j^s=0$。二者之和还恢复了公式 (63) 中规定的 $V_{j,x}$ 表达式。因此，用于构造精确物理场的双线性方程，同时提供了建立 Darboux–Lax 表示所需的关系。特别地，第 2.3 节的 Gram 行列式解在 τ 函数为正的区域内满足这些相容关系。

最后，我们用 PF 中的势变量表达这一线性系统。根据重构关系，有''')
gap('en',84,85,'Substituting these expressions into (64), we obtain')
gap('zh',84,85,'将这些表达式代入 (64)，便得到')
gap('en',85,86,r'''Equation (67) gives the Darboux–Lax system in the PF variables. The potential relation used above is also contained in the PF lattice constraint, whose $x$-derivative gives''')
gap('zh',85,86,r'''公式 (67) 给出了 PF 变量下的 Darboux–Lax 系统。前面使用的辅助势关系也包含在 PF 的格点约束中，对该约束关于 $x$ 求导，即得''')
end_en=r'''Through the Darboux–Lax representation, we interpret the nonlinear field equations as the conditions that make lattice transfer consistent with time evolution. We describe these two operations through linear equations for an auxiliary wave function and, under the conditions of the compatibility theorem, recover the nonlinear system by requiring them to agree. This gives us a way to examine the integrable structure of the equations at finite lattice spacing. By expressing the same linear problem in PE and PF variables, we also show how the two formulations retain this structure despite their different treatment of the potential.

We have therefore connected the construction of the lattice equations with both their exact solutions and their Darboux–Lax representation. Starting from the continuous bilinear relations, we obtained a semi-discrete system whose wave fields can be reconstructed explicitly and compared quantitatively with the continuous DLW solutions. These exact fields also allow us to assess what happens when we use the nonlinear equations for computation. Although PE and PF reconstruct the same fields analytically, their numerical implementations evolve different variables and introduce further approximations in $x$ and $t$. With the exact solutions and the $y$-discretization error now available as references, we can investigate how these choices affect the accuracy of the computed physical fields.'''
end_zh=r'''通过 Darboux–Lax 表示，我们将非线性场方程理解为格点传递与时间演化保持一致所需的条件。我们用辅助波函数的线性方程描述这两种操作，并在相容性定理的条件下，通过要求二者一致来恢复非线性系统。这使我们能够在有限格距下考察方程的可积结构。通过分别用 PE 与 PF 变量表达同一个线性问题，我们也说明了两种表示虽然对势变量采取不同的处理方式，却保留了这一共同结构。

由此，我们将格点方程的构造与其精确解及 Darboux–Lax 表示联系起来。从连续双线性关系出发，我们得到了一个物理场可以显式重构、并能与连续 DLW 解进行定量比较的半离散系统。这些精确物理场也使我们能够评估将非线性方程用于实际计算时的情况。尽管 PE 与 PF 在解析层面重构出相同的物理场，它们的数值实现却推进不同的变量，并在 $x$ 与 $t$ 方向引入进一步的近似。有了精确解及 $y$ 方向离散误差作为参照，我们便可以考察这些选择如何影响计算所得物理场的精度。'''
for lang,txt in [('en',end_en),('zh',end_zh)]:
 pat=rf'(<a id="{lang}-eq-86"></a>\s*\$\$[\s\S]*?\$\$)[\s\S]*?(?=## 3\.)'
 s,n=re.subn(pat,lambda m:m[1]+'\n\n'+txt+'\n\n',s,count=1);assert n==1

# Renumber numbered equations in reading order, preserving stable HTML anchors.
# Removed continuum-limit equations redirect to their stronger replacement.
redirect={48:61,49:201,50:201,65:201,66:60,67:3,68:201}
old_eq={}
for m in re.finditer(r'<a id="en-eq-(\d+)"></a>\s*\$\$([\s\S]*?)\$\$',original):
 tag=re.search(r'\\tag\{(\d+)\}',m[2])
 if tag:old_eq[int(tag[1])]=int(m[1])
parts=re.split(r'(?m)(?=^# .*\{#zh-title\})',s)
assert len(parts)==2
maps=[]
for k,part in enumerate(parts):
 lang=('en','zh')[k]; counter=[0]; anchor_num={}
 def number(m):
  counter[0]+=1;anchor_num[int(m[1])]=counter[0]
  return f'<a id="{lang}-eq-{m[1]}"></a>\n\n$$'+re.sub(r'\\tag\{\d+\}',lambda _:r'\tag{'+str(counter[0])+'}',m[2])+'$$'
 part=re.sub(rf'<a id="{lang}-eq-(\d+)"></a>\s*\$\$([\s\S]*?\\tag\{{\d+\}}[\s\S]*?)\$\$',number,part)
 for old,target in redirect.items():
  part=part.replace(f'#{lang}-eq-{old})',f'#{lang}-eq-{target})')
 tagmap={n:anchor_num.get(a,anchor_num.get(redirect.get(a))) for n,a in old_eq.items()}
 # All parenthesized integer references denote equations in this manuscript.
 part=re.sub(r'\((\d+)\)',lambda m:'('+str(tagmap.get(int(m[1])) or m[1])+')',part)
 # Correct linked labels from their actual target anchors.
 part=re.sub(rf'\[\(\d+\)\]\(#{lang}-eq-(\d+)\)',lambda m:f'[({anchor_num[int(m[1])]})](#{lang}-eq-{m[1]})',part)
 parts[k]=part;maps.append(anchor_num)
s=''.join(parts)
assert maps[0]==maps[1]
# Result numbering after merging three old continuum results into one theorem.
for a,b in [('2.11','2.9'),('2.8','2.8')]:
 if a!=b:s=s.replace(a,b)
# Existing appendix refers to old results by number; resolve those references.
s=s.replace('Proposition 2.7 uniformly','the staggered reconstruction expansion uniformly')
s=s.replace('Theorem 2.9 supplies','Theorem 2.7 supplies').replace('定理 2.9 提供','定理 2.7 提供')
src.write_text(s,encoding='utf-8')
(backup/'sync_metadata.json').write_text(json.dumps({'backup':str(backup),'equation_map':maps[0],'proof_status':'Darboux–Lax proof kept original; revised expanded proof pending review'},ensure_ascii=False,indent=2),encoding='utf-8')
print(backup)
