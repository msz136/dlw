import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import ast,json,sys,hashlib
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2]
num=root/'Paper/dlw_semidiscrete/numerics'
sys.path.insert(0,str(num/'lib'))
from gramtau import ContRef
from solver import XGrid
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in num.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
src=ast.parse((num/'experiments/e7_fd_baseline.py').read_text(encoding='utf-8'))
funcs=[n for n in src.body if isinstance(n,ast.FunctionDef)]
X=XGrid(256,40,4); ys=np.linspace(-6,6,241); C=ContRef([1],[2],[3],4)
ns={'np':np,'X':X,'A':4.,'dy':ys[1]-ys[0],
    'U':np.array([C.u0_row(y,X.x,0) for y in ys]),
    'V':np.array([C.v0_row(y,X.x,0) for y in ys])}
exec(compile(ast.Module(body=funcs,type_ignores=[]),'e7_functions','exec'),ns)
ur,vr,_=ns['run'](.01/128,.01); rows=[]
for div in [2,4,8,16]:
    u,v,_=ns['run'](.01/div,.01)
    rows.append({'dt':.01/div,'error_v':float(np.max(abs(v-vr)))})
for i in range(1,len(rows)):rows[i]['order']=float(np.log2(rows[i-1]['error_v']/rows[i]['error_v']))
e6=[]
for nx in [64,128]:
    xg=XGrid(nx,60,4); theta=2*np.pi*(nx//8)/60
    vec=np.exp(1j*theta*xg.x)
    actual=(xg.D1@vec)[0]/vec[0]
    used=np.sin(theta*xg.dx)/xg.dx
    e6.append({'nx':nx,'actual_effective_k':float(actual.imag),'prediction_uses_k':float(used)})
e1=ast.parse((num/'experiments/e1_continuum.py').read_text(encoding='utf-8'))
norm=next(n for n in e1.body if isinstance(n,ast.FunctionDef) and n.name=='norms')
xs=np.linspace(-1.5,1.5,25); scope={'np':np,'DXW':xs[1]-xs[0]}
exec(compile(ast.Module(body=[norm],type_ignores=[]),'norm','exec'),scope)
unit=np.ones((12,25)); value=scope['norms'](unit,unit,.25,xs)[2]
out={'E7_live_source_self_convergence':rows,'E6_mode_mismatch':e6,'E1_constant_norm':{'computed':float(value),'rectangle_exact':3.0},'E5_index':{'declared_site':0,'actual_site':-6+(0-(-6+1))}}
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in num.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
assert before==after
out['production_unchanged']=True
Path(__file__).with_name('recheck_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
