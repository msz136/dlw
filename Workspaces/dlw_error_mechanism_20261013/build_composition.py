"""Build the paper-style source analysis at the workspace root."""
from pathlib import Path
import html
import json
import re
import subprocess
import pandas as pd
from bs4 import BeautifulSoup
from build_report import table

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'dlw_error_composition.html'
src = (HERE / 'composition.paper.source.html').read_text(encoding='utf-8')
df = pd.read_csv(HERE / 'sources/leading_u_budget.csv')
rows = []
for case in ('A', 'C'):
    for kind in ('FD', 'SD'):
        r = df[(df.case == case) & (df.method == kind)].iloc[0]
        rows.append([case, 'PE' if kind == 'SD' else kind, f'{r.rms_y_leading:.6g}', f'{r.rms_x_leading:.6g}', f'{r.cosine_leading:+.4f}', f'{r.rms_total_leading:.6g}'])
assert src.count('LEADING_TABLE') == 1
src = src.replace('LEADING_TABLE', table('表1　u 分量的二阶空间截断残差（h = k = 0.1，t = 0）',
                                      ['算例', '方法', 'y 误差 ‖Yₛ‖', 'x 误差 ‖X‖', '方向系数 cₛ', '合成 ‖X + Yₛ‖'], rows))
eq_numbers = [int(x) for x in re.findall(r'\\tag\{(\d+)\}', src)]
assert eq_numbers == list(range(1, 11))
math = []
def replace(m):
    i = len(math)
    math.append({'tex': html.unescape(m[1] if m[1] is not None else m[2]), 'display': m[1] is not None})
    return f'MATHPLACEHOLDER{i}END'
body = re.sub(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', replace, src, flags=re.S)
(HERE / 'composition_math.json').write_text(json.dumps(math, ensure_ascii=False), encoding='utf-8')
node = "const fs=require('fs'),path=require('path');const k=require(path.join(process.argv[2],'katex.js'));const xs=JSON.parse(fs.readFileSync(path.join(process.argv[1],'composition_math.json'),'utf8'));fs.writeFileSync(path.join(process.argv[1],'composition_rendered.json'),JSON.stringify(xs.map(x=>k.renderToString(x.tex,{displayMode:x.display,strict:'error',throwOnError:true,output:'htmlAndMathml'}))));"
subprocess.run(['node', '-e', node, str(HERE), str(ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist')], check=True)
for i, value in enumerate(json.loads((HERE / 'composition_rendered.json').read_text(encoding='utf-8'))):
    body = body.replace(f'MATHPLACEHOLDER{i}END', value)
css = '''<style>*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#f4f3f0;color:#20201e;font:17px/1.9 Georgia,"Times New Roman","SimSun",serif}main{max-width:1080px;margin:28px auto;padding:46px 58px 56px;background:#fff}h1{font-size:30px;line-height:1.5;font-weight:600;text-align:center;margin:0 0 28px}h2{font-size:23px;line-height:1.6;font-weight:600;margin:34px 0 16px}h3{font-size:19px;line-height:1.6;font-weight:600;margin:25px 0 12px}p{margin:14px 0;text-align:justify;overflow-wrap:break-word}.katex{font-size:1.03em}.katex-display{font-size:.94em;overflow-x:auto;overflow-y:hidden;padding:8px 0;margin:17px 0}.table-wrap{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;font-variant-numeric:tabular-nums}caption{text-align:left;margin-bottom:11px}th,td{padding:10px 12px;white-space:nowrap;text-align:right;font-weight:normal}th:nth-child(-n+2),td:nth-child(-n+2){text-align:left}thead th{border-top:1px solid #222;border-bottom:1px solid #777}tbody tr:last-child td{border-bottom:1px solid #222}details{margin-top:32px;border-top:1px solid #bbb;padding-top:18px}summary{cursor:pointer;font-weight:600}summary:focus-visible{outline:2px solid #235b75;outline-offset:4px}a{color:#235b75;text-underline-offset:3px}a:focus-visible{outline:2px solid #235b75;outline-offset:3px}@media(max-width:720px){body{font-size:16px}main{margin:0;padding:26px 20px 38px}h1{font-size:25px}h2{font-size:21px}h3{font-size:18px}.katex-display{font-size:.83em}table{font-size:14px;min-width:610px}th,td{padding:9px}}@media print{@page{size:A4;margin:18mm}body{background:white;font-size:11pt;line-height:1.8}main{max-width:none;margin:0;padding:0}h1{font-size:19pt}h2{font-size:14pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}.katex-display{font-size:.9em;overflow:visible;break-inside:avoid}.table-wrap{overflow:visible;break-inside:avoid}table{font-size:10pt;min-width:0}p{orphans:3;widows:3}}</style>'''
page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>从解析式看误差为什么抵消</title><meta name="description" content="DLW可积半离散与直接差分的领先截断误差：AFD与APE的推导、共同x误差及孤子算例中的抵消。"><link rel="stylesheet" href="Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css">' + css + '</head><body><main>' + body + '</main></body></html>'
soup = BeautifulSoup(page, 'html.parser')
assert len(soup.select('.katex')) == len(math) and not soup.select('.katex-error')
for a in soup.select('[href]'):
    assert (OUT.parent / a['href']).resolve().exists(), a['href']
assert 'MATHPLACEHOLDER' not in page and 'LEADING_TABLE' not in page
assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', src)
assert not any(term in soup.get_text() for term in ('CSV', 'JSON', 'Python', '脚本', '缓存', '复现', '本页', '程序里', '首先', '下一层问题'))
assert '—' not in src and '–' not in src
assert len(soup.select('tbody tr')) == 4
assert len(soup.select('[id]')) == len({x['id'] for x in soup.select('[id]')})
OUT.write_text(page, encoding='utf-8')
result = {'passed': True, 'math_fragments': len(math), 'numbered_equations': len(eq_numbers), 'tables': 1, 'numeric_rows': len(rows), 'links': len(soup.select('[href]')), 'report': str(OUT), 'source': str(HERE / 'composition.paper.source.html'), 'humanizer': 'applied in file mode', 'new_numerical_experiments': False}
(HERE / 'composition_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
