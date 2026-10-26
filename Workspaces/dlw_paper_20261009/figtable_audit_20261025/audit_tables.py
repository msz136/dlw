"""Independent read-only audit: saved arrays/records -> CSV -> HTML.

No solver, reference evaluator or project validation script is imported/run.
"""
from pathlib import Path
import csv, hashlib, json, re
import numpy as np
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
P=HERE.parent
R=P/'report_refresh_20261024'
F=R/'natural_selection_20261025/figures/data'
N=R/'natural_selection_20261025'
CASES=['A','D','Gaussian','Sinusoidal']
NAMES=['One-soliton','Two-soliton','Gaussian','Sinusoidal']
METHODS={'endpoint':'Endpoint-SD','centered':'Centered-SD','fd':'FD'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
paper=ROOT/'dlw-paper.html'
doc=BeautifulSoup(paper.read_text(encoding='utf-8'),'html.parser')
checks=[]; arraychecks=[]; artifactchecks=[]; metachecks=[]
all_records={}
for stage,tid,csvfile,keys,mkey in [
 ('rate','table-initial','table1_initial_derivative_errors.csv',['error_ut','error_vt'],'method'),
 ('final','table-final','table2_final_field_errors.csv',['error_u','error_v'],'space')]:
 rows=list(csv.DictReader((R/csvfile).open(encoding='utf-8-sig',newline='')))
 assert len(rows)==12
 table=doc.find(id=tid)
 assert [t.get_text(strip=True) for t in table.select('thead tr:first-child th[colspan]')]==list(METHODS.values())
 assert [r.th.get_text(strip=True) for r in table.select('tbody tr')]==NAMES
 all_records[stage]=rows
 for case,tr in zip(CASES,table.select('tbody tr')):
  values=[[float(next(r for r in rows if r['case']==case and r[mkey]==method)[key]) for key in keys] for method in METHODS.values()]
  minima=np.min(values,axis=0)
  for j,td in enumerate(tr.find_all('td')):
   pfx=list(METHODS)[j//2];method=METHODS[pfx];q='uv'[j%2];value=values[j//2][j%2]
   raw=float(td['data-value']);visible=re.sub(r'\s+','',td.get_text()).replace('×','e').replace('10','',1)
   mantissa,exp=f'{value:.3e}'.split('e')
   value_match=raw==value
   visible_match=td.sup.get_text()==str(int(exp)) and mantissa in td.get_text()
   bold_match=bool(bool(td.strong)==(value==minima[j%2]))
   assert value_match and visible_match and bold_match,(stage,case,method,q)
   row=next(r for r in rows if r['case']==case and r[mkey]==method)
   source_path=(N/('initial_results.json' if stage=='rate' else 'results.json')) if pfx=='centered' else ((P/'spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024/baselines.json') if stage=='rate' and case in ['A','D'] else (R/('rk4_spatial/results.json' if case in ['A','D'] else 'nondegenerate_rk4_20261024/'+('initial_results.json' if stage=='rate' else 'results.json'))))
   records=read(source_path)
   rec=next(r for r in records if r['case']==case and r['method']==method and r['h']==r['dx']==.1)
   rec_value=rec['total' if stage=='rate' else 'error'][j%2]
   assert value==rec_value
   data=np.load(F/f'{case}.npz')
   err=data[f'{pfx}_error_{stage}_{q}']
   num=data[f'{pfx}_{stage}_{q}'];ref=data[f'{pfx}_ref_{stage}_{q}']
   identity=np.array_equal(err,num-ref)
   saved_max=float(np.max(abs(err)))
   assert identity and saved_max<=value+1e-12,(stage,case,method,q,saved_max,value)
   checks.append(dict(stage=stage,case=case,method=method,field=q,value=value,record=rel(source_path),html_raw_exact=value_match,html_4_significant_digits=visible_match,bold_correct=bold_match,bold=bool(td.strong),prepared_native_max=saved_max,prepared_max_minus_full_table=saved_max-value,error_array_equals_num_minus_ref=identity))
   if j%2==0:
    assert float(row['h'])==float(row['dx'])==.1
    if stage=='final':
     assert row['integrator']==rec['integrator']=='RK4' and float(row['dt'])==rec['dt']==1e-4 and float(row['T'])==rec['T']==rec['reached']==.01 and rec['status']=='complete'
    else:assert float(row['t'])==rec.get('t',0)==0
    metachecks.append(dict(stage=stage,case=case,method=method,parameters_consistent=True))
   # Full trajectory comparison needs no reference re-evaluation.
   if stage=='final':
    art=ROOT/rec['artifact'];rawdata=np.load(art)
    hash_ok=sha(art)==rec['artifact_sha256'];assert hash_ok
    xs=data['x'];ys=data[f'{pfx}_y_{q}'];rawys=rawdata['y' if q=='u' else 'yv']
    ix=np.array([np.flatnonzero(abs(rawdata['x']-v)<1e-10)[0] for v in xs]);iy=np.array([np.flatnonzero(abs(rawys-v)<1e-10)[0] for v in ys])
    crop=rawdata[q][np.ix_(iy,ix)]
    crop_exact=np.array_equal(crop,num);assert crop_exact
    ref_exact=None
    if q+'_ref' in rawdata.files:
     ref_exact=np.array_equal(rawdata[q+'_ref'][np.ix_(iy,ix)],ref);assert ref_exact
     full_error=abs(rawdata[q]-rawdata[q+'_ref'])
     full_max=float(np.max(full_error[abs(rawys)<=1.8+1e-12]))
     assert full_max==value
     arraychecks.append(dict(stage=stage,case=case,method=method,field=q,artifact=rel(art),full_saved_array_max_equals_table=True,full_saved_array_max=full_max))
    artifactchecks.append(dict(case=case,method=method,field=q,artifact=rel(art),artifact_hash_matches_record=hash_ok,prepared_field_is_exact_native_subset=crop_exact,prepared_reference_is_exact_saved_subset=ref_exact))
   if stage=='rate' and (pfx=='centered' or case not in ['A','D']):
    art=N/f'initial_{case}.npz' if pfx=='centered' else R/'nondegenerate_rk4_20261024'/f'initial_{case}_{method}.npz'
    rawdata=np.load(art);rawys=rawdata['y' if q=='u' else 'yv']
    xs=data['x'];ys=data[f'{pfx}_y_{q}']
    ix=np.array([np.flatnonzero(abs(rawdata['x']-v)<1e-10)[0] for v in xs]);iy=np.array([np.flatnonzero(abs(rawys-v)<1e-10)[0] for v in ys])
    assert np.array_equal(rawdata[q+'t'][np.ix_(iy,ix)],num)
    assert np.array_equal(rawdata[q+'t_ref'][np.ix_(iy,ix)],ref)
    max_full=float(np.max(abs(rawdata[q+'t']-rawdata[q+'t_ref'])[abs(rawys)<({'A':5,'D':30}.get(case,1.8)+ (0 if case in ['A','D'] else 1e-12))][:,abs(rawdata['x'])<=({'A':5,'D':30}.get(case,96))]))
    assert max_full==value
    arraychecks.append(dict(stage=stage,case=case,method=method,field=q,artifact=rel(art),prepared_values_and_references_exact_native_subsets=True,full_saved_array_max_equals_table=True))

ratios={}
for case in CASES:
 rows=all_records['final'];v={r['space']:[float(r['error_u']),float(r['error_v'])] for r in rows if r['case']==case}
 ratios[case]=dict(endpoint_over_centered=[a/b for a,b in zip(v['Endpoint-SD'],v['Centered-SD'])],fd_over_centered=[a/b for a,b in zip(v['FD'],v['Centered-SD'])])
parameters=doc.find(id='table-parameters')
paramrows=[[re.sub(r'\s+','',e.get_text()).replace('−','-') for e in r.find_all(['th','td'])] for r in parameters.select('tbody tr')]
assert paramrows==[['One-soliton','(1,2)','R=5','[-10,10)'],['Two-soliton','(1,2),(4,-3)','R=30','[-40,40)']]
result=dict(status='passed',scope='Saved-record and saved-array audit only; no numerical experiment or continuous reference recalculated.',paper_sha256=sha(paper),table_values=len(checks),bold_minima=sum(r['bold'] for r in checks),error_entries=checks,full_saved_array_checks=arraychecks,terminal_native_subsets=artifactchecks,metadata_checks=metachecks,parameter_table=paramrows,prose_ratios=ratios,empty_later_sections=[sec for sec in ['section-5.3','section-5.4','section-5.5'] if len(doc.find(id=sec).find_all(['p','table','figure']))==0])
(HERE/'table_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],table_values=result['table_values'],bold_minima=result['bold_minima'],native_final_subsets=len(artifactchecks),full_saved_array_checks=len(arraychecks),ratios=ratios),ensure_ascii=False,indent=2))
