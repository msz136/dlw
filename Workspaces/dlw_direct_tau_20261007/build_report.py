"""Paper-style report of the direct bilinear recurrence and completed runs."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from direct_tau import GramTau

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE/'out'
REPORT = ROOT/'report/dlw_direct_tau.html'

def main():
    results = json.loads((OUT/'results.json').read_text())
    audit = json.loads((HERE/'validation.json').read_text())
    assert audit['success'] and all(r['completed'] for r in results)
    plt.rcParams.update({'font.family':'DejaVu Serif', 'font.size':10,
                         'axes.spines.top':False, 'axes.spines.right':False})
    fig, axes = plt.subplots(3, 2, figsize=(10, 8.5), layout='constrained')
    table, ordertable, spatial = [], [], []
    for row, case in enumerate(('A', 'B', 'C')):
        variants = {}
        for nx in (256, 512):
            record = next(r for r in results if r['case']==case and r['config']['intervals']==nx
                          and r['config']['dt']==.000125)
            variants[nx] = record
            with np.load(OUT/f'{case}_n{nx}_dt1.npz') as data:
                exact = GramTau(case).fields(data['js'], data['x'], .01)
                mask = abs(data['x']) <= 10
                for column, field in enumerate(('u', 'v')):
                    curve = abs(data[field]-exact[column]).max(axis=0)
                    axes[row, column].semilogy(data['x'][mask], np.maximum(curve[mask], 1e-15),
                        color='#264c78' if nx==256 else '#a93d28',
                        label=rf'$N_x={nx}$', lw=1.1)
        for column, field in enumerate(('u', 'v')):
            axes[row, column].set(title=rf'Case {case}: $e_{field}(x)$', xlabel='$x$', ylabel='Maximum absolute error')
            axes[row, column].legend(frameon=False, fontsize=9)
        a, b = variants[256]['final'], variants[512]['final']
        table.append(f"<tr><th>{case}</th><td>{a['u']:.5e}</td><td>{a['v']:.5e}</td>"
                     f"<td>{b['u']:.5e}</td><td>{b['v']:.5e}</td></tr>")
        pu, pv = [next(o['observed_order'] for o in audit['temporal_orders'] if o['case']==case and o['field']==f)
                  for f in ('u', 'v')]
        ordertable.append(f'<tr><th>{case}</th><td>{pu:.3f}</td><td>{pv:.3f}</td></tr>')
        spatial.append(dict(case=case, u_error_reduction=a['u']/b['u'], v_error_reduction=a['v']/b['v']))
    fig.savefig(OUT/'field_errors.png', dpi=200)
    plt.close(fig)
    validation = audit['independent_raw_bilinear_audits']
    residual = max(max(r['Bminus'], r['Bplus']) for r in validation)
    html = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DLW：直接双线性 τ 推进</title>
<link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css">
<style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#202020;font-family:"SimSun","Songti SC",serif;line-height:1.8}
main{max-width:980px;margin:auto;padding:48px 32px 64px}h1{font-size:29px;font-weight:600;line-height:1.4;margin:0 0 12px}
h2{font-size:21px;margin:36px 0 12px;font-weight:600}p{margin:12px 0}a{color:#254e78;text-underline-offset:3px}
.meta{font-size:14px;color:#555}.math-display{overflow-x:auto;padding:2px 0}.katex{font-size:1.05em}
.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px;text-align:right;margin:12px 0}
th,td{padding:9px 12px;white-space:nowrap;border-bottom:1px solid #ddd}thead th{border-top:1.5px solid #222;border-bottom:1px solid #222}
tbody th{text-align:left}img{width:100%;height:auto;display:block;margin-top:24px}figcaption{font-size:14px;color:#555}
.note{font-size:15px;color:#444}.rule{border-top:1px solid #ccc;margin-top:30px;padding-top:12px}
@media(max-width:600px){main{padding:28px 18px}h1{font-size:24px}.katex{font-size:.95em}}
@media print{main{padding:0;max-width:none}h2{break-after:avoid}table,img{break-inside:avoid}}
</style></head><body><main>
<p class="meta">DLW 数值分析 · 2026-10-07</p><h1>直接在双线性方程上推进 τ</h1>
<p>保留 \(F_j,G_j\) 为演化变量。两条方程在隐式中点离散后，可沿格点逐层求解两个线性系统。</p>

<h2>1　从 \(j\) 到 \(j+1\)</h2>
<p>令 \(s_\pm=a\pm h/2\)，原方程为</p>
\[B_{s_-}F_j\!\cdot G_j=0,\qquad B_{s_+}F_j\!\cdot G_{j+1}=0,\qquad B_s=D_x^2+D_t+2sD_x.\]
<p>把空间部分记为</p>
\[\mathcal L_s(F,G)=F_{xx}G-2F_xG_x+FG_{xx}+2s(F_xG-FG_x).\]
<p>由于 \(D_tF\cdot G=F_tG-FG_t\)，两条方程依次给出</p>
\[\begin{aligned}
F_{j,t}&=\frac{F_jG_{j,t}-\mathcal L_{s_-}(F_j,G_j)}{G_j},\\
G_{j+1,t}&=\frac{G_{j+1}F_{j,t}+\mathcal L_{s_+}(F_j,G_{j+1})}{F_j}.
\end{aligned}\]
<p>给定当前全部层的初值和下侧时间边界，先算 \(F_{j,t}\)，再算 \(G_{j+1,t}\)，随后进入下一层。这里递推的是时间演化；\(G_{j+1}\) 的当前值也来自已给的初值或前一时间步。</p>

<h2>2　实际采用的时间递推</h2>
<p>记 \(\bar F=(F^{n+1}+F^n)/2\)、\(\delta_tF=(F^{n+1}-F^n)/\Delta t\)，对 \(G\) 同样定义。中点格式为</p>
\[\begin{aligned}
\bar G_j\delta_tF_j-\bar F_j\delta_tG_j
+\mathcal L_{s_-}(\bar F_j,\bar G_j)&=0,\\
\bar G_{j+1}\delta_tF_j-\bar F_j\delta_tG_{j+1}
+\mathcal L_{s_+}(\bar F_j,\bar G_{j+1})&=0.
\end{aligned}\]
<p>已知 \(G_j^n,G_j^{n+1}\) 时，第一式对 \(F_j^{n+1}\) 线性；得到 \(F_j^{n+1}\) 后，第二式对 \(G_{j+1}^{n+1}\) 线性。每个时间步的求解顺序为</p>
\[G_{j_L}^{n+1}\longrightarrow F_{j_L}^{n+1}\longrightarrow G_{j_L+1}^{n+1}
\longrightarrow F_{j_L+1}^{n+1}\longrightarrow\cdots.\]
<p>时间项还可直接化成 \((F^{n+1}G^n-F^nG^{n+1})/\Delta t\)。因此每层只需两次稀疏线性求解，24 层每步共 48 次。</p>
<p>空间取四阶中心 \(D_1\) 及 \(D_2=D_1D_1\)。τ 用对数存储，线性求解的未知量为新旧 τ 比值；所求残差仍是上述原始 τ 中点格式。</p>

<h2>3　完整运行结果</h2>
<p>\(x\in[-20,20]\) 等分 256 份，含 257 个端点节点；\(y\in[-1.5,1.5]\) 等分 24 份。取 \(a=2\)、\(h=0.125\)、\(\Delta t=0.000125\)、\(T=0.01\)，主运行共 80 步。</p>
<p>A：\((p,q)=(1,2)\)；B：\((p,q)=(4,-3)\)；C：\((p_1,p_2)=(6,4)\)、\((q_1,q_2)=(-5,-3)\)。初值取有限 \(h\) 的 Gram τ；下侧 \(G_{-12}\) 及两侧各四个 \(x\) 节点取对应解析值，内部 τ 由数值格式推进。</p>
<p>恢复物理场</p>
\[u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.\]
<p>以下为 \(x\in[-10,10]\) 原生节点及全部 \(y\) 层上的终点最大绝对误差，参照为有限 \(h\) Gram τ 诱导的物理场。</p>
<div class="scroll"><table><thead><tr><th>算例</th><th>\(E_u\)，256份</th><th>\(E_v\)，256份</th><th>\(E_u\)，512份</th><th>\(E_v\)，512份</th></tr></thead><tbody>__RESULT_ROWS__</tbody></table></div>
<p>三组算例及全部 12 组主运行、时间加密和空间加密运行均到达 \(T=0.01\)。取 \(\Delta t,\Delta t/2,\Delta t/4\)，以相邻终点场差估计时间阶：</p>
\[p_f=\log_2\frac{\|f_{\Delta t}-f_{\Delta t/2}\|_\infty}{\|f_{\Delta t/2}-f_{\Delta t/4}\|_\infty}.\]
<div class="scroll"><table><thead><tr><th>算例</th><th>\(p_u\)</th><th>\(p_v\)</th></tr></thead><tbody>__ORDER_ROWS__</tbody></table></div>
<p>独立差分模板对带扰动的一步更新检验两条原始双线性残差，归一化残差最大为 __RESIDUAL__；全部时间步的缩放线性方程残差最大为 __LINEAR__。</p>
<figure><img src="../Workspaces/dlw_direct_tau_20261007/out/field_errors.png" alt="A、B、C三组算例的u、v终点局部误差，比较256与512份网格"><figcaption>局部误差 \(e_f(x)=\max_j|f_j^{\rm num}(x,T)-f_j^*(x,T)|\)。蓝色为 256 份，红色为 512 份。</figcaption></figure>
<p class="note">这里的下侧 τ 边界与原 SD 报告的下层 \(u\) 边界不同；参照也采用有限 \(h\) 的双线性解。表中结果用于评价本方案的误差和加密收敛，不据此作旧方案的优劣排名。此短时实验尚不建立一般稳定性或全离散可积性结论。</p>
<p class="rule"><a href="../Workspaces/dlw_direct_tau_20261007/direct_tau.py">数值实现</a> · <a href="../Workspaces/dlw_direct_tau_20261007/validation.json">验证数据</a> · <a href="../dlw_numerical.html">原 DLW 数值报告</a></p>
</main></body></html>'''
    html = html.replace('__RESULT_ROWS__', ''.join(table)).replace('__ORDER_ROWS__', ''.join(ordertable))
    html = html.replace('__RESIDUAL__', f'{residual:.2e}').replace('__LINEAR__', f"{audit['maximum_linear_residual']:.2e}")
    (HERE/'report_source.html').write_text(html, encoding='utf-8')
    (HERE/'report_summary.json').write_text(json.dumps(dict(all_completed=True, spatial_reductions=spatial,
        report=str(REPORT), source=str(HERE/'report_source.html')), indent=2)+'\n', encoding='utf-8')
    print(str(HERE/'report_source.html'))

if __name__ == '__main__':
    main()
