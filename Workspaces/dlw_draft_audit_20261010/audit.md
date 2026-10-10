# DLW 论文草稿：推导与适用范围审查

审查对象：[dlw_paper_draft.html](dlw_paper_draft.html)。审查日期：2026 年 10 月 10 日。下文括号中的原式编号均指该稿。

**结论。** 第 1—6 节的主代数链成立：连续双线性表示、交错构造、任意有限阶 Gram 恒等式、正则谱域、PE/PF 非线性化、二阶一致性与固定谱连续极限，以及带非退化条件的形式 Lax 相容性，均未发现推翻命题的错误。需要修改的是数值部分的条件和可复现说明：补充高频增长分支；写明 PF 初始化的端点跳跃未知量；区分半离散守恒律与实际网格算法；补证算例 B/C 的正则性。这些问题不使现有孤子恒等式失效，但影响读者如何解释数值比较。

| 程度 | 位置 | 审查意见 |
|---|---|---|
| P2 | 第 5、7、8 节及结论 | 缺少连续系统和 PE 的高频增长分析；一致性与精确解极限不能作为一般数值收敛依据。 |
| P2 | 第 7.1 节 PF 初始化、原式（56）、（60）后 | 当前文字未给出实际使用的增广端点跳跃问题；仅按普通中心差分与一个归一化条件不能复现初始化。 |
| P2 | 第 7.2 节、原式（65）—（70） | 守恒律在连续 $x$ 的 PE/PF 层面成立；实际差分及 FD 存在明确缺陷项，不能据此声称节点保持精确等质量。 |
| P3 | 第 8.1 节与命题 3.3、定理 5.3 | B/C 不在已证明的正则谱域内，需要独立正性证明或扩展定理。实际参数可补证，不是奇异反例。 |
| P3 | 第 7.3、8.4 节 | 固定隐式残差容差不保证细化时间步时仍测得二阶；总误差接近也不能证明时间阶。当前百分比陈述本身成立。 |

## 1　连续双线性表示的独立推导

令

$$r=\log(f/g),\qquad b=\log(fg),\qquad u=2r_x,\quad v=2b_{xy}.$$

在 $f,g>0$ 的区域，直接展开 Hirota 算子，有

$$E:=\frac{B_af\cdot g}{fg}=b_{xx}+r_x^2+r_t+2ar_x,$$

$$\frac{(D_yB_a-4D_x)f\cdot g}{fg}=H+r_yE,
\qquad H=b_{yt}+r_{xxy}+2(r_x+a)b_{xy}-4r_x.$$

第二式中的 $r_yE$ 不能在一般恒等式中遗漏；只有结合第一条双线性方程才能消去它。进一步求导得到原 DLW 两个残差的精确表达

$$u_{yt}+v_{xx}+[(u+2a)u_y]_x=2E_{xy},$$

$$v_t+u_{xxy}+[(u+2a)v-4u]_x=2H_x.$$

因此 $E=H=0$ 确实推出原式（1）。这也独立核对了常数 $-4u$、平移 $2a$ 及时间项的符号。反向只由物理场方程得到 $E_{xy}=H_x=0$，仍有积分函数；稿件只声称双线性解产生 DLW 解，范围正确。

由乘积微分

$$\partial_y(B_af\cdot g)=B_af_y\cdot g+B_af\cdot g_y,$$

$$D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y,$$

在第一条双线性方程成立时，第二条恰好等价于

$$B_af\cdot g_y+2D_xf\cdot g=0.$$

原式（4）的正号与系数 2 正确。

## 2　交错离散与命题 2.1

固定第一因子，设

$$\Phi(s)=B_{a+s}f(y)\cdot g(y+s).$$

这里 $s$ 同时平移第二因子的坐标和算子参数，并非同时平移两个因子。其导数为

$$\Phi^{(m)}(0)=B_af\cdot\partial_y^m g+2mD_xf\cdot\partial_y^{m-1}g\quad(m\ge1).$$

由中心 Taylor 展开，

$$\frac{\Phi(d)+\Phi(-d)}2=\Phi(0)+\frac{h^2}{8}\Phi''(0)+O_K(h^4),$$

$$\frac{\Phi(d)-\Phi(-d)}h=\Phi'(0)+\frac{h^2}{24}\Phi'''(0)+O_K(h^4),\qquad d=h/2.$$

这逐项给出原式（6）及其证明中的误差系数。平均与差商分别趋于两条连续双线性关系；单条格点关系本身不应被称为对同一条连续方程的二阶近似。稿件当前采用平均／差商表述，正确。

