"""Register the completed direct-tau experiment in the existing DLW topic."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = ROOT/'report/dlw_direct_tau.html'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    validation = json.loads((HERE/'validation.json').read_text(encoding='utf-8'))
    browser = json.loads((HERE/'browser_validation.json').read_text(encoding='utf-8'))
    rows = json.loads((HERE/'out/results.json').read_text(encoding='utf-8'))
    assert validation['success'] and browser['success'] and len(rows)==12
    assert all(r['completed'] and not r['reason'] for r in rows)
    assert validation['source_sha256'] == sha(HERE/'direct_tau.py')
    manifest_path = HERE/'manifest.json'
    files = [p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
             and 'before_registration' not in p.parts and p != manifest_path]
    manifest = dict(date='2026-10-07', success=True, report=str(REPORT),
        method='Original-tau implicit midpoint, alternating linear F_j/G_{j+1} solves',
        all_runs_completed=12, final_time=.01,
        scope='Fixed uniform x, given lower G and analytic nonperiodic x strips; finite-h Gram reference',
        files={p.relative_to(ROOT).as_posix():sha(p) for p in [*files, REPORT]})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    backup = HERE/'before_registration'
    backup.mkdir(exist_ok=True)
    progress_path, index_path = ROOT/'PROGRESS_LOG.md', ROOT/'FILE_INDEX.md'
    for path in (progress_path, index_path):
        target = backup/path.name
        if not target.exists():
            shutil.copy2(path, target)
    # Only edit the existing line; do not display the long progress history.
    progress = progress_path.read_bytes().decode('utf-8')
    pattern = re.compile(r'(^> \*\*\d{4}-\d{2}-\d{2}（DLW数值分析笔记本）：\*\* )([^\r\n]*)', re.MULTILINE)
    matches = list(pattern.finditer(progress))
    assert len(matches)==1, 'Expected the existing DLW numerical notebook topic'
    match = matches[0]
    history = re.sub(r'^\*\*2026-10-07直接τ：\*\* .*? \*\*既有记录：\*\* ', '', match.group(2))
    note = ('**2026-10-07直接τ：** 原始双线性中点沿 $G_j^{n+1}$ → $F_j^{n+1}$ → '
        '$G_{j+1}^{n+1}$ 逐层两次线性求解，A/B/C共12组完整运行至T=0.01，'
        '时间阶约2，256→512份双场误差均降低；独立原始B残差最大1.27e-10。'
        '下侧G与非周期x解析条带闭合，使用有限h Gram参照，区别于原lower-u实验。'
        '[推导与结果](report/dlw_direct_tau.html)，实现和证据见 '
        '`Workspaces/dlw_direct_tau_20261007/`。 **既有记录：** ')
    updated = match.group(1)+note+history
    progress = progress[:match.start()]+updated+progress[match.end():]
    progress_path.write_bytes(progress.encode('utf-8'))

    index = index_path.read_bytes().decode('utf-8')
    newline = '\r\n' if '\r\n' in index else '\n'
    begin, end = '<!-- DLW_DIRECT_TAU_INDEX_BEGIN -->', '<!-- DLW_DIRECT_TAU_INDEX_END -->'
    indexed = sorted(set([*files, REPORT, manifest_path, *backup.glob('*')]), key=lambda p:p.relative_to(ROOT).as_posix())
    lines = [begin, '', '**DLW 直接双线性 τ 数值推进（2026-10-07）：**', '']
    for path in indexed:
        relative = path.relative_to(ROOT).as_posix()
        lines.append('- ['+relative+']('+relative+')')
    lines += ['', end]
    section = newline.join(lines)
    if begin in index:
        index = re.sub(re.escape(begin)+r'.*?'+re.escape(end), lambda _:section, index, flags=re.DOTALL)
    else:
        anchor = '<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->'
        if anchor in index:
            index = index.replace(anchor, section+newline+newline+anchor, 1)
        else:
            index += newline+newline+section+newline
    index_path.write_bytes(index.encode('utf-8'))
    print(json.dumps(dict(success=True, completed_runs=12, report=str(REPORT), indexed_files=len(indexed)), ensure_ascii=False))

if __name__ == '__main__':
    main()
