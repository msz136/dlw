# GSG、2HS 与 DLW 数值结果

<nav aria-label="报告目录"><a href="#gsg">一、GSG</a><a href="#hs">二、2HS</a><a href="#dlw">三、DLW</a><a href="#results">误差比较</a><a href="#waveforms">2HS 波形图</a><a href="#dlw-figures">DLW 波形图</a><a href="#time">时间算法</a><a href="#density">动网格对照</a><a href="#hs-equations">离散方程</a><a href="#sources">参考资料</a></nav>

<h2 id="gsg">一、GSG：五种 Scheme 的指标与结果</h2>

先认清这五个编号：

| 编号 | 方程＋网格＋时间算法 |
|---|---|
| **Scheme 1** | **可积半离散式Ⅰ＋自适应动网格＋一阶 Euler 型更新** |
| **Scheme 2** | **可积半离散式Ⅱ＋自适应动网格＋一阶 Euler 型更新** |
| **Scheme 3** | **普通差分＋自适应动网格＋显式 Euler** |
| **Scheme 4** | **普通差分＋自适应动网格＋预测校正**，空间方程与 Scheme 3 相同 |
| **Scheme 5** | **普通差分＋均匀固定网格＋Crank–Nicolson（C–N）** |

**Scheme 1、2 都是动网格**，区别在于两套可积半离散方程，不是一个动网格、一个均匀网格。Scheme 3、4 主要区别是时间算法；只有 Scheme 5 使用均匀固定网格。这里的自适应密度来自 GSG 自身的守恒律。

### 五种方法的误差有多大

下表逐一列出 **Scheme 1–5 在 $t=5$ 的结果**。规则 kink 取 $p_1=0.8/\sqrt2$，不规则 kink 取 $p_1=0.9$，环孤子取 $p_1=2$。

**数值是从原文图 2、3、6、7、8 读取的近似峰值，不是论文提供的原始数据。** $u$ 误差和坐标 $x$ 误差分开列；“未给出”表示原文没有相应误差曲线，不表示误差为零。

| 方法 | 规则 kink：$u$ 误差峰值 | 不规则 kink：$u$ 误差峰值 | 环孤子：$u$ 误差峰值 | 坐标 $x$ 误差峰值 | 来源 |
|---|---:|---:|---:|---|---|
| **Scheme 1**<br>可积Ⅰ·动格·Euler | 约 $0.31$ | 约 $0.051$ | 约 $0.005$–$0.006$ | 未给出 | 图 2(a–c) |
| **Scheme 2**<br>可积Ⅱ·动格·Euler | 未给出独立误差曲线；波形有明显偏移 | 未展示 | 未展示 | 规则 kink 约 **$1.5$** | 图 3(a–b) |
| **Scheme 3**<br>差分·动格·Euler | 约 $0.29$ | 约 $0.032$ | 约 $0.008$–$0.009$ | 未给出 | 图 6(a–c) |
| **Scheme 4**<br>差分·动格·预测校正 | 约 $0.50$ | 约 $0.092$ | 约 $0.058$ | 未给出 | 图 7(a–c) |
| **Scheme 5**<br>差分·均匀格·C–N | 约 $1.55$ | 固定单值格式不适用 | 固定单值格式不适用 | 固定网格，未给出坐标误差 | 图 8(b) |

按图中误差峰值，**Scheme 3 在两类 kink 中较小，Scheme 1 在环孤子中最小；Scheme 4 在三例中都高于 Scheme 1、3；Scheme 5 的规则 kink 误差明显更大。** Scheme 2 只有 $x$ 误差图，不能把 $1.5$ 当成 $u$ 误差加入排名。

原文文字笼统称普通动网格在 kink 上有优势，但图 7 的 Scheme 4 并不支持这一概括。这里按各 Scheme 的误差图分别列结果，不再把 Scheme 3、4 合并成一个结论。

### 每种 Scheme 展示了哪些指标

