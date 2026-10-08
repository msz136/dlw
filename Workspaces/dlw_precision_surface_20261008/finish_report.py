from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],'mathtext.fontset':'stix','font.size':11})
rows=[]
for case in 'ABC':
    d=np.load(HERE/f'case_{case}.npz')
    r=json.loads((HERE/f'case_{case}.json').read_text())
    rows.append(f'<tr><td>{case}</td><td>{r["max_errors"]["u"]:.6g}</td><td>{r["max_errors"]["v"]:.6g}</td></tr>')
    fig,axs=plt.subplots(2,2,figsize=(11,9),layout='constrained')
    for row,key in enumerate(('u','v')):
        num,exact=d[key],d['exact_'+key]
        lo,hi=float(exact.min()),float(exact.max())
        levels=np.linspace(lo,hi,9)[1:-1]
        ax=axs[row,0]
        p=ax.pcolormesh(d['x'],d['y'],num,shading='auto',cmap='viridis',vmin=lo,vmax=hi,rasterized=True)
        ax.contour(d['x'],d['y'],num,levels=levels,colors='white',linewidths=.8)
        ax.contour(d['x'],d['y'],exact,levels=levels,colors='black',linewidths=.65,linestyles='dashed')
        fig.colorbar(p,ax=ax,label=key)
        ax.set_title(f'{key}: numerical field + matched contours')
        ax.legend(handles=[Line2D([0],[0],color='white',lw=1.2,label='Numerical contour'),Line2D([0],[0],color='black',ls='--',label='Exact contour')],facecolor='#777777',labelcolor='white',loc='upper right',fontsize=9)
        ax=axs[row,1]
        p=ax.pcolormesh(d['x'],d['y'],abs(num-exact),shading='auto',cmap='magma',vmin=0,rasterized=True)
        fig.colorbar(p,ax=ax,label=f'Absolute error in {key}',format='%.1e')
        ax.set_title(rf'$|{key}_h-{key}_*|$')
    for ax in axs.flat:
        ax.set(xlim=(-30,30),ylim=(-30,30),xlabel='$x$',ylabel='$y$')
        ax.set_aspect('equal')
    fig.suptitle(f'Case {case} | SD2 + RK4, fixed mesh | t = 0.01',fontsize=16)
    fig.savefig(HERE/f'case_{case}_contours.png',dpi=160)
    plt.close(fig)

