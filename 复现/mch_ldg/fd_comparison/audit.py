"""Audit saved sources, completed endpoints, shared evaluation and time controls."""
import json,hashlib
from pathlib import Path
from urllib.parse import urlparse,unquote
import numpy as np
from bs4 import BeautifulSoup
from analyze_comparison import HERE,ROOT,records,label
from fd import DirectFD
from fd_rusanov import RusanovFD
from fd3 import ThirdOrderFD

checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
rr=records()
for r in rr:
    p=Path(r['path']);s=r['summary'];c=r['config'];a=np.load(p/'trajectory.npz')
    check(r['id']+' ordered outputs',np.all(np.diff(a['t'])>0))
    check(r['id']+' finite snapshots',np.all(np.isfinite(a['u'])))
    if s['completed']:check(r['id']+' reached T',abs(a['t'][-1]-c['T'])<1e-10)
    else:check(r['id']+' failure recorded',s['failure'] is not None and s['reached']<c['T'])
    for name,digest in s['source_hashes'].items():
        pp=p/'source'/name
        if not pp.exists():pp=ROOT/'versions/v1_periodic/mch'/name
        check(r['id']+' source '+name,pp.exists() and hashlib.sha256(pp.read_bytes()).hexdigest()==digest)
    if r['kind']=='FD':
        cls=ThirdOrderFD if c['order']==3 else (RusanovFD if c.get('variant')=='rusanov' else DirectFD)
        d=cls(**{k:c[k] for k in ['n','left','right','kappa','order','offset']})
        check(r['id']+' energy readback',abs(d.energy(a['u'][-1])-s['final']['energy'])<1e-8)
controls=[]
for method in ['FD2 half-cell','FD4 half-cell','FD-Rusanov']:
    sub=[r for r in rr if label(r)==method and r['config']['case']=='5.4' and r['config']['n']==2560]
    base=next(r for r in sub if r['config']['dt']==.00025)
    half=next(r for r in sub if r['config']['dt']==.000125)
    u=np.load(Path(base['path'])/'trajectory.npz')['u'][-1];v=np.load(Path(half['path'])/'trajectory.npz')['u'][-1]
    h=(base['config']['right']-base['config']['left'])/2560
    dist=float(np.sqrt(h*np.sum((u-v)**2)))
    controls.append(dict(method=method,native_state_l2_difference=dist,max_difference=float(max(abs(u-v)))))
    check(method+' temporal state difference',dist<1e-7,dist)
data=json.loads((HERE/'analysis/comparison.json').read_text())
check('manifest count',data['run_count']==len(rr))
check('failure count',len(data['failures'])==sum(not r['summary']['completed'] for r in rr))
for v in data['rows']:
    check(v['id']+f" t={v['t']} finite common error",np.isfinite(v['l2_u']) and np.isfinite(v['sampled_linf_u']))
    if v['t']==v['T']:check(v['id']+' final ranking complete',v['completed'])
for r in data['evaluation_controls']:check(r['id']+' evaluation quadrature',r['l2_relative_difference']<1e-5)
reports=['mch_ldg_fd_comparison_20261015.html']
if (HERE/'analysis/third_summary.json').exists():
    third=json.loads((HERE/'analysis/third_summary.json').read_text())
    check('FD3 manifest count',third['fd3_run_count']==sum(r['kind']=='FD' and r['config']['order']==3 for r in rr))
    check('FD3 smooth order',all(abs(p-3)<.1 for p in third['smooth_orders']))
    for c in third['time_controls']:
        check('FD3 temporal '+c['case']+' offset '+str(c['offset']),c['native_l2_distance']<1e-6,c['native_l2_distance'])
    reports.append('mch_ldg_fd3_comparison_20261015.html')
for name in reports:
    report=HERE.parents[2]/'report'/name
    soup=BeautifulSoup(report.read_text(encoding='utf-8'),'html.parser')
    for tag in soup.select('[href],img[src]'):
        ref=tag.get('href') or tag.get('src')
        if urlparse(ref).scheme or ref.startswith('#'):continue
        check(name+' link '+ref,(report.parent/unquote(ref)).resolve().exists())
out=dict(total=len(checks),passed=sum(c['passed'] for c in checks),failures=[c for c in checks if not c['passed']],time_controls=controls,checks=checks)
(HERE/'analysis/audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));assert not out['failures']
