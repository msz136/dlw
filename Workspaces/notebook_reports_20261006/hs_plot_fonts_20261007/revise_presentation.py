"""Apply the shared presentation revision without discarding saved outputs."""
from pathlib import Path
import hashlib
import sys
import nbformat

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parent.parent
sys.path.insert(0, str(PROJECT))
from hs_presentation import apply_presentation
from revise_hs_structure import transform

NOTEBOOK = ROOT / 'notebook/2HS数值分析report.ipynb'
before = nbformat.read(NOTEBOOK, 4)
after = apply_presentation(transform(before))
assert len(before.cells) == len(after.cells)
for old, new in zip(before.cells, after.cells):
    assert old.id == new.id
    if old.cell_type == 'code':
        assert old.get('outputs') == new.get('outputs')
        assert old.execution_count == new.execution_count
        compile(new.source, new.id, 'exec')
nbformat.validate(after)
nbformat.write(after, NOTEBOOK)
print('Updated 2HS typography and endpoint display:', hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest())
