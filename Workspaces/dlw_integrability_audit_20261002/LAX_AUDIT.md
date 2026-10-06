# DLW Lax 工作审计：全系统、解族及退化支

日期：2026-10-02。直接检查公式和脚本；未把旧 `VERDICT.md` 的结论当作前提。
原始源码、根报告、进度索引未改。只运行轻量精确检查，未跑 PDE 实验或 Lean 编译。

## 1. 当前能确认的层次

| 对象 | 已确认 | 不能据此宣布 |
|---|---|---|
| 原交错双线性对，完整 (x,t,j) | 两个热算子的 Darboux 交织恒等式；可转写到 SD/SDR 场 | 已完成一般初值的 IST、周期谱理论或无穷独立守恒量 |
| SD 两场方程 | 局部开链、模积分自由度可重构双线性对及热势；相容结构不限于 Gram 族 | 全局周期/指定衰减边界下无条件双射 |
| SDR (Q,R,M) 方程 | 在 (Q\ne0)、规范相容时，同一 Darboux 结构可直接转写 | 已给出完整矩阵谱表示、一般谱变换或边界完备性 |
| 任意 (N) Gram 解族 | 精确谱波函数；与背景色散匹配；非恒定谱渐近因子 | 所有初值均由此有限维解族和谱数据重构 |
| 旧秩一形变标量递推 | 恒等式成立，但对任意系数函数都成立 | 其相容性等价于 DLW，或能否定其他 Lax 表示 |
| (x) 无关 SDR 支 | 单点幅度互逆演化，物理 (u=0,v) 静止 | 完整 DLW 半离散系统的 Lax 证明 |

审计范围内未找到一个最新的、对一般 (x) 依赖 SD/SDR 已证明充分必要且含不可消去谱参数的有限维矩阵 Lax 对。
存在的是下面的有内容的算子/Darboux结构，以及解族上的谱构造。

## 2. 完整 (x,t,j) 的 Darboux 算子

设 (d=h/2)、(W=v-\delta_0u)，以及

\[
H=\frac{u^2}{2}+2au+h^2\left(\frac{W^2}{32}-\frac W4\right),\quad
w^-=a+\frac u2+\frac h8(W-4),\quad
w^+=a+\frac u2-\frac h8(W-4).
\]

时间算子与格点算子为

\[
\mathcal H_j=\partial_t+\partial_x^2+V_j,\qquad
T_j^\pm=\partial_x-w_j^\pm,
\]

\[
\mathcal H_j\psi_j=0,\qquad T_j^+\psi_{j+1}=T_j^-\psi_j.
\]

对任意波函数都有精确算子恒等式

\[
(\partial_t+\partial_x^2+V+2w_x)(\partial_x-w)
-(\partial_x-w)(\partial_t+\partial_x^2+V)
=-(w_t+w_{xx}+2ww_x+V_x).
\]

在双线性势中 (V_j=2(\log G_j)_{xx})，两个交织关系共用

\[
V_j^F=2(\log F_j)_{xx}=V_j+2w^-_{j,x}
=V_{j+1}+2w^+_{j,x}.
\]

所以完整的两个 Darboux 恒等式确实由原双线性残差的 (x) 导数控制。
它们的作用不同于对一个选定波函数拟合递推。

### 一般物理场的约束与局部充分必要性

令

\[
E^-=w^-_t+w^-_{xx}+2w^-w^-_x+V_x,\quad
E^+=w^+_t+w^+_{xx}+2w^+w^+_x+V_{j+1,x},
\]

并取 (V_{j+1}-V_j=(h/2)W_{j,x})。独立精确化简得到

\[
E^--E^+=\frac h4\{W_t-W_{xx}+[(u+2a)W-4u]_x\},
\]

\[
E^-+E^+=u_t+H_x+u_{xx}+\frac h2W_{xx}+2V_x.
\]

于是两个交织恒等式等价于上述两项为零。对第二项作格点后差分，利用势差约束，恰得

\[
\delta_-(u_t+H_x)+(\delta_-u+M_-W)_{xx}=0,
\]

即 `NONLINEAR_CLOSURE.md` 的 N1；第一项为该文的等价第二式。
反过来，N1 与第二式保证两条规定 (V_x) 的关系相容，故在局部开链可选择 (V) 并得到两个交织关系。
相应 (x) 积分及仅依赖 (t) 的规范自由度仍需固定；周期/衰减边界不是自动结论。

### 裸格点算子在退化支可能漏约束

将两条交织关系缩写为 (L_j=(T_j^+)^{-1}T_j^-) 的零曲率，不能直接把充分必要性外推到所有分支。
当 (W=4) 时 (T^+=T^-)，形式上 (L_j=1)。

一个精确反例是 (h=1,a=0,u_j=jx,W_j=4,V_j=0)。裸线性对成为相同的热算子和 (L_j=1)，零曲率恒零；
但原物理方程残差为

\[
N1=(2j-1)x,\qquad N2=2jx.
\]

因此须保留两个 Darboux 交织约束，或另证裸线性对在指定非退化状态类上的逆向含义。
该反例只针对“约化成 (L=1) 后，裸零曲率自动等价完整 SD”的过度推论；
它不否定非退化 (W-4) 分支上的谱表示，也不否定整体可积性。

## 3. SDR 转写及 (x) 无关支

当前根报告式 (21) 的 SDR 为

\[
Q_t=-Q_{xx}-2aQ_x-\mathcal KQ,\quad
R_t=R_{xx}-2aR_x+\mathcal KR,
\]

\[
\mathcal K=(M_j+M_{j+1})_x+\frac{h^2}{4}[(QR)^2-1],\quad
M_{j+1}-M_j=h(1-QR),
\]

