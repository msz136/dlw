"""Read back saved fields against the four-term tau formula; compare half steps."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
GRID = np.linspace(-1., 1., 32001)


def exact_aux(X, t):
    beta = np.array([0., 1.1-11., 1.25-5., 1.1-11.+1.25-5.])[:, None]
    omega = np.array([0., 1/1.1-1/11, 1/1.25-1/5, 1/1.1-1/11+1/1.25-1/5])[:, None]
    phase = np.array([0., np.log(6.5), np.log(6.5), 2*np.log(6.5)+np.log(12/507)])[:, None]
    weights = np.exp(beta*X+omega*t+phase)
    weights /= weights.sum(axis=0)
    mean = (weights*omega).sum(axis=0)
    u = (weights*omega**2).sum(axis=0)-mean**2
    rho = 1/(1-(weights*omega*beta).sum(axis=0)+mean*(weights*beta).sum(axis=0))
    return X-mean-1/11-1/5, u, rho


def exact(x, t):
    lo, hi = x-3., x+3.
    for _ in range(60):
        mid = (lo+hi)/2
        left = exact_aux(mid, t)[0] < x
        lo, hi = np.where(left, mid, lo), np.where(left, hi, mid)
    xx, u, rho = exact_aux((lo+hi)/2, t)
    assert np.max(np.abs(xx-x)) < 3e-14
    return u, rho


def main():
    rows, diffs, initial = [], [], {}
    documents = {}
    for group in ('main', 'half_dt'):
        doc = json.loads((HERE/group/'results.json').read_text())
        documents[group] = doc
        for scheme, result in doc['results'].items():
            assert result['status']=='completed' and result['last_time']==.5
            path = HERE/group/result['profile']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==result['profile_sha256']
            with np.load(path) as z:
                for t in (0., .25, .5):
                    reference = exact(GRID, t)
                    for i, field in enumerate(('u','rho')):
                        coords=z[f't{t}_'+('x' if field=='u' else 'rho_x')]
                        values=z[f't{t}_{field}']
                        assert np.isfinite(coords).all() and np.isfinite(values).all()
                        assert (np.diff(coords)>0).all() and coords[0]<=-1 and coords[-1]>=1
                        error=float(np.abs(np.interp(GRID,coords,values)-reference[i]).max())
                        difference=abs(error-result['metrics'][str(t)][field])
                        diffs.append(difference)
                        assert difference<5e-13
                        rows.append(dict(run=group,scheme=scheme,time=t,field=field,error=error))
                if group=='main':
                    initial[scheme]=z['t0.0_x'].copy()
                    _, u, _ = exact_aux(np.linspace(-4,4,1601),0.)
                    if scheme=='S1':
                        assert np.max(np.abs(z['t0.0_u']-u))<1e-13
    # S1 reconstructs coordinates by summing edges; allow its accumulation roundoff.
    initial_node_difference=float(np.max(np.abs(initial['S1']-initial['S3'])))
    assert initial_node_difference<1e-13
    assert np.allclose(initial['S4'][[0,-1]],initial['S1'][[0,-1]],rtol=0,atol=1e-13)
    changes={s:{f:abs(documents['main']['results'][s]['metrics']['0.5'][f]-documents['half_dt']['results'][s]['metrics']['0.5'][f]) for f in ('u','rho')} for s in ('S1','S3','S4')}
    for doc in documents.values():
        for f in ('u','rho'):
            assert doc['results']['S4']['metrics']['0.5'][f]<doc['results']['S3']['metrics']['0.5'][f]<doc['results']['S1']['metrics']['0.5'][f]
    result=dict(trajectories=6,independent_metrics=len(rows),max_independent_difference=max(diffs),max_initial_moving_node_difference=initial_node_difference,same_initial_endpoints=True,half_dt_endpoint_changes=changes,endpoint_ranking_unchanged=True)
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    with (HERE/'errors.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print(json.dumps(result))


if __name__=='__main__':
    main()
