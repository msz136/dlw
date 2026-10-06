"""Independent saved-state boundaries, paired initial fields, and cell mass."""
import json
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import experiment as e


def main():
    runs = json.loads((ROOT/'out/results.json').read_text(encoding='utf-8'))['runs']
    rows, initial, pairs = [], {}, []
    for r in runs:
        assert r['source_sha256'] == e.sha(ROOT/'experiment.py')
        assert e.sha(r['profile']) == r['profile_sha256']
        s = r['spec']
        with np.load(r['profile']) as a:
            boundary_error, mass_rows = 0., []
            for h in r['history']:
                prefix = 't'+format(h['t'], 'g')
                x, R = a[prefix+'_x'], a[prefix+'_R']
                assert abs(x[0]+1)+abs(x[-1]-1) < 1e-13
                for f in ('u', 'v'):
                    boundary_error = max(boundary_error, float(abs((a[prefix+'_'+f]-a[prefix+'_exact_'+f])[:, [0, -1]]).max()))
                masses = .5*(R[1:]+R[:-1])*np.diff(x)
                mass_rows.append(dict(t=h['t'], relative_cellmass_deviation=float(abs(masses/masses.mean()-1).max())))
            key = tuple(s[k] for k in ('case', 'mesh', 'motion', 'variant', 'nx', 'h', 'dt'))
            initial[(key, s['model'])] = tuple(a['t0_'+k].copy() for k in ('x', 'u', 'v'))
            rows.append(dict(spec=s, endpoint_field_error=boundary_error, cellmass_checks=mass_rows))
    for (key, model), aa in initial.items():
        if model == 'SD' and (key, 'FD') in initial:
            bb = initial[(key, 'FD')]
            pairs.append(dict(type='SD_vs_FD', key=key, difference=max(float(abs(x-y).max()) for x, y in zip(aa, bb))))
        if key[2] == 'moving':
            kf = list(key); kf[2] = 'frozen'; kf = tuple(kf)
            if (kf, model) in initial:
                bb = initial[(kf, model)]
                pairs.append(dict(type='moving_vs_frozen', key=key, model=model,
                                  difference=max(float(abs(x-y).max()) for x, y in zip(aa, bb))))
    maxboundary = max(r['endpoint_field_error'] for r in rows)
    maxinitial = max(r['difference'] for r in pairs)
    assert maxboundary < 1e-11 and maxinitial < 1e-11
    result = dict(source_sha256=e.sha(ROOT/'experiment.py'), runs=len(runs),
                  snapshot_count=sum(len(r['history']) for r in runs),
                  max_native_boundary_error=maxboundary, max_initial_pair_difference=maxinitial,
                  pair_checks=len(pairs), rows=rows, initial_pairs=pairs,
                  cellmass_note='Native-node trapezoidal cell mass is a diagnostic; initial grid uses dense mass inversion. No exact discrete equidistribution certificate.')
    e.dump(HERE/'snapshot_boundary_mesh.json', result)
    print('snapshots', result['snapshot_count'], 'runs', len(runs), 'boundary', maxboundary, 'initial pairs', maxinitial)


if __name__ == '__main__':
    main()
