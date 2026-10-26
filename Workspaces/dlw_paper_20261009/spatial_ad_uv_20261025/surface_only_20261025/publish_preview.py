"""Publish the surface-only design preview without changing the manuscript."""
from pathlib import Path
from datetime import datetime
import hashlib, json, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAGE = ROOT / 'report/dlw_overlay_design_choices_20261025.html'
PREFIX = '../Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/surface_only_20261025/figures/'
CASES = ['A', 'D', 'Gaussian', 'Sinusoidal']
NAMES = {'A':'One-soliton (A)', 'D':'Two-soliton (D)', 'Gaussian':'Gaussian', 'Sinusoidal':'Sinusoidal'}
manifest = json.loads((HERE / 'manifest.json').read_text())
peaks = {}
for case in CASES:
    record = next(r for r in manifest if r['case'] == case and r['mode'] == 'plain')
    peaks[case] = [[name] + [next(r['maximum'] for r in record['records'] if r['field'] == q and r['method'] == name) for q in ['u','v']] for name in ['Endpoint-SD','Centered-SD','FD']]

if PAGE.exists() and not (HERE / 'before_overlay_preview.html').exists():
    shutil.copy2(PAGE, HERE / 'before_overlay_preview.html')

html = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DLW 三格式透明误差曲面</title>
<style>
*{box-sizing:border-box}body{max-width:1280px;margin:32px auto;padding:0 24px;background:#fff;color:#262626;font:16px/1.75 "Microsoft YaHei",sans-serif}
h1{font-size:28px;line-height:1.4;margin:0 0 12px}h2{font-size:20px;font-weight:600;margin:22px 0 10px}p{margin:8px 0 16px}.lead{max-width:1060px;color:#444}
.controls,nav{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:16px 0}nav{gap:8px}button,select{font:inherit;padding:7px 13px;border:1px solid #9ca4ab;background:white;color:#282828;border-radius:3px;cursor:pointer}button[aria-pressed=true]{background:#204e70;border-color:#204e70;color:#fff}
button:focus-visible,select:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #d98235;outline-offset:3px}a{color:#225d86}figure{margin:12px 0 24px}img{display:block;width:100%;height:auto}figcaption{color:#555;font-size:14px;text-align:center;margin-top:6px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}[hidden]{display:none!important}.note{color:#555;font-size:14px;border-top:1px solid #ddd;padding-top:14px}.tablewrap{overflow-x:auto}table{border-collapse:collapse;max-width:720px;width:100%;font-size:15px;margin:14px 0 26px}th,td{text-align:right;padding:7px 14px;font-variant-numeric:tabular-nums}th:first-child,td:first-child{text-align:left}thead{border-top:2px solid #333;border-bottom:1px solid #555}tbody{border-bottom:2px solid #333}small{color:#666} @media(max-width:760px){body{padding:0 12px;margin:20px auto}.pair{grid-template-columns:1fr}h1{font-size:24px}}
</style></head><body>
<h1>三格式叠加：透明误差曲面</h1>
<p class="lead">将 Endpoint-SD、Centered-SD 和 FD 的误差画成三张半透明曲面，在同一坐标系中比较形状与高度。左图为 |u − u*|，右图为 |v − v*|；T = 0.01，RK4，h = Δx = 0.1，Δt = 10⁻⁴。</p>
<div class="controls"><label>算例 <select id="case"><option value="A">One-soliton（A）</option><option value="D">Two-soliton（D）</option><option value="Gaussian" selected>Gaussian</option><option value="Sinusoidal">Sinusoidal</option></select></label><label><input id="compare" type="checkbox"> 两版并排</label><a href="dlw_uv_figure_choices_20261025.html">已有图集</a></div>
<nav aria-label="曲面样式"><button data-mode="plain" aria-pressed="true" type="button">无网格曲面</button><button data-mode="mesh" aria-pressed="false" type="button">淡网格曲面</button></nav>
<h2 id="title">无网格曲面</h2><p id="description">用透明填色与柔和光照表现起伏，突出三张曲面的整体轮廓。</p>
<figure id="single"><a id="full" href="__PREFIX__plain_Gaussian.png"><img id="selected" src="__PREFIX__plain_Gaussian.png" alt="高斯算例的三格式透明误差曲面"></a><figcaption>点击图片可查看原尺寸。</figcaption></figure>
<div class="pair" id="paired" hidden><figure><a id="plainlink" href="__PREFIX__plain_Gaussian.png"><img id="plainimg" src="__PREFIX__plain_Gaussian.png" alt="无网格透明曲面"></a><figcaption>无网格曲面</figcaption></figure><figure><a id="meshlink" href="__PREFIX__mesh_Gaussian.png"><img id="meshimg" src="__PREFIX__mesh_Gaussian.png" alt="淡网格透明曲面"></a><figcaption>淡网格曲面</figcaption></figure></div>
<p class="note">每个物理场内，三种格式共用线性高度刻度。曲面以原始节点值作分片线性连接；接近零高度处逐渐变透明。淡网格版只增加稀疏的曲面网格。两版使用相同数据、视角与透明度。</p>
<h2>图示范围内的误差峰值</h2><div class="tablewrap"><table><thead><tr><th>空间格式</th><th>max |u − u*|</th><th>max |v − v*|</th></tr></thead><tbody id="peaks"></tbody></table></div>
<p><small>曲面样式预览 · 2026-10-25</small></p>
<script>
const prefix=__PREFIX_JSON__, peaks=__PEAKS__, names=__NAMES__;
const choices={plain:{title:'无网格曲面',description:'用透明填色与柔和光照表现起伏，突出三张曲面的整体轮廓。'},mesh:{title:'淡网格曲面',description:'在相同曲面上加入稀疏、低对比度的网格，辅助辨认曲面的弯曲方向。'}};
let mode='plain';const $=id=>document.getElementById(id);const path=(m,c)=>prefix+m+'_'+c+'.png';
function show(){const c=$('case').value,choice=choices[mode];$('title').textContent=choice.title;$('description').textContent=choice.description;$('selected').src=path(mode,c);$('selected').alt=names[c]+' · '+choice.title;$('full').href=path(mode,c);for(const m of ['plain','mesh']){$(m+'img').src=path(m,c);$(m+'img').alt=names[c]+' · '+choices[m].title;$(m+'link').href=path(m,c);}$('single').hidden=$('compare').checked;$('paired').hidden=!$('compare').checked;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));$('peaks').replaceChildren(...peaks[c].map(row=>{const tr=document.createElement('tr');row.forEach((v,i)=>{const td=document.createElement('td');td.textContent=i===0?v:v.toExponential(4);tr.appendChild(td)});return tr}));}
document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;show()}));$('case').addEventListener('change',show);$('compare').addEventListener('change',show);show();
</script></body></html>
'''.replace('__PREFIX__', PREFIX).replace('__PREFIX_JSON__', json.dumps(PREFIX)).replace('__PEAKS__', json.dumps(peaks)).replace('__NAMES__', json.dumps(NAMES))
PAGE.write_text(html, encoding='utf-8')

# Side-by-side overview for visual appraisal.
w, h, head = 990, 482, 38
sheet = Image.new('RGB', (2*w, len(CASES)*(h+head)), 'white')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 23)
for i, case in enumerate(CASES):
    for j, mode in enumerate(['plain','mesh']):
        draw.text((j*w+20, i*(h+head)+7), NAMES[case]+' | '+('No mesh' if mode=='plain' else 'Faint mesh'), font=font, fill='#333333')
        im=Image.open(HERE/'figures'/f'{mode}_{case}.png').resize((w,h), Image.Resampling.LANCZOS)
        sheet.paste(im,(j*w,i*(h+head)+head))
sheet.save(HERE/'figures/contact_sheet.png')

checks = {'entries':len(manifest),'images':[]}
assert len(manifest)==8
for r in manifest:
    assert r['renderer']=='per-pixel depth compositing of visible method sheets'
    for file, expected in [(Path(r['source']),r['source_sha256']), (HERE/'figures'/r['png'],r['png_sha256'])]:
        assert hashlib.sha256(file.read_bytes()).hexdigest()==expected
    assert not r['section_lines'] and not r['raw_point_markers']
    checks['images'].append(r['png'])
script=re.search(r'<script>(.*?)</script>',html,re.S).group(1)
js=HERE/'preview_script.cjs';js.write_text(script,encoding='utf-8')
subprocess.run(['node','--check',str(js)],check=True)
paper_hash=hashlib.sha256((ROOT/'dlw-paper.html').read_bytes()).hexdigest()
publication=HERE/'publication.json'
expected_paper_hash=json.loads(publication.read_text())['paper_sha256'] if publication.exists() else 'a7c317a8db6c3232bd176d5abc19148328d0eecddc7c6b01c90321edec13d0e1'
assert paper_hash==expected_paper_hash
checks.update(main_paper_sha256=paper_hash,source_and_image_hashes=True,javascript_syntax=True,main_paper_unchanged=True,page=str(PAGE))
(HERE/'preview_validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('Published',PAGE)
print('Verified all 8 previews, source hashes, JavaScript syntax, unchanged manuscript.')
