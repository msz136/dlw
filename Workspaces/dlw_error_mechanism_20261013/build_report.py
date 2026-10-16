"""Build the reader report only from completed, validated experiments."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
import json
import re
import subprocess
import pandas as pd
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'report/dlw_error_mechanism_20261013.html'
ASSETS = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'
NAMES = {'SD': 'PE', 'FD': 'FD'}


def transport(case):
    tags = [f'{case}_T0.010_dt0.000100_parts_cache5',
            f'{case}_T0.010_dt0.000100_parts',
            f'{case}_T0.010_dt0.000500_parts_cache5']
    for tag in tags:
        path = HERE / 'transport' / tag / 'validation.json'
        if path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
            assert data['passed'], path
            return data
    raise FileNotFoundError(f'No completed and validated transport: {case}')


def table(caption, headers, rows):
    cells = ''.join('<tr>' + ''.join('<td>' + html.escape(str(x)) + '</td>' for x in row) + '</tr>' for row in rows)
    return ('<div class="table-wrap"><table><caption>' + html.escape(caption) + '</caption><thead><tr>'
            + ''.join('<th scope="col">' + html.escape(x) + '</th>' for x in headers)
            + '</tr></thead><tbody>' + cells + '</tbody></table></div>')


def sci(x):
    return f'{x:.4e}'


def make_content():
    source = (HERE / 'report.source.html').read_text(encoding='utf-8')
    data = {case: transport(case) for case in ('A', 'C')}
    tokens = {}
    initial = pd.read_csv(HERE / 'sources/baseline_source_budget.csv')
    rows = []
    for case, field in [('A', 'v'), ('C', 'u')]:
        for kind in ('SD', 'FD'):
            r = initial[(initial.case == case) & (initial.field == field) & (initial.model == kind)].iloc[0]
            rows.append([f'{case}：{field}', NAMES[kind], sci(r.rms_y), sci(r.rms_x), f'{r.cosine_y_x:+.4f}', sci(r.rms_total)])
    tokens['INITIAL_SOURCE_TABLE'] = table('表1　初始瞬间的误差源；各场 RMS', ['算例／场', '方法', 'y 源', 'x 源', 'y/x 余弦', '总源'], rows)

    rows = []
    for case, d in data.items():
        for kind in ('SD', 'FD'):
            r = next(x for x in d['final_comparisons'] if x['comparison'] == 'against_actual' and x['propagator'] == kind)
            assert r['relative_residual'] < .05 and r['cosine'] > .99
            rows.append([case, NAMES[kind], sci(r['relative_residual']), f"{r['cosine']:.10f}"])
    tokens['CLOSURE_TABLE'] = table('表2　T=0.01 独立预测与实际误差场的核对', ['算例', '方法', '场相对偏差', '场余弦'], rows)
    if data['C']['config']['dt'] != .0001:
        controls = pd.read_csv(HERE / 'transport/time_refinement_validation.csv')
        c_final = controls[(controls.case == 'C') & controls.label.str.startswith('archive_')]
        assert len(c_final) == 2 and c_final.relative_residual.max() < .001
        tokens['CLOSURE_TABLE'] += (f'<p class="note">A 传播预算取原时间步 0.0001；C 预算取 0.0005，其实际末态误差场与原时间步归档的相对差最大 {c_final.relative_residual.max():.2e}。空间方法、物理初值与观察窗不变；C 在 t=0.002 的四格预测另经细步核对。</p>')

    rows = []
    effects = {}
    for case, d in data.items():
        m = {x['label']: x for x in d['final_metrics']}
        for p in ('SD', 'FD'):
            rows.append([case, NAMES[p], sci(m[f'{p}_from_SD']['joint_rms']), sci(m[f'{p}_from_FD']['joint_rms'])])
        prop = [abs(m[f'SD_from_{s}']['joint_rms'] / m[f'FD_from_{s}']['joint_rms'] - 1) * 100 for s in ('SD', 'FD')]
        src = [abs(m[f'{p}_from_SD']['joint_rms'] / m[f'{p}_from_FD']['joint_rms'] - 1) * 100 for p in ('SD', 'FD')]
        effects[case] = {'propagator_percent': prop, 'source_percent': src}
    tokens['EXCHANGE_TABLE'] = table('表3　传播器与误差源交换；联合 RMS', ['算例', '传播器', 'PE 源', 'FD 源'], rows)
    tokens['EXCHANGE_INTERPRETATION'] = '<p>' + '；'.join(
        f'{case} 中，固定源而交换传播器，范数变化 {min(e["propagator_percent"]):.3g}%–{max(e["propagator_percent"]):.3g}%；固定传播器而交换源，变化 {min(e["source_percent"]):.2f}%–{max(e["source_percent"]):.2f}%'
        for case, e in effects.items()) + '。在通过场重建核验的短窗内，源的差别对方法排名的作用明显更大。</p>'

    rows, checks = [], []
    for case, field in [('A', 'v'), ('C', 'u')]:
        d = data[case]
        m = {x['label']: x for x in d['final_metrics']}
        for kind in ('SD', 'FD'):
            angle = next(x['cosine'] for x in d['final_source_budget'] if x['kind'] == kind and x['comparison'] == 'part_angle_' + field)
            closure = next(x['relative_residual'] for x in d['final_source_budget'] if x['kind'] == kind and x['comparison'] == 'sum_parts_vs_one_step')
            checks.append(closure)
            rows.append([f'{case}：{field}', NAMES[kind], sci(m[f'{kind}_part_y_model'][field + '_rms']), sci(m[f'{kind}_part_x_stencil'][field + '_rms']), f'{angle:+.4f}', sci(m[f'actual_{kind}'][field + '_rms'])])
    tokens['TRANSPORT_BUDGET_TABLE'] = table('表4　T=0.01 经传播的分源误差与实际误差', ['算例／场', '方法', 'y 源贡献', 'x 源贡献', 'y/x 余弦', '实际总误差'], rows)
    tokens['TRANSPORT_BUDGET_INTERPRETATION'] = (f'<p>三源之和与一步缺陷预测的场相对偏差最大为 {max(checks):.2e}。源分解在终态仍闭合：A 的 FD 保持强反向抵消，C 的 PE 保持使 u 总误差减小的反向分量。这将初始源的方向关系与真实末态误差连接起来。</p><p class="note">C 的辅助分源采用五个时刻的插值；四个独立留出时刻对主要 y/x 源的全域相对误差小于 7.72×10⁻⁸。上节的一步缺陷与传播器始终逐步直接计算，分源之和另与它们独立核对。</p>')

    refinement = pd.read_csv(HERE / 'refinement/comparison.csv')
    rows = []
    for field in ('u', 'v'):
        for dx in (.1, .025):
            v = {k: float(refinement[(refinement.model == k) & (refinement.field == field) & (refinement.dx == dx)].iloc[0].rms) for k in ('SD', 'FD')}
            rows.append([field, dx, sci(v['SD']), sci(v['FD']), f'{v["SD"] / v["FD"]:.4f}'])
    tokens['REFINEMENT_TABLE'] = table('表5　预报后的 x 加密实验；T=0.001，h=0.1', ['场', 'Δx', 'PE 误差', 'FD 误差', 'PE/FD'], rows)

    phase = pd.read_csv(HERE / 'morphology/endpoint_summary.csv')
    rows = []
    for case in ('A', 'C'):
        for kind in ('SD', 'FD'):
            r = phase[(phase.dataset == f'{case}_{kind}_RK4') & (phase.window == 'full')].iloc[0]
            rows.append([case, NAMES[kind], f'{100 * r.nonlinear_explained_fraction:.2f}%', sci(r.joint_rms_raw), sci(r.joint_rms_aligned)])
    tokens['PHASE_TABLE'] = table('表6　T=0.01 共同相位对齐；原观察窗', ['算例', '方法', '平方误差解释率', '原联合 RMS', '对齐后联合 RMS'], rows)

    boundary = pd.read_csv(HERE / 'boundary/endpoint_summary.csv')
    rows = []
    for kind in ('SD', 'FD'):
        r = boundary[(boundary.model == kind) & (boundary.field == 'u')].iloc[0]
        rows.append([NAMES[kind], f'{100 * r.delta_relative_old_error:.2f}%', f'{100 * r.y_constant_squared_fraction:.3f}%', sci(r.old_error_rms), sci(r.new_error_rms)])
    tokens['BOUNDARY_TABLE'] = table('表7　A：扩大 y 缓冲后 u 误差场的变化', ['方法', '差场／原误差范数', '条带平方解释率', '原误差 RMS', '扩大后 RMS'], rows)
    tr = pd.read_csv(HERE / 'transport/time_refinement_validation.csv')
    act = tr[(tr.case == 'A') & tr.label.str.startswith('actual_')]
    tokens['LONG_TIME_CHECK'] = f'<p>将此延长实验的时间步减半，真实误差场相对变化最大 {act.relative_residual.max():.2e}，支持上述放大来自所研究的空间离散动力学，而非当前时间步误差。</p>'
    for key, value in tokens.items():
        assert source.count(key) == 1, key
        source = source.replace(key, value)
    return source, effects


def main():
    source, effects = make_content()
    math = []

    def protect(match):
        idx = len(math)
        math.append({'tex': html.unescape(match[1] if match[1] is not None else match[2]), 'display': match[1] is not None})
        return f'MATHPLACEHOLDER{idx:05d}END'

    body = re.sub(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', protect, source, flags=re.S)
    (HERE / 'math.json').write_text(json.dumps(math, ensure_ascii=False), encoding='utf-8')
    node = "const fs=require('fs'),path=require('path');const k=require(path.join(process.argv[2],'katex.js'));const xs=JSON.parse(fs.readFileSync(path.join(process.argv[1],'math.json'),'utf8'));const ys=xs.map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error',output:'htmlAndMathml'}));fs.writeFileSync(path.join(process.argv[1],'math.rendered.json'),JSON.stringify(ys));"
    subprocess.run(['node', '-e', node, str(HERE), str(ASSETS)], check=True)
    for i, value in enumerate(json.loads((HERE / 'math.rendered.json').read_text(encoding='utf-8'))):
        body = body.replace(f'MATHPLACEHOLDER{i:05d}END', value)
    css = '''*{box-sizing:border-box}body{margin:0;background:#f5f4f1;color:#252523;font:17px/1.9 Georgia,"Times New Roman","SimSun",serif}main{max-width:1080px;margin:28px auto;padding:42px 55px;background:#fff}.eyebrow{font:13px/1.7 system-ui,sans-serif;color:#666}h1{font-size:32px;line-height:1.45;margin:17px 0 25px}h2{font-size:23px;line-height:1.6;margin:0 0 18px}.lead{font-size:19px}section{margin:36px 0;padding-top:25px;border-top:1px solid #c6c6c0}p{margin:15px 0;overflow-wrap:anywhere}a{color:#235b75;text-underline-offset:3px}a:focus-visible{outline:2px solid #235b75;outline-offset:3px}.note,footer,figcaption{font-size:14px;color:#555}.table-wrap{overflow:auto;margin:25px 0}table{border-collapse:collapse;width:100%;font:14px/1.7 Georgia,"Times New Roman","SimSun",serif;font-variant-numeric:tabular-nums}caption{text-align:left;margin-bottom:10px;font-size:15px}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #ddd;white-space:nowrap}thead th{border-top:1px solid #555;border-bottom:1px solid #555}figure{margin:28px 0}figure img{display:block;width:100%;height:auto}figcaption{margin-top:9px;line-height:1.75}.katex-display{overflow-x:auto;overflow-y:hidden;padding:8px 0;font-size:.92em}footer{border-top:1px solid #bbb;padding-top:16px;margin-top:40px}@media(max-width:720px){body{font-size:16px}main{margin:0;padding:25px 19px}h1{font-size:26px}h2{font-size:21px}.lead{font-size:17px}.katex-display{font-size:.83em}section{margin-top:30px}table{font-size:13px}}@media print{body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}h1{font-size:22pt}h2{font-size:15pt;break-after:avoid}section{margin:24px 0;padding-top:18px}.table-wrap{overflow:visible}.katex-display{overflow:visible}figure{break-inside:avoid}a{color:inherit}}'''
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="DLW实际PE/FD求解路线的误差源、传播、抵消及预测后网格实验。"><title>DLW：误差如何产生、组成与演化</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>' + css + '</style></head><body><main>' + body + '</main></body></html>'
    soup = BeautifulSoup(page, 'html.parser')
    local = []
    for tag in soup.select('[href], [src]'):
        raw = tag.get('href') or tag.get('src')
        parsed = urlsplit(raw)
        if parsed.scheme:
            continue
        if parsed.path:
            target = (OUT.parent / unquote(parsed.path)).resolve()
            assert target.exists(), target
        local.append(raw)
    assert len(soup.select('table')) == 7
    assert len(soup.select('figure img')) >= 5
    assert not soup.select('.katex-error')
    assert len(soup.select('.katex')) == len(math)
    assert not re.search(r'[A-Z_]{6,}_TABLE|MATHPLACEHOLDER|LONG_TIME_CHECK|EXCHANGE_INTERPRETATION', page)
    assert r'\(' not in body and r'\[' not in body
    assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', source)
    OUT.write_text(page, encoding='utf-8')
    result = {'report': str(OUT), 'tables': 7, 'figures': len(soup.select('figure img')), 'math_fragments': len(math), 'local_links_checked': len(local), 'strict_katex': True, 'exchange_effects': effects, 'passed': True}
    (HERE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