\[
u=2Q_x/Q,\quad W=4(1-QR),\quad V_j=2M_{j,x}.
\]

因此完整 Darboux 格点式可写成

\[
\left[\partial_x-a-\frac{Q_x}{Q}-\frac h2QR\right]\psi_{j+1}
=\left[\partial_x-a-\frac{Q_x}{Q}+\frac h2QR\right]\psi_j.
\]

这仍是含 (x) 微分的全系统结构。若令所有 (Q,R,M) 与 (x) 无关，则

\[
Q_t=-\frac{h^2}{4}[(QR)^2-1]Q,\quad
R_t=\frac{h^2}{4}[(QR)^2-1]R,\quad (QR)_t=0.
\]

物理场为 (u=0,v_j=4(1-Q_jR_j))，随 (t) 静止。
任何只描述这一支的矩阵对，均不能代替完整 (x,t,j) 系统的证明。

## 4. 谱参数证据的准确范围

`S_INTEGRABILITY_STATUS.md` 构造

\[
\psi_j(z)=e^{zx-z^2t}\left(\frac{z-a+d}{z-a-d}\right)^j
\frac{\tau_1(j;z)}{\tau_0(j)}.
\]

这里仅将 Gram 系数参数改为 (z)，格点乘子中的 (a,h) 不变。
任意 (N) 下满足上一节的热方程与格点方程。
正实无奇点孤子支的归一化谱渐近因子为

\[
\mathcal T(z)=\prod_{i=1}^N\frac{z-p_i}{z+q_i},
\]

与 (t,j,h) 无关，且 (N=1) 已有 (\mathcal T'(z)=(p+q)/(z+q)^2\ne0)。
这证明了解族上的非平凡谱边界数据；比“先取无谱矩阵再证明乘积无谱”更强。
但一般场的 Jost 存在唯一性、谱数据完备性、逆问题及非局部热势规范尚未建立。
普通指数规范可以从算子系数消去 (z)，不能自行消去规定边界归一化中的 (z)；
当前也未证明满足所有边界要求的不可消去矩阵谱参数。

## 5. 为什么不能使用旧矩阵的全系统定论

1. `laxverify.py` 的 (L_n=(z+Q_{n+1})/(z+Q_n))、(M_n=Q_{n,t}/(z+Q_n)) 对任意 (Q_n(x,t)) 均有
   (L_{n,t}+L_nM_n-M_{n+1}L_n=0)。它没有生成原 DLW 方程。
2. 固定 (z) 的标量乘积不等于矩阵 `[[1,Qnext],[1,Q]]` 的 Möbius 映射复合；后者把下一步谱输入改成前一步输出。
   已核验 (z=5,Q_0=1,Q_1=2,Q_2=3)：前者 (4/3)，后者 (25/19)。
3. `final_test.py` 由一条试探波函数的四个邻值拟合二阶递推，再乘三个开链矩阵；未验证周期势或端点相容。
   因此其迹随时空变化既不能证明全系统不可积，也不能从这个迹构造周期守恒量。
4. `Paper/gsg_project/lax/lean/DLWLaxDegenerate.lean:247` 的 `zf_all` 显式假设 `∀ i, IsZFree (Q i)`，
   而 `Lmat` 定义本来就没有 (z)。它证明指定矩阵乘积无谱，不能排除别的表示。
5. `Paper/reports/dlw_laxpair_report.md` 是连续文献搜集，不是有限 (h) 的 Lax 推导；其中不同归一化尚需对应。
   该旧报告第20行把 (u_{yt}+v_{xx}+\frac12(u^2)_{xy}=0) 的 (x) 积分写成
   (u_t+v_x+\frac12(u^2)_y=0)，不成立：首项应是 (\partial_x^{-1}u_{yt})，并带积分自由度。
   最新 `verify_nonlinear_closure.py` 已验证 GLDW–Sheng/Yu 的明确 Miura 归一化对应，故也不能继续沿用旧报告“对应尚未验证”的表述。

## 6. 本次实际运行与证据路径

- `Workspaces/dlw_semidiscrete/verify_integrability_structure.py`：45 组辅助 Toda 精确系数恒等式；任意波函数 Darboux 算子恒等式；物理场热势重构；旧矩阵混淆反例；全部通过。
- `Workspaces/dlw_semidiscrete/verify_s_spectral.py`：(N=1,\dots,5)，共180组参数/步长/格点/谱值；热方程及格点谱关系逐指数系数精确为零；符号秩一更新和任意 (N) 收缩抵消通过。
- `Workspaces/dlw_semidiscrete/verify_nonlinear_closure.py`：一般消元、二阶物理极限、正确连续 Hirota 方程及 Miura 归一化全部符号通过。
- 本目录 `lax_audit_checks.py`：独立证明 (E^-\pm E^+) 组合、旧标量零曲率的任意系数恒等式及 (W=4) 反例；全部通过。
  实际输出的结构记录为 `lax_audit_checks.json`。
- 四项实际运行标准输出保存在 `LAX_CHECK_RUNS.md`；检查输入和相关源文件的 SHA-256 保存在 `lax_source_hashes.json`。

可引用的当前结论：完整半离散 DLW 已有局部 Darboux 相容结构，任意 (N) Gram 解族上有精确谱波函数与非平凡谱渐近数据。
若按2HS的“完整含谱参数Lax对支持半离散可积性”流程衡量，DLW仍需完成一般场、指定边界及退化分支下的完整谱表示与相容逆向证明；
一般 IST 未证明，也不存在由现有旧矩阵工作支持的不可积定论。
