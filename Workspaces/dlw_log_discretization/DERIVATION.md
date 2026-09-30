# 对数差商替换：推导与孤子检验

这是真正更换离散算子的方案，不是已有可积系统的变量改写。
交叉比本身不唯一决定混合项格式。这里明确选择：两个 tau 同在 y=jh，
y 导数取前向差商，在格边中点配上端点算术平均。
工作在 tau 非零且可以选择光滑局部对数的区域。

## 连续起点

令 B=D_x^2+D_t+2aD_x，q=log(f/g)，r=log(fg)。有精确恒等式

\[
S=\frac{Bf\cdot g}{fg}=r_{xx}+q_x^2+q_t+2aq_x,
\]
\[
\frac{(D_yB+2\lambda D_x)f\cdot g}{fg}
=q_yS+q_{xxy}+r_{yt}+2(q_x+a)r_{xy}+2\lambda q_x.
\]

因此在 S=0 下，只需令第二式右侧最后四项之和为零。

## 对数离散势系统

记 D_+z_j=(z_{j+1}-z_j)/h，M_+z_j=(z_{j+1}+z_j)/2，
q_j=log(F_j/G_j)，r_j=log(F_jG_j)。则

\[
D_+q_j=\frac1h\log\frac{F_{j+1}G_j}{F_jG_{j+1}},\qquad
D_+r_j=\frac1h\log\frac{F_{j+1}G_{j+1}}{F_jG_j}.
\]

选择离散方程

\[
S_j=r_{j,xx}+q_{j,x}^2+q_{j,t}+2aq_{j,x}=0,
\]
\[
C_j=D_+q_{j,xx}+D_+r_{j,t}
+2(M_+q_{j,x}+a)D_+r_{j,x}+2\lambda M_+q_{j,x}=0.
\]

第二式在格边中点有二阶形式相容性。这不是数值解收敛定理。

## tau 形式：只有第一式仍是双线性

第一式为 B F_j.G_j=0。定义 X=F_{j+1}G_j、Y=F_jG_{j+1}，第二式精确等于

\[
\frac1h\left(\frac{BF_{j+1}\cdot G_j}{X}
-\frac{BF_j\cdot G_{j+1}}Y\right)
+\lambda\left(\frac{D_xF_{j+1}\cdot G_j}X
+\frac{D_xF_j\cdot G_{j+1}}Y\right)=0.
\]

乘以 hXY 得

\[
Y\,BF_{j+1}\cdot G_j-X\,BF_j\cdot G_{j+1}
+\lambda h(Y\,D_xF_{j+1}\cdot G_j+X\,D_xF_j\cdot G_{j+1})=0.
\]

这是四次 tau 关系，不能称为关于原 F,G 的 Hirota 双线性方程。
X,Y 是乘法因子，导数只作用于点号两侧；一般不能把两个不同的分母同时约去。
不排除引入更多 tau 后另行双线性化，但本次没有作出这种构造。

## 闭合非线性系统

定义节点变量 u_j=2 q_{j,x}、边变量 v_{j+1/2}=2 D_+r_{j,x}，
并写 ubar=M_+u_j。对 S 作 2D_+partial_x，对 C 作 2partial_x，得到

\[
\boxed{D_+u_{j,t}+\partial_x[(\bar u+2a)D_+u_j]+v_{j+1/2,xx}=0,}
\]
\[
\boxed{v_{j+1/2,t}+\partial_x[(\bar u+2a)v_{j+1/2}]
+D_+u_{j,xx}+2\lambda\partial_x\bar u=0.}
\]

lambda=-2 时末项为 -4 partial_x ubar。
这是局部两场半离散系统。反向重构需处理积分常数、平均模态和边界约束，
不在此声称无条件全局等价。

## 一孤子试探为何失败

取 F_j=1+A E_j、G_j=1+C E_j，E_{j+1}=R E_j、E_x=kE、E_t=omega E。
令 P=k^2+omega+2ak、Q=k^2-omega-2ak，第一式要求 AP+CQ=0。
记 T=AP=-CQ，清分母后的第二式是 K1 E+K2 E^2+K3 E^3，其中

\[
K_1=2T(R-1)+\lambda h k(A-C)(R+1),
\]
\[
K_2=T(R-1)(A+C)(R+1)+2\lambda h kR(A^2-C^2),\qquad
K_3=ACR K_1.
\]

若 R+1 非零且 K1=0，则

\[
K_2=\frac{T(A+C)(R-1)^3}{R+1}.
\]

一般非退化参数下这个系数非零。因此旧的一指数 tau 对不能直接搬来。
这不是排除所有其他孤子或其他 tau 表示的结论。

具体取 a=2、lambda=-2、A=1/12、C=1/3、k=omega=3。
消去一次项要求 R=(8-3h)/(8+3h)，但余项为

\[
-\frac{45h^3}{4(8+3h)^2}E_j^2.
\]

h=1/10 时为 -9 E_j^2/55112。归一化势方程的残差还需除以 hXY，
因此在正则有界区域这与二阶形式相容性并不矛盾。

## 能给出的显式 tau 解及验证范围

势表示 F=exp((r+q)/2)、G=exp((r-q)/2) 本身不是已经求出的通解。
一个显式背景解是

\[
q_j=k_0x-(k_0^2+2ak_0)t+\ell jh,\qquad
r_j=-2\lambda k_0jh\,t,
\qquad F_j=e^{(r_j+q_j)/2},\quad G_j=e^{(r_j-q_j)/2}.
\]

它对应 u=2k0、v=0，只是常数背景，不是孤子。
本次没有构造出新模型的非平凡 N 孤子 tau 族。

运行 verify_log_scheme.py（需 SymPy）可复核：连续势恒等式、tau 交叉表达、
闭合非线性系统、具体一孤子非零残差、显式背景解。均为符号恒等检验。
本方案可作为二阶相容的非线性差分模型研究，但不是已建立的可积双线性离散化。
