"""Produce concise, auditable snapshot source budgets and refinement orders."""
from pathlib import Path
import csv
import json
import math

HERE=Path(__file__).resolve().parent


def load(stem,case):
    with (HERE/f'{stem}_{case}.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    for r in rows:
        for k in r:
            if k not in ('case','scan','model','region','field','source','backend','term'):
                r[k]=float(r[k])
    return rows


def main():
    baselines, orders, buffer_changes = [], [], []
    for case in ('A','C'):
        corr=load('source_correlations',case)
        metrics=load('source_metrics',case)
        for kind in ('SD','FD'):
            for field in ('u','v'):
                base=next(r for r in corr if r['scan']=='snapshot' and r['t']==0 and r['model']==kind and r['field']==field and r['region']=='observation')
                record={k:base[k] for k in ('case','model','field','rms_y','rms_x','rms_wrap','rms_total','cosine_y_x','cancellation_ratio')}
                record.update(y_energy=base['rms_y']**2,x_energy=base['rms_x']**2,
                              cross_energy=2*base['rms_y']*base['rms_x']*base['cosine_y_x'])
                record['energy_budget_relative_residual']=abs(record['y_energy']+record['x_energy']+record['cross_energy']-base['rms_total']**2)/base['rms_total']**2
                baselines.append(record)
                for scan, source, var in [('h_refine','y_model','h'),('dx_refine','x_stencil','dx')]:
                    series=[r for r in metrics if r['model']==kind and r['field']==field and r['region']=='observation' and r['source']==source
                            and (r['scan']==scan or r['scan']=='snapshot' and r['t']==0)]
                    series.sort(key=lambda r:r[var],reverse=True)
                    for first,second in zip(series,series[1:]):
                        orders.append(dict(case=case,model=kind,field=field,source=source,coarse=first[var],fine=second[var],
                                           coarse_rms=first['rms'],fine_rms=second['rms'],order=math.log(first['rms']/second['rms'])/math.log(first[var]/second[var])))
                for r in corr:
                    if r['model']==kind and r['field']==field and r['region']=='observation' and r['scan'] in ('x_buffer','y_buffer'):
                        buffer_changes.append(dict(case=case,model=kind,field=field,scan=r['scan'],extra=r['value'],
                            y_rms_change=r['rms_y']-base['rms_y'],x_rms_change=r['rms_x']-base['rms_x'],total_rms_change=r['rms_total']-base['rms_total']))
    for name,rows in [('baseline_source_budget',baselines),('source_refinement_orders',orders),('source_buffer_changes',buffer_changes)]:
        with (HERE/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={'baseline':baselines,'refinement_orders':orders,'max_buffer_change':{k:max(abs(r[k]) for r in buffer_changes) for k in ('y_rms_change','x_rms_change','total_rms_change')}}
    (HERE/'source_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Baselines:',json.dumps(baselines,indent=2))
    print('Refinement orders:',json.dumps(orders,indent=2))
    print('Buffer:',result['max_buffer_change'])


if __name__=='__main__':
    main()
