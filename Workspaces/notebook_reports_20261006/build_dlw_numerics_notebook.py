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

以 DLW 单孤子与二孤子的解析解为参照，比较 SD、SD2 与 FD，以及固定网格与动网格。SD 直接推进双线性方程，采用隐式中点；SD2、FD 比较 Euler 与 RK4。''')
    code('imports')
    md('design', r'''## 1　模型与实验设计

连续 DLW 方程为

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}$$

采用 Sheng–Yu 原文的三组孤子参数，$a=2$、$c_i=1$，初相位为零。A、B 分别对应图 1(a)、1(b)，C 对应图 3；具体 $p_i,q_i$ 如下表。取 $\Delta t=0.000125$、$T=0.01$。''')
    code('config')
    md('exact-text', r'''### 1.1　孤子参照

记 $S_i=p_i+q_i$、$\omega_i=q_i^2-p_i^2$、$\ell_i=(p_i-a)^{-1}+(q_i+a)^{-1}$，并令 $\theta_i=S_ix+\omega_it+\ell_i y$。单孤子的 $g=1+e^{\theta_1}/S_1$；二孤子的

$$g=1+\frac{e^{\theta_1}}{S_1}+\frac{e^{\theta_2}}{S_2}
+\frac{(p_1-p_2)(q_1-q_2)e^{\theta_1+\theta_2}}
{(p_1+q_1)(p_1+q_2)(p_2+q_1)(p_2+q_2)}.$$

$f$ 在各指数项中加入因子 $\gamma_i=-(p_i-a)/(q_i+a)$。物理场取

$$u_*=2\partial_x(\log f-\log g),\qquad
v_*=2\partial_x\partial_y(\log f+\log g).$$

用对数和计算正系数 tau 函数；对数的一阶、二阶导数分别是指数率的加权均值、协方差。''')
    code('reference')
    cells.extend(build_spatial_cells(CELLS))
    md('time-text', r'''## 3　时间推进与误差评价

SD 使用第 2.1 节的隐式中点递推。SD2、FD 的 Euler 更新为 $z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n)$；RK4 使用同一右端的四个时间级，状态与节点同步更新。

在 $x\in[-10,10]$ 的 4001 个等距点及全部 $y$ 层上，三次样条重构数值场，计算

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_h(x,y,T)-f_*(x,y,T)|,\qquad f\in\{u,v\}.$$

三种方案从相同的物理初值 $u_*(0),v_*(0)$ 出发。''')
    code('time')
    md('space-text', r'''## 4　空间方案的比较

在均匀固定网格上比较三种方案。SD 使用隐式中点，SD2、FD 使用 RK4；时间步长均为 $0.000125$，终点均为 $T=0.01$。每行加粗值为最小误差。''')
    code('space_experiment')
    md('temporal-text', r'''## 5　时间算法的比较

在固定网格上比较 SD2、FD 的 Euler 与 RK4。''')
    code('time_experiment')
    md('order-text', r'''取 $\Delta t$、$\Delta t/2$、$\Delta t/4$，以相邻时间步长的数值场差估计时间阶：

$$p_f=\log_2\frac{\|f_{\Delta t}-f_{\Delta t/2}\|_{\infty,\mathcal G}}
{\|f_{\Delta t/2}-f_{\Delta t/4}\|_{\infty,\mathcal G}}.$$

下面分别计算 SD 隐式中点与 SD2 Euler 的时间观测阶。''')
    code('order')
    md('moving-text', r'''## 6　固定网格与动网格的比较

保持节点数、时间步长与各方案的时间算法一致，比较固定网格与动网格。SD 使用隐式中点，SD2、FD 使用 RK4。''')
    code('mesh_experiment')
    md('curve-text', r'''## 7　局部误差曲线

取 $x\in[-1,1]$，画出 $e_f(x)=\max_j|f_h(x,y_j,T)-f_*(x,y_j,T)|$。SD 使用隐式中点，SD2、FD 使用 RK4；蓝、橙、绿分别对应三种方案，同一场的两幅图使用相同纵轴尺度。''')
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
        primary_runs=24, time_order_additional_runs=12, self_contained=True,
        source_modules=['dlw_numeric_cells.py', 'sd_tau_cell.py', 'tau_report_cells.py',
                        'revise_dlw_structure.py'],
        original_model_references=['dlw_single_aligned_20260929/experiment.py',
        'dlw_sd2_uv_init_20260929/consistent_sd2.py', 'dlw_two_soliton_20260929/models.py',
        'dlw_two_soliton_20260929/reference.py', 'dlw_semidiscrete/numerics/lib/parametric_open.py',
        'dlw_semidiscrete/numerics/lib/solver.py', 'dlw_sd2_20260929/sd2.py'])
    (HERE/'dlw_build_validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    build()
