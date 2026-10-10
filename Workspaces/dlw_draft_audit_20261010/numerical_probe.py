from pathlib import Path
import re,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
path=ROOT/'notebook/DLW数值分析report.ipynb'
nb=json.loads(path.read_text(encoding='utf-8'))
ns={}
# Load only definitions and configuration, never execute experiment or figure cells.
for i in (1,3,5,7,8,10,12,13,15,17,19):
    cell=nb['cells'][i]
    assert cell['cell_type']=='code',(i,cell['cell_type'])
    source=''.join(cell['source']).replace('from IPython.display import display','')
    exec(compile(source,f'{path.name}:cell{i}','exec'),ns)
records=[]
for case in ('A','B','C'):
    for model in ('SD','SD2','FD'):
        p=ns['Problem'](case,model,'fixed',dict(ns['CONFIG']))
        state=p.initial(); u,v=p.fields(state,0.)
        rhs=p.stage(0.,state)
        uref,vref=p.m.G.uv(p.m.js,p.X.x,0.)
        rec={'case':case,'model':model,'initial_u_error':float(abs(u-uref).max()),
             'initial_v_error':float(abs(v-vref).max())}
        if model=='SD2':
            Q,R=p.m.unpack(state[:-p.X.n],0.)
            rec.update(Q_min=float(Q.min()),jump_min=float(np.min(p.m.jump)),jump_max=float(np.max(p.m.jump)),
                       periodic_lift_residual=float(abs(p.m.D@Q[0]-.5*uref[0]*Q[0]).max()),
                       augmented_lift_residual=float(abs(p.m.D@Q[0]+p.m.b*p.m.jump[0]-.5*uref[0]*Q[0]).max()))
        if model=='SD':
            P,W=p.m.unpack(state[:-p.X.n]); Pt,Wt=p.m.unpack(rhs[:-p.X.n])
            rho=1-W/4
            flux=(u+2*p.m.a)*rho-p.X.d1(rho)-2*p.m.a
            defect=-Wt/4+p.X.d1(flux)
            predicted=p.X.d2(rho)-p.X.d1(p.X.d1(rho))
            rec.update(nodal_continuity_defect=float(abs(defect).max()),
                       defect_formula_error=float(abs(defect-predicted).max()),
                       periodic_mass_derivative=float(abs(np.sum(-Wt/4,axis=1)).max()))
        records.append(rec)
# Scalar demonstration of fixed tolerance accepting the Euler predictor.
z=np.array([1.]);dt=1e-6
out=ns['step'](lambda t,z:z,0.,z,dt,'CN')
cn_demo={'dt':dt,'returned':float(out[0]),'Euler':float(1+dt),
         'exact_CN':float((1+dt/2)/(1-dt/2)),'solver':ns['step'].cn_last}
result={'notebook_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'definition_cells':[1,3,5,7,8,10,12,13,15,17,19],'records':records,'CN_tolerance_demo':cn_demo,
        'new_PDE_trajectories':0}
(HERE/'numerical_probe.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
