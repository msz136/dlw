# T03：N=1 精确族、物理中点与二阶展开独立核对

2026-10-01。只核对原 SD（不移动 a，不改变物理重构）。来源：
`Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md` §1、4；
`Workspaces/dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md` §2、3；
`Workspaces/dlw_semidiscrete/numerics/lib/dynamics.py` 的 `Reference.uv`。
不采用历史投影结果作为数学依据。

## 1. 定义及实正则域

固定实数 a，记

\[
P=p-a,\quad Q=q+a,\quad K=p+q=P+Q>0,\quad
\Gamma=-P/Q>0,\quad \ell=P^{-1}+Q^{-1},\quad
\omega=q^2-p^2.
\]

上述条件强制 PQ<0、\(\ell=K/(PQ)<0\)、\(\Gamma\ne1\)。
既允许 P<0<Q，也允许 Q<0<P。相位 \(\phi\in\mathbb R\)，
\(0<h<2\min(|P|,|Q|)\)。N=1 的常数 \(\rho/K\) 已吸入 \(e^\phi\)。
这保证下列有限 h 比值为正，τ 在全实 x,y,t 上为正。

\[
\chi_h=\frac{P+h/2}{P-h/2}\frac{Q+h/2}{Q-h/2},\qquad
\gamma_h=-\frac{P+h/2}{Q-h/2}.
\]

## 2. 自然解析插值（物理中点）

格点关系为 \(y=(j+1/2)h\)。将 \(j=y/h-1/2\) 代入实对数指数，定义

\[
\lambda_h=h^{-1}\log\chi_h,\quad \delta_h=\tfrac h2\lambda_h,\quad
Z_h=Kx+\lambda_hy+\omega t+\phi,
\]
\[
\varepsilon_h=\log\gamma_h-\log\Gamma-\tfrac12\log\chi_h
=\tfrac12\left[\log\left(1-\frac{h^2}{4P^2}\right)
-\log\left(1-\frac{h^2}{4Q^2}\right)\right].
\]

于是位于 y 的 F 与位于 \(y\pm h/2\) 的 G 为

\[
F_h(y)=1+\Gamma e^{Z_h+\varepsilon_h},\qquad
G_h(y\pm h/2)=1+e^{Z_h\pm\delta_h}.
\]

令 \(s(z)=(1+e^{-z})^{-1}\)。精确的物理函数为

\[
u_h=K\{2s(Z_h+\log\Gamma+\varepsilon_h)
-s(Z_h-\delta_h)-s(Z_h+\delta_h)\},
\]
\[
v_h=\frac{4K}{h}\{s(Z_h+\delta_h)-s(Z_h-\delta_h)\}
 +\frac{u_h(x,y+h,t)-u_h(x,y-h,t)}{2h}.
\]

这些是整个窗口内的解析函数，有限格点求值只是其限制；并非在有限采样点上拟合插值。

## 3. 二阶系数

\[
c_3=(P^{-3}+Q^{-3})/12,\qquad
\gamma_2=(Q^{-2}-P^{-2})/8.
\]
\[
\lambda_h=\ell+h^2c_3+O(h^4),\qquad
\varepsilon_h=h^2\gamma_2+O(h^4).
\]
记 \(z=Kx+\ell y+\omega t+\phi\)、\(f(z)=s(z+\log\Gamma)\)。
连续场为

\[
u_0=2K(f-s),\qquad v_0=2K\ell(f'+s').
\]

逐项 Taylor 得到

\[
B_u=2Kyc_3(f'-s')+2K\gamma_2f'-\frac{K\ell^2}{4}s'',
\]
\[
B_v=2Kc_3(f'+s')+2K\ell yc_3(f''+s'')
 +2K\ell\gamma_2f''+\frac{K\ell^3}{12}(4f'''-5s''').
\]

核对 B_v 的一种分解为

\[
W_h=4K\ell s'+h^2\left(4Kc_3s'+4K\ell yc_3s''
+\frac{K\ell^3}{6}s'''\right)+O(h^4),
\]
\[
\delta_0u_h=\partial_yu_0+h^2\left(\partial_y B_u
+\tfrac16\partial_y^3u_0\right)+O(h^4).
\]

精确 u_h,v_h 是 h 的偶函数。所有实紧窗口及其任意固定阶实导数上，展开余项为 O(h⁴)；
在固定正则参数的紧邻域可取一致常数。未经额外尾部估计，不从此宣称整个 \(\mathbb R^2\) 的 L² 余项；
直线孤子在沿波峰方向没有衰减，本身通常不属于全二维无权 L²。

## 4. 不可切向吸收的极点

在 \(z_*=i\pi(2n+1)\) 附近写 \(\zeta=z-z_*\)，有

\[
s(z)=\zeta^{-1}+\tfrac12+\tfrac1{12}\zeta+O(\zeta^3).
\]

由于 \(\log\Gamma\ne0\)，f 在这些 s 极点处解析。因此

\[
B_u=-\frac{K\ell^2}{2}\zeta^{-3}+O(\zeta^{-2}),
\qquad
B_v=\frac52K\ell^3\zeta^{-4}+O(\zeta^{-3}).
\]

连续 u 的任意 p,q,φ 切向只含 f,s,f′,s′ 及仿射 x,y,t 系数，所以极点阶数至多 2。
连续 v 本身已有二阶极点，任意切向可有三阶；因此不能把 u 的“三阶即法向”判据直接用于 v。
但是 v 的四阶系数也非零。u 单分量已足以推出双场 B 不在完整参数切空间内。

若在一个有内点的实窗口上 B 等于某参数切向的 L² 函数，则由实解析性它在窗口内恒等；
固定实 y,t 后，对复 x 的亚纯延拓恒等，和上面的三阶极点矛盾。
因有限维切空间闭合，任何正权双场 L² 范数中的法向距离均严格正。

## 5. 有限 h 的更强函数不等价

对任何允许的 h>0，u_h 在复 x 上有三个不同的竖直极点族：
F 的留数为 +2，两个 G 的留数各为 −1。
\(\delta_h\ne0\)，因为 \(\chi_h=1\) 将推出 \(hK=0\)。
F 与任一 G 的极点族重合需 \(\gamma_h=1\) 或 \(\gamma_h=\chi_h\)，两者同样推出 K=0。
任意正则连续 N=1 场 u_0 只有两个不同的竖直极点族，留数为 +2、−2。
所以有限 h 解析物理 u_h 不能与任何正则实连续单孤子函数恒等。
当 h→0，两个 −1 极点族合并成 −2，这与二阶接近一致。

## 6. 适用边界

以上是精确解族的静态函数几何。它不允许通过更换目标初值宣称求解收益，
也不给共同连续初值演化误差的正下界。共同初值的初态修正、传播和实际边界响应必须另行处理。
本核对没有推进 PDE、数值扫描、采样拟合或多孤子扩展。
