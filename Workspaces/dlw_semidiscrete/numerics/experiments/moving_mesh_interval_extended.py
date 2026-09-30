"""Additional regular parameter cases at nx=128 for interval robustness."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'lib'), str(ROOT / 'experiments')]
from moving_mesh_interval_study import transport_run, INTERVALS_D, PARAMETER_INDICES
from moving_mesh_route1_geometry import width
from moving_mesh_study import ALL
from parametric import Exact


def main():
    runs = []
    for idx, pars in enumerate(ALL):
        if idx in PARAMETER_INDICES:
            continue
        pid = f'P{idx+1}'
        pulse_width = width(Exact(pars, .125))
        for interval in INTERVALS_D:
            row = transport_run(pars, pulse_width, 128, .001, interval,
                                diagnose_defects=True)
            row['parameter_id'] = pid
            row['pulse_width'] = pulse_width
            runs.append(row)
            print(pid, interval, row['status'], row['remaps'], flush=True)
    result = {'scope': {'equation': 'controlled transport, not DLW',
                        'nx': 128, 'dt_nominal': .001,
                        'additional_parameter_indices': [i+1 for i in range(len(ALL))
                                                         if i not in PARAMETER_INDICES],
                        'D_final': 2}, 'runs': runs}
    sources = (Path(__file__), ROOT / 'experiments/moving_mesh_interval_study.py')
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sources}
    dest = ROOT / 'out' / 'moving_mesh' / 'interval_extended.json'
    dest.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
