"""Build the GSG / 2HS report source, reusing existing measured tables."""
from pathlib import Path
import html
import re
import json
import base64
import subprocess
import sys
import markdown
from bs4 import BeautifulSoup
from scipy.integrate._ivp import dop853_coefficients as dc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sections(path):
    text = path.read_text(encoding='utf-8')
    result = {}
    for match in re.finditer(r'^#{2,3} (.+)\n([\s\S]*?)(?=^#{1,3} |\Z)', text, re.M):
        tables = re.findall(r'^\|.+\|\n(?:\|.*\|\n)+', match[2], re.M)
        if tables:
            result[match[1]] = tables[0]
    return result


def details(title, content):
    return f'<details markdown="1"><summary>{title}</summary>\n\n{content}\n\n</details>'


from four_scheme_results import NAMES as SCHEMES


def cells(table):
    return [[v.strip() for v in row.strip().strip('|').split('|')]
            for row in table.strip().splitlines()]


def grid_table(table):
    source = cells(table)
    assert source[0][-2:] == ['普通ALE＋Rm动格', '普通ALE＋固定格']
    rows = ['| p | ' + ' | '.join(SCHEMES) + ' |', '|---:|' + '---:|'*6]
    for row in source[2:]:
        assert len(row) == 7
        rows.append('| ' + ' | '.join([row[0], '—', '—', '—', '—', row[-2], row[-1]]) + ' |')
    return '\n'.join(rows)


def time_table(table):
    source = cells(table)
    assert source[0][1:] == ['Euler', 'Heun', 'RK4', 'RK8']
    rm = next(row[1:] for row in source[2:] if row[0].startswith('DR '))
    fixed = next(row[1:] for row in source[2:] if row[0].startswith('DF '))
    rows = ['| 方案 | Euler | Heun | RK4 | RK8 |', '|---|---:|---:|---:|---:|']
    for name, values in zip(SCHEMES, [['—']*4]*4+[rm, fixed]):
        rows.append('| ' + ' | '.join([name]+values) + ' |')
    return '\n'.join(rows)


