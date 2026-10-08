"""User-directed prose and math-markup revision; preserves all code cells."""
import re

S2_PROOF=r'''证明。固定 $(x,y,t)$，令

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t)
=B_af\cdot g(y+s)+2sD_xf\cdot g(y+s).$$

这里 $f$ 的 $y$ 坐标保持不变，$s$ 只作用于第二个因子的平移和算子参数。对 $s$ 求导，在 $s=0$ 处得到

$$\begin{aligned}
\Phi(0)&=B_af\cdot g,\\
\Phi'(0)&=B_af\cdot g_y+2D_xf\cdot g,\\
\Phi''(0)&=B_af\cdot g_{yy}+4D_xf\cdot g_y,\\
\Phi^{(3)}(0)&=B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}.
\end{aligned}$$

由于 $\mathcal B_h^{\pm}=\Phi(\pm h/2)$，Taylor 展开给出

$$\mathcal B_h^{\pm}=\Phi(0)\pm\frac h2\Phi'(0)
+\frac{h^2}{8}\Phi''(0)\pm\frac{h^3}{48}\Phi^{(3)}(0)
+\frac{h^4}{384}\Phi^{(4)}(0)+O(h^5).$$

两式相加后除以 $2$，奇次项相消：

$$\begin{aligned}
\frac{\mathcal B_h^++\mathcal B_h^-}{2}
&=\Phi(0)+\frac{h^2}{8}\Phi''(0)+O(h^4)\\
&=B_af\cdot g+\frac{h^2}{8}
\left(B_af\cdot g_{yy}+4D_xf\cdot g_y\right)+O(h^4).
\end{aligned}$$

两式相减后除以 $h$，偶次项相消：

$$\begin{aligned}
\frac{\mathcal B_h^+-\mathcal B_h^-}{h}
&=\Phi'(0)+\frac{h^2}{24}\Phi^{(3)}(0)+O(h^4)\\
&=B_af\cdot g_y+2D_xf\cdot g
+\frac{h^2}{24}\left(B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}\right)+O(h^4).
\end{aligned}$$

舍去显式的二阶项即得（S2）。'''

TAU_DEFINITION=r'''## 3　Gram τ 函数

记 $d=h/2$，定义格点乘子

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad
\chi_{ik}=\lambda_h(p_i-a)\lambda_h(q_k+a).$$

取常数 $p_i,q_i,\rho_i$，定义

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\chi_{ik}^{\,j}e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{T10}$$

所求的两个 τ 函数取为

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{T11}$$

$\tau_0$ 与参数 $s$ 无关。下节证明（T11）满足（S1）的两条方程。

这里 $N$ 是行列式的阶数，$n$ 是辅助层编号。式（T11）取 $n=1$ 和 $n=0$；证明时使用相邻层 $\tau_{n+1},\tau_n$ 的恒等式。所有分母和格点乘子均取非零值。若允许 $n<0$，还需 $p_i-s\ne0$，以使（T10）中的负整数次幂有定义。'''