条件方面，紧集必须有一个允许左右移位的共同开邻域；原文已明确。实解析性强于所需，只要涉及的有限阶混合导数有界即可。这是可精简条件，不构成错误。

## 3　Gram 恒等式、正则域与算例参数

### 3.1　任意阶恒等式

写第 $n$ 层矩阵为

$$M=I+\left[\frac{r_ic_k}{p_i+q_k}\right],\quad
r_x=Pr,\ r_t=-P^2r,\ c_x=Qc,\ c_t=Q^2c.$$

取 $b=(Q+sI)^{-1}c$，则

$$M_x=rc^{\mathsf T},\quad M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,
\quad M_{n+1}=M-rb^{\mathsf T},\quad b_x=c-sb.$$

第三式来自

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s},$$

其中单位矩阵不发生辅助层缩放，这是秩一更新成立的关键。令 $H=M^{-1}$、$z=Hr$，并定义

$$\kappa=c^{\mathsf T}z,\quad \zeta=b^{\mathsf T}z,\quad
\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,
\quad\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.$$

由逆矩阵微分与行列式引理得到

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}$$

独立消元给出

$$\zeta_{xx}+\zeta_t+2s\zeta_x=2\kappa_x(1-\zeta).$$

因此 $\psi=\tau_{n+1}/\tau_n=1-\zeta$ 满足

$$\psi_t+\psi_{xx}+2s\psi_x+2\kappa_x\psi=0.$$

而对 $f=\psi g$，

$$B_sf\cdot g=g^2\left[\psi_t+\psi_{xx}+2s\psi_x+2(\log g)_{xx}\psi\right].$$

于是得到原式（9）。以上等式不依赖 $N=1,2$，是一般有限阶证明。

对于不可逆的 $M$，将所有权重改为 $\varepsilon\rho_i$。在固定 $x,t,j$ 下，$M(0)=I$，双线性残差关于 $\varepsilon$ 是多项式；它在零附近为零，因而恒为零。此延拓无需假设 $\tau_n$ 始终非零。注意：延拓的是双线性恒等式，含对数的物理场仍需另行保证正性。

最后设 $z=p_i-a, w=q_k+a$，直接约分得

$$-\frac{z-d}{w+d}\frac{z+d}{z-d}\frac{w+d}{w-d}
=-\frac{z+d}{w-d}.$$

故 $\tau_1(j;a-d)=\tau_1(j+1;a+d)$，同一相邻层恒等式给出两条交错方程。定理 3.1 的非零条件足以支持这里所有除法及负整数格点幂。

补充核验采用独立的主子式展开，对 $N=1,2,3,4$、$j=-2,0,3$、相邻层 $n=0,1,2$ 及两种 $s=a\pm h/2$ 逐指数系数做精确有理数计算；同时检查跨格点方程，全部残差为零。这是对证明的计算交叉核验，不以有限个 $N$ 代替一般证明。

### 3.2　命题 3.3 的正性

任意递增行指标 $i_1<\cdots<i_m$ 和列指标 $k_1<\cdots<k_m$ 对应的 Cauchy 子式为

$$\det\left[\frac1{p_{i_r}+q_{k_s}}\right]
=\frac{\prod_{r<s}(p_{i_s}-p_{i_r})(q_{k_s}-q_{k_r})}
{\prod_{r,s}(p_{i_r}+q_{k_s})}>0.$$

在 $0<p_1<\cdots<p_N<a-d$、$0<q_1<\cdots<q_N$ 下，所有格点乘子及取层因子为正，因此 Gram 矩阵为 $I+D_1CD_2$，其中两个对角矩阵均正。展开

$$\det(I+A)=\sum_{I\subseteq\{1,\ldots,N\}}\det A_{I,I}$$

即得 $\tau\ge1$。故 $F,G>0$，对数场在所有有限 $x,t,j$ 处光滑。这里“全局正则”不等于关于全空间时间的一致有界性，也不是任意初值问题的全局适定性。

### 3.3　B/C 算例需要补证，但确实正则

算例 A 满足命题 3.3；B 的 $p=4,q=-3,a=2$，C 的 $p=(6,4),q=(-5,-3),a=2$ 不满足该命题。故正文不能直接援引它来覆盖全部实验参数；定理 5.3 的字面范围也不包括 B/C。

令每组相位为

$$\theta_i=(p_i+q_i)x+(q_i^2-p_i^2)t+
y\left(\frac1{p_i-a}+\frac1{q_i+a}\right).$$

对 B，直接展开连续行列式得

$$g=1+e^\theta,\qquad f=1+2e^\theta.$$

对 C，Cauchy 矩阵与两个行取层因子的乘积分别给出

