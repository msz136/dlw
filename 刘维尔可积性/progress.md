# 归档进度与证据边界

2026-10-11。本次是归档；已核对现有文稿的方程、记号、适用域及文件位置，未重新认证证明、执行研究脚本或进行新数值计算。未定位原证明的结论统一记为“既有报告声称，待独立复核”。最新完整报告见 [候选报告全文](sources/2026-10-11_mixed_bvp_candidate.md)，其中内部的“定理”“已证明”均是报告作者的声称。

本文保留归档时的证据边界。后续新增推导、实际检查记录和持续研究入口见 [research/STATE.md](research/STATE.md)，原始外部报告保留原样。

## 记号与闭合

[周期约化原稿](../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md) 使用 $U=u+2a$、$w=v-\delta_0u-4$，$\delta_0u_j=(u_{j+1}-u_{j-1})/(2h)$。其 $c=\Pi w$、$q=\Pi(Uw)$；[一般周期场稿](../Workspaces/dlw_general_field_20261006/RESEARCH_NOTES.md) 将 $q$ 固定为 `gamma`。本专题统一用 $m=\Pi w$、$q=\Pi(Uw)$、$\Gamma(t)$ 表示实全线平均通量多项式的常数项。该 $\Gamma$ 不是先验时间常数。

周期格点只强制 $m_{xx}=0$、$m_t+q_x=0$。周期 $x$ 强制 $m$ 为时空常数，却仍留下 $q=\Gamma(t)$；旧稿的固定 `gamma` 是自治闭合选择。当前实全线分支另选固定 $A\ne0$、$m=Ax$，因而 $q=\Gamma(t)$。两套闭合不同，不互相代入。候选报告另用 $c=2dA$ 作线性算子系数，与旧稿的平均 $c$ 无关；本专题摘要不复用该 $c$。

## 1. 有限维 Fourier 对数轮廓

既有报告声称，待独立复核；本次未定位其 Moser 原证明或半径证明，不能用历史孤子文稿替代。

偶数 $M$，$x$ 周期 $L$，$C_p,C_s>0$、$B\ne0$；每个有限 $N$ 取

$$
z=\sum_{n=1}^N(a_n\cos k_nx+b_n\sin k_nx),\qquad k_n=2\pi n/L,
$$

$$
p=\frac{C_pe^z}{\int_0^Le^z},\quad s=\frac{C_se^{-z}}{\int_0^Le^{-z}},\quad
b=B-z_x,\quad U_j=b+(-1)^jp,\quad w_j=(-1)^js.
$$

$m=0$，$\Gamma=ps=C_pC_s/[(\int e^z)(\int e^{-z})]$ 空间恒定；随初值改变，沿 $z_t=-Bz_x$ 的行波守恒。报告声称小邻域内有 $2N$ 维辛不变族及 $N$ 个独立对合积分

$$
I_n=\frac{C_n}{2}(A_n^2+B_n^2),\quad
C_n=\frac{hM\Gamma_0L}{k_n},\quad \Gamma_0=C_pC_s/L^2,
\quad H=BP,\quad P=hML\Gamma=P_0-\sum_nk_nI_n,
\quad P_0=hML\Gamma_0.
$$

$(A_n,B_n)$ 是 Moser 变换后的坐标，不是原始 $(a_n,b_n)$；积分微分独立性限于每个模态对均非零的正则区。报告给出的充分半径为 $R_N=\log(1+1/(2N))/(8\sqrt N)$，具体适用球、坐标及范数仍需原证明核对。各族始终保留 $m=0$、$ps$ 空间常数等限制；任意有限 $N$ 不能替代 $N=\infty$，也不说明在整个物理场空间中稠密。

## 2. 空间仿射族（目前暂置）

既有报告声称，待独立复核；原证明未定位。取 $R_j^\pm=U_j\pm(h/4)w_j=a_j^\pm(t)x+b_j^\pm(t)$，并额外闭合

$$
\Pi[U_t+D(U^2/2+h^2w^2/32)]=\kappa x+\delta,\quad \kappa>0,
\quad a'=\kappa-a^2,\quad b'=\delta-ab,\quad |a|<\sqrt\kappa.
$$

对每个 $(j,\pm)$ 定义

$$
Q=\frac{\operatorname{atanh}(a/\sqrt\kappa)}{\sqrt\kappa},\quad
P=\frac{b-\delta a/\kappa}{\sqrt{\kappa-a^2}},\quad
\{a,b\}=(\kappa-a^2)^{3/2},\quad H=\sum_{j,\pm}P_j^\pm.
$$

报告声称 $4M$ 维 / $2M$ 个独立对合积分，辛叶非紧。这是在约化族上构造的 Poisson 结构，未声称从全场自然继承。

## 3. 一般周期场旧路线

[守恒族原稿](../Workspaces/dlw_general_field_20261006/CONSERVATION_FAMILY_VERDICT.md) 在固定有限 $M\ge2$、周期 $x$、$m=c\ne0$、$q=\gamma$ 固定闭合及组件空间平均固定的域上，声称 $\mathcal K,\mathcal P,\mathcal C_3,\mathcal C_5,\ldots$ 两两对合、任意有限前缀泛型独立，且包含实际时间 Hamiltonian。[周期混合时间草稿](../Workspaces/dlw_general_field_20261006/MIXED_TIME_EXISTENCE.md) 使用该闭合构造解族；这与下述实全线混合候选定理不同。

