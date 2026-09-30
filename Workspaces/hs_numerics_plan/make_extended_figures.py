"""Additional GSG-style numerical figures from measured 2-HS results."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hs_exact import Soliton

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'out';FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'figure.dpi':140,'savefig.dpi':180,'axes.grid':True,'grid.alpha':.22})
data=json.loads((OUT/'extended_methods.json').read_text())
mesh=json.loads((OUT/'mesh_representation.json').read_text())
snap=np.load(OUT/'snapshots.npz'); mesh_npz=np.load(OUT/'mesh_representation.npz')

# Figure 5: methods of orders 1, 2, 4 and 8 against the exact finite-a solution.
fig,axs=plt.subplots(1,2,figsize=(11,4))
for method in ('euler','heun','midpoint','trapezoid','rk4','rk8'):
    rows=sorted([r for r in data['semi_discrete']['rows'] if r['method']==method],key=lambda r:r['dt'])
    axs[0].loglog([r['dt'] for r in rows],[r['error']['u_linf'] for r in rows],'-o',label=method)
    axs[1].loglog([r['dt'] for r in rows],[r['error']['rho_linf'] for r in rows],'-o',label=method)
axs[0].set(xlabel='time step',ylabel='max u error',title='Finite-a exact single soliton')
axs[1].set(xlabel='time step',ylabel='max rho error',title='Density on moving edges')
axs[0].legend(ncol=2,fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig5_time_orders.png');plt.close(fig)

# Figure 6: direct fixed-grid finite differences and the time-error floor.
fig,axs=plt.subplots(1,2,figsize=(11,4))
space=data['fixed_grid_spatial']; dx=np.array([r['dx'] for r in space])
axs[0].loglog(dx,[r['u_linf'] for r in space],'-o',label='u')
axs[0].loglog(dx,[r['rho_linf'] for r in space],'-s',label='rho')
axs[0].loglog(dx,space[0]['u_linf']*(dx/dx[0])**2,':',color='.4',label='O(dx^2)')
axs[0].set(xlabel='fixed physical grid dx',ylabel='max error vs continuous exact',title='Direct finite difference spatial convergence')
axs[0].legend()
for method in ('euler','heun','midpoint','trapezoid','rk4','rk8'):
    rows=sorted([r for r in data['fixed_grid_time']['rows'] if r['method']==method],key=lambda r:r['dt'])
    axs[1].loglog([r['dt'] for r in rows],[r['temporal_state_linf'] for r in rows],'-o',label=method)
axs[1].set(xlabel='time step',ylabel='max state difference vs fine RK8',title='Time error at fixed dx=0.04')
axs[1].legend(ncol=2,fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig6_direct_fd.png');plt.close(fig)

# Figure 7: natural hodograph versus curvature-based representations.
fig,axs=plt.subplots(1,2,figsize=(11,4))
xx=mesh_npz['dense_x'];ue=mesh_npz['exact_u']
names=('natural','uniform','u_curvature','two_field_curvature')
labels=('2-HS natural','uniform physical','u monitor','two-field monitor')
for name,label in zip(names,labels):
    x=mesh_npz[f'{name}_x']
    mask=(x>=-.8)&(x<=1.2)
    axs[0].plot(x[mask],np.arange(len(x))[mask],'-',label=label)
axs[0].set(xlabel='physical x near crest',ylabel='node index',title='Equal-node mesh distribution')
rows={r['mesh']:r for r in mesh['rows'] if r['t']==.5}
pos=np.arange(len(names));width=.36
axs[1].bar(pos-width/2,[rows[n]['u_linf'] for n in names],width,label='u')
axs[1].bar(pos+width/2,[rows[n]['rho_linf'] for n in names],width,label='rho')
axs[1].set(xticks=pos,xticklabels=('natural','uniform','u monitor','two-field'),
           ylabel='max linear-interpolation error',yscale='log',title='Representation error only')
axs[0].legend(fontsize=8);axs[1].legend(fontsize=8)
fig.tight_layout();fig.savefig(FIG/'fig7_mesh_sampling.png');plt.close(fig)

# Figure 8: double-soliton error growth and failure of longer run.
fig,axs=plt.subplots(1,2,figsize=(11,4))
base=json.loads((OUT/'results.json').read_text())
for row in base['E4_collision']:
    axs[0].semilogy([r['t'] for r in row['stages']],
                    [max(r['metrics']['solver_u']['linf'],1e-17) for r in row['stages']],
                    '-o',label=f"RK4 dt={row['dt']:g}")
for row in data['collision_rk8']['T_to_3']:
    axs[0].semilogy([r['t'] for r in row['stages']],
                    [max(r['error']['u_linf'],1e-17) for r in row['stages']],
                    '--s',label=f"RK8 dt={row['dt']:g}")
axs[0].set(xlabel='time T',ylabel='max u error vs finite-a double soliton',title='Interaction window')
axs[0].legend(fontsize=7)
long=data['collision_rk8']['long']
tt=[r['t'] for r in long['stages']]
axs[1].semilogy(tt,[max(r['error']['u_linf'],1e-17) for r in long['stages']],'-o',label='RK8 u error')
axs[1].semilogy(tt,[r['error']['min_d'] for r in long['stages']],'-s',label='minimum edge d')
axs[1].axvline(tt[-1],color='r',ls=':',label='stop')
axs[1].set(xlabel='time T',ylabel='error / edge length',title='Long-window stopping diagnostic')
axs[1].legend(fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig8_collision_error.png');plt.close(fig)
# Figure 9: numerical points against the exact finite-a solution in both fields.
fig,axs=plt.subplots(2,2,figsize=(10,6),sharex='row')
for row,(prefix,ref,title) in enumerate((
    ('single',Soliton((5.,)),'Single soliton at T=1'),
    ('double',Soliton((1.1,1.25)),'Two-soliton interaction at T=3'))):
    t=float(snap[f'{prefix}_times'][-1]);a=.02;k=np.arange(-200,201)
    exact=ref.lattice_state(k,a,t)
    xn=snap[f'{prefix}_x'][-1];un=snap[f'{prefix}_u'][-1]
    rn=snap[f'{prefix}_rho'][-1]
    axs[row,0].plot(exact['x'],exact['u'],'k-',lw=1.4,label='exact finite-a')
    axs[row,0].plot(xn[::5],un[::5],'.',ms=2.5,label='numerical RK4')
    xm=(exact['x'][1:]+exact['x'][:-1])/2
    xnm=(xn[1:]+xn[:-1])/2
    axs[row,1].plot(xm,exact['rho'],'k-',lw=1.4,label='exact finite-a')
    axs[row,1].plot(xnm[::5],rn[::5],'.',ms=2.5,label='numerical RK4')
    axs[row,0].set(ylabel='u',title=title+' / u')
    axs[row,1].set(ylabel='rho on edges',title=title+' / rho')
    axs[row,0].legend(fontsize=7);axs[row,1].legend(fontsize=7)
axs[1,0].set(xlabel='physical x');axs[1,1].set(xlabel='physical x')
fig.tight_layout();fig.savefig(FIG/'fig9_exact_numeric.png');plt.close(fig)

# Figure 10: node trajectories and changing natural edge lengths.
fig,axs=plt.subplots(1,2,figsize=(10,4))
times=snap['single_times'];xx=snap['single_x']
for j in range(140,261,8):
    axs[0].plot(times,xx[:,j]-xx[0,j],color=plt.cm.viridis((j-140)/120),lw=1)
for i,t in enumerate(times):
    axs[1].plot((xx[i,1:]+xx[i,:-1])/2,np.diff(xx[i]),label=f'T={t:g}')
axs[0].set(xlabel='time T',ylabel='node displacement x_k(T)-x_k(0)',title='Natural moving-grid trajectories')
axs[1].set(xlabel='physical x',ylabel='edge length d',title='Grid expands near wave crest')
axs[1].legend(fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig10_grid_motion.png');plt.close(fig)
print('Wrote figures 5-10 in',FIG)
