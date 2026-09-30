# 从指定双线性对到二阶一致的闭合非线性 DLW 格点系统

日期：2026-09-19。验证：`verify_nonlinear_closure.py`。

> **后续验证已完成**：见 `GRAM_INTEGRABILITY_REASSESSMENT.md`。纯 x,t,j 的 Gram 构造
> 已有任意 N 的双线性证明，因此下面的条件性非线性化现在有确切的任意 N 行列式解族。
> 下文“尚未恢复旧 Gram 声称”记录的是本报告写作时的边界；额外 y 相位混合构造仍须区分。

## 0. 结论与适用范围

**可以完成非线性化。** 将用户指定的两条方程作为起点：

\[
 B_{a-h/2}F_j\cdot G_j=0,\qquad
 B_{a+h/2}F_j\cdot G_{j+1}=0,\qquad
 B_s=D_x^2+D_t+2sD_x. \tag{B}
\]

下面给出有限非零步长下的精确代数消元，以及二阶一致的物理变量与闭合系统。
它的连续极限是原文的 **\(\lambda=-2\)** DLW；这组固定系数的起点没有独立的任意 \(\lambda\)。

这是一项关于方程 (B) 的条件定理，不依赖旧 Gram τ 引擎，也不需要参数移位结构恒等式。
**没有据此恢复旧报告对特定 Gram τ、N 孤子解或可积性的声称。**
此前“不能非线性化”的表述过强：旧 τ 实现是否满足 (B)，与 (B) 本身能否非线性化，是不同问题。

工作在 τ 非零、可选择光滑局部对数的区域。实变量可取正 τ；固定符号时用对数绝对值。
以下一致性假设相应光滑插值及足够阶的导数一致有界；不声称已证明离散解的收敛或稳定性。

## 1. 推荐物理变量：在 F 格点上对称配对

采用半整数交错几何：

\[
 y(F_j)=(j+\tfrac12)h,\qquad y(G_j)=jh.
\]

记中心差分、后向差分、后向平均和二阶差分为

\[
 \delta_0 z_j=\frac{z_{j+1}-z_{j-1}}{2h},\quad
 \delta_-z_j=\frac{z_j-z_{j-1}}h,\quad
 M_-z_j=\frac{z_j+z_{j-1}}2,\quad
 \Delta_h z_j=\frac{z_{j+1}-2z_j+z_{j-1}}{h^2}.
\]

定义两个物理场，均标记在 F 格点：

\[
 \boxed{u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}}},\qquad
 \boxed{v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j}. \tag{1}
\]

第二个定义经代入第一个定义，确实同时含 F 与 G 的格点差分。
它不是把单独的 \(G_{j+1}/G_j\) 差商误认成 \(2(\log fg)_{xy}\)。

与用户原始的 \(\widehat u_j=2\partial_x\log(F_j/G_j)\) 的精确关系是

\[
 u_j=\widehat u_j-\partial_x\log(G_{j+1}/G_j).
\]

这项对称化使 u 定义在同一个物理中点，消除了混合位置引入的一阶偏移。

## 2. 最终闭合系统

为排版简洁，定义两个**显式表达式**（不是新的未知场或独立方程）：

\[
 W_j[u,v]=v_j-\delta_0u_j,\qquad
 H_j[u,v]=\frac12u_j^2+2au_j
       +h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right). \tag{2}
\]

则所求非线性微分—差分系统为

\[
 \boxed{\delta_-\bigl(u_{j,t}+\partial_xH_j\bigr)
 +\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_h\delta_-u_j\right)=0,} \tag{N1}
\]

\[
 \boxed{v_{j,t}
 +\partial_x\left[\delta_0H_j+(u_j+2a)(v_j-\delta_0u_j)-4u_j\right]
 +\partial_x^2\left[\delta_0u_j+
             \frac{h^2}{4}\Delta_h(v_j-\delta_0u_j)\right]=0.} \tag{N2}
\]

式 (2) 直接代入即可得到完全展开的两场方程。没有 τ、对数势、积分算子、逆差分算子，
也没有需要额外求解的辅助场。空间格点模板最远到 \(j\pm2\)，不是严格的仅 \(j,j+1\) 两点格式。
N1 自然位于两个 F 格点的中点；N2 位于 F 格点。有限 h 时两式均为精确关系。

## 3. 消元推导

仅在证明中写 \(\alpha_j=\log F_j,\ \beta_j=\log G_j\)。归一化的双线性残差为

