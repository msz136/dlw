"""Render the research abstracts using existing local KaTeX; check local references."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / 'report/dlw_research_abstracts_20261013.html'
ASSETS = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'


def main():
    source = (HERE / 'report.source.html').read_text(encoding='utf-8')
    math = []

    def protect(match):
        index = len(math)
        math.append({'tex': html.unescape(match[1] if match[1] is not None else match[2]),
                     'display': match[1] is not None})
        return f'MATHPLACEHOLDER{index:05d}END'

    body = re.sub(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', protect, source, flags=re.S)
    (HERE / 'math.json').write_text(json.dumps(math, ensure_ascii=False), encoding='utf-8')
    node = """const fs=require('fs'),path=require('path');const k=require(path.join(process.argv[2],'katex.js'));const xs=JSON.parse(fs.readFileSync(path.join(process.argv[1],'math.json'),'utf8'));const ys=xs.map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error',output:'htmlAndMathml'}));fs.writeFileSync(path.join(process.argv[1],'math.rendered.json'),JSON.stringify(ys));"""
    subprocess.run(['node', '-e', node, str(HERE), str(ASSETS)], check=True)
    rendered = json.loads((HERE / 'math.rendered.json').read_text(encoding='utf-8'))
    for i, value in enumerate(rendered):
        body = body.replace(f'MATHPLACEHOLDER{i:05d}END', value)
    css = '''*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:#f4f3f0;color:#242423;font:17px/1.95 Georgia,"Times New Roman","SimSun",serif}main{max-width:1040px;margin:30px auto;padding:44px 60px;background:#fff}.eyebrow{font:13px/1.7 system-ui,sans-serif;letter-spacing:.03em;color:#666}h1{font-size:32px;line-height:1.5;margin:18px 0 22px}h2{font-size:23px;line-height:1.6;margin:0 0 18px}h3{font-size:20px;margin:30px 0 14px}.lead{font-size:19px}section{margin:42px 0;padding-top:28px;border-top:1px solid #c4c4bd}p{margin:16px 0;overflow-wrap:anywhere}.abstract{line-height:2}.meaning{padding-left:17px;border-left:3px solid #759097}.evidence,.source,footer{font-size:15px;color:#555}nav{display:flex;flex-wrap:wrap;gap:5px 20px;margin-top:26px;font-size:14px}a{color:#28576a;text-underline-offset:3px}a:focus-visible{outline:2px solid #28576a;outline-offset:4px}.table-wrap{overflow:auto;margin:25px 0}table{border-collapse:collapse;width:100%;font-size:15px}caption{text-align:left;margin-bottom:10px}th,td{text-align:left;padding:9px 12px;border-bottom:1px solid #ddd}thead th{border-top:1px solid #555;border-bottom:1px solid #555}.katex-display{overflow-x:auto;overflow-y:hidden;padding:8px 0;font-size:.93em}footer{border-top:1px solid #bbb;padding-top:16px;margin-top:42px}@media(max-width:700px){body{font-size:16px}main{margin:0;padding:24px 20px}h1{font-size:26px}h2{font-size:21px}h3{font-size:18px}.lead{font-size:17px}section{margin-top:32px}.katex-display{font-size:.84em}table{min-width:510px}}@media print{body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}nav{display:none}h1{font-size:22pt}h2{font-size:16pt;break-after:avoid}h3{font-size:13pt;break-after:avoid}section{margin:24px 0;padding-top:18px}.abstract{line-height:1.8}.katex-display{overflow:visible}.table-wrap{overflow:visible}table{min-width:0}a{color:inherit}}'''
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="DLW 六项研究摘要：谱守恒漂移、误差频谱、Poisson 括号、Liouville 约化、数值辛保持与带源 Lax 表示。"><title>DLW：六项研究摘要与误差机制</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>' + css + '</style></head><body><main>' + body + '</main></body></html>'
    OUT.write_text(page, encoding='utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    ids = [tag['id'] for tag in soup.select('[id]')]
    links = []
    for tag in soup.select('[href], [src]'):
        raw = tag.get('href') or tag.get('src')
        parsed = urlsplit(raw)
        if parsed.scheme:
            continue
        if parsed.path:
            target = (OUT.parent / unquote(parsed.path)).resolve()
            assert target.exists(), target
        elif parsed.fragment:
            assert parsed.fragment in ids, parsed.fragment
        links.append(raw)
    assert len(ids) == len(set(ids))
    assert not soup.select('.katex-error')
    assert len(soup.select('.katex')) == len(math)
    assert len(soup.select('p.abstract')) == 7
    assert 'MATHPLACEHOLDER' not in page
    assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', source)
    assert r'\(' not in body and r'\[' not in body
    result = {'report': str(OUT), 'abstracts': 7, 'math_fragments': len(math),
              'local_links_checked': len(links), 'unique_sections': len(ids),
              'strict_katex': True, 'new_experiments': False}
    (HERE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
