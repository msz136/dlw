"""Independent 1000-node check; leaves main-paper 2001-node results intact."""
import json
import numpy as np
from conserved_mesh import ROOT,ale,run,reference

rows=[];saved={}
for ci,p in enumerate([(5.,),(1.1,1.25)]):
 sol=ale.Soliton(p)
 for mi,mode in enumerate(['fixed','rm']):
  x,u,r,low=run(sol,mode,.0005,n=999)
  xh,uh,rh,_=run(sol,mode,.00025,n=999)
  ue,re,_,_=reference(sol,x,.25);mask=abs(x)<=2.5
  eu=abs(u-ue);er=abs(r-re)
  row=dict(case=['One soliton','Two solitons'][ci],method=['Fixed FD','Conserved-density moving FD'][mi],nodes=len(x),u=float(max(eu[mask])),rho=float(max(er[mask])),dt_halving_change=float(max(np.max(abs(x-xh)),np.max(abs(u-uh)),np.max(abs(r-rh)))),min_h=low[0],min_rho=low[1],min_Rm=low[2],metric='native nodes in [-2.5,2.5]')
  rows.append(row);print(json.dumps(row),flush=True)
  for q,a in [('x',x),('u',u),('rho',r),('eu',eu),('er',er)]:saved[f'{ci}_{mi}_{q}']=a
(ROOT/'data/mesh_1000_nodes.json').write_text(json.dumps(rows,indent=2))
np.savez_compressed(ROOT/'data/mesh_1000_nodes.npz',**saved)
