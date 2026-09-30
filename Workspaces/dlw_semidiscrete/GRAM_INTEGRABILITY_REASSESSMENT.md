# Gram τ 序列在新非线性 DLW 系统中的性质：重新核验

日期：2026-09-19。承接 `NONLINEAR_CLOSURE.md`。

> **谱构造后续进展**：见 `S_INTEGRABILITY_STATUS.md`。任意 N Gram 解上的精确谱波函数
> 与非平凡谱渐近比现已给出，并完成秩一更新证明及 180 组精确检查。
> 一般初值的逆散射可解性仍未建立；“S 可积”不能直接等同于弱 Lax 对或 Painlevé 失败。

## 1. 本次结论

**纯格点 Gram 构造可以保留，而且确实给出上一份报告闭合 u/v 系统的任意 N 行列式解。**
旧审计否定的是另一种把连续 y 相位也随 s 改动的混合构造，不能据此否定只含 x、t、j 的半离散构造。

| 性质 | 本次判断及证据 |
|---|---|
| 两条有限 h 双线性方程 | 成立；下面给出任意 N 的行列式证明，另有 N=1..5 精确系数验证 |
| 新非线性 u/v 方程 | 成立；由一般消元定理推出，另直接代入验证 N=1,2,3 |
| 整数 τ_n 序列 | 固定 s 的双线性链成立；参数—格点恒等式可推广到任意整数 n |
| 实解无奇点 | 有明确充分参数区间，保证所有相关 τ 严格为正 |
| 凸性 | 正系数区间内 τ 和 log τ 的连续指数插值具有凸性；不意味着 u/v 凸 |
| 孤子相互作用 | 归一化两体系数与 h、n、s 无关；通常的非退化分离散射中保留弹性相移结构 |
| 守恒性质 | 闭合系统有明确的 x 方向局部守恒律；行列式孤子可算出质量积分 |
| 线性相容结构 | 已推导并精确验证两条热算子 Darboux 交织关系及格点连接 |
| 辅助层级 | τ_n 的辅助连续负流满足 2D Toda 恒等式，N=1..5 精确验证 |
| 强/完全可积 | 本轮不作定论；尚未建立不可消去谱参数的完整谱问题、逆散射或无穷独立守恒量 |
| 高波数稳定性 | 不保持一般稳定性：x 高频仍有线性指数增长支 |

旧 `lax/VERDICT.md` 的“不是强可积”“半离散系统已经证明 S-可积”等全系统定性均超出其证据，不能继续作为定论。
本次新增的是可具体检查的解族、守恒律和 Darboux 结构，不通过重命名“强/弱”来代替证明。

## 2. 必须分开的两种 τ 构造

令 \(d=h/2\)、\(P_i=p_i-a\)、\(Q_k=q_k+a\)，

\[
 \lambda_h(z)=\frac{z+d}{z-d},\qquad
 \chi_{ik}=\lambda_h(P_i)\lambda_h(Q_k).
\]

本次采用的**纯半离散**构造为

\[
 \tau_n(j;s)=\det_{1\le i,k\le N}\left[
 \delta_{ik}+\frac{\rho_i}{p_i+q_k}
 \left(-\frac{p_i-s}{q_k+s}\right)^n
 \chi_{ik}^{\,j}
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
 \right]. \tag{G}
\]

其中 \(n,j\in\mathbb Z\)，谱参数避开分母零点，\(\rho_i\) 为常数。
可以再乘共同的行/列相位常数，或保留一个**各 s 层共用**的独立旁观参数相位；下面的结论仍成立。
式 (G) 没有一个随 s 变化的、额外连续物理 y。

取

\[
 F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j;s).
\]

在 (G) 中 \(\tau_0\) **与 s 无关**，因此后一式可简写为 \(G_j=\tau_0(j)\)。

相比之下，`jet3.py`/`jet4.py` 的混合构造还包含

\[
 \exp\left[y\left(\frac1{p_i-s}+\frac1{q_k+s}\right)\right]. \tag{Y}
\]

这使 \(\tau_0(j;s)\) 也依赖 s；F 和 G 因而使用了不同的 y 相位。
对这个不同对象，旧审计的非零残差有实际意义。
**但 y=0 的限制此时是在定义一个只剩 x、t、j 的半离散函数，不是仅在一个 x/t 基点“碰巧通过”。**
本次按全部实际指数向量合并系数，证明 (G) 对所有 x、t 恒成立。
相位 (Y) 在不同 s 层不匹配的问题仍成立，但不能外推为 (G) 不成立。