| 方法 | $u$ 波形对照 | $u$ 点误差曲线 | $x$ 坐标误差 | 时间精度 | 空间精度 |
|---|---|---|---|---|---|
| Scheme 1<br>可积Ⅰ·动格·Euler | 三类波形，$t=5,10$，图 1 | 三类波形，$t=5$，图 2 | 未给出 | 一阶更新 | 光滑非退化分支形式二阶 |
| Scheme 2<br>可积Ⅱ·动格·Euler | 规则 kink，$t=5$，图 3(a) | 未给出 | 规则 kink，$t=5$，图 3(b) | 一阶更新 | 光滑相容分支形式二阶 |
| Scheme 3<br>差分·动格·Euler | 三类波形，$t=5$，图 5 | 三类波形，$t=5$，图 6 | 未给出 | 一阶 Euler | 光滑规则网格形式二阶 |
| Scheme 4<br>差分·动格·预测校正 | 三类波形，$t=5,10$，图 4；与 Scheme 3 对照见图 5 | 三类波形，$t=5$，图 7 | 未给出 | 二阶预测校正形式，需场与格距一致预测 | 与 Scheme 3 相同 |
| Scheme 5<br>差分·均匀格·C–N | 规则 kink，$t=5,6,6.5$，图 8 | 规则 kink，$t=5$，图 8(b) | 未给出 | C–N 二阶时间形式 | 印刷式存在一阶配点残差 |

原文没有给五种方法统一的 $L^2$ 误差、守恒量漂移、计算耗时或网格/时间减半的观测阶，也没有完整列出节点数、步长和边界配置。上表的阶数来自公式分析，不是原文实测收敛阶。

误差图的横轴均标为 $y$，原文没有充分说明数值解与精确解如何配对、插值。因此这些图上峰值不能直接与第二章在共同物理 $x$ 点上计算的 2HS 总误差作数值大小比较。

### 1.1 五种方法分别怎么算

连续方程为

$$u_{xt}=(1-\partial_x^2)\sin u.\tag{G1}$$

令 $p_k=u_{k+1}-u_k$、$\delta_k=x_{k+1}-x_k$、$A_k=(u_{k+1}+u_k)/2$，$B_k=\cos u_{k+1}-\cos u_k$。$p_k$ 表示相邻节点的场差，与孤子参数 $p_1$ 不同。

| 方法 | 空间方程 | 时间更新 |
|---|---|---|
| Scheme 1：可积动网格 | $\dot p_k=\delta_k\sin A_k$，$\dot\delta_k=\cos(p_k/2)B_k$ | 一阶 Euler 型更新 |
| Scheme 2：可积动网格 | $\dot p_k=\Delta_k\sin A_k$，$\dot\delta_k=B_k$；$\Delta_k=\sqrt{4a^2-4\sin^2(p_k/2)}$ | 一阶 Euler 型更新 |
| Scheme 3：普通动网格 | $\dot p_k=\delta_k\sin A_k$，$\dot\delta_k=B_k$ | 显式 Euler |
| Scheme 4：普通动网格 | 与 Scheme 3 相同 | 一阶预测后，用前后两层右端的平均值校正 |
| Scheme 5：固定网格 | 直接差分连续方程 | Crank–Nicolson |

Scheme 1–3 都按 $Z^{n+1}=Z^n+\Delta t\,H(Z^n)$ 更新场差和格距，再由边界值累加场差得到 $u$。Scheme 4 的校正是

$$p_k^{n+1}=p_k^n+\frac{\Delta t}{2}\left[\delta_k^n\sin A_k^n+\widetilde\delta_k^{n+1}\sin\widetilde A_k^{n+1}\right],\qquad
\delta_k^{n+1}=\delta_k^n+\frac{\Delta t}{2}\left[B_k^n+\widetilde B_k^{n+1}\right].\tag{G2}$$

波浪号表示预测值。要实现二阶预测校正，场与格距都要一致地预测。Scheme 5 的原文公式是

$$p_k^{n+1}=p_k^n+\Delta t\left[h\bar f_k-\frac{\bar f_{k+1}-2\bar f_k+\bar f_{k-1}}h\right],\qquad
\bar f_k=\frac{\sin u_k^n+\sin u_k^{n+1}}2,\quad h=\Delta x.\tag{G3}$$

Scheme 1 与 3 主要比较空间方程，Scheme 3 与 4 比较时间算法。与 Scheme 5 比较时，网格、空间方程和时间算法都变了。这里的“可积”指半离散方程，Euler 时间更新不因此自动可积。

### 1.2 网格为什么会向陡坡集中

GSG 的守恒密度是

