# 刘维尔可积性

归档日期：2026-10-11。**尚无一般物理场上的完整无限维 Liouville 定理，也没有一般不可积性证明。** 本专题汇总现有结果、前提与缺口；本次仅整理文档，未开展新证明、数值研究或重跑历史核验。

## 原方程与平均兼容

取 $h>0$、$D=\partial_x$，$j$ 为 $M$ 周期格点：

$$
\delta_-[U_t+D(U^2/2+h^2w^2/32)]+D^2(\delta_-U+M_-w)=0,
\qquad w_t+D(Uw)-D^2w=0,
$$

$$
\delta_-f_j=(f_j-f_{j-1})/h,\qquad M_-f_j=(f_j+f_{j-1})/2,
\qquad \Pi f=M^{-1}\sum_{j=0}^{M-1}f_j.
$$

令 $m=\Pi w$、$q=\Pi(Uw)$。方程强制 $m_{xx}=0$、$m_t+q_x=0$，故在实全线上

$$
m=A(t)x+B(t),\qquad
q=-A'(t)x^2/2-B'(t)x+\Gamma(t).
$$

$\Gamma$ 是平均通量的空间积分自由度。周期 $x$ 时另有 $A=0$、$B'=0$、$q=\Gamma(t)$；将 $\Gamma$ 再设为时间常数属于附加闭合。原稿的物理变量为 $U=u+2a$、$w=v-\delta_0u-4$；旧周期报告的 $c=\Pi w$ 对应这里的 $m$，其 `gamma` 对应平均通量。不同稿件的 $c$ 不混用，闭合来源须明示。

## 路线状态与积分数

| 路线 | 适用域及额外前提 | 守恒量数量与结构 | 当前状态 / 缺口 |
|---|---|---|---|
| Fourier 对数轮廓精确解族 | 偶数 $M$、周期 $x$；$C_p,C_s>0$、$B\ne0$；每个有限 $N$ 的小邻域；$m=0$、$ps$ 空间常数 | $2N$ 维辛族，$N$ 个独立对合积分；为 Moser 坐标作用量 | 既有报告声称，待独立复核；原证明未定位。行波族不稠密于整个物理场，任意有限 $N$ 不等于 $N=\infty$ |
| 空间仿射族（暂置） | $R_j^\pm=U_j\pm hw_j/4=a_j^\pm x+b_j^\pm$；额外平均闭合 $\kappa x+\delta$、$\kappa>0$、$\lvert a\rvert<\sqrt\kappa$ | $4M$ 维，$2M$ 个独立对合积分，非紧叶；约化族上构造的 Poisson 结构 | 既有报告声称，待独立复核；原证明未定位。不宣称全场结构的自然继承 |
| 一般周期场的旧守恒层级 | 固定有限 $M\ge2$、周期 $x$；$m=c\ne0$、$q=\gamma$ 固定闭合，固定组件空间平均 | $\mathcal K,\mathcal P,\mathcal C_3,\mathcal C_5,\ldots$；草稿声称任意有限前缀独立、对合 | 原稿可查；混合时间解族区别于任意初值流。谱完备性、作用角与共同合法相空间未完成 |
| 一般函数涨落的当前探索分支 | $M=2$、实全线；$d=h/8$、固定 $A\ne0$、$m=Ax$；不施加指数行波关系 | 谱平滑泛函 $I_\rho$ 是一族；既有报告声称可取任意有限多个独立对合成员，尚无完备积分数定理 | 旧结构的物理 Hamilton 性有非闭合障碍；局部谱时钟、半线真空线性反演不足以给出全局非线性谱坐标 |
| 2026-10-11 混合边值候选定理 | 上一分支中 $A>0$、有限 $T$；$a_+(-T)=g_+$、$a_-(T)=g_-$，明确加权 Sobolev 小数据 | 报告声称两个组件积分守恒、谱泛函可沿真实轨道定义；没有新增完备性定理 | **候选定理，未完整独立复核**。非线性中心单射、正则初值重启、Hamilton 辅助流切向性未证 |

各路线的公式及证据限制见 [progress.md](progress.md)。当前 $M=2,m=Ax$ 只是探索分支；目标仍是一般物理场，可换路线并逐步扩大条件域。

## 当前分支的最必要公式

$$
U_0=b+p,\quad U_1=b-p,\quad w_0=Ax+s,\quad w_1=Ax-s,
\quad \Gamma(t)=p(0,t)s(0,t),\quad b=\frac{\Gamma-ps}{Ax},
$$

$$
b(0,t)=-(ps)_x(0,t)/A,\qquad
p_t=-D(bp+4d^2ms)-p_{xx},\quad s_t=-D(bs+mp)+s_{xx}.
$$

报告给出的严格单调式为

$$
\frac d{dt}\int_{\mathbb R}ps
=-\frac A2\int_{\mathbb R}(p^2+4d^2s^2+b^2).
$$

其衰减、正则及零点商条件须审定；这是单调量，不能计为守恒积分。它阻碍非平凡时间周期 / 紧环面物理运动，不排除非紧 Liouville 结构。

## 源文件索引

- [原方程与周期平均约束](../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md)：核对 $U,u,w,c$ 与闭合来源。
- [一般周期场的守恒族与计数](../Workspaces/dlw_general_field_20261006/CONSERVATION_FAMILY_VERDICT.md)、[主方程与解析边界](../Workspaces/dlw_general_field_20261006/RESEARCH_NOTES.md)、[周期混合时间存在性草稿](../Workspaces/dlw_general_field_20261006/MIXED_TIME_EXISTENCE.md)：均保留原稿范围，不移用于 $m=Ax$。
- [周期场完备性与初值流障碍](../Workspaces/dlw_field_liouville_20261006/THEORY.md)：列出有限子族独立与无限维完备性的区别。
- [历史综合报告](../dlw_liouville_integrability.md)、[有限孤子参数族材料](../Workspaces/dlw_liouville_20261005/README.md)：历史路线另有前提，不等同于本专题的 Fourier 对数族。
- [2026-10-11 混合边值候选报告全文](sources/2026-10-11_mixed_bvp_candidate.md)：外部研究草稿，尚未完整独立复核；未取得其提及的复核脚本。

## 下一步

1. 先审查候选报告的负移位线性逆统一界、端点时间迹、非线性 Lipschitz 估计与矩归纳；结论随审查结果修订。
2. 明确物理场自身定义的函数空间、平均闭合与可积性定义，处理中心初值恢复和正则重启，再在同一条件域核验 Hamilton / Poisson 结构。
3. 完成非线性逆谱、零点连接、相位恢复与积分完备性；遇到障碍时明确其相空间、结构和正则类别的适用范围，调整方法继续推进一般场可积性目标。

继续工作的简短提示见 [GOAL.md](GOAL.md)。候选结构失败或特定拓扑下初值不适定，均不能直接升级为一般不可积性。
