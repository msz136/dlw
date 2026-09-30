"""DLW paper Fig1(a,b): fixed exact paper parameters, common continuous data."""
import sys,json,csv,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate._ivp import dop853_coefficients as dc
HERE=Path(__file__).resolve().parent;LIB=HERE.parent/'dlw_semidiscrete/numerics/lib'
sys.path.insert(0,str(LIB))
import parametric as pm
from parametric_open import OpenModel
OUT=HERE/'out';OUT.mkdir(parents=True,exist_ok=True)
CASES={'fig1a':pm.Parameters(a=2,p=1,q=2,rho=1),'fig1b':pm.Parameters(a=2,p=4,q=-3,rho=1)}
TIMES=(0.,.005,.01,.02,.05,.1,.25,.5,1.)

class PaperExact(pm.Exact):
    def __init__(self,pars,h,continuous=False):
        self.pars,self.h,self.continuous=pars,h,continuous
        P,Q=pars.p-pars.a,pars.q+pars.a
        assert pars.p+pars.q>0 and pars.rho>0 and P*Q<0 and min(abs(P),abs(Q))>h/2
        self.S=pars.p+pars.q;self.omega=pars.q**2-pars.p**2
        self.ry=1/P+1/Q
        self.chi=np.log((P+h/2)/(P-h/2))+np.log((Q+h/2)/(Q-h/2))
        self.gamma=np.log(-(P+h/2)/(Q-h/2));self.gamma0=np.log(-P/Q)

# The field/RHS code is unchanged; only its exact-reference factory supports both regular sectors.
pm.Exact=PaperExact
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
def csvout(p,rows):
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def advance(fun,t,z,h,method):
    if method=='euler':return z+h*fun(t,z)
    if method=='heun':
        k=fun(t,z);return z+h*(k+fun(t+h,z+h*k))/2
    if method=='rk4':return pm.rk4(fun,t,z,h)
    ks=[]
    for i in range(12):ks.append(fun(t+dc.C[i]*h,z+h*sum(dc.A[i,j]*ks[j] for j in range(i) if dc.A[i,j])))
    return z+h*sum(dc.B[j]*ks[j] for j in range(12) if dc.B[j])

def experiment(spec):
    pars=CASES[spec['case']];h,nx,dt=spec['h'],spec['nx'],spec['dt']
    m=OpenModel(pars,h=h,nx=nx,L=20.,yhalf=1.5,model=spec['model'],continuous=True)
    z=m.exact(0.);scale=[float(np.max(abs(v))) for v in m.G.uv(m.js,m.X.x,0.)]
    history=[];arrays={'x':m.X.x,'y':m.y};first_bad=None
    def sample(t,z,tag):
        nonlocal first_bad
        uv=m.fields(z,t);ref=m.G.uv(m.js,m.X.x,t)
        errors=[float(np.max(abs(v-w))) for v,w in zip(uv,ref)]
        rel=[e/s for e,s in zip(errors,scale)]
        if first_bad is None and max(rel)>.01:first_bad=t
        history.append(dict(t=t,kind=tag,u_error=errors[0],v_error=errors[1],u_relative_initial_peak=rel[0],v_relative_initial_peak=rel[1]))
        for label,v in zip(('u','v'),uv):arrays[f't{t:g}_{label}']=v.copy()
    sample(0.,z,'requested');last=0.;status='completed';reason=''
    samples={round(t/dt):t for t in TIMES[1:]}
    for j in range(1,round(1/dt)+1):
        with np.errstate(over='raise',invalid='raise',divide='raise'):
            try:
                zz=advance(m.rhs,(j-1)*dt,z,dt,spec['method'])
                if not np.all(np.isfinite(zz)) or np.max(abs(zz))>1000:raise FloatingPointError('state magnitude exceeded 1000 or nonfinite state')
            except (FloatingPointError,OverflowError) as exc:
                status='stopped';reason=str(exc);break
        z=zz;last=j*dt
        if j in samples:sample(samples[j],z,'requested')
    if abs(history[-1]['t']-last)>1e-12:sample(last,z,'last_valid')
    key=f"{spec['case']}_{spec['model']}_{spec['method']}_{spec['purpose']}"
    path=OUT/(key+'.npz');np.savez_compressed(path,**arrays)
    return dict(spec=spec,status=status,reason=reason,reached=last,attempted_until=1.,history=history,first_sample_over_1pct=first_bad,initial_peaks=scale,profile=str(path.resolve()),profile_sha256=sha(path))

def check_reference():
    checks=[]
    for case,pars in CASES.items():
        # Independent direct tau derivatives at paper phases=0,c1=1.
        x=np.linspace(-3,3,121);h=.125;j=np.array([-3,0,4]);y=(j[:,None]+.5)*h
        S=pars.p+pars.q;P=pars.p-pars.a;Q=pars.q+pars.a;R=1/P+1/Q
        z=S*x[None,:]+R*y+(pars.q**2-pars.p**2)*.1
        E=np.exp(z)/S;gamma=-P/Q;F=1+gamma*E;G=1+E
        u=2*S*(gamma*E/F-E/G);v=2*S*R*(gamma*E/F**2+E/G**2)
        ref=PaperExact(pars,h,True).uv(j,x,.1)
        err=max(float(np.max(abs(u-ref[0]))),float(np.max(abs(v-ref[1]))));assert err<1e-12
        checks.append(dict(case=case,tau_formula_error=err,gamma=gamma,rho_code_is_phase_weight=1))
    return checks

