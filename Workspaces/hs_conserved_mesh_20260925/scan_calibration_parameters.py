"""Extend the calibrated-lattice comparison to nine fixed p values.

Reuse exact matching old records, keep frozen solvers unchanged, and collect
matched RK4 comparisons plus spatial/time/domain sensitivity controls.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import run_parameter_calibration as base

HERE=Path(__file__).resolve().parent
OUT=HERE/"out"/"calibration_parameter_scan"
PS=(3.,4.,5.,6.,8.,10.,12.,16.,20.)
ROUTES=base.ROUTES


def plan():
    result={}
    for p in PS:
        for route in ROUTES:
            for n,dt,label in ((400,base.DT,"main"),(800,base.DT,"space"),
                               (800,base.DT/2,"time")):
                spec=dict(p=p,route=route,n=n,dt=dt,method="rk4",halfwidth=4.,purposes=[label])
                result[base.case_key(spec)]=spec
            if p in (3.,20.):
                spec=dict(p=p,route=route,n=500,dt=base.DT,method="rk4",halfwidth=5.,
                          purposes=["domain"])
                result[base.case_key(spec)]=spec
    return result


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    old_root=base.OUT
    old=json.loads((old_root/"results.json").read_text(encoding="utf-8"))
    hashes=base.source_hashes()
    assert hashes==old["source_hashes"]
    hashes["scan_calibration_parameters.py"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    spec_plan=plan()
    path=OUT/"results.json"
    if path.exists():
        saved=json.loads(path.read_text(encoding="utf-8"))
        assert saved["source_hashes"]==hashes and saved["plan"]==spec_plan
    else:
        saved=dict(source_hashes=hashes,plan=spec_plan,configuration=dict(
            p=PS,physical_c=1.,N=400,dt=base.DT,method="rk4",times=base.TIMES,
            core=[-2.,2.],evaluation_points=8001,scope="exploratory deterministic p scan"),rows={})
        base.dump(path,saved)
    # Redirect only the new driver's artifacts; the original module file is untouched.
    base.OUT=OUT
    for key,spec in spec_plan.items():
        if key in saved["rows"]:
            continue
        if key in old["rows"]:
            row=dict(old["rows"][key])
            row["spec"]=spec
            row["profile"]=str((old_root/row["profile"]).resolve())
            row["provenance"]="reused exact matching original calibration record"
        else:
            try:
                row={"spec":spec,**base.run_one(spec),"provenance":"new evolution"}
                row["profile"]=str((OUT/row["profile"]).resolve())
            except Exception as exc:
                row=dict(spec=spec,status="failed",error=f"{type(exc).__name__}: {exc}",
                         provenance="new evolution")
        saved["rows"][key]=row
        base.dump(path,saved)
        print(f"{len(saved['rows'])}/{len(spec_plan)} {key}: {row['status']} ({row['provenance']})",
              flush=True)
    print(path,flush=True)


if __name__=="__main__":
    main()
