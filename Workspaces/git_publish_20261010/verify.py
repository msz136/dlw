"""Validate the lightweight submission without rerunning research experiments."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '.deps'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')


def main():
    files = [f for f in git('diff', '--cached', '--name-only', '-z').split('\0') if f]
    assert [f for f in files if f.startswith('Paper/')] == ['Paper/LITERATURE.md']
    assert not any(Path(f).suffix.lower() in ('.png', '.jpg', '.pdf', '.npz', '.npy', '.html', '.ipynb') for f in files)
    counts = {'python': 0, 'json': 0, 'javascript': 0}
    node = Path('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
    for f in files:
        p = ROOT / f
        if p.suffix.lower() not in ('.py', '.pyw', '.json', '.cjs', '.md', '.txt'):
            continue
        text = p.read_text(encoding='utf-8-sig')
        assert not re.search(r'(?m)^(<<<<<<< |=======\s*$|>>>>>>> )', text), f
        assert not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----', text), f
        if p.suffix in ('.py', '.pyw'):
            ast.parse(text, filename=f)
            counts['python'] += 1
        elif p.suffix == '.json':
            json.loads(text)
            counts['json'] += 1
        elif p.suffix == '.cjs':
            subprocess.run([str(node), '--check', str(p)], check=True, capture_output=True)
            counts['javascript'] += 1
    import nbformat
    notebooks = list((ROOT / 'notebook').glob('*report.ipynb'))
    for p in notebooks:
        nbformat.validate(nbformat.read(p, as_version=4))
    # Confirm downloaded PDFs still match the original acquisition manifests.
    hashes = {}
    manifests = [
        ROOT / 'Paper/sources/literature_download_20261010.json',
        ROOT / 'Workspaces/dlw_structure_benchmarks/manifest.json',
    ]
    for manifest in manifests:
        for item in json.loads(manifest.read_text(encoding='utf-8')):
            if 'sha256' not in item:
                continue
            path = ROOT / item['file'] if 'file' in item else ROOT / 'Paper/sources' / item['filename']
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            assert actual == item['sha256'], path
            hashes[path.relative_to(ROOT).as_posix()] = actual
    catalogue = (ROOT / 'Paper/LITERATURE.md').read_text(encoding='utf-8')
    assert catalogue.count(' | PDF |') == 39
    assert catalogue.count('仅链接，尚无 PDF') == 2
    for f in git('ls-files', '--others', '--ignored', '--exclude-standard', 'Paper').splitlines():
        assert f != 'Paper/LITERATURE.md'
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
    evidence = {
        'date': '2026-10-10', 'base_commit': git('rev-parse', 'HEAD').strip(),
        'scope': 'lightweight sources, manuscripts, numerical summaries and literature catalogue',
        'staged_files': files, 'staged_worktree_bytes': sum((ROOT / f).stat().st_size for f in files),
        'syntax_checks': counts, 'local_notebooks_validated': [p.relative_to(ROOT).as_posix() for p in notebooks],
        'paper_staged': ['Paper/LITERATURE.md'], 'catalogue_pdfs': 39, 'catalogue_link_only': 2,
        'original_pdf_hashes_verified': hashes,
        'images_html_notebook_outputs': 'retained locally; excluded from this commit',
        'research_experiments_rerun': False, 'credentials_scan': 'no matching credential patterns',
    }
    (HERE / 'validation.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(files), 'bytes': evidence['staged_worktree_bytes'], 'checks': counts, 'original_pdfs': len(hashes)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