def main():
    src = (HERE / '_src/numerical_analysis.md').read_text(encoding='utf-8')
    if '<!-- DLW_MAIN_TABLE -->' in src:
        subprocess.run([sys.executable,str(HERE/'integrate_dlw_numerics.py')],check=True)
        dlw=json.loads((HERE/'dlw_numerical_update/integration.json').read_text(encoding='utf-8'))
        for marker,key in [('MAIN','main_table'),('HALF','half_table'),('FINE','fine_table')]:
            src=src.replace(f'<!-- DLW_{marker}_TABLE -->',dlw[key])
    if '<!-- ATLAS_COUNTS -->' in src:
        from sync_waveform_atlas import main as update_atlas
        update_atlas()
        atlas=json.loads((HERE/'atlas_update/integration.json').read_text(encoding='utf-8'))
        src=src.replace('<!-- ATLAS_COUNTS -->',atlas['counts_table'])
        src=src.replace('<!-- ATLAS_EXAMPLES -->',atlas['examples_table'])
    from four_scheme_results import ReviewedTables, METHODS
    tables=ReviewedTables()
    tables.audit()
    if '<!-- REVIEWED_FIGURES -->' in src:
        from plot_four_scheme_waveforms import main as plot_reviewed
        plot_reviewed()
        src=src.replace('<!-- REVIEWED_FIGURES -->',(HERE/'four_scheme_figures/figures.html').read_text(encoding='utf-8'))
    src=src.replace('<!-- REVIEW_COUNTS -->',tables.count_table())
    src = src.replace('<!-- TIME_TABLE_MAIN -->', tables.time_table(12,.25))
    src = src.replace('<!-- TIME_TABLE_REST -->', '\n\n'.join(details(
        f'20参数完整表：{label}，t={t}（N=200，Δt=.0125，8001评价点）',tables.parameter_table(200,m,t))
        for m,label in METHODS.items() for t in (.25,.5)))
    src = src.replace('<!-- DYNAMIC_TABLE_MAIN -->', tables.parameter_table(400,'rk4',.5))
    src = src.replace('<!-- DYNAMIC_TABLE_REST -->', '\n\n'.join(details(
        f'20参数完整表：{label}，t={t}（N=400，Δt=.003125，16001评价点）',tables.parameter_table(400,m,t))
        for m,label in METHODS.items() for t in (.25,.5) if (m,t)!=('rk4',.5)))
    rows = ['| 级 i | cᵢ | bᵢ | 非零 aᵢⱼ（j 从 1 开始） |', '|---:|---:|---:|---|']
    for i in range(12):
        coeff = '; '.join(f'a({i+1},{j+1})={dc.A[i,j]:.17g}' for j in range(i) if dc.A[i,j] != 0)
        rows.append(f'| {i+1} | {dc.C[i]:.17g} | {dc.B[i]:.17g} | {coeff or "—"} |')
    src = src.replace('<!-- RK8_COEFFICIENTS -->', details('DOP853 八阶主公式：十二级完整系数', '\n'.join(rows)))
    # Protect TeX before Markdown: underscores, backslashes and tables must survive.
    formulas = []
    def protect(m):
        formulas.append(m[0])
        return f'MATHPLACEHOLDER{len(formulas)-1}END'
    src = re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$', protect, src)
    src = re.sub(r'^## ', '### ', src, flags=re.M)
    body = markdown.markdown(src, extensions=['tables', 'md_in_html'])
    for i, formula in enumerate(formulas):
        # Decode author-supplied entities once, then escape all HTML-sensitive math.
        body = body.replace(f'MATHPLACEHOLDER{i}END', html.escape(html.unescape(formula), quote=False))
    soup = BeautifulSoup(body, 'html.parser')
    title = soup.h1.extract().get_text()
    for img in soup.find_all('img'):
        relative=img['src']
        path=ROOT/relative
        assert path.is_file(),relative
        img['data-source']=relative
        img['src']='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
    for table in soup.find_all('table'):
        table.wrap(soup.new_tag('div', attrs={'class':'tablewrap', 'tabindex':'0', 'role':'region', 'aria-label':'数据表，可横向滚动'}))
    for img in soup.find_all('img'):
        img['loading'] = 'lazy'
    css = '''
:root{color-scheme:light;--paper:#fffdf7;--ink:#292d29;--muted:#62665d;--rule:#d8d7ca;--accent:#365e52}*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:#eeede5;color:var(--ink);font:17px/1.9 "Iowan Old Style","Palatino Linotype",Georgia,"Songti SC","Source Han Serif SC","Noto Serif CJK SC","SimSun",serif}main{max-width:1160px;margin:28px auto;padding:54px 64px 64px;background:var(--paper)}header{border-bottom:2px solid var(--accent);padding-bottom:24px;margin-bottom:25px}h1{font-size:34px;line-height:1.4;letter-spacing:.01em;margin:14px 0}h2{font-size:28px;line-height:1.5;margin-top:70px;padding-bottom:14px;border-bottom:2px solid var(--accent)}h3{font-size:21px;margin-top:38px;line-height:1.6}p{margin:16px 0}a{color:#245a4d;text-underline-offset:4px}a:focus-visible,summary:focus-visible,.tablewrap:focus-visible{outline:3px solid #997d35;outline-offset:3px}.eyebrow,.meta,figcaption,.endnote{color:var(--muted);font-size:14px}.lead{border-left:3px solid var(--accent);padding:16px 22px;background:#f0f3e9;margin:24px 0}nav{display:flex;flex-wrap:wrap;gap:10px 24px;padding:18px 0;border-block:1px solid var(--rule);font-size:15px}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.65;font-variant-numeric:tabular-nums}th,td{text-align:left;vertical-align:top;padding:12px 10px;border-bottom:1px solid var(--rule)}th{background:#eaece2;font-weight:600}tr:nth-child(even) td{background:#f7f7f0}.tablewrap{overflow:auto;margin:22px 0;max-width:100%}.tablewrap table{min-width:710px}.katex-display{overflow-x:auto;overflow-y:hidden;padding:10px 2px;font-size:.98em}details{margin:20px 0;padding:14px 18px;border:1px solid var(--rule);background:#fafaf4}summary{cursor:pointer;font-size:15px;font-weight:600}figure{margin:30px 0}img{max-width:100%;height:auto;display:block;margin:auto}figcaption{margin-top:10px}footer{border-top:1px solid var(--rule);margin-top:44px;padding-top:16px}.skip{position:absolute;left:12px;top:-100px}.skip:focus{top:12px;background:white;padding:10px;z-index:5}@media(max-width:760px){main{padding:25px 20px;margin:0}h1{font-size:27px}h2{font-size:24px;margin-top:50px}h3{font-size:19px}body{font-size:16px}.katex-display{font-size:.86em}}@media print{body,main{background:white}main{margin:0;padding:0;max-width:none}nav,.skip{display:none}h2,h3{break-after:avoid}tr{break-inside:avoid}.tablewrap{overflow:visible}.tablewrap table{min-width:0;font-size:10px}details{border:0}details>*{display:block!important}}
'''
    output = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="先整理GSG原文五种数值方案，再比较2HS的可积半离散与普通差分、守恒密度动网格与固定网格，以及四种时间算法的已有双场误差。">
<title>{title}</title><style>@@KATEX_CSS@@</style><style>{css}</style></head>
<body><a class="skip" href="#main">跳到正文</a><main id="main"><header><div class="eyebrow">数值分析</div><h1>{title}</h1><p class="meta">2026 年 9 月 27 日 · <a href="index.html">项目主报告</a></p></header>
{soup}
<footer class="meta">实验数据截至 2026-09-27。</footer></main>
<script>@@KATEX_JS@@</script><script>document.addEventListener('DOMContentLoaded',()=>{{renderMathInElement(document.getElementById('main'),{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false,strict:false}});}});</script></body></html>'''
    (HERE / '_src/numerical_analysis.src.html').write_text(output, encoding='utf-8')
    manifest = {'math_expressions':len(formulas), 'chapters':len(soup.find_all('h2')), 'embedded_images':len(soup.find_all('img')), 'time_tables':9, 'dynamic_tables':8,
                'reviewed_expanded_numeric_cells':1280,'table_source':'Workspaces/hs_four_schemes_20260927/out/main_cells.csv',
                'scheme_order':SCHEMES, 'available_schemes':['S1','S2','S3','S4'], 'unconstructed_schemes':[],
                'new_experiments':0, 'authoritative_prose':'_src/numerical_analysis.md'}
    (HERE / 'numerical_report_build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False))


if __name__ == '__main__':
    main()
