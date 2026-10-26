### 2.5 连续极限 {#zh-limits}

在建立半离散方程及其精确解之后，我们进一步考察它们在格点间距趋于零时如何逼近连续 DLW 系统。我们希望明确格点如何改变精确波场，以及连续方程如何从离散关系中恢复。首先，我们导出半离散与连续 Gram 解之差的展开，并给出其首项系数；重构物理场的二阶收敛由此直接得到。随后，我们考察非线性方程的相容性。

本小节中，$O_K(h^m)$ 表示在紧集 $K$ 上由 $C_Kh^m$ 一致控制的余项，其中 $C_K$ 与 $h$ 无关。我们假设函数在 $K$ 的一个开邻域内充分光滑。使用展开式的导数时，余项估计也适用于所需导数。

我们首先比较精确解族中相互对应的成员。为在同一物理位置进行比较，我们将格点 τ 函数延拓到连续坐标 $y$，并保留交错重构。对于正函数 $f_h,g_h$，定义

<a id="zh-eq-47"></a>

$$\begin{aligned}U_h(y)&=\partial_x[2\log f_h(y)-\log g_h(y-h/2)-\log g_h(y+h/2)],\\\Omega_h(y)&=\partial_x[\log g_h(y+h/2)-\log g_h(y-h/2)],\\V_h(y)&=\frac4h\Omega_h(y)+\frac{U_h(y+h)-U_h(y-h)}{2h}.\end{aligned}\tag{38}$$

这里及下文在表示 $y$ 方向平移时，省略共同的变量 $x,t$。在 $y=(j+\tfrac12)h$ 处，这些表达式与格点重构公式 (18) 一致。

**定理 2.7（精确波场的误差首项与收敛性）。** 固定行列式阶数 $N$，并选取满足下列条件的实谱参数，其中 $h_0>0$：

<a id="zh-eq-59"></a>

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad 0<q_1<\cdots<q_N,\qquad \rho_i>0.\tag{50}$$

设 $f,g$ 为公式 (5) 中的连续 Gram τ 函数，$u,v$ 为通过公式 (2) 定义的物理场。对于 $0<h\le h_0$，将正格点因子延拓到实数次幂，并令

<a id="zh-eq-60"></a>

$$g_h(x,y,t)=\tau_0(y/h),\qquad f_h(x,y,t)=\tau_1(y/h-1/2;a-h/2).\tag{51}$$

设 $U_h,V_h$ 为上述交错重构得到的物理场。记 $\alpha=\log f$、$\beta=\log g$、$z_i=p_i-a$、$w_i=q_i+a$，并定义

$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,$$

$$\alpha_2=\sum_{i=1}^{N}(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_{i=1}^{N}c_i\rho_i\partial_{\rho_i}\beta.$$

则在任意紧集 $K$ 上，一致地有

<a id="zh-eq-201"></a>

$$\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}\tag{60}$$

因此，对于充分小的 $h>0$，有

<a id="zh-eq-61"></a>

$$\sup_K\bigl(|U_h-u|+|V_h-v|\bigr)\le C_Kh^2\tag{52}$$

这一展开同时适用于通过 PE 与 PF 重构的物理场。

**证明。** 我们保持谱参数固定，首先展开格点因子：

<a id="zh-eq-62"></a>

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),\tag{53}$$

对于各行列式元素，格点相位中 $y$ 的系数因而满足

<a id="zh-eq-63"></a>

$$\frac1h\log[\lambda_h(z_i)\lambda_h(w_k)]=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).\tag{54}$$

在 $f_h$ 中，半格点位移还与辅助参数的平移相结合，得到如下振幅因子：

<a id="zh-eq-64"></a>

$$\begin{aligned}-\frac{z_i+h/2}{w_k-h/2}[\lambda_h(z_i)\lambda_h(w_k)]^{-1/2}&=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}\\&=-\frac{z_i}{w_k}\left[1+\frac{h^2}{8}\left(\frac1{w_k^2}-\frac1{z_i^2}\right)+O(h^4)\right].\end{aligned}\tag{55}$$

因此，相位与中心化振幅相对于连续形式的差异均从 $h^2$ 阶开始。

为确定行列式中的系数，我们采用主子式展开。每个主子式的行与列使用同一个指标集 $\mathcal I$，其相位修正为 $h^2y\sum_{i\in\mathcal I}c_i$，而 $f_h$ 的额外振幅修正为 $h^2\sum_{i\in\mathcal I}d_i$。算子 $\rho_i\partial_{\rho_i}$ 恰好选出包含指标 $i$ 的主子式。先展开行列式，再展开其对数，得到

$$\log f_h=\alpha+h^2\alpha_2+O_K(h^4),\qquad \log g_h=\beta+h^2\beta_2+O_K(h^4).$$

所述谱条件保证连续 τ 函数及其实数次幂延拓为正。由于 $N$ 和谱参数保持固定，这些展开连同下面所需的导数在紧集上一致成立。

接下来，我们将对数展开代入交错重构。围绕物理位置 $y$ 作对称 Taylor 展开，得到

$$U_h=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4).$$

对于第二个物理场，相应的展开为

$$\frac4h\Omega_h=4\beta_{xy}+h^2\left[4(\beta_2)_{xy}+\frac16\beta_{xyyy}\right]+O_K(h^4),$$

