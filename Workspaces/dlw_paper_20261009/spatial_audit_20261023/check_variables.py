"""Compare new physical-field integrator to frozen auxiliary-variable solver.
Both use the identical Fourier grid and ghost rule for this controlled check.
"""
from run import *
from scipy.sparse import coo_matrix
exec(compile(SOURCE.read_text(encoding='utf8'),str(SOURCE),'exec'))
from run import step as uvstep
out={}
for kind,cls in [('Centered-SD',SDModel),('FD',FDModel)]:
    m=Model('A',kind,dx=.2)
    cfg=case_config('A');cfg['nx']=m.nx
    old=cls('A',kind,cfg);old.X=m
    z=m.initial();q=old.initial();f=m.rhs(0,z);oq=old.rhs(0,q);pp,ww=old.unpack(oq)
    b,bt=m.boundary(0)
    expected=f[1]-m.centered(f[0],bt) if kind=='Centered-SD' else f[1]
    rhsdiff=max(float(abs(np.diff(f[0],axis=0)/m.h-pp).max()),float(abs(expected-ww).max()))
    for i in range(100):
        z=uvstep(m,i*.0001,z,.0001)
        q=step(old.rhs,i*.0001,q,.0001,'RK4')
    fields=np.array(old.fields(q,.01))
    diff=[float(abs(z[j]-fields[j]).max()) for j in range(2)]
    out[kind]=dict(rhs_transform_difference=rhsdiff,final_field_difference=diff)
    assert rhsdiff<1e-9 and max(diff)<1e-8,out
(HERE/'variable_validation.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
