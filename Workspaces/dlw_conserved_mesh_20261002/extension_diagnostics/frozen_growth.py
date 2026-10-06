"""Frozen field Jacobian probes. These do not prove nonlinear stability."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvals
from scipy.sparse.linalg import LinearOperator,eigs

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('ex', HERE.parent/'experiment.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)

def main():
    out=[]
    for nx in (33,65):
        _,D=e.derivative_matrix(nx)
        val=eigvals((D@D)[1:-1,1:-1])
        for model in ('SD','FD'):
            s=dict(case='A',model=model,mesh='fixed',motion='fixed',nx=nx,h=.125,dt=2.5e-5,T=.01,variant='spectrum')
            p=e.Problem(s);z=p.initial();n=p.np+p.nq
            calls=0
            def mv(v):
                nonlocal calls
                calls+=1
                vv=np.r_[v,np.zeros(nx-2)]
                eps=1e-5/max(1.,np.linalg.norm(v))
                return (p.rhs(0.,z+eps*vv)[:n]-p.rhs(0.,z-eps*vv)[:n])/(2*eps)
            L=LinearOperator((n,n),matvec=mv,dtype=float)
            lam,vec=eigs(L,k=4,which='LR',tol=3e-6,maxiter=2000,ncv=50)
            residuals=[float(np.linalg.norm(L@vec[:,j].real-lam[j].real*vec[:,j].real+lam[j].imag*vec[:,j].imag)/np.linalg.norm(vec[:,j])) for j in range(4)]
            row=dict(nx=nx,model=model,d2_min_real=float(val.real.min()),d2_max_abs=float(abs(val).max()),
                field_eigenvalues=[dict(real=float(x.real),imag=float(x.imag)) for x in lam],
                real_part_residuals=residuals,jvp_calls=calls,
                caveat='Frozen initial Jacobian at fixed mesh; real-part residual is not a nonlinear bound.')
            out.append(row);print(json.dumps(row),flush=True)
    (HERE/'growth.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