$$C=\begin{pmatrix}1&1/3\\-1&1\end{pmatrix},\quad
\det C=4/3,\quad\gamma_1=4/3,\quad\gamma_2=2,$$

$$g=1+e^{\theta_1}+e^{\theta_2}+\frac43e^{\theta_1+\theta_2},$$

$$f=1+\frac43e^{\theta_1}+2e^{\theta_2}+\frac{32}{9}e^{\theta_1+\theta_2}.$$

各系数均正，故两组连续基准都全局非奇异。相应有限格距族在 $0<h<2$ 时，所有单独乘子 $\lambda_h(p_i-a),\lambda_h(q_i+a)$ 和取层因子仍为正，所有主子式系数也为正；当前 $h=0.125$ 在此范围内。定理 5.3 的同一证明可据此扩展到这两组固定谱数据。建议将这段简短核验加在参数表之后；无需把 B/C 错判为非法参数。

## 4　从双线性方程到 PE 与 PF

### 4.1　共同对数势

写 $\alpha_j=\log F_j, \beta_j=\log G_j$，则

$$u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,
\quad\omega_j=(\beta_{j+1}-\beta_j)_x,
\quad Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.$$

对原式（22）相加后求 $x$ 导数，平方项之和为 $(u_j^2+\omega_j^2)/2$，参数项之和为 $2au_j-h\omega_j$，从而

$$u_{j,t}+\partial_x\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}=0.$$

两式相减后求导，平方项之差为 $u_j\omega_j$，二阶对数项之差为 $-\omega_{j,x}$，得到

$$\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}=0.$$

原式（25）的扩散符号正确。

### 4.2　PE 消元与等价性

由 $Z_j-u_j=2(\beta_j+\beta_{j+1})_x$，

$$\delta_-Z_j=\delta_-u_j+\frac4hM_-\omega_j.$$

令 $W=4\omega/h=v-\delta_0u$，以及

$$\mathcal A=\frac{u^2}2+2au+h^2\left(\frac{W^2}{32}-\frac W4\right),$$

共同方程变为

$$\delta_-u_t+\partial_x\delta_-\mathcal A+
\partial_x^2(\delta_-u+M_-W)=0,$$

$$W_t+[(u+2a)W-4u]_x-W_{xx}=0.$$

使用恒等式

$$\delta_--M_-\delta_0=-\frac{h^2}4\Delta_h\delta_-,\quad
M_+\delta_-=\delta_0,\quad M_+M_-=1+\frac{h^2}4\Delta_h,$$

第一式化为原式（26）第一条；对第一式作 $M_+$ 平均，再加第二式，二阶 $x$ 导数部分为

$$\partial_x^2\left[\delta_0u+M_+M_-W-W\right]
=\partial_x^2\left[\delta_0u+\frac{h^2}4\Delta_hW\right],$$

即原式（26）第二条。反向相减即可恢复 $W$ 方程，故原式（26）与（27）确实等价。

但对 $u_t$ 作过格点差分后，$y$ 向共同模态不再由内点方程单独确定。PE 初边值问题需要下边界或其他均值规范，稿件原式（57）已经提供下边界。PE 与原双线性对之间没有据此得到无条件双向等价；稿件也没有作此声明。

### 4.3　PF 与时间规范

定义

$$M_j=\beta_{j,x},\quad Q_j=\frac{F_j}{\sqrt{G_jG_{j+1}}},\quad
R_j=\frac{1-\omega_j/h}{Q_j}.$$

于是 $u=2Q_x/Q, \omega=h(1-QR),\ M_{j+1}-M_j=h(1-QR)$。恒等式

$$u_x+u^2/2=2Q_{xx}/Q$$

将第一场方程化成

$$\partial_x\left[\frac{Q_t+Q_{xx}+2aQ_x}{Q}
+(M_j+M_{j+1})_x+\frac{h^2}{4}(Q^2R^2-1)\right]=0.$$

单独积分只能得到一个 $c_j(t)$。对于稿件给定的精确 τ 比值，方括号等于原式（22）的 $(A_j+C_j)/2$，因而确为零。这一理由充分，原式（32）到（33）没有非法丢掉积分常数。

记

$$K_j=(M_j+M_{j+1})_x+\frac{h^2}4(Q_j^2R_j^2-1).$$

将 $\omega=h(1-QR)$ 代入第二场方程，得到

$$0=(QR)_t-(QR)_{xx}+2a(QR)_x+2(Q_xR)_x$$

$$\phantom{0}=R(Q_t+Q_{xx}+2aQ_x)+Q(R_t-R_{xx}+2aR_x).$$

