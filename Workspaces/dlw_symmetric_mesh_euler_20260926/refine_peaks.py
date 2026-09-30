"""Extra output-resolution check for P6's marginal fine-grid v comparison."""
import json
from pathlib import Path
import numpy as np
from sym_model import SymmetricProblem,BASE,Parameters,evaluate
from experiment import OUT,sha,dump
from analyze import load_rows

def main():
    new,_,old=load_rows();rows={**old,**new['rows']};out={}
    for phase in ('space_x','fine_half','fine_quarter'):
        for branch in ('fixed','minus','plus','symmetric'):
            key=f'P6_sd_{branch}_{phase}';r=rows[key]
            root=OUT if branch=='symmetric' else BASE/'out'
            file=root/r['profile'];assert sha(file)==r['profile_sha256']
            a=np.load(file);p=SymmetricProblem(Parameters(4,1,3,4),route='sd',branch=branch,nx=1024)
            zz,ss=a['t0.01_z'],a['t0.01_s']
            e32=evaluate(p,zz,ss,.01,evaluation_factor=32,reconstruction_factor=32)
            e64=evaluate(p,zz,ss,.01,evaluation_factor=64,reconstruction_factor=64)
            out[key]=dict(source=str(file),sha256=sha(file),dt=r['spec']['dt'],original=r['snapshots']['0.01']['errors'],dense32=e32,dense64=e64)
    dump(OUT/'p6_dense_peak_check.json',dict(reason='Symmetric v benefit changed sign under Euler step reduction; re-evaluate common physical maxima much more densely.',rows=out))
    for phase in ('space_x','fine_half','fine_quarter'):
        base=out[f'P6_sd_fixed_{phase}']['dense64'];sym=out[f'P6_sd_symmetric_{phase}']['dense64']
        print(phase,'symmetric / fixed', {f:sym[f]/base[f] for f in ('u','v')})
    print('max dense32/dense64 change',max(abs(r['dense32'][f]/r['dense64'][f]-1) for r in out.values() for f in ('u','v')))

if __name__=='__main__':main()
