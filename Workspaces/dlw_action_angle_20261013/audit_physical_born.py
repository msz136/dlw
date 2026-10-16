"""Independent numerical path: raw chi connection and original q,d bracket.

No reciprocal-field, norming-bracket or vector-frame formula is used to compute
the left side. Finite numerical evidence, not an all-M analytic certificate.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

L=2*np.pi
rows=[]
for M in (2,3,4,5):
    m=M-1; delta=1/(512*M**3); S=M*delta
    sign=np.sign(np.arange(M)[None,:]-np.arange(M)[:,None])
    P=np.ones((M,M))/M
    eye=np.eye(M)
    Hj=[np.diag(eye[j])-eye/M for j in range(m)]
    labels=[]
    for n in (-5,-2,-1,1,2,5):
        for ell in range(1,M):
            slow=ell-1 if n>0 else ell
            fast=M-1 if n>0 else 0
            center=n-delta/np.tan(np.pi*ell/M)
            def eig(t):return np.linalg.eigh(t*P-1j*delta*sign)
            def collision(t):
                e,_=eig(t);return e[fast]-e[slow]-n
            width=delta/2
            t=brentq(collision,center-width,center+width,xtol=1e-14,rtol=1e-14)
            e,V=eig(t);ef=V[:,fast];es=V[:,slow]
            lam=1j*t
            K=[np.outer(eye[j],lam/S+sign[j]) for j in range(M)]
            # Delta_first=q+S+sign_first*d_first. The sign matrix here is m x m.
            Gd=[K[j]-K[m]+sum((sign[i,j]*Hj[i] for i in range(m)),start=np.zeros((M,M),complex)) for j in range(m)]
            Cp=np.outer(es,ef.conj());Cm=np.outer(ef,es.conj())
            coeff=[]
            for C in (Cp,Cm):
                coeff.append((np.array([np.trace(C@H) for H in Hj]),np.array([np.trace(C@G) for G in Gd])))
            gamma=float(np.real(ef.conj()@P@ef-es.conj()@P@es))
            omega=(S*S+t*t)/(16*S)
            labels.append(dict(n=n,ell=ell,t=t,coeff=coeff,expected=omega*gamma/L,
                               root_error=abs(e[fast]-e[slow]-n)))
    worst=0.;count=0
    for i,A in enumerate(labels):
        for j,B in enumerate(labels):
            for si in (0,1):
                for sj in (0,1):
                    phase_a=(-1 if si==0 else 1)*A['n']
                    phase_b=(-1 if sj==0 else 1)*B['n']
                    if phase_a+phase_b:continue
                    aq,ad=A['coeff'][si];bq,bd=B['coeff'][sj]
                    actual=-1j*phase_b/(16*L)*(aq@bd+ad@bq)
                    target=A['expected']*(1 if si==0 else -1) if i==j and si!=sj else 0
                    scale=np.sqrt(abs(A['expected']*B['expected']))
                    worst=max(worst,float(abs(actual-target)/scale));count+=1
    conditions=[]
    for n in (1,2,5):
        block=[a for a in labels if a['n']==n]
        mat=[]
        for a in block:
            q,d=a['coeff'][0];mat.append(np.r_[q,d*1j*S/n])
        for a in block:
            q,d=a['coeff'][1];mat.append(np.r_[q.conj(),d.conj()*1j*S/n])
        conditions.append(float(np.linalg.cond(np.array(mat))))
    rows.append({'M':M,'delta':delta,'signed_collision_labels':len(labels),
                 'nontrivial_bracket_comparisons':count,'max_scaled_bracket_error':worst,
                 'max_collision_residual':max(a['root_error'] for a in labels),
                 'positive_balanced_Born_condition_numbers':conditions})
assert max(r['max_scaled_bracket_error'] for r in rows)<1e-7,rows
out={'scope':'Finite floating-point audit using the original raw connection and original Poisson tensor; not proof of all-mode bounds or nonlinear periodicity.', 'cases':rows}
Path(__file__).with_name('physical_born_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