结合 $Q_t+Q_{xx}+2aQ_x=-KQ$，并用 $Q>0$ 除法，得到

$$Q_t+Q_{xx}+2aQ_x+KQ=0,\qquad
R_t-R_{xx}+2aR_x-KR=0.$$

这证明原式（39）。推导不要求 $R>0$，也不要求 $QR>0$；后者是某些网格或反向 Lax 论证的额外条件，不能从 $Q>0$ 推出。

命题 4.2 只比较“同一正 τ 对”恢复的物理场，成立。对任意 PF 数值解，若作 $Q\mapsto e^{c(t)}Q, R\mapsto e^{-c(t)}R$，物理场及 Lax 系数保持不变，但 PF 残差增加 $c'Q,-c'R$。因此物理场等价不自动固定势的时间规范；稿件数值下边界实际承担了规范选择。

## 5　二阶一致性与精确解连续极限

### 5.1　命题 5.1 的主误差项

设 $A_0=u^2/2+2au, W_0=v-u_y, A_2=W_0^2/32-W_0/4$。在第一条方程的中点 $m=y-h/2$ 展开，可将原式（41）加强写成

$$\mathcal N_{1,h}=\mathcal C_1+h^2\left[
\frac{u_{yyyt}}{24}+\partial_x\left(\frac{(A_0)_{yyy}}{24}+(A_2)_y\right)
+\partial_x^2\left(\frac{v_{yy}}8-\frac{u_{yyy}}4\right)\right]+O_K(h^4).$$

该式所有连续量均在 $m$ 评价。第二条在物理半格点 $y$ 展开，得到

$$\mathcal N_{2,h}=\mathcal C_2+h^2\left[
\partial_x\left(\frac12u_yu_{yy}+(A_2)_y\right)
+\partial_x^2\left(\frac{v_{yy}}4-\frac{u_{yyy}}{12}\right)\right]+O_K(h^4).$$

其中用到

$$\frac{(A_0)_{yyy}-(u+2a)u_{yyy}}6=\frac12u_yu_{yy}.$$

因此两式的二阶一致性正确，且第一条必须在后移半格点比较。若将第一条直接与 $y$ 处连续方程比较，任意测试场通常会出现一阶位置误差；原命题已正确区分评价点。

### 5.2　命题 5.2 的场重构

令 $\alpha=\log f, \beta=\log g, u=2(\alpha-\beta)_x$。半格点 Taylor 展开给出

$$u^{[h]}=u-\frac{h^2}4\beta_{xyy}+O_K(h^4),\qquad
\frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}6\beta_{xyyy}+O_K(h^4).$$

还必须对 $u^{[h]}$ 本身取中心差分，不能只使用其零阶误差界。保留导数展开得

$$\delta_0u^{[h]}=u_y+h^2\left(\frac{u_{yyy}}6-\frac{\beta_{xyyy}}4\right)+O_K(h^4),$$

$$v^{[h]}=2(\alpha+\beta)_{xy}
+h^2\left(\frac{u_{yyy}}6-\frac{\beta_{xyyy}}{12}\right)+O_K(h^4).$$

所以原式（42）成立。紧邻域上的严格正性保证对数导数有界；只知道某些孤立采样点非零不足以支持该结论。

### 5.3　定理 5.3：一阶项为什么消失

固定 $N,p_i,q_i,\rho_i,a$，令 $z_i=p_i-a, w_k=q_k+a$。在谱点与零、乘子极点保持固定距离时，

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4).$$

因此相位的 $y$ 系数只有偶次修正。更重要的是，$F_j$ 位于半格点；对实数 $y$ 定义 $f^{(h)}(y)=\tau_1(y/h-1/2;a-h/2)$ 后，振幅为

$$-\frac{z+d}{w-d}\bigl(\lambda_h(z)\lambda_h(w)\bigr)^{-1/2}
=-\frac zw\sqrt{\frac{1-d^2/z^2}{1-d^2/w^2}}.$$

右端等号使用正平方根分支以及定理中的 $z<0<w$。若忽略半格点移位，只展开 $-(z+d)/(w-d)$，会错误地产生一阶振幅误差。稿件将两项合并处理，正确。

有限阶行列式是矩阵元的多项式；所有固定阶 $x,y,t$ 导数都以 $O_K(h^2)$ 收敛。正性下界使该估计传递到对数导数，统一导数界又允许对随 $h$ 变化的函数族使用第 5.2 节重构展开。因此原式（44）成立。

连续双线性方程也必须证明，而非只由相位的形式极限猜测。精确离散方程对实数插值成立；取平均和差商并用共同导数界令 $h\to0$，分别得到 $B_af^{(0)}\cdot g^{(0)}=0$ 及原式（4）。这一极限论证完整。