$$r=\sqrt{1+u_x^2},\qquad r_t+(r\cos u)_x=0,\qquad dy=r\,dx-r\cos u\,dt.\tag{G4}$$

在单值、坐标不退化的分支上，等距取 $y$ 节点，就有 $x_y=1/r$、$x_t=\cos u$。坡度大时 $r$ 大，物理格距小，节点便向陡坡集中。论文使用这一密度，没有比较更多密度选择；环形解则按参数曲线处理。

三种动网格空间模型在光滑、规则网格上的形式一致性为二阶。固定格 Scheme 5 按印刷公式展开有半格配点造成的一阶项，不能仅凭“中心差分＋C–N”认定空间二阶。论文没有提供独立的网格、时间减半收敛表。

### 1.3 五种方法的原文结果图

<details class="source-figure"><summary>Scheme 1 · 可积半离散式Ⅰ＋动网格＋Euler 型更新 · 原文图 2 · 三类波形的 u 误差</summary><figure><img src="Workspaces/gsg_project/dlw_report/gsg_figures/scheme1.png" alt="GSG Scheme 1：三类波形的 u 误差"></figure></details>

<details class="source-figure"><summary>Scheme 2 · 可积半离散式Ⅱ＋动网格＋Euler 型更新 · 原文图 3 · 规则 kink 的波形及 x 坐标误差</summary><figure><img src="Workspaces/gsg_project/dlw_report/gsg_figures/scheme2.png" alt="GSG Scheme 2：规则 kink 的波形及 x 坐标误差"></figure></details>

<details class="source-figure"><summary>Scheme 3 · 普通差分＋动网格＋Euler · 原文图 6 · 三类波形的 u 误差</summary><figure><img src="Workspaces/gsg_project/dlw_report/gsg_figures/scheme3.png" alt="GSG Scheme 3：三类波形的 u 误差"></figure></details>

<details class="source-figure"><summary>Scheme 4 · 普通差分＋动网格＋预测校正 · 原文图 7 · 三类波形的 u 误差</summary><figure><img src="Workspaces/gsg_project/dlw_report/gsg_figures/scheme4.png" alt="GSG Scheme 4：三类波形的 u 误差"></figure></details>

<details class="source-figure"><summary>Scheme 5 · 普通差分＋均匀固定网格＋C–N · 原文图 8 · 规则 kink 的波形及 u 误差</summary><figure><img src="Workspaces/gsg_project/dlw_report/gsg_figures/scheme5.png" alt="GSG Scheme 5：规则 kink 的波形及 u 误差"></figure></details>

<h2 id="hs">二、2HS：可积离散、直接差分与动网格对照</h2>

**四种方案都有结果。** 本轮采用论文的动网格，与普通差分的均匀固定网格作对照；编号按下表重新定义。

| 编号 | 空间方法与网格 | 用途 |
|---|---|---|
| **S1** | 原论文可积半离散＋论文动网格 | 原方案 |
| **S2** | 参数校准半离散＋论文动网格 | 与 S1 比，检验参数校准 |
| **S3** | 连续 2HS 直接 ALE 差分＋论文动网格 | 与 S1/S2 比，比较空间离散方法 |
| **S4** | 同一套直接 ALE 差分＋均匀固定网格 | 与 S3 比，去掉动网格因素 |

四种方案各配 Euler、Heun、RK4、固定步长 DOP853（下称 RK8）。S1/S2/S3 都按 $\dot x=-u$ 推进节点，但各自的数值场不同，节点轨迹不要求相同。S3 是本轮新实现的论文动网格差分，不是旧的同变量差分或固定端点密度动网格。

<h3 id="waveforms">波形与空间误差：四种方案一起看</h3>

每张图的三列为 $p=5,12,22$；前两行是 $u$、$\rho$ 波形，后两行是逐点绝对误差。黑线为精确解，红色 S1、橙色 S2、绿色 S3、蓝色 S4。波形符号取自数值节点（每四个显示一个）；误差在线性重构后的 16001 个公共物理点上计算，与表格口径一致。

固定 $N=400$、$\Delta t=.003125$。先展示 RK4，其后是 Euler、Heun、RK8；两个时刻的图均直接显示。误差用对数纵轴，以同时看清原式和其他方案的不同量级；低于 $10^{-12}$ 的部分不显示。

