# 周期半离散 DLW 的 Lax 表示

从物理方程重构热势，通过一阶 Darboux 交织得到格点传递方程，再沿周期格点构造归一化谱算子。逐格点相容关系在非退化支上与原方程等价。

## 1. 物理方程与闭合条件

设 $U_j(x,t),w_j(x,t)$ 为光滑实值场，$j\in\mathbb Z/M\mathbb Z$，$x\in\mathbb T_{L_x}$。固定

$$M\ge2,\qquad h>0,\qquad L_x>0,\qquad c\ne0,\qquad\gamma\in\mathbb R.\tag{1}$$

定义格点移位、后差分、相邻平均及格点均值：

$$Ef_j=f_{j+1},\quad\delta_-f_j=\frac{f_j-f_{j-1}}h,\quad
M_-f_j=\frac{f_j+f_{j-1}}2,\quad
\Pi f=\frac1M\sum_{j=0}^{M-1}f_j,\quad P_0=I-\Pi.\tag{2}$$

物理方程为

$$\begin{aligned}
\delta_-\!\left[U_t+\partial_x\!\left(\frac{U^2}2+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)&=0,\\
w_t+\partial_x(Uw)-\partial_x^2w&=0.
\end{aligned}\tag{3}$$

本文取固定平均的周期场：

$$\Pi w=c,\qquad\Pi(Uw)=\gamma.\tag{4}$$

两式在每个 $(x,t)$ 成立。旧变量的对应关系为 $U=u+2a$、$w=W-4$，其中 $a$ 是旧归一化中的常背景参数；因此 $W_j\ne4$ 对应 $w_j\ne0$。

## 2. 从物理方程重构周期热势

在格点零均值子空间上，$\delta_-$ 可逆。定义

$$R=\left(\delta_-\big|_{\ker\Pi}\right)^{-1}M_-P_0,\qquad
\delta_-R=M_-P_0,\qquad R^*=-R.\tag{5}$$

记 $\beta=h^2/32$。由式（3）的第一式及 $\partial_x\Pi w=0$，得到

$$U_t=-\partial_x\!\left(\frac{U^2}2+\beta w^2+\partial_xU+R\partial_xw\right)+\lambda(x,t),\tag{6}$$

其中 $\lambda$ 在各格点相同。为确定它，定义

$$e_j=\frac12U_j^2w_j+\frac\beta3w_j^3+w_j\partial_xU_j
+\frac12w_j(R\partial_xw)_j,\qquad\bar e=\Pi e.\tag{7}$$

利用 $R^*=-R$、式（3）的第二式及 $\Pi(Uw)=\gamma$，对乘积平均求时间导数：

$$0=\partial_t\Pi(Uw)=c\lambda-2\partial_x\bar e,
\qquad\lambda=\frac2c\partial_x\bar e.\tag{8}$$

这给出闭合场上的显式时间演化。取热势

$$\boxed{V_j=\frac12(R\partial_xw)_j-\frac h4\partial_xw_j-\frac{\bar e}{c}+v_0(t).}\tag{9}$$

其中 $v_0(t)$ 是共同的时间规范。由式（5）直接得到

$$V_{j+1}-V_j=\frac h2\partial_xw_j,\qquad V_{j+M}=V_j.\tag{10}$$

由于 $U,w$ 在 $x$ 方向周期，$V$ 也在 $x$ 方向周期。式（9）为每个满足式（3）、（4）的光滑场给出了同一套格点热势。

## 3. 一阶因子的 Darboux 交织

在每个格点定义

$$\alpha_j=\frac{U_j}2+\frac{hw_j}8,\qquad
\eta_j=\frac{U_j}2-\frac{hw_j}8,\qquad
A_j=\partial_x-\alpha_j,\qquad B_j=\partial_x-\eta_j.\tag{11}$$

两个因子共用一个中间热势：

$$V_j^F=V_j+2\partial_x\alpha_j
=V_{j+1}+2\partial_x\eta_j.\tag{12}$$

第二个等号正是势差式（10）。定义 Riccati 残差

$$\begin{aligned}
\mathcal E_j^\alpha&=\partial_t\alpha_j+\partial_x^2\alpha_j
+2\alpha_j\partial_x\alpha_j+\partial_xV_j,\\
\mathcal E_j^\eta&=\partial_t\eta_j+\partial_x^2\eta_j
+2\eta_j\partial_x\eta_j+\partial_xV_{j+1}.
\end{aligned}\tag{13}$$

将式（11）代入，并用势差式（10），可逐项整理为

$$\mathcal E_j^\alpha-\mathcal E_j^\eta
=\frac h4\left[\partial_tw_j-\partial_x^2w_j+\partial_x(U_jw_j)\right],\tag{14}$$

$$\mathcal E_j^\alpha+\mathcal E_j^\eta
=\partial_tU_j+\partial_x\!\left(\frac{U_j^2}2+\frac{h^2w_j^2}{32}\right)
+\partial_x^2U_j+\frac h2\partial_x^2w_j+2\partial_xV_j.\tag{15}$$

式（14）由物理方程的第二式为零。将式（6）、（8）、（9）代入式（15），各项抵消，得到 $\mathcal E_j^\alpha=\mathcal E_j^\eta=0$。

连接非线性方程与线性算子的恒等式是

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2\partial_xr)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-\left(\partial_tr+\partial_x^2r+2r\partial_xr+\partial_xV\right).
\end{aligned}\tag{16}$$

