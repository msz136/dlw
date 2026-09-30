"""Match reviewed cells by mathematical configuration, never HTML table index."""
import csv
import json
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'Workspaces/hs_table_data_20260927/out'
NAMES=['S1 原可积＋Rm','S2 原可积＋均匀','S3 校准可积＋Rm','S4 校准可积＋均匀','S5 直接差分＋Rm','S6 直接差分＋均匀']
METHODS={'euler':'Euler','heun':'Heun','rk4':'RK4','rk8':'RK8'}

class ReviewedTables:
    def __init__(self):
        self.review=json.loads((HERE/'table_handoff_review/review.json').read_text(encoding='utf-8'))
        assert self.review['status']=='passed'
        for filename,key in [('results.json','results_sha256'),('expanded_cells.csv','expanded_csv_sha256')]:
            assert hashlib.sha256((SOURCE/filename).read_bytes()).hexdigest()==self.review[key]
        with (SOURCE/'expanded_cells.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        self.cells={(int(float(r['p'])),int(r['N']),r['method'],float(r['t']),r['scheme']):r for r in rows}
        assert len(self.cells)==1920
    def display(self,p,n,method,t,scheme):
        r=self.cells[p,n,method,t,scheme]
        assert float(r['dt'])==(.003125 if n==400 else .0125)
        assert int(r['evaluation_points'])==(16001 if n==400 else 8001)
        if scheme in ('S1','S2','S3','S4'):
            assert r['status']=='model_not_constructed';return '—'
        assert r['status']=='completed'
        return f"{float(r['u_error']):.3e} / {float(r['rho_error']):.3e}"
    def parameter_table(self,n,method,t):
        rows=['| p | '+' | '.join(NAMES)+' |','|---:|'+'---:|'*6]
        for p in range(3,23):rows.append('| '+str(p)+' | '+' | '.join(self.display(p,n,method,t,f'S{i}') for i in range(1,7))+' |')
        return '\n'.join(rows)
    def time_table(self,p,t):
        rows=['| 方案 | Euler | Heun | RK4 | RK8 |','|---|---:|---:|---:|---:|']
        for i,name in enumerate(NAMES,1):rows.append('| '+name+' | '+' | '.join(self.display(p,200,m,t,f'S{i}') for m in METHODS)+' |')
        return '\n'.join(rows)
    def count_table(self):
        rows=['| N / 时间步长 | 时间算法 | t=.25：u 改善 | t=.5：u 改善 | 两个时刻的 rho 改善 |','|---|---|---:|---:|---|']
        for n in (400,200):
            for m,label in METHODS.items():
                a,b=[self.review['counts'][f'N{n}_{m}_t{t}'] for t in (.25,.5)]
                rows.append(f'| {n} / '+('.003125' if n==400 else '.0125')+f' | {label} | {a["u"]}/20 | {b["u"]}/20 | {a["rho"]}/20、{b["rho"]}/20 |')
        return '\n'.join(rows)