**结论范围。** 定理覆盖固定谱、固定有限 $N$、固定紧集上的精确解族。它不覆盖 $p_i-a\to0$ 的随 $h$ 变谱、$N\to\infty$、扩大到无界区域的一致误差，也不证明任意离散初值解或 Euler/RK4/C–N 的收敛性。

## 6　Lax 相容性及其非退化条件

### 6.1　辅助势的可构造性

以 $U=u+2a, w=W-4$ 记

$$F_j=U_{j,t}+\partial_x(U_j^2/2+h^2w_j^2/32).$$

此处 $F_j$ 只是本段残差记号，不指原 τ 函数。势方程为

$$V_{j,x}=-\frac12(F_j+U_{j,xx}+\tfrac h2w_{j,xx}),\qquad
V_{j+1}-V_j=\tfrac h2w_{j,x}.$$

取后向差分，第二式给出 $\delta_-V_{j,x}=w_{j-1,xx}/2$。代入第一式即得

$$\delta_-F_j+\partial_x^2(\delta_-U_j+M_-w_j)=0.$$

故 PE 第一式正是势方程的局部相容条件。在一个 $x$ 区间和开格点链上，参考格点积分后递推即可，剩余自由度为共同的 $c(t)$。若改为周期格点链，还需闭合条件 $\sum_jw_{j,x}=0$；若要求 $x$ 周期势，还需相应积分条件。稿件明确只讨论局部区间／格点链，没有越过这一范围。

### 6.2　交织恒等式与反向推导

定义 $\alpha=U/2+hw/8, \eta=U/2-hw/8$，以及

$$E^\alpha=\alpha_t+\alpha_{xx}+2\alpha\alpha_x+V_{j,x},\qquad
E^\eta=\eta_t+\eta_{xx}+2\eta\eta_x+V_{j+1,x}.$$

直接计算得到

$$E^\alpha-E^\eta=\frac h4[w_t-w_{xx}+(Uw)_x],$$

$$E^\alpha+E^\eta=F+U_{xx}+\frac h2w_{xx}+2V_x.$$

这重新得到原式（51）。再对任意测试函数展开

$$ (\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)
=-(r_t+r_{xx}+2rr_x+V_x).$$

当两项残差为零时，共同中间势为 $V_j+2\alpha_x=V_{j+1}+2\eta_x$。令 $A=\partial_x-\alpha, B=\partial_x-\eta, T=B^{-1}A$，消去中间势即得原式（49），证明正向相容性。

反向有精确算子恒等式

$$B(T_t-\mathscr Q_{j+1}T+T\mathscr Q_j)=-E^\alpha+E^\eta T,$$

$$T=I-B^{-1}\frac{hw}4
=I-\frac{hw}4\partial_x^{-1}+O(\partial_x^{-2}).$$

先比较零次系数，得 $E^\alpha=E^\eta$；再比较负一次系数，得 $wE^\eta=0$。在 $w\ne0$ 的区域，两残差都为零，进而恢复两条 PE 方程。这里是在形式伪微分算子代数中求逆，不是已证明某个边值算子 $B$ 可逆。

非退化条件确实必要。例如在一个至少含三个格点的局部链上取 $w_j=0, V_j=0, U_j=jx$，则 $A_j=B_j$、$T_j=I$，形式 Lax 条件恒成立；但 PE 第一式含 $(2j-1)x/h$，一般不为零。稿件已排除这一退化情形。

对于 τ 解，$V_j=2(\log G_j)_{xx}$ 使 Riccati 残差等于相应对数双线性残差的 $x$ 导数；常数 $a\mp h/2$ 的符号也正确。

### 6.3　PF 的线性问题

代入 $U=2Q_x/Q+2a, w=-4QR, V=2M_x$，立即得到原式（55）。PF 约束给出势差，PF 演化给出 Riccati 残差为零。反向在 $QR\ne0$ 时恢复的是 PE 物理场方程；它不能自动恢复 PF 的时间规范。原文最后一句使用“恢复 PE 的物理场方程”，范围准确。

这一节证成的是形式 Darboux–Lax 相容性，未建立周期谱理论或刘维尔可积性；不应将它扩写成这些更强结论。

## 7　需要补入的高频分析

在零背景 $u=v=0$ 附近，取连续扰动 $e^{\sigma t+ikx+i\ell y}$，其中 $\ell\ne0$。线性化原式（1）得到

