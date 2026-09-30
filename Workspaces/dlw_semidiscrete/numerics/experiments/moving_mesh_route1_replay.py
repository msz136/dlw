"""Replay SD/FD generated x trajectories through both physical field solvers.

The source is coupled to its own current numerical field. Stage coordinates
and velocities are recorded, so a self replay must reproduce the source run.
"""
from pathlib import Path
import sys, json, hashlib, time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
import numpy as np
from moving_mesh import MovingProblem
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import observe, norm


def source_run(pars,model,T=.04,dt=.000125):
    p=MovingProblem(pars,h=.125,nx=128,model=model)
    z,s=p.initial('moving',balanced=False)
    stages=[];n=round(T/dt)
    for i in range(n):
        t=i*dt
        def calc(tt,zz,ss):
            dz,ds=p.rhs(tt,(zz,ss),balanced=False,mesh_mode='moving')
            return dz,ds
        k1,l1=calc(t,z,s)
        s2=s+dt*l1/2;k2,l2=calc(t+dt/2,z+dt*k1/2,s2)
        s3=s+dt*l2/2;k3,l3=calc(t+dt/2,z+dt*k2/2,s3)
        s4=s+dt*l3;k4,l4=calc(t+dt,z+dt*k3,s4)
        stages.append([(s.copy(),l1.copy()),(s2,l2.copy()),
                       (s3,l3.copy()),(s4,l4.copy())])
        z=z+dt*(k1+2*k2+2*k3+k4)/6
        s=s+dt*(l1+2*l2+2*l3+l4)/6
        p.set_s(s)
        if not np.all(np.isfinite(z)) or norm(z)>1e3:
            raise ValueError(f'source {model} diverged at t={t}')
    return stages,s,z,observe(p,z,T,'source',0,0.)


def replay(pars,model,stages,s_final,T=.04,dt=.000125):
    p=MovingProblem(pars,h=.125,nx=128,model=model)
    z,_=p.initial('moving',balanced=False)
    for i,stage in enumerate(stages):
        t=i*dt
        def field(tt,zz,k):
            s,velocity=stage[k]
            p.set_s(s)
            physical=p.m.rhs(tt,zz)
            P,Q=p.m.unpack(zz)
            transport=p.m.pack(p.X.d1(P)*velocity,p.X.d1(Q)*velocity)
            return physical+transport
        k1=field(t,z,0)
        k2=field(t+dt/2,z+dt*k1/2,1)
        k3=field(t+dt/2,z+dt*k2/2,2)
        k4=field(t+dt,z+dt*k3,3)
        z=z+dt*(k1+2*k2+2*k3+k4)/6
    p.set_s(s_final)
    return z,observe(p,z,T,'replay',0,0.)


def main():
    result={'scope':{'cases':['P1','P7'],'T':.04,'dt':.000125,'nx':128,
                     'self_replay_check':'max state difference',
                     'reference':'finite-h exact one-soliton'},'runs':[]}
    for index in (0,6):
        pars=ALL[index]
        mesh_paths={}
        for source in ('structure','fd'):
            begin=time.perf_counter()
            stages,s_final,z_source,source_ob=source_run(pars,source)
            mesh_paths[source]=(stages,s_final)
            row={'parameter_id':f'P{index+1}','source_model':source,
                 'source_observation':source_ob,'targets':{},
                 'seconds_source':time.perf_counter()-begin}
            for target in ('structure','fd'):
                z,ob=replay(pars,target,stages,s_final)
                row['targets'][target]={'observation':ob,
                   'self_replay_state_difference':norm(z-z_source) if target==source else None}
            result['runs'].append(row)
            print(f'P{index+1} {source} self replay: '
                  f'{row["targets"][source]["self_replay_state_difference"]:.3e}',flush=True)
        a,af=mesh_paths['structure'];b,bf=mesh_paths['fd']
        result.setdefault('trajectory_differences',[]).append({
            'parameter_id':f'P{index+1}',
            'maximum_stage_node_difference':max(norm(x[k][0]-y[k][0])
                                                 for x,y in zip(a,b) for k in range(4)),
            'final_node_difference':norm(af-bf)})
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in paths}
    (ROOT/'out'/'moving_mesh'/'route1_replay.json').write_text(
        json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
