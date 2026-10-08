"""Register only the verified notebook, retaining the earlier proof history.

Run after the parent agent confirms native execution and visual review.
Without --register, write proposed shared records only inside this project.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DELIVERY = ROOT / 'notebook/DLW刘维尔可积性report.ipynb'
MIRROR = HERE / DELIVERY.name
NONLINEAR = ROOT / 'notebook/非线性化report.ipynb'
PROGRESS = ROOT / 'PROGRESS_LOG.md'
INDEX = ROOT / 'FILE_INDEX.md'
USAGE = ROOT / 'report/notebook_usage.html'
BACKUPS = HERE / 'before_records'
REGISTRATION = HERE / 'registration.json'
INDEX_BEGIN = '<!-- INTEGRABILITY_NOTEBOOK_INDEX_BEGIN -->'
INDEX_END = '<!-- INTEGRABILITY_NOTEBOOK_INDEX_END -->'


def sha(data: bytes | str) -> str:
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text('utf-8-sig'))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def link(path: Path, description: str) -> str:
    return f'- [{rel(path)}]({rel(path)})（{description}）'


def passed(record: dict) -> bool:
    explicit = record.get('success', record.get('passed', record.get('valid')))
    if explicit is not None:
        return bool(explicit)
    return record.get('status') in {'PASSED', 'CONTENT_REVIEW_PASSED', 'VISUAL_REVIEW_PASSED'}


def describe(path: Path) -> str:
    name = path.name
    suffix = path.suffix.lower()
    relative = path.relative_to(HERE).as_posix()
    if relative.startswith('before_records/'):
        return '使用说明、共享记录或检查脚本修改前原件'
    if relative.startswith('nonlinear_revision/before_revision/'):
        return '非线性化定义补充前的 notebook、生成器或执行证据'
    if relative.startswith('nonlinear_revision/'):
        return '式（7）关键残差定义补充的源码、真实局部执行或保留检查'
    if 'execution_inputs/' in relative:
        return '整本执行前的笔记本输入原件'
    if suffix == '.png':
        return '正文、关键代码或公式的真实浏览器预览'
    if suffix == '.lean':
        return '实际编译的 Lean 代码单元或独立审阅示例'
    if suffix == '.ipynb':
        return '交付镜像、运行前输入或真实运行输出'
    if name == 'integrability_runtime.py':
        return '复用本机 Lean 与完整已检查库的逐单元编译接口'
    if name == 'library_manifest.json':
        return '105 模块源码、编译产物及 Lean/Mathlib 身份哈希清单'
    if name == 'build_integrability_notebook.py':
        return '中文正文、LaTeX 与关键 Lean 单元的权威生成器'
    if name == 'MATHEMATICAL_REVIEW.md':
        return '条件、守恒、对易、Jacobian 见证与最终基础范围的审阅'
    if name == 'README.md':
        return '本次生成、运行、审阅与登记入口'
    if name == 'register_integrability_notebook.py':
        return '同专题记录合并及交付哈希登记'
    if name == 'registration.json':
        return '当前交付哈希与共享记录修改前后证据'
    if suffix == '.cjs':
        return '实际浏览器排版、公式与资源检查'
    if suffix == '.py':
        return '本专题构建、执行或核验脚本'
    if suffix == '.json':
        return '构建、数学、执行、视觉或登记核验结果'
    if suffix == '.txt':
        return '原始编译输出或源码摘要'
    if suffix == '.html':
        return 'notebook 正文的浏览器核验预览'
    return '本专题研究或核验材料'


def project_files() -> list[Path]:
    """Index materials and actual cell inputs; artifact identity is in manifests."""
    ignored = {'__pycache__', 'proof_cache', 'runtime_validation_library'}
    paths = []
    for path in HERE.rglob('*'):
        if not path.is_file() or ignored.intersection(path.relative_to(HERE).parts):
            continue
        if path.suffix in {'.olean', '.ilean', '.ir', '.server', '.private', '.pyc'}:
            continue
        if path.name in {'proposed_PROGRESS_LOG.md', 'proposed_FILE_INDEX.md', 'prepared_registration.json'}:
            continue
        if path.suffix.lower() in {'.py', '.cjs', '.js', '.css', '.md', '.html', '.json', '.ipynb', '.png', '.txt', '.lean'}:
            paths.append(path)
    return sorted(paths, key=lambda p: rel(p).lower())


def make_progress(text: str, notebook, execution: dict, nonlinear_revision: dict) -> str:
    code_count = sum(c.cell_type == 'code' for c in notebook.cells)
    total_count = len(notebook.cells)
    seconds = execution.get('elapsed_seconds', execution.get('seconds'))
    partial_seconds = execution['partial_revision_elapsed_seconds']
    intro = (
        '> **Notebook 展示（2026-10-07）：** '
        '[DLW刘维尔可积性report.ipynb](notebook/DLW刘维尔可积性report.ipynb) '
        '按周期格点与自由坐标、原物理方程、Cₙ/H₀/K/P、守恒、对易、有限 Fourier Jacobian 非零子式、'
        '开稠密独立集及最终定理组织，每个关键 Lean 结论配 LaTeX 对照。'
        f'{total_count} 原生单元／{code_count} 代码的首次完整本地执行为 {seconds} 秒；'
        '随后给守恒单元补入 K/P 的显式导数零目标，'
        f'仅将准备、库导入与该守恒单元在新内核局部复核 {partial_seconds} 秒，'
        '其余 14 代码单元的源码、执行计数与输出保持，保存真实编译输出；'
        '复用已核验的 105 模块库，每次只编译当前显示代码。'
        '最终定理仍显式使用 FactorSpectralFoundation，具体正规 PDO 表示、形式逆元及迹／Adler 基础范围与原证明报告一致。'
        '源码、原生执行、数学审阅、浏览器预览与交付哈希见 '
        '[Notebook 项目](Workspaces/integrability_notebook_20261007/README.md)；'
        '运行步骤见 [使用说明](report/notebook_usage.html)。\n\n'
    )
    start = '<!-- DLW_LEAN_PROGRESS_BEGIN -->\n'
    assert start in text and '<!-- DLW_LEAN_PROGRESS_END -->' in text
    if '> **Notebook 展示（2026-10-07）：**' not in text:
        text = text.replace(start, start + intro, 1)
    label = '> **2026-10-06（非线性化与2HS独立笔记本）：** '
    addition = (
        '**关键残差定义补充（2026-10-07）：** '
        '非线性化 notebook 的 lean-uw 单元完整展示 fluxUW、fluxOmega、reportN1、reportN2，'
        '与式（7）的两个左端逐项对应，并用 rfl 核对显示定义与原库定义相同。'
        '运行本地准备、UW 导入、起点与终点四个相关单元实际编译通过，'
        f'共 {nonlinear_revision["targeted_seconds"]} 秒，保存两残差定义和原公理输出；'
        '其余 13 个代码单元及执行计数、原始输出完整保留，未重算数值。'
        '权威生成器同步，修改前 notebook／生成器／执行证据与本次真实输出见 '
        '[nonlinear_revision](Workspaces/integrability_notebook_20261007/nonlinear_revision/README.md)。 '
        '**此前记录：** '
    )
    assert label in text
    if '**关键残差定义补充（2026-10-07）：**' not in text:
        text = text.replace(label, label + addition, 1)
    return text


def make_index(text: str, materials: list[Path], source_paths: list[Path]) -> str:
    rows = [
        INDEX_BEGIN,
        '**一般周期 DLW 刘维尔可积性的可执行 Notebook（2026-10-07）：**',
        '',
        link(DELIVERY, '条件与坐标、守恒量、守恒与对易、Jacobian 独立见证和带显式基础前提的最终定理'),
        link(NONLINEAR, '式（7）的 reportN1/reportN2 完整定义已补充并局部实跑'),
        link(USAGE, '四份 notebook 的 VS Code／Colab 使用方法'),
    ]
    for path in materials:
        rows.append(link(path, describe(path)))
    if REGISTRATION not in materials:
        rows.append(link(REGISTRATION, '当前交付哈希与共享记录修改前后证据'))
    rows.extend([
        '- `Workspaces/integrability_notebook_20261007/lean_runs/`（各次显示单元的真实编译输入、产物与 history；具体身份见执行及 runtime 证据）',
        '- `Workspaces/integrability_notebook_20261007/proof_cache/`（运行器接口的空兼容目录；当前直接复用原研究工程 .lean-runs 的完整编译库）',
        '- `Workspaces/integrability_notebook_20261007/runtime_validation_library/`（源码／产物变更核验用隔离副本；105 模块不与原库混用，检查记录见 runtime_validation.json）',
        '- `Workspaces/integrability_notebook_20261007/preview/assets/`（离线预览的本地公式排版资源）',
        link(ROOT / 'Workspaces/notebook_reports_20261006/build_nonlinear_notebook.py', '既有非线性化权威生成器，同步完整残差定义'),
        link(ROOT / 'Workspaces/notebook_reports_20261006/nonlinear_execution_validation.json', '保留原整本执行，另登记本次相关单元局部重跑'),
        link(ROOT / 'Workspaces/notebook_reports_20261006/verify_notebook_reports.py', '继续核验既有三份报告并允许新增 notebook'),
        '',
        'Notebook 直接引用的原研究报告与关键证明源：',
        '',
    ])
    rows.extend(link(path, '原证明报告或关键定义／定理源，原件保持') for path in source_paths)
    rows.extend(['', INDEX_END, ''])
    block = '\n'.join(rows)
    if INDEX_BEGIN in text:
        pattern = re.escape(INDEX_BEGIN) + r'.*?' + re.escape(INDEX_END)
        text = re.sub(pattern, lambda _: block.rstrip(), text, count=1, flags=re.S)
    else:
        anchor = '<!-- NOTEBOOK_LECTURES_INDEX_BEGIN -->'
        assert anchor in text
        text = text.replace(anchor, block + '\n' + anchor, 1)
    old = '与 [DLW数值分析](notebook/DLW数值分析report.ipynb)，运行步骤见'
    new = '、[DLW数值分析](notebook/DLW数值分析report.ipynb) 与 [DLW刘维尔可积性](notebook/DLW刘维尔可积性report.ipynb)，运行步骤见'
    if old in text:
        text = text.replace(old, new, 1)
    text = text.replace('[2HS数值分析](notebook/2HS数值分析report.ipynb) 、[DLW数值分析]',
                        '[2HS数值分析](notebook/2HS数值分析report.ipynb)、[DLW数值分析]', 1)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--register', action='store_true')
    parser.add_argument('--execution', type=Path, default=HERE / 'integrability_execution_validation.json')
    parser.add_argument('--content', type=Path, default=HERE / 'mathematical_content_validation.json')
    parser.add_argument('--visual', type=Path, default=HERE / 'browser_validation.json')
    args = parser.parse_args()
    execution = read_json(args.execution)
    content = read_json(args.content)
    visual = read_json(args.visual)
    assert passed(execution), 'Notebook execution must pass before registration.'
    assert passed(content), 'Content review must pass before registration.'
    assert passed(visual), 'Visual review must pass before registration.'
    assert DELIVERY.read_bytes() == MIRROR.read_bytes(), 'Root delivery and executed project mirror differ.'
    assert execution['notebook_sha256'] == sha(DELIVERY.read_bytes())
    notebook = nbformat.read(DELIVERY, 4)
    nbformat.validate(notebook)
    if content.get('notebook_sha256') != sha(DELIVERY.read_bytes()):
        reviewed_draft = HERE / 'latest_source_draft.ipynb'
        assert content['notebook_sha256'] == sha(reviewed_draft.read_bytes())
        draft = nbformat.read(reviewed_draft, 4)
        assert [(c.id, c.cell_type, c.source) for c in draft.cells] == [
            (c.id, c.cell_type, c.source) for c in notebook.cells
        ], 'Displayed content changed after mathematical review.'
    code = [c for c in notebook.cells if c.cell_type == 'code']
    assert all(c.execution_count is not None for c in code)
    assert not [o for c in code for o in c.outputs if o.output_type == 'error']
    assert not any('sorryAx' in o.get('text', '') for c in code for o in c.outputs)
    nonlinear_revision = read_json(HERE / 'nonlinear_revision/revision_validation.json')
    assert passed(nonlinear_revision)
    assert nonlinear_revision['after_sha256'] == sha(NONLINEAR.read_bytes())
    library = read_json(HERE / 'library_manifest.json')
    for source in library['sources'].values():
        assert sha(Path(source['path']).read_bytes()) == source['sha256']
    assert len(library['sources']) == 105
    source_paths = sorted({Path(path) for path in read_json(HERE / 'build_integrability_validation.json')['source_sha256']}, key=str)
    assert all(p.is_file() for p in source_paths)
    materials = project_files()
    progress_before = PROGRESS.read_bytes()
    index_before = INDEX.read_bytes()
    progress_text = make_progress(progress_before.decode('utf-8-sig').replace('\r\n', '\n'), notebook, execution, nonlinear_revision)
    index_text = make_index(index_before.decode('utf-8-sig').replace('\r\n', '\n'), materials, source_paths)
    if not args.register:
        (HERE / 'proposed_PROGRESS_LOG.md').write_text(progress_text, 'utf-8')
        (HERE / 'proposed_FILE_INDEX.md').write_text(index_text, 'utf-8')
        print(json.dumps({'prepared': True, 'root_records_modified': False,
                          'indexed_project_materials': len(materials)}, ensure_ascii=False))
        return

    # First registration starts from the backed-up shared records; later runs
    # replace only this task's marker/prefix and never rewrite old registries.
    if not REGISTRATION.exists():
        assert PROGRESS.read_bytes() == (BACKUPS / 'PROGRESS_LOG.md').read_bytes()
        assert INDEX.read_bytes() == (BACKUPS / 'FILE_INDEX.md').read_bytes()
    assert PROGRESS.read_bytes() == progress_before
    assert INDEX.read_bytes() == index_before
    PROGRESS.write_text(progress_text, 'utf-8')
    INDEX.write_text(index_text, 'utf-8')
    record_paths = [
        (PROGRESS, BACKUPS / 'PROGRESS_LOG.md'),
        (INDEX, BACKUPS / 'FILE_INDEX.md'),
        (USAGE, BACKUPS / 'notebook_usage.html'),
        (ROOT / 'Workspaces/notebook_reports_20261006/verify_notebook_reports.py', BACKUPS / 'verify_notebook_reports.py'),
    ]
    records = [{'path': str(path), 'before': str(backup),
                'before_sha256': sha(backup.read_bytes()), 'after_sha256': sha(path.read_bytes())}
               for path, backup in record_paths]
    current_paths = set(materials + source_paths + [DELIVERY, NONLINEAR, USAGE,
        ROOT / 'Workspaces/notebook_reports_20261006/build_nonlinear_notebook.py',
        ROOT / 'Workspaces/notebook_reports_20261006/nonlinear_execution_validation.json',
        ROOT / 'Workspaces/notebook_reports_20261006/verify_notebook_reports.py'])
    current_paths.discard(REGISTRATION)
    registration = {
        'date': '2026-10-07', 'success': True,
        'delivery': {'path': str(DELIVERY), 'sha256': sha(DELIVERY.read_bytes()),
                     'project_mirror': str(MIRROR), 'mirror_identical': True,
                     'cells': len(notebook.cells), 'code_cells': len(code),
                     'actual_outputs_saved': True},
        'scope': 'general periodic physical fields; each finite conserved commuting family generically independent; explicit FactorSpectralFoundation retained',
        'execution': {'path': str(args.execution), 'sha256': sha(args.execution.read_bytes()),
                      'initial_complete_execution_seconds': execution.get('elapsed_seconds', execution.get('seconds')),
                      'initial_complete_execution_evidence': execution['original_full_execution_validation'],
                      'later_partial_revision_seconds': execution['partial_revision_elapsed_seconds'],
                      'later_partial_revision_evidence': execution['partial_revision_execution_validation'],
                      'mode': 'initial complete execution plus later conservation-cell revision; no second full rerun'},
        'content_review': {'path': str(args.content), 'sha256': sha(args.content.read_bytes())},
        'visual_review': {'path': str(args.visual), 'sha256': sha(args.visual.read_bytes())},
        'library_manifest': {'path': str(HERE / 'library_manifest.json'),
                             'sha256': sha((HERE / 'library_manifest.json').read_bytes()), 'source_modules': 105},
        'nonlinear_definition_revision': nonlinear_revision,
        'records': records,
        'current_files': [{'path': str(path), 'exists': path.is_file(), 'sha256': sha(path.read_bytes())}
                          for path in sorted(current_paths, key=str)],
        'original_proof_sources_unchanged': True,
        'historical_registrations_unchanged': True,
    }
    REGISTRATION.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({'success': True, 'registration': str(REGISTRATION),
                      'delivery_sha256': registration['delivery']['sha256'],
                      'registered_files': len(registration['current_files'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
