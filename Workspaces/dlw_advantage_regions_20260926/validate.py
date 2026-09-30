from error_model import ErrorModel,Parameters,norm
from scan import HERE,dump
import numpy as np
checks={};rng=np.random.default_rng(9538)
for route,c,k in [('fd',0,0),('sd',0,0),('sd',.04248652711,.00844851896)]:
    m=ErrorModel(Parameters(),nx=64,route=route,c=c,kappa=k)
    z=m.exact(.004)+rng.normal(0,1e-4,m.exact(.004).shape)
    e=rng.normal(0,1e-3,z.shape)
    defect=norm(m.rhs(.004,z+e)-m.rhs(.004,z)-m.jac(.004,z,e)-m.quadratic(e))
    assert defect<3e-11,defect
    checks[f'{route}_{c}_quadratic_identity']=defect
    eps=1e-5
    jdefect=norm((m.rhs(.004,z+eps*e)-m.rhs(.004,z-eps*e))/(2*eps)-m.jac(.004,z,e))
    assert jdefect<2e-7,jdefect
    checks[f'{route}_{c}_jacobian_difference']=jdefect
# At fixed y data, replacing x derivatives by analytic derivatives should be
# approached at fourth order, away from periodized far tails.
for route in ('fd','sd'):
    es=[]
    for nx in (128,256,512):
        m=ErrorModel(Parameters(),nx=nx,route=route)
        p,v=m.unpack(m.rhs(0,m.exact(0))-m.analytic_x_rhs(0))
        es.append(max(norm(p[:,abs(m.X.x)<7]),norm(v[:,abs(m.X.x)<7])))
    order=float(np.log2(es[-2]/es[-1]));assert 3.7<order<4.4,order
    checks[route+'_analytic_x_convergence']={'errors':es,'last_order':order}
dump(HERE/'validation.json',checks)
print('8 analytic/Jacobian checks passed')

