"""Nine-parameter first-order time comparison with unchanged spatial routes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import run_parameter_calibration as base
from scan_calibration_parameters import PS, ROUTES

HERE=Path(__file__).resolve().parent
OUT=HERE/"out"/"euler_comparison"
DTS=(.0125,.00625,.003125,.0015625)


def plan():
    plans={}
    for p in PS:
        for route in ROUTES:
            for dt in DTS:
                spec=dict(p=p,route=route,n=400,method="euler",dt=dt,halfwidth=4.,
                          purposes=["euler_time_sweep"])
                plans[base.case_key(spec)]=spec
            if p in (3.,12.,20.):
                spec=dict(p=p,route=route,n=400,method="rk4",dt=.0015625,halfwidth=4.,
                          purposes=["rk4_reference_halfstep_check"])
                plans[base.case_key(spec)]=spec
    return plans


def main():
    old_path=HERE/"out"/"calibration_parameter_scan"/"results.json"
    old=json.loads(old_path.read_text(encoding="utf-8"))
    hashes=base.source_hashes()
    assert all(old["source_hashes"].get(k)==v for k,v in hashes.items())
    hashes["run_euler_comparison.py"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest=plan()
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/"results.json"
    if path.exists():
        saved=json.loads(path.read_text(encoding="utf-8"))
        assert saved["source_hashes"]==hashes and saved["plan"]==manifest
    else:
        saved=dict(source_hashes=hashes,plan=manifest,configuration=dict(
            p=PS,n=400,times=base.TIMES,dts=DTS,primary_dt=.003125,
            routes=ROUTES,physical_c=1.,core=[-2.,2.],evaluation_points=8001,
            rk4_reference=str(old_path.resolve()),
            rk4_reference_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest(),
            scope="deterministic first-order time experiment; not exact GSG replication"),rows={})
        base.dump(path,saved)
    base.OUT=OUT
    for key,spec in manifest.items():
        if key in saved["rows"]:continue
        try:
            row=dict(spec=spec,**base.run_one(spec))
            row["profile"]=str((OUT/row["profile"]).resolve())
        except Exception as exc:
            row=dict(spec=spec,status="failed",error=f"{type(exc).__name__}: {exc}")
        saved["rows"][key]=row
        base.dump(path,saved)
        print(f"{len(saved['rows'])}/{len(manifest)} {key}: {row['status']}",flush=True)
    print(path,flush=True)


if __name__=="__main__":main()
