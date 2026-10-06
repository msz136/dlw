from pathlib import Path
import numpy as np, json
M=3; NX=64;T=.02;h=.125;c=-4.;gamma=-16.;beta=h*h/32
x=2*np.pi*np.arange(NX)/NX;k=np.fft.fftfreq(NX,1/NX)
R=h*(np.sign(np.arange(M)[:,None]-np.arange(M)[None,:])/2-(np.arange(M)[:,None]-np.arange(M)[None,:])/M)
def project(z):return z-z.mean(axis=-2,keepdims=True)
def rr(z):return np.einsum('ij,...jx->...ix',R,z)
def dx(z):return np.fft.ifft(1j*k*np.fft.fft(z,axis=-1),axis=-1).real
AT=project(np.array([.04*np.cos(x)+.015*np.sin(2*x),-.03*np.sin(x),.02*np.cos(2*x)]))
s0=project(np.array([.025*np.sin(x),.035*np.cos(2*x),-.02*np.cos(x)]))
def reconstruct(A,s):
 p=A-rr(s)/2;b=(gamma-(p*s).mean(axis=-2,keepdims=True))/c
 return p,b+p,c+s
def FG(A,s):
 p,U,w=reconstruct(A,s)
 return -project(U*U/2+beta*w*w)-rr(U*w)/2,-project(U*w)
def invariants(A,s):
 p,U,w=reconstruct(A,s);ux=dx(U);wx=dx(w)
 e=U*U*w/2+beta*w**3/3+w*ux+w*rr(wx)/2
 K=h*np.sum((e-gamma*U).mean(axis=-1),axis=-1)*2*np.pi
 Q4=h*np.sum((U**3*w/3+2*beta*U*w**3/3+2*U*w*ux-4*ux*wx/3+U*w*rr(wx)).mean(axis=-1),axis=-1)*2*np.pi
 Mom=h*np.sum((p*s).mean(axis=-1),axis=-1)*2*np.pi
 return K,Q4,Mom
results=[]
for NT in [32,64,128,256]:
 dt=T/NT;times=np.linspace(0,T,NT+1);z=k*k*dt;E=np.exp(-z)
 phi1=np.ones_like(z);phi2=np.ones_like(z)/2
 mask=z!=0;phi1[mask]=-np.expm1(-z[mask])/z[mask];phi2[mask]=(z[mask]+np.expm1(-z[mask]))/z[mask]**2
 w0=dt*(phi1-phi2);w1=dt*phi2
 Ah=np.exp(-(T-times[:,None,None])*k*k)*np.fft.fft(AT)[None,:,:]
 sh=np.exp(-times[:,None,None]*k*k)*np.fft.fft(s0)[None,:,:]
 for it in range(100):
  A=np.fft.ifft(Ah,axis=-1).real;s=np.fft.ifft(sh,axis=-1).real
  F,G=FG(A,s);Fh=np.fft.fft(F,axis=-1);Gh=np.fft.fft(G,axis=-1)
  An=Ah.copy();sn=sh.copy();An[-1]=np.fft.fft(AT);sn[0]=np.fft.fft(s0)
  for n in range(NT):sn[n+1]=E*sn[n]+1j*k*(w0*Gh[n]+w1*Gh[n+1])
  for n in range(NT-1,-1,-1):An[n]=E*An[n+1]-1j*k*(w0*Fh[n+1]+w1*Fh[n])
  err=max(np.max(np.abs(An-Ah)),np.max(np.abs(sn-sh)))/NX;Ah,sh=An,sn
  if err<2e-14:break
 A=np.fft.ifft(Ah,axis=-1).real;s=np.fft.ifft(sh,axis=-1).real
 vals=invariants(A,s);p,U,w=reconstruct(A,s)
 record={'time_steps':NT,'iterations':it+1,'picard_increment':float(err),'K_drift':float(np.ptp(vals[0])),'Q4_drift':float(np.ptp(vals[1])),'momentum_drift':float(np.ptp(vals[2])),'mean_w_error':float(np.max(abs(w.mean(axis=1)-c))),'mean_Uw_error':float(np.max(abs((U*w).mean(axis=1)-gamma)))}
 results.append(record);print(record,flush=True)
open(str(Path(__file__).resolve().parent / 'mixed_time_probe.json'),'w').write(json.dumps(results,indent=2))
