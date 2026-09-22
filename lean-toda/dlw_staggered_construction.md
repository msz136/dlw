# DLW：保留任意 N 孤子行列式结构的 y 半离散构造

本文固定原论文后续使用的 lambda=-2，保留任意 a。
来源：Sheng & Yu, Physica D 432 (2022) 133140，第 (7)、(11)-(15)、(29)-(31) 式。
这是从论文已知行列式恒等式推导的构造；未进行独立文献新颖性检索。

## 1. 结果及“最小”的含义

令 B=D_x^2+D_t+2aD_x。新系统为

\[
(B-hD_x)F_j\cdot G_j=0,\qquad
(B+hD_x)F_j\cdot G_{j+1}=0.
\]

G_j 位于 y=jh，F_j 位于 y=(j+1/2)h。只有 y 被离散化。

“小改动”指保持两个 tau 函数、两条方程、相邻格点、x 二阶/t 一阶导数，
只把 B 的一阶导数系数作正负 h 修正，并采用交错位置。
没有证明它在所有可能离散化中具有某种全局最小性。
旧的同点方程 B f_j.g_j=0 不再原样保留。

## 2. 发现路径

对负流的因子化格点乘子

\[
R_i=\frac{1+\epsilon/(q_i+b)}{1-\epsilon/(p_i-b)}
\]

检索低阶相邻格点双线性关系，得到

\[
B_b F_j\cdot G_j=0,\qquad
B_{b+\epsilon}F_j\cdot G_{j+1}=0,
\quad B_s=D_x^2+D_t+2sD_x.
\]

选择 b=a-h/2、epsilon=h，得到上面的对称参数形式。
这一探索只用于发现；任意 N 的依据是第 5 节的行列式归约。

## 3. 双孤子显式公式

定义 d=h/2、P_i=p_i-a、Q_i=q_i+a，并令

\[
\rho_i=\frac{(P_i+d)(Q_i+d)}{(P_i-d)(Q_i-d)},\qquad
r_i=-\frac{P_i+d}{Q_i-d},
\]
\[
E_{i,j}=\rho_i^j
\exp\big((p_i+q_i)x+(q_i^2-p_i^2)t+\theta_{i0}\big),
\]
\[
\Gamma=\frac{(p_1-p_2)(q_1-q_2)}
{(p_1+q_1)(p_1+q_2)(p_2+q_1)(p_2+q_2)}.
\]

则

\[
G_j=1+\frac{E_{1,j}}{p_1+q_1}
      +\frac{E_{2,j}}{p_2+q_2}+\Gamma E_{1,j}E_{2,j},
\]
\[
F_j=1+\frac{r_1 E_{1,j}}{p_1+q_1}
      +\frac{r_2 E_{2,j}}{p_2+q_2}
      +\Gamma r_1r_2 E_{1,j}E_{2,j}.
\]

原论文的四项结构和 Cauchy 相互作用因子 Gamma 保留不变。
改变的是格点传播因子，以及 F 的谱比值 r_i。
上述解不是旧系统的一组新解，而是新格点方程的解。

## 4. 任意 N 的有限和形式

对任意指标子集 S，定义

\[
C_S=\prod_{i\in S}\frac1{p_i+q_i}
\prod_{i<k,\ i,k\in S}
\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)}.
\]

空集对应的乘积为 1。令

\[
G_j=\sum_{S\subseteq\{1,\ldots,N\}}C_S\prod_{i\in S}E_{i,j},
\qquad
F_j=\sum_{S\subseteq\{1,\ldots,N\}}C_S\prod_{i\in S}(r_i E_{i,j}).
\]

展开有 2^N 项，但可以紧凑写成 N 阶行列式。
这是通用代数 tau 解族；参数不自动保证实值性、无零点或无奇点。

## 5. 任意 N 的行列式论证

令

\[
M_{ik}(j)=\frac{e^{\xi_i+\eta_k}}{p_i+q_k}
\left(\frac{p_i-a+d}{p_i-a-d}\right)^j
\left(\frac{q_k+a+d}{q_k+a-d}\right)^j,
\]

其中 xi_i=p_i x-p_i^2 t+xi_i0，eta_k=q_k x+q_k^2 t+eta_k0。
对任意参数 s 定义

\[
T_s(M)=\det\left[\delta_{ik}-\frac{p_i-s}{q_k+s}M_{ik}\right],
\qquad T_0^{\mathrm{base}}(M)=\det(I+M).
\]

