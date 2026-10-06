# 半离散 DLW 的刘维尔可积性研究

更新：2026-10-06。本文整理半离散 DLW 的一般周期场 Hamilton 结构、独立对合守恒层级，以及有限孤子解族的可积几何。最新一般场结论集中在 [第 13–17 节](#sec-field-theorem)：对每个固定周期格点数 $M\ge2$，构造包含实际 Hamiltonian 的守恒族 $\mathcal K,\mathcal P,\mathcal C_3,\mathcal C_5,\ldots$，证明两两对合和任意有限前缀的泛型独立性。两格点进一步得到局部可逆场变换与相容三 Hamilton 算子。

第 4–10 节保留有限孤子模空间与跨孤子数拼接的研究；这些参数空间结构与第 13–17 节直接从原场括号出发的结果分别使用。本文新增内容为附带推导和符号证书的研究证明草稿。

## 阅读目录

1. [结论、维数与计数](#sec-results)
2. [固定方程、变量与解族](#sec-system)
3. [研究过程：哪些路线成立，哪些遇到障碍](#sec-history)
4. [有限 N 孤子的参数 Hamilton 系统](#sec-moduli)
5. [统一的谱守恒量及独立性](#sec-integrals)
6. [任意 N：从物理场反推孤子参数](#sec-inverse)
7. [格点移动和孤子散射的相容性](#sec-scattering)
8. [跨 N 拼接：零强度边界](#sec-gluing)
9. [不预先指定 N 的共同泊松代数](#sec-atomic)
10. [原场 J₀ 的继承障碍](#sec-obstructions)
11. [可以与不可以宣称的结论](#sec-claims)
12. [复核、资料与下一步](#sec-verification)
13. [一般周期物理场的独立对合守恒族](#sec-field-theorem)
14. [任意有限周期的矩阵表示与物理泊松坐标](#sec-field-matrix)
15. [两格点的一般场与三 Hamilton 结构](#sec-field-two-site)
16. [一般场解的解析设置](#sec-field-analysis)
17. [本轮证明与核验材料](#sec-field-evidence)

<a id="sec-results"></a>
## 1. 结论、维数与计数

### 1.1 有限孤子解族的结果

在下文明确的正系数、非共振参数范围内，对任意有限孤子数 $N$：

- 标准 Gram 子集展开给出原半离散方程的精确 $N$ 孤子解；
- 去掉孤子编号置换后，可以由完整物理场恢复归一化的 $F,G$，再恢复谱参数与相位；参数映射也没有额外的无效切向方向；
- 在参数诱导的光滑模空间上，构造秩为 $2N$ 的泊松结构和精确的物理时间 Hamilton 流；
- 每个固定 $S_1,\ldots,S_N$ 的非空连通辛叶上，系统具有 $N$ 个独立、对易积分，满足刘维尔可积性；
- 用 $S_k\to0$ 的零强度退化，可以连接相邻孤子数的物理场、Hamilton 函数、谱守恒量及相容观测量的括号；
- 有一个不需要预先指定 $N$ 的有限原子测度表示及共同泊松可观测量代数。

这里没有宣称整个原方程的任意初值空间都可积，也没有证明原 $J_0$ 的继承、全局 Sobolev 嵌入、所有退化层或无穷多个孤子的收敛理论。

### 1.2 必须纠正的维数理解

| 对象 | 维数 / 泊松秩 | 需要或可以取的积分 |
|---|---|---|
| 固定 $N$，参数 $(S_i,Q_i,P_i)$ | $3N$ 维，秩 $2N$ | $S_i$ 是选定括号的 $N$ 个 Casimir |
| 固定全部 $S_i$ 的辛叶 | $2N$ 维 | 需要 $N$ 个独立、两两对易积分 |
| 完整 $3N$ 维参数空间的谱部分 | 有 $2N$ 个谱自由度 | 非退化域内 $C_1,\ldots,C_{2N}$ 独立 |
| $0,1,\ldots,M$ 孤子层的并集 | 各层分别为 $0,3,\ldots,3M$ 维 | 按所在层与辛叶计数，不把维数相加 |
| 所有有限孤子数的并集 | 无统一有限维数 | 有共同守恒量序列，但有限 $N$ 点上不可能无限独立 |

**前 $1$ 到 $N$ 孤子解族不是由线性叠加张成的 $N$ 维空间。** 非线性方程中的双孤子通常不等于两个单孤子相加。不同层通过特殊退化边界连接，不是直和，也不是一个固定维数的普通辛流形。

### 1.3 本文使用的刘维尔定义

在 $2m$ 维辛空间上，一个 Hamilton 系统若在开稠密的正则部分具有 $m$ 个微分独立、两两泊松对易的第一积分，并可取其中一个为 Hamilton 函数，称为刘维尔可积。退化泊松空间上应在辛叶内计数。

不必显式写出原 PDE 的全部解。也不能仅因“存在显式解”或“有 Lax 关系”就跳过 Hamilton、独立性和对易性。紧致不变环面的结论还需要刘维尔–Arnold 定理的紧致性等条件；本文孤子位置为实数，不宣称紧致环面。

<a id="sec-system"></a>
## 2. 固定方程、变量与解族

### 2.1 保持同一个半离散起点

取 $h>0$、$a\in\mathbb R$，$j\in\mathbb Z$，$x,t$ 连续。起点为

$$
B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0,
\qquad B_s=D_x^2+D_t+2sD_x.
$$

物理重构为

$$
u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\quad
W_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j},\quad
v_j=W_j+\frac{u_{j+1}-u_{j-1}}{2h}.
$$

记 $U=u+2a$、$w=W-4$、$\beta=h^2/32$，则同一非线性系统可写为

$$
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\beta w^2\right)\right]
+\partial_x^2(\delta_-U+M_-w)=0,
\qquad
w_t+\partial_x(Uw)-w_{xx}=0,
$$

其中 $\delta_-=(I-E^{-1})/h$、$M_-=(I+E^{-1})/2$。完整的两场闭合式、积分自由度和二阶连续极限见 [NONLINEAR_CLOSURE.md](Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md)。其连续极限对应原文固定的 $\lambda=-2$，不能额外把 $\lambda$ 当成独立自由参数。

### 2.2 $N$ 孤子不是 $N$ 个解

参数全部选定以后，$u_j(x,t),v_j(x,t)$ 是**一个**包含 $N$ 个相互作用孤子的解。让这些参数变化，得到一整族解。用于 Hamilton 描述的是某个时刻的状态空间；每个初始状态沿参数流确定整段精确解。

为避免混淆：$N$ 在本文后半部始终是孤子数，周期格点数改记为 $M$。有限周期格点而 $x$ 仍连续的场空间仍然无限维。

### 2.3 标准正实孤子子集展开

记 $d=h/2$，

$$
S_i=p_i+q_i>0,\qquad c_i=p_i-q_i,
$$
$$
\gamma_i=-\frac{p_i-a+d}{q_i+a-d},\qquad
\chi_i=\frac{(p_i-a+d)(q_i+a+d)}{(p_i-a-d)(q_i+a-d)},
$$
$$
A_{ik}=\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)},\qquad
E_i=e^{S_i x-S_i c_i t+\theta_i}\chi_i^j.
$$

$\theta_i$ 吸收原公式中正振幅和 $1/S_i$ 的归一化。例如原振幅为一时，初始 $\theta_i=-\log S_i$。令 $a_I=\prod_{i<k\in I}A_{ik}$，空乘积为一，则

$$
G_j=\sum_{I\subset\{1,\ldots,N\}}a_I\prod_{i\in I}E_i,
\qquad
F_j=\sum_Ia_I\prod_{i\in I}\gamma_i E_i.
$$

$G_{j+1}$ 由 $E_i\mapsto\chi_i E_i$ 得到。单孤子为 $G=1+E_1$，双孤子为 $G=1+E_1+E_2+A_{12}E_1E_2$。

任意 $N$ 的精确双线性证明已经由 Cauchy 主子式展开、Gram 秩一更新及行列式恒等式给出，见 [既有 Gram 核验](Workspaces/dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md)。本研究没有把另一种混合连续 $y$ 相位构造的失败归到这个纯 $x,t,j$ 构造上。

### 2.4 当前定理域

后文物理模空间重构采用以下充分条件：

1. 所有出现的分母和所有 $p_i+q_k$ 非零；
2. $S_i>0$、$\gamma_i>0$、$0<\chi_i<1$、$A_{ik}>0$；
3. 不同子集 $I,J$ 的指数数据不同：
   $$\left(\sum_{i\in I}S_i,\prod_{i\in I}\chi_i\right)
   \ne\left(\sum_{i\in J}S_i,\prod_{i\in J}\chi_i\right).$$
4. 通过 $p_1<\cdots<p_N$ 固定编号置换。时间分离散射另要求相应速度不同。

条件 2 保证全部 tau 项为正，且 $F,G>0$。条件 3 是有限指数项不重合的非共振条件；在严格正则域内去掉的是有限组真正的解析共振条件。每个有限 $N$ 都有非空的适用区域。

论文已使用的四个实例在 $a=2,h=1/8$ 时如下，均落入当前条件域：

| 算例 | $(p_i,q_i)$ | $S_i$ | $c_i$ |
|---|---|---|---|
| Fig.1(a) | $(1,2)$ | $3$ | $-1$ |
| Fig.1(b) | $(4,-3)$ | $1$ | $7$ |
| Fig.3 | $(6,-5),(4,-3)$ | $1,1$ | $11,7$ |
| Fig.4 | $(1,2),(4,-3)$ | $3,1$ | $-1,7$ |

<a id="sec-history"></a>
## 3. 研究过程：哪些路线成立，哪些遇到障碍

### 3.1 第一阶段：原场的 Hamilton 表示

原 Hamilton 报告处理周期 $j$、周期 $x$ 的平均约束。令 $\Pi$ 为格点平均、$P_0=I-\Pi$。原隐式方程要求

$$\Pi w=c_0\ne0,\qquad \Pi(Uw)=\gamma_0,$$

固定平均通量 $\gamma_0$ 后取自治闭合。设 $U=b+p_0$、$w=c_0+s_0$，$\Pi p_0=\Pi s_0=0$，则

$$b=\frac{\gamma_0-\Pi(p_0s_0)}{c_0}.$$

逆格点差分 $R=(\delta_-|_{P_0})^{-1}M_-P_0$ 具有 $R^*=-R$。候选泛函为

$$
\mathcal H_0=h\sum_j\int\left(\frac12U^2w+\frac\beta3w^3+wU_x+\frac12wRw_x\right)dx.
$$

扣除 $\gamma_0h\sum\int U$ 再限制于约束，得到约化泛函 $\mathcal K$ 和常算子

$$J_{\rm red}=-\begin{pmatrix}0&P_0\partial_x\\P_0\partial_x&0\end{pmatrix}.$$

反对称、Jacobi 和原方程等价性可直接验证；物理变量上的算子由约束坐标图推前。**这是真正从原方程约束出发的场 Hamilton 构造，与后面人为指定的孤子模空间括号不可混同。**

原报告也排除了若干严格限定的局部候选：逆差分符号有零频极点，固定有限作用范围的 Laurent 多项式不能在足够多格点 Fourier 模式上匹配它。这只排除相应候选类，不证明不存在其他结构。

原页面及其内容在 [Hamilton 历史稿](dlw_hamilton.html) 保留。该稿登记的历史核验与本次复核分开，不将旧运行记录说成本次重跑。

### 3.2 第二阶段：Lax／交织结构和形式守恒律

完整热算子交织结构使用

$$T_j^\pm=\partial_x-w_j^\pm,\qquad
w_j^-=\frac U2+\frac h8w,\quad w_j^+=\frac U2-\frac h8w,$$
$$\mathscr H_j=\partial_t+\partial_x^2+V_j,\qquad
\mathscr H_j^F T_j^-=T_j^-\mathscr H_j,\quad
\mathscr H_j^F T_j^+=T_j^+\mathscr H_{j+1}.$$

形式上 $L_j=(T_j^+)^{-1}T_j^-$ 满足格点 Lax 演化；也可由辅助波函数的对数展开产生逐阶形式守恒密度。这些步骤必须保留势差、积分常数和边界规范。

曾特别检查 $W=4$ 的退化集合。由消去式反推时若除以 $W-4$ 会引入限制；完整交织关系不应被这个除法替代。仅仅集合零测也不能无条件恢复丢掉的方程。

在周期扇区，单值算子及其归一化伪微分谱量给出对易层级的形式构造；已有工作草稿还考察了独立性及低阶物理密度识别。**形式无限维层级不是有限维刘维尔–Arnold 紧环面定理，也不自动处理任意非周期边界。**

### 3.3 第三阶段：无限格点为什么不能直接照搬

主要障碍包括：

- 开链乘积满足两端不同的演化，不能直接套周期迹守恒；
- 背景减除、先积分还是先求格点极限，可能给出不同结果；
- 归一化传输系数的梯度可在格点方向有常数尾部，括号随窗口长度增长；
- 某些局部化扰动类上，形式传输量被背景固定，不能提供新增的独立作用变量；
- 形式逆算子恒等式可能遗漏真实算子的有限秩边界模态。

因此“有很多形式密度”“系数逐点收敛”“孤子显式可解”都不能分别代替收敛、独立性和泊松定义域的证明。

### 3.4 第四阶段：光滑种子函数的特殊分支

曾构造带限 $L^2$ 种子 $f,g$ 的线性系统

$$f_t=-(D+a)^2f,\qquad g_t=(D-a)^2g,$$

以 Cayley 算子 $(D+h/2)(D-h/2)^{-1}$ 生成全部格点，再构造 tau。其正则小量域内有精确的非线性物理解；种子上

$$H_n=\langle g,D^nf\rangle$$

形成独立、对易的层级。之后又把种子扩展成任意有限多对。

这是一族有无限自由度的特殊解，不是原论文指数孤子的同一函数空间。原场二形式拉回到进一步光滑、频谱避零的种子类上，已有收敛及正确时间演化的解析草稿；**核、可逆性、完整泊松逆及双 Hamilton 相容仍未完成**。因此后续主线回到原来的有限孤子族。

### 3.5 第五、六阶段：有限孤子模空间与跨 N 拼接

新的目标不再是一次解决任意物理初值，而是：

1. 精确描述标准 $N$ 孤子族的真实自由度；
2. 给出一套明确的 Hamilton 描述及完整积分；
3. 证明参数确实是物理解的坐标，而非冗余标记；
4. 找出不同孤子数之间可保持结构的退化方式。

后面给出这条主线的构造与证明，也保留其不等同于原场 $J_0$ 约化的限制。

<a id="sec-moduli"></a>
## 4. 有限 N 孤子的参数 Hamilton 系统

### 4.1 先把状态坐标写清楚

令当前相位 $\Theta_i(t)=\theta_i-S_ic_it$，定义

$$Q_i=-\frac{\Theta_i}{S_i},\qquad P_i=S_ic_i.$$

这里大写 $P,Q$ 与原谱参数小写 $p,q$ 不同，也不要与旧 Hamilton 报告中的平均投影 $P_0$ 混淆。$Q$ 是相位位置，不必等于碰撞时的瞬时波峰位置。

原 tau 时间演化精确给出

$$\dot Q_i=P_i/S_i=c_i,\qquad \dot P_i=0,\qquad\dot S_i=0.$$

改变初始 $Q,P$ 是选择不同的解；选定它们后随 $t$ 演化，是同一个解上的运动。

### 4.2 明确指定泊松结构

在 $3N$ 维有序参数域上，定义

$$\{Q_i,P_k\}=\delta_{ik},\qquad\{S_i,\cdot\}=0,$$

其余基本括号为零。它在这些坐标中是常张量，故满足反对称、Leibniz 和 Jacobi，秩为 $2N$。

取

$$\boxed{H_N=\sum_{i=1}^N\frac{P_i^2}{2S_i}}.$$

则 Hamilton 方程就是上述精确参数流。$P_1,\ldots,P_N$ 微分独立、两两对易且守恒。在某个 $P_i\ne0$ 的正则域上，可用 $H_N$ 替换该 $P_i$，得到包含 Hamilton 函数的一组完整积分。

**参数系统定理。** 对每个有限 $N$，上述泊松参数系统在每个固定 $S$ 的非空连通辛叶上刘维尔可积；时间流对所有实 $t$ 存在，保持正则谱条件。临界点按通常正则域表述处理。此定理不需要把 $N=1,2,3$ 的实验逐个外推。

### 4.3 这个构造的意义与局限

把已知线性相位演化 Hamilton 化，本身并不足以宣称重大新可积发现。这里额外核对了：精确原方程、物理参数识别、传输谱系数、格点移动、碰撞相移和跨 $N$ 边界。创新性还需与已有孤子力学文献比较。

不固定 $S$，得到一族辛叶组成的退化泊松系统；并不是因为 $3N$ 可能为奇数就无法谈可积性。另一方面，不能把所选的 $S_i$ Casimir 直接当作原 $J_0$ 已有的 Casimir。

<a id="sec-integrals"></a>
## 5. 统一的谱守恒量及独立性

### 5.1 生成式与前四项

采用既有形式传输函数的约定

$$T_N(z)=\prod_{i=1}^N\frac{z+q_i}{z-p_i},\qquad
\log T_N(z)=\sum_{r\ge1}C_r^{(N)}z^{-r},$$

得到

$$\boxed{C_r^{(N)}=\frac1r\sum_{i=1}^N[p_i^r-(-q_i)^r]}.$$

因此

$$
C_1=\sum_i S_i,\qquad C_2=\frac12\sum_iS_ic_i,
$$
$$
C_3=\sum_i\left(\frac{S_i^3}{12}+\frac{S_ic_i^2}{4}\right),\qquad
C_4=\frac18\sum_i S_ic_i(S_i^2+c_i^2).
$$

与时间 Hamilton 函数的联系是

$$H_N=2C_3-\frac16\sum_iS_i^3,\qquad C_2=\frac12\sum_iP_i.$$

谱参数随时间不变，故这些量守恒；它们只依赖 $P,S$，故在所选括号下两两对易。这里是模空间上的谱函数；尚未把它们全都实现为原场任意初值上的可容许守恒泛函。

### 5.2 完整参数空间：前 2N 项独立

$$\frac{\partial C_r}{\partial p_i}=p_i^{r-1},\qquad
\frac{\partial C_r}{\partial q_i}=(-q_i)^{r-1}.$$

$C_1,\ldots,C_{2N}$ 的谱 Jacobian 是节点

$$p_1,\ldots,p_N,-q_1,\ldots,-q_N$$

组成的 Vandermonde 矩阵。当前条件排除了节点重合，所以其行列式非零。这给出 $2N$ 个谱方向上的独立积分；还有 $N$ 个相位方向不被谱量记录。

### 5.3 固定 S 的叶：需要 N 项

$C_1$ 已固定，不能算一个叶内独立积分。对 $k=1,\ldots,N$，

$$\partial_{c_i}C_{k+1}
=\frac12\left[\left(\frac{c_i+S_i}{2}\right)^k-
\left(\frac{c_i-S_i}{2}\right)^k\right].$$

它关于 $c_i$ 的最高次项是 $kS_ic_i^{k-1}/2^k$，所以 Jacobian 行列式最高总次数部分为

$$\frac{N!\prod_iS_i}{2^{N(N+1)/2}}\prod_{i<k}(c_k-c_i),$$

不恒为零。因此 $C_2,\ldots,C_{N+1}$ 在一般位置独立；特殊零点处可用本来处处独立的 $P_i$ 描述完整积分。

对双孤子，精确小行列式为

$$\det\frac{\partial(C_2,C_3)}{\partial(c_1,c_2)}
=\frac{S_1S_2(c_2-c_1)}4.$$

论文 Fig.3、Fig.4 分别得到 $-1$、$6$。

### 5.4 数量不能无限重复计算

固定 $N$ 时，虽然有无限多公式 $C_r$，却至多有 $2N$ 个独立谱自由度；固定 $S$ 后至多有 $N$ 个叶内独立、对易积分。不同阶的公式不等于新的独立方向。

<a id="sec-inverse"></a>
## 6. 任意 N：从物理场反推孤子参数

这一节解决“参数上的积分是否真的对应物理解”的问题。结论在 §2.4 的非共振正则域成立；解族采用参数诱导的光滑模空间结构，不默认某个 Sobolev 空间中的全局嵌入。

### 6.1 从完整物理场恢复归一化 tau

从 $u,v$ 得到 $W=v-\delta_0u$。定义

$$R_j(x)=\exp\left(\frac h4\int_{-\infty}^xW_j(y)dy\right),$$
$$L_j(x)=\exp\left(\int_{-\infty}^x\left(\frac{u_j(y)}2+\frac h8W_j(y)\right)dy\right).$$

因为 $S_i>0$，$x\to-\infty$ 时 $F_j,G_j\to1$，故

$$R_j=G_{j+1}/G_j,\qquad L_j=F_j/G_j.$$

又因为 $0<\chi_i<1$，固定 $x$ 时 $j\to+\infty$ 有 $G_j\to1$，从而

$$\boxed{\log G_j=-\sum_{k=j}^{\infty}\log R_k,\qquad F_j=L_jG_j.}$$

这是望远镜极限。有限指数和使尾部按几何级数衰减；在紧谱参数集、紧 $x$ 集上，固定阶参数导数只增加多项式格点因子，仍可控。这里没有把全空间发散的 Hamilton 积分强行赋值。

### 6.2 指数项的唯一性

$G$ 是有限项

$$b_I e^{\alpha_Ix}r_I^j,\qquad
\alpha_I=\sum_{i\in I}S_i,\quad r_I=\prod_{i\in I}\chi_i$$

之和。不同 $\alpha$ 的实指数函数线性独立；相同 $\alpha$ 下，不同 $r>0$ 的序列 $r^j$ 由 Vandermonde 矩阵区分。所以非共振条件下，完整 $G$ 唯一确定全部支持点 $(\alpha_I,r_I)$ 和系数 $b_I$。

### 6.3 从全部子集项找出单个孤子

把支持写为 $v_i=(S_i,\log\chi_i)$ 的全部子集和。因为每个 $S_i>0$，可以逐次恢复生成元：

1. 去掉空集项，已知子集和初始化为 $\{0\}$；
2. 取剩余项中第一坐标最小者，固定规则处理并列；它必是尚未恢复的一个单项；
3. 从剩余支持中删去“这个新单项＋每个已知子集和”，再扩大已知集合；
4. 重复直至恢复全部 $N$ 项。

理由是：含有未知单项又额外含其他正 $S$ 项的和，比那个未知单项更大；全由已知单项组成的和则早已删除。非共振确保删除不发生歧义。

单项在 $G$ 中的系数是 $e^{\Theta_i}$，在 $F$ 中的系数是 $\gamma_ie^{\Theta_i}$，故可以恢复 $\Theta_i,\gamma_i$。

### 6.4 恢复 p、q 的显式公式

为避免与动量混淆，记 $\widetilde P=p-a$、$\widetilde Q=q+a$。由 $\gamma,\chi$ 可解得

$$\widetilde P=d\frac{\chi+1-2\gamma}{\chi-1},\qquad
\widetilde Q=d\frac{\gamma\chi+\gamma-2\chi}{\gamma(\chi-1)}.$$

分母在当前条件下非零。恢复 $p,q$ 后按 $p$ 排序，就除去了标签置换。于是整个参数映射在所声明的域上是单射，而不仅是一个参数生成器。

### 6.5 没有隐藏的无效切向方向

若参数变化使 $\delta u=\delta W=0$，上一重构式给出 $\delta G=\delta F=0$。展开后，$\delta G$ 是

$$e^{\alpha_Ix}r_I^j\bigl(\delta b_I+b_Ix\delta\alpha_I+b_Ij\delta\log r_I\bigr)$$

的有限和。先用 $x$ 的指数多项式独立性，再用 $r^j,jr^j$ 的合流 Vandermonde 独立性，可知所有系数变分为零。单项因而给出 $\delta S_i=\delta\chi_i=\delta\Theta_i=0$；$\delta F=0$ 再给出 $\delta\gamma_i=0$。显式反演说明全部谱参数变分为零。

因此映射是浸入。有限维切空间可由有限个物理场取值区分，逆函数定理给出局部观测坐标。**单射、浸入和参数诱导的模空间结构，不自动等于在任意选定的环境函数空间里全局嵌入。**

### 6.6 论文算例的直接检查

在 $a=2,h=1/8,x=t=0$、原振幅归一化下：

- 单孤子 $(Q,P)\mapsto(u_0(0),W_0(0))$ 的 Jacobian：Fig.1(a) 为 $-1202688/2070617$；Fig.1(b) 为 $131072/6528025$；
- 双孤子用 $(u_0,W_0,u_1,W_1)$ 检查四个固定 $S$ 的参数，Fig.3、Fig.4 均得到非零精确有理行列式。

这些是定位符号错误的直接证书；任意 $N$ 的论证是上面的重构与独立性证明，不是有限样例外推。

<a id="sec-scattering"></a>
## 7. 格点移动和孤子散射的相容性

格点前进一步使

$$Q_i\mapsto Q_i-\frac{\log\chi_i}{S_i},\qquad P_i\mapsto P_i.$$

固定 $S$ 时，每个位置修正只依赖自己的 $P_i$，所以这是正则剪切变换。

不同速度下的分离散射相移为

$$\Delta Q_i=-\frac1{S_i}\sum_{k\ne i}\operatorname{sgn}(c_i-c_k)\log A_{ik}.$$

而

$$A_{ik}=\frac{(S_i-S_k)^2-(c_i-c_k)^2}{(S_i+S_k)^2-(c_i-c_k)^2}.$$

在速度次序固定的正则区域内，直接微分可得

$$\partial_{P_k}\Delta Q_i=\partial_{P_i}\Delta Q_k.$$

所以相移映射保持同一正则括号；成对恒等式求和即适用于任意 $N$。这验证了参数结构与精确碰撞的相容性，但仍不证明它唯一或由 $J_0$ 继承。

<a id="sec-gluing"></a>
## 8. 跨 N 拼接：零强度边界

### 8.1 为什么“把孤子移远”不是所需的删除

固定 $S_*>0$，让 $\theta_*\to-\infty$，额外孤子会离开每个固定的局部观测窗口，但 $C_1$ 仍多出 $S_*$。因此若把这种局部场极限直接认成低阶解，就不能同时保持这串谱量连续。

这只排除该拓扑下、保留这些谱量的无记忆删除；不排除记录“远处仍有孤子”的边界，也不是全系统不可积证据。

### 8.2 使谱强度 S 消失

令 $r=c-2a$，则

$$\gamma=-\frac{S+r+h}{S-r-h},\qquad
\chi=\frac{(S+h)^2-r^2}{(S-h)^2-r^2}.$$

新增孤子取 $S_*\to0$，$c_*$ 保持有界，避开 $r_*=\pm h$ 及 $(c_*-c_i)^2=S_i^2$ 等极点。在 $S_*=0$ 的正则延拓上，

$$\gamma_*=\chi_*=1,\qquad A_{i*}=1,\qquad E_*=e^{\Theta_*}.$$

子集展开按是否包含新指标配对，给出

$$F_{N+1}=(1+e^{\Theta_*})F_N,\quad
G_{N+1}=(1+e^{\Theta_*})G_N.$$

$G_{j+1}$ 也乘同一个常数，因此物理 $u,W,v$ 完全不变。多个零强度项可按任意顺序删除。

这使用重写后的、可延拓的子集表达。不能不处理归一化，就把 $p+q=0$ 代入原来含 $1/(p+q)$ 的行列式条目。

### 8.3 物理极限与统一谱量

在有界且远离极点的谱参数区域，新系数均为 $1+O(S_*)$。将新 tau 与 $(1+E_*)$ 乘旧 tau 比较，各正单项系数比为 $1+O(S_*)$。对数导数是指数斜率的加权均值，高阶对数导数是相应累积量；有限斜率有界，所以固定阶 $x$ 导数的物理场差为 $O(S_*)$，可对 $x,j,t$ 一致控制。共同参考因子在物理组合中消掉。

新增孤子对谱量的贡献为

$$\frac{((S_*+c_*)/2)^r-((c_*-S_*)/2)^r}{r},$$

它是含因子 $S_*$ 的多项式。因此全部 $C_r$ 和新增 Hamilton 项 $S_*c_*^2/2$ 都趋于零。谱因子 $(z+q_*)/(z-p_*)$ 同时约成一。

这解释了为什么这种删除能使“物理场＋守恒量”一起衔接。它是不同初始状态的极限，**不是**时间演化中守恒量下降或孤子自发消失。

### 8.4 泊松括号在边界上的相容性

为处理 $S=0$，不用会除以 $S$ 的 $Q$ 坐标，而用

$$\{\Theta_i,c_k\}=-\delta_{ik},\qquad\{S_i,\cdot\}=0.$$

选择能光滑延拓、且在零强度边界不依赖被删除的 $\Theta_*,c_*$ 的观测量 $A,B$。这些边界上的相应偏导数为零，所以括号中新增指标的贡献消失，其余项正好是旧括号。

于是先算括号再删除，和先删除再算括号，结果相同。这个结论依赖明确的相容观测量类别；$\Theta_*$ 本身不能作为已经删除该孤子后的观测量。

<a id="sec-atomic"></a>
## 9. 不预先指定 N 的共同泊松代数

### 9.1 有限原子记录

把有限配置表示为

$$\mu=\sum_{i=1}^N S_i\,\delta_{(S_i,\Theta_i,c_i)}.$$

置换编号不改变 $\mu$，零强度项就是零测度，因此没有残留的虚假标签。原子仍只有有限多个；这个表达本身不证明无穷孤子 tau 收敛。

对测试函数 $\phi$，记

$$M_\phi(\mu)=\int\phi\,d\mu=\sum_iS_i\phi(S_i,\Theta_i,c_i).$$

采用局部光滑测试、以及对 $S,c$ 多项式增长而相位方向适当有界的测试，并对有限柱函数作链式运算；用这些分离观测量指定拓扑和光滑观测代数。谱参数逃向无穷时另需矩控制，不把局部场收敛等同于所有谱矩收敛。

### 9.2 不含 N 的定义

在标记空间上定义

$$[\phi,\psi]_B=-S(\phi_\Theta\psi_c-\phi_c\psi_\Theta).$$

$S$ 是中心变量，所以此括号满足 Jacobi。共同的矩括号为

$$\boxed{\{M_\phi,M_\psi\}=M_{[\phi,\psi]_B}}.$$

对有限柱函数按链式法则延拓。在一个 $N$ 原子层上，右侧等于

$$-\sum_i S_i^2(\phi_\Theta\psi_c-\phi_c\psi_\Theta)_i,$$

恰与原来的参数括号计算一致。因此这是一个真正跨 $N$ 定义的共同代数，不仅是把一份公式写 $N$ 次。

局部用远离 $S=0$ 的截断函数选出不同原子，可以恢复各个坐标，故该代数局部不仅包含常数或谱量。任意与这种代数对应的真实商空间全局分层性质，还需额外几何审查；不自动套用要求适当作用、局部紧致等条件的奇异约化定理。

### 9.3 共同 Hamilton 函数与层级

$$H(\mu)=M_{c^2/2}(\mu),\qquad C_r(\mu)=M_{b_r}(\mu),$$
$$b_r(S,c)=\frac{((S+c)/2)^r-((c-S)/2)^r}{rS}.$$

$b_r$ 在 $S=0$ 有多项式延拓，取值 $(c/2)^{r-1}$。这些函数与相位无关，故全部对易。

时间流是标记变换

$$ (S,\Theta,c)\mapsto(S,\Theta-Sct,c) $$

对 $\mu$ 的推前。它保留每层及各固定 $S$ 的辛叶。格点剪切也与零强度删除相容。

**拼接结论的准确形式：**所有有限正则孤子层共享一个泊松观测代数、Hamilton 函数及谱层级；它们通过零强度边界相容连接，各固定 $N$、固定 $S$ 的正则叶仍刘维尔可积。整个并集不因此变成一个普通的固定维数刘维尔系统。

<a id="sec-obstructions"></a>
## 10. 原场 J₀ 的继承障碍

不能把“找到了新的参数括号”写成“原场泊松约化已经证明”。对单孤子，若采用让以下质量成为可容许 Casimir 的原 $J_0=-\operatorname{offdiag}(D)$ 边界设置，则

$$M_u=\log\frac{(p-a)^2-d^2}{(q+a)^2-d^2},\qquad
M_W=\frac4h\log\chi.$$

但新参数括号一般给出 $\{Q,M_u\}\ne0$、$\{Q,M_W\}\ne0$。在两个论文单孤子点，精确结果为

| 算例 | $\{Q,M_u\}$ | $\{Q,M_W\}$ |
|---|---|---|
| Fig.1(a) | $-10496/41769$ | $-131072/208845$ |
| Fig.1(b) | $-14592/28985$ | $131072/86955$ |

因此在这个质量确为 Casimir 的定义域内，新括号不能是保留这些 Casimir 的直接泊松限制或 Dirac 约化。原 Casimir 不会被常规 Dirac 修正变成非 Casimir。

此前还检查了双孤子的一个朴素“逐格点辛形式取单位长度平均”方案：在固定两种总质量的谱叶上，必要的一形式 $\sum_i c_i\,d\Pi_i$ 不闭。它排除的是这个具体平均约化，不能推出所有边界扩充或其他可容许观测量设置都失败。

若继续追原结构，需要真正推导边界自由度、辛边界项或合适的散射约化。已有的新参数模型则可以作为独立的、明示结构来源的结果保留。

<a id="sec-claims"></a>
## 11. 可以与不可以宣称的结论

### 可作为待独立复核的定理草稿表述

> 对任意有限 $N$，在指定正系数、非共振的标准半离散 DLW 孤子族上，以谱参数与相位诱导光滑模空间结构，可以构造秩为 $2N$ 的泊松张量，使精确孤子时间演化 Hamilton 化，并在每个固定 $S$ 的辛叶上刘维尔可积。零强度退化与物理重构、共同谱层级及相容泊松观测量匹配；所有有限孤子数可在一个有限原子观测框架中统一描述。

### 本文没有证明

- 原半离散 DLW 的所有解、所有边界条件上的刘维尔可积性；
- 所选参数括号是原 $J_0$ 的继承，或存在已证明的双 Hamilton 兼容对；
- 无穷格点等于无穷孤子，或无穷多个孤子的 tau、谱矩全部收敛；
- 共振指数、谱点碰撞、breather、有理解和所有奇异层都已包含；
- 一般环境函数空间中的全局嵌入及完整 Whitney 分层定理；
- 非线性适定性、稳定性或全离散数值算法保持上述结构；
- 研究创新性已完成文献排重，或这些草稿已达到无需复核的发表状态。

特别是：显式相位直线运动允许 Hamilton 化，因此不能只以“存在正则坐标”作为充分创新点。可评价的内容应是严格模空间识别、与原谱数据和散射的联系、相容退化，以及与已有文献的差异。

<a id="sec-verification"></a>
## 12. 复核、资料与下一步

### 12.1 本次交付的可复核材料

- [验证说明与运行方式](Workspaces/dlw_liouville_20261005/README.md)
- [任意阶谱量、反演及一般代数证书](Workspaces/dlw_liouville_20261005/verify_general_structure.py)
- [单／双孤子参数与谱量](Workspaces/dlw_liouville_20261005/moduli_certificate.py)
- [双孤子物理坐标精确秩](Workspaces/dlw_liouville_20261005/physical_immersion_certificate.py)
- [单孤子物理坐标与质量障碍](Workspaces/dlw_liouville_20261005/single_and_casimir_certificate.py)
- [跨 N 的零强度证书](Workspaces/dlw_liouville_20261005/cross_n_certificate.py)
- [共同原子泊松括号及 Jacobi](Workspaces/dlw_liouville_20261005/atomic_poisson_certificate.py)
- [拼接证明补充](Workspaces/dlw_liouville_20261005/CROSS_N_GLUING_PROOF.md)
- [原子泊松构造补充](Workspaces/dlw_liouville_20261005/ATOMIC_POISSON_CONSTRUCTION.md)
- [本次运行结果](Workspaces/dlw_liouville_20261005/validation.json)

本次运行的是精确符号代数与有理数证书。它们辅助复核一般证明；没有以 $N\le6$ 的检查冒充任意 $N$ 定理，也没有以数值扫描冒充连续域估计。没有重新运行原 Lean 工程，也没有执行新的 PDE 时间数值模拟。

### 12.2 参考资料与各自用途

1. [原双线性到非线性闭合](Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md)：固定方程、物理变量和边界自由度。
2. [Gram 与相移核验](Workspaces/dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md)：任意 $N$ 的精确 tau 及交织结构。
3. [谱结构后续](Workspaces/dlw_semidiscrete/S_INTEGRABILITY_STATUS.md)：既有谱波函数与传输约定；不能由标题推定完整 IST。
4. Ruoci Sun, [Complete integrability of the Benjamin–Ono equation on the multi-soliton manifolds](https://link.springer.com/article/10.1007/s00220-021-03996-1), CMP 383 (2021)：真正的多孤子流形辛几何与可积性参照，不是本文 DLW 定理的自动来源。
5. Ruijsenaars, [Action-angle maps and scattering theory for some finite-dimensional integrable systems I. The pure soliton case](https://ir.cwi.nl/pub/2452)：有限维孤子力学与散射的比较方向。
6. Sjamaar–Lerman, [Stratified symplectic spaces and reduction](https://annals.math.princeton.edu/1991/134-2/p05) (1991)：奇异空间和层间 Hamilton 结构的几何参照。
7. Lê–Somberg–Vanžura, [Poisson smooth structures on stratified symplectic spaces](https://arxiv.org/abs/1011.0462)：光滑观测结构的参照；本文未验证其所有全局假设。

### 12.3 最值得继续的事情

先独立审阅本稿中的反向重构、共同观测量代数及拓扑条件。然后决定论文主张的强度：若以精确孤子模空间为对象，应把新括号来源写明；若要声称原场 Hamilton 约化，必须另行解决质量、边界项和散射定义域。不要为了“覆盖所有解”无限扩大任务，也不要把一个漂亮的参数模型误写成整个 PDE 的可积性证明。

<a id="sec-field-theorem"></a>
## 13 一般周期物理场的独立对合守恒族

本节给出本轮研究的主要结果。格点周期记为 $M\ge2$，孤子个数仍记为 $N$；$M$ 个格点上的 $x$ 变量连续，因此这里的状态空间是无限维函数空间。

### 13.1 相空间与实际 Hamiltonian

取实光滑周期场 $x\in\mathbb T_{L_x}$、$j\in\mathbb Z/M\mathbb Z$，令

$$
U=u+2a,\qquad w=v-\delta_0u-4,\qquad\beta=\frac{h^2}{32}.
$$

记 $\Pi$ 为格点平均、$P_0=I-\Pi$。固定 $c\ne0,\gamma\in\mathbb R$，采用平均闭合

$$
\Pi w=c,\qquad\Pi(Uw)=\gamma.
$$

独立场坐标可取

$$
p=P_0U,\qquad s=w-c,\qquad
U=p+\frac{\gamma-\Pi(ps)}c,\qquad w=c+s.
$$

这里的 $p,s$ 是场函数。采用 $h\sum_j\int dx$ 的变分配对，原场约化泊松算子为

$$
J_{\rm red}=-\begin{pmatrix}0&P_0\partial_x\\P_0\partial_x&0\end{pmatrix}.
$$

令 $R=(\delta_-|_{P_0})^{-1}M_-P_0$；它是固定的斜对称格点矩阵。定义

$$
\mathcal H_0=h\sum_j\int e_j\,dx,
\qquad e_j=\frac12U_j^2w_j+\frac\beta3w_j^3+w_jU_{j,x}
+\frac12w_j(Rw_x)_j,
$$
$$
\mathcal K=\mathcal H_0-\gamma h\sum_j\int U_j\,dx,
\qquad
\mathcal P=h\sum_j\int p_js_j\,dx.
$$

直接变分得到

$$
\mathcal K_p=Uw-\gamma-w_x,\qquad
\mathcal K_s=P_0\left(\frac{U^2}2+\beta w^2+U_x+Rw_x\right),
$$
$$
p_t=-\partial_x\mathcal K_s,\qquad s_t=-\partial_x\mathcal K_p.
$$

因此 $\mathcal K$ 生成原来的物理时间演化，$\mathcal P$ 生成负向空间平移。各分量的 $x$ 平均是该常泊松算子的 Casimir。

### 13.2 全族守恒量

从物理场构造转移算子与单值算子

$$
T_j=\left(D-\frac{U_j}{2}+\frac{hw_j}{8}\right)^{-1}
\left(D-\frac{U_j}{2}-\frac{hw_j}{8}\right),
\qquad \mathcal M=T_{M-1}\cdots T_0,\qquad D=\partial_x.
$$

设

$$
G=\frac{hMc}{4},\qquad B=\frac\gamma{2c},\qquad
L=-G(\mathcal M-I)^{-1}+(B-G/2)I.
$$

其展开为 $L=D+\sum_{k\ge1}\ell_kD^{-k}$。定义

$$
\boxed{\mathcal C_n=\frac1n\operatorname{Tr}L^n
=\frac1n\int\operatorname{res}_D L^n\,dx,\qquad n\ge1.}
$$

每个固定阶数的留数只涉及有限个场导数。以下是本节的具体结论。

**定理形式的结论。** 对每个固定有限 $M\ge2$，在上述平均闭合的光滑周期相空间上，

$$
\boxed{\mathcal K,\quad\mathcal P,\quad\mathcal C_3,\quad
\mathcal C_5,\quad\ldots}
$$

是包含物理 Hamiltonian 的两两对合守恒族。任意有限前缀的微分在泛型区域独立；同样的独立性见证可以放在包含均匀背景的固定分量均值辛叶内。由此得到一般周期场的无穷维 Hamilton 可积结构，采用的是无穷独立对合守恒层级的含义。

### 13.3 守恒性的任意阶证明

周期完整交织关系给出

$$
L_t=[-D^2-V_0,L].
$$

比较零阶系数可得 $(V_0)_x=2(\ell_1)_x$；空间常数与 $L$ 交换，故

$$
L_t=[-(L^2)_+,L].
$$

利用周期伪微分算子的迹恒等式 $\operatorname{Tr}[A,B]=0$，

$$
\frac{d\mathcal C_n}{dt}
=\frac1n\operatorname{Tr}[-(L^2)_+,L^n]=0.
$$

这里由平均闭合构造周期热势时，保留格点共同模态；$\int\Pi U\,dx$ 的守恒性由平移 Hamiltonian $\mathcal P$ 保证。

### 13.4 对合性的任意阶证明

令 $b_j=U_j/2,d_j=hw_j/8$。在原常场括号下，$b_j+d_j$ 与 $b_j-d_j$ 是符号相反的独立一阶因子场。乘积、求逆的 Adler 因子化规则将其送到 $\mathcal M$ 的括号。相应 Adler 映射写为

$$
A_{\mathcal M}(X)=(\mathcal M X)_+\mathcal M
-\mathcal M(X\mathcal M)_+.
$$

令 $A=(\mathcal M-I)^{-1}$。在对约束面外作变分时保持 $G,B$ 为固定归一化常数，则

$$
\nabla_{\mathcal M}\mathcal C_n=G A L^{n-1}A,
\qquad [\nabla_{\mathcal M}\mathcal C_n,\mathcal M]=0.
$$

所以 $A_{\mathcal M}(\nabla\mathcal C_n)$ 是与 $\mathcal M$ 的交换子；再与另一个同样交换的梯度配对，迹为零。这证明所有阶数的谱泛函在因子场括号下对合。

接下来核对原约化括号。共同改变 $U_j\mapsto U_j+2f(x)$ 会使转移算子作共同的标量规范共轭；谱迹保持不变，因而

$$
\sum_j\frac{\delta\mathcal C_n}{\delta U_j}=0.
$$

平均约束重构的链式法则于是给出

$$
(\mathcal C_n)_p=(\mathcal C_n)_U,\qquad
(\mathcal C_n)_s=P_0(\mathcal C_n)_w.
$$

在 $J_{\rm red}$ 的配对中，$P_0$ 可以移到已经零格点平均的梯度上。因此约化括号恰好等于上述因子场括号，得到

$$
\boxed{\{\mathcal C_m,\mathcal C_n\}_{\rm red}=0\qquad(m,n\ge1).}
$$

因子化规则的原始来源是 [Mas–Ramos 的乘积与求逆定理](https://arxiv.org/html/q-alg/9501009v2)；与本 DLW 平均闭合和原括号的对应由这里的链式法则完成。

### 13.5 任意长独立子序列

考虑相空间内的切片

$$
w_j=c,\quad U_0=2B+2f(x),\quad U_1=2B-2f(x),
\quad U_j=2B\ (j\ge2),\quad\int f\,dx=0.
$$

奇数阶迹的二次部分满足

$$
\mathcal C_{2k+1}^{(2)}
=\frac2M(-1)^{k+1}\int(D^k f)^2dx
+\text{较低导数阶的二次项}.
$$

系数的推导如下。记 $\eta=hc/8$，在该切片对 $D,f,B,\eta$ 同赋权一。归一化后的 $L$ 系数在 $\eta=0$ 有代数延拓，因为 $\mathcal M-I$ 含因子 $\eta$，而归一化恰好消去它。该系数极限为

$$
L\big|_{\eta=0}=M\left[\sum_j(D-B-f_j)^{-1}\right]^{-1}+B,
\quad(f_0,f_1,f_2,\ldots)=(f,-f,0,\ldots).
$$

二次展开给出

$$
L\big|_{\eta=0}=D-\frac2M f(D-B)^{-1}f+O(f^4).
$$

最高的二次导数项没有剩余权重容纳 $B$ 或 $\eta$，故在 $B=\eta=0$ 的系数极限计算即可得到上述 $2/M$ 与符号。这是提取多项式系数的方法；实际见证仍取 $c\ne0$。

令 $f=\varepsilon\sum_{i=1}^N a_i\cos(k_ix)$，其中非零频率两两不同、$a_i\ne0$。$\mathcal C_1,\mathcal C_3,\ldots,\mathcal C_{2N-1}$ 的振幅 Jacobian 首项是不同次数的频率多项式在 $k_i^2$ 的取值矩阵，行列式含非零因子

$$
\prod_{i<j}(k_j^2-k_i^2).
$$

故每个有限块均存在独立见证。固定阶数的泛函在约化场坐标中是微分多项式；相应非零见证行列式的非零集开且稠密。取可数交得到各有限块同时独立的泛型集合。

### 13.6 把实际 Hamiltonian 纳入独立族

在上述 $s=0$ 切片，$d\mathcal P$ 对所有 $p$ 的振幅方向都为零，而奇数阶迹对这些方向的 Jacobian 可逆。再取

$$
\delta s_0=f,\qquad\delta s_1=-f,\qquad\delta s_j=0\ (j\ge2),
$$

便有 $d\mathcal P=4h\int f^2dx\ne0$。所以 $\mathcal P$ 与任意有限奇数阶块联合独立。平移不变性给出 $\{\mathcal P,\mathcal C_n\}=0$。

首个迹与原能量的关系为

$$
\mathcal C_1=-\frac{\mathcal H_0}{8G}
+\left(\frac{G^2}{12}+B^2\right)L_x,
$$

从而

$$
\mathcal K=-8G\mathcal C_1+\frac\gamma c\mathcal P+\text{常数}.
$$

$G\ne0$，因此以 $\mathcal K$ 替换 $\mathcal C_1$ 保持独立性。这就得到定理中展示的具体守恒族。

<a id="sec-field-matrix"></a>
## 14 任意有限周期的矩阵表示与物理泊松坐标

令 $m=M-1$、$S=G/2=\sum_jd_j$、$\nu=B-S$。记 $H$ 为严格下三角全一矩阵，$\mathbf d=(d_j)$，$\mathbf1=(1,\ldots,1)^T$，并令

$$
C=\operatorname{diag}(b-d)-2\operatorname{diag}(d)H
-\frac\nu S\mathbf d\mathbf1^T.
$$

取 $Z$ 的列为 $e_j-e_m$，$E$ 选取前 $m$ 个分量，$K=E-\mathbf d_{<m}\mathbf1^T/S$。转移波函数之差的基变换给出

$$
\begin{pmatrix}\phi\\\xi\end{pmatrix}_x
=\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}
\begin{pmatrix}\phi\\\xi\end{pmatrix},
$$
$$
q=\mathbf1^TCZ,\qquad
r=\frac1S K(C\mathbf d-\mathbf d_x),\qquad V=KCZ,
$$
$$
\boxed{L=D-q(DI_m-V)^{-1}r.}
$$

完整推导见 [全周期矩阵 Lax 证明](Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md)。基变换仅要求总量 $S\ne0$。

### 14.1 可直接计算的守恒密度

令

$$
z_1=r,\qquad z_{n+1}=Vz_n-Dz_n-
\sum_{i+j=n\atop i,j\ge1}z_i(qz_j),\qquad\rho_n=-qz_n.
$$

则 $\mathcal C_n=\int\rho_n dx$，密度代表相差一个总导数时给出同一积分。前几项为

$$
\rho_1=-qr,\qquad\rho_2=qr_x-qVr,
$$
$$
\rho_3=(qr)^2-qV^2r+qV_xr+2qVr_x-qr_{xx}.
$$

任意阶局部恒等式是

$$
(\rho_n)_t+D\left[(\rho_n)_x+2\rho_{n+1}
-\sum_{i+j=n\atop i,j\ge1}\rho_i\rho_j\right]=0.
$$

### 14.2 一般周期的独立物理场坐标

可以取 $m$ 对场函数 $(q_j,d_j)$ 为坐标，其中

$$
q_j=b_j-b_m-d_j-2\sum_{k=j+1}^{m}d_k+d_m,\qquad j<m.
$$

反向恢复公式为

$$
d_m=S-\sum_{j<m}d_j,\qquad
b_m=B-\sum_{j<m}d_j-\frac1S\sum_{j<m}d_jq_j,
$$
$$
b_j=b_m+q_j+d_j+2\sum_{k=j+1}^{m-1}d_k+d_m.
$$

这是原约化坐标 $(p,s)$ 的仿射可逆变换。用普通积分定义泛函导数时，原物理泊松括号变成

$$
\{q_i(x),d_j(y)\}=-\frac1{16}\delta_{ij}D_x\delta(x-y),
\quad\{q_i,q_j\}=\{d_i,d_j\}=0.
$$

若统一使用 $h\sum\int$ 配对，则对应算子系数为 $-h/16$。这两个写法是同一括号的不同梯度归一化。

矩阵分量由这些独立坐标确定，例如

$$
V_{ij}=\delta_{ij}(b_i-d_i)-2d_i\mathbf1_{j<i}-\frac{d_iq_j}{S}.
$$

三格点有 $V_{01}=-d_0q_1/S$、$V_{10}=-d_1(2S+q_0)/S$，从而在相应分母非零的区域，可从 $q_0,q_1,V_{01},V_{10}$ 恢复全部物理场。详见 [全周期泊松坐标证明](Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_FREE_FIELD_POISSON.md)。

<a id="sec-field-two-site"></a>
## 15 两格点的一般场与三 Hamilton 结构

两格点时记 $p_0=p,p_1=-p,s_0=s,s_1=-s$，$\eta=hc/8$。在 $p-2\eta\ne0$ 的坐标域，定义新场

$$
\alpha=\left(\frac p2-\eta\right)
\left[-\frac{s_x}c+\left(1-\frac{s^2}{c^2}\right)
\left(\frac p2+\eta\right)\right],
\qquad d=B-\frac{ps}c+\frac{p_x}{p-2\eta}.
$$

得到

$$
L=D-(D-d)^{-1}\alpha,
$$
$$
\alpha_t=\alpha_{xx}-2(\alpha d)_x,
\qquad d_t=-d_{xx}-(d^2)_x+2\alpha_x.
$$

固定分量均值后，该变换在均匀场附近局部可逆；完整 $L$ 的反向恢复还可通过 $\lambda_\pm=B\pm2\eta$ 处的 Riccati／Floquet 数据给出。零均值叶上的标记单值矩阵为非平凡 Jordan 情形，恢复证明保留了这一点。详见 [逆变换与局部层级](Workspaces/dlw_general_field_20261006/TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md)。

### 15.1 三个相容算子

令

$$
J_1=\begin{pmatrix}0&D\\D&0\end{pmatrix},\qquad
J_2=\begin{pmatrix}2\alpha D+\alpha_x&-D^2+dD\\
D^2+dD+d_x&-2D\end{pmatrix}.
$$

记 $z=2\alpha d-\alpha_x$，第三个算子为

$$
J_3=\begin{pmatrix}
2zD+z_x&D^3-2dD^2+(d^2-d_x-4\alpha)D-2\alpha_x\\
D^3+2dD^2+(d^2+3d_x-4\alpha)D+d_{xx}+2dd_x-2\alpha_x&-4dD-2d_x
\end{pmatrix}.
$$

以两格点归一化 $J_{ps}=-D\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$、$\mathcal K/(2h)$ 计算，变量变换的 Frechet 导数给出精确推前

$$
\boxed{J_{\rm phys}=-\frac1{2c}
\left[J_3-2BJ_2+(B^2-4\eta^2)J_1\right].}
$$

这是逐项核验的算子恒等式。利用局部可逆变换保持 Jacobi 恒等式，再比较上式对 $B,\eta$ 的多项式系数，可得三个算子各自为泊松算子且两两相容。

### 15.2 任意阶 Lenard 关系与物理时间

两场密度可递推为

$$
\rho_1=-\alpha,\qquad
\rho_{n+1}=d\rho_n-D\rho_n+\sum_{i=1}^{n-1}\rho_i\rho_{n-i}.
$$

写 $\mathcal C_n=\int\rho_n dx$，有

$$
J_2\delta\mathcal C_n=J_1\delta\mathcal C_{n+1},\qquad
J_3\delta\mathcal C_n=J_2\delta\mathcal C_{n+1}.
$$

任意阶证明由 Riccati 生成式及其变分给出；第三算子的完整生成恒等式包含零次平移项，取负幂系数后得到上述关系。物理时间明确满足

$$
\begin{pmatrix}\alpha_t\\d_t\end{pmatrix}
=J_1\delta\mathcal C_3=J_2\delta\mathcal C_2=J_3\delta\mathcal C_1.
$$

完整算子证明、归一化与标记谱值的 Casimir 联系见 [两格点泊松铅笔](Workspaces/dlw_general_field_20261006/TWO_SITE_POISSON_PENCIL.md)。

<a id="sec-field-analysis"></a>
## 16 一般场解的解析设置

### 16.1 高频增长的明确形式

在均匀背景 $U=\gamma/c,w=c$，非零格点 Fourier 模式 $\theta=2\pi m/M$ 与空间频率 $k$ 的线性化特征值为

$$
\lambda_\pm=-i\frac\gamma c k\ \pm
\sqrt{k^4-\frac{hc}{2}\cot(\theta/2)k^3-\frac{h^2c^2}{16}k^2}.
$$

正支实部随高频增长为 $k^2$。因此该背景附近通常的可微 Sobolev 初值解流受到明确限制。守恒层级与这种增长可以同时成立。

### 16.2 混合时间数据给出实际的一般场解

取可逆泊松变换 $A=p+Rs/2$。方程成为

$$
A_t=-A_{xx}+D F(A,s),\qquad s_t=s_{xx}+D G(A,s),
$$

其中

$$
F=-P_0(U^2/2+\beta w^2)-\tfrac12R(Uw),\qquad G=-P_0(Uw).
$$

它们是场变量的多项式，不含空间导数。给定 $A(T)=A_T,s(0)=s_0$，两部分各自沿稳定方向用热半群写成积分方程。在一维周期 $H^r$、$r>1/2$ 中，热半群导数估计使迭代的 Lipschitz 常数为 $O(\sqrt T)$，因而短时间存在唯一的有界 mild 解，并在时间区间内部平滑。

这些解满足同一个物理方程，沿其光滑部分守恒族保持常值。两端状态之间还满足 Hamilton 作用量的生成关系。详见 [混合时间存在性证明](Workspaces/dlw_general_field_20261006/MIXED_TIME_EXISTENCE.md)。三格点数值核验中，时间步减半后能量和下一阶守恒量漂移约缩小四倍，与所用二阶时间积分一致。

<a id="sec-field-evidence"></a>
## 17 本轮证明与核验材料

本轮内容为构造性证明草稿。各任意阶／任意周期结论的依据是正文中的代数与变分论证；符号证书用于核验展开、算子伴随、逆变换和具体阶数。

- [本轮材料入口](Workspaces/dlw_general_field_20261006/README.md)
- [独立对合守恒族及物理 Hamiltonian](Workspaces/dlw_general_field_20261006/CONSERVATION_FAMILY_VERDICT.md)
- [全周期矩阵 Lax 与密度递推](Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md)
- [全周期物理泊松坐标](Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_FREE_FIELD_POISSON.md)
- [两格点逆变换与局部守恒族](Workspaces/dlw_general_field_20261006/TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md)
- [两格点三 Hamilton 算子与 Lenard 证明](Workspaces/dlw_general_field_20261006/TWO_SITE_POISSON_PENCIL.md)
- [实际运行的检查结果](Workspaces/dlw_general_field_20261006/validation.json)

后续集中于完整周期谱坐标、角变量与守恒代数的谱完备性。两格点的三算子标量系数公式与一般 $M$ 的矩阵／自由场泊松实现分别记录，使用时按对应结构选择。

本轮参考的原始研究包括 [Mas–Ramos](https://arxiv.org/abs/q-alg/9501009)、[多 boson KP Hamilton 结构](https://arxiv.org/abs/hep-th/9401058)、[约束 KP 的矩阵 Hamilton 结构](https://arxiv.org/abs/solv-int/9801019)、[Kaup–Broer 的 dressing 研究](https://doi.org/10.1016/j.physd.2020.132478)，以及用于比较解析方法的[正反向抛物系统短时存在性研究](https://arxiv.org/abs/1806.08138)。具体 DLW 变换与归一化由本文计算。