此外，旧 `audit_tau.py` 对 G 的系数也使用了 `n=1`，与目标 G=τ_0 不同；它不能单独作为目标格点对的反例。
旧连续 (6) 的算子混淆已在 `NONLINEAR_CLOSURE.md` §7 纠正。

## 3. 任意 N、任意整数 n 的精确结构

### 3.1 固定 s 的 Gram 双线性链

对 (G) 有

\[
 \boxed{(D_x^2+D_t+2sD_x)\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.} \tag{G1}
\]

这里格点乘子和 n 因子都可以吸收到行、列振幅中，所以不会改变证明。
下面给出不依赖有限 N 扫描的行列式论证。

设 M 为 τ_n 的矩阵，r、c 为其指数行列因子，并设
\(b_k=c_k/(q_k+s)\)。直接求导和比较相邻 n 可得

\[
 M_x=rc^{\mathsf T},\qquad
 M_t=-\operatorname{diag}(p)rc^{\mathsf T}
       +rc^{\mathsf T}\operatorname{diag}(q),\qquad
 M_{n+1}=M-rb^{\mathsf T}.
\]

在 M 可逆区域，记 \(z=M^{-1}r\)、\(\kappa=c^{\mathsf T}z=(\log\det M)_x\)、
\(\zeta=b^{\mathsf T}z\)。矩阵行列式引理给出

\[
 \frac{\tau_{n+1}}{\tau_n}=1-\zeta.
\]

利用 \(r_t=-\operatorname{diag}(p)^2r\)、\(c_t=\operatorname{diag}(q)^2c\)，
以及 \((M^{-1})_x=-M^{-1}M_xM^{-1}\)，可直接计算

\[
 \zeta_t+\zeta_{xx}+2s\zeta_x=2\kappa_x(1-\zeta).
\]

因此 \(\psi=\tau_{n+1}/\tau_n\) 满足

\[
 \psi_t+\psi_{xx}+2s\psi_x+2(\log\tau_n)_{xx}\psi=0,
\]

乘以 \(\tau_n^2\) 恰为 (G1)。清除分母后它是行列式恒等式，延拓到 τ 的零点也成立；
非线性物理场则仍需避开这些零点。附录给出标量消去细节。

### 3.2 参数—格点恒等式实际上在纯格点构造中成立

关键是逐矩阵元的有理恒等式

\[
 -\frac{P_i-d}{Q_k+d}\,
 \frac{P_i+d}{P_i-d}\frac{Q_k+d}{Q_k-d}
 =-\frac{P_i+d}{Q_k-d}.
\]

故对于任意整数 n，

\[
 \boxed{\tau_n(j;a-d)=\tau_n(j+n;a+d).} \tag{G2}
\]

没有指数近似、没有 h 展开，也没有把 y 相位不同的项强行视为同一指数。
特别是 \(F_j=\tau_1(j+1;a+d)\)。结合 (G1) 的 n=0 及 τ_0 与 s 无关，得到

\[
 \boxed{B_{a-d}F_j\cdot G_j=0,\qquad B_{a+d}F_j\cdot G_{j+1}=0.} \tag{G3}
\]

这是任意 N 的证明。上一份报告的非线性消元定理因此直接适用，(G) 产生其 u/v 系统的精确解。

## 4. 新物理变量、无奇点与凸性

继续使用已证明的定义

\[
 u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
 v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.
\]

一个便于使用的全实无奇点充分条件是

\[
 h>0,\quad 0<p_1<\cdots<p_N<a-d,\quad
 0<q_1<\cdots<q_N,\quad \rho_i>0. \tag{R}
\]

此时所有 \(p_i+q_k>0\)，\(\lambda_h(P_i)>0\)、\(\lambda_h(Q_k)>0\)，
且 \(-(p_i-s)/(q_i+s)>0\) 对 \(s=a\pm d\) 成立。

用主子式展开，任意子集 S 的 Cauchy 行列式为

\[
 \det\left[\frac1{p_i+q_k}\right]_{i,k\in S}
 =\frac{\prod_{i<k\in S}(p_k-p_i)(q_k-q_i)}
        {\prod_{i,k\in S}(p_i+q_k)}>0.
\]

所以 (G) 的所有指数项系数为正，常数项为 1，特别地

\[
 F_j>0,\qquad G_j>0
 \quad\text{对所有实 x,t 及所有整数 j 成立。}
\]

这给出全实域无对数奇点的解族；不是对任意复参数、breather 或退化有理极限的正则性声明。

如果用户说的“凸函数”确实也包含凸性：在 (R) 下，正系数指数和 τ 的 Hessian 半正定；
\(\log\tau\) 的 Hessian 是指数斜率的加权协方差，也半正定。
这个结论适用于 x、t，以及用正 χ 定义的实格点坐标插值；u/v 是不同 log τ 的有符号组合及导数，
不能据此宣布 u/v 为凸函数。

