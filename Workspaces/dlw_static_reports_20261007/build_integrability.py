"""Build a theory-focused report without executing or editing its notebook."""
from pathlib import Path
import hashlib
import html
import json
import subprocess
import sys

from bs4 import BeautifulSoup
import mistune
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SHARED = ROOT / 'Workspaces' / 'dlw_notebook_static_20261007'
sys.path.insert(0, str(SHARED))
import build_static as common

NOTEBOOK = ROOT / 'notebook' / 'DLW刘维尔可积性report.ipynb'
DEST = ROOT / 'dlw_integrability.html'
OMITTED_MARKDOWN = {'load-text', 'references'}
TRIM_AFTER = {
    'conditions-text': '以下代码显示库中的参数',
    'coordinates-text': '`FieldCoordinates` 保存',
    'start-text': '下方 `physicalDLW`',
    'foundation-text': '`NormalPDOModel` 对应',
    'charges-text': '`periodicDensityPolynomial par n`',
    'conservation-text': '下方 `HasDerivAt',
    'involution-text': '`spectralCommutes` 与',
    'frequency-text': '`actualOddFrequencyPolynomial`',
    'jacobian-text': '这里是 $N$ 维 Fourier 切片',
    'generic-text': '`IsOpen`、`Dense`',
    'endpoint-text': '此处没有进一步断言',
}
EXTRA_CSS = '''
.report-title>p{text-indent:0;font-size:11pt;line-height:1.8;margin:0 0 24px}
table th:first-child,table td:first-child{text-align:left}
@media(max-width:650px){.report-title>p{font-size:10.5pt}}
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_source(cell):
    source = cell.source
    if cell.id in TRIM_AFTER:
        marker = TRIM_AFTER[cell.id]
        assert source.count(marker) == 1, cell.id
        source = source.split(marker, 1)[0].rstrip()
    if cell.id == 'intro':
        source = source.split('\n\n', 1)[0] + '\n\n从光滑周期场和原 DLW 方程出发，构造全阶谱族，依次证明守恒、对易和任意有限前缀的泛型独立性。'
    elif cell.id == 'conditions-text':
        source = source.replace('周期格点与真实场', '周期格点与闭合场')
        source = source.replace(' 用 `Fin par.M` 表示', '')
        source = source.replace('格点 $j', '格点为 $j', 1)
        source = source.replace('Adler 接口中的形式 PDO 元素，不是物理坐标', 'Adler 公式中的形式 PDO 元素')
    elif cell.id == 'start-text':
        source = source.replace('原方程与演化起点', '原 DLW 方程')
    elif cell.id == 'foundation-text':
        source = source.replace('本文保留一个显式基础参数：每个闭合场都有', '假设每个闭合场都存在')
    elif cell.id == 'energy-text':
        marker = '`H0` 展开式（8）的密度'
        assert source.count(marker) == 1
        source = source.split(marker, 1)[0].rstrip()
        source = source.replace('实际 Hamiltonian 与最终族', 'Hamiltonian 与守恒族')
        source = source.replace('第一留数的真实系数计算给出', '计算第一留数的系数，得到')
    elif cell.id == 'bracket-text':
        first = source.split('在零均值场上', 1)[0].rstrip()
        formula = source.split('$$')[-2]
        source = first + '\n\n在零均值场上 $P_0\\partial_x=\\partial_x$。对零均值方向 $v=(v_p,v_s)$，谱量的变分微分由其 Euler 梯度与 $v$ 的积分配对给出：\n\n$$' + formula + '$$'
        source = source.replace('使用真实变分配对', '定义变分配对')
    elif cell.id == 'conservation-text':
        source = source.replace('普通时间守恒', '时间守恒')
        source = source.replace('真实时空链式法则、混合导数交换与周期积分微分于是得到', '由链式法则、混合导数交换与周期积分微分，得到')
    elif cell.id == 'involution-text':
        source = source.replace('已证明的因子坐标和投影变换将其传到真实约化括号', '经因子坐标和投影变换，得到约化括号')
    elif cell.id == 'frequency-text':
        source += '\n\n这里 $F_k(\\xi)$ 是频率多项式，式（15）给出其次数与最高系数；它与第 6 节的守恒族 $F_n$ 采用不同的编号。'
    elif cell.id == 'jacobian-text':
        source = source.replace('独立性：真实 Jacobian 非零', '独立性：Jacobian 非零')
        source = source.replace('定义实际微分矩阵', '定义微分矩阵')
        source = source.replace('真实行列式的首个可能系数为', '行列式的首个可能非零系数为')
        source += '\n\n这一 Fourier 切片上的 Jacobian 子式非零，因而相应的泛函微分线性独立。'
    elif cell.id == 'generic-text':
        source = source.replace('再加入真实 $s$ 方向', '再加入 $s$ 方向')
    elif cell.id == 'endpoint-text':
        old = '以上结论一并组成 `PeriodicIntegrabilityConclusion`，最后的 `periodicIntegrability` 正是从基础前提到这一结论的主定理：'
        assert old in source
        source = source.replace(old, '以上结论组成周期场可积性定理：')
    return source.rstrip()


def build():
    source_hash = sha(NOTEBOOK)
    notebook = nbformat.read(NOTEBOOK,4)
    common.FORMULAS.clear()
    markdown = mistune.create_markdown(renderer=common.Renderer(escape=False), plugins=['math','table','strikethrough'])
    parts, snippets = [], []
    for cell in notebook.cells:
        cid = html.escape(cell.id, quote=True)
        if cell.cell_type == 'markdown':
            if cell.id in OMITTED_MARKDOWN:
                continue
            classes = 'markdown-cell' + (' report-title' if cell.id == 'intro' else '')
            parts.append(f'<section id="{cid}" data-cell="{cid}" class="{classes}">{markdown(markdown_source(cell))}</section>')
        elif cell.cell_type == 'code' and cell.id == 'lean-endpoint':
            code, first, last = common.excerpt(cell.source, 'theorem periodicIntegrability', 'general_periodic_dlw_integrability par foundation')
            snippets.append({'cell':cell.id,'first':first,'last':last,'lines':last-first+1})
            parts.append(f'<section id="{cid}" data-cell="{cid}" class="code-cell"><pre class="source key-code" data-first-line="{first}" data-last-line="{last}"><code>{html.escape(code)}</code></pre></section>')
        elif cell.cell_type != 'code':
            raise ValueError('Unsupported notebook cell')
    soup = BeautifulSoup(''.join(parts),'html.parser')
    rendered_math = json.loads(subprocess.run(['node',str(SHARED/'render_math.cjs')],input=json.dumps(common.FORMULAS),text=True,encoding='utf-8',capture_output=True,check=True).stdout)
    for node in list(soup.select('[data-math]')):
        index = int(node['data-math'])
        node.clear()
        node.append(BeautifulSoup(rendered_math[index],'html.parser'))
        node['data-formula'] = str(index)
        del node['data-math']
    nav = soup.new_tag('nav',attrs={'aria-label':'目录'})
    for i,heading in enumerate(soup.select('h2'),1):
        heading['id'] = f'section-{i}'
        link = soup.new_tag('a',href=f'#section-{i}')
        link.string = heading.get_text()
        nav.append(link)
    soup.select_one('#intro').append(nav)
    title = soup.h1.get_text()
    style = common.font_css()+common.CSS+EXTRA_CSS
    document = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    document += '<title>'+html.escape(title)+'</title><meta name="description" content="一般周期 DLW 的刘维尔可积性：周期闭合场、全阶谱族、守恒、对易与泛型独立性的理论推导。">'
    document += '<style>'+style+'</style></head><body><main>'+str(soup)+'</main></body></html>\n'
    document += '<!-- KaTeX license\n'+(common.KATEX/'LICENSE').read_text('utf-8').replace('--','—')+'\n-->\n'
    if DEST.exists() and not (HERE/'before'/'dlw_integrability.html').exists():
        (HERE/'before'/'dlw_integrability.html').write_bytes(DEST.read_bytes())
    DEST.write_text(document,encoding='utf-8')
    assert sha(NOTEBOOK) == source_hash
    manifest = {'success':True,'source':str(NOTEBOOK),'source_sha256':source_hash,'delivery':str(DEST),'delivery_sha256':sha(DEST),
      'cells':len(soup.select('section[data-cell]')),
      'source_cells':len(notebook.cells),'code_cells':len(snippets),
      'key_code':snippets,'visible_code_lines':sum(x['lines'] for x in snippets),
      'source_saved_outputs':sum(len(c.get('outputs',[])) for c in notebook.cells),
      'visible_saved_outputs':len(soup.select('section .output')),'math_expressions':len(common.FORMULAS),
      'standalone':True,'notebook_edited':False,'notebook_executed':False,
      'foundation_condition_preserved':True,'bytes':DEST.stat().st_size}
    (HERE/'build_validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    build()