def main():
    plan=[]
    for case in CASES:
        for model in ('structure','fd'):
            for method in ('euler','heun','rk4','rk8'):
                for purpose,dt in (('main',.000125),('time_half',.0000625)):
                    plan.append(dict(case=case,model=model,method=method,purpose=purpose,dt=dt,h=.125,nx=256))
            for purpose,h,nx in (('space_y',.0625,256),('space_x',.125,512)):
                plan.append(dict(case=case,model=model,method='rk4',purpose=purpose,dt=.000125,h=h,nx=nx))
    sources={str(p):sha(p) for p in (Path(__file__),LIB/'parametric.py',LIB/'parametric_open.py',LIB/'dynamics.py',LIB/'solver.py')}
    frozen=dict(plan=plan,sources=sources,reference_checks=check_reference(),paper_parameters={k:vars(v) for k,v in CASES.items()})
    dest=OUT/'results.json';saved=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {**frozen,'runs':[]}
    assert saved['sources']==sources and saved['plan']==plan
    for spec in plan:
        if any(r['spec']==spec for r in saved['runs']):continue
        r=experiment(spec);saved['runs'].append(r);dump(dest,saved)
        print(len(saved['runs']),spec,r['status'],r['reached'],flush=True)
    rows=[]
    for r in saved['runs']:
        assert sha(r['profile'])==r['profile_sha256']
        with np.load(r['profile']) as z:
            spec=r['spec'];ref=PaperExact(CASES[spec['case']],spec['h'],True);n=round(1.5/spec['h']);js=np.arange(-n,n)
            for e in r['history']:
                exact=ref.uv(js,z['x'],e['t'])
                for f,target in zip(('u','v'),exact):assert abs(float(np.max(abs(z[f"t{e['t']:g}_{f}"]-target)))-e[f'{f}_error'])<1e-12
                rows.append({**spec,**e,'run_status':r['status'],'reached':r['reached']})
    csvout(OUT/'errors.csv',rows)
    status=[{**r['spec'],'status':r['status'],'reached':r['reached'],'first_sample_over_1pct':r['first_sample_over_1pct'],'reason':r['reason']} for r in saved['runs']]
    csvout(OUT/'status.csv',status)
    table=[]
    for case in CASES:
        for model in ('structure','fd'):
            r=next(r for r in saved['runs'] if r['spec']['case']==case and r['spec']['model']==model and r['spec']['method']=='rk4' and r['spec']['purpose']=='main')
            for t in (.005,.01,.02,1.):
                e=next((e for e in r['history'] if abs(e['t']-t)<1e-12),None)
                table.append(f"| {case} | {model} | {t:g} | "+(f"{e['u_error']:.6e} | {e['v_error']:.6e}" if e else '未到达 | 未到达')+' |')
    report='''# DLW 原文图1两组参数：数值演化交接

本次只运行此前讨论的图1(a)/(b)两组单孤子，未扫描自选参数；不声称覆盖原文所有周期波、双孤子或有理解图。

- 图1(a)：a=2,p=1,q=2,c1=1,xi10=eta10=0，原图t=1。
- 图1(b)：a=2,p=4,q=-3,c1=1,xi10=eta10=0，原图t=0；这里额外尝试演化至t=1。
- 代码rho=1是tau的相位权重exp(xi10+eta10)/c1，不是2HS物理密度。DLW未知量为u,v。
- 图1(b)属于P=p-a>0,Q=q+a<0的另一正则分支；新Reference仅扩展旧代码的参数检查，场公式与演化RHS未改。两组独立直接tau求导核对通过。

比较结构半离散SD与普通交错差分FD；均使用共同连续初值/时变边界、固定网格、背景相对二次外推y闭合，无滤波或内部解析解重置。不是2HS四方案的照搬，也没有对DLW发明校准项。网格x∈[-10,10)、nx=256，y中点覆盖[-1.5,1.5]、h=.125；x四阶周期差分，主dt=.000125。Euler/Heun/RK4/固定步长DOP853八阶，均补时间步减半；另RK4分别加密x或y。共40条轨道。

每条尝试推进至t=1；遇非有限值或状态绝对值超过1000即记录停止。1%初始峰值仅作观察指标，不作为提前停止条件。“推进完成”不等于“精度通过”。误差是原生共同物理格点全域最大绝对误差；不是单个空间点，也未将其称为连续上确界。时间样点0/.005/.01/.02/.05/.1/.25/.5/1，原图1(b)的t=0仅检验初值，不能代表求解精度。

## RK4主配置结果

| 原图 | 模型 | t | u误差 | v误差 |
|---|---|---:|---:|---:|
'''+ '\n'.join(table)+'''

完整四算法和减步/加密数据见out/errors.csv；各轨道停止时刻、失败原因及首次采样超过1%见out/status.csv。未到达时刻不可用最后有效状态冒填。out/results.json包含源码哈希、原始剖面路径和哈希；所有保存误差已从剖面独立读回核对。

这批数值设置由本项目选择，原论文提供的是精确解图，并未给这些时间算法的精度表。当前短时结果不能替代图1(a) t=1的传播验收；背景边界与x周期绕接的影响也属于实际总误差。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print('\n'.join(table),flush=True)

if __name__=='__main__':main()
