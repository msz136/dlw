"""Analyze saved trajectories only; no PDE integrations or parameter fitting."""
import csv,json
from pathlib import Path
import numpy as np
from mch.ldg import LDG


def load_index(pattern):
    files=sorted(Path('results').glob(pattern))
    if not files:return []
    out=[]
    for r in json.loads(files[-1].read_text(encoding='utf-8')):
        p=Path(r['path']);s=json.loads((p/'summary.json').read_text(encoding='utf-8'));s['path']=str(p);out.append(s)
    return out


def distance(a,b):
    c=a['config'];d=LDG(**{k:c[k] for k in ['n','k','left','right','kappa','flux']})
    ua=np.load(Path(a['path'])/'trajectory.npz')['u'][-1]
    ub=np.load(Path(b['path'])/'trajectory.npz')['u'][-1]
    return np.sqrt(d.energy(ua-ub))


def analyze():
    allrows=[]
    for p in sorted(Path('results').glob('*/summary.json')):
        s=json.loads(p.read_text());c=s['config'];f=s['final']
        allrows.append(dict(path=str(p.parent),case=c['case'],flux=c['flux'],k=c['k'],n=c['n'],left=c['left'],right=c['right'],dt=c['dt'],T=c['T'],projection=c['projection'],boundary=c['boundary'],completed=s['completed'],reached=s['reached'],diagnostic_time=f['t'],energy_error=f['energy_error'],l2_u=f['l2_u'],l2_r=f['l2_r'],energy_loss=f['energy_loss'],norm_loss=np.sqrt(s['initial']['energy'])-np.sqrt(f['energy']),mass_drift=f['mass_drift'],wall_seconds=s['wall_seconds']))
    with open('results/all_runs.csv','w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
    orders=[]
    for name,pattern in [('baseline','suite_smooth_*.json'),('expanded','control_domain_*.json')]:
        rows=load_index(pattern)
        for k in (1,2,3):
            for flux in ('conservative','dissipative'):
                rr=sorted([r for r in rows if r['config']['k']==k and r['config']['flux']==flux],key=lambda r:r['config']['n'])
                for a,b in zip(rr[:-1],rr[1:]):
                    orders.append(dict(group=name,k=k,flux=flux,n0=a['config']['n'],n1=b['config']['n'],error0=a['final']['energy_error'],error1=b['final']['energy_error'],order=np.log2(a['final']['energy_error']/b['final']['energy_error'])))
    comparisons=[]
    base=load_index('suite_peakon_*.json')
    for label,pattern in [('half_dt','suite_timecheck_*.json'),('dirichlet','alignment_boundary_*.json'),('l2_initial','alignment_initialization_*.json')]:
        for a in base:
            bb=[b for b in load_index(pattern) if b['config']['case']=='5.4' and b['config']['flux']==a['config']['flux']]
            if bb:
                b=bb[0]
                comparisons.append(dict(control=label,flux=a['config']['flux'],state_energy_distance=float(distance(a,b)),energy_loss0=a['final']['energy_loss'],energy_loss1=b['final']['energy_loss'],path0=a['path'],path1=b['path']))
    rk=sorted(load_index('control_rk4_*.json'),key=lambda r:-r['config']['dt'])
    diffs=[float(distance(a,b)) for a,b in zip(rk[:-1],rk[1:])]
    timeorders=[float(np.log2(a/b)) for a,b in zip(diffs[:-1],diffs[1:])]
    paper=np.loadtxt('search/figure3_dissipative_digitized.csv',delimiter=',',skiprows=1)
    a=next(r for r in base if r['config']['flux']=='dissipative')
    hist=json.loads((Path(a['path'])/'history.json').read_text());tt=np.array([r['t'] for r in hist]);E=np.array([r['energy'] for r in hist]);nn=np.sqrt(E[0])-np.sqrt(E)
    mask=(tt>=paper[0,0])&(tt<=paper[-1,0]);paper_y=np.interp(tt[mask],paper[:,0],paper[:,1])
    result=dict(total_runs=len(allrows),completed_runs=sum(r['completed'] for r in allrows),failed_runs=[r for r in allrows if not r['completed']],orders=orders,controls=comparisons,
                rk4=dict(differences=diffs,observed_orders=timeorders),
                figure3_metric_hypothesis=dict(our_energy_loss=float(E[0]-E[-1]),our_norm_loss=float(nn[-1]),paper_last_time=float(paper[-1,0]),paper_last_ordinate=float(paper[-1,1]),norm_curve_max_difference=float(max(abs(nn[mask]-paper_y))),caveat='Similarity supports a metric hypothesis, not confirmation of authors implementation.'))
    Path('results/analysis.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['orders','failed_runs']},indent=2))
    return result

if __name__=='__main__':analyze()
