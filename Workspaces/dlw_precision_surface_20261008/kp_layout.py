"""KP Fig.3 layout applied to cached DLW runs; no PDE rerun or notebook edit."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],'mathtext.fontset':'stix','font.size':12})
data={}
for case in 'ABC':
    d=np.load(HERE/f'case_{case}.npz')
    x,y=d['x'],d['y'];X,Y=np.meshgrid(x,y)
    fig=plt.figure(figsize=(14,8),layout='constrained')
    gs=fig.add_gridspec(2,3,width_ratios=(1.2,1,1))
    for row,key in enumerate(('u','v')):
        num,exact=d[key],d['exact_'+key]
        lo,hi=min(float(num.min()),float(exact.min())),max(float(num.max()),float(exact.max()))
        norm=Normalize(lo,hi);levels=np.linspace(lo,hi,13)[1:-1]
        ax=fig.add_subplot(gs[row,0],projection='3d')
        ax.plot_surface(X[::2,::2],Y[::2,::2],num[::2,::2],cmap='jet',norm=norm,rcount=len(y)//2,ccount=len(x)//2,linewidth=0,antialiased=False)
        ax.set(xlabel='$x$',ylabel='$y$',zlabel=f'${key}$',xlim=(-30,30),ylim=(-30,30))
        ax.view_init(28,-62);ax.set_box_aspect((1.2,1,.85))
        ax.set_title(f'{key}: numerical surface')
        for axis in (ax.xaxis,ax.yaxis,ax.zaxis):axis.set_major_locator(MaxNLocator(4))
        for col,z,title in [(1,num,'Numerical contours'),(2,exact,'Exact contours')]:
            ax=fig.add_subplot(gs[row,col])
            cs=ax.contour(x,y,z,levels=levels,cmap='jet',norm=norm,linewidths=1.1)
            ax.set(xlabel='$x$',ylabel='$y$',xlim=(-30,30),ylim=(-30,30),title=f'{key}: {title}')
            ax.set_aspect('equal');ax.grid(color='#dddddd',lw=.4,alpha=.45)
            if col==2:
                bar=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap='jet'),ax=ax,fraction=.04,pad=.02)
                bar.set_label(key)
    fig.suptitle(f'DLW Case {case} | KP-inspired layout | t=0.01\nSD2 + RK4, fixed mesh',fontsize=18)
    fig.savefig(HERE/f'case_{case}_kp.png',dpi=160,bbox_inches='tight')
    plt.close(fig)
    # Display decimation only. Full arrays remain the error-statistic source.
    ix=np.unique(np.r_[np.arange(0,len(x),3),len(x)-1])
    iy=np.unique(np.r_[np.arange(0,len(y),3),len(y)-1])
    data[case]={'x':x[ix].tolist(),'y':y[iy].tolist()}
    for key in ('u','v'):
        for kind,z in [('numerical',d[key]),('exact',d['exact_'+key]),('error',abs(d[key]-d['exact_'+key]))]:
            data[case][key+'_'+kind]=z[np.ix_(iy,ix)].tolist()

original='https://data.aimsciences.org/aimsmath-data/DCDS-B/2022/5/PIC/1531-3492_2022_5_2441-3.jpg'
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KP 原图与 DLW 试画</title><style>body{max-width:1220px;margin:38px auto;padding:0 22px;background:#faf9f6;color:#222;font:18px/1.75 Georgia,"Times New Roman","SimSun",serif}h1{font-size:30px}h2{font-size:24px;margin-top:38px}img{max-width:100%;height:auto}figure{margin:20px 0}figcaption{font-size:15px;color:#555}a{color:#225e88}label{display:inline-block;margin-right:20px}select{padding:6px;font:inherit}#rotate{height:670px;background:white}#status{font-size:15px;color:#555}input{vertical-align:middle}details{margin:20px 0}summary{cursor:pointer}@media(max-width:600px){#rotate{height:500px}} </style>
<h1>KP 的画法，放到 DLW 上</h1><p>KP 的 Fig.3 固定 t=20，在同一个 x,y 平面上依次给出三维曲面、数值等高线、解析等高线；Fig.2 用同样的三列布局排列多个时刻。数值与解析分开画，避免曲面和网线互相遮挡。它另用 Fig.1 的误差曲线及 Table 1 的收敛表评估精度。<a href="https://www.aimsciences.org/article/doi/10.3934/dcdsb.2021139?viewType=HTML">论文与图注</a></p>
<h2>KP 原图 · Fig.3</h2><figure><img src="'''+original+'''" style="width:740px" alt="KP Fig.3：曲面、数值等高线、解析等高线" onerror="this.hidden=true;document.getElementById('remoteNote').hidden=false"><figcaption>Cai、Chen、Chen，DCDS-B 27(5), 2441–2453 (2022)，DOI 10.3934/dcdsb.2021139。图由期刊网站直接加载。<a href="'''+original+'''">打开原图</a></figcaption><p id="remoteNote" hidden>期刊原图未能加载，请使用上方原图链接查看。</p></figure>
<h2>DLW · 同样的三列布局</h2><p>以下使用已有实际数值结果：SD2＋RK4，固定网格，t=0.01。每个算例上行为 u，下行为 v；左列只画数值曲面，中列画数值等高线，右列画解析等高线。每一行的数值／解析等高线使用完全相同的高度与色标，颜色不再代表不同解。误差图另列，以免叠加遮挡。</p>
<p>A 是单孤子负波谷；B 的 u 是单孤子正波脊、v 是负波谷；C 是两条相互作用的波脊。宽 y 范围可以显示 C 的两条分支，窄 y 范围主要截到相互作用中心。我们保持 t=0.01；原图的 KP lump 与 DLW 线孤子形态不同，这里借用的是展示布局。</p>'''
for case in 'ABC':
    html+=f'<h3>Case {case}</h3><figure><img src="../Workspaces/dlw_precision_surface_20261008/case_{case}_kp.png"><figcaption>曲面与两个等高线面板分别展示。<a href="../Workspaces/dlw_precision_surface_20261008/case_{case}_contours.png">查看独立绝对误差图</a></figcaption></figure>'
html+='''<h2>可旋转预览</h2><p>拖动曲面可旋转，滚轮可缩放；工具栏可以重置视角及导出图像。数值场、解析场和误差可以切换，默认使用单一蓝色曲面。x、y 范围只调整现有快照的展示，不重跑求解器。时间固定为0.01。</p>
<label>算例 <select id="case"><option>A</option><option>B</option><option selected>C</option></select></label><label>场 <select id="field"><option>u</option><option>v</option></select></label><label>显示 <select id="kind"><option value="numerical">数值场</option><option value="exact">解析场</option><option value="error">绝对误差</option></select></label><br>
<label>x 范围 ±<input type="range" id="xhalf" min="5" max="30" step="5" value="30"><output id="xout">30</output></label><label>y 范围 ±<input type="range" id="yhalf" min="5" max="30" step="5" value="30"><output id="yout">30</output></label>
<p id="status">正在加载旋转图。交互预览使用 Plotly.js，需要联网；上方静态试画可离线查看。</p><div id="rotate"></div>
<p>后续 Notebook 可以把展示范围、配色和视角放在末尾的独立绘图单元，读取已经算好的快照；若改变时间或扩大计算域，则需要新的数值结果。本轮只制作独立预览，Notebook 未修改。</p>
<script id="snapshot" type="application/json">'''+json.dumps(data,separators=(',',':'))+'''</script>
<script src="https://cdn.plot.ly/plotly-3.1.0.min.js" onerror="document.getElementById('status').textContent='交互库未能加载；上方静态图仍可查看。'"></script><script>
const samples=JSON.parse(document.getElementById('snapshot').textContent);
function draw(){
 if(!window.Plotly)return;
 const c=document.getElementById('case').value,f=document.getElementById('field').value,k=document.getElementById('kind').value,d=samples[c];
 const xh=Number(document.getElementById('xhalf').value),yh=Number(document.getElementById('yhalf').value);
 document.getElementById('xout').textContent=xh;document.getElementById('yout').textContent=yh;
 const ix=d.x.map((v,i)=>i).filter(i=>Math.abs(d.x[i])<=xh),iy=d.y.map((v,i)=>i).filter(i=>Math.abs(d.y[i])<=yh);
 const z=iy.map(j=>ix.map(i=>d[f+'_'+k][j][i]));
 const trace={type:'surface',x:ix.map(i=>d.x[i]),y:iy.map(i=>d.y[i]),z:z,showscale:k==='error',colorscale:k==='error'?'Magma':[[0,'#4b8ab6'],[1,'#4b8ab6']],colorbar:{title:{text:'绝对误差'}},hovertemplate:'x=%{x:.3f}<br>y=%{y:.3f}<br>值=%{z:.6g}<extra></extra>',lighting:{ambient:.7,diffuse:.8,specular:.15}};
 const title='Case '+c+' · '+f+' · '+({numerical:'数值场',exact:'解析场',error:'绝对误差'})[k]+' · t=0.01';
 Plotly.react('rotate',[trace],{title:{text:title},margin:{l:0,r:0,t:55,b:0},uirevision:'view',scene:{dragmode:'orbit',xaxis:{title:{text:'x'},range:[-xh,xh]},yaxis:{title:{text:'y'},range:[-yh,yh]},zaxis:{title:{text:k==='error'?'绝对误差':f}},aspectmode:'manual',aspectratio:{x:1.2,y:1,z:.7},camera:{eye:{x:1.6,y:-1.6,z:1.1}}}},{responsive:true,scrollZoom:true,displaylogo:false});
 document.getElementById('status').textContent='拖动可旋转，滚轮可缩放。显示使用抽样网格；误差统计仍来自完整数据。';
}
for(const id of ['case','field','kind','xhalf','yhalf'])document.getElementById(id).addEventListener('input',draw);
draw();</script></html>'''
out=ROOT/'report/kp_dlw_comparison.html';out.write_text(html,encoding='utf-8')
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'notebook').glob('*数值分析report.ipynb')}
(HERE/'kp_validation.json').write_text(json.dumps({'layout':'Numerical surface / numerical contour / exact contour; identical contour levels and norm per field','cases':list(data),'T':.01,'actual_data':'case_A/B/C.npz; SD2/RK4/fixed','interactive':'Plotly.js via CDN; 3x display subsampling; full cache unchanged','original_figure':original,'notebook_hashes':hashes},indent=2),encoding='utf-8')
log=ROOT/'PROGRESS_LOG.md';s=log.read_text(encoding='utf-8')
anchor='文献元数据在 Paper/refs/plotting_reference_search_20261008.json；Notebook 未修改。'
note=' **KP 布局试画：** 按 KP Fig3 的曲面／数值等高线／解析等高线三列，生成 A/B/C 各自 u/v 两行图，统一相同场的等高线高度和色标、取消叠加网线。新增 [KP 原图与 DLW 对照](report/kp_dlw_comparison.html)，期刊原图直接在线加载，附独立 Plotly.js 旋转预览（算例、场、数值/解析/误差、x/y 展示范围可选）。直接读取既有 T=.01 数值缓存，不重算 PDE、不改 Notebook；脚本及证据为 kp_layout.py、kp_validation.json。'
if ' **KP 布局试画：**' not in s:
 assert anchor in s
 log.write_text(s.replace(anchor,anchor+note,1),encoding='utf-8')
index=ROOT/'FILE_INDEX.md';s=index.read_text(encoding='utf-8')
if 'report/kp_dlw_comparison.html' not in s:
 index.write_text(s+'\n- `report/kp_dlw_comparison.html`：KP Fig3 原图与 DLW A/B/C 三列布局试画、独立可旋转场预览（在线 Plotly.js）。\n- `Workspaces/dlw_precision_surface_20261008/kp_layout.py`、`kp_validation.json`、`case_A_kp.png`、`case_B_kp.png`、`case_C_kp.png`：KP 布局试画生成器、核验与三个算例图。\n',encoding='utf-8')
print(out)