<!-- REVIEWED_FIGURES -->

<h3 id="results">2.1 四种方案的误差：20 个参数</h3>

先看 **$c=1$、RK4、$N=400$、$\Delta t=.003125$、$t=.5$**。$N$ 为区间数；每格依次为 **$u$ 误差 / $\rho$ 误差**，在公共物理区间 $[-2,2]$ 的 16001 个点上计算。参数 $p=3,4,\ldots,22$，越大波形越陡。

<!-- DYNAMIC_TABLE_MAIN -->

**校准在全部 20 个参数上都降低了原可积式的双场误差。普通差分采用论文动网格后，两个场的误差在这组配置下都高于固定网格。** 校准方案与普通动网格差分相比，只有 $p=22$ 的 $u$ 误差更小，$\rho$ 没有胜出。

下表只汇总上述 RK4、$t=.5$ 配置；“更小”不要求达到某个改善百分比。

<!-- REVIEW_COUNTS -->

其他算法和时刻的完整结果：

<!-- DYNAMIC_TABLE_REST -->

这些是同一参数族的数值比较，不是独立统计样本；不能把一组配置的排名推广到所有步长和时刻。

### 2.2 时间算法的影响

再看较粗配置 **$p=12$、$N=200$、$\Delta t=.0125$、$t=.25$**，用 8001 个共同物理点评价。每行固定空间方案，横向只换时间算法。

<!-- TIME_TABLE_MAIN -->

这里比较的仍是连续总误差。高阶时间推进能减小时间误差，却不会消除空间离散和重构误差；Euler 偶尔更小，也不能据此判断它的时间精度更高。

<!-- TIME_TABLE_REST -->

代表参数 $p=5,12,22$ 的减半步长检查中，四种配对只有一次单场排名翻转：**$p=22$、$N=200$、Euler、$t=.5$ 的 S2/S3 的 $u$ 误差**。因此临界优势需结合减步结果判断。

<h3 id="density">2.3 动网格如何构造，怎样做对照</h3>

论文网格来自 $\rho_t=(u\rho)_x$，使用守恒坐标

$$dX=\rho\,dx+u\rho\,dt,\qquad x_X=\rho^{-1},\qquad x_t|_X=-u.\tag{H1}$$

S1/S2/S3 初始都在 $X\in[-4,4]$ 上等距取 $N+1$ 个点，再由精确解映射到物理位置 $x$。之后所有节点、包括两端，都按 $-u$ 运动。这里 $\rho$ 同时是物理未知量和论文坐标的密度；小密度对应较大的物理格距，所以论文网格并不必然向波峰集中。

S4 初始在物理区间 $[-4,4]$ 均匀布点，之后固定。S3/S4 共用相同的差分算子与场方程，只改变初始节点和节点速度；这组对照用来考察论文动网格的作用。

**比较还受两点影响。** 论文映射后的初始物理区间略宽于 $[-4,4]$；此外，S1/S2 由左端解析 $u$ 确定积分常数，S3/S4 则指定两端解析 $u$ 来反演。因此主表比较的是完整方法，S1/S3 的差异不能全部归因于可积性。

额外 32 条控制把 S4 的初始端点改成与 S3 相同，覆盖 $p=3,5,12,22$、两套分辨率、四种算法；之后 S4 仍固定，S3 继续运动。出现 **2 次单场排名翻转**，说明初始区间对小差距有影响。这项检查尚不能替代全参数同域和扩域验证。

与 GSG 的对照思路相同：先比较动网格下的不同空间方法，再用普通固定网格作参照。这里四方案都运行同样的四种时间算法，避免像 GSG Scheme 5 那样只采用另一种时间算法；两系统的误差数值本身不作直接大小比较。

<h3 id="hs-equations">2.4 四种方案具体怎么算</h3>

连续目标固定为

$$u_{tx}-uu_{xx}-\frac12u_x^2-4u-\frac12(\rho^2-1)=0,\qquad \rho_t=(u\rho)_x.\tag{H2}$$

**S1/S2：论文半离散式。** 令 $d_k=x_{k+1}-x_k$、$v_k=u_{k+1}-u_k$、$a=8/N$，胞元密度为 $r_k=a/d_k$：

