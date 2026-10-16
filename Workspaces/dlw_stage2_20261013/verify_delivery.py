"""Check stage-2 saved certificates, report, and unchanged source inputs."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
import ast
import csv
import hashlib
import json
import re
from bs4 import BeautifulSoup
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = ROOT/'report/dlw_stage2_20261013.html'
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def data(path):
    return json.loads(path.read_text(encoding='utf-8'),
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})


source = REPORT.read_text(encoding='utf-8')
doc = BeautifulSoup(source, 'html.parser')
ids = Counter(t['id'] for t in doc.select('[id]'))
check('unique HTML ids', all(v == 1 for v in ids.values()))
check('strict mathematics rendered', not doc.select('.katex-error') and
      'MATHPLACEHOLDER' not in source, {'formula_count': len(doc.select('.katex'))})
tokens = ['REDUCTION_PROOF','SYMPLECTIC_PROOF','ERROR_LAX_PROOF','SYNTHESIS_PROOF',
          'SYMPLECTIC_TABLE','SYMPLECTIC_FIGURE','TOLERANCE_FIGURE']
check('all report sections embedded', not any(t in source for t in tokens))
missing = []
count = 0
for tag in doc.select('[href], [src]'):
    for attr in ('href','src'):
        if not tag.has_attr(attr):
            continue
        value = urlsplit(tag[attr])
        if value.scheme or value.netloc:
            continue
        count += 1
        path = (REPORT.parent/unquote(value.path)).resolve() if value.path else REPORT
        if not path.exists():
            missing.append(tag[attr])
        elif value.fragment and path.suffix == '.html':
            other = doc if path == REPORT else BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            if not other.find(id=unquote(value.fragment)):
                missing.append(tag[attr])
check('local links and anchors', not missing, {'count': count, 'missing': missing})
widths = [[sum(int(c.get('colspan',1)) for c in tr.find_all(['th','td'],recursive=False))
           for tr in table.find_all('tr')] for table in doc.select('table')]
check('table column consistency', all(len(set(w)) == 1 for w in widths), {'tables':len(widths)})
css = ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css'
fonts = re.findall(r'url\(([^)]+)\)',css.read_text(encoding='utf-8'))
check('offline math fonts', all((css.parent/f.strip('"\'')).is_file() for f in fonts))
bad_controls = []
for path in HERE.rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    if any(ord(c)<32 and c not in '\n\r\t' for c in text):
        bad_controls.append(path.name)
check('no illegal Markdown control characters', not bad_controls, bad_controls)
for path in HERE.rglob('*.py'):
    ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
check('all project Python syntax', True)

baseline=data(HERE/'baseline.json')
changes = [str(p) for p,h in baseline.items() if sha(ROOT/p) != h]
check('source notebook, paper, and stage-1 files unchanged', not changes, changes)
red=data(HERE/'reduction/verification.json')
check('2A exact symbolic certificates', red['symbolic']['passed'])
check('2A original equations on five actual elliptic waves', len(red['numerical']) == 5 and
      max(max(r['original_eq1_linf'],r['original_eq2_linf']) for r in red['numerical']) < 2e-10)
check('2A independent momentum and original symplectic pairing',
      max(abs(r['omega_minus_momentum_derivative']) for r in red['numerical']) < 1e-9 and
      all(r['P_derivative_m']<0 and r['min_abs_w']>0 for r in red['numerical']))
sym=data(HERE/'symplectic/validation.json')
check('2B all numeric validations', sym['passed'] and len(sym['checks']) == 40 and
      all(r['passed'] for r in sym['checks']), {'checks':len(sym['checks'])})
check('2B validated source hashes',
      sym['sources']['script_sha256'] == sha(HERE/'symplectic/symplectic_experiment.py') and
      sym['sources']['stage1_sha256'] == sha(Path(sym['sources']['stage1_code'])))
lax=data(HERE/'error_lax/exact_checks.json')
check('2C exact checks and script hash', lax['passed'] and lax['check_count'] == 38 and
      lax['checked_scalar_entries'] == 158 and
      lax['script_sha256'] == sha(HERE/'error_lax/verify_error_lax.py'),
      {'checks':lax['check_count'],'scalar_entries':lax['checked_scalar_entries']})
check('independent synthesis identities', data(HERE/'synthesis_validation.json')['passed'])
images = list((HERE/'symplectic').glob('*.png'))
for path in images:
    with Image.open(path) as im:
        im.verify()
check('two PNG/PDF figure pairs', len(images) == 2 and all(p.with_suffix('.pdf').is_file() for p in images))
with (HERE/'symplectic/fixed_time.csv').open(encoding='utf-8-sig',newline='') as stream:
    reference_rows=[r for r in csv.DictReader(stream) if int(r['steps']) == 8]
check('main numerical table values', len(reference_rows) == 3 and all(
    f'{float(r[key]):.5e}' in source for r in reference_rows
    for key in ('symplectic_defect','physical_field_error_vs_DOP853_linf')))
result = {'passed':all(r['passed'] for r in checks),'checks':checks,
          'report_sha256':sha(REPORT),'report_bytes':REPORT.stat().st_size,
          'visual_review':['symplectic_defect.png','midpoint_solver_tolerance.png'],
          'scope':'Saved-certificate and document checks; images visually reviewed; no browser-layout claim.'}
(HERE/'delivery_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'checks':len(checks),
                  'failures':[c for c in checks if not c['passed']]},ensure_ascii=False))
raise SystemExit(0 if result['passed'] else 1)
