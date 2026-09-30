"""Paper two-soliton parameters, continuous initial data at t=0, T=0.5."""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'hs_two_soliton_point_20260928/run_four_schemes.py'
spec = importlib.util.spec_from_file_location('two_soliton_model', SOURCE)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
model.T0, model.T1 = 0., .5
model.TIMES = (0., .25, .5)
model.U0, model.X0, _ = model.SOL.continuous_X(model.X, model.T0)
model.GRID = np.linspace(-1, 1, 32001)


def main():
    for name, dt in [('main', .003125), ('half_dt', .0015625)]:
        out = HERE / name
        out.mkdir(exist_ok=True)
        model.HERE, model.DT = out, dt
        config = dict(p=[1.1, 1.25], q=[11, 5], c_phys=1., a=model.A,
                      n=model.N, phase_normalized=[float(np.log(6.5))]*2,
                      shift=model.SOL.shift, initial='common continuous two-soliton at t=0',
                      X_bounds=[-4, 4], evaluation_bounds=[-1, 1], evaluation_points=32001,
                      initial_physical_bounds=[float(model.X0[0]), float(model.X0[-1])],
                      dt=dt, t0=0., t1=.5, times=model.TIMES, method='rk4',
                      driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      source_driver_sha256=model.base.sha(SOURCE),
                      four_scheme_sha256=model.base.sha(model.base.__file__),
                      engine_hashes=model.eng.source_hashes())
        results = {}
        for scheme in ('S1', 'S3', 'S4'):
            results[scheme] = model.run(scheme)
            (out / 'results.json').write_text(json.dumps(dict(configuration=config, results=results), indent=2)+'\n', encoding='utf-8')
            print(name, scheme, results[scheme]['status'], results[scheme]['last_time'], results[scheme]['metrics'].get('0.5'), flush=True)


if __name__ == '__main__':
    main()