$$\begin{pmatrix}
i\ell(\sigma+2aik)&-k^2\\
-i(k^2\ell+4k)&\sigma+2aik
\end{pmatrix}\binom{\widehat u}{\widehat v}=0,$$

故

$$\boxed{(\sigma+2aik)^2=k^4+\frac{4k^3}{\ell}.}$$

对固定正 $\ell$ 和 $k\to+\infty$，存在 $\operatorname{Re}\sigma\sim k^2>0$ 的分支。平移 $2a$ 只改变虚部，不能抑制增长。该线性流不能在通常各向同性 Sobolev 范数中具有对任意高频扰动统一的有限时连续依赖估计。

对 PE，取 $u,W\propto e^{\sigma t+ikx+ij\theta}$，$\theta\not\equiv0\pmod{2\pi}$。利用

$$\frac{M_-}{\delta_-}=\frac{h}{2i}\cot(\theta/2),$$

将第一式除以 $\delta_-$ 的符号，得

$$\begin{pmatrix}
s-k^2&i[-kh^2/4+k^2h\cot(\theta/2)/2]\\
-4ik&s+k^2
\end{pmatrix}\binom{\widehat u}{\widehat W}=0,
\qquad s=\sigma+2aik.$$

因此

$$\boxed{(\sigma+2aik)^2=k^4-k^2h^2+2k^3h\cot(\theta/2).}$$

令 $\theta=\ell h$，它趋于连续色散关系。固定非零格点波数时，大 $k$ 同样有增长分支；在 $\theta=\pi$ 时，根号内为 $k^2(k^2-h^2)$，$k>h$ 已有正增长。这里没有把真实方程的增长分支误判为差分符号错误。

进一步取正文的 $x$ 中心差分，在周期网格上，若 $x$ 模态为 $e^{ii\kappa}$，令

$$\widehat k=\frac{\sin\kappa}{\Delta x},\qquad
K_2=\frac{4\sin^2(\kappa/2)}{\Delta x^2},$$

相应特征关系为

$$(\sigma+2ai\widehat k)^2=K_2^2-h^2\widehat k^2
+2h\widehat kK_2\cot(\theta/2).$$

特别在 $x$ Nyquist 模态 $\kappa=\pi$，存在 $\sigma=+4/\Delta x^2$。因此减小时间步并不能消除这一空间增长分支，空间加密也可能加快小扰动放大。该 Fourier 分析针对无限／周期均匀网格的线性化；它并未计算本文有限 $y$ 边界算子的完整谱或确定某次实验的失效时刻。

**建议补写。** “以下结果限于指定解析孤子、分辨率及 $T=0.01$ 的短时计算。连续系统及 PE 线性化存在高频增长分支；二阶一致性与精确 Gram 解族的连续极限不构成一般初值数值收敛定理。”这是当前理论与数值结果之间最重要的范围说明。

## 8　PF 初始化与边界的实际离散问题

正文称由 $D_1Q=u_*Q/2$ 和 $Q_0=1$ 确定初始 $Q$，但未列出端点如何进入 $D_1$。中心差分是二步递推，单个左端归一化不能替代边界闭合；若误用 PE/FD 的周期矩阵，甚至可能没有正解。

例如算例 B 的 $u_*>0$。若 $D_1$ 是周期中心差分且 $Q>0$，对各节点求和将得到

$$0=\sum_i(D_1Q)_i=\frac12\sum_i u_{*,i}Q_i>0,$$

矛盾。因此端点条件是数学构造的一部分。

Notebook 实际增加了跳跃未知量 $\chi$，令 $Q(x+L)=Q(x)+\chi$，并求解

$$\begin{pmatrix}
D_\xi-\tfrac12\operatorname{diag}(Ju_*)&b\\
e_0^{\mathsf T}&0
\end{pmatrix}
\binom{Q}{\chi}=\binom{0}{1},\qquad
b=\frac{e_0+e_{N_x-1}}{2\Delta\xi}.$$

这里 $J$ 为网格 Jacobian；固定网格 $J=1$。正文应同时写明该矩阵可逆、$Q_i>0$ 和 $1+\chi>0$ 为实施条件。代码逐次检查正性，但没有证明任意数据下可逆／保正。

当前代码还按最下层边界更新各层的右端比值。若 $b_j=1+\chi_j(0)$、$b_0(t)=1+\chi_0(t)$，它使用

$$b_j(t)=b_j\frac{b_0(t)}{b_0(0)},\qquad
\chi_{Q,j}=b_j(t)-1,\quad\chi_{R,j}=b_j(t)^{-1}-1.$$

这比“按左右端背景值处理边界”具体得多，建议写入可复现说明。