$$\dot d_k=-v_k,\qquad
\dot v_k=2d_k(u_{k+1}+u_k)+\frac{[d_k^2-a(a-C)]^2-v_k^2}{2d_k}-\frac{C^2d_k}{2}.\tag{H3}$$

由左端解析值累加 $v_k$ 恢复 $u_k$，推进左端 $\dot x_0=-u_0$，再累加格距恢复节点。**S1 取 $C=1$；S2 取 $C=a+\sqrt{1+a^2}$。** 校准只改离散参数，连续参照始终为 $c_{\mathrm{phys}}=1$。它消去原式相对该连续目标的一阶模型差；这不意味着总误差在所有配置中都胜过普通差分。可积结构指半离散方程，不意味着这里的显式时间推进也可积。

**S3/S4：直接差分连续方程。** 取节点变量 $m=u_{xx}+2$、$\rho$，节点速度为 $V$：

$$\begin{aligned}
\dot x_i&=V_i,\\
\dot m_i&=(u_i+V_i)(D_1m)_i+2(D_1u)_i m_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=(u_i+V_i)(D_1\rho)_i+\rho_i(D_1u)_i,\qquad (D_2u)_i=m_i-2.
\end{aligned}\tag{H4}$$

S3 取 $V_i=-u_i$，输运项抵消；S4 取 $V_i=0$。设 $h_-=x_i-x_{i-1}$、$h_+=x_{i+1}-x_i$，两者都用

$$\begin{aligned}
(D_1f)_i&=-\frac{h_+f_{i-1}}{h_-(h_-+h_+)}+\frac{h_+-h_-}{h_-h_+}f_i+\frac{h_-f_{i+1}}{h_+(h_-+h_+)},\\
(D_2f)_i&=\frac2{h_-+h_+}\left(\frac{f_{i+1}-f_i}{h_+}-\frac{f_i-f_{i-1}}{h_-}\right).
\end{aligned}\tag{H5}$$

每个时间级在当前节点上解三对角方程 $D_2u=m-2$，边界场取当前物理位置和时刻的解析值。S3 独立推进节点密度，不强制 $\rho d=a$；这是它与论文胞元质量关系的区别。

<h3 id="time">2.5 四种时间算法</h3>

把场和节点一起记作 $Z$，右端记作 $H(t,Z)$，时间步长为 $h_t$。每个中间级都重新计算节点、场和边界值。

$$\begin{array}{ll}
\text{Euler:}&Z^{n+1}=Z^n+h_tH(t_n,Z^n).\\[3pt]
\text{Heun:}&K_1=H(t_n,Z^n),\quad K_2=H(t_n+h_t,Z^n+h_tK_1),\\
&Z^{n+1}=Z^n+\frac{h_t}{2}(K_1+K_2).
\end{array}\tag{H11}$$

$$\begin{aligned}
\text{RK4:}\quad K_1&=H(t_n,Z^n),\quad K_2=H(t_n+h_t/2,Z^n+h_tK_1/2),\\
K_3&=H(t_n+h_t/2,Z^n+h_tK_2/2),\quad K_4=H(t_n+h_t,Z^n+h_tK_3),\\
Z^{n+1}&=Z^n+\frac{h_t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}\tag{H12}$$

RK8 用固定步长 DOP853 的十二级八阶主公式：

$$K_i=H\left(t_n+c_i h_t,Z^n+h_t\sum_{j&lt;i}a_{ij}K_j\right),\qquad
Z^{n+1}=Z^n+h_t\sum_{i=1}^{12}b_iK_i.\tag{H13}$$

<!-- RK8_COEFFICIENTS -->

四种方法每步分别计算 1、2、4、12 次右端。表中采用相同节点数和时间步长，计算量并不相同。

### 2.6 初值与误差

单孤子取 $p&gt;2$，令 $s=1-2/p$、$q=p/(p-1)$、$\beta=p-q$、$\theta=\beta X-st$，精确解为

$$x=\frac\theta\beta+\frac{s}{2}\tanh\frac\theta2+\frac{1-s^2}{4}t,\qquad
u=\frac{s^2}{4}\operatorname{sech}^2\frac\theta2,\qquad
\rho=\frac{1-s^2}{1-s^2\tanh^2(\theta/2)}.\tag{H14}$$

