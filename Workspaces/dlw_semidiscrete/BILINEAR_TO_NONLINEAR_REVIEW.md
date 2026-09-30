# 双线性到非线性：步骤、可逆性与其他变量选择

日期：2026-09-24。本文只讨论现行交错双线性系统；最后一节另列真正改变离散方程的方案。现行公式和完整反向重构见 [NONLINEAR_CLOSURE.md](NONLINEAR_CLOSURE.md)，有限格距参数族见 [ALTERNATIVE_DISCRETIZATIONS.md](ALTERNATIVE_DISCRETIZATIONS.md)。

## 0. Miura 论文与本系统的准确联系

Cerveró–Estévez 的 [Miura 论文](../../Paper/refs/miura9803007.pdf)（arXiv:solv-int/9803007）式 (2.1) 使用 \(U,\eta\)：

\[
U_{ty}+(\eta_{xy}+2UU_y)_x=0,\qquad
\eta_{ty}+(U_{xy}+2U\eta_y)_x=0. \tag{M0}
\]

其与我们连续 \(\lambda=-2\) DLW **恰好等价**。取

\[
U=a+\frac{u}{2},\qquad \eta_y=\frac{v-4}{2}; \tag{M1}
\]

将 (M1) 代入 (M0) 并把每式乘 2，逐项得到

\[
u_{yt}+v_{xx}+[(u+2a)u_y]_x=0,
\qquad
v_t+u_{xxy}+[(u+2a)v-4u]_x=0. \tag{M2}
\]

这正是我们的连续 DLW 方程。常数 \(4\) 在第一式被 \(x\) 导数消去，在第二式产生必需的 \(-4u_x\)。所以该论文对**连续系统**确实相关；但 (M0) 本身不指定我们采用哪一种有限 \(h\) 双线性对。

还有更直接的 tau 对应。设 \(f=e^\alpha,g=e^\beta\)、\(q=\alpha-\beta\)、\(S=B_af\cdot g/(fg)\)，并选择一个势规范

\[
U=a+q_x,\quad \eta=(\alpha+\beta)_x-2y-a^2x,
\quad m=\frac{U+\eta}{2},\quad \widehat m=\frac{\eta-U}{2}. \tag{M3}
\]

于是 \(u=2q_x\)、\(v=2(\alpha+\beta)_{xy}\)，且

\[
m=\alpha_x+\frac a2-y-\frac{a^2x}{2},\qquad
\widehat m=\beta_x-\frac a2-y-\frac{a^2x}{2}. \tag{M4}
\]

由下文式 (1) **逐项精确得到**

\[
2m_x-[U_x-U^2-q_t]=S,
\qquad
2\widehat m_x-[-U_x-U^2-q_t]=S. \tag{M5}
\]

在 \(S=0\) 时，取 \(\partial_x^{-1}U_t=q_t\) 的积分规范，(M5) 就是该论文式 (2.17) 的 Miura 关系。它说明 tau 的两个对数导数正好是 modified 场（加上显式背景）。**这是连续层的真实 Miura 联系。** 半离散层则需从两条离散壁方程重新做代数；不能把连续 \(\partial_x^{-1}\) 公式当成有限 \(h\) 的证明。下面的中点/跳量构造就是这个重新推导。

## 1. 起点：两条方程与格点位置

令 \(B_s=D_x^2+D_t+2sD_x\)，\(h\ne0\)。起点是

\[
B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0. \tag{B}
\]

\(F_j\) 位于 \(y=(j+1/2)h\)，\(G_j\) 位于 \(y=jh\)。以下在 \(F_j,G_j,G_{j+1}\) 非零、可局部取光滑对数的区域工作。设 \(\alpha_j=\log F_j\)、\(\beta_j=\log G_j\)。实值且固定符号时可用 \(\log|F_j|,\log|G_j|\)。

关键恒等式是

\[
\frac{B_s f\cdot g}{fg}=(\log f+\log g)_{xx}
+(\log f-\log g)_x^2+(\log f-\log g)_t
+2s(\log f-\log g)_x. \tag{1}
\]

平方项从 \(D_x^2\) 除以 \(fg\) 后精确产生；这一步没有做小 \(h\) 近似。用 (1) 归一化 (B)，分别记结果为 \(A_j=0,C_j=0\)，其中