## 5. 孤子系数、相移与连续极限

令

\[
 E_i=\frac{\rho_i}{p_i+q_i}
      e^{(p_i+q_i)x+(q_i^2-p_i^2)t}\chi_{ii}^{\,j},\quad
 \gamma_i(s)=-\frac{p_i-s}{q_i+s}.
\]

则主子式展开可以写为

\[
 \tau_n(j;s)=\sum_{S\subset\{1,\ldots,N\}}
 \left(\prod_{i\in S}\gamma_i(s)^n E_i\right)
 \left(\prod_{i<k\in S}A_{ik}\right),
\]
\[
 \boxed{A_{ik}=\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)}.} \tag{I}
\]

**归一化相互作用系数 A 不含 h、s、n。** 不应与未归一化的双指数系数 κ 混为一谈；后者会带入单孤子幅度因子。

当各孤子具有不同 x/t 速度、可作通常的 t→±∞ 分离渐近时，其余指数趋于 0 或 ∞，
留下的第 i 个局部剖面等价于 \(E_i\mapsto E_i\prod_k A_{ik}\)。
F、G、G_{j+1} 接受同一相位替换，新增背景的线性对数项在物理变换中抵消，
所以新 u/v 变量保留有限 h 下的弹性孤子相移结构。
相位位移 \(\log A_{ik}\) 及 x 位移 \(\log A_{ik}/(p_i+q_i)\) 与 h 无关（符号由散射方向决定）；
换算成 y 方向几何位移时需要除以 \(\log\chi_{ii}/h\)，会有 h 依赖。

作为可直接使用的单孤子，写 \(S=p+q\)、\(\gamma=-(P+d)/(Q-d)\)、\(\chi=\lambda_h(P)\lambda_h(Q)\)，
\(E=\rho e^{Sx+(q^2-p^2)t}\chi^j/S\)，则

\[
 G_j=1+E,\quad F_j=1+\gamma E,\quad G_{j+1}=1+\chi E,
\]
\[
 u_j=U(E):=S\left[\frac{2\gamma E}{1+\gamma E}
                    -\frac{E}{1+E}-\frac{\chi E}{1+\chi E}\right],
\]
\[
 v_j=\frac{4S}{h}\left[\frac{\chi E}{1+\chi E}-\frac{E}{1+E}\right]
       +\frac{U(\chi E)-U(E/\chi)}{2h}.
\]

与连续物理位置比较时，G 在 y=jh、F 在 y=(j+1/2)h。局部正实分支上，

\[
 \frac1h\log\chi_{ik}
 =\frac1{P_i}+\frac1{Q_k}
 +\frac{h^2}{12}(P_i^{-3}+Q_k^{-3})+O(h^4),
\]
\[
 \log\frac{\gamma_i(a-d)}{\gamma_i(a)}
 =\frac h2(P_i^{-1}+Q_i^{-1})
 +\frac{h^2}{8}(Q_i^{-2}-P_i^{-2})+O(h^3).
\]

前者给出格点相位二阶逼近；后者的一阶项恰对应 F 的半格点位置。
因此固定物理 y 的紧集、谱参数远离极点、τ 远离零点时，F/G 行列式及相应物理 u/v 对连续解都是二阶逼近。
不能把这一结论简化成“只重正化相位，F 的振幅系数完全不变”：F 的 γ 也随 h 改变。

## 6. 明确的守恒律

设 \(W=v-\delta_0u\)，以及上一份报告中的 H。闭合系统直接给出

\[
 W_{j,t}+\partial_x\left[(u_j+2a)W_j-4u_j-W_{j,x}\right]=0, \tag{C1}
\]
\[
 v_{j,t}+\partial_x\left[\delta_0H_j+(u_j+2a)W_j-4u_j
             +\partial_x\left(\delta_0u_j+\frac{h^2}{4}\Delta_hW_j\right)\right]=0. \tag{C2}
\]

在 x 周期边界或通量在 ±∞ 相等、积分存在时，每个 j 的 \(\int W_jdx\)、\(\int v_jdx\) 守恒。
N1 同时给出 \(\partial_t\delta_-\int u_jdx=0\)。这些律之间有依赖关系；不声称它们组成无穷独立守恒量族。

对 (R) 中的 N 孤子，因所有 \(p_i+q_i>0\)，x→−∞ 由常数项主导、x→+∞ 由全子集主导，
可精确算出