四种方案均以该连续孤子为初始目标。S1/S2 取解析节点 $u$、初始格距 $d_k$ 和胞元密度 $r_k=a/d_k$；S3/S4 取解析节点密度，并置 $m_i=(D_2u^*)_i+2$。将数值场线性插值到共同物理点 $\mathcal G\subset[-2,2]$，计算

$$E_u=\max_{x\in\mathcal G}|u_h(x,t)-u^*(x,t)|,\qquad
E_\rho=\max_{x\in\mathcal G}|\rho_h(x,t)-\rho^*(x,t)|.\tag{H15}$$

这是相对连续解的总误差，包含空间、时间和线性重构误差，不是单独的时间误差。S1/S2 的密度在胞元中点，S3/S4 在节点；先重构到同一组物理点再比较。

### 数据核对

640 条主轨道、96 条减半步长轨道均已完成，主表共 **1280 个双场数值格**。本次独立读回 736 条轨道，重算三档评价密度的 8832 项误差，最大绝对差小于 $2.45\times10^{-15}$；另核对 32 条同初始区间控制。轨道及来源哈希一致，保存场有限、节点有序、密度为正。

16001 点加密到 32001 点，误差最大相对变化约 **1.962%**；从各主表的原评价密度加密到 32001 点，四种配对的单场排名均未翻转。交接中的独立连续沿轨迹差商检查给出 S3 的 $m,\rho$ 右端残差约 1.98–2.00 阶，这是空间一致性证据，不是总误差收敛阶证明。

[本轮交接](Workspaces/hs_four_schemes_20260927/HANDOFF.md) · [完整四方案表](Workspaces/hs_four_schemes_20260927/out/main_wide.csv) · [减半步长](Workspaces/hs_four_schemes_20260927/out/time_half_wide.csv) · [同初始区间控制](Workspaces/hs_four_schemes_20260927/out/domain_control_cells.csv) · [独立读回审查](Workspaces/gsg_project/dlw_report/four_scheme_review/review.json)

<h3 id="sources">参考资料</h3>

- [GSG 原论文](Paper/sources/Numerical_Algorithms_gsg%20(1).pdf)，§2–4；[空间阶与配点核对](Workspaces/hs_conserved_mesh_20260925/ACCURACY_ORDER_COMPARISON.md)。
- [2HS 原论文](Paper/sources/2%20Huner%20Saxton.pdf)，(11)、(81)、(100)；[参数校准推导](Workspaces/hs_conserved_mesh_20260925/PARAMETER_CALIBRATION_REPORT.md)。
- [四方案实现与验证](Workspaces/hs_four_schemes_20260927/HANDOFF.md)；[原 DLW 数值报告](Workspaces/dlw_semidiscrete/numerics/REPORT.md)。


<h2 id="dlw">三、DLW：空间方法与动网格的数值比较</h2>

**DLW 中，动网格和半离散方法都能在部分算例中降低误差，但收益会随参数和分辨率变化。** 下面先固定 Euler，比较四种完整方案。SD 指可积半离散来源的空间方程，FD 指直接差分连续方程；这里的完整数值算法还包括 $x$ 差分和时间推进，不宣称整体可积。

| 编号 | 空间方法 | x 网格 | 比较用途 |
|---|---|---|---|
| **D1** | 原始 SD，$c=\kappa=0$ | 均匀固定 | 与 D2 比空间方法 |
| **D2** | 普通 FD | 均匀固定 | 固定网格基准 |
| **D3** | 与 D1 相同的 SD | 负支密度持续动网格 | 与 D1 比网格，与 D4 比空间方法 |
| **D4** | 与 D2 相同的 FD | 同一负支规则的持续动网格 | 与 D2 比网格 |

本章编号 D1–D4 独立于前面的 2HS。选负支作为正文代表，是因为它在 P6 的加密检查中仍保持双场收益；正支、对称密度的结果在后面补充。这里去掉的是“非均匀初始布点＋持续运动”这套动网格设置，不能把收益单独归给节点运动。

<h3 id="dlw-results">3.1 四方案主结果</h3>