\[
 A_j=(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
 +(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x,
\]
\[
 C_j=(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
 +(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x.
\]

它们分别等于 (B) 左侧除以 \(F_jG_j\)、\(F_jG_{j+1}\)。因此 (B) 等价于 \(A_j=C_j=0\)。

证明用的中间量为

\[
 r_j=\frac2h(\beta_{j+1}-\beta_j)_x,\quad
 Q_j=(2\alpha_j+\beta_j+\beta_{j+1})_x,
 \quad u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x.
\]

精确的和、差恒等式（对任意非零 τ 成立，不需要先假定残差为零）：

\[
 u_{j,t}+\partial_x\left(\frac{u_j^2}{2}+2au_j
                  +\frac{h^2r_j^2}{8}-\frac{h^2r_j}{2}\right)+Q_{j,xx}
       =\partial_x(A_j+C_j), \tag{3}
\]
\[
 r_{j,t}+\partial_x[(u_j+2a)r_j-2u_j]-r_{j,xx}
       =\frac2h\partial_x(A_j-C_j). \tag{4}
\]

注意两式中所有显式一阶 h 项已经抵消。这是采用对称变量的原因。

消去 Q 的代数关系为

\[
 \delta_-Q_j=\delta_-u_j+r_j+r_{j-1}. \tag{5}
\]

由物理变量定义 \(v_j=2r_j+\delta_0u_j\)，故 \(2r_j=W_j[u,v]\)，无需逆算子。
对 (3) 作 \(\delta_-\)，利用

\[
 M_-\delta_0=(1+\tfrac{h^2}{4}\Delta_h)\delta_-
\]

即可得到 N1。

把 (4) 乘以 2 后，得到等价的第二式

\[
 (v_j-\delta_0u_j)_t+
 \partial_x[(u_j+2a)(v_j-\delta_0u_j)-4u_j]
 -(v_j-\delta_0u_j)_{xx}=0. \tag{6}
\]

令 \(M_+z_j=(z_j+z_{j+1})/2\)。将 \(M_+\)(N1) 加到 (6)，利用

\[
 M_+\delta_-=\delta_0,\qquad M_+M_-=1+\tfrac{h^2}{4}\Delta_h,
\]

就得到 N2。这里只是可逆的方程组合：保留 N1，第二式加减 \(M_+\)(N1)。
没有把 N1 单独替换成平均后的式子，因此未在这一步丢弃交错格点模态。

## 4. 二阶物理极限和 DLW 极限

在 F 格点位置 y，设 \(F_j=f(y)\)、\(G_j=g(y-h/2)\)、\(G_{j+1}=g(y+h/2)\)，
并记 \(\alpha=\log f,\beta=\log g\)。Taylor 展开给出

\[
 u_j=2(\alpha-\beta)_x-\frac{h^2}{4}\beta_{xyy}+O(h^4),
\]
\[
 v_j=2(\alpha+\beta)_{xy}
       +h^2\left(\frac13\alpha_{xyyy}-\frac5{12}\beta_{xyyy}\right)+O(h^4).
\]

因此两个定义都以二阶精度趋于论文的物理变量。

现在把物理场 u、v 作为任意光滑插值。N1 应在其自然位置 \(y-h/2\) 比较：
\(\delta_-\) 是该位置的中心导数，\(M_-\) 是该位置的中心平均。
又因 \(H=u^2/2+2au+O(h^2)\)，N1 的局部截断误差为 \(O(h^2)\)，主项为

\[
 \boxed{u_{yt}+v_{xx}+(u u_y)_x+2au_{xy}=0.} \tag{DLW1}
\]

N2 在 F 格点处展开，\(\delta_0=\partial_y+O(h^2)\)，
\(\Delta_h=\partial_y^2+O(h^2)\)。其通量主项为

\[
 \partial_y(u^2/2+2au)+(u+2a)(v-u_y)-4u=(u+2a)v-4u.
\]

因此 N2 以 \(O(h^2)\) 截断误差恢复

\[
 \boxed{v_t+(uv)_x+u_{xxy}+2av_x-4u_x=0.} \tag{DLW2}
\]

这正是 Physica D 原文 (1)–(2) 在 \(\lambda=-2\) 时的系统。
\((uu_y)_x=u u_{xy}+u_xu_y\)，故第一式的展开形式也完全一致。
二阶一致性不等于已经证明数值稳定性或解的收敛。

## 5. 微分消元的反向重构与边界条件

任何满足 (B) 的非零 τ 都通过 (1) 给出 N1–N2 的解。
反向在局部开链/无限格点上也可重构，需处理被 x 微分、格点差分消掉的积分自由度：

1. 从已知 u、v 计算 \(r=(v-\delta_0u)/2\)。递推选取
   \(\beta_{j+1,x}-\beta_{j,x}=hr_j/2\)，再取
   \(\alpha_{j,x}=(u_j+\beta_{j,x}+\beta_{j+1,x})/2\)。
2. N1 保证 (3) 左侧 S_j 与 j 无关。共同改变
   \(\alpha_j\mapsto\alpha_j+s(x,t)\)、\(\beta_j\mapsto\beta_j+s(x,t)\)，
   不改变 u、v，却使 \(S_j\mapsto S_j+4s_{xxx}\)。局部取 \(4s_{xxx}=-S_j\)。
3. 由 (6) 和 S=0 得 \(A_{j,x}=C_{j,x}=0\)。剩下 A_j、C_j 仅依赖 t。
   对 \(\alpha_j,\beta_j\) 加仅依赖 t 的函数 f_j、g_j，递推选择
   \(g'_{j+1}-g'_j=C_j-A_j\)、\(f'_j=g'_j-A_j\)，便有 A_j=C_j=0。

所以可称为**局部、模积分自由度的等价非线性化**。
对于周期格点、周期 x 或指定衰减边界，递推和三次积分可能受到整体相容条件限制；
这里不声称每个闭合系统的周期解都自动对应同周期 τ。
与连续 DLW 相同，含 \(u_{yt}\) 的方程也需要相应边界/平均模态条件才能讨论唯一演化。

## 6. 若坚持原始 u 定义：较短的一阶格式

另一组完全精确、只用一条格边的变量是

\[
 \widehat u_j=2(\log F_j/G_j)_x,\quad
 \widehat v_{j+1/2}=\frac2h\partial_x\log\frac{F_{j+1}G_{j+1}}{F_jG_j}.
\]

令 \(D_+z_j=(z_{j+1}-z_j)/h\)、\(\bar z_j=(z_{j+1}+z_j)/2\)，并在下式省略
\(\widehat v\) 的边下标。直接消元得到

\[
 D_+\widehat u_t+\partial_x[(\bar{\widehat u}+2a-h)D_+\widehat u]
       +\widehat v_{xx}=0,
\]
\[
 \widehat v_t+\partial_x\left[(\bar{\widehat u}+2a+h)\widehat v
 -\frac h4\bigl(\widehat v^2-(D_+\widehat u)^2\bigr)
 -4\bar{\widehat u}\right]+(D_+\widehat u)_{xx}=0.
\]

这说明原始变量同样可以闭合；但把它们直接作为同一光滑物理场的采样时，显式 O(h) 项不会消失。
若目标包括对称交错物理解释与二阶一致性，推荐第 1–2 节的定义和系统。

## 7. 必须纠正的旧审计结论

原文 (6) 是

\[
 [D_yB_a-4D_x]f\cdot g=0,
\]

而 `audit_gauge.py` 的文件说明和实现把它当成了
\(B_af\cdot g_y-4D_xf\cdot g=0\)。二者不同。

正确恒等式为

\[
 \partial_y(B_af\cdot g)=B_af_y\cdot g+B_af\cdot g_y,
 \qquad D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y.
\]

在 \(B_af\cdot g=0\) 下，原文 (6) 等价于

\[
 B_af\cdot g_y+2D_xf\cdot g=0.
\]

这恰好是用户指定双线性对的一阶差商极限。
新脚本对一般符号 p、q、a 的连续 N=1 Gram τ 检查了正确 (6)、(7)，均精确为零。
因此旧“论文 (6) 与 τ 不相容、相位常数救不活”的结论没有原来的证据支持，不应继续引用。
这项纠正不等于已经验证有限 h 的旧 τ 构造；其参数相位移位问题仍须按具体定义另查。

## 8. 验证记录

运行：`python Workspaces/dlw_semidiscrete/verify_nonlinear_closure.py`（从工作区根目录）。

- 任意符号函数 \(\alpha_j(x,t),\beta_j(x,t)\) 下验证 (3)、(4)、(5) 及 N1、N2 残差恒等式。
- 保留任意光滑函数的 y Taylor jets，精确验证连续两式及一阶截断项的抵消。
- 验证两个物理变量定义的主项与一阶系数。
- 三个不同有理点、五个 h 值，使用有理数/Fraction 扫描二阶归一化截断误差。
- 用指数系数代数验证正确的连续 N=1 双线性对；不把单点数值小量作为零。

所有符号判零均得到字面 0。未运行 Lean，未验证新 N 孤子解，未进行稳定性实验。
