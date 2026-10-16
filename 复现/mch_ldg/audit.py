"""Readback checks for every saved run, source provenance, and report links."""
import hashlib,json
from pathlib import Path
from urllib.parse import unquote,urlparse
import numpy as np
from bs4 import BeautifulSoup
from mch.ldg import LDG
from mch.boundary import DirichletLDG

root=Path(__file__).resolve().parents[2]
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
for path in sorted(Path('results').glob('*/summary.json')):
    s=json.loads(path.read_text());c=s['config'];a=np.load(path.parent/'trajectory.npz')
    check(str(path.parent)+' shape',a['u'].shape==(len(a['t']),c['n'],c['k']+1))
    check(str(path.parent)+' output times',np.all(np.diff(a['t'])>0))
    hist=json.loads((path.parent/'history.json').read_text())
    check(str(path.parent)+' diagnostic times',np.allclose(a['t'],[r['t'] for r in hist]))
    if s['completed']:
        check(str(path.parent)+' endpoint',abs(a['t'][-1]-c['T'])<1e-10 and abs(s['reached']-c['T'])<1e-10)
        check(str(path.parent)+' finite',np.all(np.isfinite(a['u'])))
    else:
        check(str(path.parent)+' failure marked',s['failure'] is not None and s['reached']<c['T'])
    kwargs={key:c[key] for key in ['n','k','left','right','kappa','flux']}
    d=DirichletLDG(**kwargs,boundary_value=c.get('boundary_value',0.)) if c['boundary']=='dirichlet' else LDG(**kwargs)
    check(str(path.parent)+' energy readback',abs(d.energy(a['u'][-1])-hist[-1]['energy'])<1e-9)
    for name,digest in s['source_hashes'].items():
        src=path.parent/'source'/name
        if not src.exists():src=Path('versions/v1_periodic/mch')/name
        check(str(path.parent)+' source '+name,src.exists() and hashlib.sha256(src.read_bytes()).hexdigest()==digest)
report=root/'report/mch_ldg_reproduction_20261015.html'
soup=BeautifulSoup(report.read_text(encoding='utf-8'),'html.parser')
for tag in soup.select('[href],img[src]'):
    ref=tag.get('href') or tag.get('src')
    if urlparse(ref).scheme or ref.startswith('#'):continue
    target=(report.parent/unquote(ref)).resolve()
    check('report link '+ref,target.exists())
for flux in ('conservative','dissipative'):
    for bg in (0.,1.):
        d=DirichletLDG(n=20,k=3,boundary_value=bg,flux=flux)
        u=np.zeros((20,4));u[:,0]=bg
        check(f'Dirichlet constant bg={bg} {flux}',np.max(abs(d.rhs(u)))<1e-10)
out=dict(total=len(checks),passed=sum(r['passed'] for r in checks),failures=[r for r in checks if not r['passed']],checks=checks)
Path('results/audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));assert not out['failures']
