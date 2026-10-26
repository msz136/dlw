from pathlib import Path
import json, hashlib
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PROJECT=HERE.parent
CASES=['D','Gaussian'];PREFIX='../Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/'
CHOICES=[
 ('original','A · 现有叠加图','现有版本','三套双向网格与半透明曲面，共同线性高度。'),
 ('light','B · 淡曲面与单向截线','贴近现有风格','保留淡曲面，用七组单方向截线代替交叉网格。曲线使用全部原生 x 采样点。'),
 ('profiles','C · 纯截线叠加','最简洁的三维版','去掉曲面填色，三种格式用颜色和线型区分。共同线性高度保留误差的绝对量级比例。'),
 ('log','D · 对数截线','侧重数量级','稀疏截线采用共同对数高度，让小误差结构也占据可读的空间。低于该分量最大误差的 10⁻⁴ 的线段省略；竖轴刻度为实际误差值。'),
 ('summary','E · 三维图与最大误差曲线','推荐：用于论文定量比较','上部展示七组原生截线；下部在每个 x 位置取所有原生 y 节点上的最大误差，再以对数刻度比较三种格式。它概括整个 y 区间，不依赖单个截面。'),
 ('zoom','F · 全高度与低高度放大','备选：全部采用三维视图','上排保留共同线性高度；下排放大较小误差所在的高度区间。两排分别标明量级，三种格式在各面板内共用同一尺度。下排仅绘坐标上界以内的线段，完整峰值见上排。'),
]
items=[]
for mode,title,tag,description in CHOICES:
    paths={c:PREFIX+('figures/errors_3d_overlay_'+c+'.png' if mode=='original' else 'overlay_design_20261025/figures/'+mode+'_'+c+'.png') for c in CASES}
    items.append(dict(mode=mode,title=title,tag=tag,description=description,paths=paths))