papers=[
 {'title':'Efficient linearized local energy-preserving method for the Kadomtsev-Petviashvili equation','authors':'Jiaxiang Cai, Juan Chen, Min Chen','year':2022,'doi':'10.3934/dcdsb.2021139','url':'https://www.aimsciences.org/article/doi/10.3934/dcdsb.2021139?viewType=HTML','figures':'Fig. 2/3: full x,y surfaces and separate numerical/exact contours; Fig. 1 error history; Table 1 convergence.','figure_url':'https://data.aimsciences.org//aimsmath-data/DCDS-B/2022/5/PIC/1531-3492_2022_5_2441-3.jpg'},
 {'title':'Exact and numerical approaches for solitary and periodic waves in a (2+1)-dimensional breaking soliton system with adaptive moving mesh','authors':'Amer Ahmed, A. R. Alharbi, Haza S. Alayachi, Ishak Hashim','year':2025,'doi':'10.3934/math.2025380','url':'https://www.aimspress.com/article/id/67f79c36ba35de0692a8cb8e','figures':'Fig. 1-5: exact x,y surfaces at t=0; Fig. 6: numerical/exact profiles at fixed y=2, not full-plane accuracy; Fig. 7 convergence.','figure_url':'https://www.aimspress.com/aimspress-data/math/2025/4/PIC/math-10-04-380-g006.jpg'},
 {'title':'High precision numerical approach for the Davey-Stewartson II equation for Schwartz class initial data','authors':'Christian Klein, Ken McLaughlin, Nikola Stoilov','year':2020,'doi':'10.1098/rspa.2019.0864','url':'https://arxiv.org/html/1911.11721','figures':'Fig. 3/6: two-dimensional physical fields; Fig. 5/8: maximum error versus resolution. Schwartz examples use independent numerical inverse-scattering reference, not an analytical exact solution.'}
]
refs=ROOT/'Paper/refs/plotting_reference_search_20261008.json'
refs.parent.mkdir(parents=True,exist_ok=True)
refs.write_text(json.dumps({'searched_on':'2026-10-08','papers':papers},ensure_ascii=False,indent=2),encoding='utf-8')
sections=''
for case in 'ABC':
    sections+=f'<h2>Case {case}</h2><figure><img src="../Workspaces/dlw_precision_surface_20261008/case_{case}_comparison.png"><figcaption>物理场与绝对误差。上行为 u，下行为 v；左列彩色曲面为数值解，黑色网线为解析解；右列为同一采样点的绝对误差。</figcaption></figure><details><summary>查看二维等高线与误差图</summary><img src="../Workspaces/dlw_precision_surface_20261008/case_{case}_contours.png"><p>左列白实线为数值等高线，黑虚线为相同高度的解析等高线；右列为绝对误差，色标从零开始。</p></details>'
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 孤子场与数值精度：试画及论文参考</title><style>body{max-width:1040px;margin:48px auto;padding:0 22px;color:#242424;background:#faf9f6;font:18px/1.8 Georgia,"Times New Roman","SimSun",serif}h1{font-size:30px}h2{font-size:24px;margin-top:42px}h3{font-size:20px}img{max-width:100%;height:auto;background:white}figure{margin:20px 0}figcaption{font-size:15px;color:#555}a{color:#225e88}table{border-collapse:collapse;width:100%;margin:22px 0}td,th{padding:9px;border-bottom:1px solid #ccc;text-align:left}summary{cursor:pointer}small{color:#666}</style>
<h1>DLW 孤子场与数值精度</h1><p>固定 t=0.01，保留 x、y 两个空间方向。每个算例分别展示 u、v 的数值／解析叠加和绝对误差；另附二维等高线对照。以下数值场均来自 SD2＋RK4 固定网格的实际计算。</p>
<p>计算域 x∈[−40,40)、y∈[−30,30)，展示 x、y∈[−30,30]；Δx=0.15625、h=0.125、Δt=0.000125，共推进80步。只扩大实际空间范围，格距与时间步保持原值。下表取展示采样点上的最大绝对误差，不是全方法比较或收敛阶证明。</p>
<table><tr><th>算例</th><th>max |u数值−u解析|</th><th>max |v数值−v解析|</th></tr>'''+''.join(rows)+'''</table>
<p>A 是单条负波谷，B 的 u 是单条正波脊、v 是负波谷。C 的两条波脊在宽 y 范围内可以分辨：原来的窄 y 截面主要截到了相互作用中心。二孤子不要求每一个固定 y 的一维切片都出现两个峰，因此 t=0.01 可以用于形态与精度的同步展示。三维曲面的遮挡及显示抽样会影响细部判断，细部对照请结合等高线图。</p>'''+sections+'''
<h2>GSG 论文到底固定了什么？</h2><p>GSG 的物理未知量是 u(x,t)。其中 y、τ 来自 hodograph 换元：dy=r dx−r cos(u)dt，dτ=dt；y 不是额外的物理空间方向。Fig.1 在 t=5、10 叠加数值与解析的 x 曲线，Fig.2 在 t=5 单独画绝对误差曲线，横轴标作辅助坐标 y；它仍然是一维误差剖面。这里借鉴它“物理场对照＋误差”的结构，将 DLW 的 x 曲线扩展为完整 x,y 曲面。</p>
<figure><img src="../Workspaces/dlw_precision_surface_20261008/gsg_original_figures.png"><figcaption>本地 Numerical_Algorithms_gsg (1).pdf，第15页（印刷页365），Fig.1/2。<a href="../Paper/sources/Numerical_Algorithms_gsg%20(1).pdf">原论文</a></figcaption></figure>
<h2>二维数值论文可以怎样照着画？</h2>
<h3>1. KP：曲面、数值等高线、解析等高线</h3><p>Cai、Chen、Chen（2022）的 Fig.2/3 在固定时刻保留完整 x,y 平面，按“曲面／数值等高线／解析等高线”并排；Fig.1 给误差随时间，Table 1 给网格加密误差与收敛阶。这篇最适合作为 DLW 的二维图式参考。上面的等高线候选进一步将相同高度的数值／解析线叠加，并配独立误差图。</p><p><a href="https://www.aimsciences.org/article/doi/10.3934/dcdsb.2021139?viewType=HTML">论文与图注</a> · <a href="https://data.aimsciences.org//aimsmath-data/DCDS-B/2022/5/PIC/1531-3492_2022_5_2441-3.jpg">Fig.3 原图</a></p>
<h3>2. Breaking soliton：固定 y 的数值／解析截面</h3><p>Ahmed 等（2025）虽然研究 (2+1) 维系统，但 Fig.6 的数值对照固定 y=2，以浅蓝实线表示数值解、黑虚线表示解析解；图中另显示非均匀网格。Fig.1—5 是固定 t=0 的解析曲面，Fig.7 给误差与分辨率的关系。这种截面适合补充峰高和相位对照，不能单凭该截面判断整个 x,y 平面的误差。</p><p><a href="https://www.aimspress.com/article/id/67f79c36ba35de0692a8cb8e">论文与图注</a> · <a href="https://www.aimspress.com/aimspress-data/math/2025/4/PIC/math-10-04-380-g006.jpg">Fig.6 原图</a></p>
<h3>3. Davey–Stewartson II：场图与精度收敛分别展示</h3><p>Klein、McLaughlin、Stoilov（2020）在 Fig.3/6 展示二维物理场，在 Fig.5/8 展示最大误差随 Fourier 分辨率的下降。Schwartz 初值算例的参考来自独立的数值逆散射求解，并非解析精确解。可借鉴其精度论证结构：场图看形态，误差图看位置，收敛图或表看精度阶。</p><p><a href="https://arxiv.org/html/1911.11721">论文全文与图</a></p>
<h2>2HS 如何同步？</h2><p>2HS 的物理场是 u、ρ，变量为 x,t。固定 t 时采用 GSG 式数值／解析曲线叠加＋误差曲线；若需要盒式曲面，底面使用 x,t，配套展示数值场与误差，不能将 t 轴标为 y。<a href="../Workspaces/paper_plot_reference_20261008/numerical_paper_layout.png">已有实际数值／解析截面对照</a>；<a href="../Workspaces/paired_field_preview_20261008/hs_box.png">已有 x,t 盒式场／误差候选</a>。</p><p>当前扩展 x∈[−5,5] 的 2HS 试算在 t=0.5 的 u 右尾出现明显偏差，最大绝对误差约0.279。它应保留在误差展示中，不能解释为孤子波峰。本轮只试画与查阅文献，Notebook 保持原样。</p></html>'''
out=ROOT/'report/dlw_precision_surface_preview.html'
out.write_text(html,encoding='utf-8')
notes=' **宽域实际数值与检索：** 完成 A/B/C 的 SD2＋RK4 固定网格宽域计算，T=.01、L=80、nx=512、yhalf=30，保持 Δx=.15625/h=.125/dt=.000125。各算例一张 u/v 数值曲面＋解析网线／绝对误差四面板图，另附数值／解析等高线叠加及误差图；最大 u/v 误差 A=.0117614/.00726232、B=.000128786/.0000618617、C=.000204436/.000132186。GSG y 为 hodograph 辅助坐标，物理变量 x,t；Fig1 t=5/10，Fig2 t=5。检索并核对 KP（2022，全 xy 曲面及数值/解析等高线）、breaking soliton（2025，数值对照固定 y=2）与 DSII（2020，独立逆散射数值参考及精度收敛）。见 [试画与文献报告](report/dlw_precision_surface_preview.html)，原始数值及核验在 Workspaces/dlw_precision_surface_20261008/，文献元数据在 Paper/refs/plotting_reference_search_20261008.json；Notebook 未修改。'
log=ROOT/'PROGRESS_LOG.md'
s=log.read_text(encoding='utf-8')
anchor='见 [原图与试画](Workspaces/paper_plot_reference_20261008/paper_vs_preview.png)。'
if ' **宽域实际数值与检索：**' not in s:
    assert anchor in s
    log.write_text(s.replace(anchor,anchor+notes,1),encoding='utf-8')
index=ROOT/'FILE_INDEX.md'
s=index.read_text(encoding='utf-8')
if 'dlw_precision_surface_preview.html' not in s:
    s+='\n- `report/dlw_precision_surface_preview.html`：A/B/C 实际数值／解析场与绝对误差、GSG 变量核对及二维数值绘图论文参考。\n- `Workspaces/dlw_precision_surface_20261008/`：`run_preview.py`、`finish_report.py`；A/B/C 各自的 `.npz` 数值/解析缓存、`.json` 计算参数与误差、`_comparison.png` 曲面图和 `_contours.png` 等高线图；`gsg_original_figures.png`、`validation.json`。\n- `Paper/refs/plotting_reference_search_20261008.json`：KP、breaking soliton、DSII 三篇一手文献的 DOI、图号与展示范围。\n'
    index.write_text(s,encoding='utf-8')
for name,expected in [('DLW数值分析report.ipynb','ec01306900b061b3cc21ec84e3495d2800cb0e1b3ba36ed1a42055f0dceda4a9'),('2HS数值分析report.ipynb','53f670a87104a10c87aa0513970f4cd2ac904d2a59450b0d462e8d9133a06b08')]:
    assert hashlib.sha256((ROOT/'notebook'/name).read_bytes()).hexdigest()==expected
print(out)