共同设置为 **Euler、$N_x=512$、$h_y=1/8$、$\Delta t=1.25\times10^{-5}$、$T=.01$**。计算窗口 $x\in[-20,20)$，24 个 F 层；误差在公共物理核心 $x\in[-10,10)$、$|y_j|&lt;1.5$ 上评价。所有方案使用同一个连续单孤子初态与参照，$\rho=p+q$ 在本章是相位参数。每格为 **$u$ 最大绝对误差 / $v$ 最大绝对误差**。

<!-- DLW_MAIN_TABLE -->

**P6 最能说明两种作用。** 固定网格下 SD 比 FD 的双场误差小；换负支动网格后，两种空间方法都改善。D3 相对 D1 的 $u/v$ 误差降低约 **51.2% / 50.1%**，D4 相对 D2 降低约 **45.3% / 46.6%**。但 P10 的 SD 动网格使 $v$ 误差增加约 12.5%，P5 的 SD 中 $u$ 也略有增加；动网格不是普遍改善。

<h3 id="dlw-figures">3.2 波形、空间误差和加密后的变化</h3>

下图三列分别为 **P6、P2、P10**。前两行在最接近 $y=0$ 的实际 F 层上画 $u,v$ 波形（准确的 $y$ 值写在图中）；后两行画每个物理 $x$ 位置上跨全部评价 $y$ 层的最大绝对误差。后两行再对 $x$ 取最大值，就是上表指标。黑线为连续精确解，四条彩色线对应 D1–D4。

<figure><img src="Workspaces/gsg_project/dlw_report/dlw_numerical_update/waveforms_errors.png" alt="DLW四方案在P6、P2、P10的双场波形与沿x的最大误差"></figure>

**P6 的二维误差分布**如下：每行一种方案，两列分别为 $u,v$，横轴是 $x$、纵轴是 $y$。所有面板共用色标，显示绝对误差的十进制对数，颜色越深误差越小。图只展示 $x\in[-4,4]$ 的波区；表格仍用完整公共核心，不能只凭这幅局部图判断全域最大误差。

<figure><img src="Workspaces/gsg_project/dlw_report/dlw_numerical_update/p6_error_maps.png" alt="P6四方案在物理x和y平面的双场绝对误差分布"></figure>

**再看加密是否保留收益。** 下图纵轴是同一种空间方法的“动网格误差／固定网格误差”，低于 1 才有改善；左列 $N_x=512$，右列 $N_x=1024$，时间步仍相同。P2 的细网格动网格误差明显增长，P10 动网格没有完成，不能补成零或用终止前误差替代。

<figure><img src="Workspaces/gsg_project/dlw_report/dlw_numerical_update/mesh_refinement.png" alt="DLW负支动网格相对固定网格的误差比及x加密后的变化"></figure>

### 3.3 减步、加密与失败情况

全主表时间步减半后，动网格／固定和同网格 SD／FD 的单场排名均未翻转。空间加密则会改变结论，下面保留全部参数和未完成项。

<details markdown="1"><summary>Euler 时间步减半：Nx=512，h=1/8，dt=6.25e−6，T=.01</summary>

<!-- DLW_HALF_TABLE -->

</details>

<details markdown="1"><summary>x 网格加密：Nx=1024，h=1/8，dt=1.25e−5，T=.01</summary>

<!-- DLW_FINE_TABLE -->

</details>

P6 进一步取 $N_x=1024$、$\Delta t=3.125\times10^{-6}$ 后，D3 相对 D1 仍降低约 **17.6% / 3.4%**；同一负支规则下，SD/FD 的双场误差比分别约 **.896 / .879**。这些优势小于主网格上的幅度。

P2 的细网格存在高频扰动敏感性；P10 的细网格动网格在 $T=.01$ 前停止，减半步长也没有修复。原两支实验共 208 条正式及控制尝试，198 条完成、10 条未完成，另有先导实验。因此当前证据只支持所测短时配置，不能写成长距离传播或一般稳定性结论。

### 3.4 方程、网格与推进方式

两种方法都推进 $P=\delta_-u$ 与物理场 $v$，由左侧解析基值恢复 $u$。定义

$$\delta_-f_j=\frac{f_j-f_{j-1}}h,\quad M_-f_j=\frac{f_j+f_{j-1}}2,\quad
\delta_0f_j=\frac{f_{j+1}-f_{j-1}}{2h},\qquad w=v-\delta_0u.\tag{D1}$$

**原始 SD** 的短闭合形式为

