"""Evaluate the frozen refinement prediction against independent source data."""
from pathlib import Path
import csv
import importlib.util
import json
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'refinement'
spec=importlib.util.spec_from_file_location('mechanism_sources',HERE/'sources/common_sources.py')
S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
spec=importlib.util.spec_from_file_location('mechanism_homotopy',HERE/'homotopy.py')
H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)


def compare(a,b):
    return dict(relative_vector_difference=float(np.linalg.norm(a-b)/np.linalg.norm(b)),
                cosine=float(np.vdot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))))


def main():
    rows=[];checks={}
    for kind in ('SD','FD'):
        with np.load(H.SHARED/f'C_{kind}_RK4.npz') as archive:
            pos=np.flatnonzero(np.isclose(archive['t'],.001,atol=1e-14,rtol=0))
            assert len(pos)==1
            i=pos[0]
            for field in ('u','v'):
                e=archive[field][i]-archive['exact_'+field][i]
                rows.append(dict(model=kind,dx=.1,T=.001,field=field,rms=float(np.sqrt(np.mean(e**2)))))
        record=json.loads((OUT/f'C_{kind}_dx0025.json').read_text(encoding='utf-8'))
        obj=H.NS['SDModel' if kind=='SD' else 'FDModel']('C',kind,record['config'])
        parts=S.source_parts(obj,0.,details=True)
        iy=np.flatnonzero(abs(obj.y)<30)
        ix=np.flatnonzero(abs(obj.X.x)<=30+1e-10)
        with np.load(OUT/f'C_{kind}_dx0025.npz') as archive:
            assert np.array_equal(archive['x'],obj.X.x[ix])
            assert np.array_equal(archive['y'],obj.y[iy])
            for field in ('u','v'):
                error=archive['error_'+field]
                predicted=.001*parts['fields']['total'][field][np.ix_(iy,ix)]
                rows.append(dict(model=kind,dx=.025,T=.001,field=field,rms=float(np.sqrt(np.mean(error**2)))))
                checks[f'{kind}_{field}_initial_source_prediction']=compare(predicted,error)
        del parts,obj
    with np.load(OUT/'C_SD_dx0025.npz') as a,np.load(OUT/'C_SD_dx0025_halfdt.npz') as b:
        for field in ('u','v'):
            checks[f'SD_{field}_time_refinement']=compare(b['error_'+field],a['error_'+field])
    ratios={}
    for dx in (.1,.025):
        for field in ('u','v'):
            values={r['model']:r['rms'] for r in rows if r['dx']==dx and r['field']==field}
            ratios[f'dx{dx}_{field}']=values['SD']/values['FD']
    result=dict(rows=rows,ratios=ratios,checks=checks,
                prediction_confirmed=ratios['dx0.1_u']<1<ratios['dx0.025_u'])
    with (OUT/'comparison.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
