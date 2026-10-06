"""Present the saved DLW results as concise prose, paired errors and curves."""
from pathlib import Path
import csv
import json
import re
import shutil
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = ROOT / 'Workspaces/gsg_project/dlw_report'
SOURCE = REPORT / '_src/index.md'
GENERATOR = REPORT / 'generate_index_report.py'
BEFORE = HERE / 'before'
BEFORE.mkdir(parents=True, exist_ok=True)


def backup():
    for path, name in (
        (ROOT / 'index.html', 'index.html'),
        (SOURCE, 'index.md'),
        (REPORT / '_src/index.src.html', 'index.src.html'),
        (GENERATOR, 'generate_index_report.py'),
        (ROOT / 'Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md', 'CONTROLLED_RESULTS.md'),
        (ROOT / 'PROGRESS_LOG.md', 'PROGRESS_LOG.md'),
        (ROOT / 'FILE_INDEX.md', 'FILE_INDEX.md'),
    ):
        if not (BEFORE / name).exists():
            shutil.copy2(path, BEFORE / name)


def results():
    data = {}
    for relative in (
        'Workspaces/dlw_single_aligned_20260929/out/index_t001.csv',
        'Workspaces/dlw_sd2_uv_init_20260929/out/comparison.csv',
    ):
        with (ROOT / relative).open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                if float(row['t']) == .01 and row['case'] in ('fig1a', 'fig1b', 'fig3'):
                    data[(row['case'], row['method'], row['mesh'])] = row
    assert len(data) == 12
    return data


CASES = {'fig1a': '单孤子 A', 'fig1b': '单孤子 B', 'fig3': '二孤子 C'}
MODELS = ('SD', 'SD2', 'FD')
TABLE_ROWS = []


def number(value, best, dagger=False):
    mantissa, exponent = f'{value:.3e}'.split('e')
    label = f'{mantissa}e{int(exponent):d}'
    if best:
        label = f'<strong>{label}</strong>'
    if dagger:
        label += '<sup>†</sup>'
    return f'<td class="error-value" data-error="{value:.17g}">{label}</td>'


