from pathlib import Path
import json,re,hashlib,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'buffered_run'
rows=json.loads((OUT/'results.json').read_text())
keys={(r['case'],r['model'],r['method'],r['mesh']) for r in rows}
expected={(c,m,t,g) for c in 'ABCD' for m in ['SD','SD2','FD'] for t,g in [('RK4','fixed'),('Euler','fixed'),('CN','fixed'),('RK4','moving')]}
assert len(rows)==48 and keys==expected
cn=[]
for r in rows:
    cfg=r['config'];case=r['case'];half=dict(A=5,B=10,C=30,D=30)[case];comp=dict(A=10,B=20,C=40,D=40)[case]
    assert r['completed'] and abs(r['reached']-.01)<1e-14
    assert cfg['L']==2*comp and cfg['yhalf']==comp and cfg['nx']==20*comp
    assert cfg['eval_half']==half and cfg['eval_yhalf']==half and cfg['h']==.1 and cfg['dt']==.0001
    assert min(r['support_margins'])>0 and r['min_J']>0
    assert all(np.isfinite(list(r['max_errors'].values())))
    stem='_'.join(r[k] for k in ['case','model','method','mesh'])
    with np.load(OUT/(stem+'_state.npz')) as d:
        assert np.isfinite(d['state']).all()
        assert len(d['x'])==cfg['nx'] and len(d['y'])==cfg['nx']
    if r['method']=='CN':
        assert len(r['cn_diagnostics'])==100
        for d in r['cn_diagnostics']:assert d['residual']<=d['tolerance']
        cn.extend(r['cn_diagnostics'])
    if r['method']=='RK4' and r['mesh']=='fixed':
        with np.load(OUT/(stem+'.npz')) as d:
            assert len(d['x'])==cfg['eval_points'] and len(d['y'])==20*half
            for f in ['u','v']:assert float(abs(d[f]-d['exact_'+f]).max())==r['max_errors'][f]
for c in 'ABCD':
    baseline=max((OUT/f'{c}_{m}_RK4_fixed.json').stat().st_mtime for m in ['SD','SD2','FD'])
    for kind in ['fields','errors']:
        for ext in ['png','pdf','py']:
            asset=HERE/'figures'/f'{c}_{kind}.{ext}'
            assert asset.exists() and asset.stat().st_mtime>=baseline, str(asset)
text=(HERE/'manuscript.md').read_text(encoding='utf8')
before=(OUT/'before/manuscript.md').read_text(encoding='utf8')
assert re.findall(r'\$\$[\s\S]*?\$\$',text)==re.findall(r'\$\$[\s\S]*?\$\$',before)
tables=re.findall(r'<table class="comparison">[\s\S]*?</table>',text)
assert len(tables)==6
R={(r['case'],r['model'],r['method'],r['mesh']):r for r in rows}
for i,tab in enumerate(tables):
    values=[]
    for c in 'ABCD':
        if i%3==0:
            values.extend(R[c,m,'RK4','fixed']['max_errors'][f] for f in ['u','v'] for m in ['SD','SD2','FD'])
        elif i%3==1:
            values.extend(R[c,m,t,'fixed']['max_errors'][f] for m in ['SD','SD2','FD'] for f in ['u','v'] for t in ['Euler','RK4','CN'])
        else:
            values.extend(R[c,m,'RK4',g]['max_errors'][f] for m in ['SD','SD2','FD'] for g in ['fixed','moving'] for f in ['u','v'])
    actual=re.findall(r'[0-9]+\.[0-9]+e[+-][0-9]+',tab)
    assert actual==[f'{v:.6e}' for v in values],i
nbpath=HERE.parents[1]/'notebook/DLW数值分析report.ipynb'
nb=json.loads(nbpath.read_text(encoding='utf8'))
assert nb['metadata']['buffered_rerun']['status']=='completed_48_paper_runs'
manifest=json.loads((OUT/'manifest.json').read_text())
manifest['notebook_sha256']=hashlib.sha256(nbpath.read_bytes()).hexdigest()
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
report=dict(runs=48,all_completed=True,cn_steps=len(cn),cn_max_iterations=max(d['iterations'] for d in cn),min_J=min(r['min_J'] for r in rows),minimum_x_support_margin=min(min(r['support_margins']) for r in rows),max_initial_error=max(r['initial_error'] for r in rows),fixed_field_caches_checked=12,table_values_checked=288,display_equations_unchanged=True)
(OUT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
