"""Common physical-field evaluation of LDG and FD; no PDE reruns."""
import sys,json,csv
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import CubicSpline
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(ROOT))
from mch.ldg import LDG
from mch.exact import profile


def records():
    result=[]
    for p in sorted((HERE/'results').glob('*/manifest.json')):
        for entry in json.loads(p.read_text(encoding='utf-8')):
            if 'smoke_' in entry['id']:continue
            path=Path(entry['path']);s=json.loads((path/'summary.json').read_text(encoding='utf-8'))
            result.append(dict(entry,config=s['config'],summary=s))
    # Reuse the previous verified N640 half-time-step LDG runs.
    for p in sorted((ROOT/'results').glob('suite_timecheck_*.json'))[-1:]:
        for entry in json.loads(p.read_text(encoding='utf-8')):
            path=ROOT/entry['path'];s=json.loads((path/'summary.json').read_text(encoding='utf-8'))
            result.append(dict(kind='LDG',path=str(path),id='reused_'+path.name,config=s['config'],summary=s))
    return result


def label(r):
    c=r['config']
    if r['kind']=='LDG':return 'LDG-c' if c['flux']=='conservative' else 'LDG-d'
    if c.get('variant')=='rusanov':return 'FD-Rusanov'
    return f"FD{c['order']}"+(' half-cell' if c['offset']==.5 else ' aligned')


def evaluator(r,state):
    c=r['config']
    if r['kind']=='LDG':
        d=LDG(**{k:c[k] for k in ['n','k','left','right','kappa','flux']})
        return lambda x:d.sample(state,x)
    z=np.load(Path(r['path'])/'trajectory.npz');x=z['x'];L=c['right']-c['left']
    cs=CubicSpline(np.r_[x,x[0]+L],np.r_[state,state[0]],bc_type='periodic')
    return lambda xx:cs(x[0]+(np.asarray(xx)-x[0])%L)


def metric(r,state,t,ncells=10240,nsamples=80000):
    c=r['config'];left,right=c['left'],c['right'];L=right-left
    sample=evaluator(r,state)
    z,w=leggauss(4);dx=L/ncells
    xq=left+(np.arange(ncells)[:,None]+.5)*dx+.5*dx*z
    exact=lambda xx:profile(c['case'],xx,t,alpha=c.get('alpha',.5),kappa=c['kappa'])[0]
    eq=sample(xq)-exact(xq)
    l2=np.sqrt(dx/2*np.sum(eq*eq*w))
    xe=t if c['case']=='5.4' else .5*np.log((1+c['alpha'])/(1-c['alpha']))/c['alpha']+(1+2/(1-c['alpha']**2))*t
    xx=np.unique(np.r_[np.linspace(left,right,nsamples,endpoint=False),xe])
    if r['kind']=='LDG':
        edges=left+np.arange(c['n']+1)*L/c['n'];eps=1e-10*L/c['n']
        xx=np.unique(np.r_[xx,edges[:-1]+eps,edges[1:]-eps])
    uu=sample(xx);ee=uu-exact(xx);idx=int(np.argmax(uu))
    exact_peak=float(exact(np.array([xe]))[0])
    return dict(l2_u=float(l2),sampled_linf_u=float(max(abs(ee))),peak_x=float(xx[idx]),peak_position_error=float(xx[idx]-xe),
                peak_height=float(uu[idx]),peak_height_error=float(uu[idx]-exact_peak),quadrature_intervals=ncells,sample_count=len(xx))


def analyze():
    rows=[];evaluation_controls=[]
    out=HERE/'analysis';out.mkdir(exist_ok=True)
    previous=json.loads((out/'comparison.json').read_text(encoding='utf-8')) if (out/'comparison.json').exists() else {}
    cache={(r['path'],r['t']):r for r in previous.get('rows',[])}
    control_cache={r['id']:r for r in previous.get('evaluation_controls',[])}
    all_records=records()
    for r in all_records:
        c=r['config'];a=np.load(Path(r['path'])/'trajectory.npz');s=r['summary']
        for target in sorted(set([0.,.5,c['T']])):
            i=int(np.argmin(abs(a['t']-target)))
            if abs(a['t'][i]-target)>1e-9:continue
            if (r['path'],target) in cache:
                row=cache[(r['path'],target)]
                m=row
            else:
                m=metric(r,a['u'][i],target)
                row=dict(id=r['id'],path=r['path'],method=label(r),kind=r['kind'],case=c['case'],n=c['n'],dof=c['n']*(c['k']+1 if r['kind']=='LDG' else 1),
                         dt=c['dt'],t=target,T=c['T'],completed=s['completed'],reached=s['reached'],**m)
            rows.append(row)
            # Independently tighten common evaluation for final, largest-state controls.
            if target==c['T'] and row['dof']>=1280:
                if r['id'] in control_cache:evaluation_controls.append(control_cache[r['id']])
                else:
                    mm=metric(r,a['u'][i],target,ncells=20480,nsamples=160000)
                    evaluation_controls.append(dict(id=r['id'],l2_relative_difference=abs(mm['l2_u']-m['l2_u'])/max(m['l2_u'],1e-30),linf_absolute_difference=abs(mm['sampled_linf_u']-m['sampled_linf_u'])))
    results=dict(run_count=len(all_records),completed=sum(r['summary']['completed'] for r in all_records),rows=rows,evaluation_controls=evaluation_controls,
                 failures=[dict(id=r['id'],method=label(r),case=r['config']['case'],n=r['config']['n'],dt=r['config']['dt'],reached=r['summary']['reached'],last_diagnostic_time=r['summary'].get('last_diagnostic_time',r['summary']['final']['t'])) for r in all_records if not r['summary']['completed']])
    (out/'comparison.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    with (out/'physical_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps(dict(runs=results['run_count'],completed=results['completed'],metrics=len(rows),evaluation_l2_relative_max=max([v['l2_relative_difference'] for v in evaluation_controls] or [0]),evaluation_linf_absolute_max=max([v['linf_absolute_difference'] for v in evaluation_controls] or [0])),indent=2))
    return results

if __name__=='__main__':analyze()
