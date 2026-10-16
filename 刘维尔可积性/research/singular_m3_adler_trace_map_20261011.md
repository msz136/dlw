# M=3 三阶层的 Adler／GD 算式校准

2026-10-11。此稿仅核验受限 cotangent 的形式向量算式；高阶实际共同时间窗尚未由它证明。阶段合法性沿用 [零通量阶段审计](singular_branch_review_20261011.md) 的共 $U$ 商、配对 Dirac 及实际归一化分析。

明确采用

\[
H_{\rm std}(P,X)=(PX)_+P-P(XP)_+.
\]

这个定义下原因子括号的物理系数是 $+1/8$。反向定义 $P(XP)_+-(PX)_+P$ 才配 $-1/8$。统一校准是原 Hamiltonian
$\widetilde H=-8\operatorname{Tr}D^2(P-I)$：
$H_{\rm std}(P,-8D^2)/8$ 在相应主层给真实 $-[D^2,P]$。

在已合法的 $M=3$ 三阶最小图，

\[
P=I+aQ^{-1},\qquad a=a_3\ne0,\qquad
Q=D^3+uD+v.
\]

冻结当前轨道值 $a$，若 $dF=\operatorname{Tr}Y\,dQ$，其受限代表是

\[
X=-QYQ/a.
\]

记 $C=(QYQ)_+$、$A=(YQ)_+$、$B=(QY)_+$。直接展开

\[
H_{\rm std}(P,X)=Q^{-1}[C,Q]Q^{-1}
+(B-A)+a(Q^{-1}B-AQ^{-1}).
\]

由 $P_t=-aQ^{-1}Q_tQ^{-1}$，未缩放的向量为

\[
Q_t=\frac{[Q,C]+QAQ-QBQ}{a}+QA-BQ.
\tag{1}
\]

故 $F_m=m^{-1}\operatorname{Tr}Q^{m/3}$ 的
$Y=Q^{m/3-1}/3$ 与 $Q$ commute，给物理 $+1/8$ 缩放后的冻结代表

\[
Q_t^{*}=
\frac{[Q,(Q^{m/3+1})_+]}{24a}
+\frac{[Q,(Q^{m/3})_+]}{24}.
\tag{2}
\]

这是两个负号 Lax 约定 GD 时间的组合：
$[Q,B]=-[B,Q]$。$m$ 与 $m+3$ 的最高阶生成算子不同，不能只把式 (2) 称作一个普通 $m$ 次 GD 时间。

阶段理由不能省略：此 trace 代表与 $P$ commute，Adler 向量为
$-[(PX)_-,P-I]/8$，在 $P-I$ 阶数 $-3$ 时至多 $-5$，所以保持 $a_1,\ldots,a_4$，从而对当前 $c,q,\chi$ 配对层和去二阶项切向。实际外延与该受限代表相差已处理的 conormal；只有在该完整阶段商内，Dirac 修正可按此前论证消去。

实际 $a$ 不是 Casimir。允许初态改变 $a$ 时

\[
dF_m=dF_m^*+\frac{mF_m}{3a}\,da,\qquad
a=-H_0/(8L).
\]

因此实际归一化还加

\[
-\frac{mF_m}{24La}\,X_{H_0}^{D}.
\tag{3}
\]

此项是原实际 $t_2$ 向量，不是可以任意删去的平移。此前阶段 trace 对合已证明 $F_m,a$ 沿这些向量保持，故相关系数沿每条共同形式轨道恒定；这仍不替代高阶实际局部流存在性。

式 (1)–(3) 可用于研究 M=3 的实际辅助共同流。当前已成立的全 $M$ 实际结果仍是 [二、三阶 cKP mixed 原时间轨道](singular_ckp_actual_mixed_flow_20261011.md)；无限多个高阶生成算子的共同实际时间窗、谱独立性和 Liouville 完备性尚未完成。
