"""Add only the DLW temporal CN experiment, preserving all other saved cells."""
from pathlib import Path
import sys, os, time, json, shutil, hashlib, copy
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=PROJECT.parents[1]
sys.path.insert(0,str(PROJECT))
from dlw_numeric_cells import CELLS

path=ROOT/'notebook/DLW数值分析report.ipynb'
backup=HERE/'before';backup.mkdir(exist_ok=True)
for original in (path, ROOT/'dlw_numerical.html'):
    if not (backup/original.name).exists():shutil.copy2(original,backup/original.name)
original=nbformat.read(path,4)
nb=nbformat.read(path,4);lookup={c.id:c for c in nb.cells}
lookup['dlw-time'].source=CELLS['time'].strip()
lookup['dlw-time_experiment'].source=CELLS['time_experiment'].strip()
formula=r'''

时间算法比较另加入 Crank–Nicolson（C–N）：

$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$

这是二阶隐式梯形法，采用迭代求解并检查隐式方程残差。
'''
if 'Crank–Nicolson' not in lookup['dlw-time-text'].source:
    lookup['dlw-time-text'].source += formula
lookup['dlw-temporal-text'].source=lookup['dlw-temporal-text'].source.replace(
    'Euler 与 RK4。','Euler、RK4 与 Crank–Nicolson。保持相同的初值、空间格距、时间步长 $\\Delta t=0.000125$ 和终点 $T=0.01$。其他实验的时间算法保持原设置。')
definitions=[]
for cell in nb.cells:
    if cell.cell_type=='code': definitions.append(cell)
    if cell.id=='dlw-time':break

export=nbformat.v4.new_code_cell(f'''
from pathlib import Path
import json
rows=[]
for r in results.values():
    row={{k:r[k] for k in ('case','model','method','mesh','completed','reached','max_errors')}}
    row['completed']=bool(row['completed'])
    if r['method']=='CN':
        diag=r['cn_diagnostics']
        assert len(diag)==round(CONFIG['T']/CONFIG['dt'])
        assert all(d['residual']<=d['tolerance'] for d in diag)
        row.update(max_iterations=max(d['iterations'] for d in diag),
            max_residual=max(d['residual'] for d in diag),
            max_residual_ratio=max(d['residual']/d['tolerance'] for d in diag))
    assert r['completed'],r['reason']
    rows.append(row)
# Independent checks distinguish implicit trapezoidal from explicit predictors and midpoint.
lambda_value=-2.
got=step(lambda t,z:lambda_value*z,0.,np.array([1.]),.05,'CN')[0]
expected=(1+.05*lambda_value/2)/(1-.05*lambda_value/2)
assert abs(got-expected)<2e-11,(got,expected)
errors=[]
for dt in (.1,.05,.025):
    z=np.array([1.])
    for i in range(round(1/dt)):
        z=step(lambda t,z:-z*z,i*dt,z,dt,'CN')
    errors.append(abs(z[0]-.5))
orders=np.log2(np.array(errors[:-1])/errors[1:])
assert np.all((orders>1.95)&(orders<2.05)),orders
assert abs(step(lambda t,z:np.full_like(z,t*t),0.,np.array([0.]),.1,'CN')[0]-.0005)<1e-14
Path({str(HERE/'results.json')!r}).write_text(json.dumps(dict(rows=rows,
    scalar_trapezoidal_check=True,nonautonomous_endpoint_check=True,
    nonlinear_second_order=orders.tolist(),config=CONFIG),indent=2),encoding='utf-8')
''',id='cn-validation')
temp=nbformat.v4.new_notebook(cells=copy.deepcopy(definitions+[lookup['dlw-space_experiment'],lookup['dlw-time_experiment'],export]))
for c in temp.cells:
    if c.cell_type=='code':compile(c.source,c.id,'exec')
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
started=time.perf_counter()
NotebookClient(temp,km=km,timeout=600,allow_errors=False,
    resources={'metadata':{'path':str(ROOT)}},
    on_cell_start=lambda cell,cell_index,**kw:print('Executing',cell.id,flush=True)).execute(
    env={**os.environ,'MPLBACKEND':'module://matplotlib_inline.backend_inline'})
for id in ('dlw-time','dlw-time_experiment'):
    executed=next(c for c in temp.cells if c.id==id)
    lookup[id].outputs=executed.outputs
    lookup[id].execution_count=executed.execution_count
    lookup[id].metadata=executed.metadata
allowed={'dlw-time','dlw-time_experiment','dlw-time-text','dlw-temporal-text'}
for old in original.cells:
    if old.id not in allowed:assert old==lookup[old.id],old.id
nbformat.validate(nb);nbformat.write(nb,path)
validation=dict(success=True,seconds=time.perf_counter()-started,new_runs=9,
    only_temporal_experiment_changed=True,unchanged_other_cells=True,
    notebook_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    source_reference='Paper/sources/gsg.txt: Scheme 5, equations (4.13)-(4.14)',
    interpretation='CN temporal endpoint averaging adapted to existing DLW RHS; no GSG spatial equation copied')
(HERE/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2),flush=True)