EXPANSION=r'''### 4.1　Cauchy 展开与孤子表达式

将（T10）的矩阵记为 $I+K$。主子式展开为

$$\det(I+K)=\sum_{I\subseteq\{1,\ldots,N\}}\det K[I,I].$$

每个主子式的行、列指数因子可分别提出，剩余的 Cauchy 行列式为

$$\det\left[\frac1{p_i+q_k}\right]_{i,k\in I}
=\frac{\prod_{i<k\atop i,k\in I}(p_k-p_i)(q_k-q_i)}
{\prod_{i,k\in I}(p_i+q_k)}.\tag{T12}$$

令

$$\gamma_i=-\frac{p_i-a+d}{q_i+a-d},\qquad
\chi_i=\chi_{ii},\qquad
E_i=\frac{\rho_i}{p_i+q_i}\chi_i^j
e^{(p_i+q_i)x+(q_i^2-p_i^2)t},\tag{T3}$$
$$A_{ik}=\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)}.\tag{T4}$$

从（T12）的分母中提出对角因子 $\prod_{i\in I}(p_i+q_i)$，其余因子按每一对 $i<k$ 合并，得到

$$\det K[I,I]=
\left(\prod_{i\in I}\gamma_i(s)^nE_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\qquad
\gamma_i(s)=-\frac{p_i-s}{q_i+s}.$$

分别取 $n=0$ 和 $n=1,\ s=a-d$，便得到（T11）的子集展开：

$$\boxed{\begin{aligned}
G_j&=\sum_{I\subseteq\{1,\ldots,N\}}
\left(\prod_{i\in I}E_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\\
F_j&=\sum_{I\subseteq\{1,\ldots,N\}}
\left(\prod_{i\in I}\gamma_iE_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right).
\end{aligned}}\tag{T7}$$

空乘积取 $1$，$G_{j+1}$ 由每个 $E_i$ 替换为 $\chi_iE_i$ 得到。（T7）将行列式写成有限个指数项，单孤子和双孤子可直接读出。

当 $N=1$ 时，

$$G_j=1+E_1,\qquad F_j=1+\gamma_1E_1,\qquad
G_{j+1}=1+\chi_1E_1.\tag{T5}$$

当 $N=2$ 时，

$$\begin{aligned}
G_j&=1+E_1+E_2+A_{12}E_1E_2,\\
F_j&=1+\gamma_1E_1+\gamma_2E_2+A_{12}\gamma_1\gamma_2E_1E_2,\\
G_{j+1}&=1+\chi_1E_1+\chi_2E_2+A_{12}\chi_1\chi_2E_1E_2.
\end{aligned}\tag{T6}$$

**推论 4（双孤子展开）。** 二阶 Gram 行列式的归一化相互作用系数为 $A_{12}$，与格距 $h$ 无关。'''

