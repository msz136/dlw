"""A sufficient criterion for sufficiently small T; no time evolution or fitting."""
from error_model import ErrorModel,Parameters,norm
from scan import HERE,OUT,dump,sha
import json
import numpy as np
def main():
    scan=json.loads((OUT/'scan.json').read_text(encoding='utf-8'));rows={}
    for key,s in scan['plan'].items():
        a,p,q=s['parameters'];m=ErrorModel(Parameters(a,p,q,p+q),**{k:s[k] for k in ('route','c','kappa','h','nx','L','yhalf')})
        tau=m.rhs(0,m.exact(0))-m.exact(0,True);p,v=m.unpack(tau)
        rows[key]=dict(spec=s,initial_physical_error_velocity=[norm(m.linear_u(p)),norm(v)])
    groups=[]
    for center in ('P2','P6'):
        for config in ('main','fine'):
            for method in ('original','theory'):
                ratios=[];center_ratio=None
                for key,row in rows.items():
                    s=row['spec']
                    if (s['center'],s['config'],s['method'])!=(center,config,method):continue
                    fd=rows[f'{s["point"]}_{config}_fd']['initial_physical_error_velocity']
                    ratio=np.array(row['initial_physical_error_velocity'])/fd;ratios.append(ratio)
                    if s['point']==center+'_000':center_ratio=ratio.tolist()
                groups.append(dict(center=center,config=config,method=method,center_ratio=center_ratio,
                    sampled_both_smaller=int(sum(max(r)<1 for r in ratios)),sampled_u_max=float(max(r[0] for r in ratios)),sampled_v_max=float(max(r[1] for r in ratios))))
    dump(OUT/'initial_defect.json',dict(rows=rows,groups=groups,metric='Maximum on original physical nodes of error velocity at t=0',
        source_hashes={str(HERE/'initial_defect.py'):sha(HERE/'initial_defect.py'),str(HERE/'error_model.py'):sha(HERE/'error_model.py')}))
    print(json.dumps(groups,indent=2))
if __name__=='__main__':main()
