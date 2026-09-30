"""Read-only audit of frozen trajectories and physical-error comparisons."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv, json, hashlib
import numpy as np
from scan import OUT, PVALUES, SymmetricProblem, Parameters, evaluate, sha, dump
from supplement import high_band

HERE = Path(__file__).resolve().parent
BRANCHES = ('fixed', 'minus', 'plus', 'symmetric')
CONFIGS = ('main', 'time_half', 'fine_half', 'fine_quarter')


def load():
    docs = [json.loads((OUT / (name + '.json')).read_text(encoding='utf-8'))
            for name in ('scan', 'refinement')]
    rows = {}
    for d in docs:
        assert d['plan'].keys() == d['rows'].keys()
        for key, row in d['rows'].items():
            assert key not in rows and row['spec'] == d['plan'][key]
            rows[key] = row
    return docs, rows


def key(p, route, branch, config):
    return f'p{p:.6f}_{route}_{branch}_{config}'


def worker(item):
    name, r = item
    spec = r['spec']; file = Path(r['profile'])
    assert sha(file) == r['profile_sha256'], name
    a = np.load(file)
    ih = hashlib.sha256(a['z0'].tobytes()+a['s0'].tobytes()).hexdigest()
    if 'initial_hash' in r: assert ih == r['initial_hash'], name
    p = SymmetricProblem(Parameters(spec['a'], spec['p'], spec['q'], spec['rho']),
                         **{k: spec[k] for k in ('route','branch','nx','h','L','yhalf')})
    z0, s0 = p.initial()
    assert np.array_equal(z0,a['z0']) and np.array_equal(s0,a['s0']), name
    ans = dict(initial_hash=ih, readback=0., evaluation_change=0., reconstruction_change=0.,
               initial_error=evaluate(p,z0,s0,0.,evaluation_factor=8), snapshots={})
    for ts, sn in r['snapshots'].items():
        t = float(ts); z, s = a[f't{ts}_z'], a[f't{ts}_s']
        ev = evaluate(p,z,s,t,evaluation_factor=8)
        bands = high_band(p,z,s,t)
        ans['snapshots'][ts] = dict(errors=ev, bands=bands, geometry=p.geometry(t,z,s))
        for f in ('u','v'):
            ans['readback'] = max(ans['readback'],abs(ev[f]-sn['evaluation_double'][f]))
            ans['evaluation_change'] = max(ans['evaluation_change'],abs(ev[f]/sn['errors'][f]-1))
            ans['reconstruction_change'] = max(ans['reconstruction_change'],abs(sn['reconstruction_double'][f]/sn['errors'][f]-1))
    # Resolve maxima more densely in the five-point candidate band and at delicate rankings.
    if ((.9 <= spec['p'] <= 1.1 and spec['branch'] in ('fixed','minus'))
        or (spec['p'] in PVALUES and spec['branch']=='symmetric')):
        z,s=a['t0.01_z'],a['t0.01_s']
        ans['dense_error']=evaluate(p,z,s,.01,evaluation_factor=32,reconstruction_factor=32)
        ans['dense_change']=max(abs(ans['dense_error'][f]/ans['snapshots']['0.01']['errors'][f]-1) for f in ('u','v'))
    return name,ans


def main():
    docs, rows=load()
    hashes={}
    for d in docs:
        for group in ('source_hashes','comparison_manifests'):
            for path,hh in d[group].items():
                if path in hashes: assert hashes[path]==hh
                hashes[path]=hh
    for path,hh in hashes.items(): assert sha(path)==hh,path
    audited={}
    with ProcessPoolExecutor(max_workers=4) as pool:
        fs=[pool.submit(worker,it) for it in rows.items()]
        for future in as_completed(fs):
            k,r=future.result();audited[k]=r
            if len(audited)%32==0: print(f'Audited {len(audited)}/{len(rows)}',flush=True)
    assert max(r['readback'] for r in audited.values()) < 1e-14
    pairs=0
    for k,r in rows.items():
        s=r['spec']
        if s['route']=='sd':
            assert audited[k]['initial_hash']==audited[key(s['p'],'fd',s['branch'],s['config'])]['initial_hash']
            pairs+=1
        if not r['reused'] and s['branch']!='fixed':
            assert r['steps_with_nonzero_mesh_velocity']==r['steps']
    def err(p,route,branch,config,t=.01,dense=False):
        r=audited[key(p,route,branch,config)]
        return r['dense_error'] if dense else r['snapshots'][str(t)]['errors']
    def ratio(a,b):return {f:a[f]/b[f] for f in ('u','v')}
    ratios={};winners={};sensitivity=[];csvrows=[]
    for k,r in rows.items():
        s=r['spec'];p=s['p'];c=s['config'];b=s['branch'];route=s['route'];ar=audited[k]
        ratios[k]={'moving_to_fixed':ratio(err(p,route,b,c),err(p,route,'fixed',c))}
        if route=='sd':ratios[k]['sd_to_fd']=ratio(err(p,'sd',b,c),err(p,'fd',b,c))
        for ts,snap in ar['snapshots'].items():
            csvrows.append(dict(key=k,p=p,route=route,branch=b,config=c,nx=s['nx'],h=s['h'],dt=s['dt'],t=float(ts),
                status=r['status'],reused=r['reused'],E_u=snap['errors']['u'],E_v=snap['errors']['v'],
                high_fraction_u=snap['bands']['u']['high_band_nodal']/snap['bands']['u']['total_nodal'],
                high_fraction_v=snap['bands']['v']['high_band_nodal']/snap['bands']['v']['total_nodal'],
                J_min=snap['geometry']['min_J'],R_min=snap['geometry']['min_R']))
    for p in PVALUES:
        for c in CONFIGS[:3]:
            for route in ('fd','sd'):
                es={b:err(p,route,b,c) for b in BRANCHES}
                win={f:min(es,key=lambda b:es[b][f]) for f in ('u','v')}
                near={f:[b for b in BRANCHES if es[b][f]<=1.02*es[win[f]][f]] for f in ('u','v')}
                winners[f'{p}_{route}_{c}']=dict(strict=win,within_two_percent=near)
    for p in sorted({s['spec']['p'] for s in rows.values()}):
        for route in ('fd','sd'):
            for b in BRANCHES:
                for c0,c1 in (('main','time_half'),('fine_half','fine_quarter')):
                    if key(p,route,b,c1) not in rows:continue
                    e0,e1=err(p,route,b,c0),err(p,route,b,c1)
                    sensitivity.append(dict(p=p,route=route,branch=b,configs=[c0,c1],
                        error_ratio=ratio(e1,e0),max_relative_change=max(abs(e1[f]/e0[f]-1) for f in ('u','v'))))
    band={}
    for p in (.9,.95,1,1.05,1.1):
        for c in CONFIGS:
            if key(p,'sd','minus',c) not in rows:continue
            band[f'{p}_{c}']=dict(sd_fd=ratio(err(p,'sd','minus',c),err(p,'fd','minus',c)),
                dense_sd_fd=ratio(err(p,'sd','minus',c,dense=True),err(p,'fd','minus',c,dense=True)),
                minus_fixed=ratio(err(p,'sd','minus',c),err(p,'sd','fixed',c)),
                earlier_sd_fd=ratio(err(p,'sd','minus',c,t=.005),err(p,'fd','minus',c,t=.005)))
    audit=dict(records=len(rows),new=sum(not r['reused'] for r in rows.values()),
        reused=sum(r['reused'] for r in rows.values()),completed=sum(r['status']=='completed' for r in rows.values()),
        verified_hashes=len(hashes),verified_profiles=len(audited),paired_initial_states=pairs,
        error_readback_max=max(r['readback'] for r in audited.values()),
        evaluation_change=max(r['evaluation_change'] for r in audited.values()),
        reconstruction_change=max(r['reconstruction_change'] for r in audited.values()),
        dense_change=max(r.get('dense_change',0.) for r in audited.values()),
        candidate_dense_change=max(r.get('dense_change',0.) for k,r in audited.items() if .9<=rows[k]['spec']['p']<=1.1 and rows[k]['spec']['branch'] in ('fixed','minus')),
        minimum_J=min(r['minimum_J'] for r in rows.values()),
        minimum_R=min(s['geometry']['min_R'] for r in audited.values() for s in r['snapshots'].values()),
        failures=[k for k,r in rows.items() if r['status']!='completed'],
        new_moving_every_step=True,
        all_main_time_change=max(r['max_relative_change'] for r in sensitivity if r['configs'][0]=='main'),
        all_fine_time_change=max(r['max_relative_change'] for r in sensitivity if r['configs'][0]=='fine_half'))
    dump(OUT/'summary.json',dict(audit=audit,ratios=ratios,winners=winners,sensitivity=sensitivity,candidate_band=band,readback=audited))
    with (OUT/'errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(csvrows[0]));writer.writeheader();writer.writerows(csvrows)
    rcsv=[]
    for k,r in ratios.items():
        for comparison,values in r.items():rcsv.append(dict(key=k,comparison=comparison,u=values['u'],v=values['v']))
    with (OUT/'ratios.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rcsv[0]));writer.writeheader();writer.writerows(rcsv)
    print(json.dumps(audit,indent=2));print(json.dumps(band,indent=2))


if __name__=='__main__':main()
