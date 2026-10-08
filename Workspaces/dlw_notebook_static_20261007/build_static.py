"""Export the current DLW notebook, without execution, to a standalone report."""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
import subprocess

from bs4 import BeautifulSoup
import mistune
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NOTEBOOK = ROOT / 'notebook' / 'DLW数值分析report.ipynb'
DEST = ROOT / 'dlw_numerical.html'
KATEX = ROOT / 'Workspaces' / 'gsg_project' / 'dlw_report' / '_assets' / 'package'
FORMULAS = []
OMITTED_CELLS = {'dlw-conclusion-text', 'dlw-summary', 'dlw-limits',
                 'dlw-field-data', 'dlw-plot-config-text', 'dlw-field-config', 'dlw-field-helpers'}
MARKDOWN_EDITS = {
    'dlw-field-text': [('## 8', '## 7')],
    'dlw-title': [('# DLW 数值分析 report', '# DLW 数值分析')],
    'dlw-spatial-text': [('下方代码定义共用网格、差分与场值恢复。', '')],
    'dlw-sd2-text': [('这里的 $D_1$ 使用代码 `dx` 的端点跃变量修正。', '算子 $D_1$ 按端点跃变量延拓。')],
}
RK4_RECURRENCE = r'''记 $\mathcal F$ 为对应空间离散的右端，RK4 的递推为

$$\begin{aligned}
k_1&=\mathcal F(t_n,z^n),\\
k_2&=\mathcal F\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}k_1\right),\\
k_3&=\mathcal F\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}k_2\right),\\
k_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t k_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4).
\end{aligned}$$'''


def markdown_source(cell):
    source = cell.source
    source = source.split('\n\n**对应代码。**', 1)[0]
    if cell.id == 'dlw-exact-text':
        source = source.split('\n\n精确参照由 `Exact`', 1)[0]
    if cell.id == 'dlw-time-text' and 'k_1&=' not in source:
        source = source.replace('\n\n在 $x\\in[-10,10]$', '\n\n'+RK4_RECURRENCE+'\n\n在 $x\\in[-10,10]$',1)
    for old, new in MARKDOWN_EDITS.get(cell.id, []):
        if old in source:
            source = source.replace(old, new, 1)
    return source


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Renderer(mistune.HTMLRenderer):
    def math(self, tex, display):
        index = len(FORMULAS)
        FORMULAS.append({'tex': tex, 'display': display})
        tag = 'div' if display else 'span'
        return f'<{tag} data-math="{index}"></{tag}>'

    def block_math(self, text):
        return self.math(text, True) + '\n'

    def inline_math(self, text):
        return self.math(text, False)


CSS = '''
*{box-sizing:border-box}body{margin:0;background:#eee;color:#111;font:12pt/1.8 "Times New Roman",SimSun,serif}
main{max-width:1000px;margin:28px auto;padding:60px 56px;background:#fff}
h1{font-size:18pt;line-height:1.65;text-align:center;font-weight:bold;margin:0 0 32px}
h2{font-size:14pt;line-height:1.5;margin:34px 0 18px;scroll-margin-top:24px}
h3{font-size:12pt;line-height:1.55;margin:28px 0 12px}
h1,h2,h3{text-wrap:balance}p{margin:12px 0;text-align:justify;text-indent:2em;text-wrap:pretty}
#dlw-title>p{text-indent:0;font-size:11pt;line-height:1.8;margin:0 0 24px}
a{color:#222;text-underline-offset:3px}strong{font-weight:bold}
.output{margin:18px 0 24px}.result-text{white-space:pre-line;text-indent:0}
.table-wrap{overflow-x:auto;margin:18px 0}table{border-collapse:collapse;font-size:10.5pt;line-height:1.6;width:100%;font-variant-numeric:tabular-nums;border:0;border-top:1.5px solid #111;border-bottom:1.5px solid #111}
tr,th,td{border:0}th,td{padding:9px 8px;text-align:right;vertical-align:middle;white-space:nowrap}thead{border-bottom:1px solid #111}thead th{font-weight:bold}tbody th{font-weight:400}
figure{margin:24px 0}img{display:block;width:100%;height:auto;margin:auto}
.katex-display{overflow-x:auto;overflow-y:hidden;font-size:.88em;padding:8px 0;margin:18px 0}.katex-display>.katex{min-width:max-content}
ul,ol{padding-left:1.5em}blockquote{margin:16px 0;padding-left:16px;border-left:2px solid #ddd;color:#555}
@media(max-width:650px){body{font-size:11pt}main{margin:0;padding:28px 18px}h1{font-size:16pt}h2{font-size:13pt}h3{font-size:11.5pt}#dlw-title>p{font-size:10.5pt}table{font-size:9pt}th,td{padding:7px}}
@media print{@page{size:A4;margin:22mm 20mm}body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}h1{font-size:18pt}h2{font-size:14pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}.table-wrap{overflow:visible}table{font-size:9pt}th,td{padding:5px;white-space:normal}tr,figure{break-inside:avoid}.katex-display{overflow:visible}a{color:inherit}}
'''


def font_css():
    css = (KATEX / 'dist' / 'katex.min.css').read_text('utf-8')
    def embed(match):
        name = match.group(1)
        data = base64.b64encode((KATEX / 'dist' / 'fonts' / name).read_bytes()).decode('ascii')
        return f'src:url(data:font/woff2;base64,{data}) format("woff2")'
    faces = css.count('@font-face')
    css = re.sub(r'src:url\(fonts/([^)]*\.woff2)\)[^;}]*', embed, css)
    assert 'url(fonts/' not in css
    assert css.count('@font-face') == faces
    assert '.katex{font:normal 1.21em KaTeX_Main' in css
    assert css.count('{') == css.count('}')
    return css


