"""One error distribution per figure: Euler, physical x in [-1,1]."""
from pathlib import Path
import csv
import importlib.util
import json
import hashlib
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
ROOT = HERE.parents[2]
FIG = HERE/'figures'
FIG.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('dlw_saved_plot', PARENT/'plot_fields.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
SELECT = (original.XX >= -1.) & (original.XX <= 1.)
XX = original.XX[SELECT]
YY = original.YY
EXTENT = (XX[0]-(XX[1]-XX[0])/2, XX[-1]+(XX[1]-XX[0])/2, -1.5, 1.5)
assert len(XX) == 401 and XX[0] == -1 and XX[-1] == 1


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    plt.rcParams.update({'font.family':'DejaVu Serif', 'font.size':12,
        'axes.linewidth':.7, 'xtick.direction':'in', 'ytick.direction':'in',
        'axes.spines.top':False, 'axes.spines.right':False,
        'pdf.fonttype':42, 'savefig.facecolor':'white'})
    refs = {c: original.reference(c, XX, YY, .01) for c in original.CASES}
    errors, records, archive = {}, [], {'x':XX, 'y':YY}
    previous = json.loads((PARENT/'plot_validation.json').read_text(encoding='utf-8'))
    runs = {k:r for k,r in original.saved_runs().items() if k[1]=='Euler'}
    assert len(runs) == 18
    with np.load(PARENT/'plotted_fields.npz', allow_pickle=False) as old:
        for key, run in runs.items():
            case, method, mesh, model = key
            assert sha(run['profile']) == run['profile_sha256']
            with np.load(run['profile'], allow_pickle=False) as saved:
                assert np.array_equal(saved['y'], YY)
                for field in original.FIELDS:
                    sampled = CubicSpline(saved['t0.01_x'], saved['t0.01_'+field], axis=-1)(XX)
                    error = np.abs(sampled-refs[case][field])
                    prior_error = old['_'.join(key)+'_abs_error_'+field][:,SELECT]
                    discrepancy = float(np.max(np.abs(error-prior_error)))
                    assert discrepancy < 1e-12
                    errors[(*key,field)] = error
                    archive['_'.join(key)+'_abs_error_'+field] = error
                    j,i = np.unravel_index(np.argmax(error),error.shape)
                    prior = next(r for r in previous['records'] if all(r[k]==v for k,v in
                        dict(case=case,method=method,mesh=mesh,model=model,field=field).items()))
                    records.append(dict(case=case,method=method,mesh=mesh,model=model,field=field,
                        cropped_max=float(error.max()), max_x=float(XX[i]), max_y=float(YY[j]),
                        original_full_max=prior['full_max'], crop_readback_difference=discrepancy,
                        profile=run['profile'],profile_sha256=run['profile_sha256']))
    color_limits = {c:{f:max(r['cropped_max'] for r in records if r['case']==c and r['field']==f)
                        for f in original.FIELDS} for c in original.CASES}
    figures = []
    for case in original.CASES:
        for mesh in ('fixed','moving'):
            for field in original.FIELDS:
                for model in original.MODELS:
                    key = (case,'Euler',mesh,model,field)
                    error = errors[key]
                    record = next(r for r in records if tuple(r[k] for k in ('case','method','mesh','model','field'))==key)
                    upper = color_limits[case][field]
                    fig,ax = plt.subplots(figsize=(6.6,5.7),layout='constrained')
                    im = ax.imshow(error,extent=EXTENT,origin='lower',interpolation='nearest',
                        aspect='auto',cmap='magma',norm=PowerNorm(.5,vmin=0,vmax=upper))
                    ax.plot(record['max_x'],record['max_y'],'+',color='#4edcc5',ms=9,mew=1.3)
                    ax.set(xlim=(-1,1),ylim=(-1.5,1.5),xlabel='$x$',ylabel='$y$')
                    ax.set_xticks([-1,-.5,0,.5,1]); ax.set_yticks([-1.5,-1,-.5,0,.5,1,1.5])
                    fig.colorbar(im,ax=ax,shrink=.88,label=f'$|{field}_h-{field}_*|$')
                    label = original.model_label(case,'Euler',mesh,model)
                    ax.set_title(f'{original.CASES[case][1]} | Euler / {mesh} / {label}\n'
                        f'$|{field}_h-{field}_*|$, t=0.01; window max={record["cropped_max"]:.3e}',fontsize=12.5,pad=10)
                    assert len(fig.axes)==2  # One distribution and its colorbar.
                    paths = []
                    stem = f'{case}_euler_{mesh}_{model.lower()}_{field}_error_xm1p1'
                    for ext in ('png','pdf'):
                        path = FIG/f'{stem}.{ext}'
                        fig.savefig(path,dpi=200)
                        paths.append(str(path.relative_to(ROOT)).replace('\\','/'))
                    plt.close(fig)
                    figures.append(dict(case=case,method='Euler',mesh=mesh,model=model,field=field,
                        png=paths[0],pdf=paths[1],cropped_max=record['cropped_max'],color_upper=upper,
                        distribution_axes=1,colorbar_axes=1))
            print(f'Plotted {case} Euler {mesh}: six separate error figures',flush=True)
    np.savez_compressed(HERE/'euler_cropped_errors.npz',**archive)
    with (HERE/'euler_cropped_errors.csv').open('w',encoding='utf-8-sig',newline='') as handle:
        writer = csv.DictWriter(handle,fieldnames=list(records[0]))
        writer.writeheader();writer.writerows(records)
    result = dict(time=.01,method='Euler',x_interval=[-1.,1.],x_points=401,y_points=24,
        y_interval=[-1.5,1.5],source_runs=18,error_fields=36,png_figures=36,pdf_figures=36,
        color_scale='PowerNorm(gamma=0.5); same case/field scale across models and mesh strategies; ticks retain absolute-error units',
        reconstruction='Existing 0.005 x spacing, default CubicSpline; original 24 y layers without interpolation',
        maximum_crop_readback_difference=max(r['crop_readback_difference'] for r in records),
        source_archive=dict(path=str(PARENT/'plotted_fields.npz'),sha256=sha(PARENT/'plotted_fields.npz')),
        color_limits=color_limits,records=records,figures=figures)
    (HERE/'euler_plot_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('source_runs','error_fields','png_figures','maximum_crop_readback_difference')}))


if __name__=='__main__':
    main()
