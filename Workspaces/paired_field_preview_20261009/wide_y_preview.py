"""Repeat the selected candidate styles on an actual wide-y moving-mesh DLW run."""
from pathlib import Path
import ast, json, hashlib, time, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=ROOT/'Workspaces/paired_field_preview_20261008'
paths=[ROOT/f'notebook/{name}数值分析report.ipynb' for name in ('DLW','2HS')]
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
book=json.loads(paths[0].read_text(encoding='utf-8'))
cells={c['id']:''.join(c['source']) for c in book['cells']}
ns={}
for key in ('dlw-imports','dlw-config','dlw-reference','dlw-spatial','dlw-sd_fd','dlw-sd',
            'dlw-sd2_lift','dlw-sd2_evolution','dlw-fd','dlw-mesh','dlw-time'):
    exec(cells[key],ns)
config=dict(ns['CONFIG'],L=80.,nx=512,yhalf=30.,eval_half=30.,eval_points=1201)
started=time.perf_counter()
cache=HERE/'wide_moving_data.npz'
if cache.exists():
    saved=np.load(cache)
    meta=json.loads((HERE/'numerical_run.json').read_text())
    assert meta['config']==config
    data=dict(x=saved['x'],second=saved['y'],axis='$y$',
              fields=[saved['u'],saved['v']],errors=[saved['eu'],saved['ev']])
else:
    print('Computing DLW C: SD2/RK4/moving, x calculation [-40,40), y [-30,30)',flush=True)
    result=ns['solve']('C','SD2','RK4','moving',config)
    assert result['completed'],result['reason']
    assert all(np.isfinite(f).all() for f in result['fields'])
    assert np.all(np.diff(result['native_x'])>0)
    data=dict(x=result['x'],second=result['y'],axis='$y$',
              fields=result['fields'],errors=[result['errors'][f] for f in ('u','v')])
    np.savez_compressed(cache,x=data['x'],y=data['second'],u=data['fields'][0],v=data['fields'][1],
        eu=data['errors'][0],ev=data['errors'][1],exact_u=result['exact'][0],exact_v=result['exact'][1])
    meta=dict(config=config,model='SD2',method='RK4',mesh='moving',case='C',
        completed=bool(result['completed']),reached=float(result['reached']),
        min_J=result['min_J'],max_errors=result['max_errors'],seconds=time.perf_counter()-started)
    (HERE/'numerical_run.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
data.update(keys=('u','v'),title='DLW Case C | SD2, RK4, moving mesh | t=0.01 | x,y in [-30,30]')
# Reuse the exact plotting function from the attached candidate's generator.
tree=ast.parse((OLD/'preview.py').read_text(encoding='utf-8'))
render_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[render_node],type_ignores=[]),'original_render','exec'),globals())
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],
    'mathtext.fontset':'stix','font.size':11,'figure.dpi':110})
for style in ('box','floor','map'):
    render(data,style,'dlw')
    print('Rendered',style,flush=True)

saved=np.load(OLD/'data.npz')
hs=dict(x=saved['hs_x'],second=saved['hs_t'],axis='$t$',
    fields=[saved['hs_u'],saved['hs_rho']],errors=[saved['hs_eu'],saved['hs_erho']],
    keys=('u',r'\rho'),title='2HS two solitons | Integrable, RK4 | original time history 0 to 0.5')
for style in ('box','floor','map'):render(hs,style,'hs')

def sheet(names,out):
    width=1000;header=55;pad=20
    tiles=[]
    for name,label in names:
        im=Image.open(HERE/name).convert('RGB')
        im.thumbnail((width,850),Image.Resampling.LANCZOS)
        tiles.append((im,label))
    height=max(im.height for im,_ in tiles)
    canvas=Image.new('RGB',(3*width+4*pad,((len(tiles)+2)//3)*(height+header+pad)+pad),'white')
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/times.ttf',30)
    for i,(im,label) in enumerate(tiles):
        x=pad+(i%3)*(width+pad);y=pad+(i//3)*(height+header+pad)
        draw.text((x+10,y),label,font=font,fill='#111111')
        canvas.paste(im,(x+(width-im.width)//2,y+header))
    canvas.save(HERE/out)
names=[(f'dlw_{s}.png',f'DLW | {label}') for s,label in
       (('box','A: boxed surfaces'),('floor','B: floor projections'),('map','C: heatmaps'))]
sheet(names,'dlw_candidates_wide_y.png')
sheet(names+[(f'hs_{s}.png',f'2HS | {label}') for s,label in
       (('box','A: boxed surfaces'),('floor','B: floor projections'),('map','C: heatmaps'))],
       'candidates_wide_y.png')

html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 宽 y 范围绘图候选</title><style>body{max-width:1200px;margin:36px auto;padding:0 24px;font:18px/1.75 "Times New Roman",SimSun,serif;color:#222;background:#fff}h1{font-size:28px}h2{font-size:23px;margin-top:40px}img{max-width:100%;height:auto}figure{margin:18px 0}figcaption{font-size:15px;color:#555}a{color:#265c7c}</style><h1>DLW Case C：扩大 y 范围后的三种画法</h1><p>固定 t=0.01，以实际 SD2＋RK4 动网格数值解展示 u、v 及绝对误差。展示范围 x,y∈[-30,30]，计算域 x∈[-40,40)、y∈[-30,30)，保持 Δx=0.15625、h=0.125、Δt=0.000125。三种画法使用同一份场数据和误差。</p><p>扩大 y 后，两条分支更容易分辨。为避免 x 截掉斜向分支，x 展示范围同时扩大。2HS 的第二坐标是时间 t，保留原来的 0 至 0.5 时间历史。</p>'''
for style,label in (('box','A　盒式曲面'),('floor','B　曲面与底面投影'),('map','C　二维热图')):
    link=f'../Workspaces/paired_field_preview_20261009/dlw_{style}'
    html+=f'<h2>{label}</h2><figure><a href="{link}.png"><img src="{link}.png" alt="{label}：物理场与绝对误差"></a><figcaption>左列数值物理场，右列绝对误差；上行 u，下行 v。<a href="{link}.pdf">PDF</a> · <a href="{link}.png">完整图片</a></figcaption></figure>'
html+='<p><a href="../Workspaces/paired_field_preview_20261009/candidates_wide_y.png">查看 DLW 与 2HS 六图总览</a></p></html>'
report=ROOT/'report/dlw_wide_y_candidates_20261009.html'
report.write_text(html,encoding='utf-8')
for p in paths:assert hashes[p.name]==hashlib.sha256(p.read_bytes()).hexdigest()
validation=dict(notebooks_unchanged=True,hashes=hashes,reference=str(OLD/'candidates.png'),
    numerical_run=meta,styles=['box','floor','map'],hs_original_data_reused=True,
    display_xlim=[-30,30],display_ylim=[-30,30],old_display_ylim=[-1.5,1.5])
(HERE/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(report,flush=True)
