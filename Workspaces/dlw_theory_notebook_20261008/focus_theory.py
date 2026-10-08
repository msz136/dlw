"""Keep Gram exactness as the main statement and shorten supporting material."""
import re

EXACT_LIMIT=r'''### 6.1　Gram 解族的极限

对上述正实谱参数，连续 τ 函数为

$$\tau_n^{(0)}(x,y,t)=\det\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-a}{q_k+a}\right)^n
e^{(p_i+q_k)x+(q_k^2-p_i^2)t+y((p_i-a)^{-1}+(q_k+a)^{-1})}\right].\tag{L4}$$

令 $f^{(0)}=\tau_1^{(0)}$、$g^{(0)}=\tau_0^{(0)}$，并由（C2）定义 $u^{(0)},v^{(0)}$。有限 $h$ 的 $F_j,G_j$ 分别以 $j=y/h-1/2$ 和 $j=y/h$ 作正实指数插值，再按（N4）及 $v=(4/h)\omega+\delta_0u$ 重构 $u^{(h)},v^{(h)}$。

固定任意有限 $N$，若谱参数在某个 $h_0>0$ 处满足第 5 节的正性条件，则对任意 $R>0$，存在 $C_R\ge0$、$\varepsilon_R>0$，使 $0<h<\varepsilon_R$ 时

$$\sup_{|x|,|y|,|t|\le R}\left(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\right)\le C_Rh^2.\tag{L8}$$

这里取极限的是随 $h$ 变化的精确 Gram 解。其相位满足 $h^{-1}\log\lambda_h(z)=z^{-1}+O(h^2)$，F 的半格移位与振幅的一阶项相消；对数导数在紧区域上保持正则，因而得到上述二阶界。'''

def focus(cells):
    if any(c.cell_type=='markdown' and c.source.startswith('### 6.1　Gram 解族的极限') for c in cells):return cells
    for c in cells:
        if c.cell_type!='markdown':continue
        s=c.source
        if s.startswith('# DLW 理论'):
            s=r'''# DLW 理论

从连续 DLW 的双线性表示构造交错格点方程，给出 Gram τ 函数，并证明它满足两条半离散双线性方程。随后恢复非线性场，说明其连续极限。

连续变量为 $(x,y,t)$，离散格点为 $j\in\mathbb Z$，格距为 $h>0$。参数 $a$ 固定，采用 $\lambda=-2$ 的 DLW 归一化。'''
        if s.startswith('## 1　'):
            s=s[:s.index('**定理 1')]+r'将（C2）代入并求导，由（C3）得到连续 DLW 方程（C1）。'
        if s.startswith('## 2　'):
            s=s.replace('**定理 2（二阶双线性一致性）。**','二阶展开为：')
        if s.startswith('## 4　任意 N'):
            s=s.replace('## 4　任意 N 的 τ 函数满足半离散方程','## 4　Gram τ 函数的精确性')
            s=s.replace('**定理 3（Gram 精确解）。**','**主定理（Gram 精确解）。**')
        if s.startswith('### 4.1　'):
            s=s[:s.index('**推论 4')]+r'归一化相互作用系数 $A_{12}$ 与格距 $h$ 无关。'
        if s.startswith('## 5　'):
            s=s.replace('**定理 5（正则物理解）。**','')
        if s.startswith('## 6　'):
            s=s.replace('**定理 6（二阶非线性一致性）。**','二阶非线性一致性如下。')
        if s.startswith('## 7　精确孤子'):
            s=EXACT_LIMIT
        if s.startswith('## 8　'):
            s=s.replace('## 8　补充：保留势的非线性表示','## 附录　保留势的非线性表示')
        s=s.replace('### 8.2　势差的乘积分解','### 势差的乘积分解')
        c.source=s.strip()
    return cells
