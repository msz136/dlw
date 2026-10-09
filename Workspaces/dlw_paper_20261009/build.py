from pathlib import Path
import base64, html, json, re, subprocess
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
source = (HERE / 'manuscript.md').read_text(encoding='utf-8')
formulas = []
def math_slot(m):
    display = m[0].startswith('$$')
    tex = m[0][2:-2] if display else m[0][1:-1]
    formulas.append(dict(tex=tex, display=display))
    return f'MATHSLOT{len(formulas)-1}END'
text = re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$', math_slot, source)
body = markdown.markdown(text, extensions=['tables'])
(HERE / 'formulas.json').write_text(json.dumps(formulas, ensure_ascii=False), encoding='utf-8')
subprocess.run(['node', str(HERE / 'render.cjs')], check=True)
rendered = json.loads((HERE / 'rendered.json').read_text(encoding='utf-8'))
body = re.sub(r'MATHSLOT(\d+)END', lambda m: rendered[int(m[1])], body)
body = re.sub(r'<p>(<div class="eq">[\s\S]*?</div>)</p>', r'\1', body)
assets = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'
css = (assets / 'katex.css').read_text(encoding='utf-8')
css = re.sub(r'src: (url\([^)]*\.woff2\) format\("woff2"\))[^;]*;', r'src: \1;', css)
def embed(m):
    path = assets / m[1].strip('"\'')
    return 'url(data:font/woff2;base64,' + base64.b64encode(path.read_bytes()).decode() + ')'
css = re.sub(r'url\(([^)]+)\)', embed, css)
css += '''
*{box-sizing:border-box}html{background:#fff;color:#171717}body{margin:0;font-family:"Times New Roman","Noto Serif SC",SimSun,serif;font-size:17px;line-height:1.9}main{max-width:960px;margin:54px auto 80px;padding:0 32px}h1{font-size:29px;text-align:center;font-weight:600;margin:0 0 22px;line-height:1.5}h2{font-size:22px;margin:36px 0 16px;font-weight:600}h3{font-size:18px;margin:25px 0 12px}p{margin:12px 0;text-align:justify}.eq{max-width:100%;overflow-x:auto;margin:20px 0;padding:5px 2px}.katex{font-size:1.04em}.katex-display{margin:0}.katex-display>.katex{text-align:center}table{width:100%;border-collapse:collapse;margin:24px 0;font-size:15px;border-top:1.5px solid #222;border-bottom:1.5px solid #222}th,td{text-align:left;vertical-align:top;padding:10px 12px}thead{border-bottom:1px solid #444}a{color:#273b51;text-underline-offset:3px}footer{border-top:1px solid #bbb;margin-top:36px;padding-top:10px;font-size:14px;color:#444}nav{font-size:14px;text-align:center;margin:24px 0 32px;line-height:2.2}nav a{display:inline-block;margin:0 9px}@media(max-width:600px){body{font-size:16px}main{margin:26px auto 44px;padding:0 18px}h1{font-size:24px}h2{font-size:20px}.katex{font-size:1em}table{font-size:14px}th,td{padding:8px 6px}.eq .katex-display>.katex{text-align:left}}@media print{main{max-width:none;margin:0;padding:0}body{font-size:10.5pt}h1{font-size:18pt}h2{font-size:14pt;break-after:avoid}h3{break-after:avoid}.eq{font-size:8.5pt;overflow:visible;break-inside:avoid}nav{display:none}footer{font-size:9pt}a{color:inherit}}
'''
css += """
.abstract{font-size:16px;margin:24px 0;padding:0 20px}.abstract-label{font-weight:bold;margin-right:1em}figure{margin:32px 0;break-inside:avoid}figure img{display:block;width:100%;height:auto}figcaption{font-size:14px;text-align:center;line-height:1.65;margin:12px 0}table{font-variant-numeric:tabular-nums;font-size:13px;white-space:nowrap}th,td{padding:7px 10px}.table-wrap{overflow-x:auto;max-width:100%}nav{border-top:1px solid #ccc;border-bottom:1px solid #ccc;padding:12px 0}h1{max-width:820px;margin-left:auto;margin-right:auto}h3{font-size:19px}@media print{.table-wrap{overflow:visible}table{font-size:8pt}th,td{padding:4px}figure{max-height:240mm}nav{display:none}}@media(max-width:600px){.abstract{padding:0;font-size:15px}figure{margin-left:-8px;margin-right:-8px}figcaption{padding:0 8px}}
"""
css += "table.comparison th,table.comparison td{text-align:center;vertical-align:middle;background:white}table.comparison tbody th{font-weight:normal}table.comparison thead th{font-weight:600}table.comparison strong{font-weight:800}table.comparison tbody tr:has(th[rowspan=\"6\"]){border-top:1px solid #ddd}"
count = 0
toc = []
def heading(m):
    global count
    count += 1
    toc.append(f'<a href="#s{count}">{html.escape(re.sub("<[^>]*>", "", m[1]))}</a>')
    return f'<h2 id="s{count}">{m[1]}</h2>'
body = re.sub(r'<h2>(.*?)</h2>', heading, body)
page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>（2+1）维 DLW 方程的半离散化、Lax 表示与数值模拟</title><meta name="description" content="DLW 方程的交错半离散化、Gram 行列式解、两种非线性形式、连续极限与孤子数值比较。"><style>' + css + '</style></head><body><main>' + body + '</main></body></html>'
dest = ROOT / 'report/dlw_paper_draft.html'
dest.write_text(page, encoding='utf-8')
tags = [int(n) for f in formulas for n in re.findall(r'\\tag\{(\d+)\}', f['tex'])]
assert tags == list(range(1,76)), tags
assert 'MATHSLOT' not in page
for link in re.findall(r'href="([^"#]+)"', page):
    if not link.startswith(('https://','http://')): assert (dest.parent / link).exists(), link
result = {'html':str(dest), 'formulas':len(formulas), 'numbered_equations':len(tags), 'offline':True, 'spatial_operator':'partial_x', 'local_links_checked':True}
(HERE / 'build_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