\[
 \boxed{\int_{\mathbb R}u_j\,dx
       =\sum_i\log\frac{P_i^2-d^2}{Q_i^2-d^2},\qquad
 \int_{\mathbb R}v_j\,dx=\frac4h\sum_i\log\chi_{ii}.} \tag{C3}
\]

它们与 t、j 无关，且连续极限分别为
\(2\sum_i\log(-P_i/Q_i)\) 和 \(4\sum_i(P_i^{-1}+Q_i^{-1})\)。
这也展示了旧报告“某个密度随 x,t 变化，所以不是守恒密度”的错误：守恒密度可以随时空变化，
需要检验的是局部散度律或满足边界条件的积分。

## 7. 可实际验证的 Darboux 线性结构

在证明用的对数势中设 \(\alpha_j=\log F_j\)、\(\beta_j=\log G_j\)，

\[
 V_j=2\beta_{j,xx},\quad V^F_j=2\alpha_{j,xx},\quad
 \mathcal H_j=\partial_t+\partial_x^2+V_j,\quad
 \mathcal H^F_j=\partial_t+\partial_x^2+V^F_j.
\]

令

\[
 w^-_j=a-d+(\alpha_j-\beta_j)_x,\quad
 w^+_j=a+d+(\alpha_j-\beta_{j+1})_x,\quad
 T_j^\pm=\partial_x-w_j^\pm.
\]

由 G3 得到的种子
\(e^{s x-s^2t}F/G\) 满足对应热方程，且有精确交织恒等式

\[
 \boxed{\mathcal H^F_jT_j^-=T_j^-\mathcal H_j,\qquad
        \mathcal H^F_jT_j^+=T_j^+\mathcal H_{j+1}.} \tag{D1}
\]

事实上对任意 w、V、试探波函数 ψ，

\[
 [\partial_t+\partial_x^2+V+2w_x](\partial_x-w)\psi
 -(\partial_x-w)[\partial_t+\partial_x^2+V]\psi
 =-(w_t+w_{xx}+2ww_x+V_x)\psi.
\]

代入上述两组 w、V，右侧分别是归一化双线性残差的 x 导数乘以 −ψ；这已对任意符号函数验证。

由此得到相容的格点线性关系

\[
 \mathcal H_j\psi_j=0,\qquad T_j^+\psi_{j+1}=T_j^-\psi_j. \tag{D2}
\]

它在新物理变量中的格点部分尤其简洁：

\[
 \boxed{
 \left[\partial_x-a-\frac{u_j}{2}+\frac h8(W_j-4)\right]\psi_{j+1}
 =\left[\partial_x-a-\frac{u_j}{2}-\frac h8(W_j-4)\right]\psi_j.} \tag{D3}
\]

时间势 V 可按

\[
 V_{j+1}-V_j=\frac h2 W_{j,x},\qquad
 V_{j,x}=-\frac12\left(u_{j,t}+H_{j,x}+u_{j,xx}+\frac h2W_{j,xx}\right)
\]

从物理场局部重构；后一式涉及一次 x 积分，带有相应积分自由度。
这与上一份报告的局部重构边界一致。

在形式逆算子意义下，\(L_j=(T_j^+)^{-1}T_j^-\) 满足
\(\mathcal H_{j+1}L_j=L_j\mathcal H_j\)。
这个结构比“从某个 τ 比值拟合一个矩阵递推”更有内容，因为相容障碍就是原方程残差。
但本轮仍未证明不可消去的谱参数、全套谱理论或周期谱不变量；
把 \(\psi=e^{zx-z^2t}\widehat\psi\) 代入虽可引入 z，却是可逆规范变化，不能凭此宣称已有非平凡谱曲线。

### 辅助 2D Toda 序列

固定 s，对所有 τ_n 使用同一额外相位
\(e^{\eta(1/(p_i-s)+1/(q_k+s))}\)，则精确检查满足

\[
 \left(\tfrac12D_xD_\eta-1\right)\tau_n\cdot\tau_n
       +\tau_{n+1}\tau_{n-1}=0.
\]

本轮对 N=1..5、n=−1,0,1、三个步长共 45 组作了系数级验证。
这是辅助层级的证据；\(\partial_\eta\) 不是物理格点差分，不能将该恒等式未经推导直接改成新的 j 方向方程。

## 8. 为什么旧“不可积定论”不成立

1. `final_test.py` 从单个试探波函数的相邻值拟合递推系数，没有先证明与原方程等价的时空相容条件。
2. 它将几个格点的开链乘积当作周期单值矩阵，没有验证周期边界。
   真正的 \(L_{j,t}=M_{j+1}L_j-L_jM_j\) 只给出开链
   \(T_t=M_NT-TM_0\)；只有端点相容等条件下才可由此推出迹守恒。