重新执行当前 Notebook 的定义和初始化得到：三算例各三方法共九组的初始场最大差不超过 $1.77\times10^{-13}$，支持“共同初始物理场”的陈述。PF 最下层跳跃约为 A 的 $-0.7492$、B 的 $0.9999$、C 的 $1.6663$；去掉跳跃后，初始化方程的最大残差分别约为 2.40、3.20、5.33；保留增广项则为 $1.7\times10^{-15}$ 以内。可见缺失的条件并非可忽略的尾部修正。

原式（62）本身代数正确：由 $m_1=m_0-hD_1(QR)_0$ 代入边界 $Q$ 方程，立即得到其 $m_0$ 表达。在动网格上必须区分物质导数和固定物理坐标导数。代码对增广线性系统求导，含 $J_t=D_\xi\mathcal V$ 及 $\dot u=u_t+\mathcal V u_x$，随后用 $Q_t=\dot Q-\mathcal V D_1Q$。只使用解析 $u_t$ 而不对离散提升求导，不能复现这一边界。

## 9　守恒密度、FD 缺陷与网格条件

### 9.1　连续 $x$ 的 PE/PF 层面

由 $W_t+[(u+2a)W-4u]_x-W_{xx}=0$，令

$$\rho=1-W/4,\qquad q=(u+2a)\rho-\rho_x-2a,$$

直接代入得 $\rho_t+q_x=0$。PF 中 $\rho=QR$，两势方程相乘相加也得到同一关系。原式（65）、（66）的系数及符号正确。

有限个固定 $y$ 层取等权平均仍满足 $\bar\rho_t+\bar q_x=0$。左端固定时，

$$\frac d{dt}\int_{x_L}^{x_i(t)}\bar\rho\,dx
=-\bar q(x_i)+\bar q(x_L)+\bar\rho(x_i)\dot x_i,$$

故原式（69）确为保持累积质量的速度。条件是密度光滑、$\bar\rho>0$、坐标映射可逆；若左右端都固定，还需两端通量相等。只要求 $Q>0$ 不保证 $\bar\rho>0$。

### 9.2　FD 即使只离散 $y$，也已有源项

设 FD 的 $x$ 暂保持连续，仍按原式（64）的 $y$ 算子定义 $W=v-\delta_0u$。在内部层消去 $u_t$，使用 $M_+M_-=1+h^2\Delta_h/4$，得到

$$W_t+[(u+2a)W-4u]_x-W_{xx}
=\frac{h^2}2\partial_x[(\delta_0u)(\Delta_hu)]
+\frac{h^2}4\partial_x^2\Delta_hv.$$

原因是离散乘积恒等式

$$\delta_0(u^2/2+2au)-(u+2a)\delta_0u
=\frac{h^2}2(\delta_0u)(\Delta_hu).$$

因此 FD 的相同 $\rho,q$ 满足的是

$$\rho_t+q_x=-\frac{h^2}8\partial_x[(\delta_0u)(\Delta_hu)]
-\frac{h^2}{16}\partial_x^2\Delta_hv,$$

一般不为零。FD 采用同一个速度可以作为一致的网格监测规则，但不能直接继承 PE/PF 的精确等质量推导。光滑有界导数下这里的缺陷为二阶，这不否定 FD 的一致性。

### 9.3　实际 $x$ 差分也不精确保持所写通量关系

对于固定均匀网格上的 PE，代码给出

$$\dot\rho=-D_1[(u+2a)\rho-2a]+D_2\rho.$$

若网格通量取正文的 $q_h=(u+2a)\rho-D_1\rho-2a$，则

$$\boxed{\dot\rho+D_1q_h=(D_2-D_1^2)\rho
=-\frac{\Delta x^2}4D_2^2\rho.}$$

末个恒等式适用于周期均匀三点差分；它在光滑场上为二阶缺陷，但有限格距下一般不为零。当前初始化的最大节点缺陷，A/B/C 分别约为 0.2383、$7.49\times10^{-4}$、$1.47\times10^{-3}$，与右端预测相差不超过 $2.4\times10^{-14}$。另一方面周期节点总质量的时间导数约为 $10^{-15}$，所以应精确区分“原节点通量恒等式失效”和“总质量不守恒”；后者不能由前者推出。

PF 的离散 $QR$ 方程还涉及中心差分不满足连续乘积法则；动网格中 $D_1,D_2$ 又含变化的 Jacobian。因此原式（68）是半离散模型的网格设计依据，尚不是所实施算法的离散质量定理。

**建议措辞。** 将三方法共同的描述改为“以 PE/PF 半离散守恒密度构造监测函数，采用相应速度的差分近似；FD 使用同一监测规则”。保留已经计算的误差降幅，但不要称三种全离散实现都严格保持累积质量。

