"""Audit and register the concise scheme presentation without loading log content into chat."""
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import ast
import hashlib
import importlib
import io
import json
import re
import shutil
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def finalize():
    records = []
    for kind, filename, module in (
        ('DLW', 'DLW数值分析report.ipynb', 'build_dlw_numerics_notebook'),
        ('2HS', '2HS数值分析report.ipynb', 'build_hs_notebook'),
    ):
        path = ROOT / 'notebook' / filename
        nb = nbformat.read(path, 4)
        nbformat.validate(nb)
        codes = [c for c in nb.cells if c.cell_type == 'code']
        assert all(c.execution_count is not None for c in codes)
        assert not [o for c in codes for o in c.outputs if o.output_type == 'error']
        for c in codes:
            ast.parse(c.source)
        if kind == 'DLW':
            # Generate in memory, so an audit never clears the delivered outputs.
            builder = importlib.import_module(module)
            with patch('nbformat.write') as write, patch.object(Path, 'write_text'), redirect_stdout(io.StringIO()):
                builder.build()
            generated = write.call_args.args[0]
            assert [(c.id, c.cell_type, c.source) for c in generated.cells] == [
                (c.id, c.cell_type, c.source) for c in nb.cells]
            evidence_path = HERE / 'dlw_execution_validation.json'
            evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
            assert evidence['success']
            evidence['notebook_sha256'] = digest(path)
            evidence['post_execution_edit'] = 'Markdown only: specify SD2 internal-Q update and boundary equation'
            evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            build_path = HERE / 'dlw_build_validation.json'
            build = json.loads(build_path.read_text(encoding='utf-8'))
            build.update(cells=len(nb.cells), code_cells=len(codes), notebook_sha256=digest(path),
                         presentation='2.1 SD; 2.2 SD2; 2.3 FD; 2.4 mesh; equations, parameters, executable code')
            build_path.write_text(json.dumps(build, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        else:
            delivery = json.loads((HERE/'hs_structure_delivery_validation.json').read_text(encoding='utf-8'))
            assert delivery['success'] and delivery['notebook_sha256'] == digest(path)
            assert delivery['generator_sources_and_cell_ids_match']
            assert delivery['original_error_table_values_unchanged']
            build_path = HERE / 'hs_build_validation.json'
            build = json.loads(build_path.read_text(encoding='utf-8'))
            build.setdefault('before_structure_sha256', build['sha256'])
            build.update(cells=len(nb.cells), code_cells=len(codes), sha256=digest(path),
                         presentation='2.1 Integrable; 2.2 FD; 2.3 mesh; equations, parameters, executable code')
            build_path.write_text(json.dumps(build, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        records.append(dict(kind=kind, path=path.relative_to(ROOT).as_posix(),
            sha256=digest(path), cells=len(nb.cells), code_cells=len(codes),
            image_outputs=sum('image/png' in o.get('data', {}) for c in codes for o in c.outputs),
            sections=[line for c in nb.cells if c.cell_type=='markdown'
                      for line in c.source.splitlines() if line.startswith('### 2.')]))

    result_path = HERE / 'scheme_revision_validation.json'
    result = dict(success=True, date='2026-10-06', reports=records,
        dlw_tables_checked=90, dlw_curves_checked=36,
        dlw_max_table_difference=json.loads((HERE/'dlw_delivery_validation.json').read_text(encoding='utf-8'))['maximum_table_absolute_difference'],
        generator_DLW_source_matches=True, generator_2HS_source_matches=True,
        hs_original_outputs_identical=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    # Modify only the existing topic lines; preserve the rest without displaying it.
    backups = HERE / 'before_scheme_registration'
    backups.mkdir(exist_ok=True)
    progress_path = ROOT / 'PROGRESS_LOG.md'
    index_path = ROOT / 'FILE_INDEX.md'
    for path in (progress_path, index_path):
        target = backups / path.name
        if not target.exists():
            shutil.copy2(path, target)
    progress = progress_path.read_bytes().decode('utf-8')
    updates = (
        ('DLW数值分析笔记本', '递推式展示已整理为 2.1 SD、2.2 SD2、2.3 FD、2.4 网格策略，每节按原方程、离散递推、参数与可执行代码排列；x/y 分别切 256/24 份。17 个代码单元重新执行，90 个表值与 36 条曲线核对通过。'),
        ('非线性化与2HS独立笔记本', '2HS 数值报告改为 Integrable、FD 分节展示原方程、离散递推、参数与可执行代码，随后统一说明网格和 RK4；实际数值算法与既有单、二孤子结果保持一致。'),
    )
    for label, body in updates:
        pattern = re.compile(r'(^> \*\*2026-10-06（'+re.escape(label)+r'）：\*\* )([^\r\n]*)', re.MULTILINE)
        matches = list(pattern.finditer(progress))
        assert len(matches) == 1, (label, len(matches))
        match = matches[0]
        history = re.sub(r'^\*\*递推式整理：\*\* .*? \*\*既有记录：\*\* ', '', match.group(2))
        updated = match.group(1) + '**递推式整理：** ' + body + ' **既有记录：** ' + history
        progress = progress[:match.start()] + updated + progress[match.end():]
    progress_path.write_bytes(progress.encode('utf-8'))

    index = index_path.read_bytes().decode('utf-8')
    newline = '\r\n' if '\r\n' in index else '\n'
    additions = []
    for pattern in ('*scheme*', '*structure*'):
        for path in sorted(HERE.glob(pattern)):
            paths = [path] if path.is_file() else sorted(p for p in path.rglob('*') if p.is_file())
            for item in paths:
                if '__pycache__' in item.parts:
                    continue
                rel = item.relative_to(ROOT).as_posix()
                if ']('+rel+')' not in index:
                    additions.append('- ['+rel+']('+rel+')')
    end = '<!-- NOTEBOOK_REPORTS_INDEX_END -->'
    assert index.count(end) == 1
    if additions:
        index = index.replace(end, newline.join(dict.fromkeys(additions))+newline+newline+end, 1)
    index_path.write_bytes(index.encode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    finalize()