[完备性与解析障碍原稿](../Workspaces/dlw_field_liouville_20261006/THEORY.md) 明确：无限独立对合只给出各向同性，未证明最大性 / 完备性或全局谱反演；常背景附近特定 Sobolev 可微初值流的高频障碍不否定守恒层级。本次未重跑其符号、数值或 Lean 历史检查。旧稿中较强的“可积”表述按其定义和前提阅读，不作为一般场完整 Liouville 定理。

## 4. 当前实全线一般函数分支

$M=2$、$d=h/8$、固定 $A\ne0$、$m=Ax$；重构与物理方程见 [README](README.md)。$\Gamma=p(0)s(0)$ 来自零点光滑闭合，$b(0)=-(ps)_x(0)/A$；不再限定 $p\propto e^z$、$s\propto e^{-z}$。$M=2$、$m=Ax$ 与实全线渐近仍是分支条件，不是全 $M$ 全场结果。

旧候选结构为

$$
J=-\frac1{2h}\begin{pmatrix}0&D\\D&0\end{pmatrix},\qquad
I_b=\operatorname{PV}\int_{\mathbb R}b,
$$

$$
K=h\operatorname{PV}\int_{\mathbb R}
\left[m(p^2+4d^2s^2)+2sp_x-\frac{(\Gamma-ps)^2}{m}\right],
\qquad
\mathcal dK=\alpha-2hI_b\mathcal d\Gamma,\quad
\mathcal d\alpha=2h\mathcal dI_b\wedge\mathcal d\Gamma,\quad \alpha=\iota_X\Omega.
$$

$\mathcal d$ 表示场空间外微分，区别于常数 $d=h/8$。一般非零的 $\mathcal d\alpha$ 阻碍该旧结构生成物理时间；局部有限阶或标量修正的排除只适用于相应候选类别。不能由此推断系统普遍不可积。

此前谱研究的原证明未定位：既有报告声称，待独立复核。谱平滑泛函 $I_\rho$ 是一族，可构造任意有限多个独立对合成员；这不是无限维完备性。实谱带速度 $v(\lambda)=-2A(\lambda^2-4d^2)$，$XF=-v\partial_\lambda F$。局部正则谱窗内，谱时钟 $c_{\rm clk}$ 满足 $Xc_{\rm clk}=1$，$J_\eta=\int\eta(\xi-c_{\rm clk})F(\xi)d\xi$ 自主守恒；$c_{\rm clk}$ 不是旧平均 $c$，也不是全局时钟。

报告还声称：左右半线完整矩阵在 $(-2d,2d)\cup i\mathbb R$ 的振荡轮廓有真空线性反演；$p,s$ 均为奇函数时，全线相对散射矩阵为 $I$，半线数据仍可能保留信息。非线性逆谱、零点连接和相位完备性未完成。解流拉回辛形式的方案仍依赖真实物理初值流、合法相空间及受限形式的弱非退化性。

## 5. 2026-10-11 候选报告的接续状态

**候选定理，未完整独立复核。** [全文](sources/2026-10-11_mixed_bvp_candidate.md) 为本次收到的外部研究草稿，保留其完整推导和内部声称；提及的符号复核脚本未取得，未运行。

- 报告声称严格单调式 $\frac d{dt}\int ps=-\frac A2\int(p^2+4d^2s^2+b^2)$ 在其正则、衰减与零点商条件下成立；不是守恒量。对 $A\ne0$，它阻碍非平凡时间周期 / 紧环面运动，不排除非紧 Liouville 结构。
- 旧解析时间迹构造降级为局部解析时空解族；系数权重比更正见全文式（6）。未建立自然初始场拓扑上的双向流。
- 报告声称 $A>0,d>0,T>0$、$k\ge6$ 时，以 $a_+=p+2ds$、$a_-=p-2ds$ 的混合输入 $a_+(-T)=g_+$、$a_-(T)=g_-$ 在明确加权 Sobolev 空间构造全线唯一小解并实解析依赖；对任意预先指定有限矩阶 $\ell\ge1$，提高到 $k\ge2\ell+6$ 后可传播矩。正文以 $m$ 表示矩阶，与本专题 $m=\Pi w$ 区分。$A<0$ 仅声称反转时间、交换组件并反向分配端点后的同类结果。
- 报告的两个组件积分 $\int p$、$\int s$ 守恒；全线小解仍待审定，不能标为已认证。须逐项审查负移位线性逆的统一界、端点时间迹、非线性 Lipschitz 与矩归纳。
- 中心映射线性化声称单射但逆无界；非线性中心单射仍未证明。高频增长仅阻碍自然加权 Sobolev 真空 $C^1$ 流覆盖整族，不排除更强尺度或较小非真空域。
- 谱泛函声称可沿混合解定义，旧括号表达式可收敛并延续对合计算；$J\mathcal dI_\rho$ 对中心值集合的切向性未证，故未建立其完整 Poisson 代数。旧 $\alpha$ 非闭合缺陷声称仍出现在真实小解族中。

下一步先审定候选定理依赖，再推进中心初值恢复、替代结构和完整非线性谱坐标，或换路线扩大适用域。持续建立一般物理场可积性的目标见 [GOAL](GOAL.md)；以上任何单一障碍均不是一般不可积性定理，也不作为任务终点。
