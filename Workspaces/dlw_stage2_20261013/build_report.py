"""Build the stage-2 mathematical report with strict offline KaTeX."""
from pathlib import Path
import csv
import html
import json
import os
import re
import subprocess
from urllib.parse import urlsplit, unquote
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'report/dlw_stage2_20261013.html'
MATH = []


def link(path):
    return os.path.relpath(path, OUT.parent).replace('\\', '/')


def render(text, source=None, appendix=False):
    def protect(match):
        groups = match.groups()
        tex = next(v for v in groups if v is not None)
        index = len(MATH)
        MATH.append({'tex': tex, 'display': groups[0] is not None or groups[1] is not None})
        return f'MATHPLACEHOLDER{index:05d}END'
    text = re.sub(r'\$\$(.*?)\$\$|\\\[(.*?)\\\]|\\\((.*?)\\\)|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$',
                  protect, text, flags=re.S)
    result = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    if appendix:
        result = re.sub(r'<(/?)h([1-6])>', lambda m: f'<{m[1]}h{min(int(m[2])+2,6)}>', result)
    if source:
        def rewrite(match):
            attr, raw = match[1], html.unescape(match[2])
            parsed = urlsplit(raw)
            if parsed.scheme or not parsed.path:
                return match[0]
            target = (source.parent / unquote(parsed.path)).resolve()
            return f'{attr}="{html.escape(link(target) + ("#" + parsed.fragment if parsed.fragment else ""), quote=True)}"'
        result = re.sub(r'(href|src)="([^"]+)"', rewrite, result)
    return result.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')


def figure(path, caption):
    assert path.is_file(), path
    return f'<figure><a href="{link(path)}"><img loading="lazy" src="{link(path)}" alt="{html.escape(caption)}"></a><figcaption>{html.escape(caption)}</figcaption></figure>'


def detail(path, title):
    return '<details><summary>'+title+'</summary>'+render(path.read_text(encoding='utf-8'), path, True)+'</details>'


def main():
    source = HERE / 'manuscript.md'
    body = render(source.read_text(encoding='utf-8'), source)
    # Insert exact tables and figures from the completed experiments.
    with (HERE/'symplectic/fixed_time.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = [r for r in csv.DictReader(stream) if int(r['steps']) == 8]
    table = '| 时间推进 | 辛缺陷 | 物理场末态最大误差 |\n|---|---:|---:|\n'
    for r in rows:
        table += f'| {r["method"]} | {float(r["symplectic_defect"]):.5e} | {float(r["physical_field_error_vs_DOP853_linf"]):.5e} |\n'
    body = body.replace('<p>SYMPLECTIC_TABLE</p>', render(table))
    body = body.replace('<p>SYMPLECTIC_FIGURE</p>', figure(HERE/'symplectic/symplectic_defect.png',
        '图1　真实 DLW Hamilton 网格流的单步及固定时间辛缺陷。低于统一拟合阈值的数据不用于估阶。'))
    body = body.replace('<p>TOLERANCE_FIGURE</p>', figure(HERE/'symplectic/midpoint_solver_tolerance.png',
        '图2　中点法的实际 Newton 迭代映射与理想隐式微分公式。未解准时，后者会掩盖实际辛缺陷。'))
    for token, path, title in [
        ('REDUCTION_PROOF', HERE/'reduction/report.md', '2A 完整定理、证明与验证'),
        ('SYMPLECTIC_PROOF', HERE/'symplectic/report.md', '2B 辛形式、变分算法与完整数值结果'),
        ('ERROR_LAX_PROOF', HERE/'error_lax/REPORT.md', '2C 完整残差恒等式、误差 Lax 表示与谱误差界'),
        ('SYNTHESIS_PROOF', HERE/'synthesis.md', '相位对齐误差界、辛剪切与强迫误差界的证明')]:
        body = body.replace('<p>'+token+'</p>', detail(path, title))
    (HERE/'report_math.json').write_text(json.dumps(MATH,ensure_ascii=False),encoding='utf-8')
    node = """const fs=require('fs'),path=require('path');const k=require(path.resolve(process.argv[1],'../gsg_project/dlw_report/_assets/package/dist/katex.js'));const src=JSON.parse(fs.readFileSync(path.join(process.argv[1],'report_math.json'),'utf8'));const out=src.map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error',output:'htmlAndMathml'}));fs.writeFileSync(path.join(process.argv[1],'report_math_rendered.json'),JSON.stringify(out));"""
    subprocess.run(['node','-e',node,str(HERE)],check=True)
    rendered=json.loads((HERE/'report_math_rendered.json').read_text(encoding='utf-8'))
    for i, value in enumerate(rendered):
        body=body.replace(f'MATHPLACEHOLDER{i:05d}END',value)
    css='''*{box-sizing:border-box}body{margin:0;background:#f3f2ef;color:#202020;font:17px/1.9 Georgia,"Times New Roman","SimSun",serif}main{max-width:1140px;margin:28px auto;padding:42px 52px;background:#fff}h1{font-size:28px;line-height:1.5;text-align:center;margin:0 0 24px}h2{font-size:23px;margin-top:40px}h3{font-size:20px}h4{font-size:18px}a{color:#28556d;text-underline-offset:3px}p,li{overflow-wrap:anywhere}img{max-width:100%;height:auto;display:block;margin:auto}figure{margin:26px 0}figcaption{font-size:14px;color:#555;text-align:center;margin-top:8px}details{border-top:1px solid #bbb;margin:24px 0;padding:14px 0}summary{cursor:pointer;font-weight:600;color:#28556d}a:focus-visible,summary:focus-visible{outline:2px solid #28556d;outline-offset:4px}.table-wrap{overflow-x:auto;margin:22px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #ddd}th{border-block:1px solid #777}.katex-display{overflow-x:auto;overflow-y:hidden;padding:7px 0;font-size:.91em}pre{overflow:auto;font-size:13px;background:#f7f7f5;padding:14px}code{font-size:.86em}li{margin:8px 0}@media(max-width:700px){body{font-size:16px}main{margin:0;padding:24px 18px}h1{font-size:24px}h2{font-size:21px}table{min-width:580px}.katex-display{font-size:.82em}}@media print{body{background:white;font-size:10.5pt}main{padding:0;margin:0;max-width:none}h1{font-size:20pt}h2{font-size:15pt}figure{break-inside:avoid}.table-wrap{overflow:visible}table{min-width:0;font-size:9pt}a,summary{color:inherit}}'''
    out='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="DLW原结构行波Liouville约化、时间离散辛缺陷及误差Lax残差理论。"><title>DLW：合法约化、辛保持与误差Lax缺陷</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+css+'</style></head><body><main>'+body+'</main></body></html>'
    OUT.write_text(out,encoding='utf-8')
    print(json.dumps({'report':str(OUT),'math_count':len(MATH),'bytes':OUT.stat().st_size},ensure_ascii=False))


if __name__=='__main__':
    main()
