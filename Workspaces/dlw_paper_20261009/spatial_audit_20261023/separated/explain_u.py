"""Check analytic leading h^2 coefficients of the initial u_t defects."""
from run_separated import *

def coefficients(m,y,include_v=False):
    # Normalized bivariate Taylor coefficients of tau, then log(tau).
    out=[]
    for isf in [True,False]:
        _,w=m.G.tau(np.asarray(y)/m.h-.5,m.x,0,isf)
        s=m.G.rates[:,0,None,None]; e=m.G.rates[:,2,None,None]
        degree=3 if include_v else 2
        T={(n,j):np.sum(w*s**n*e**j,axis=0)/(math.factorial(n)*math.factorial(j)) for n in range(4) for j in range(degree+1)}
        L={(0,0):np.zeros_like(T[0,0])}
        for j in range(1,degree+1):L[0,j]=T[0,j]-sum(k*L[0,k]*T[0,j-k] for k in range(1,j))/j
        for n in range(1,4):
          for j in range(degree+1):
            L[n,j]=T[n,j]-sum(i*L[i,k]*T[n-i,j-k] for i in range(1,n+1) for k in range(j+1) if (i,k)!=(n,j))/n
        out.append(L)
    f,g=out
    diff=lambda n,j:2*math.factorial(n)*math.factorial(j)*(f[n,j]-g[n,j])
    plus=lambda n,j:2*math.factorial(n)*math.factorial(j)*(f[n,j]+g[n,j])
    uy=diff(1,1);v=plus(1,1)
    uxy=diff(2,1);vx=plus(2,1)
    vxxy=plus(3,2);uxxyy=diff(3,2)
    ax=((v-uy)/16-.25)*(vx-uxy)
    ans=[vxxy/24,-vxxy/12+uxxyy/4-ax,-vxxy/12]
    if include_v:
        uyy=diff(1,2);uxyy=diff(2,2)
        axy=(plus(1,2)-uyy)*(vx-uxy)/16+((v-uy)/16-.25)*(plus(2,2)-uxyy)
        ans.extend([diff(3,3)/12-plus(3,3)/4-(uxy*uyy+uy*uxyy)/2-axy,-diff(3,3)/6])
    return np.array(ans)

def check_v():
    rows=[]
    data=json.loads((HERE/'spatial.json').read_text())
    for case in CASES:
        h=.025;m=Model(case,'Centered-SD',.1,h);pred=np.zeros(2);xx=abs(m.x)<=HALF_WIDTHS[case]
        for start in range(0,len(m.y),64):
            yy=m.y[start:start+64];mask=abs(yy)<HALF_WIDTHS[case]
            if mask.any():pred=np.maximum(pred,np.max(abs(coefficients(m,yy[mask],True)[3:,:,xx]),axis=(1,2)))
        actual=[next(r['Y'][1] for r in data if r['case']==case and r['h']==h and r['dx']==.1 and r['method']==method) for method in ['Centered-SD','FD']]
        row=dict(case=case,h=h,predicted=(h*h*pred).tolist(),measured=actual,relative_difference=(abs(h*h*pred-actual)/actual).tolist())
        rows.append(row);print(json.dumps(row),flush=True)
    (HERE/'v_leading_coefficients.json').write_text(json.dumps(rows,indent=2))

def run_check():
    records=[]
    for case in CASES:
      for h in [.1,.05,.025]:
        m=Model(case,'Centered-SD',.1,h)
        base=coefficients(m,m.y[:1]);pred=np.zeros(3)
        xx=abs(m.x)<=HALF_WIDTHS[case]
        for start in range(0,len(m.y),64):
            yy=m.y[start:start+64];mask=abs(yy)<HALF_WIDTHS[case]
            if mask.any():
                c=coefficients(m,yy[mask])-base
                pred=np.maximum(pred,np.max(abs(c[:,:,xx]),axis=(1,2)))
        data=json.loads((HERE/'spatial.json').read_text())
        measured=[next(r['Y'][0] for r in data if r['case']==case and r['method']==method and r['h']==h and r['dx']==.1) for method in ['Endpoint-SD','Centered-SD','FD']]
        row=dict(case=case,h=h,predicted=(h*h*pred).tolist(),measured=measured,relative_maximum_difference=(abs(h*h*pred-measured)/measured).tolist(),FD_over_Endpoint=measured[2]/measured[0],Centered_over_Endpoint=measured[1]/measured[0])
        records.append(row);print(json.dumps(row),flush=True)
    (HERE/'u_leading_coefficients.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':
    if len(sys.argv)>1:check_v()
    else:run_check()
