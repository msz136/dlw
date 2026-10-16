"""Add the bilinear-to-P/W derivation as Markdown, preserving every executable cell."""
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import hashlib
import io
import json
import re
import shutil
import nbformat
import build_dlw_numerics_notebook as builder
from revise_dlw_structure import TEXT

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATH = ROOT / 'notebook/DLW数值分析report.ipynb'

def main():
    backup = HERE / 'before_sd_derivation'
    backup.mkdir(exist_ok=True)
    for path in (PATH, ROOT/'PROGRESS_LOG.md', ROOT/'FILE_INDEX.md'):
        target = backup / path.name
        if not target.exists():
            shutil.copy2(path, target)
    before = nbformat.read(PATH, 4)
    original_code = {c.id: json.dumps(c, sort_keys=True) for c in before.cells if c.cell_type == 'code'}
    sd = next(c for c in before.cells if c.id == 'dlw-sd-text')
    sd.source = TEXT['sd-text'].strip()
    nbformat.validate(before)
    assert original_code == {c.id: json.dumps(c, sort_keys=True) for c in before.cells if c.cell_type == 'code'}
    nbformat.write(before, PATH)
    with patch('nbformat.write') as write, patch.object(Path, 'write_text'), redirect_stdout(io.StringIO()):
        builder.build()
    generated = write.call_args.args[0]
    assert [(c.id, c.source) for c in generated.cells] == [(c.id, c.source) for c in before.cells]

    # Reuse the existing symbolic identities for precisely this elimination.
    symbolic_source = ROOT/'Workspaces/dlw_semidiscrete/verify_nonlinear_closure.py'
    symbolic_prefix = symbolic_source.read_text(encoding='utf-8').split('original_u =', 1)[0]
    with redirect_stdout(io.StringIO()) as output:
        exec(compile(symbolic_prefix, str(symbolic_source), 'exec'), {})
    checks = output.getvalue().splitlines()
    sha = hashlib.sha256(PATH.read_bytes()).hexdigest()
    for name in ('dlw_build_validation.json', 'dlw_delivery_validation.json', 'dlw_execution_validation.json'):
        path = HERE/name
        evidence = json.loads(path.read_text(encoding='utf-8'))
        evidence.setdefault('before_sd_derivation_sha256', evidence['notebook_sha256'])
        evidence['notebook_sha256'] = sha
        evidence['sd_derivation_revision'] = 'Markdown only; all code cells, execution counts and outputs unchanged'
        path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    result_path = HERE/'sd_derivation_validation.json'
    result = dict(success=True, notebook=str(PATH), notebook_sha256=sha,
        changed_cell='dlw-sd-text', code_outputs_and_execution_counts_identical=True,
        generator_sources_match=True, symbolic_checks=checks, backup=str(backup))
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    # Merge into the existing topic without displaying or reading its history into chat.
    progress_path = ROOT/'PROGRESS_LOG.md'
    progress = progress_path.read_bytes().decode('utf-8')
    pattern = re.compile(r'(^> \*\*2026-10-06（DLW数值分析笔记本）：\*\* )([^\r\n]*)', re.MULTILINE)
    match = pattern.search(progress)
    assert match is not None
    history = re.sub(r'^\*\*SD推导：\*\* .*? \*\*既有记录：\*\* ', '', match.group(2))
    note = (r'**SD推导：** 第2.1节补入两条 $B_{a\mp h/2}F_j\cdot G=0$ 到 $P_t,W_t$ 的 '
            'LaTeX 推导：对数归一化、和差、格点差分消势；无新增代码，17 个原代码单元及输出完整保持，'
            '相关符号恒等式核对通过。 **既有记录：** ')
    progress = progress[:match.start()]+match.group(1)+note+history+progress[match.end():]
    progress_path.write_bytes(progress.encode('utf-8'))
    index_path = ROOT/'FILE_INDEX.md'
    index = index_path.read_bytes().decode('utf-8')
    newline = '\r\n' if '\r\n' in index else '\n'
    lines = []
    for path in [Path(__file__).resolve(), result_path, *sorted(backup.glob('*'))]:
        relative = path.relative_to(ROOT).as_posix()
        if ']('+relative+')' not in index:
            lines.append('- ['+relative+']('+relative+')')
    end = '<!-- NOTEBOOK_REPORTS_INDEX_END -->'
    assert index.count(end) == 1
    if lines:
        index = index.replace(end, newline.join(lines)+newline+newline+end, 1)
        index_path.write_bytes(index.encode('utf-8'))
    print(json.dumps({k:v for k,v in result.items() if k != 'symbolic_checks'}, ensure_ascii=False, indent=2))
    print('Symbolic identities checked:', len(checks))

if __name__ == '__main__':
    main()
