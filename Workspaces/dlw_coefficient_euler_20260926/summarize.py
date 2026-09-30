"""Read-back audit and reproducible tables. No trajectory fitting."""
import csv,json
import numpy as np
from collections import Counter
from run import HERE,OUT,CASES,THEORY,COEFS,sha,dump,errors,FamilyModel

def main():
    allrows=[];sources={};counts={}
    for filename in ('results.json','refinements.json','boundary_controls.json'):
        p=OUT/filename
        if not p.exists():continue
        d=json.loads(p.read_text(encoding='utf-8'));assert len(d['rows'])==len(d['plan'])
        allrows+=list(d['rows'].values());sources.update(d['source_hashes'])
        counts[filename]=dict(Counter(r['status'] for r in d['rows'].values()))
    for p,h in sources.items():assert sha(p)==h,p
    rows=[r for r in allrows if r['status']=='completed']
    idx={(r['spec']['case'],r['spec']['route'],r['spec']['c'],r['spec']['kappa'],r['spec']['purpose']):r for r in rows}
    readback=0.;init_groups={};flat=[]
    for r in rows:
        s=r['spec'];p=OUT/r['profile'];assert sha(p)==r['profile_sha256']
        group=(s['case'],s['h'],s['nx'],s['L'],s['yhalf'])
        init_groups.setdefault(group,set()).add(r['initial_state_sha256'])
        a=np.load(p)
        m=FamilyModel(CASES[s['case']],**{k:s[k] for k in ('route','c','kappa','h','nx','L','yhalf')})
        for t,snap in r['snapshots'].items():
            uv=[a[f't{t}_{f}'] for f in ('u','v')]
            checked=errors(m,uv,float(t),4)
            for f in ('u','v'):
                readback=max(readback,abs(checked[f]-snap['errors'][f]))
                flat.append({**s,'time':t,'field':f,'error':snap['errors'][f],'eval_double':snap['eval_double'][f],'nodal':snap['nodal_errors'][f]})
    assert all(len(v)==1 for v in init_groups.values())
    assert readback<1e-14
    with (OUT/'errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    def er(case,route,c,k,purpose='main',t='0.01'):
        row=idx.get((case,route,c,k,purpose))
        return None if row is None else np.array(list(row['snapshots'][t]['errors'].values()))
    def pair(v):return '失败' if v is None else ' / '.join(f'{z:.4e}' for z in v)
    def table(configs,purpose):
        lines=['| 参数 (a,p,q) | '+' | '.join(z[0] for z in configs)+' |','|'+'---|'*(len(configs)+1)]
        for name,p in CASES.items():
            lines.append(f'| {name} ({p.a:g},{p.p:g},{p.q:g}) | '+' | '.join(pair(er(name,*cfg[1:],purpose)) for cfg in configs)+' |')
        return '\n'.join(lines)
    named=[('普通差分','fd',0.,0.),('原可积 (0,0)','sd',0.,0.),('理论共用系数','sd',*THEORY)]
    axial=[('c=-1/8,κ=0','sd',-.125,0.),('c=1/8,κ=0','sd',.125,0.),('c=0,κ=-1/8','sd',0.,-.125),('c=0,κ=1/8','sd',0.,.125)]
    corners=[(f'({c:g},{k:g})','sd',c,k) for c in (-.125,.125) for k in (-.125,.125)]
    tables={'main_primary':table(named,'main'),'main_axial':table(axial,'main'),'main_joint':table(corners,'main'),
            'space_x':table(named,'space_x'),'fine_time':table(named,'fine_time'),'fine_xy':table(named,'fine_xy')}
    diagnostics={};rankings={}
    for purpose in ('main','time_half','space_y','space_x','domain_x','domain_y','fine_time','fine_xy','wide_fine','wide_fine_xy','tall_fine'):
        rankings[purpose]={}
        for name in CASES:
            f=er(name,'fd',0.,0.,purpose);o=er(name,'sd',0.,0.,purpose);th=er(name,'sd',*THEORY,purpose)
            if f is not None and o is not None and th is not None:
                rankings[purpose][name]={'original_over_fd':(o/f).tolist(),'theory_over_fd':(th/f).tolist(),'theory_over_original':(th/o).tolist()}
    for name in CASES:
        diagnostics[name]={}
        for label,route,c,k in named:
            base=er(name,route,c,k)
            by={}
            for purpose in ('time_half','space_y','space_x','domain_x','domain_y','fine_time','fine_xy','wide_fine','wide_fine_xy','tall_fine'):
                val=er(name,route,c,k,purpose)
                if val is not None:by[purpose]={'error':val.tolist(),'relative_change_vs_main':(val/base-1).tolist()}
            diagnostics[name][label]=by
    initial_eval={}
    for name in CASES:
        m=FamilyModel(CASES[name]);uv=m.fields(m.exact(0),0)
        initial_eval[name]=errors(m,uv,0,8)
    evalmax=max(abs(f['eval_double']/f['error']-1) for f in flat)
    audits={}
    for purpose in ('time_half','space_y','space_x','domain_x','domain_y'):
        flips=[];total=0;max_change=0.
        for r in rows:
            s=r['spec']
            if s['purpose']!='main':continue
            base=er(s['case'],s['route'],s['c'],s['kappa'])
            alt=er(s['case'],s['route'],s['c'],s['kappa'],purpose)
            if alt is None:continue
            max_change=max(max_change,float(np.max(abs(alt/base-1))))
            if s['route']!='sd':continue
            fd=er(s['case'],'fd',0.,0.);fda=er(s['case'],'fd',0.,0.,purpose)
            for i,f in enumerate(('u','v')):
                total+=1
                if (base[i]<fd[i])!=(alt[i]<fda[i]):flips.append(dict(case=s['case'],c=s['c'],kappa=s['kappa'],field=f))
        audits[purpose]=dict(fd_comparisons=total,rank_flips=flips,max_relative_error_change=max_change)
    eval_clean=max(abs(f['eval_double']/f['error']-1) for f in flat if f['case']!='P5')
    result=dict(counts=counts,source_hashes_verified=True,profile_hashes_verified=len(rows),same_initial_hashes=True,
        error_readback_max=readback,initial_max_nodal=max(r['initial_field_error'] for r in rows),
        evaluation_max_relative_change=evalmax,evaluation_max_relative_change_excluding_P5=eval_clean,
        sensitivity_audits=audits,initial_interpolated_errors=initial_eval,
        rankings=rankings,diagnostics=diagnostics,tables=tables)
    dump(OUT/'summary.json',result)
    (OUT/'tables.md').write_text('\n\n'.join('### '+k+'\n\n'+v for k,v in tables.items())+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rankings','diagnostics','tables')},indent=2))
    print(tables['main_primary']);print(tables['fine_time']);print(tables['fine_xy'])
if __name__=='__main__':main()
