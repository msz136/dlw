from pathlib import Path
import json
import hashlib
import numpy as np
import common as C

HERE=Path(__file__).resolve().parent


def main():
    cfg=C.NS['case_config']('A');cfg.update(nx=24,L=8.,yhalf=1.2,eval_half=2.,eval_yhalf=.6)
    rng=np.random.default_rng(314159)
    rows=[]
    for kind in ['SD','FD']:
        obj,_=C.setup('A',kind,cfg)
        t=.003;dt=1e-4
        z=C.reference(obj,t)
        dirs=rng.normal(size=(2,z.size))*.01
        value,analytic=C.step_and_jvp(obj,t,z,dirs,dt)
        cs=np.array([np.imag(C.common_step(obj,t,z+1j*1e-25*d,dt))/1e-25 for d in dirs])
        fd=np.array([(C.common_step(obj,t,z+1e-4*d,dt)-C.common_step(obj,t,z-1e-4*d,dt))/(2e-4) for d in dirs])
        scale=np.max(abs(analytic))
        entry=dict(kind=kind,nstate=z.size,
                   affine_roundtrip_linf=float(np.max(abs(C.from_native(obj,C.to_native(obj,z,t),t)-z))),
                   batched_jvp_complex_step_relative_linf=float(np.max(abs(analytic-cs))/scale),
                   batched_jvp_centered_relative_linf=float(np.max(abs(analytic-fd))/scale),
                   base_step_linf_difference=float(np.max(abs(value-C.common_step(obj,t,z,dt)))))
        assert entry['affine_roundtrip_linf']<1e-13
        assert entry['batched_jvp_complex_step_relative_linf']<2e-12
        assert entry['batched_jvp_centered_relative_linf']<2e-7
        assert entry['base_step_linf_difference']<1e-14
        rows.append(entry)
    result=dict(passed=True,checks=rows,protocol_sha256=hashlib.sha256((HERE/'PROTOCOL.md').read_bytes()).hexdigest(),
                common_sha256=hashlib.sha256((HERE/'common.py').read_bytes()).hexdigest(),
                frozen_solver_sha256=hashlib.sha256((C.ROOT/'Workspaces/dlw_three_tracks_20261013/shared/solver_cells.json').read_bytes()).hexdigest())
    (HERE/'common_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
