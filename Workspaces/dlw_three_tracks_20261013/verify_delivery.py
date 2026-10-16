"""Validate saved scientific artifacts and report links without rerunning solvers."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
import ast
import csv
import hashlib
import json
import re
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = ROOT / 'report/dlw_three_tracks_20261013.html'
checks = []


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


source = REPORT.read_text(encoding='utf-8')
doc = BeautifulSoup(source, 'html.parser')
ids = Counter(tag['id'] for tag in doc.select('[id]'))
check('unique HTML ids', all(v == 1 for v in ids.values()))
check('strict rendered mathematics', not doc.select('.katex-error') and
      'MATHPLACEHOLDER' not in source and len(doc.select('.katex')) > 250,
      {'formula_count': len(doc.select('.katex'))})
missing = []
local_count = 0
for tag in doc.select('[href], [src]'):
    for attr in ('href', 'src'):
        if not tag.has_attr(attr):
            continue
        value = urlsplit(tag[attr])
        if value.scheme or value.netloc:
            continue
        local_count += 1
        path = (REPORT.parent / unquote(value.path)).resolve() if value.path else REPORT
        if not path.exists():
            missing.append(tag[attr])
        elif value.fragment and path.suffix == '.html':
            target = doc if path == REPORT else BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            if not target.find(id=unquote(value.fragment)):
                missing.append(tag[attr])
check('all local report links and anchors exist', not missing,
      {'count': local_count, 'missing': missing})
table_widths = []
for table in doc.select('table'):
    widths = [sum(int(cell.get('colspan', 1)) for cell in row.find_all(['th', 'td'], recursive=False))
              for row in table.find_all('tr')]
    table_widths.append(widths)
check('consistent table column counts', all(len(set(v)) == 1 for v in table_widths),
      {'tables': len(table_widths)})
css = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css'
font_files = re.findall(r'url\(([^)]+)\)', css.read_text(encoding='utf-8'))
check('local math fonts exist', all((css.parent / item.strip('"\'')).exists() for item in font_files))

bundle = read_json(HERE / 'shared/solver_cells.json')
notebook = Path(bundle['notebook'])
check('source notebook matches frozen input', sha(notebook) == bundle['notebook_sha256'],
      {'sha256': sha(notebook)})
receipts = []
for receipt in sorted((HERE / 'shared').glob('*RK4*.json')):
    meta = read_json(receipt)
    label = meta['label']
    passed = (sha(receipt.with_suffix('.npz')) == meta['npz_sha256'] and
              sha(HERE / 'shared/solver_cells.json') == meta['solver_cells_sha256'] and
              meta['notebook_sha256'] == bundle['notebook_sha256'])
    entry = {'label': label, 'hashes_match': passed}
    if 'halfdt' not in label:
        archived = ROOT / 'Workspaces/dlw_paper_20261009/buffered_run' / f'{label}_fixed_state.npz'
        with np.load(HERE / 'shared' / f'{label}_endpoints.npz') as new, np.load(archived) as old:
            delta = float(np.max(abs(new['final'] - old['state'][:-len(new['x'])])))
        entry['archived_endpoint_max_difference'] = delta
        passed = passed and delta == 0.0
    check(f'trajectory input integrity: {label}', passed, entry)
    receipts.append(entry)
check('six shared trajectory receipts', len(receipts) == 6)

con = read_json(HERE / 'conservation/validation.json')
check('1A saved validation', con['passed'])
central = [r for r in con['summary'] if r['run'].startswith('centered')]
check('1A central defect integral agreement',
      max(abs(r[f'I{n}_drift_minus_integrated_defect']) for r in central for n in (1, 2, 3)) < 7.5e-13)
check('1A exact I1/K/P identity along trajectories',
      max(r['I1_K_Pmom_identity_max_residual'] for r in con['summary']) < 7e-15)
poi = read_json(HERE / 'poisson/exact_checks.json')
check('1C exact checks and source hash', poi['passed'] and poi['check_count'] == 66 and
      poi['jacobi_total_triples'] == 1596 and all(r['passed'] for r in poi['checks']) and
      poi['script_sha256'] == sha(HERE / 'poisson/verify_poisson.py'))
spec = read_json(HERE / 'spectrum/out/manifest.json')
check('1B source and all input hashes',
      spec['script_sha256'] == sha(HERE / 'spectrum/analyze_error_fields.py') and
      all(sha(Path(r['file'])) == r['sha256'] for r in spec['inputs']))
cal = spec['transform_calibration']
check('1B transform calibrations', cal['nyquist_mode_included'] and
      abs(cal['known_mode_kx'] - cal['recovered_mode_kx']) < 1e-12 and
      abs(cal['known_mode_ky'] - cal['recovered_mode_ky']) < 1e-12 and
      cal['morlet_relative_scale_error'] < .02, cal)
parseval = max(c['max_parseval_relative_residual'] for r in spec['inputs'] for c in r['checks'])
check('1B Hann Parseval', parseval < 2e-15, {'max_relative_residual': parseval})
with (HERE / 'spectrum/out/spectral_metrics.csv').open(encoding='utf-8', newline='') as stream:
    fields = list(csv.DictReader(stream))
check('1B all 252 field frames recorded', len(fields) == 252)
pywt_path = Path(spec['packages']['pywt_import_path']).resolve()
check('isolated PyWavelets import', pywt_path.is_file() and pywt_path.is_relative_to(HERE / 'spectrum/vendor'))

gif_info = []
for path in sorted((HERE / 'spectrum/out').glob('*.gif')):
    with Image.open(path) as im:
        frames = im.n_frames
        for frame in (0, frames // 2, frames - 1):
            im.seek(frame)
            im.convert('RGB').load()
        gif_info.append({'file': path.name, 'frames': frames, 'size': list(im.size)})
check('four readable animations with 21 frames', len(gif_info) == 4 and
      all(r['frames'] == 21 for r in gif_info), gif_info)
for folder in ('conservation', 'spectrum/out'):
    images = [p for p in (HERE / folder).glob('*.png') if '_animation_frame' not in p.stem]
    for path in images:
        with Image.open(path) as im:
            im.verify()
    check(f'{folder} PNG and PDF pairs', len(images) > 0 and all(p.with_suffix('.pdf').is_file() for p in images),
          {'png_count': len(images)})
scripts = [p for p in HERE.rglob('*.py') if 'vendor' not in p.parts]
for path in scripts:
    ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
check('project Python syntax', True, {'script_count': len(scripts)})

result = {'passed': all(c['passed'] for c in checks), 'checks': checks,
          'report_sha256': sha(REPORT), 'report_bytes': REPORT.stat().st_size,
          'scope': 'Artifact integrity and saved scientific certificates; no PDE rerun or browser layout check.'}
(HERE / 'delivery_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'passed': result['passed'], 'checks': len(checks),
                  'failures': [c for c in checks if not c['passed']]}, ensure_ascii=False))
raise SystemExit(0 if result['passed'] else 1)
