"""Export the current DLW notebook, without execution, to a standalone report."""
from pathlib import Path
import ast
import base64
import hashlib
import html
import json
import re
import subprocess
import textwrap

from bs4 import BeautifulSoup
import mistune
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NOTEBOOK = ROOT / 'notebook' / 'DLW数值分析report.ipynb'
DEST = ROOT / 'dlw_numerical.html'
KATEX = ROOT / 'Workspaces' / 'gsg_project' / 'dlw_report' / '_assets' / 'package'
FORMULAS = []
OMITTED_CELLS = {'dlw-conclusion-text', 'dlw-summary', 'dlw-limits'}
MARKDOWN_EDITS = {
    'dlw-title': [('# DLW 数值分析 report', '# DLW 数值分析')],
    'dlw-spatial-text': [('下方代码定义共用网格、差分与场值恢复。', 'FD 与 SD2 共用上述网格、差分与场值恢复。')],
    'dlw-sd2-text': [('先定义初值与下边界的求解，再定义递推；代码中的', '代码中的')],
}
KEY_CODE = {
    'dlw-sd2_evolution': [('SD2：势导数递推与 Q、R 更新', 'H = self.h**2/4', 'rt = rxx')],
    'dlw-fd': [('FD：连续方程的差分右端', 'fp = -np.diff', 'fv = -d1')],
    'dlw-time': [('Euler 与 RK4 的时间更新', 'def step(', 'return state+dt*(k1'),
                 ('公共物理点上的误差评价', 'xx = np.linspace', 'errors = {f:')],
}
KEY_METHODS = {
    'dlw-sd': [('SD：单层线性求解', 'solve_one'),
               ('SD：逐层交替更新 F 与 G', 'advance')],
}


def markdown_source(cell):
    source = cell.source
    for old, new in MARKDOWN_EDITS.get(cell.id, []):
        if old in source:
            source = source.replace(old, new, 1)
    return source


def excerpt(source, start, end):
    lines = source.splitlines()
    first = next(i for i, line in enumerate(lines) if line.strip().startswith(start))
    last = next(i for i, line in enumerate(lines) if i >= first and line.strip().startswith(end))
    return textwrap.dedent('\n'.join(lines[first:last+1])), first+1, last+1