def revise(cells):
    """Apply to the original builder output or to an already revised notebook."""
    if any(c.cell_type=='markdown' and c.source.startswith(TAU_DEFINITION[:24]) for c in cells):
        return cells
    by={c.id:c for c in cells}
    for c in cells:
        if c.cell_type!='markdown':continue
        if '下面的 `continuous_DLW` 明确列出' in c.source:
            c.source=c.source.replace('下面的 `continuous_DLW` 明确列出','下面的 `continuous_DLW` 列出')
            c.source=c.source.replace('\n\n这里证明的是双线性表示产生 DLW 解；从任意 DLW 场反向恢复 τ 函数还涉及积分条件。','')
        if '证明取 $\\Phi(s)' in c.source:
            c.source=c.source[:c.source.index('证明取 $\\Phi(s)')]+S2_PROOF
        if c.source.startswith('## 3　τ 函数：'):
            c.source=TAU_DEFINITION
            definition=c
        if c.source.startswith('### 行列式表示与展开'):
            c.source=EXPANSION
            expansion=c
        if c.source.startswith('## 4　任意 N'):
            replacements=[
                ('**定理 4（Gram 精确解）。** 在所有谱分母非零的条件下，（T10）—（T11）满足（S1）。','**定理 3（Gram 精确解）。** 在第 3 节的谱参数条件下，由（T10）定义的（T11）满足（S1）。'),
                ('**引理。**式（T10）满足','**引理。** 式（T10）满足'),
                ('证明。固定 j、s、n，把矩阵写为 Mᵢₖ=δᵢₖ+rᵢcₖ/(pᵢ+qₖ)，其中',r'证明。固定 $j,s,n$，把矩阵写为 $M_{ik}=\delta_{ik}+r_ic_k/(p_i+q_k)$，其中'),
                ('令 P=diag(pᵢ)、Q=diag(qᵢ)、b=(Q+sI)⁻¹c。由定义直接得到',r'令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义得'),
                ('最后一个等式来自 −(pᵢ−s)/(qₖ+s)−1=−(pᵢ+qₖ)/(qₖ+s)。在 M 可逆处记',r'最后一式来自 $-(p_i-s)/(q_k+s)-1=-(p_i+q_k)/(q_k+s)$。在 $M$ 可逆处记'),
                ('最后一步是矩阵行列式引理。Jacobi 微分公式给出 κ=(log τₙ)ₓ；亦可将其理解为 τₙ,ₓ/τₙ，无需选择复对数分支。再定义',r'矩阵行列式引理给出 $\psi=1-\zeta$。Jacobi 微分公式给出 $\kappa=\tau_{n,x}/\tau_n$；当 $\tau_n>0$ 时，这就是 $\partial_x\log\tau_n$。再定义'),
                ('使用 Hₓ=−HMₓH、Hₜ=−HMₜH，逐项求导得到',r'利用 $H_x=-HM_xH$ 和 $H_t=-HM_tH$，逐项求导得'),
                ('例如 zₓ=HPr−κz，故 ζₓ=(c−sb)ᵀz+bᵀ(HPr−κz)，即第二式。再微分第二式，并代入其余三式：',r'由 $z_x=HPr-\kappa z$，得 $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$，即第二式。再对第二式求导，并代入其余三式：'),
                ('由于 ψ=1−ζ，因此',r'由 $\psi=1-\zeta$，得'),
                ('另一方面，对任意 f=ψg，有直接展开恒等式',r'对任意 $f=\psi g$，直接展开得'),
                ('取 g=τₙ、f=τₙ₊₁，式（T20）即证明（T13）。为去掉 M 可逆的临时条件，把全部 ρᵢ 同乘一个参数 ε；在 ε=0 时 M=I，故恒等式在 ε=0 的邻域成立。原双线性残差是 ε 的多项式，因此对所有 ε 恒为零；取 ε=1 即覆盖 τₙ 的零点。引理得证。',r'取 $g=\tau_n$、$f=\tau_{n+1}$，由（T20）得（T13）。将全部 $\rho_i$ 替换为 $\varepsilon\rho_i$，则 $\varepsilon=0$ 时 $M=I$，恒等式在零点邻域成立。双线性残差是 $\varepsilon$ 的多项式，因而对所有 $\varepsilon$ 恒为零。取 $\varepsilon=1$，结论也适用于 $\tau_n=0$ 的点。'),
                ('在式（T13）中取 n=0、s=a−d，立即得到第一条方程。第二条来自逐矩阵元恒等式：',r'在（T13）中取 $n=0$、$s=a-d$，得第一条方程。第二条使用逐矩阵元恒等式'),
                ('再在式（T13）中取 n=0、s=a+d，并把 j 换为 j+1，即得',r'再在（T13）中取 $n=0$、$s=a+d$，并将 $j$ 换为 $j+1$，得'),
                ('式（T7）或等价的式（T10）—（T11）因而满足原半离散双线性方程（S1），对每个有限 N、所有 x、t 及整数 j 成立。',r'因此（T11）对每个有限 $N$、所有实数 $x,t$ 及整数 $j$ 满足（S1）。')
            ]
            for a,b in replacements:
                assert a in c.source,a
                c.source=c.source.replace(a,b)
        c.source=re.sub(r'\n{3,}','\n\n',c.source).strip()
    # Move the subset expansion and its independent Lean cell after the general proof.
    interaction=next(c for c in cells if c.cell_type=='code' and c.source.startswith('%%lean interaction'))
    result=[]
    for c in cells:
        if c.id in (expansion.id,interaction.id):continue
        if c.cell_type=='markdown' and (c.source.startswith('**运行证明。**') or c.source.startswith('下面展开任意 N 双线性链的 Lean')):continue
        result.append(c)
        if c.cell_type=='code' and c.source.startswith('%%lean gram'):
            result.extend([expansion,interaction])
    return result
