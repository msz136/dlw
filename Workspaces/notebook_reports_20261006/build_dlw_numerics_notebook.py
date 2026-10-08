"""Build the native DLW report; scientific outputs are produced by execution."""
from pathlib import Path
import hashlib
import json
import nbformat as nbf
from dlw_numeric_cells import CELLS
from revise_dlw_structure import build_spatial_cells

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT/'notebook'/'DLW数值分析report.ipynb'

def build():
    cells = []
    def md(name, text):
        cells.append(nbf.v4.new_markdown_cell(text.strip(), id='dlw-'+name))
    def code(name):
        cells.append(nbf.v4.new_code_cell(CELLS[name].strip(), id='dlw-'+name))
    md('title', r'''# DLW 数值分析 report

以 DLW 单孤子与二孤子的解析解为参照，采用两种可积半离散方法（SD、SD2）和一种直接差分方法（FD）计算数值解，比较固定网格、动网格及不同时间算法下的误差。''')
    code('imports')
    md('design', r'''## 1　模型与实验设计

连续 DLW 方程为

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}$$

采用 Sheng–Yu 原文的三组孤子参数，$a=2$、$c_i=1$，初相位为零。A、B 分别对应图 1(a)、1(b)，C 对应图 3；具体 $p_i,q_i$ 如下表。取 $\Delta t=0.000125$、$T=0.01$。''')
    code('config')
    md('exact-text', r'''### 1.1　孤子精确解

$x,y$ 为空间坐标，$t$ 为时间。由表中的 $p_i,q_i$ 及 $a=2$，确定

$$S_i=p_i+q_i,\qquad \omega_i=q_i^2-p_i^2,\qquad
\ell_i=\frac1{p_i-a}+\frac1{q_i+a},\qquad
\gamma_i=-\frac{p_i-a}{q_i+a}.$$

在给定的 $(x,y,t)$ 处，记

$$\theta_i(x,y,t)=S_ix+\omega_it+\ell_i y,\qquad
E_i(x,y,t)=e^{\theta_i(x,y,t)}.$$

单孤子的解析式为

$$\begin{aligned}
g(x,y,t)&=1+\frac{E_1(x,y,t)}{S_1},\\
f(x,y,t)&=1+\frac{\gamma_1E_1(x,y,t)}{S_1}.
\end{aligned}$$

二孤子记

$$C_{12}=\frac{(p_1-p_2)(q_1-q_2)}
{(p_1+q_1)(p_1+q_2)(p_2+q_1)(p_2+q_2)},$$

则

$$\begin{aligned}
g(x,y,t)&=1+\frac{E_1(x,y,t)}{S_1}+\frac{E_2(x,y,t)}{S_2}
+C_{12}E_1(x,y,t)E_2(x,y,t),\\
f(x,y,t)&=1+\frac{\gamma_1E_1(x,y,t)}{S_1}+\frac{\gamma_2E_2(x,y,t)}{S_2}
+\gamma_1\gamma_2C_{12}E_1(x,y,t)E_2(x,y,t).
\end{aligned}$$

精确解由这两个解析函数直接求导：

$$\begin{aligned}
u_*(x,y,t)&=2\partial_x[\log f(x,y,t)-\log g(x,y,t)],\\
v_*(x,y,t)&=2\partial_x\partial_y[\log f(x,y,t)+\log g(x,y,t)].
\end{aligned}$$

展开对数导数，即可直接计算其值：

$$\begin{aligned}
u_*(x,y,t)&=2\left[\frac{f_x(x,y,t)}{f(x,y,t)}-\frac{g_x(x,y,t)}{g(x,y,t)}\right],\\
v_*(x,y,t)&=2\Bigg[\frac{f_{xy}(x,y,t)}{f(x,y,t)}
-\frac{f_x(x,y,t)f_y(x,y,t)}{f(x,y,t)^2}\\
&\qquad+\frac{g_{xy}(x,y,t)}{g(x,y,t)}
-\frac{g_x(x,y,t)g_y(x,y,t)}{g(x,y,t)^2}\Bigg].
\end{aligned}$$

这些导数由指数项的解析式得到：$\partial_xE_i=S_iE_i$、$\partial_yE_i=\ell_iE_i$、$\partial_x\partial_yE_i=S_i\ell_iE_i$；交叉项 $E_1E_2$ 的 $x,y$ 指数率分别为 $S_1+S_2$、$\ell_1+\ell_2$。给定 $(x,y,t)$，计算相应的 $f,g$ 及其导数，再代入上式，即得到该点的精确参照值。

精确参照由 `Exact` 类按上述解析式计算；调用 `uv(js, x, t)`，返回指定空间点与时刻的精确参照值。''')
    code('reference')
    cells.extend(build_spatial_cells(CELLS))
    md('time-text', r'''## 3　时间推进与误差评价

三种方案分别以第 2 节的离散右端 $\mathcal F$ 推进。Euler 更新为 $z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n)$；RK4 的递推为

$$\begin{aligned}
k_1&=\mathcal F(t_n,z^n),\\
k_2&=\mathcal F\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}k_1\right),\\
k_3&=\mathcal F\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}k_2\right),\\
k_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t k_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4).
\end{aligned}$$

状态与节点使用同一时间算法同步更新。

时间算法比较另加入 Crank–Nicolson（C–N）：

$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$

这是二阶隐式梯形法，采用迭代求解并检查隐式方程残差。

在 $x\in[-10,10]$ 的 4001 个等距点及全部 $y$ 层上，三次样条重构数值场，计算

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_h(x,y,T)-f_*(x,y,T)|,\qquad f\in\{u,v\}.$$

三种方案从相同的物理初值 $u_*(0),v_*(0)$ 出发。''')
    code('time')
    md('space-text', r'''## 4　空间方案的比较

在均匀固定网格上比较三种方案，时间算法统一为 RK4，时间步长为 $0.000125$，终点为 $T=0.01$。每行加粗值为最小误差。''')
    code('space_experiment')
    md('temporal-text', r'''## 5　时间算法的比较

在固定网格上分别比较 SD、SD2、FD 的 Euler、RK4 与 Crank–Nicolson。保持相同的初值、空间格距、时间步长 $\Delta t=0.000125$ 和终点 $T=0.01$。其他实验的时间算法保持原设置。''')
    code('time_experiment')
    md('order-text', r'''取 $\Delta t$、$\Delta t/2$、$\Delta t/4$，以相邻时间步长的数值场差估计时间阶：

$$p_f=\log_2\frac{\|f_{\Delta t}-f_{\Delta t/2}\|_{\infty,\mathcal G}}
{\|f_{\Delta t/2}-f_{\Delta t/4}\|_{\infty,\mathcal G}}.$$

下面计算 SD 与 SD2 在 Euler 更新下的时间观测阶。''')
    code('order')
    md('moving-text', r'''## 6　固定网格与动网格的比较

保持节点数与时间步长一致，三种方案均使用 RK4，比较固定网格与动网格。''')
    code('mesh_experiment')
    md('curve-text', r'''## 7　局部误差曲线

取 $x\in[-1,1]$，画出 $e_f(x)=\max_j|f_h(x,y_j,T)-f_*(x,y_j,T)|$。三种方案均使用 Euler；蓝、橙、绿分别对应 SD、SD2、FD，同一场的两幅图使用相同纵轴尺度。''')
    code('curves')
    md('conclusion-text', r'''## 8　结果

配对表给出空间方案的最小误差与动网格相对固定网格的误差比；比值小于 1 表示该场误差降低。''')
    code('summary')
    md('limits', r'''参考资料：H.-H. Sheng and G.-F. Yu, *Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system*, Physica D 432 (2022), 133140。''')
    nb = nbf.v4.new_notebook(cells=cells, metadata={
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
        'colab': {'name': DEST.name, 'provenance': []},
        'report': {'source_html': str(ROOT/'dlw_numerical.html'), 'self_contained': True,
                   'spatial_accuracy_order': 2,
                   'spatial_stencil': 'three-point centered D1 and direct D2',
                   'runtime': 'Python; no Lean or external project files required'}})
    from static_field_plots import apply_dlw
    nb = apply_dlw(nb)
    cells = nb.cells
    nbf.validate(nb)
    DEST.parent.mkdir(exist_ok=True)
    nbf.write(nb, DEST)
    manifest = dict(notebook=str(DEST), cells=len(cells), code_cells=sum(c.cell_type=='code' for c in cells),
        source_html_sha256=hashlib.sha256((ROOT/'dlw_numerical.html').read_bytes()).hexdigest(),
        notebook_sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),
        configuration={'nx':256,'h':.125,'dt':.000125,'T':.01,'L':40.,'eval_points':4001},
        spatial_discretization={'order':2,'D1':'(f[i+1]-f[i-1])/(2*dx)',
                                'D2':'(f[i+1]-2*f[i]+f[i-1])/dx**2',
                                'moving':'Dxx=J**-2*Dxxi-Jxi*J**-3*Dxi'},
        primary_runs=36, time_order_additional_runs=12, self_contained=True,
        source_modules=['dlw_numeric_cells.py', 'sd_nonlinear_cell.py',
                        'revise_dlw_structure.py'],
        original_model_references=['dlw_single_aligned_20260929/experiment.py',
        'dlw_sd2_uv_init_20260929/consistent_sd2.py', 'dlw_two_soliton_20260929/models.py',
        'dlw_two_soliton_20260929/reference.py', 'dlw_semidiscrete/numerics/lib/parametric_open.py',
        'dlw_semidiscrete/numerics/lib/solver.py', 'dlw_sd2_20260929/sd2.py'])
    (HERE/'dlw_build_validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    build()
