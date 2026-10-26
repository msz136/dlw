"""Independent saved-array audit, without importing the experiment runner."""
from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent


def max_error(value, reference, y):
    return float(np.max(abs(value-reference)[abs(y)<=1.8+1e-12]))


rows = json.loads((HERE/'results.json').read_text(encoding='utf8'))
initial = json.loads((HERE/'initial_results.json').read_text(encoding='utf8'))
irecords = {(r['case'],r['method']):r for r in initial}
audits = []
for record in rows:
    case, method = record['case'], record['method']
    path = HERE/f'{case}_{method}_RK4.npz'
    with np.load(path) as f, np.load(HERE/f'initial_{case}_{method}.npz') as g:
        assert record['status']=='complete' and float(f['reached'])==.01
        assert (record['h'],record['dx'],record['dt'],record['a'])==(.1,.1,.0001,2.)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['artifact_sha256']
        assert np.array_equal(f['x'],g['x']) and np.array_equal(f['y'],g['y'])
        assert np.array_equal(f['yv'],g['yv'])
        assert np.isfinite(f['z']).all() and np.isfinite(f['u']).all() and np.isfinite(f['v']).all()
        if method=='Centered-SD':
            u,w = f['z']
            freq = 2*np.pi*np.fft.rfftfreq(len(f['x']),.1)
            pmult = np.zeros_like(freq,dtype=complex)
            pmult[1:-1]=1/(1j*freq[1:-1])
            aa = w*w/32-w/4
            primitive = np.fft.irfft(np.fft.rfft(np.diff(aa,axis=0),axis=-1)*pmult,
                                     n=len(f['x']),axis=-1)
            reconstructed = np.diff(u,axis=0)/.1+(w[1:]+w[:-1])/2+.1*primitive
            map_difference = float(np.max(abs(reconstructed-f['v'])))
        else:
            map_difference = float(np.max(abs(f['z'][1]-f['v'])))
        assert map_difference<1e-13
        end = [max_error(f['u'],f['u_ref'],f['y']),max_error(f['v'],f['v_ref'],f['yv'])]
        start = [max_error(g['ut'],g['ut_ref'],g['y']),max_error(g['vt'],g['vt_ref'],g['yv'])]
        end_difference = float(np.max(abs(np.array(end)-record['error'])))
        initial_difference = float(np.max(abs(np.array(start)-irecords[case,method]['total'])))
        assert end_difference==0 and initial_difference==0
        audits.append(dict(case=case,method=method,recomputed_final_errors=end,
                           recomputed_initial_errors=start,final_record_difference=end_difference,
                           initial_record_difference=initial_difference,
                           independently_reconstructed_v_difference=map_difference))
out = dict(status='passed',records=len(audits),audits=audits,
           scope='Saved physical-field reconstruction, parameters, completion, source-state hashes and table maxima. Reference certification is separate.')
(HERE/'independent_saved_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