def method_excerpt(source, method_name):
    methods = [node for node in ast.walk(ast.parse(source))
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == method_name]
    assert len(methods) == 1, (method_name, len(methods))
    method = methods[0]
    first, last = method.lineno, method.end_lineno
    fragment = textwrap.dedent('\n'.join(source.splitlines()[first-1:last]))
    return fragment, first, last


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
code,pre{font-family:Consolas,"Microsoft YaHei",monospace}p code,li code{font-size:.88em;overflow-wrap:anywhere}
.source{margin:8px 0 22px;padding:12px 15px;border:1px solid #ddd;background:#fafafa;overflow-x:auto;font-size:9.5pt;line-height:1.65;tab-size:4;text-align:left}
.source code{white-space:pre;font-size:inherit;color:#333}.code-caption{text-indent:0;margin:18px 0 6px;font-size:10.5pt;color:#444}
.output{margin:18px 0 24px}.output pre{font-size:10pt;line-height:1.7;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:8px 0}.result-text{white-space:pre-line;text-indent:0}
.table-wrap{overflow-x:auto;margin:18px 0}table{border-collapse:collapse;font-size:10.5pt;line-height:1.6;width:100%;font-variant-numeric:tabular-nums;border-top:1.5px solid;border-bottom:1.5px solid}
th,td{padding:9px 8px;text-align:right;vertical-align:middle;white-space:nowrap;border-bottom:1px solid #ddd}thead th{border-bottom:1px solid #333;font-weight:bold}tbody th{font-weight:400}table tr:last-child td,table tr:last-child th{border-bottom:0}
figure{margin:24px 0}img{display:block;width:100%;height:auto;margin:auto}
.katex-display{overflow-x:auto;overflow-y:hidden;font-size:.88em;padding:8px 0;margin:18px 0}.katex-display>.katex{min-width:max-content}
ul,ol{padding-left:1.5em}blockquote{margin:16px 0;padding-left:16px;border-left:2px solid #ddd;color:#555}
@media(max-width:650px){body{font-size:11pt}main{margin:0;padding:28px 18px}h1{font-size:16pt}h2{font-size:13pt}h3{font-size:11.5pt}#dlw-title>p{font-size:10.5pt}.source{font-size:9pt;padding:10px}table{font-size:9pt}th,td{padding:7px}}
@media print{@page{size:A4;margin:22mm 20mm}body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}h1{font-size:18pt}h2{font-size:14pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}.source{font-size:8.5pt;padding:8px;overflow:visible}.source code{white-space:pre-wrap;overflow-wrap:anywhere}.table-wrap{overflow:visible}table{font-size:9pt}th,td{padding:5px;white-space:normal}tr,figure{break-inside:avoid}.katex-display{overflow:visible}a{color:inherit}}
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
        return '<figure><img alt="DLW 局部误差曲线" src="data:image/png;base64,' + data['image/png'].replace('\n', '') + '"></figure>'
    if 'text/html' in data:
        soup = BeautifulSoup(data['text/html'], 'html.parser')
        assert not soup.find('script')
        for table in soup.find_all('table'):
            wrapper = soup.new_tag('div', attrs={'class': 'table-wrap'})
            table.wrap(wrapper)
        return str(soup)
    if 'text/plain' in data:
        return '<pre>' + html.escape(data['text/plain']) + '</pre>'
    raise ValueError('Unsupported output MIME: ' + str(list(data)))


def build():
    # Never execute notebook code; preserve its current sources and saved outputs.
    FORMULAS.clear()
    notebook_bytes = NOTEBOOK.read_bytes()
    notebook = nbformat.reads(notebook_bytes.decode('utf-8'), as_version=4)
    cells = [cell for cell in notebook.cells if cell.id not in OMITTED_CELLS]
    markdown = mistune.create_markdown(renderer=Renderer(escape=False), plugins=['math', 'table', 'strikethrough'])
    parts = []
    visible_lines = 0
    excerpt_count = 0
    excerpt_manifest = []
    for cell in cells:
        cid = html.escape(cell.id, quote=True)
        if cell.cell_type == 'markdown':
            content = markdown(markdown_source(cell))
            parts.append(f'<section class="markdown-cell" id="{cid}" data-cell="{cid}">{content}</section>')
        elif cell.cell_type == 'code':
            snippets = []
            excerpts = [(label, *excerpt(cell.source, start, end), None)
                        for label, start, end in KEY_CODE.get(cell.id, [])]
            excerpts.extend((label, *method_excerpt(cell.source, method), method)
                            for label, method in KEY_METHODS.get(cell.id, []))
            for label, fragment, first, last, method in excerpts:
                visible_lines += last-first+1
                excerpt_count += 1
                excerpt_manifest.append({'cell':cell.id, 'label':label,
                                         'first_line':first, 'last_line':last,
                                         'method':method})
                snippets.append(f'<p class="code-caption">{html.escape(label)}</p><pre class="source key-code" data-first-line="{first}" data-last-line="{last}"><code>{html.escape(fragment)}</code></pre>')
            outputs = ''.join(f'<div class="output" data-output="{i}">{output_html(o)}</div>' for i,o in enumerate(cell.outputs))
            parts.append(f'<section class="code-cell" id="{cid}" data-cell="{cid}">{"".join(snippets)}{outputs}</section>')
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
    result += '<title>' + html.escape(title) + '</title><meta name="description" content="DLW 孤子数值分析：模型、推导、代码、误差表与结果图。">'
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
        'visible_code_excerpts':excerpt_count,'visible_code_lines':visible_lines,
        'key_code':excerpt_manifest,'image_outputs':len(soup.select('figure img')),
        'full_sources_included':False,'font_style':'Original Times New Roman / SimSun; intact embedded KaTeX fonts',
        'saved_outputs':sum(len(c.get('outputs',[])) for c in cells),'math_expressions':len(FORMULAS),
        'backup':str(before/'index.html'),'backup_sha256':sha((before/'index.html').read_bytes()),
        'archive':str(archive),'standalone':True,'notebook_executed':False}
    assert NOTEBOOK.read_bytes() == notebook_bytes
    (HERE/'build_validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    build()