style='''body{margin:32px auto;max-width:1220px;padding:0 24px;color:#242424;background:#fff;font:17px/1.75 "Microsoft YaHei",sans-serif}h1{font-size:28px;line-height:1.35;margin-bottom:10px}h2{font-size:21px;font-weight:600;margin:18px 0 8px}p{margin:8px 0 15px}.intro{max-width:1040px;color:#444}nav{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}button,select{font:inherit;padding:8px 12px;background:#fff;color:#333;border:1px solid #aaa;border-radius:3px;cursor:pointer}button[aria-pressed=true]{background:#163f62;color:white;border-color:#163f62}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #d77824;outline-offset:3px}.controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:18px 0}.tag{font-size:14px;color:#315c75}.description{max-width:1080px;min-height:52px}figure{margin:12px 0 22px}img{max-width:100%;height:auto;display:block;margin:auto}a{color:#1c628c}.compare{display:grid;grid-template-columns:1fr 1fr;gap:16px}.compare[hidden]{display:none}.compare figcaption{font-size:14px;text-align:center}.method{font-size:14px;color:#555;border-top:1px solid #ddd;padding-top:12px}table{border-collapse:collapse;width:100%;max-width:760px;margin:14px 0 26px;font-size:15px}th,td{padding:6px 12px;text-align:right}th:first-child,td:first-child{text-align:left}thead{border-top:2px solid #333;border-bottom:1px solid #555}tbody{border-bottom:2px solid #333}small{font-size:14px;color:#555}@media(max-width:750px){body{padding:0 12px}.compare{grid-template-columns:1fr}.controls{gap:10px}}'''
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 三格式叠加误差图：展示方案</title><style>'''+style+'''</style></head><body>
<h1>三格式叠加误差图：让形状与量级都能看清</h1>
<p class="intro">采用二孤子 D 和高斯算例的同一份 T = 0.01 误差数据，比较五种改法与原图。二孤子的 v 峰值相差约 70 倍，高斯约 87 倍；共同线性高度下，较小曲面只占总高度的约 1%。</p>
<div class="controls"><label>算例 <select id="case"><option value="D">Two-soliton（D）</option><option value="Gaussian">Gaussian</option></select></label><label><input type="checkbox" id="compare"> 与原图并排对照</label><a href="dlw_uv_figure_choices_20261025.html">返回已有图集</a></div>
<nav aria-label="展示方式">'''+''.join('<button type="button" data-mode="'+r['mode']+'" aria-pressed="false">'+r['title']+'</button>' for r in items)+'''</nav>
<h2 id="title"></h2><div id="tag" class="tag"></div><p id="description" class="description"></p>
<figure id="single"><a id="full" href="#"><img id="selected" alt=""></a></figure>
<div id="paired" class="compare" hidden><figure><img id="before" alt="原图"><figcaption>原图</figcaption></figure><figure><img id="after" alt="候选图"><figcaption id="afterlabel"></figcaption></figure></div>
<p class="method">各候选均保留原始误差值，曲线连接全部 x 采样点。七组截线取自最接近目标 y 值的原生网格位置。B 的淡曲面省略低于分量最大误差 10⁻⁴ 的部分；D 使用同一阈值显示对数截线。E 的下图使用全部原生 y 节点计算最大值。点击大图可查看原尺寸。</p>
<h2>当前算例的误差峰值</h2><table><thead><tr><th>空间格式</th><th>max |u − u*|</th><th>max |v − v*|</th></tr></thead><tbody id="peaks"></tbody></table>
<p><small>原论文的图和数值表保持原版；本页用于比较展示方式。</small></p>
<script>'''
audit=json.loads((HERE/'audit_numbers.json').read_text()) if (HERE/'audit_numbers.json').exists() else {}
# Read native errors independently, rather than depending on the audit's schema.
import numpy as np
peaks={}
for c in CASES:
    d=np.load(PROJECT.parent/'report_refresh_20261024/natural_selection_20261025/figures/data'/(c+'.npz'))
    win=(-30,30) if c=='D' else (-18,18);mask=(d['x']>=win[0])&(d['x']<=win[1])
    peaks[c]=[[name]+[float(np.abs(d[p+'_error_final_'+q][:,mask]).max()) for q in ['u','v']] for p,name in [('endpoint','Endpoint-SD'),('centered','Centered-SD'),('fd','FD')]]
html+='const choices='+json.dumps(items,ensure_ascii=False)+';const peaks='+json.dumps(peaks)+';'
html+='''let mode='summary';const $=x=>document.getElementById(x);function show(){const c=$('case').value,r=choices.find(x=>x.mode===mode),original=choices[0].paths[c];$('title').textContent=r.title;$('tag').textContent=r.tag;$('description').textContent=r.description;$('selected').src=r.paths[c];$('selected').alt=c+' '+r.title;$('full').href=r.paths[c];$('before').src=original;$('after').src=r.paths[c];$('afterlabel').textContent=r.title;const paired=$('compare').checked;$('single').hidden=paired;$('paired').hidden=!paired;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));$('peaks').innerHTML=peaks[c].map(r=>'<tr><td>'+r[0]+'</td><td>'+r[1].toExponential(4)+'</td><td>'+r[2].toExponential(4)+'</td></tr>').join('');}document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;show()});$('case').onchange=show;$('compare').onchange=show;show();</script></body></html>'''
target=ROOT/'report/dlw_overlay_design_choices_20261025.html';target.write_text(html,encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
for case in CASES:
    canvas=Image.new('RGB',(1800,3*560),'white');dr=ImageDraw.Draw(canvas)
    for i,r in enumerate(items):
        f=(target.parent/r['paths'][case]).resolve();im=Image.open(f);im.thumbnail((880,500))
        x=(i%2)*900;y=(i//2)*560;canvas.paste(im,(x+(900-im.width)//2,y+50+(500-im.height)//2))
        lab=['A Original','B Light surfaces','C Sparse profiles','D Logarithmic height','E 3D + transverse maxima','F Full height + height zoom'][i]
        dr.text((x+14,y+10),lab,fill='#222222',font=font)
    canvas.save(HERE/'figures'/('contact_'+case+'.png'))
print(target)
