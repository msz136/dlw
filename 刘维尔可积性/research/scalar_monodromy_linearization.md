# 全周期标量单值算子在均匀背景的线性忠实性

2026-10-11。本命题审查完整算子系数是否丢失原场方向；它不是谱不变量独立性或 Liouville 完备性定理。下述证明只用形式微分算子代数，不预设原物理初值流。

## 命题与适用域

固定有限 $M\ge2$、$h>0$、空间周期 $L$。记 $a_j=U_j/2$、$g_j=hw_j/8$，冻结 $\sum_jg_j=S\ne0$ 和 $\sum_ja_jg_j=BS$ 的截面。这里冻结平均通量是选定截面；一般时间自由模须另按移动坐标处理，不称为方程强制常数。

在均匀背景 $a_j=B$、$g_j=\delta\ne0$，$S=M\delta$。定义

$$
T_j=(D-a_j+g_j)^{-1}(D-a_j-g_j),\quad
\mathcal P=T_{M-1}\cdots T_0,\quad
\mathcal L=-G(\mathcal P-I)^{-1}+B-G/2,
\quad G=2S.
$$

令 $\kappa=2\pi i n/L$、$n\ne0$，扰动为
$\delta a_j=e^{\kappa x}\alpha_j$、$\delta g_j=e^{\kappa x}\beta_j$。
线性化平均截面条件为 $\sum\alpha_j=\sum\beta_j=0$。

**命题。** 在该 $2(M-1)$ 维复 Fourier 切空间上，$D\mathcal P$ 和 $D\mathcal L$ 都单射；若 $\mathcal L=D+\sum_{r\ge1}\ell_rD^{-r}$，则仅前 $2(M-1)$ 个完整系数的线性化就足以恢复全部 $(\alpha,\beta)$。实场由正、负频率共轭配对得到相同结论。零 Fourier 模态由组件空间平均固定，不包含于本命题。

## 1. 带移位的确切变分

用 $\zeta$ 表示形式右符号，置 $z=\zeta-B$、$t(z)=(z-\delta)/(z+\delta)$。公式 $D e^{\kappa x}=e^{\kappa x}(D+\kappa)$ 保留了左右不对易性。从 $(D-a_j+g_j)T_j=D-a_j-g_j$ 得

$$
\delta T_j=e^{\kappa x}
\frac{-2(\delta\alpha_j+z\beta_j)}{(z+\kappa+\delta)(z+\delta)}.
$$

乘积求导时，扰动左边的背景因子必须取 $t(z+\kappa)$，右边取 $t(z)$。因此

$$
\delta\mathcal P
=e^{\kappa x}\frac{-2\mathsf N(z)}{(z+\kappa+\delta)^M(z+\delta)^M},
$$

$$
\mathsf N(z)=\sum_{j=0}^{M-1}(\delta\alpha_j+z\beta_j)
v(z)^{M-1-j}u(z)^j,
$$

$$
u(z)=z^2+\kappa z-\delta^2-\kappa\delta,\qquad
v(z)=z^2+\kappa z-\delta^2+\kappa\delta.
$$

平均约束消去了 $\mathsf N$ 的最高两阶系数，故 $\deg\mathsf N\le2M-3$；更直接的分解见下一节。

## 2. 反射恢复两组场方向

置 $m=M-1$、$W=z^2+\kappa z-\delta^2$、$\varepsilon=\kappa\delta\ne0$，定义

$$
F_j(W)=(W+\varepsilon)^{m-j}(W-\varepsilon)^j,
\quad A(W)=\sum_{j=0}^m\alpha_jF_j(W),
\quad Q(W)=\sum_{j=0}^m\beta_jF_j(W).
$$

由于两组系数和为零，$\deg A,\deg Q\le m-1$，且 $\mathsf N(z)=\delta A(W)+zQ(W)$。反射 $\iota(z)=-\kappa-z$ 保持 $W$，因而