3. 固定 z 的标量比值 \((z+Q_{j+1})/(z+Q_j)\) 相乘，
   与矩阵 \(\begin{pmatrix}1&Q_{j+1}\\1&Q_j\end{pmatrix}\) 表示的 Möbius 映射复合不是同一运算。
   例如 z=5、Q_0=1、Q_1=2、Q_2=3：前者为 4/3，后者为 25/19。
4. Lean 文件的 `zf_all` 明确要求所有 Q 已经 `IsZFree`，而 `Lmat` 的定义本来就没有谱参数。
   它证明的是这个指定无谱矩阵乘积仍无谱，不能排除别的谱表示，更不能证明整个系统不可积。
   本轮没有改动或重跑 Lean 工程；问题在数学建模和结论外推，不在形式证明是否通过。
5. 守恒密度不要求逐点常数；连续 DLW 的 Painlevé 或“weak Lax”文献性质也不能自动移植到有限 h 系统。

因此应撤回旧文档的全系统强/弱可积定论，保留其中那些指定矩阵的代数恒等式及其原有假设。

## 9. 仍需明确的限制：精确解不等于稳定性

利用与新方案等价的两点物理形式，在零背景线性化并取
\(e^{ikx+i\ell jh+\sigma t}\)。令

\[
 K_h=\frac2h\sin\frac{\ell h}{2},\qquad
 C_h=\cos\frac{\ell h}{2},\qquad K_h\ne0.
\]

精确线性色散关系是

\[
 \boxed{(\sigma+2aik)^2=k^4+\frac{4k^3C_h}{K_h}-h^2k^2.} \tag{S}
\]

固定非退化格点波数后，\(|k|\to\infty\) 时存在 \(\Re\sigma\sim+k^2\) 的增长支。
因此 y 半离散化没有消除 x 方向的高频线性不稳定。
这里只给出线性结论，不把它未经函数空间分析升级为非线性不适定定理。

## 10. 可复现证据与未完成边界

运行（工作区根目录）：

```
python Workspaces/dlw_semidiscrete/verify_gram_reassessment.py
python Workspaces/dlw_semidiscrete/verify_integrability_structure.py
```

第一项不导入旧 τ 引擎。用 Fraction 表示实际指数向量及其系数；
主子式展开与直接矩阵排列展开在 N≤3 交叉核验。

- 纯格点双线性对：N=1..5，每个 N 的 2 组参数 × 5 个 h × 4 个 j，共 200 组；两式残差全部字面零。
- 整数 τ_n 链与移位恒等式：n=−2..2，精确检查。
- 新非线性系统直接代入：N=1,2,3，2 组参数 × 3 个 h × 3 个 j，共 54 组；全部 Fraction(0)。
  这些直接代入是精确有理 jet 点检验；任意 x,t 的结论由前述系数恒等式及一般消元证明保证。
- 故意构造的混合 y 相位反例有非零系数；将该额外 y 限制为 0 后，对所有 x,t 的系数恒零。
- 辅助 Toda：45 组精确系数检查；Darboux、相互作用系数、质量因子、线性色散均作符号检查。

机器结果：`gram_reassessment_results.json`。前一轮的 `verify_nonlinear_closure.py` 提供一般消元与二阶一致性证明。

尚未完成：不可消去谱参数的完整 Lax 谱问题、无穷独立守恒量或递归算子、周期谱理论、
非线性稳定性、全体复参数与退化解的正则性。这些是可继续研究的问题，不构成对上述已证性质的否定。

## 附录：Gram 引理的标量计算

在 §3.1 的记号下，再记
\(\mu=c^{\mathsf T}\operatorname{diag}(q)z\)、
\(\nu=c^{\mathsf T}M^{-1}\operatorname{diag}(p)r\)、
\(\eta_1=b^{\mathsf T}M^{-1}\operatorname{diag}(p)r\)、
\(\eta_2=b^{\mathsf T}M^{-1}\operatorname{diag}(p)^2r\)。直接微分得

\[
 \kappa_x=\mu+\nu-\kappa^2,\quad
 \zeta_x=\kappa(1-\zeta)-s\zeta+\eta_1,
\]
\[
 (\eta_1)_x=\nu(1-\zeta)-s\eta_1+\eta_2,\quad
 \zeta_t=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\]

代入即得 \(\zeta_t+\zeta_{xx}+2s\zeta_x=2\kappa_x(1-\zeta)\)。
整个证明不使用矩阵大小 N 的特殊性，也不依赖指数函数在某点取值为 1。