$$H=\frac{u^2}{2}+2au+h^2\left(\frac{w^2}{32}-\frac w4\right),\qquad
P_t=-\delta_-H_x-(P+M_-w)_{xx},\qquad
w_t=-[(u+2a)w-4u]_x+w_{xx}.\tag{D2}$$

实际以 $v_t=w_t+\delta_0u_t$ 转成 $P/v$ 状态。**普通 FD** 在相同交错 $y$ 网格上为

$$P_t=-\delta_-\left(\frac{u^2}{2}+2au\right)_x-(M_-v)_{xx},\qquad
v_t=-[(u+2a)v-4u]_x-(\delta_0u)_{xx}.\tag{D3}$$

两者共用四阶中心 $x$ 导数，二阶导数取一阶算子的复合；$y$ 方向为二阶一致形式。$y$ 边界使用解析左基值及鬼点，右端对相对解析背景的扰动作二次外推；$x$ 采用宽周期窗口。

负支使用有限 $h$ 密度和通量

$$r^-_j=1-\frac{w_j}{4},\qquad q^-_j=(u_j+2a)r^-_j-\partial_xr^-_j-2a.\tag{D4}$$

在共同的 22 个内部 F 层上等权平均，得到 $R,Q$；初始反演 $R$ 的累计积分，等质量布点。之后每步从当前数值场重算

$$V_i=\dot X_i=\frac{Q_i-Q_0}{R_i}.\tag{D5}$$

所有 $y$ 层共用这一套移动的 $x$ 节点。固定网格取 $V=0$。同一网格规则下 FD/SD 初始节点与状态一致，但随后轨迹可以不同；该密度的半离散守恒结构属于 SD，对 FD 则是相同的网格驱动规则。

记 $X=\xi+s$、$J=1+D_\xi s$，用 $D_x=J^{-1}D_\xi$ 计算物理导数，并同步 Euler 更新

$$\begin{aligned}
P^{n+1}&=P^n+\Delta t(F_P+V D_xP),\\
v^{n+1}&=v^n+\Delta t(F_v+V D_xv),\\
s^{n+1}&=s^n+\Delta t V.
\end{aligned}\tag{D6}$$

没有滤波、人工耗散或内部精确解回填。误差用共同物理点上的连续解析解计算：先在计算坐标加密，再插值到共同物理位置；本章表与图沿用原实验的 $4N_x$ 周期评价网格在核心区内的点。它包括 $x/y$ 空间误差、Euler 时间误差和重构误差。与 2HS 相比，本组受控实验只有 Euler，不能填成相同的四算法比较。

### 3.5 密度和系数：作为补充比较

**密度不同，最优场也可能不同。** P6 的正支 SD 在主网格上比固定格降低约 73.7% / 57.7%，但细网格、较小时间步下 $v$ 反增约 5.3%。对称密度的主网格双场收益更大，细网格 $v$ 优势却会随减步消失。完整结果见[两支密度](Workspaces/dlw_branch_mesh_euler_20260926/REPORT.md)和[对称密度](Workspaces/dlw_symmetric_mesh_euler_20260926/REPORT.md)。

**优势参数带也受时刻限制。** 固定 $a=4,q=3$，在 $p=.9,.95,1,1.05,1.1$、$T=.01$ 的所测主网格与细网格配置下，负支 SD 双场优于负支 FD；但细网格在 $T=.005$ 时 $u$ 全部反败。这是采样结果，未证明整个连续参数区间或整个时间段上的优势，见[参数扫描](Workspaces/dlw_p_regions_20260926/REPORT.md)。

**系数调整单独看。** 固定网格的另一批实验比较原式与预先由空间残差得到的共用系数 $(c,\kappa)=(.04248652711,.00844851896)$。P2/P6 的结构方案有短时局部优势，但调整系数并非普遍改善；其中 P5 的窄域结果存在尾部污染，不能与本章宽域主表混用。见[系数实验](Workspaces/dlw_coefficient_euler_20260926/REPORT.md)。

本次从保存场重新核对本章主表、减步表和细网格表的完整轨道指标，并核对绘图误差与主表一致；没有重新做时间演化。[本章数据与核对记录](Workspaces/gsg_project/dlw_report/dlw_numerical_update/integration.json)。