它作用于任意辅助函数。分别取 $r=\alpha_j,\eta_j$，得到两个完整交织关系：

$$\begin{aligned}
(\partial_t+\partial_x^2+V_j^F)A_j
&=A_j(\partial_t+\partial_x^2+V_j),\\
(\partial_t+\partial_x^2+V_j^F)B_j
&=B_j(\partial_t+\partial_x^2+V_{j+1}).
\end{aligned}\tag{17}$$

## 4. 逐格点 Lax 对与原方程的等价性

在形式伪微分算子代数中，一阶首一算子 $B_j$ 具有形式逆。定义

$$\boxed{T_j=B_j^{-1}A_j
=\left(\partial_x-\frac{U_j}2+\frac{hw_j}8\right)^{-1}
\left(\partial_x-\frac{U_j}2-\frac{hw_j}8\right),\qquad
Q_j=-\partial_x^2-V_j.}\tag{18}$$

这里形式求逆按 $\partial_x$ 的负次幂展开，系数由逐阶递推确定。令 $Q_j^F=-\partial_x^2-V_j^F$，式（17）等价于

$$\partial_tA_j=Q_j^FA_j-A_jQ_j,\qquad
\partial_tB_j=Q_j^FB_j-B_jQ_{j+1}.\tag{19}$$

对 $T_j=B_j^{-1}A_j$ 求导，使用 $\partial_tB_j^{-1}=-B_j^{-1}(\partial_tB_j)B_j^{-1}$，中间热算子消去：

$$\boxed{\partial_tT_j=Q_{j+1}T_j-T_jQ_j.}\tag{20}$$

因此辅助线性方程为

$$\boxed{(\partial_x-\eta_j)\psi_{j+1}=(\partial_x-\alpha_j)\psi_j,
\qquad\partial_t\psi_j=-\partial_x^2\psi_j-V_j\psi_j.}\tag{21}$$

式（20）保证先作格点传递、再作时间演化，与相反顺序得到相同结果。

### 非退化支上的反向推导

保持式（10）的势差关系，对一般场计算传递残差。由式（16）可得精确恒等式

$$B_j\left(\partial_tT_j-Q_{j+1}T_j+T_jQ_j\right)
=-\mathcal E_j^\alpha+\mathcal E_j^\eta T_j.\tag{22}$$

记 $g_j=hw_j/4$，则 $T_j=I-B_j^{-1}g_j$。若式（20）成立，式（22）变为

$$\mathcal E_j^\eta-\mathcal E_j^\alpha
=\mathcal E_j^\eta B_j^{-1}g_j.\tag{23}$$

左侧是乘法算子，右侧至多为 $-1$ 阶。比较 $\partial_x^0$ 的系数，得到 $\mathcal E_j^\alpha=\mathcal E_j^\eta$；比较 $\partial_x^{-1}$ 的系数，得到 $\mathcal E_j^\eta g_j=0$。在

$$\boxed{w_j(x,t)\ne0\quad\text{对所有 }j,x,t\text{ 成立}}
\qquad\Longleftrightarrow\qquad W_j(x,t)\ne4\tag{24}$$

的状态域内，两项 Riccati 残差均为零。式（14）恢复原方程的第二式；对式（15）取 $\delta_-$，再用式（10），恢复原方程的第一式。

