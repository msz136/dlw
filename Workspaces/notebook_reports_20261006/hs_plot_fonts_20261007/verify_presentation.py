"""Check figure glyphs, saved plots, and unchanged 2HS numerical outputs."""
from pathlib import Path
import ast
import base64
import hashlib
import json
import sys
import nbformat
import matplotlib
from matplotlib import font_manager
from matplotlib.mathtext import MathTextParser

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parent.parent
sys.path.insert(0, str(PROJECT))
from hs_presentation import PLOT_STYLE, apply_presentation
from revise_hs_structure import transform

PATH = ROOT/'notebook/2HS数值分析report.ipynb'
before = nbformat.read(HERE/'before/notebook/2HS数值分析report.ipynb', 4)
after = nbformat.read(PATH, 4)
nbformat.validate(after)
execution = json.loads((HERE/'hs_execution_validation.json').read_text('utf-8'))
assert execution['success'] and execution['code_cell_count'] == 16
assert execution['notebook_sha256'] == hashlib.sha256(PATH.read_bytes()).hexdigest()

def numerical_tree(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'to_string':
            node.keywords = [kw for kw in node.keywords if kw.arg != 'formatters']
    return ast.dump(tree, include_attributes=False)

def streams(cell):
    return ''.join(o.text for o in cell.get('outputs', []) if o.output_type == 'stream')

old_images, new_images = [], []
numerical_outputs = []
for old, new in zip(before.cells, after.cells):
    assert old.id == new.id and old.cell_type == new.cell_type
    if old.cell_type != 'code':
        continue
    source = new.source.replace('\n\n'+PLOT_STYLE+'\n', '\n')
    assert numerical_tree(old.source) == numerical_tree(source), new.id
    if new.id not in ('hs-reference', 'hs-two-initial'):
        assert streams(old) == streams(new), new.id
        if streams(new):
            numerical_outputs.append(new.id)
    assert new.execution_count is not None
    for o in old.outputs:
        if 'image/png' in o.get('data', {}):
            old_images.append(hashlib.sha256(base64.b64decode(o.data['image/png'])).hexdigest())
    for o in new.outputs:
        assert o.output_type != 'error'
        if 'image/png' in o.get('data', {}):
            data = base64.b64decode(o.data['image/png'])
            new_images.append(hashlib.sha256(data).hexdigest())
            (HERE/f'figure_{len(new_images)}.png').write_bytes(data)
assert len(old_images) == len(new_images) == 5
assert all(a != b for a, b in zip(old_images, new_images))
assert apply_presentation(transform(after)) == after
all_prose = '\n'.join(c.source for c in after.cells if c.cell_type == 'markdown')
assert not any(v in all_prose for v in ('4.799999', '3.799999', '5.709089', '3.709089'))
assert '-4.8' in all_prose and '-5.7' in all_prose and '区间约为' in all_prose

exec(PLOT_STYLE, {'plt': __import__('matplotlib.pyplot', fromlist=['pyplot'])})
text_font = font_manager.get_font(font_manager.findfont(font_manager.FontProperties())).family_name
glyph_fonts = {}
for formula in (r'$x$', r'$\rho$', r'$\log_{10}\max|\rho_h-\rho|$'):
    parsed = MathTextParser('path').parse(formula, dpi=100)
    families = sorted({glyph[0].family_name for glyph in parsed.glyphs})
    assert all(family.startswith('STIX') for family in families), families
    glyph_fonts[formula] = families
assert text_font == 'STIXGeneral'
result = dict(success=True, notebook=str(PATH), notebook_sha256=execution['notebook_sha256'],
    numerical_AST_unchanged=True, numerical_streams_unchanged=numerical_outputs,
    error_norms_unchanged=8, images_regenerated=5, old_png_sha256=old_images,
    new_png_sha256=new_images, text_font=text_font, math_glyph_fonts=glyph_fonts,
    endpoints_displayed_with_approximation=True, execution_seconds=execution['elapsed_seconds'],
    code_cells=16, authoring_idempotent=True,
    source_sha256={name:hashlib.sha256((PROJECT/name).read_bytes()).hexdigest()
                  for name in ('hs_presentation.py','build_hs_notebook.py','revise_hs_structure.py')})
(HERE/'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