def output_html(output):
    kind = output.output_type
    if kind == 'stream':
        return '<p class="result-text">' + html.escape(output.text) + '</p>'
    if kind == 'error':
        raise ValueError('The notebook contains an error output')
    data = output.get('data', {})
    if 'image/png' in data:
        return '<figure><img alt="DLW 数值与解析物理场或绝对误差分布" src="data:image/png;base64,' + data['image/png'].replace('\n', '') + '"></figure>'
    if 'text/html' in data:
        soup = BeautifulSoup(data['text/html'], 'html.parser')
        assert not soup.find('script')
        for table in soup.find_all('table'):
            if 'dataframe' in table.get('class', []):
                for row in table.find_all('tr'):
                    first = row.find(['th','td'])
                    assert first.name == 'th'
                    first.decompose()
                for td in table.find_all('td'):
                    singleton = re.fullmatch(r'\((-?\d+(?:\.\d+)?),\)',td.get_text(strip=True))
                    if singleton:
                        td.string = singleton.group(1)
            labels = {'fixed':'固定网格', 'moving':'动网格', 'Midpoint':'隐式中点',
                      'dt 与 dt/2 场差':'Δt 与 Δt/2 场差',
                      'dt/2 与 dt/4 场差':'Δt/2 与 Δt/4 场差'}
            for cell in table.find_all(['th','td']):
                label = cell.get_text(strip=True)
                if label in labels:
                    cell.string = labels[label]
            wrapper = soup.new_tag('div', attrs={'class': 'table-wrap'})
            table.wrap(wrapper)
        return str(soup)
    if 'text/plain' in data:
        return '<p class="result-text">' + html.escape(data['text/plain']) + '</p>'
    raise ValueError('Unsupported output MIME: ' + str(list(data)))


def build():
    # Never execute notebook code; preserve its current sources and saved outputs.
    FORMULAS.clear()
    notebook_bytes = NOTEBOOK.read_bytes()
    notebook = nbformat.reads(notebook_bytes.decode('utf-8'), as_version=4)
    cells = [cell for cell in notebook.cells if cell.id not in OMITTED_CELLS]
    markdown = mistune.create_markdown(renderer=Renderer(escape=False), plugins=['math', 'table', 'strikethrough'])
    parts = []
    for cell in cells:
        cid = html.escape(cell.id, quote=True)
        if cell.cell_type == 'markdown':
            content = markdown(markdown_source(cell))
            parts.append(f'<section class="markdown-cell" id="{cid}" data-cell="{cid}">{content}</section>')
        elif cell.cell_type == 'code':
            outputs = ''.join(f'<div class="output" data-output="{i}">{output_html(o)}</div>' for i,o in enumerate(cell.outputs))
            parts.append(f'<section class="output-cell" id="{cid}" data-cell="{cid}">{outputs}</section>')
        else:
            raise ValueError('Unsupported cell type ' + cell.cell_type)
    soup = BeautifulSoup(''.join(parts), 'html.parser')
    rendered = json.loads(subprocess.run(['node', str(HERE/'render_math.cjs')], input=json.dumps(FORMULAS), text=True, encoding='utf-8', capture_output=True, check=True).stdout)
    for node in list(soup.select('[data-math]')):
        index = int(node['data-math'])
        node.clear()
        node.append(BeautifulSoup(rendered[index], 'html.parser'))
        node['data-formula'] = str(index)
        del node['data-math']
    for i,heading in enumerate(soup.select('h2'),1):
        heading['id'] = 'section-' + str(i)
    title = soup.h1.get_text()
    style = font_css() + CSS
    license_text = (KATEX/'LICENSE').read_text('utf-8').replace('--','—')
    result = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    result += '<title>' + html.escape(title) + '</title><meta name="description" content="DLW 孤子数值分析：精确解、离散递推、误差比较与结果图。">'
    result += '<style>' + style + '</style></head><body><main>' + str(soup) + '</main></body></html>\n'
    result += '<!-- KaTeX license\n' + license_text + '\n-->\n'
    before = HERE/'before'
    before.mkdir(exist_ok=True)
    if not (before/'index.html').exists():
        (before/'index.html').write_bytes(DEST.read_bytes())
    archive = ROOT/'report'/'DLW数值分析_原HTML_20261007.html'
    if not archive.exists():
        old = (before/'index.html').read_text('utf-8')
        assert '<head>' in old
        archive.write_text(old.replace('<head>', '<head>\n<base href="../">', 1), encoding='utf-8')
    DEST.write_text(result, encoding='utf-8')
    manifest = {'success':True, 'source':str(NOTEBOOK), 'source_sha256':sha(notebook_bytes),
        'delivery':str(DEST),'delivery_sha256':sha(DEST.read_bytes()),'bytes':DEST.stat().st_size,
        'source_cells':len(notebook.cells),'cells':len(cells),
        'code_cells':sum(c.cell_type=='code' for c in cells),
        'omitted_cells':[c.id for c in notebook.cells if c.id in OMITTED_CELLS],
        'table_of_contents':False,
        'visible_code_excerpts':0,'visible_code_lines':0,
        'key_code':[],'image_outputs':len(soup.select('figure img')),
        'presentation':'mathematical exposition and saved numerical results',
        'full_sources_included':False,'font_style':'Original Times New Roman / SimSun; intact embedded KaTeX fonts',
        'saved_outputs':sum(len(c.get('outputs',[])) for c in cells),'math_expressions':len(FORMULAS),
        'backup':str(before/'index.html'),'backup_sha256':sha((before/'index.html').read_bytes()),
        'archive':str(archive),'standalone':True,'notebook_executed':False}
    assert NOTEBOOK.read_bytes() == notebook_bytes
    (HERE/'build_validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    build()
