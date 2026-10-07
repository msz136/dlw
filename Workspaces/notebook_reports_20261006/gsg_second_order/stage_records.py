"""Stage only this revision's additions to shared records."""
from pathlib import Path
import difflib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
snippets = json.loads((HERE/'record_snippets.json').read_text('utf-8'))
patches = []
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    before = subprocess.run(['git','show','HEAD:'+name], cwd=ROOT,
        check=True, capture_output=True).stdout.decode('utf-8')
    if name == 'PROGRESS_LOG.md':
        marker = '**静态报告精简（2026-10-07）：** '
        assert marker in before
        after = before.replace(marker, snippets['progress_note']+marker,1)
    else:
        after = before.rstrip()+'\n\n'+snippets['index_block']+'\n'
    patches.append(''.join(difflib.unified_diff(before.splitlines(keepends=True),
        after.splitlines(keepends=True), fromfile='a/'+name, tofile='b/'+name)))
patch = HERE/'records_staging.patch'
patch.write_text(''.join(patches), encoding='utf-8', newline='\n')
for args in (['git','apply','--cached','--check',str(patch)],
             ['git','apply','--cached',str(patch)]):
    subprocess.run(args, cwd=ROOT, check=True)
print('Staged the GSG revision only in PROGRESS_LOG.md and FILE_INDEX.md.')
