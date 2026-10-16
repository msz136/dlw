"""Structural checks independent of long-time experiments."""
import json
from pathlib import Path
import numpy as np
from mch.ldg import LDG
from mch.exact import profile


def main():
    checks=[]; rng=np.random.default_rng(137)
    def check(name,value,tol):
        checks.append(dict(name=name,value=float(value),tolerance=tol,passed=bool(value<tol)))
    for k in range(4):
        for flux in ('conservative','dissipative'):
            d=LDG(n=13,k=k,left=-np.pi,right=np.pi,kappa=.7,flux=flux)
            u=.05*rng.normal(size=(d.n,k+1));u[:,0]+=1
            wt=np.tile(d.mass,d.n)
            adj=d.dp.toarray()*wt[:,None]+d.dm.toarray().T*wt[None,:]
            check(f'adjoint P{k} {flux}',np.max(abs(adj)),1e-11)
            check(f'constant P{k} {flux}',np.max(abs(d.deriv_minus(np.pad(np.ones((d.n,1)),((0,0),(0,k)))))),1e-11)
            ut=d.rhs(u)
            rate=d.energy_rate(u,ut); pred=d.predicted_energy_rate(u)
            check(f'energy identity P{k} {flux}',abs(rate-pred)/(1+abs(pred)),2e-10)
            check(f'mass derivative P{k} {flux}',abs(d.mass_integral(ut)),1e-10)
            if flux=='dissipative': check(f'energy sign P{k}',max(0.,rate),1e-10)
            vec=rng.normal(size=d.A.shape[0]);sol=d.lu.solve(vec)
            check(f'Helmholtz P{k} {flux}',np.linalg.norm(d.A@sol-vec)/np.linalg.norm(vec),1e-10)
    for case,kap in [('5.1',0.),('5.2',1.),('5.3',1.)]:
        x=np.linspace(-8,8,77)+.013;t=.11;eps=1e-5
        u,r=profile(case,x,t,kappa=kap)
        fd=(profile(case,x+eps,t,kappa=kap)[0]-profile(case,x-eps,t,kappa=kap)[0])/(2*eps)
        check(f'exact derivative {case}',np.max(abs(fd-r)),2e-7)
    # Discrete Radau derivative must equal L2 projection of exact derivative.
    d=LDG(n=20,k=3,left=-np.pi,right=np.pi)
    u=d.project(lambda x:1+.1*np.cos(x))
    rp=d.project(lambda x:-.1*np.sin(x),'l2')
    check('Radau derivative identity',np.max(abs(d.deriv_minus(u)-rp)),1e-11)
    p=Path('results');p.mkdir(exist_ok=True)
    (p/'verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(dict(total=len(checks),passed=sum(c['passed'] for c in checks),failures=[c for c in checks if not c['passed']]),indent=2))
    assert all(c['passed'] for c in checks)

if __name__=='__main__':main()
