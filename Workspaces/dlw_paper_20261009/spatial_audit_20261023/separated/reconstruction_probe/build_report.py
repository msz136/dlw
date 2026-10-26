from pathlib import Path
import json,math,re,subprocess
import markdown
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
old=json.loads((HERE.parent/'spatial.json').read_text())
rows=[json.loads((HERE/f'{c}_{h:g}{suffix}.json').read_text()) for suffix in ['', '_left'] for c in 'ABCD' for h in [.1,.05,.025]]
for r in rows:
    if r['primitive'].startswith('periodic zero-mean'):r['primitive']='mean gauge; Fourier Nyquist zero'
assert len(rows)==24 and all(r['status']=='complete' for r in rows)
summary=dict(runs=len(rows),max_map_residual=max(r['map_residual'] for r in rows),max_first_equation_identity=max(r['first_equation_identity'] for r in rows),max_pushforward_check=max(r['pushforward_check'] for r in rows))
summary['endpoint_u_difference_max']=max(abs(r['defects'][0]-next(x['total'][0] for x in old if x['case']==r['case'] and x['h']==r['h'] and x['dx']==.1 and x['method']=='Endpoint-SD')) for r in rows)
summary['v_orders_mean_gauge']={c:[math.log2(next(r['defects'][1] for r in rows if r['case']==c and r['h']==h1 and r['primitive'].startswith('mean'))/next(r['defects'][1] for r in rows if r['case']==c and r['h']==h2 and r['primitive'].startswith('mean'))) for h1,h2 in [(.1,.05),(.05,.025)]] for c in 'ABCD'}
(HERE/'summary.json').write_text(json.dumps(summary,indent=2))
source=(HERE/'derivation.md').read_text(encoding='utf8')
source+='\n\n## 对照数据：h=dx=0.1，t=0\n\n采用统一零均值积分约定。每个量均为对应物理位置的完整初始导数缺陷最大值。\n\n'
source+='| 算例 | 原Centered的u | 新重构的U | 原Centered的v | 新重构的V |\n|---|---:|---:|---:|---:|\n'
for c in 'ABCD':
    o=next(x for x in old if x['case']==c and x['method']=='Centered-SD' and x['h']==.1 and x['dx']==.1)
    n=next(r for r in rows if r['case']==c and r['h']==.1 and r['primitive'].startswith('mean'))
    source+='| '+c+' | '+' | '.join(f'{v:.6e}' for v in [o['total'][0],n['defects'][0],o['total'][1],n['defects'][1]])+' |\n'
source+='\n新U与Endpoint-SD初始缺陷最大值之差：'+f"{summary['endpoint_u_difference_max']:.3e}"+'。新V的观测阶（两次减半）如下。\n\n| 算例 | 0.1→0.05 | 0.05→0.025 |\n|---|---:|---:|\n'
for c,pp in summary['v_orders_mean_gauge'].items():source+=f'| {c} | {pp[0]:.4f} | {pp[1]:.4f} |\n'
(HERE/'report.md').write_text(source,encoding='utf8')
natural=HERE/'natural_reconstruction.md'
if natural.exists():
    source+='\n\n'+natural.read_text(encoding='utf8')+'\n\n## 局部方案的U初始残差，h=dx=0.1\n\n| 算例 | 原Centered | 直接Delta Z | 通量平均 | Endpoint参考 |\n|---|---:|---:|---:|---:|\n'
    checks=[]
    for c in 'ABCD':
        ori=next(x for x in old if x['case']==c and x['method']=='Centered-SD' and x['h']==.1 and x['dx']==.1)
        end=next(x for x in old if x['case']==c and x['method']=='Endpoint-SD' and x['h']==.1 and x['dx']==.1)
        loc=json.loads((HERE/f'{c}_0.1_local.json').read_text());flux=json.loads((HERE/f'{c}_0.1_fluxmean.json').read_text())
        source+='| '+c+' | '+' | '.join(f'{v:.6e}' for v in [ori['total'][0],loc['defects'][0],flux['defects'][0],end['total'][0]])+' |\n'
        for h in [.1,.05,.025]:
            for tag in ['local','fluxmean']:checks.append(json.loads((HERE/f'{c}_{h:g}_{tag}.json').read_text()))
    assert len(checks)==24 and all(r['status']=='complete' for r in checks)
    (HERE/'natural_validation.json').write_text(json.dumps(dict(runs=24,max_map_residual=max(r['map_residual'] for r in checks),max_pushforward_check=max(r['pushforward_check'] for r in checks)),indent=2))
    (HERE/'report.md').write_text(source,encoding='utf8')
new_note=HERE/'bilinear_potential_derivation.md'
if new_note.exists():
    source=new_note.read_text(encoding='utf8')+'\n\n---\n\n# 前两轮构造与对照记录\n\n'+source
    (HERE/'report.md').write_text(source,encoding='utf8')
formula=[]
def protect(m):
    s=m[0];formula.append(dict(tex=s[2:-2],display=s.startswith('\\[')));return f'MATHPLACEHOLDER{len(formula)-1}END'
protected=re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,source)
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));"
res=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formula),text=True,encoding='utf8',capture_output=True,check=True)
html=markdown.markdown(protected,extensions=['tables'])
for i,v in enumerate(json.loads(res.stdout)):
    token=f'MATHPLACEHOLDER{i}END';html=html.replace('<p>'+token+'</p>','<div class="equation">'+v+'</div>');html=html.replace(token,v)
css='body{max-width:1050px;margin:40px auto;padding:0 24px;font:17px/1.8 Georgia,"Microsoft YaHei",serif;color:#222}h1{font-size:26px}h2{font-size:21px;margin-top:32px}table{border-collapse:collapse;width:100%;font-size:15px}th,td{padding:9px;text-align:center}thead{border-top:2px solid;border-bottom:1px solid}tbody{border-bottom:2px solid}.equation{overflow-x:auto}.katex{font-size:1em}'
report=ROOT/'report/dlw_centered_reconstruction_probe_20261023.html'
report.write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Centered-SD 物理场重构探索</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+css+'</style><body>'+html+'</body></html>',encoding='utf8')
print(json.dumps(summary,indent=2));print(report)
