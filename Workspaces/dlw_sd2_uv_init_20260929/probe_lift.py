import sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,bmat,csc_matrix,diags
from scipy.sparse.linalg import splu
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'dlw_two_soliton_20260929'))
from models import Problem
from reference import CASES

def matrices(X):
    n=X.n;ii=np.arange(n)
    d=coo_matrix((np.concatenate([np.full(n,c/(12*X.dx)) for c in (1,-8,8,-1)]),(np.tile(ii,4),np.concatenate([(ii+k)%n for k in (-2,-1,1,2)]))),shape=(n,n)).tocsc()
    b=np.zeros(n);b[:2]=[7,-1];b[-2:]=[-1,7];b/=12*X.dx
    return d,b

def lift(X,u):
    d,b=matrices(X);n=X.n
    A=bmat([[d-diags(.5*X.J*u),csc_matrix(b[:,None])],[csc_matrix(([1.],([0],[0])),shape=(1,n)),csc_matrix((1,1))]],format='csc')
    rhs=np.r_[np.zeros(n),1.];lu=splu(A);sol=lu.solve(rhs)
    q,jump=sol[:-1],sol[-1]
    return q,jump,float(abs(2*(d@q+b*jump)/X.J/q-u).max())

def main():
    for name in CASES:
        for mesh in ('fixed','moving'):
            s=dict(case=name,model='SD2',mesh=mesh,nx=1024 if name=='fig5' else 256,L=640. if name=='fig5' else 40.,h=.125)
            p=Problem(s);p.initial();u,v=p.m.G.uv(p.m.js,p.X.x,0.)
            qq,jj,ee=zip(*(lift(p.X,uu) for uu in u))
            qq=np.array(qq);analytic=p.m.G.qr(p.m.js,p.X.x,0.)[0]
            print(name,mesh,'err',max(ee),'minQ',qq.min(),'analytic_difference',abs(qq-analytic).max(),'jumps',min(jj),max(jj),flush=True)

if __name__=='__main__':main()