由此，在固定闭合周期场、式（9）的热势和条件（24）下，逐格点相容方程（20）与物理方程（3）等价。两个完整交织关系（17）与物理方程的对应适用于含 $w_j=0$ 的场。条件（24）用于从传递商恢复两个因子的残差。

## 5. 周期单值算子与归一化 Lax 对

沿格点环按顺序相乘：

$$\mathcal M=T_{M-1}\cdots T_0.\tag{25}$$

对乘积求时间导数，式（20）中的内部项相邻抵消。由 $Q_M=Q_0$，得到

$$\partial_t\mathcal M=Q_0\mathcal M-\mathcal M Q_0.\tag{26}$$

闭合条件给出两个常数

$$G=\sum_j\frac{hw_j}4=\frac{hMc}4\ne0,\qquad
B=\frac\gamma{2c}.\tag{27}$$

传递算子的前两阶展开为

$$\mathcal M=I-G\partial_x^{-1}
+\left(\frac{G^2}2-GB\right)\partial_x^{-2}
+O(\partial_x^{-3}).\tag{28}$$

式（28）由 $T_j=I-g_j\partial_x^{-1}+(\partial_xg_j-\eta_jg_j)\partial_x^{-2}+\cdots$ 有序相乘得到；使用 $\partial_xG=0$ 及 $\sum_jU_jg_j=hM\gamma/4=2GB$。这里的 $O$ 表示形式算子阶数。

由于 $G\ne0$，$\mathcal M-I$ 是可形式求逆的 $-1$ 阶算子。定义

$$\boxed{L=-G(\mathcal M-I)^{-1}+(B-G/2)I
=\partial_x+\sum_{k\ge1}\ell_k\partial_x^{-k}.}\tag{29}$$

常数 $G,B$ 不随时间变化，式（26）通过求逆与仿射变换传到 $L$：

$$\boxed{\partial_tL=[Q_0,L],\qquad Q_0=-\partial_x^2-V_0.}\tag{30}$$

比较式（30）的 $\partial_x^0$ 系数，得到 $\partial_xV_0=2\partial_x\ell_1$。因此可选时间规范，使

$$\boxed{Q_0=-(L^2)_+=-\partial_x^2-2\ell_1.}\tag{31}$$

下标 $+$ 表示保留 $\partial_x$ 的非负次幂。式（30）是由原物理时间演化导出的归一化 Lax 对；式（20）保留逐格点相容关系，用于第 4 节的反向等价。

在辅助波函数上，周期谱问题可取 Floquet 条件 $\psi_M=\mu\psi_0$。于是 $\mathcal M\psi_0=\mu\psi_0$；当 $\mu\ne1$ 时，对应的归一化谱参数为

$$L\psi_0=\zeta\psi_0,\qquad
\zeta=B-\frac G2-\frac G{\mu-1}.\tag{32}$$

## 6. 条件与守恒量

| 推导步骤 | 条件 |
|---|---|
| 原场到完整 Darboux 交织 | 光滑实值周期场；固定 $M,h,L_x,c,\gamma$；式（3）、（4）；热势取式（9） |
| 交织到逐格点传递式 | 首一因子在形式伪微分代数中求逆；允许个别 $w_j=0$ |
| 逐格点传递式恢复物理方程 | 同一热势及势差关系；逐点 $w_j\ne0$，即 $W_j\ne4$ |
| 周期归一化谱算子 | 格点热势闭合；$G=hMc/4\ne0$；形式求逆与乘法 |
| Floquet 参数变换 | $\mu\ne1$ |

最后取循环留数迹：$\operatorname{Tr}X=\int_0^{L_x}\operatorname{res}_{\partial_x}X\,dx$，其中留数是 $\partial_x^{-1}$ 的系数。式（30）给出

$$\mathcal C_n=\frac1n\operatorname{Tr}L^n,\qquad
\frac{d}{dt}\mathcal C_n
=\operatorname{Tr}\!\left(L^{n-1}[Q_0,L]\right)=0,
\qquad n\ge1.\tag{33}$$

因此前述谱守恒量沿原半离散 DLW 的物理时间演化保持不变。这里用到的是由原方程导出的 Lax 演化和周期循环迹。

<footer><p>推导依据：<a href="../Workspaces/dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md">周期热势与单值算子推导</a>；<a href="../Workspaces/dlw_integrability_audit_20261002/LAX_AUDIT.md">Darboux 算子恒等式</a>；<a href="../dlw_integrability.html">周期场可积性</a>。</p></footer>