$$\begin{aligned}\frac{U_h(y+h)-U_h(y-h)}{2h}={}&u_y+h^2\left[2(\alpha_2-\beta_2)_{xy}-\frac14\beta_{xyyy}+\frac16u_{yyy}\right]+O_K(h^4).\end{aligned}$$

将二者相加，得到

$$V_h=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).$$

最后，连续重构关系给出 $4\beta_{xy}=v-u_y$。在两个物理场展开中使用这一恒等式，即得所述系数 $C_U,C_V$。它们在 $K$ 上有界，因此得到二阶收敛估计。由于 PE 与 PF 从同一组 τ 函数重构出相同的物理场，结论对两种表示均成立。□

通过这一展开，我们可以描述格点间距较小但非零时，$y$ 方向离散如何改变重构波场。系数 $C_U,C_V$ 分别刻画两个物理场差异首项的空间分布。含 $\alpha_2,\beta_2$ 的项来自行列式解本身的变化，其余项则来自交错重构。在所述假设下，这些系数在紧集上有界。因此，这一展开直接蕴含：当 $h\to0$ 时，两个重构物理场均在紧集上以二阶精度一致收敛到相应的连续 DLW 物理场。

现在，我们转向非线性方程。为用物理变量表达其连续极限，我们引入

<a id="zh-eq-51"></a>

$$W_j=v_j-\delta_0u_j=\frac4h\omega_j,\qquad \mathcal F_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{42}$$

PE 方程于是写为

<a id="zh-eq-52"></a>

$$\begin{aligned}E_{1,h,j}&:=\delta_-u_{j,t}+\partial_x\delta_-\mathcal F_j+\partial_x^2(\delta_-u_j+\mathcal M_-W_j)=0,\\E_{2,h,j}&:=W_{j,t}-W_{j,xx}+\partial_x[(u_j+2a)W_j-4u_j]=0.\end{aligned}\tag{43}$$

令 $\mathcal M_+z_j=(z_{j+1}+z_j)/2$。恒等式 $\mathcal M_+\delta_-=\delta_0$ 表明，$\mathcal M_+E_{1,h,j}+E_{2,h,j}$ 中的时间导数为 $v_{j,t}$。因此，我们将这一组合与连续 DLW 系统的第二式进行比较。

**命题 2.8（方程的相容性）。** 在 $y_j=(j+\tfrac12)h$ 处对充分光滑的物理场 $u,v$ 取样，并定义连续残差

<a id="zh-eq-53"></a>

$$\mathcal C_1=u_{yt}+v_{xx}+[(u+2a)u_y]_x,\qquad \mathcal C_2=v_t+u_{xxy}+[(u+2a)v-4u]_x.\tag{44}$$

则在紧集上一致地有

<a id="zh-eq-54"></a>

$$E_{1,h,j}=\mathcal C_1(x,y_j-h/2,t)+O_K(h^2),\qquad \mathcal M_+E_{1,h,j}+E_{2,h,j}=\mathcal C_2(x,y_j,t)+O_K(h^2).\tag{45}$$

**证明。** 记 $m_j=y_j-h/2$。围绕差分与平均算子各自的中心展开，得到

<a id="zh-eq-55"></a>

$$\begin{aligned}\delta_-z_j&=z_y(m_j)+\frac{h^2}{24}z_{yyy}(m_j)+O_K(h^4),\\\mathcal M_-z_j&=z(m_j)+\frac{h^2}{8}z_{yy}(m_j)+O_K(h^4),\\\delta_0z_j&=z_y(y_j)+\frac{h^2}{6}z_{yyy}(y_j)+O_K(h^4).\end{aligned}\tag{46}$$

因此，

<a id="zh-eq-56"></a>

$$W_j=(v-u_y)(y_j)+O_K(h^2),\quad \mathcal F_j=\left(\frac{u^2}{2}+2au\right)(y_j)+O_K(h^2),\quad \delta_-u_j+\mathcal M_-W_j=v(m_j)+O_K(h^2).\tag{47}$$

这些展开在所需的求导后仍成立。代入第一条残差，得到 $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$。

对于第二条残差，记 $w=v-u_y$，可得

<a id="zh-eq-57"></a>

$$E_{2,h,j}=\{w_t-w_{xx}+[(u+2a)w-4u]_x\}(y_j)+O_K(h^2).\tag{48}$$

将第一条残差关于 $y_j$ 作平均，再与第二条相加，得到

<a id="zh-eq-58"></a>

$$\begin{aligned}\mathcal M_+E_{1,h,j}+E_{2,h,j}&=u_{yt}+v_{xx}+[(u+2a)u_y]_x\\&\quad +(v-u_y)_t-(v-u_y)_{xx}+[(u+2a)(v-u_y)-4u]_x+O_K(h^2)\\&=v_t+u_{xxy}+[(u+2a)v-4u]_x+O_K(h^2).\end{aligned}\tag{49}$$

这里，所有连续物理场均在 $y_j$ 处取值。第二个结论得证。□

连续极限分析表明，所构造的格点系统与连续 DLW 模型保持着可定量描述的联系。我们建立了格点方程对连续方程的二阶相容性，并对本节考察的精确解族，得到了两个物理场在紧集上的二阶一致收敛。在有限格距下，系数 $C_U,C_V$ 进一步刻画了这种逼近：它们描述各物理场差异的首项，以及这一差异在波形中的空间变化。因此，我们能够直接通过重构物理场评估 $y$ 方向离散的影响。由于 PE 与 PF 从同一组 τ 函数得到相同的物理场，上述误差展开及其系数同时适用于两种表示。