这里 base 上标用于避免把“无谱比值 tau”误读为 s=0 的 T_s。
原论文的行列式双线性恒等式给出

\[
B_s T_s(M)\cdot T_0^{\mathrm{base}}(M)=0.
\]

格点乘子独立于 x,t，可吸收到指数的行/列常数中，故可应用该恒等式。

取 G_j=T_base(M(j))、F_j=T_{a-d}(M(j))。
第一条方程立即成立。

注意每个矩阵元素均满足

\[
-\frac{p_i-a-d}{q_k+a+d}M_{ik}(j+1)
=-\frac{p_i-a+d}{q_k+a-d}M_{ik}(j).
\]

因此 T_{a+d}(M(j+1))=F_j，而 T_base(M(j+1))=G_{j+1}。
再用同一个恒等式便得到

\[
B_{a+d}F_j\cdot G_{j+1}=0.
\]

论证不依赖 N，因此适用于所有有限 N。
这是对论文已有恒等式的数学归约，不是由 N<=5 的试验外推。
尚未将原论文的任意阶行列式恒等式整体形式化到 Lean。

## 6. 连续极限与二阶形式相容性

以 F_j 所在的 Y=(j+1/2)h 为中心，写
F_j=f(Y)、G_j=g(Y-h/2)、G_{j+1}=g(Y+h/2)。
把两条方程左端记为 E_minus、E_plus。
考虑等价的归一化组合

\[
\mathcal A_h=(E_++E_-)/2,\qquad
\mathcal C_h=(E_+-E_-)/h.
\]

对足够光滑函数，展开得

\[
\mathcal A_h=Bf\cdot g
 +h^2\left(\frac18Bf\cdot g_{yy}+\frac12D_xf\cdot g_y\right)+O(h^4),
\]
\[
\mathcal C_h=Bf\cdot g_y+2D_xf\cdot g
 +h^2\left(\frac1{24}Bf\cdot g_{yyy}
              +\frac14D_xf\cdot g_{yy}\right)+O(h^4).
\]

因此极限为 Bf.g=0 和 Bf.g_y+2Dx f.g=0。
由总导数 (Bf.g)_y=Bf_y.g+Bf.g_y=0 可知后者等价于

\[
(D_yB-4D_x)f\cdot g=0,
\]

恰是原论文 lambda=-2 的第二条双线性方程。
二阶结论针对这两条归一化方程的残差，不是一般初值数值求解器的收敛定理。

另有

\[
\frac{\log\rho_i}{h}
=\frac1{P_i}+\frac1{Q_i}
 +\frac{h^2}{12}\left(\frac1{P_i^3}+\frac1{Q_i^3}\right)+O(h^4).
\]

在实参数、小步长且采用连续分支时，
r_i/sqrt(rho_i)=-(P_i/Q_i)+O(h^2)。这对应 F 位于半格点，
不能把 F_j 与 y=jh 处的连续 f 直接比较并据此误判为一阶。

## 7. 条件与未完成事项

- h>0；p_i+q_k 以及 P_i+-h/2、Q_k+-h/2 等涉及的分母/整数幂基底须非零。
- 实谱参数可取 h/2<min_i(|P_i|,|Q_i|)，保证传播因子为正；这不自动保证 tau 无零点。
- 若还原对数非线性变量，须另行限制到相应 tau 非零的区域。
- 这是两个交错 tau 场的闭合双线性系统；非线性变量的局部闭合仍未推导。
- 尚未建立一般初边值适定性、稳定性或数值收敛理论；连续模型的高频问题不会因这些代数恒等式自动消失。
- 任意 N 行列式解提供强结构证据；本次未独立推导 Lax 对、守恒律，也不宣称文献新颖性。

## 8. 已执行验证

1. SymPy 对任意 P1,P2,Q1,Q2,h 的一般双孤子展开：两式共 18 个指数系数全部恒等于零。
2. 精确有理数测试：4 组谱参数族，各测 N=1,2,3,4,5；再测旧候选的反例参数。
   共检验 2922 个系数，全部为零。测试不作 tau 正则性的断言。
3. Lean：矩阵元素的参数移位恒等式、归一化方程等价性、二阶展开的代数系数。
   不把这些小定理标注为已形式化任意 N 的行列式证明。
4. lake build TodaFormalization 成功。

复现命令：

```text
python check_dlw_staggered.py
python check_dlw_staggered.py --symbolic
lake build TodaFormalization
```

普通精确检验只需 Python 标准库；符号双孤子检验需要 SymPy。