### 9.4　坐标导数与保正条件

对于 $x=x(\xi,t)$、$J=x_\xi>0$，

$$\partial_x=J^{-1}\partial_\xi,\qquad
\partial_{xx}=J^{-2}\partial_{\xi\xi}-J^{-3}J_\xi\partial_\xi,$$

$$\dot z=z_t+\mathcal V z_x.$$

原式（70）和 ALE 输运项的符号正确；所有层共用同一 $x$ 网格，故层差分与移动坐标的时间导数可按正文处理。数值实施还需检查离散 $J_i>0$ 与节点不交叉；代码做了这两项检查。密度正性本身并不能替代离散网格检查，也不是任意时间积分的保正定理。

## 10　时间离散、误差表与结论边界

Euler、RK4 和原式（72）的隐式梯形关系写法正确。这里 C–N 使用端点右端的平均，不是把非线性右端在平均状态处求值，两者一般不同。

代码以 Euler 预测值 $z^{(0)}=z^n+\Delta t\mathcal F(t_n,z^n)$ 开始，执行

$$r^{(k)}=z^{(k)}-z^n-\frac{\Delta t}2
[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{(k)})],\qquad
z^{(k+1)}=z^{(k)}-r^{(k)}.$$

这是 Picard 迭代，不是 Newton 迭代；其收敛需另有局部条件。正文只称“迭代”，没有名称错误，但应说明容差决定了多准确地实现式（72）。

在固定终止时间且有适当传播估计时，逐步状态残差 $\varepsilon$ 可累积为 $O(\varepsilon/\Delta t)$。要使代数误差不超过二阶时间误差，通常需将残差控制到 $O(\Delta t^3)$ 或更小，而非始终固定 $10^{-11}$ 量级。实际放大还取决于问题稳定性。

用当前代码处理标量 $z'=z, z(0)=1, \Delta t=10^{-6}$，Euler 预测的隐式残差为 $5.00\times10^{-13}$，低于 $1.10\times10^{-11}$ 的阈值；代码第一次检查即接受 $1.000001$，而精确 C–N 值为 $1.0000010000005$。这是容差限制的具体例子，不表示正文默认步长下所有 PDE 步都被退化为 Euler。

第 8 节的比较措辞已经限定为三算例和固定配置。按表内值复算，PF/PE 的 $u$ 误差比约为 7.61、1.91、2.02；RK4 与 C–N 的最大相对差异约为 0.00277%；十八项动网格误差降幅约为 16.21%—66.83%，与摘要的舍入数值一致。

这些数值支持所列配置的误差比较，不单独支持一般空间／时间收敛阶、长时可靠性或普遍优势。PE 与 PF 的边界闭合不同，且非线性离散不保持连续乘积法则，因此观察到的误差差异应归于完整实现，不能仅归因于两种等价表示的“固有精度”。固定／动网格比较同时改变初始布点和后续节点运动；正文当前将两者合并描述，正确，尚不能从该表分离纯运动收益。

## 11　建议修改清单与核验材料

建议保留第 1—6 节的主公式和证明。优先在数值方法前加入第 7 节所列高频增长分析及短时适用范围；在 PF 初始化处加入增广跳跃系统和边界规范；将“守恒密度驱动”明确为监测函数设计来源，并区分 FD 与实际全离散缺陷。随后补入 B/C 正性计算和 C–N 容差说明。以上修改都无需改变现有误差表。

本次直接抽取 HTML 中全部 590 个 TeX 表达，与正文源逐项一致核对；所有 75 个编号公式均纳入逐节推导。独立符号程序与补充核验共完成 2,423 项精确零残差检查，包含上述 Taylor 主误差项与色散多项式，另执行当前 Notebook 的九组初始化、PE 连续性缺陷测量和 C–N 标量反例。没有重新演化整批 PDE 轨道，因此本次对误差表的核验是数值比值与陈述范围检查，不是再次复现全部终值。

原稿与 Notebook 保持不变。[独立核验程序](../Workspaces/dlw_draft_audit_20261010/verify.py)、[符号结果](../Workspaces/dlw_draft_audit_20261010/verification.json)、[补充核验](../Workspaces/dlw_draft_audit_20261010/supplement.json)、[数值探针](../Workspaces/dlw_draft_audit_20261010/numerical_probe.py)、[数值探针结果](../Workspaces/dlw_draft_audit_20261010/numerical_probe.json)及[审查时正文快照](../Workspaces/dlw_draft_audit_20261010/reviewed_source.md)附后，可用于后续修订复核。