def error_table(kind, data):
    headers = ['算例', '场', *MODELS] if kind == 'space' else [
        '算例', '空间方案', '场', *(['Euler', 'RK4'] if kind == 'time' else ['固定网格', '动网格'])]
    block = ['<table class="result-table">', '<thead><tr>' + ''.join(
        f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead>', '<tbody>']
    for case, name in CASES.items():
        row_index = 0
        for model in ((None,) if kind == 'space' else MODELS):
            for field in ('u', 'v'):
                if kind == 'space':
                    values = [float(data[(case, 'RK4', 'fixed')][f'{m}_{field}']) for m in MODELS]
                    labels = list(MODELS)
                    daggers = [case == 'fig1a' and m == 'SD2' for m in MODELS]
                elif kind == 'time':
                    values = [float(data[(case, method, 'fixed')][f'{model}_{field}']) for method in ('Euler', 'RK4')]
                    labels = ['Euler', 'RK4']
                    daggers = [case == 'fig1a' and model == 'SD2'] * 2
                else:
                    values = [float(data[(case, 'RK4', mesh)][f'{model}_{field}']) for mesh in ('fixed', 'moving')]
                    labels = ['fixed', 'moving']
                    daggers = [case == 'fig1a' and model == 'SD2', False]
                best = values.index(min(values))
                row_class = 'case-start' if row_index == 0 else ('pair-start' if field == 'u' else '')
                block.append(f'<tr class="{row_class}">')
                if row_index == 0:
                    rowspan = 2 if kind == 'space' else 6
                    block.append(f'<th class="case-label" scope="rowgroup" rowspan="{rowspan}">{name}</th>')
                if kind != 'space' and field == 'u':
                    block.append(f'<th class="scheme-label" scope="rowgroup" rowspan="2">{model}</th>')
                block.append(f'<th class="field-label" scope="row">${field}$</th>')
                block.extend(number(value, i == best, daggers[i]) for i, value in enumerate(values))
                block.append('</tr>')
                TABLE_ROWS.append(dict(table=kind, case=case, model=model, field=field,
                                       labels=labels, values=values, best=labels[best]))
                row_index += 1
    block += ['</tbody>', '</table>']
    return '\n'.join(block)


def revise_body(data):
    source = (BEFORE / 'index.md').read_text(encoding='utf-8')
    prefix = r'''# DLW 孤子数值解的误差比较

<p class="abstract">以 DLW 单孤子与二孤子的解析解为参照，比较 SD、SD2 与 FD 三种空间方案、Euler 与 RK4 时间算法，以及固定网格与自适应动网格。通过双场误差与误差曲线，考察各方案的精度及网格效果。</p>

## 1　实验设计

采用 Sheng–Yu 原文的三组孤子参数（表 1），均取 $a=2$、$c_i=1$，初相位为零。SD 与 SD2 是结构半离散方案的两种变量形式，FD 为直接差分；每组参数比较三种空间方案、两种时间算法与两种网格。

<div class="caption">表 1　孤子算例的谱参数。</div>

| 算例 | 原文图号 | 谱参数 |
|---|---|---|
| 单孤子 A | 图 1(a) | $(p,q)=(1,2)$ |
| 单孤子 B | 图 1(b) | $(p,q)=(4,-3)$ |
| 二孤子 C | 图 3 | $(p_1,q_1)=(6,-5)$；$(p_2,q_2)=(4,-3)$ |

计算区间为 $x\in[-20,20)$、$y\in[-1.5,1.5]$，取 $N_x=256$、$h_y=1/8$，共 24 个 $y$ 中点层。$x$ 方向采用四阶中心差分，时间步长为 $\Delta t=1.25\times10^{-4}$，终止时刻为 $T=0.01$。

在 $x\in[-10,10]$ 的 4001 个等距点及全部 $y$ 层上，用三次样条重构数值场，计算最大绝对误差

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_h(x,y,T)-f_*(x,y,T)|,\qquad f\in\{u,v\}.\tag{1}$$

其中 $f_*$ 为解析解。各方案在同一组物理点上评价，配对条件见表 2。

<div class="caption">表 2　三项配对比较。</div>

| 对照 | 比较因素 | 固定条件 |
|---|---|---|
| 空间离散化 | SD / SD2 / FD | 算例、RK4、固定网格、格距、时间步长 |
| 时间算法 | Euler / RK4 | 算例、空间方案、固定网格、格距、时间步长 |
| 网格策略 | 固定 / 动网格 | 算例、空间方案、RK4、节点数、时间步长 |

'''
    methods = source[source.index('## 2　'):source.index('## 3　')]
    algorithm = (HERE / 'algorithm_pseudocode.md').read_text(encoding='utf-8').split('\n实现来源：', 1)[0]
    algorithm = algorithm.replace('# DLW 数值递推伪代码', '### 2.5　递推伪代码', 1)
    algorithm = re.sub(r'^## (.+)$', r'<p class="algorithm-label">\1</p>', algorithm, flags=re.M)
    methods += algorithm + '\n\n'
    curves = BeautifulSoup((HERE / 'error_curves.fragment.html').read_text(encoding='utf-8'), 'html.parser')
    curves.find('p').decompose()
    for heading, (case, name) in zip(curves.find_all('h3'), CASES.items()):
        heading['id'] = 'error-case-' + name[-1]
        heading.string = name
    for i, figure in enumerate(curves.find_all('figure'), 1):
        figure['class'] = ['field-figure']
        caption = figure.find('figcaption')
        caption.string = f'图 {i}　' + caption.get_text().replace('移动网格', '动网格')
    time_formula = re.search(r'\$\$p_f=[\s\S]*?\\tag\{16\}\$\$', source).group(0)
    parts = [prefix, methods, r'''## 3　空间离散化的比较

在 RK4 与固定网格下比较三种空间方案。表 3 列出双场最大绝对误差，加粗值为每行的最小误差。

<div class="caption">表 3　三种空间方案的误差，$T=0.01$。</div>

''', error_table('space', data), r'''

<p class="table-note">† 表 3–5 中，单孤子 A 的 SD2 固定网格结果对空间分辨率敏感。</p>

单孤子 A 中，SD 的双场误差最小，较 FD 分别降低约 30% 和 16%。单孤子 B 与二孤子 C 中，FD 的双场误差最小，SD 次之，SD2 较大。

## 4　时间算法的比较

在相同空间方案、固定网格与时间步长下比较 Euler 和 RK4。表 4 将两种算法的误差并列，加粗值为每行的较小误差。

<div class="caption">表 4　Euler 与 RK4 的误差，固定网格，$T=0.01$。</div>

''', error_table('time', data), r'''

单孤子 A 中，两种算法的误差相近，差异约在 1% 以内。单孤子 B 与二孤子 C 中，RK4 在三种空间方案下均有较小的双场误差；SD2 的 $v$ 误差分别降至 Euler 的约 $1/5.9$ 和 $1/11.3$。

后两组算例中，$u$ 场在 RK4 下为 SD 优于 SD2，在 Euler 下为 SD2 优于 SD；$v$ 场则均为 SD 优于 SD2。

固定空间配置，取 $\Delta t$、$\Delta t/2$、$\Delta t/4$，以相邻时间步长的数值场差计算观测阶

''', time_formula, r'''

Euler 的单孤子试验观测阶为 0.9874–1.0025；SD2 在原文图 3–5 二孤子中的观测阶为 0.9903–1.0001，均接近一阶。

## 5　网格策略的比较

在相同算例、空间方案、RK4、节点数和时间步长下，比较均匀固定网格与自适应动网格。加粗值为每行的较小误差。

<div class="caption">表 5　固定网格与动网格的误差，RK4，$T=0.01$。</div>

''', error_table('mesh', data), r'''

单孤子 A 中，动网格降低三种方案的双场误差。单孤子 B 中，FD 的 $u$ 误差降低约 20%，$v$ 误差增加约 10%。二孤子 C 中，SD2 的双场误差分别降低约 17% 和 24%；FD 的 $u$ 误差降低约 32%，$v$ 误差增加约 10%。

<!-- DLW_SAVED_FIELDS_BEGIN -->

## 6　Euler 局部误差曲线

取 $T=0.01$、$x\in[-1,1]$，横轴为 $x$，纵轴为各 $y$ 层上的最大绝对误差 $e_f(x)=\max_j|f_h(x,y_j,T)-f_*(x,y_j,T)|$。每图用蓝、橙、绿三条曲线分别表示 SD、SD2、FD；曲线越低，误差越小。同一算例、同一场的固定网格与动网格图采用相同纵轴尺度。

''', str(curves), r'''

<!-- DLW_SAVED_FIELDS_END -->

## 7　结论

在 RK4 固定网格下，单孤子 A 的 SD 双场误差最小，单孤子 B 与二孤子 C 的 FD 双场误差最小。后两组采用 RK4 时精度提升明显；动网格在单孤子 A 中降低双场误差，在单孤子 B 与二孤子 C 中呈现不同的场间表现。Euler 的时间自收敛观测阶接近 1。

''', source[source.index('## 参考资料'):]]
    revised = ''.join(parts)
    assert re.findall(r'\\tag\{\d+\}', source) == re.findall(r'\\tag\{\d+\}', revised)
    old_formula = re.findall(r'\$\$[\s\S]*?\$\$', source)
    new_formula = re.findall(r'\$\$[\s\S]*?\$\$', revised)
    assert old_formula == new_formula
    SOURCE.write_text(revised, encoding='utf-8')
    (HERE / 'table_results.json').write_text(json.dumps(TABLE_ROWS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def revise_css():
    generator = (BEFORE / 'generate_index_report.py').read_text(encoding='utf-8')
    extra = '''
h3{text-wrap:balance;font-size:12pt;margin:28px 0 12px}
pre{margin:16px 0 22px;padding:14px 16px;border:1px solid #ddd;background:#fafafa;overflow-x:auto;text-align:left;font-size:10pt;line-height:1.65;tab-size:4;break-inside:avoid}
pre code{font-family:Consolas,"Microsoft YaHei",monospace;white-space:pre}
.algorithm-label{text-indent:0;margin-top:24px;margin-bottom:8px;font-weight:600}
.result-table{min-width:0!important;font-size:10.5pt;line-height:1.55}
.result-table th,.result-table td{padding:9px 10px;white-space:nowrap}
.result-table thead th{text-align:center;vertical-align:bottom}
.result-table tbody th{border-bottom:0;font-weight:400}
.result-table .case-label,.result-table .scheme-label{text-align:left;vertical-align:middle}
.result-table .field-label{text-align:center;vertical-align:middle}
.result-table .case-label{font-weight:600}
.result-table .error-value{text-align:right;font-variant-numeric:tabular-nums}
.result-table strong{font-weight:700;color:#000}
.result-table sup{font-size:.7em;line-height:0;margin-left:2px}
.result-table .case-start:not(:first-child)>*{border-top:1px solid #999}
.result-table .pair-start>*{border-top:1px solid #e0e0e0}
.field-figure{margin:20px 0 32px}
.field-figure figcaption{margin-top:8px}
@media(max-width:650px){.result-table{font-size:9pt}.result-table th,.result-table td{padding:8px 6px}.field-figure{margin:20px -8px 28px}.field-figure figcaption{margin-left:8px;margin-right:8px}pre{font-size:9pt;padding:12px}}
'''
    needle = "\n'''\npage="
    assert needle in generator
    generator = generator.replace(needle, extra + needle, 1)
    generator = generator.replace("extensions=['tables','md_in_html']", "extensions=['tables','md_in_html','fenced_code']")
    GENERATOR.write_text(generator, encoding='utf-8')


if __name__ == '__main__':
    backup()
    revise_body(results())
    revise_css()
    subprocess.run(['python', str(GENERATOR)], cwd=ROOT, check=True)
    subprocess.run(['powershell', '-NoProfile', '-File', str(REPORT / 'build_html.ps1')], cwd=ROOT, check=True)
    print('Revised index: 42 comparisons, 12 curve figures; original 16 equations retained.')
