"""Recompute comparisons from saved fields; avoids amplitude-dependent interpolation tolerances."""
from parametric_study import ROOT,OUT,save,inf
from parametric_perturb import compare
import json,numpy as np
from scipy.interpolate import RectBivariateSpline

def read(name):return json.loads((OUT/(name+'.json')).read_text())['data']
def key(g):return json.dumps([g['pars'],g['mode'],g['eps']],sort_keys=True)
def at(rows,t):return next((r for r in rows if abs(r['t']-t)<1e-10),None)

def main():
    original=read('parametric_perturbations');refs={key(g):g for g in read('parametric_reference_controls')};out=[]
    # Exact tensor spline interpolation must recover the input samples even for tiny amplitudes.
    yy=np.linspace(-1,1,12);xx=np.linspace(-10,10,64);zz=1e-8*np.outer(np.cos(yy),np.exp(-xx*xx))
    assert inf(RectBivariateSpline(yy,xx,zz,s=0)(yy,xx)-zz)<1e-21
    for g in original:
        if key(g) not in refs:continue
        r=refs[key(g)];target=r['references'][4]
        rr=r['references']
        controls={name:compare(rr[i],rr[j]) for name,i,j in [('x_256_384',0,1),('x_384_512',1,2),
                  ('y_003125_0015625',2,3),('dt_halving',3,4),('model_agreement',5,4)]}
        variants=[]
        for v in g['variants']:
            variants.append({'config':v['config'],'file':v['file'],'comparison':compare(v,target)})
        decisions=[]
        for t in (.005,.01):
            checks={k:at(v,t) for k,v in controls.items()}
            available=all(x is not None for x in checks.values())
            fd_gate=available and all(sum(checks[k][f]['relative_response_error'] for k in ('x_384_512','y_003125_0015625','dt_halving'))<.01 for f in ('u','v'))
            models=available and all(checks['model_agreement'][f]['relative_response_error']<.05 for f in ('u','v'))
            decisions.append({'t':t,'fd_resolution_gate':bool(fd_gate),'cross_model_gate':bool(models),
                              'joint_gate':bool(fd_gate and models)})
        out.append({'pars':g['pars'],'mode':g['mode'],'eps':g['eps'],'reference':target['file'],'controls':controls,'gates':decisions,'variants':variants})
    save('parametric_assessment',out)
    print('groups',len(out),'FD resolution passes',sum(d['fd_resolution_gate'] for g in out for d in g['gates']),
          'joint passes',sum(d['joint_gate'] for g in out for d in g['gates']),flush=True)

if __name__=='__main__':main()
