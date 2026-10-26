"""Publish the user-requested dx=h=.1 comparison; retain coarse diagnostics."""
from run import *
from scipy.interpolate import CubicSpline
import html,csv

def pair(v):return ' / '.join(f'{x:.3e}' for x in v) if v is not None else '—'
def table(head,rows):return '<table><thead><tr>'+''.join('<th>'+h+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table>'
records=[]
for case in (*CASES,'Gaussian','Sinusoidal'):
    for method in ('Endpoint-SD','Centered-SD','FD'):
        stem=HERE/f'{case}_{method}_main'
        if not stem.with_suffix('.json').exists():continue
        r=json.loads(stem.with_suffix('.json').read_text())
        half=HERE/f'{case}_{method}_main_halfdt'
        if half.with_suffix('.json').exists():r['halfdt']=json.loads(half.with_suffix('.json').read_text())
        if not r['failed_at']:
            b=np.load(stem.with_suffix('.npz'))
            if case in CASES:
                m=Model(case,method,.1,.1);err=[]
                for j,key in enumerate(('y','yv')):
                    ym=abs(b[key])<HALF_WIDTHS[case];xm=abs(b['x'])<=HALF_WIDTHS[case]
                    ref=m.profile(b[key][ym],r['T'])[j]
                    err.append(float(abs(b['z'][j,ym][:,xm]-ref[:,xm]).max()))
                r['nodal_errors']=err
            if 'halfdt' in r and not r['halfdt']['failed_at']:
                f=np.load(half.with_suffix('.npz'));diff=[]
                for j,key in enumerate(('y','yv')):
                    ym=abs(b[key])<HALF_WIDTHS[case] if case in CASES else (abs(b[key])<=1.8)
                    xm=abs(b['x'])<=HALF_WIDTHS[case] if case in CASES else np.ones(len(b['x']),bool)
                    diff.append(float(abs(b['z'][j,ym][:,xm]-f['z'][j,ym][:,xm]).max()))
                r['halfdt_difference']=diff
        records.append(r)
(HERE/'main_results.json').write_text(json.dumps(records,indent=2),encoding='utf8')
body='''<h1>六算例空间离散比较：Δx=h=0.1</h1><p>2026-10-23 · 新物理场 u,v 实现 · Fourier x 微分 · RK4 · 固定网格</p>
<h2>本轮结论</h2><p>本轮按统一 Δx=h=.1 重跑。变量改写本身通过独立对照：同一 Fourier 网格和边界下，Centered-SD 与旧 P,W 推进所得场差小于 5.5×10⁻¹³，FD 小于 1.1×10⁻¹³（A算例受控测试）。此前的四孤子旧表使用 x 中心差分，不能直接替代这份 Fourier 表。</p>
<p>四组孤子中没有一种方法对所有算例、两个场都占优。A、D 中 FD 的 u 误差较小，Centered-SD 的 v 误差较小；Endpoint-SD 的 v 误差明显较大。B 在 Δx=.1 下三种方法均出现很大的误差，时间步减半未消除这一现象。C 的 u 误差也随 x 加密明显上升。这些行保留为敏感性诊断，不据其细小差别宣称方法优势。</p>
<p>Gaussian 和正弦初值在 Δx=.1 下均触发大幅增长，未完成到 T=.1；减半时间步仍触发。这些算例应呈现增长与失效时刻，不能编成“终止误差”。附件 PDF 的成功短时结果使用 Δx=.5；本轮另外保留了该分辨率的对照。</p>
<h2>已有实验定位</h2><p>2026-10-22 四孤子 Endpoint-SD/PE/FD 结果：<a href="dlw_paper_method_comparison_20261022.html">既有比较报告</a>。其 x 算子为中心差分。附件 PDF 第12–13页给出 Endpoint-SD 的 Fourier 孤子与两类非精确数据结果，但其参数和网格不同，归档目录仅有 PDF 及索引。</p>
<h2>四组孤子：连续精确解最大误差</h2><p>A=(1,2)，B=(4,−3)，C=(6,−5;4,−3)，D=(1,2;4,−3)。a=2，Δx=h=.1，T=.01，Δt=.0001。计算半宽分别10/20/40/40，评价半宽5/10/30/30。表中数值顺序均为 u / v。</p>
<p>评价误差在 x 上用三次样条取 .02 间距；节点误差不含此后处理。Endpoint-SD 的 v 在 y 边中点取样，其余两法的 u,v 共点，均与各自实际位置上的同一连续解比较。</p>'''
body+=table(['算例','方法','评价最大误差 u / v','节点最大误差 u / v','时间步减半场差 u / v'],[[r['case'],r['method'],pair(r.get('errors')),pair(r.get('nodal_errors')),pair(r.get('halfdt_difference'))] for r in records if r['case'] in CASES])
body+='''<h2>Gaussian 与正弦：统一网格后的演化状态</h2><p>a=1/3，x∈[−96,96)，Nx=1920，y∈[−2,2]，h=.1，目标 T=.1。基准 Δt=.001，复核 .0005。失效判据为任一场非有限或 max(|u|,|v|)&gt;10⁶；以下时刻是程序首次触发判据的步末时刻，不是解析爆破时刻。</p>'''
body+=table(['初值','方法','基准首次触发时刻','时间步减半首次触发时刻'],[[r['case'],r['method'],r['failed_at'],r.get('halfdt',{}).get('failed_at','待完成')] for r in records if r['case'] not in CASES])
body+='''<h2>初边值与实现核验</h2><p>三法均推进 u,v，并用第一空间方程沿 y 求和恢复 u_t。Endpoint-SD 使用左侧背景、向后差分，无右边界。Centered-SD/FD 的上侧 u 虚点采用“给定背景＋内侧扰动二次外推”，其时间导数同步用于 Centered-SD 的 v_t；并非把两端 u,v 都固定。孤子背景是连续精确解，非精确背景是初始剖面。</p>
<p>Gaussian 与正弦的共同物理包络为 e(y)=sin[π(y+2)/4]；Endpoint-SD 的 v 在边中点取样。Gaussian 振幅 .05/.03，宽度6；正弦振幅 .03/.02，波长24。此位置对齐设置不是附件按同一 k 指定两场振幅的逐项复现。</p>
<p>Fourier 一阶 Nyquist 系数为0，二阶保留 −ξ²；不滤波、不添加黏性。已验证 Fourier 导数、虚点链式求导，以及与旧辅助变量实现的变换一致性。Endpoint-SD 的线性高频分支有附件推导支持；另两法此处报告数值观察，不套用其谱证明。</p>
<h2>如何用于正文</h2><p>5.2 可先呈现四孤子主表，并说明场间取舍；B 必须附上空间敏感性，不能仅挑 Δx=.2 的较小误差。5.5 呈现两类非精确初值的增长与分辨率依赖。当前不宜宣称“网格越细越准确”，也不能把非精确场的变化量当作误差。</p>
<p>较粗网格、y加密和后处理诊断见 <a href="dlw_spatial_diagnostics_20261023.html">补充诊断表</a>。完整新数据见 <a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/main_results.json">main_results.json</a>；<a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/variable_validation.json">变量转换核验</a>。</p>'''
out=HERE.parents[2]/'report/dlw_spatial_audit_20261023.html'
out.write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>DLW 六算例 Δx=h=.1</title><style>body{font:16px/1.75 Georgia,"Microsoft YaHei",serif;max-width:1200px;margin:40px auto;padding:0 28px;color:#26323e}h1,h2{color:#17364d}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0}th,td{padding:10px;border-bottom:1px solid #cbd5df;text-align:left}th{background:#edf2f6}</style>'+body+'</html>',encoding='utf8')
for r in records:print(r['case'],r['method'],pair(r.get('errors')),r['failed_at'],'half',r.get('halfdt',{}).get('failed_at','pending'),pair(r.get('halfdt_difference')))
print('main records',len(records),'halfdt',sum('halfdt'in r for r in records))
