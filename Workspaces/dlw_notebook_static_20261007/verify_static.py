"""Compare the selected report cells, formulas, and saved outputs to the notebook."""
from pathlib import Path
import base64
import hashlib
import json
import re

from bs4 import BeautifulSoup
import mistune
import nbformat
import build_static as build


def verify():
    notebook = nbformat.read(build.NOTEBOOK,4)
    cells = [c for c in notebook.cells if c.id not in build.OMITTED_CELLS]
    manifest=json.loads((build.HERE/'build_validation.json').read_text('utf-8'))
    assert manifest['source_sha256']==hashlib.sha256(build.NOTEBOOK.read_bytes()).hexdigest()
    page = BeautifulSoup(build.DEST.read_text('utf-8'),'html.parser')
    assert [x['data-cell'] for x in page.select('main > section[data-cell]')] == [c.id for c in cells]
    assert not page.select('.code-appendix,.full-source,#section-8')
    assert not any(page.find(attrs={'data-cell':cid}) for cid in build.OMITTED_CELLS)
    assert len(page.select('h2')) == 7
    assert not page.select('nav')
    assert not page.select('main pre,main code,.key-code,.code-caption')
    visible_text = page.main.get_text()
    assert not any(term in visible_text for term in (
        '代码', 'Exact', 'logsumexp', 'solve_one', 'advance', 'uv(js',
        'mean', 'cov', 'axis=', 'fp', 'fv', 'mx'))
    assert page.select('main > section')[-1]['data-cell'] == 'dlw-field-plots'
    assert '参考资料' not in page.get_text() and '完整代码' not in page.get_text()
    build.FORMULAS.clear()
    markdown = mistune.create_markdown(renderer=build.Renderer(escape=False),plugins=['math','table','strikethrough'])
    results=[]
    png_hashes=[]
    for cell in cells:
        section=page.find('section',attrs={'data-cell':cell.id})
        if cell.cell_type=='code':
            actual_outputs=section.select('div.output')
            assert len(actual_outputs)==len(cell.outputs)
            for actual,output in zip(actual_outputs,cell.outputs):
                data=output.get('data',{})
                if output.output_type=='stream':
                    assert actual.get_text() == output.text
                elif 'image/png' in data:
                    actual_png=base64.b64decode(actual.img['src'].split(',',1)[1])
                    source_png=base64.b64decode(data['image/png'])
                    assert actual_png==source_png
                    png_hashes.append(hashlib.sha256(actual_png).hexdigest())
                elif 'text/html' in data:
                    original=BeautifulSoup(data['text/html'],'html.parser')
                    expected=BeautifulSoup(build.output_html(output),'html.parser')
                    assert actual.get_text().split() == expected.get_text().split(), cell.id
                    assert len(actual.select('table'))==len(expected.select('table'))
                    numeric = lambda soup:[re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',td.get_text()) for td in soup.select('td')]
                    assert numeric(actual)==numeric(original),cell.id
                else:
                    assert actual.get_text()==data['text/plain']
            results.append({'cell':cell.id,'source_code_omitted':True,'outputs_exact':True,'outputs':len(cell.outputs)})
        else:
            expected=BeautifulSoup(markdown(build.markdown_source(cell)),'html.parser')
            actual=BeautifulSoup(str(section),'html.parser')
            for node in expected.select('[data-math]'):
                node.decompose()
            for node in actual.select('[data-formula],nav'):
                node.decompose()
            assert actual.get_text().split()==expected.get_text().split(),cell.id
            results.append({'cell':cell.id,'markdown_content_exact_except_presentation_edits':True})
    annotations=[x.select_one('annotation').get_text() for x in page.select('[data-formula]')]
    assert annotations==[x['tex'] for x in build.FORMULAS]
    assert not page.select('script,button,input,textarea,iframe')
    assert not page.select('[href]:not([href^="#"]),[src]:not([src^="data:"])')
    assert 'url(fonts/' not in page.style.get_text()
    assert '.katex{font:normal 1.21em KaTeX_Main' in page.style.get_text()
    assert manifest['visible_code_excerpts']==manifest['visible_code_lines']==0
    assert not manifest['key_code']
    assert not any(x in page.get_text() for x in ['$$','\\[','\\]'])
    result={'success':True,'cells':results,'formula_sources_exact':True,'math_expressions':len(annotations),
            'png_sha256':png_hashes,'retained_saved_outputs_preserved':True,'standalone_no_execution_controls':True,
            'visible_code_excerpts':len(page.select('.key-code')),
            'visible_code_lines':sum(len(p.code.get_text().splitlines()) for p in page.select('.key-code')),
            'full_code_included':False,'omitted_cells':sorted(build.OMITTED_CELLS),
            'markdown_presentation_edits':build.MARKDOWN_EDITS,
            'no_code_elements_or_implementation_prose':True,'key_code':manifest['key_code'],
            'html_sha256':hashlib.sha256(build.DEST.read_bytes()).hexdigest(),
            'notebook_sha256':hashlib.sha256(build.NOTEBOOK.read_bytes()).hexdigest()}
    (build.HERE/'content_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='cells'},ensure_ascii=False))


if __name__=='__main__':
    verify()
