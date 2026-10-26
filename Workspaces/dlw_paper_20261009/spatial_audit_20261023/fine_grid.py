"""Memory-bounded classical RK4 for dx=h=.01; identical equations/closures.
Four reusable on-disk work arrays. Only y batching is changed.
"""
from run import *
import gc
from scipy import fft as threaded_fft
BLOCK=128
OUT=HERE/'fine_dx001'
OUT.mkdir(exist_ok=True)

class FastModel(Model):
    def d1(self,f):return threaded_fft.irfft(threaded_fft.rfft(f,axis=-1,workers=4)*self.m1,n=self.nx,axis=-1,workers=4)
    def d2(self,f):return threaded_fft.irfft(threaded_fft.rfft(f,axis=-1,workers=4)*self.m2,n=self.nx,axis=-1,workers=4)

def rhs(m,t,z,out,block=BLOCK):
    n=len(m.y);h=m.h;a=m.a;b,bt=m.boundary(t)
    right=b[-1]+3*(z[0,-1]-b[-2])-3*(z[0,-2]-b[-3])+(z[0,-3]-b[-4])
    def uv(i):
        ans=np.array(z[0,np.clip(i,0,n-1)])
        ans[i<0]=b[0];ans[i>=n]=right
        return ans
    def w(i):return np.array(z[1,i])-(uv(i+1)-uv(i-1))/(2*h)
    out[0,0]=bt[1];carry=np.zeros(m.nx)
    for s in range(1,n,block):
        i=np.arange(s,min(s+block,n));u=uv(i);prev=uv(i-1);p=(u-prev)/h
        if m.method=='Centered-SD':
            ww=w(i);wp=w(i-1)
            flux=u*u/2+2*a*u+h*h*(ww*ww/32-ww/4)
            fp=prev*prev/2+2*a*prev+h*h*(wp*wp/32-wp/4)
            # Difference of separately differentiated nodal fluxes, as in original.
            r=-(m.d1(flux)-m.d1(fp))/h-m.d2(p+(ww+wp)/2)
        else:
            r=-(m.d1(u*u/2+2*a*u)-m.d1(prev*prev/2+2*a*prev))/h
            r-=m.d2(z[1,i] if m.method=='Endpoint-SD' else (z[1,i]+z[1,i-1])/2)
        summed=np.cumsum(r,axis=0)+carry
        out[0,i]=bt[1]+h*summed;carry=summed[-1].copy()
    rt=bt[-1]+3*(out[0,-1]-bt[-2])-3*(out[0,-2]-bt[-3])+(out[0,-3]-bt[-4])
    for s in range(0,n,block):
        i=np.arange(s,min(s+block,n));u=uv(i);v=np.array(z[1,i])
        if m.method=='Centered-SD':
            ww=w(i)
            lo=np.array(out[0,np.maximum(i-1,0)]);hi=np.array(out[0,np.minimum(i+1,n-1)])
            lo[i==0]=bt[0];hi[i==n-1]=rt
            out[1,i]=-m.d1((u+2*a)*ww-4*u)+m.d2(ww)+(hi-lo)/(2*h)
        elif m.method=='FD':out[1,i]=-m.d1((u+2*a)*v-4*u)-m.d2((uv(i+1)-uv(i-1))/(2*h))
        else:
            prev=uv(i-1);avg=(u+prev)/2;p=(u-prev)/h
            out[1,i]=-m.d1((avg+2*a-2*h)*v+h*v*v/4-4*avg-h*p*p/4)-m.d2(p)

def advance(m,t,z,tmp,k,acc,dt):
    n=len(m.y)
    for stage,weight,offset in ((0,1,0),(1,2,.5),(2,2,.5),(3,1,1)):
        rhs(m,t+offset*dt,z if stage==0 else tmp,k)
        for s in range(0,n,BLOCK):
            sl=slice(s,min(s+BLOCK,n));kk=np.array(k[:,sl])
            if stage==0:acc[:,sl]=kk
            else:acc[:,sl]+=weight*kk
            if stage<3:tmp[:,sl]=z[:,sl]+dt*(.5 if stage<2 else 1)*kk
            else:z[:,sl]+=dt/6*acc[:,sl]
    peak=0.
    for s in range(0,n,BLOCK):
        zz=np.array(z[:,s:s+BLOCK])
        if not np.isfinite(zz).all():return float('inf')
        peak=max(peak,float(abs(zz).max()))
    return peak

def validate():
    checks={}
    for method in ('Endpoint-SD','Centered-SD','FD'):
        m=FastModel('A',method,.2,.1);original=Model('A',method,.2,.1);z=m.initial();kk=np.empty_like(z)
        rhs(m,0,z,kk,block=17)
        er=float(abs(kk-original.rhs(0,z)).max())
        ref=step(original,0,z,.0001);advance(m,0,z,np.empty_like(z),kk,np.empty_like(z),.0001)
        es=float(abs(ref-z).max());checks[method]=dict(rhs_difference=er,rk4_difference=es)
        assert er<1e-9 and es<1e-11,checks
    (OUT/'blocked_validation.json').write_text(json.dumps(checks,indent=2));print(checks,flush=True)

def solve(case,method,dt=.0001):
    name=f'{case}_{method}_dt{dt:g}'
    dest=OUT/(name+'.json')
    if dest.exists():return
    start=time.time();m=FastModel(case,method,.01,.01);shape=(2,len(m.y),m.nx)
    arrays=[np.memmap(OUT/f'scratch_{label}.dat',dtype='float64',mode='w+',shape=shape) for label in ('state','temporary','rhs','sum')]
    z,tmp,k,acc=arrays
    for s in range(0,len(m.y),BLOCK):
        sl=slice(s,min(s+BLOCK,len(m.y)))
        z[0,sl]=m.profile(m.y[sl])[0];z[1,sl]=m.profile(m.yv[sl])[1]
        if m.G is not None:m.G._cache={}
    initial_peak=max(float(abs(z[:,s:s+BLOCK]).max()) for s in range(0,len(m.y),BLOCK))
    history=[];failed=None
    with np.errstate(over='ignore',invalid='ignore'):
        for j in range(round(.01/dt)):
            peak=advance(m,j*dt,z,tmp,k,acc,dt)
            history.append(dict(t=(j+1)*dt,max_abs=peak if np.isfinite(peak) else None))
            print(case,method,'step',j+1,'peak',peak,'seconds',round(time.time()-start,1),flush=True)
            if not np.isfinite(peak) or peak>1e6:
                failed=(j+1)*dt;break
    rec=dict(case=case,method=method,dx=.01,h=.01,dt=dt,target_T=.01,failed_at=failed,ny=len(m.y),nx=m.nx,initial_peak=initial_peak,history=history,seconds=time.time()-start,fft_backend='scipy.fft workers=4',y_block=BLOCK)
    if failed is None:
        # Preserve full successful fields for subsequent reference/error evaluation.
        np.savez_compressed(OUT/(name+'.npz'),z=z,x=m.x,y=m.y,yv=m.yv)
    else:
        inds=np.unique(np.linspace(0,len(m.y)-1,9,dtype=int))
        np.savez_compressed(OUT/(name+'_failed_slices.npz'),z=z[:,inds],x=m.x,y=m.y[inds],yv=m.yv[inds])
    dest.write_text(json.dumps(rec,indent=2),encoding='utf8')
    for ar in arrays:ar.flush()
    print('DONE',name,failed,flush=True)

if __name__=='__main__':
    if len(sys.argv)==1:validate()
    else:
        for c in sys.argv[1:]:
            for method in ('Endpoint-SD','Centered-SD','FD'):
                solve(c,method);gc.collect()
