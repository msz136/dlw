"""Independent S3 formula audit, finite-domain controls and Agent handoff."""
import json
from pathlib import Path
import numpy as np
import run_study as run
eng,ale=run.eng,run.ale
HERE,OUT=run.HERE,run.OUT

def main():
    saved=json.loads((OUT/'results.json').read_text());summary=json.loads((OUT/'summary.json').read_text())
    assert summary['runs']==736 and not summary['failed']
    audit=[];domain=[];consistency=[];controls=OUT/'domain_controls';controls.mkdir(exist_ok=True)
    # Independent continuous material derivative, not the implemented PDE RHS.
    for p in (5.,12.,22.):
        residuals=[]
        for n in (100,200,400,800):
            sol,*_=eng.initialize(p,'integrable_original',n,4.)
            u,x,_=sol.continuous_X(np.linspace(-4,4,n+1),0.)
            _,rho,m,_=ale.reference(sol,x,0.)
            rhs=run.paper_ale_rhs((x,m[1:-1],rho[1:-1]),sol,0.)
            eps=1e-5
            _,rp,mp,_=ale.reference(sol,x-eps*u,eps)
            _,rm,mm,_=ale.reference(sol,x+eps*u,-eps)
            residuals.append([float(np.max(abs(rhs[1]-(mp-mm)[1:-1]/(2*eps)))),float(np.max(abs(rhs[2]-(rp-rm)[1:-1]/(2*eps))))])
        orders=np.log2(np.array(residuals[:-1])/np.array(residuals[1:]))
        assert np.min(orders[-1])>1.9
        consistency.append(dict(p=p,n=[100,200,400,800],fields=['m','rho'],material_derivative_fd_step=eps,rhs_residuals=residuals,observed_orders=orders.tolist()))
    eng.OUT=controls;eng.TIMES=(0.,.25,.5)
    for p in (3.,5.,12.,22.):
        for n,dt in ((400,.003125),(200,.0125)):
            sol,system,z,_,_=eng.initialize(p,'integrable_original',n,4.)
            f=system.fields(0.,z);u,x,_=sol.continuous_X(np.linspace(-4,4,n+1),0.)
            _,rho,_,_=eng.safe_reference(sol,x,0.)
            state=(x,ale.second_derivative(u,x)+2,rho[1:-1])
            actual=run.paper_ale_rhs(state,sol,0.)
            old=ale.rhs(state,sol,0.,'rho',x[0],x[-1])
            _,rr,uu,_=ale.unpack(state,sol,0.,x[0],x[-1])
            checks=dict(p=p,n=n,initial_grid_match=float(np.max(abs(f['x']-x))),
                        all_node_velocity_residual=float(np.max(abs(actual[0]+uu))),
                        interior_rhs_match=max(float(np.max(abs(actual[j]-old[j]))) for j in (1,2)),
                        initial_poisson_u_residual=float(np.max(abs(uu-u))))
            assert checks['initial_grid_match']<1e-12 and checks['all_node_velocity_residual']==0 and checks['interior_rhs_match']==0 and checks['initial_poisson_u_residual']<1e-11
            audit.append(checks)
            # Uniform S4 on exactly the same initial endpoint interval as S3.
            half=float((x[-1]-x[0])/2)
            assert abs(x[-1]+x[0])<1e-12
            for method in run.METHODS:
                spec=dict(p=p,route='difference_fixed',n=n,dt=dt,halfwidth=half,method=method,purpose='matched_initial_domain')
                key=eng.case_key(spec);meta=controls/(key+'.json')
                if meta.exists():r=json.loads(meta.read_text())
                else:
                    r=eng.run_one(spec);r['profile']=str((controls/r['profile']).resolve());r['profile_sha256']=run.sha(r['profile']);r['spec']=spec;eng.dump(meta,r)
                assert run.sha(r['profile'])==r['profile_sha256']
                with np.load(r['profile']) as z:
                    for t in run.TIMES:
                        size=16001 if n==400 else 8001
                        data=tuple(z[f't{t}_{s}'] for s in ('x','u','rho_x','rho'))
                        e=eng.measure(p,data,t,size)['core']
                        def lookup(route):
                            k=eng.case_key({**spec,'route':route,'halfwidth':4.})
                            return saved['rows'][k]['snapshots'][str(t)][str(size)]
                        moving,base=lookup('difference_paper_ale'),lookup('difference_fixed')
                        domain.append(dict(p=p,n=n,dt=dt,method=method,t=t,halfwidth=half,profile=r['profile'],profile_sha256=r['profile_sha256'],u_error=e['u'],rho_error=e['rho'],u_ratio_s3_s4=moving['u']/e['u'],rho_ratio_s3_s4=moving['rho']/e['rho'],u_rank_flip=(moving['u']<base['u'])!=(moving['u']<e['u']),rho_rank_flip=(moving['rho']<base['rho'])!=(moving['rho']<e['rho'])))
    run.writecsv(OUT/'domain_control_cells.csv',domain)
    evalmax=0.;evalflips=[];timeflips=[];counts={};range_info=[]
    for r in saved['rows'].values():
        assert run.sha(r['profile'])==r['profile_sha256']
        for t in run.TIMES:
            a,b=r['snapshots'][str(t)]['16001'],r['snapshots'][str(t)]['32001']
            evalmax=max(evalmax,*(abs(b[f]/a[f]-1) for f in ('u','rho')))
    def error(p,n,dt,method,t,scheme,size):
        k=eng.case_key(dict(p=p,n=n,dt=dt,method=method,route=run.SCHEMES[scheme],halfwidth=4.))
        return saved['rows'][k]['snapshots'][str(t)][str(size)]
    for n,dt,size in ((400,.003125,16001),(200,.0125,8001)):
        for method in run.METHODS:
            for t in run.TIMES:
                for num,den in (('S2','S1'),('S3','S4'),('S1','S3'),('S2','S3')):
                    wins={f:[] for f in ('u','rho')}
                    for p in range(3,23):
                        a,b=error(p,n,dt,method,t,num,size),error(p,n,dt,method,t,den,size)
                        aa,bb=error(p,n,dt,method,t,num,32001),error(p,n,dt,method,t,den,32001)
                        for field in wins:
                            if a[field]<b[field]:wins[field].append(p)
                            if (a[field]<b[field])!=(aa[field]<bb[field]):evalflips.append(dict(p=p,n=n,method=method,t=t,pair=f'{num}/{den}',field=field))
                        if p in (5,12,22):
                            ha,hb=error(p,n,dt/2,method,t,num,size),error(p,n,dt/2,method,t,den,size)
                            for field in wins:
                                if (a[field]<b[field])!=(ha[field]<hb[field]):timeflips.append(dict(p=p,n=n,method=method,t=t,pair=f'{num}/{den}',field=field))
                    counts[f'N{n}_{method}_t{t}_{num}/{den}']=wins
    validation=dict(s3_formula_checks=audit,s3_continuous_consistency=consistency,profile_hashes_checked=len(saved['rows']),domain_control_runs=32,domain_ranking_flips=sum(int(r[f]) for r in domain for f in ('u_rank_flip','rho_rank_flip')),max_relative_eval16001_to32001=evalmax,evaluation_ranking_flips=evalflips,time_half_ranking_flips=timeflips,winning_p=counts,html_unchanged=run.sha(run.ROOT/'numerical_analysis.html')==saved['html_sha256'])
    eng.dump(OUT/'validation.json',validation)
    assert validation['html_unchanged']
    lines=[]
    for pair in ('S2/S1','S3/S4','S1/S3','S2/S3'):
        w=counts[f'N400_rk4_t0.5_{pair}'];lines.append(f"| {pair} | {len(w['u'])}/20 | {len(w['rho'])}/20 |")
    report=f'''# 2HS 四方案数值分析：Agent交接

**用户已确认新的四方案定义。它替代上一轮“3方程×Rm/固定”的六组合表；新旧S编号不能混用。此次没有修改HTML。**

| 新编号 | 方案 | 数据路线 |
|---|---|---|
| S1 | 原论文可积半离散＋论文动网格 | integrable_original |
| S2 | 参数校准半离散＋论文动网格 | integrable_calibrated |
| S3 | 连续2HS普通ALE差分＋论文动网格 | difference_paper_ale（本次新实现） |
| S4 | 同一套普通ALE差分＋均匀固定网格 | difference_fixed |

Rm已从本轮主比较移出；rho仍是物理未知量及论文网格关系中的密度，不能从方程里删去。S3不是旧difference_matched，也不是端点固定的旧difference_rho。

## 完成结果与填表

- p=3,…,22，共20个整数参数（原页面只有13行，若保留原行可筛选3/4/5/6/8/10/11/12/14/16/18/20/22）。
- Euler、Heun、RK4、固定步长DOP853八阶主公式；t=.25、.5。
- §2.1口径：N400、dt=.003125、16001评价点；§2.2口径：N200、dt=.0125、8001评价点。
- **640条主轨道全部完成，输出1280个u/rho双场单元格**；p5/12/22的96条减半步长轨道也全部完成，输出192个双场单元格。
- 合计736条：{summary['new_runs']}新算、{summary['reused_runs']}匹配复用。另完成32条固定网格同初始物理区间控制。
- `out/main_wide.csv`：每行p/时间算法/N/dt/t，新S1–S4四列，每格u误差/rho误差。四列均有数值，直接用于改写后的主表。
- `out/main_cells.csv`：未舍入数值及轨道来源；`time_half_wide.csv` / `time_half_cells.csv` 为减步表；`comparisons.csv`为S2/S1、S3/S4、S1/S3、S2/S3误差比。
- `out/results.json`保留所有主/减步轨道三档评价结果；`plan.json`记录方案、配置、代码及来源哈希。profile为绝对路径，复用轨道仍在旧目录，搬运数据包时须一起收集。

## S3如何实现

与S1/S2取相同初始物理节点：X_k均匀覆盖[-4,4]，经连续孤子hodograph映射得到x_k(0)。使用节点变量m=u_xx+2、rho；初值m=D2 u_exact+2，rho取连续解析节点值。每个时间级在当前节点上解非均匀三对角Poisson方程恢复u，端点场取当前物理位置和时间的解析值。

**所有节点，包括两端，均按x_dot=-u移动**。不强制不同方案共用节点轨迹。用S4同一套非均匀三点D1/D2，普通ALE连续方程为

```
m_dot=(u+V)*D1(m)+2*D1(u)*m+rho*D1(rho)
rho_dot=(u+V)*D1(rho)+rho*D1(u)
D2(u)=m-2
```

S3取V=-u，输运项消失；S4取V=0、两端固定。S3独立演化节点rho，不强制离散rho*d=a；这正是普通差分与论文结构保持格式的区别。S3仍可能保留部分连续结构，但未宣称其离散可积。

S1沿用论文式，C=1；S2只将离散系统常数改为C=a+sqrt(1+a²)，a=8/N；解析目标、初值与参照仍固定c_phys=1。

## 比较口径与边界限制

主指标是同一连续解析解在公共物理区间[-2,2]上的采样最大绝对误差；包含时间、空间及线性重构误差，不是单独时间误差。S1/S2的rho在胞元中点，S3/S4在节点；均先重构到相同物理评价点。

N均为区间数，但S1/S2/S3的初始物理区间由X∈[-4,4]映射得到，通常比[-4,4]稍宽；主S4沿用旧固定物理区间[-4,4]。**故主表是完整方法比较，不是严格只改变一个因素的因果实验。** S1/S2由左侧解析u确定积分常数，S3/S4的Poisson反演指定两端解析u，边界闭合也不同。不能将S1/S3的差异全部归结为可积性。

为核对S3/S4的区间影响，额外在p3/5/12/22、两分辨率、四时间法上，将S4均匀网格初始端点改成与S3相同；其后仍固定。见 `domain_control_cells.csv`，出现{validation['domain_ranking_flips']}次单场排名翻转。该控制核对代表点，不能替代全参数同域/扩域收敛证明。

## 验证与可用结论

- S3初始节点与原论文路线一致；逐项核对场右端等于既有ALE内点公式、全部节点速度为-u、初始Poisson重构正确，8组检查通过。求解器内部检查阶段有限值、正密度与节点顺序；736个profile哈希重新核对通过。
- 独立用连续精确解的沿轨迹中心差商核对S3右端一致性：p5/12/22、N100/200/400/800；最细两档的m/rho右端残差阶为1.98–2.00。该检查支持空间一致性，不是总演化误差二阶或可积性证明。
- 16001→32001点评价最大相对变化{100*evalmax:.4f}%；从各主表原评价密度加密至32001点，四种配对排名翻转{len(evalflips)}次。
- 代表参数减半步长，四配对的单场排名翻转{len(timeflips)}次；详见validation.json，不能忽略Euler误差抵消或从单档步长推断空间方法固定排名。
- 下表只汇总N400/RK4/t=.5的20个p；“胜出”指分子方案的该场误差更小，不要求改善超过某个比例。

| 分子/分母 | u胜出 | rho胜出 |
|---|---:|---:|
{chr(10).join(lines)}

完整参数列表在validation.json的winning_p。这里只是确定性参数扫描，不能把多方法、多时刻当独立样本宣称统计显著性。

## 报告改写建议

主表改为以上四方案；分别回答校准是否有效（S2/S1）、普通差分下论文网格是否有利（S3/S4，结合区间控制）、论文方案整体表现如何（S1/S3、S2/S3并注明边界与变量差异）。删除旧六组合中“方程待构造”的占位，不把旧S5/S6编号沿用为新S1–S4；旧RM结论作为历史结果保留即可。原生网格可积结果不再是缺项。

复现：运行本目录run_study.py，再运行audit_and_handoff.py。旧求解器、旧实验及根HTML均未改动。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps({k:v for k,v in validation.items() if k not in ('winning_p','s3_formula_checks')},indent=2))

if __name__=='__main__':main()
