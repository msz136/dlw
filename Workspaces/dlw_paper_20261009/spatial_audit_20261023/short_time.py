"""Common T=.01 protocol; nonexact common FD y-refined numerical reference."""
from run import *

def solve(case,method,tag,h=.1,dt=.0001,a=None):
    stem=HERE/f'{case}_{method}_short_{tag}'
    if stem.with_suffix('.json').exists():return
    m=Model(case,method,.1,h)
    if a is not None:m.a=a
    z=m.initial();start=time.time()
    for i in range(round(.01/dt)):
        z=step(m,i*dt,z,dt)
        if not np.isfinite(z).all() or abs(z).max()>1e6:raise ValueError((case,method,tag,i))
    np.savez_compressed(stem.with_suffix('.npz'),z=z,x=m.x,y=m.y,yv=m.yv)
    rec=dict(case=case,method=method,tag=tag,dx=.1,h=h,dt=dt,T=.01,a=m.a,seconds=time.time()-start)
    stem.with_suffix('.json').write_text(json.dumps(rec,indent=2))
    print(rec,flush=True)

if __name__=='__main__':
    c=sys.argv[1]
    for m in ('Endpoint-SD','Centered-SD','FD'):
        solve(c,m,'main');solve(c,m,'halfdt',dt=.00005)
    solve(c,'FD','ref4',h=.025,dt=.00005)
    solve(c,'FD','ref8',h=.0125,dt=.00005)