$$
Q(W)=\frac{\mathsf N(z)-\mathsf N(-\kappa-z)}{2z+\kappa},
\qquad
A(W)=\frac{\mathsf N(z)+\mathsf N(-\kappa-z)+\kappa Q(W)}{2\delta}.
$$

右侧是多项式恒等式，表面的 $2z+\kappa$ 商具有整除性。由此若 $\mathsf N=0$，就有 $A=Q=0$。

$F_0,\ldots,F_m$ 为次数不超过 $m$ 的多项式空间的一组基：若 $\sum c_jF_j=0$，除以 $(W+\varepsilon)^m$，以 $r=(W-\varepsilon)/(W+\varepsilon)$ 作非恒定有理变量，即得 $\sum c_jr^j=0$，故所有 $c_j=0$。于是 $A=Q=0$ 强制 $\alpha=\beta=0$。这证明 $D\mathcal P$ 单射，同时给出了明确反演步骤。

## 3. 有限系数计数与一个精确行列式

选独立变量 $\alpha_0,\ldots,\alpha_{m-1}$、$\beta_0,\ldots,\beta_{m-1}$，最后一个等于前面的负和。两组使用基 $H_j=F_j-F_m$，$0\le j<m$，该基的系数矩阵（按 $W^0,\ldots,W^{m-1}$ 排列）满足

$$
\det H=(2\varepsilon)^{m(m+1)/2}.
$$

理由是完整 $F_j$ 的系数矩阵为二维线性替换 $(W,1)\mapsto(W+\varepsilon,W-\varepsilon)$ 的 $m$ 次对称幂；按升幂排列时行列式为 $(2\varepsilon)^{m(m+1)/2}$。从前 $m$ 列减去最后一列，最高次行变成 $(0,\ldots,0,1)$，展开即为上述约化行列式。

再从 $(A,Q)$ 的系数到 $\mathsf N$ 的 $z^0,\ldots,z^{2m-1}$ 系数，交错排列是对角为 $(\delta,1,\ldots,\delta,1)$ 的三角变换。因此按“先全部 $\alpha$，再全部 $\beta$”的列顺序，得到

$$
\boxed{\det\frac{\partial(\mathsf N_0,\ldots,\mathsf N_{2m-1})}
{\partial(\alpha_0,\ldots,\alpha_{m-1},\beta_0,\ldots,\beta_{m-1})}
=(-1)^{m(m-1)/2}\delta^m(2\kappa\delta)^{m(m+1)}.}
$$

它对每个非零 Fourier 模态都非零。分母首一、次数 $2M$，所以 $\delta\mathcal P$ 的前 $2m$ 个可能非零 Laurent 系数（阶数 $-3$ 到 $-(2m+2)$）以三角非奇异变换决定 $\mathsf N$。

最后

$$
\delta\mathcal L
=e^{\kappa x}\frac{G}{[t(z+\kappa)^M-1][t(z)^M-1]}
\frac{-2\mathsf N(z)}{(z+\kappa+\delta)^M(z+\delta)^M}.
$$

前置因子首项为 $z^2/G$，非零；它将上述 $2m$ 个系数三角地移至 $\delta\ell_1,\ldots,\delta\ell_{2m}$，再以 $z=\zeta-B$ 改写也仅是三角变换。命题得证。

## 证据与后续接口

[独立精确核验脚本](verify_scalar_monodromy_linearization.py) 检查 Bernstein 基行列式、反射整除恢复、完整符号乘积变分以及有限系数矩阵；输出见 [核验记录](scalar_monodromy_linearization_checks.json)。这些有限阶检查用于抓取符号和移位错误，全 $M$ 结论的依据是上面的代数证明。

本命题补上了全周期均匀背景的一个信息计数环节，不能越级推断非线性局部逆、谱数据反演或 Hamilton 积分完备性。尤其完整算子系数包含相位信息，积分谱迹在固定平均的均匀背景上可能一阶导数全部为零。下一步须构造保持同一物理 Casimir 叶的非线性反演，证明其函数空间估计，并将全算子信息转换成具有合法 Poisson 结构的完整谱数据。
