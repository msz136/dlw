"""Audit saved four-scheme fields and import tables by configuration."""
import csv
import json
import numpy as np
from review_table_handoff import HERE, ROOT, exact, sha
SOURCE=ROOT/'Workspaces/hs_four_schemes_20260927'
OUT=HERE/'four_scheme_review'
METHODS={'euler':'Euler','heun':'Heun','rk4':'RK4','rk8':'RK8'}
NAMES=['S1 原可积·论文动格','S2 校准·论文动格','S3 直接差分·论文动格','S4 直接差分·均匀固定格']

class ReviewedTables:
    def __init__(self):
        self.data=json.loads((SOURCE/'out/results.json').read_text())
        self.validation=json.loads((SOURCE/'out/validation.json').read_text())
        with (SOURCE/'out/main_cells.csv').open(encoding='utf-8-sig',newline='') as f:self.rows=list(csv.DictReader(f))
        self.cells={(int(float(r['p'])),int(r['n']),r['method'],float(r['t']),r['scheme']):r for r in self.rows}
        assert len(self.cells)==len(self.rows)==1280
    def display(self,p,n,method,t,scheme):
        r=self.cells[p,n,method,t,scheme]
        assert float(r['dt'])==(.003125 if n==400 else .0125)
        assert int(r['evaluation_points'])==(16001 if n==400 else 8001)
        return f"{float(r['u_error']):.3e} / {float(r['rho_error']):.3e}"
    def parameter_table(self,n,method,t):
        rows=['| p | '+' | '.join(NAMES)+' |','|---:|'+'---:|'*4]
        for p in range(3,23):rows.append('| '+str(p)+' | '+' | '.join(self.display(p,n,method,t,f'S{i}') for i in range(1,5))+' |')
        return '\n'.join(rows)
    def time_table(self,p,t):
        rows=['| 方案 | Euler | Heun | RK4 | RK8 |','|---|---:|---:|---:|---:|']
        for i,name in enumerate(NAMES,1):rows.append('| '+name+' | '+' | '.join(self.display(p,200,m,t,f'S{i}') for m in METHODS)+' |')
        return '\n'.join(rows)
    def count_table(self):
        rows=['| 比较（分子/分母） | 要回答的问题 | u 误差更小 | rho 误差更小 |','|---|---|---:|---:|']
        for pair,label in [('S2/S1','校准是否有效'),('S3/S4','普通差分采用论文动网格是否有利'),('S1/S3','原可积与普通动网格差分'),('S2/S3','校准与普通动网格差分')]:
            wins=self.validation['winning_p']['N400_rk4_t0.5_'+pair]
            rows.append(f'| {pair} | {label} | {len(wins["u"])}/20 | {len(wins["rho"])}/20 |')
        return '\n'.join(rows)
    def audit(self):
        d=self.data;OUT.mkdir(exist_ok=True)
        assert len(d['rows'])==len(d['plan'])==736
        assert sha(SOURCE/'run_study.py')==d['driver_sha256']
        assert sha(ROOT/'Workspaces/hs_error_theory_20260926/run_designed_cases.py')==d['engine_sha256']
        for p,h in d['source_hashes'].items():assert sha(ROOT/'Workspaces'/p)==h
        for p,h in d['sources'].items():assert sha(p)==h
        worst=0.;checks=0
        for key,r in d['rows'].items():
            assert r['status']=='completed' and r['spec']==d['plan'][key]
            assert sha(r['profile'])==r['profile_sha256']
            with np.load(r['profile']) as z:
                for t in (.25,.5):
                    x,u,rx,rho=(z[f't{t}_{f}'] for f in ('x','u','rho_x','rho'))
                    assert all(np.isfinite(v).all() for v in (x,u,rx,rho))
                    assert np.min(np.diff(x))>0 and np.min(np.diff(rx))>0 and np.min(rho)>0
                    assert x[0]<=-2 and x[-1]>=2 and rx[0]<=-2 and rx[-1]>=2
                    xx,ue,re=exact(r['spec']['p'],t)
                    for field,e in [('u',np.abs(np.interp(xx,x,u)-ue)),('rho',np.abs(np.interp(xx,rx,rho)-re))]:
                        for size,stride in ((8001,4),(16001,2),(32001,1)):
                            diff=abs(e[::stride].max()-r['snapshots'][str(t)][str(size)][field]);worst=max(worst,float(diff));checks+=1
                            assert diff<5e-13
        for c in self.rows:
            r=d['rows'][c['case_key']];assert d['schemes'][c['scheme']]==r['spec']['route']
            for f in ('u','rho'):assert float(c[f+'_error'])==r['snapshots'][c['t']][c['evaluation_points']][f]
        for n in (200,400):
            for method in METHODS:
                for t in (.25,.5):
                    for pair in ('S2/S1','S3/S4','S1/S3','S2/S3'):
                        a,b=pair.split('/');win={f:[p for p in range(3,23) if float(self.cells[p,n,method,t,a][f+'_error'])<float(self.cells[p,n,method,t,b][f+'_error'])] for f in ('u','rho')}
                        assert win==self.validation['winning_p'][f'N{n}_{method}_t{t}_{pair}']
        with (SOURCE/'out/domain_control_cells.csv').open(encoding='utf-8-sig') as f:controls=list(csv.DictReader(f))
        for c in controls:
            assert sha(c['profile'])==c['profile_sha256']
            with np.load(c['profile']) as z:
                t=float(c['t']);xx,*ref=exact(float(c['p']),t);stride=2 if int(c['n'])==400 else 4
                for field,rr in zip(('u','rho'),ref):
                    x=z[f't{t}_'+('x' if field=='u' else 'rho_x')]
                    error=np.abs(np.interp(xx,x,z[f't{t}_{field}'])-rr)[::stride].max()
                    assert abs(error-float(c[field+'_error']))<5e-13
        result=dict(status='passed',profiles=736,metric_checks=checks,max_absolute_difference=worst,main_double_field_cells=1280,domain_control_profiles=len({c['profile'] for c in controls}),results_sha256=sha(SOURCE/'out/results.json'))
        (OUT/'review.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)

if __name__=='__main__':ReviewedTables().audit()
