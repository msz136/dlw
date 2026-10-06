"""Two frozen conserved-density interventions, same long-time DLW solver."""
from pathlib import Path
import argparse, json, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import baseline

HERE=Path(__file__).resolve().parent
OUT=HERE/'candidate_out'

class CandidateProblem(baseline.Problem):
    def initial(self):
        fine=np.linspace(-1,1,20001)
        u,v=self.G.uv(self.y,fine,0)
        R0=self.monitor_weights @ (1-v[1:-1]/4)
        den=R0-1 if self.spec['mesh']=='mass' else 1+4*(R0-1)
        if den.min()<=0:raise ValueError('new initial density nonpositive')
        mass=np.r_[0,np.cumsum(.5*(den[1:]+den[:-1])*np.diff(fine))]
        x=np.interp(np.linspace(0,mass[-1],self.X.n),mass,fine)
        x[0],x[-1]=-1,1
        self.X.set_x(x)
        u,v=self.G.uv(self.y,x,0)
        gh=self.G.uv([self.y[0]-self.h,self.y[-1]+self.h],x,0)[0]
        P=np.diff(u,axis=0)/self.h
        Q=v-self.dy(u,gh) if self.model=='SD' else v
        return self.pack(P,Q,x)

    def density_flux(self,P,Q,u,v,du,name=None):
        R0,F0=super().density_flux(P,Q,u,v,du,name='zero')
        if self.spec['mesh']=='mass':return R0-1,F0
        if self.spec['mesh']=='strong':return 1+4*(R0-1),4*F0
        raise ValueError('unknown conserved density')

def main_specs():
    return [dict(case=case,model=model,mesh=mesh,motion=motion,variant='main',nx=33,h=.125,dt=2.5e-5,T=.01)
        for case in baseline.CASES for model in ['SD','FD'] for mesh in ['mass','strong'] for motion in ['moving','frozen']]

def control_specs():
    result=[]
    for s in main_specs():
        if s['motion']=='frozen':continue
        for variant in ['time_half','x_half','y_half','combined']:
            r=dict(s,variant=variant)
            if variant in ['time_half','x_half','combined']:r['dt']/=2
            if variant in ['x_half','combined']:r['nx']=65
            if variant in ['y_half','combined']:r['h']/=2
            result.append(r)
    return result

def one(s):
    baseline.OUT=OUT;baseline.Problem=CandidateProblem
    r=baseline.one(s)
    r['candidate_sha256']=baseline.sha(__file__)
    r['base_source_sha256']=baseline.sha(HERE/'baseline.py')
    baseline.dump(OUT/(baseline.spec_key(s)+'.json'),r)
    return r

def consolidate():
    runs=[]
    for p in sorted(OUT.glob('*.json')):
        if p.name=='results.json':continue
        r=json.loads(p.read_text(encoding='utf-8'))
        if 'spec' not in r:continue
        assert r['candidate_sha256']==baseline.sha(__file__) and r['base_source_sha256']==baseline.sha(HERE/'baseline.py')
        assert r['profile_sha256']==baseline.sha(r['profile'])
        runs.append(r)
    baseline.dump(OUT/'results.json',dict(runs=runs,expected_plan=main_specs()+control_specs(),
        parameters=baseline.CASES,times=baseline.TIMES,candidate_sha256=baseline.sha(__file__),base_source_sha256=baseline.sha(HERE/'baseline.py')))
    return runs

def main():
    a=argparse.ArgumentParser();a.add_argument('--workers',type=int,default=2);args=a.parse_args()
    OUT.mkdir(exist_ok=True)
    specs=main_specs()+control_specs();todo=[]
    for s in specs:
        p=OUT/(baseline.spec_key(s)+'.json')
        if p.exists():
            r=json.loads(p.read_text(encoding='utf-8'))
            assert r['spec']==s and r['candidate_sha256']==baseline.sha(__file__) and r['base_source_sha256']==baseline.sha(HERE/'baseline.py')
        else:todo.append(s)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        tasks=[pool.submit(one,s) for s in todo]
        for task in as_completed(tasks):
            r=task.result();print(baseline.spec_key(r['spec']),r['status'],r['reached'],r['history'][-1]['errors'],flush=True)
    print('SAVED',len(consolidate()),'of',len(specs),flush=True)

if __name__=='__main__':main()
