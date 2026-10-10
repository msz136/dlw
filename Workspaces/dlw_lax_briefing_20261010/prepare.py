from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
old = ROOT / 'Workspaces/dlw_lax_derivation_20261009'
source = (old / 'compact_manuscript.md').read_text(encoding='utf-8')
source = source.replace('# 半离散 DLW 的 Lax 对', '# 半离散 DLW 的 Lax 对：构造与相容性', 1)
source = source.replace('## 1. 原方程', r'''半离散化保留连续变量 $x,t$，将 $y$ 方向替换为格点。当前已建立的表示从物理场重构辅助热势，以两个一阶 Darboux 因子的商定义格点传递算子，再由交织关系证明格点传递与时间演化相容。在逐点非退化条件下，配合辅助势的格点差关系，相容条件反向恢复原方程。PE 与 PF 共享这一线性问题，交错双线性方程给出它的 τ 函数实现。

## 1. 半离散方程与变量''', 1)
source = source.replace('## 2. 辅助势与所需条件', r'''原物理变量与本节变量的关系为 $U_j=u_j+2a$、$w_j=W_j-4$，其中 $W_j=4\omega_j/h=v_j-\delta_0u_j$，$\delta_0u_j=(u_{j+1}-u_{j-1})/(2h)$。物理场 $u_j,v_j$ 位于 $y=(j+1/2)h$。辅助势 $V_j$ 与第二物理场 $v_j$ 是不同的变量。

## 2. 辅助热势的局部重构''', 1)
source = source.replace('Q_j', r'\mathscr Q_j')
source += r'''

## 5. τ 函数与 PF 的共同线性结构

### 5.1 交错双线性方程产生 Darboux 因子

记 $B_s=D_x^2+D_t+2sD_x$，其中 $D_x,D_t$ 是 Hirota 双线性算子。半离散构造的双线性起点为

$$B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.\tag{13}$$

在 $F_j,G_j>0$ 的区域，取 $u_j=\partial_x\log[F_j^2/(G_jG_{j+1})]$、$\omega_j=\partial_x\log(G_{j+1}/G_j)$，得到

$$\begin{aligned}
V_j&=2(\log G_j)_{xx},\\
\alpha_j&=\partial_x\log(F_j/G_j)+a-h/2,\\
\eta_j&=\partial_x\log(F_j/G_{j+1})+a+h/2.
\end{aligned}\tag{14}$$

第一行满足 $V_{j+1}-V_j=2\omega_{j,x}=(h/2)w_{j,x}$。将两条双线性方程分别除以 $F_jG_j$、$F_jG_{j+1}$ 后对 $x$ 求导，恰好得到 $\mathcal E_j^\alpha=0$、$\mathcal E_j^\eta=0$。两条交错双线性关系分别产生两个 Darboux 因子，再通过共同中间热势组合成格点传递关系。这将已有的 Gram τ 函数解与 Lax 表示连接起来。

### 5.2 PF 是同一线性对的势变量表示

在势函数形式 PF 中，定义 $Q_j=F_j/\sqrt{G_jG_{j+1}}$、$M_j=(\log G_j)_x$。此处 $Q_j$ 是势变量，与时间算子 $\mathscr Q_j$ 区分。物理场及格点约束满足

$$\begin{aligned}
U_j&=2Q_{j,x}/Q_j+2a,\qquad w_j=-4Q_jR_j,\\
V_j&=2M_{j,x},\qquad M_{j+1}-M_j=h(1-Q_jR_j).
\end{aligned}\tag{15}$$

代入式（5），得到 PF 的 Lax 对

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{16}$$

PF 的格点约束求 $x$ 导数给出辅助势差，PF 演化使两项 Riccati 残差为零。因此 PE 与 PF 具有共同的 Darboux–Lax 结构。在 $Q_j\ne0$ 的定义域中，反向非退化条件为 $Q_jR_j\ne0$。

物理场在 $Q_j\mapsto c_j(t)Q_j$、$R_j\mapsto c_j(t)^{-1}R_j$ 下保持不变。由物理场反向恢复 PF 演化时，还须选定势变量的时间归一化；相容性反向论证首先恢复物理场方程。

## 6. 已证明的结论

**命题。** 对任一光滑的半离散 DLW 解，在局部空间区间和格点链上，可重构满足式（3）的辅助热势，使式（5）在形式算子意义下相容。反之，若辅助势满足式（3）的格点差关系，且每个所讨论的格点与时空点均有 $w_j\ne0$，则式（8）恢复半离散 DLW 的两条物理场方程。交错 τ 函数构造和 PF 表示均实现这一线性对。

非退化条件用于从传递商恢复两个因子的残差。当 $w_j=0$ 时，$A_j=B_j$、$T_j=I$，传递相容式可能丢失物理方程的信息。例如取 $w_j=V_j=0$、$U_j=jx$，传递相容式成立，但第一物理方程的残差为 $(2j-1)x/h$。完整 Darboux 交织关系仍保留两项残差，允许退化场。

这里证明的是连续 $x,t$、离散 $y$ 的形式 Darboux–Lax 相容性。$B_j^{-1}$ 是形式伪微分逆，具体边值问题中的算子可逆性需另行处理。空间差分和 Euler、RK4、C–N 时间推进所得数值算法的谱保持性质也需单独证明。

<footer><p>依据：<a href="dlw_lax_derivation.html">半离散 DLW 的 Lax 对完整推导</a>；<a href="dlw_paper_draft.html">DLW 理论与数值论文初稿</a>；<a href="dlw_draft_audit_20261010.html">2026年10月10日推导审查</a>。</p></footer>
'''
(HERE / 'manuscript.md').write_text(source, encoding='utf-8')
build = (old / 'build.py').read_text(encoding='utf-8')
build = build.replace("'compact_manuscript.md'", "'manuscript.md'")
build = build.replace('report/dlw_lax_derivation.html', 'report/dlw_lax_briefing.html')
build = build.replace('range(1,13)', 'range(1,17)')
build = build.replace('<title>半离散 DLW 的 Lax 对</title>', '<title>半离散 DLW 的 Lax 对：专题汇报</title>')
(HERE / 'build.py').write_text(build, encoding='utf-8')
(HERE / 'render.cjs').write_text((old / 'render.cjs').read_text(encoding='utf-8'), encoding='utf-8')
layout = (old / 'check_layout.cjs').read_text(encoding='utf-8').replace('report/dlw_lax_derivation.html', 'report/dlw_lax_briefing.html')
(HERE / 'check_layout.cjs').write_text(layout, encoding='utf-8')
(HERE / 'verify.py').write_text((old / 'local_verify.py').read_text(encoding='utf-8'), encoding='utf-8')
print('Prepared briefing source and build scripts.')
