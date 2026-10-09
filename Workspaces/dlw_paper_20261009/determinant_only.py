"""Keep the determinant presentation and remove the soliton subset expansion."""
import re

def revise(source):
    source=source.replace('## 3　Gram τ 函数与孤子展开','## 3　Gram 行列式解')
    start=source.index('$$\\lambda_h(z)=')
    end=source.index('假设对所有 $i,k$',start)
    source=source[:start]+r'''$$\lambda_h(z)=\frac{z+d}{z-d}.\tag{7}$$

'''+source[end:]
    start=source.index('**命题 3.1')
    end=source.index('## 4　',start)
    source=source[:start]+source[end:]
    start=source.index('**证明。** 上述条件蕴含')
    end=source.index('□',start)+1
    source=source[:start]+r'''**证明。** 在上述参数条件下，式（9）中 $n=0$ 和 $n=1,s=a-h/2$ 对应的矩阵均可写为 $I+D_1CD_2$，其中 $D_1,D_2$ 为正对角矩阵，$C_{ik}=1/(p_i+q_k)$。有序正参数下的 Cauchy 矩阵 $C$ 严格全正，正对角缩放保持这一性质，故 $\det(I+D_1CD_2)\ge1$。因此 $F_j,G_j\ge1$。矩阵元关于 $(x,t)$ 实解析，其行列式亦实解析。□'''+source[end:]
    start=source.index('**证明。** 记 $z_i=p_i-a<0$')
    end=source.index('引理 4.1 的矩阵计算',start)
    source=source[:start]+r'''**证明。** 记 $z_i=p_i-a<0$、$w_k=q_k+a>0$。由固定谱参数条件，$|z_i|,w_k>h_0/2$。当 $h$ 充分小时，

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4).$$

因此，$g^{(h)}$ 的行列式中第 $(i,k)$ 个指数项的 $y$ 系数为

$$k_{ik}^{(h)}=\frac1h\log\bigl(\lambda_h(z_i)\lambda_h(w_k)\bigr)
=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).$$

对 $f^{(h)}$，半格移位后的矩阵元振幅因子为

$$\widetilde\gamma_{ik}^{(h)}
=-\frac{z_i+h/2}{w_k-h/2}\bigl(\lambda_h(z_i)\lambda_h(w_k)\bigr)^{-1/2}
=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}
=-\frac{z_i}{w_k}+O(h^2).$$

将上述相位与振幅代入式（9），各矩阵元在 $h\to0$ 时趋于式（47）中的相应矩阵元，误差为 $O(h^2)$。由于行列式阶数固定，其关于矩阵元的多项式依赖给出：对任意固定多重指标 $\nu$ 及紧集 $K$，

$$\partial^\nu f^{(h)}-\partial^\nu f^{(0)}=O_K(h^2),\qquad
\partial^\nu g^{(h)}-\partial^\nu g^{(0)}=O_K(h^2).$$

这里 $\partial^\nu$ 为关于 $(x,y,t)$ 的混合导数。命题 5.1 的正对角缩放论证同样适用于实数格点插值及其连续极限，故上述四个 τ 函数均不小于 $1$。因此，相应对数导数也满足一致二阶估计，且所需导数在紧邻域内一致有界。

'''+source[end:]
    # Numerical benchmarks retain their parameters but need no subset coefficients.
    start=source.index('精确参照取（47）')
    end=source.index('\n\n',start)
    source=source[:start]+r'''精确参照取式（47）的连续 Gram 行列式，并由变换（2）计算 $u_*,v_*$。三组参数均产生正则解。算例 B、C 位于命题 5.1 所列谱域之外，其 τ 函数的正性可直接由相应的一阶、二阶行列式检查。'''+source[end:]
    tags=re.findall(r'\\tag\{(\d+)\}',source)
    mapping={n:str(i+1) for i,n in enumerate(tags)}
    for n in re.findall(r'（(\d+)）',source):
        assert n in mapping, f'dangling equation {n}'
    source=re.sub(r'\\tag\{(\d+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',source)
    source=re.sub(r'（(\d+)）',lambda m:'（'+mapping[m[1]]+'）',source)
    assert all(s not in source for s in ['命题 3.1','主子式','子集','A_{ik}','E_i(j'])
    return source