\[
\begin{aligned}
A_j&=(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x,\\
C_j&=(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x.
\end{aligned} \tag{2}
\]

## 2. 对称场与最短闭合式

**有限 \(h\) 的 Miura 式起点。** 对下壁取 \(q_j^-=\alpha_j-\beta_j\)、\(s_-=a-h/2\)，对上壁取 \(q_j^+=\alpha_j-\beta_{j+1}\)、\(s_+=a+h/2\)。分别定义

\[
U_j^\pm=s_\pm+q_{j,x}^\pm,\qquad
\eta_j^-=(\alpha_j+\beta_j)_x-s_-^2x,\quad
\eta_j^+=(\alpha_j+\beta_{j+1})_x-s_+^2x.
\]

由式 (1) 可直接改写为两条 Riccati/Miura 型残差

\[
A_j=\eta_{j,x}^-+(U_j^-)^2+q_{j,t}^-,\qquad
C_j=\eta_{j,x}^++(U_j^+)^2+q_{j,t}^+. \tag{2a}
\]

这一步在任意有限 \(h\) 都精确，且给出机器核对的第一层；但两个壁的 \(U^\pm,\eta^\pm\) 尚不是最终的两个物理场。接下来取中点与跳量。两条归一化方程自然给出各自的“壁斜率”

\[
X_j=(\alpha_j-\beta_j)_x,\quad Y_j=(\alpha_j-\beta_{j+1})_x,
\quad P_j=(\alpha_j+\beta_j)_x,\quad R_j=(\alpha_j+\beta_{j+1})_x.
\]

对这两个壁斜率取中点和跳量，在 \(F\) 格点定义

\[
u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,\qquad
w_j=\frac4h(\beta_{j+1}-\beta_j)_x. \tag{3}
\]

于是 \(X_j+Y_j=u_j\)、\(X_j-Y_j=hw_j/4\)，即

\[
X_j=\frac{u_j}{2}+\frac{hw_j}{8},\qquad
Y_j=\frac{u_j}{2}-\frac{hw_j}{8}. \tag{3a}
\]

这两个系数由线性方程解出，不是试探得到的。它们立即给出

\[
X_j^2+Y_j^2=\frac{u_j^2}{2}+\frac{h^2w_j^2}{32},\qquad
X_j^2-Y_j^2=\frac{h}{4}u_jw_j,
\]
\[
(2a-h)X_j+(2a+h)Y_j=2au_j-\frac{h^2w_j}{4},
\]
\[
(2a-h)X_j-(2a+h)Y_j=h\left(\frac{a}{2}w_j-u_j\right). \tag{3b}
\]

因此非线性项、漂移项及 \(h\) 的系数都由“和/差”自动决定。令 \(Q_j=P_j+R_j\)。由于 \(P_j-R_j=-hw_j/4\)，把 (3b) 代入 \(A_j\pm C_j\) 并对 \(x\) 求导，得到下面的残差恒等式；这就是可重复使用的推导算法。

用 \(\delta_-z_j=(z_j-z_{j-1})/h\)、\(M_-z_j=(z_j+z_{j-1})/2\)，并设

\[
H_j=\frac12u_j^2+2au_j+h^2\left(\frac{w_j^2}{32}-\frac{w_j}{4}\right). \tag{4}
\]

则 (B) **精确推出**下面只含 \(u,w\) 的局部两场系统：

\[
\boxed{\delta_-\bigl(u_t+H_x\bigr)_j+
\partial_x^2\bigl(\delta_-u_j+M_-w_j\bigr)=0,} \tag{5}
\]
\[
\boxed{w_{j,t}+\partial_x\bigl[(u_j+2a)w_j-4u_j\bigr]-w_{j,xx}=0.} \tag{6}
\]

这里的暂时势 \(Q_j=(2\alpha_j+\beta_j+\beta_{j+1})_x\)。逐项展开得到对任意非零 \(F,G\) 均成立的残差恒等式

\[
u_{j,t}+H_{j,x}+Q_{j,xx}=\partial_x(A_j+C_j),
\qquad
w_{j,t}+[(u_j+2a)w_j-4u_j]_x-w_{j,xx}
=\frac4h\partial_x(A_j-C_j), \tag{7}
\]

以及 \(\delta_-Q_j=\delta_-u_j+M_-w_j\)。对 (7) 第一式作 \(\delta_-\) 就是 (5)，第二式就是 (6)。因此这里没有假设一个新的场方程，也没有逆差分；\(Q\) 只用于推导。

## 3. 为什么原报告用 \(u,v\)

为直接逼近连续 DLW 的物理变量，定义

\[
v_j=w_j+\delta_0u_j,\qquad
\delta_0u_j=\frac{u_{j+1}-u_{j-1}}{2h}. \tag{8}
\]

这是有限 \(h\) 下可直接反解的局部换元：\(w=v-\delta_0u\)。(5) 恰是 [NONLINEAR_CLOSURE.md](NONLINEAR_CLOSURE.md) 的 (N1)；把 (5) 经 \(M_+=(1+T)/2\) 平均后加到 (6)，得到该文 (N2)。因此 **(5)(6) 与 (N1)(N2) 是同一个有限 \(h\) 系统的两种场坐标**。保留 (5) 并用 (N2) 减回 \(M_+\)(N1) 可取回 (6)，没有因平均而丢掉格点交错模态。

在 \(F_j\) 的物理位置 \(y\)，若 \(F_j=f(y)\)、\(G_j=g(y-h/2)\)、\(G_{j+1}=g(y+h/2)\)，则

\[
u_j=2(\log f/g)_x+O(h^2),\qquad
w_j=4(\log g)_{xy}+O(h^2),
\]

而 (8) 给出 \(v_j=2(\log fg)_{xy}+O(h^2)\)。所以 \(w\) 使代数最短，\(v\) 使第二个场直接对应连续论文中的 \(v\)。二者并无不同的可积性结论。

更一般地，\(v^{(c)}=w+c\delta_0u\) 对任意固定 \(c\) 都是可逆的场重定义。只有 \(c=1\) 直接趋于上述标准 DLW 的 \(v\)；改变 \(c\) 不产生新的离散方程。

## 4. 还有哪些“转化”

| 选择 | 与现行 (B) 的关系 | 得失 |
| --- | --- | --- |
| \((u,w)\)，式 (3)–(6) | 同一双线性对的精确闭合换元 | 两场公式短；\(w\) 的连续极限是 \(v-u_y\)，不是标准物理 \(v\)。 |
| \((u,v)\)，式 (8) | 同一系统的精确局部换元 | 两个场在 \(F\) 位置二阶逼近标准 DLW 的 \(u,v\)；方程模板到 \(j\pm2\)。 |
| \(\widehat u_j=2(\log F_j/G_j)_x\)，\(\widehat v_{j+1/2}=2h^{-1}\partial_x\log(F_{j+1}G_{j+1}/F_jG_j)\) | 同一 (B) 的另一精确两场闭合；公式在 [NONLINEAR_CLOSURE.md §6](NONLINEAR_CLOSURE.md) | 只用单边配对；按同位物理场直接采样会出现一阶格点偏移。 |
| 改动 \(s_\pm\) 并相应改 Gram 格点乘子 | **改变有限 \(h\) 双线性系统**；见 [ALTERNATIVE_DISCRETIZATIONS.md](ALTERNATIVE_DISCRETIZATIONS.md) | 可保持任意 \(N\) Gram 族及二阶连续极限；固定物理 \(a,h\) 下闭合方程系数不同。 |
| 同节点 tau 的对数交叉比差商 | **另立离散系统**；见 [对数差商推导](../dlw_log_discretization/DERIVATION.md) | 有局部两场方程，但在原 \(F,G\) 中第二条一般是四次关系；旧 Gram 孤子族不能直接移植。 |
| 精确采样连续解并用 \(h^{-1}\log T\) | **非局部采样表示**；见 [ALTERNATIVE_DISCRETIZATIONS.md §5.2](ALTERNATIVE_DISCRETIZATIONS.md) | 保留连续解数据；需指定谱分支与解析函数类，尚不是任意格点初值的局部系统。 |

## 5. 可逆性与适用范围

从非零 \(F,G\) 到 (5)(6) 或 (N1)(N2) 是精确的。反向可在局部开链上递推 \(\beta_{j,x}\)、恢复 \(\alpha_{j,x}\)，再用 \(x,t\) 的积分/规范自由度令 \(A_j=C_j=0\)；详细步骤见 [NONLINEAR_CLOSURE.md §5](NONLINEAR_CLOSURE.md)。周期格点、周期 \(x\) 或固定远场条件另需全局相容约束。因此“局部模规范等价”不能被写成任意边界数据下的全局一一对应。

这套换元保留已由 Gram 双线性对证明的精确解族；它本身不证明一般初值的 IST、长期稳定性或新离散化的可积性。

## 6. 以后按这个固定流程推导

1. **固定双线性对与格点位置。** 不先猜非线性式，也不把两个壁上的量当作同位采样。
2. **用式 (1) 归一化。** 给两条残差起不同名字 \(A,C\)，暂不令它们为零，这样每一步都能保留可核对的残差恒等式。
3. **先写每个壁的 Miura/Riccati 残差，再取中点与跳量。** 用式 (2a) 检查归一化；用式 (3a) 线性求回两个壁斜率，按式 (3b) 机械计算平方项与漂移项。
4. **取 \(A+C\)、\(A-C\)。** 前者给 \(u,Q\)，后者给 \(w\)；对 \(x\) 求导消掉未知的时间积分常数。
5. **只用恒等式消去 \(Q\)。** \(\delta_-Q=\delta_-u+M_-w\) 给 (5)；另一式就是 (6)。
6. **最后才换成物理场 \(v\)。** 用 (8) 对齐连续 DLW，再检查自然格点位置上的 \(O(h^2)\) 极限、反向重构所需规范和边界条件。

符号核对入口是 [verify_nonlinear_closure.py](verify_nonlinear_closure.py)。脚本对任意符号函数核对残差恒等式，而非依赖某组孤子参数的数值小量。
