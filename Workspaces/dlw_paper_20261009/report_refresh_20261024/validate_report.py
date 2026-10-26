from pathlib import Path
import csv
import hashlib
import json
from urllib.parse import unquote
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RUN=ROOT/'Workspaces/dlw_paper_20261009/spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024'
def read(path): return json.loads(path.read_text(encoding='utf8'))
doc=(ROOT/'Report.html').read_text(encoding='utf8')
s=BeautifulSoup(doc,'html.parser')
ids=[el['id'] for el in s.select('[id]')]
assert len(ids)==len(set(ids))
assert 'MATHSLOT' not in doc and 'katex-error' not in doc
assert len(s.find_all('table'))==2
missing=[]
for element in s.select('a[href],link[href]'):
    target=element['href']
    if target.startswith('#'):
        assert target[1:] in ids
    elif not (ROOT/unquote(target.split('#')[0])).exists(): missing.append(target)
assert not missing,missing
SELECTED=HERE/'natural_selection_20261025'
NEW=HERE/'nondegenerate_rk4_20261024'
CASES=['A','D','Gaussian','Sinusoidal']
LABELS={'A':'One-soliton','D':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
METHODS=['Endpoint-SD','Centered-SD','FD']
BASELINE_METHODS={'Endpoint-SD','FD'}
spatial=[r for r in read(RUN/'baselines.json') if r['dx']==r['h']==.1 and r['method'] in BASELINE_METHODS]
spatial += [r for r in read(NEW/'initial_results.json') if r['method'] in BASELINE_METHODS]
spatial += read(SELECTED/'initial_results.json')
temporal=[r for r in read(HERE/'rk4_spatial/results.json') if r['method'] in BASELINE_METHODS]
temporal += [r for r in read(NEW/'results.json') if r['method'] in BASELINE_METHODS]
temporal += read(SELECTED/'results.json')
spatial=[r for r in spatial if r['case'] in CASES]
temporal=[r for r in temporal if r['case'] in CASES]
assert len(spatial)==len(temporal)==12
assert all(r['integrator']=='RK4' and r['dt']==1e-4 and r['T']==r['reached']==.01 and r['h']==r['dx']==.1 and r['status']=='complete' for r in temporal)
checked=0;bold=0
for table_id,records,key in [('table-initial',spatial,'total'),('table-final',temporal,'error')]:
    rows=s.find(id=table_id).select('tbody tr')
    assert len(rows)==len(CASES)
    assert [h.get_text() for h in s.find(id=table_id).select('thead tr:first-child th[colspan]')]==METHODS
    for tr,case in zip(rows,CASES):
        assert tr.th.contents[0].strip()==LABELS[case]
        values=[next(r[key] for r in records if r['case']==case and r['method']==method) for method in METHODS]
        cells=tr.find_all('td');assert len(cells)==6
        minima=[min(v[j] for v in values) for j in (0,1)]
        for i,cell in enumerate(cells):
            value=values[i//2][i%2]
            assert float(cell['data-value'])==value
            expected_m,expected_e=f'{value:.3e}'.split('e')
            assert expected_m in cell.get_text() and cell.sup.get_text()==str(int(expected_e))
            best=f'{value:.3e}'==f'{minima[i%2]:.3e}'
            assert bool(cell.strong)==best
            checked+=1;bold+=best
for name,key in [('table1_initial_derivative_errors.csv','method'),('table2_final_field_errors.csv','space')]:
    with (HERE/name).open(encoding='utf-8-sig',newline='') as f: records=list(csv.DictReader(f))
    assert len(records)==12 and {r[key] for r in records}==set(METHODS)
    assert [(r['case'],r[key]) for r in records]==[(c,m) for c in CASES for m in METHODS]
    if key=='space':assert {r['integrator'] for r in records}=={'RK4'}
assert 'CSD0' not in s.get_text() and '完整势' not in s.get_text()
assert '六个算例' not in s.get_text() and '四个孤子' not in s.get_text()
assert 'A、B、C、D' not in s.get_text()
old=BeautifulSoup((SELECTED/'before_update/Report.html').read_text(encoding='utf8'),'html.parser')
for table_id,mapping in [('table-initial',[(0,0),(3,2)]),('table-final',[(0,0),(2,1),(4,2)])]:
    old_rows=old.find(id=table_id).select('tbody tr')
    old_case_order=list('ABCD')+['Gaussian','Sinusoidal']
    for case,new_row in zip(CASES,s.find(id=table_id).select('tbody tr')):
        old_row=old_rows[old_case_order.index(case)]
        old_cells=old_row.find_all('td');new_cells=new_row.find_all('td')
        for om,nm in mapping:
            for j in (0,1):assert old_cells[2*om+j]['data-value']==new_cells[2*nm+j]['data-value']
selected_audit=read(SELECTED/'validation.json')
assert selected_audit['records']==selected_audit['complete']==6
assert selected_audit['max_record_difference']==0
assert selected_audit['max_initial_rate_identity_difference']<1e-10
assert selected_audit['non_soliton_initial_and_final_references_bitwise_identical_to_certified_arrays']
assert selected_audit['non_soliton_reference_bound']==1e-13
for record in read(SELECTED/'initial_results.json'):
    assert hashlib.sha256((ROOT/record['artifact']).read_bytes()).hexdigest()==record['artifact_sha256']
    assert hashlib.sha256((ROOT/record['source_artifact']).read_bytes()).hexdigest()==record['source_artifact_sha256']
for record in read(SELECTED/'results.json'):
    assert hashlib.sha256((ROOT/record['artifact']).read_bytes()).hexdigest()==record['artifact_sha256']
    for source in record['sources']:
        assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'],source['path']
p=read(SELECTED/'report_preservation.json')
assert hashlib.sha256((ROOT/'dlw-paper.html').read_bytes()).hexdigest()==p['paper_sha256']
assert hashlib.sha256((ROOT/p['report_backup']).read_bytes()).hexdigest()==p['report_before_sha256']
original=read(HERE/'preservation.json')
assert hashlib.sha256((ROOT/original['report_backup']).read_bytes()).hexdigest()==original['report_before_sha256']
certificate=read(NEW/'reference_certificate.json')
assert certificate['status']=='verified_all_stored_sample_values'
assert 0<certificate['uniform_bound_each']<1e-9
for field in ('u','v','ut','vt'):
    assert certificate['initial'][field]<=certificate['uniform_bound_each']
for field in ('u','v'):
    assert certificate['final'][field]<=certificate['uniform_bound_each']
assert certificate['nominal_final_time']=='1/100'
assert hashlib.sha256((NEW/'reference_grid.py').read_bytes()).hexdigest()==certificate['reference_source_sha256']
assert hashlib.sha256((NEW/'certify_reference_grid.py').read_bytes()).hexdigest()==certificate['certificate_source_sha256']
assert {c['case'] for c in certificate['cases']}=={'Gaussian','Sinusoidal'}
for case in certificate['cases']:
    assert case['status']=='verified_all_stored_final_sample_values'
    assert max(case['max_certified_enclosures'].values())<certificate['uniform_bound_each']
    for path,sha in case['files'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
for case in certificate['initial_certificate']['cases']:
    for source in case['sources']:
        assert hashlib.sha256((NEW/source['path']).read_bytes()).hexdigest()==source['sha256']
result=dict(tables=2,displayed_numbers_checked=checked,bold_minima_checked=bold,
    csv_records_checked=24,formula_count=len(s.select('annotation[encoding="application/x-tex"]')),
    links_valid=True,old_report_backup_verified=True,main_paper_unchanged_during_task=True,
    manuscript_baseline=p['paper_state'],
    table2_integrator='RK4',spatial_methods=METHODS,
    existing_endpoint_fd_values_and_natural_final_values_unchanged=True,
    initial_and_final_cases=CASES,
    non_soliton_initial_family='u0=A sin(pi(y+2)/4)F(x), v0=4-3u0_y',
    non_soliton_reference_uniform_bound=certificate['uniform_bound_each'],
    selected_centered_definition='Section3.2: v=Delta_h Z=Delta_h u+2(omega_k+omega_(k-1))/h',
    selected_centered_source_and_artifact_hashes_verified=True,
    visual_inspection=False,visual_inspection_reason='Static mathematical, structural and data validation')
(HERE/'report_validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
