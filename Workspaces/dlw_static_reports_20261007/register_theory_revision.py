"""Register this theory-only revision without replacing the initial delivery record."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEST = HERE / 'theory_revision.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if DEST.exists():
        record = json.loads(DEST.read_text('utf-8'))
        for item in record['files']:
            assert sha(ROOT / item['path']) == item['sha256'], item['path']
        print(json.dumps({'success': True, 'mode': 'verify', 'files': len(record['files'])}))
        return
    checks = [json.loads((HERE / name).read_text('utf-8')) for name in
              ['build_validation.json', 'content_validation.json', 'browser_validation.json']]
    assert all(result['success'] for result in checks)
    assert checks[0]['delivery_sha256'] == checks[1]['integrability_sha256'] == sha(ROOT / 'dlw_integrability.html')
    historical = json.loads((HERE / 'registration.json').read_text('utf-8'))
    for item in historical['files']:
        if item['path'].endswith('.ipynb') or item['path'] == 'dlw_numerical.html':
            assert sha(ROOT / item['path']) == item['sha256'], item['path']
    assert sha(HERE / 'registration.json') == sha(HERE / 'before_theory/registration.json')
    paths = [ROOT / name for name in ['dlw_integrability.html', 'dlw_numerical.html', 'PROGRESS_LOG.md', 'FILE_INDEX.md']]
    paths += sorted((ROOT / 'notebook').glob('*.ipynb'))
    paths += sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p != DEST)
    shared = ROOT / 'Workspaces/dlw_notebook_static_20261007'
    paths += [shared / name for name in ['build_static.py', 'render_math.cjs']]
    record = {'success': True, 'date': '2026-10-07', 'revision': 'theory-only',
              'notebooks_unchanged': True, 'numerical_html_unchanged': True,
              'all_displayed_equations_unchanged': True, 'numbered_equations': list(range(1, 20)),
              'intermediate_code_and_outputs_removed': True, 'appendix_removed': True,
              'final_theorem_lines': 4, 'backup': 'Workspaces/dlw_static_reports_20261007/before_theory',
              'initial_registration_preserved': True,
              'files': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)} for p in paths]}
    DEST.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'success': True, 'mode': 'register', 'files': len(paths)}))


if __name__ == '__main__':
    main()
