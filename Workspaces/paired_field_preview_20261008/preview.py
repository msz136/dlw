"""Paired physical-field/error candidates using real notebook solvers.

Reads both notebooks without modifying them. DLW uses x,y at fixed t;
2HS uses x,t because this model has one spatial coordinate.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter, MaxNLocator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PATHS = [ROOT/'notebook'/n for n in ('DLW数值分析report.ipynb','2HS数值分析report.ipynb')]
hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PATHS}
cells = [{c['id']:''.join(c['source']) for c in json.loads(p.read_text(encoding='utf-8'))['cells']} for p in PATHS]
ns = {}
for key in ('dlw-imports','dlw-config','dlw-reference','dlw-spatial','dlw-sd_fd','dlw-sd',
            'dlw-sd2_lift','dlw-sd2_evolution','dlw-fd','dlw-mesh','dlw-time'):
    exec(cells[0][key],ns)
r = ns['solve']('C','SD2','RK4','moving')
assert r['completed'] and np.isclose(r['reached'],.01)
take = (r['x']>=-5)&(r['x']<=5)
dlw = dict(x=r['x'][take], second=r['y'], axis='$y$',
           fields=[v[:,take] for v in r['fields']],
           errors=[r['errors'][k][:,take] for k in ('u','v')],
           keys=('u','v'), title='DLW Case C | SD2, RK4, moving mesh | t=0.01')
print('DLW trajectory complete',flush=True)

# Independent direct four-term tau derivatives for current C parameters.
G = ns['Exact']('C',.125)
xcheck = np.linspace(-5,5,151); yy=.37; tt=.01
e1 = np.exp(xcheck-11*tt-yy/12); e2 = np.exp(xcheck-7*tt-yy/2)
def derivatives(a,b,c):
    tau=1+a*e1+b*e2+c*e1*e2
    tx=a*e1+b*e2+2*c*e1*e2
    ty=-a*e1/12-b*e2/2-7*c*e1*e2/12
    txy=-a*e1/12-b*e2/2-7*c*e1*e2/6
    return tx/tau,(txy*tau-tx*ty)/tau**2
gx,gxy=derivatives(1,1,4/3)
fx,fxy=derivatives(4/3,2,32/9)
direct=(2*(fx-gx),2*(fxy+gxy))
reference=G.uv([yy/.125-.5],xcheck,tt)
tau_difference=max(np.max(abs(v-w[0])) for v,w in zip(direct,reference))
assert tau_difference<1e-12

# Show exact long-time profiles to distinguish soliton count from visible peaks.
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],
                     'mathtext.fontset':'stix','font.size':11})
fig,axes=plt.subplots(1,3,figsize=(11,3.2),layout='constrained')
peak_counts={}
for ax,time in zip(axes,(-2.,.01,2.)):
    center=9*time; xx=np.linspace(center-12,center+12,2401)
    u=G.uv([-.5],xx,time)[0][0]
    peaks,_=find_peaks(u,prominence=.02)
    peak_counts[str(time)] = {'count':len(peaks),'x':xx[peaks].tolist()}
    ax.plot(xx,u,color='#1776bc',lw=1.7)
    ax.plot(xx[peaks],u[peaks],'o',color='#d47b19',ms=4)
    ax.set(xlabel='$x$',ylabel='$u(x,0,t)$',title=f't={time:g}')
    ax.grid(alpha=.12)
fig.suptitle('Case C: exact two-soliton profiles | y=0 | extended times are analytic only')
fig.savefig(HERE/'two_soliton_check.png',dpi=170,bbox_inches='tight')
plt.close(fig)

hs={}
for key in ('hs-prepare','hs-config','hs-reference','hs-spatial','hs-fd-spatial',
            'hs-initial-state','hs-rk4','hs-interpolation','hs-two-reference'):
    exec(cells[1][key],hs)
hs['hs_one_results']={}; hs['hs_results']={}
exec(cells[1]['hs-two-initial'],hs)
state,_=hs['hs_initial_states']()
xx=np.linspace(-5,5,401); times=[]; values=[[],[]]; errors=[[],[]]
for step in range(hs['hs_steps']+1):
    time=step*hs['hs_dt']
    if step%5==0 or step==hs['hs_steps']:
        f=hs['hs_integrable_fields'](time,state)
        exact=hs['hs_exact_physical'](xx,time)
        times.append(time)
        for i,key in enumerate(('u','rho')):
            coordinates=f['x'] if key=='u' else f['rhoX']
            v=hs['hs_interpolate'](coordinates,f[key],xx)
            values[i].append(v); errors[i].append(abs(v-exact[key]))
    if step<hs['hs_steps']:
        state=hs['hs_rk4_step'](hs['hs_integrable_rhs'],time,state,hs['hs_dt'])
assert np.isfinite(state).all() and np.all(np.diff(f['x'])>0)
hsdata=dict(x=xx,second=np.array(times),axis='$t$',fields=list(map(np.array,values)),
            errors=list(map(np.array,errors)),keys=('u',r'\rho'),
            title='2HS two solitons | Integrable, RK4 | time history 0 to 0.5')
print('2HS time history complete',flush=True)
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],
                     'mathtext.fontset':'stix','font.size':11,'figure.dpi':110})

def render(data,style,name):
    fig=plt.figure(figsize=(11,7.5),layout='constrained')
    grid=fig.add_gridspec(2,2)
    xx,ss=np.meshgrid(data['x'],data['second'])
    for row,key in enumerate(data['keys']):
        for col,kind in enumerate(('fields','errors')):
            z=data[kind][row]
            label=f'${key}$' if col==0 else f'$|{key}_h-{key}_*|$'
            ax=fig.add_subplot(grid[row,col],projection=None if style=='map' else '3d')
            cmap='viridis' if col==0 else 'magma'
            if style=='map':
                im=ax.pcolormesh(xx,ss,z,shading='auto',cmap=cmap,rasterized=True)
                ax.set(xlabel='$x$',ylabel=data['axis'])
                bar=fig.colorbar(im,ax=ax,shrink=.85,label=label)
                if col: bar.formatter=ScalarFormatter(useMathText=True);bar.formatter.set_powerlimits((0,0));bar.update_ticks()
            else:
                stride=max(1,len(data['x'])//100)
                ax.plot_surface(xx[:,::stride],ss[:,::stride],z[:,::stride],
                                cmap=cmap,linewidth=.15,edgecolor=(1,1,1,.15),
                                rcount=len(data['second']),ccount=101)
                zmin,zmax=float(z.min()),float(z.max()); span=max(zmax-zmin,1e-14)
                floor=zmin-.25*span if style=='floor' else zmin
                if style=='floor':
                    ax.contourf(xx,ss,z,zdir='z',offset=floor,levels=12,cmap=cmap,alpha=.8)
                short_label=f'$e_{{{key}}}$' if col else label
                ax.set(xlabel='$x$',ylabel=data['axis'],zlabel=short_label,zlim=(floor,zmax+.04*span))
                ax.zaxis.set_rotate_label(False)
                ax.zaxis.label.set_rotation(0)
                ax.zaxis.labelpad=3
                ax.view_init(elev=27,azim=-58)
                ax.set_box_aspect((1.35,1,.8))
                ax.xaxis.set_major_locator(MaxNLocator(5));ax.yaxis.set_major_locator(MaxNLocator(4));ax.zaxis.set_major_locator(MaxNLocator(4))
                ax.tick_params(labelsize=9,pad=1)
                if col:
                    sf=ScalarFormatter(useMathText=True);sf.set_powerlimits((0,0));ax.zaxis.set_major_formatter(sf)
                for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
                    axis.pane.fill=True;axis.pane.set_facecolor((.97,.97,.97,1))
            ax.set_title(('Physical field: ' if col==0 else 'Absolute error: ')+label,fontsize=12)
    title={'box':'A. Boxed surfaces','floor':'B. Surfaces with floor maps','map':'C. Matched heatmaps'}[style]
    fig.suptitle(title+'\n'+data['title'],fontsize=14)
    fig.savefig(HERE/f'{name}_{style}.png',dpi=160,bbox_inches='tight',pad_inches=.65)
    fig.savefig(HERE/f'{name}_{style}.pdf',bbox_inches='tight',pad_inches=.65)
    plt.close(fig)

for name,data in (('dlw',dlw),('hs',hsdata)):
    for style in ('box','floor','map'):render(data,style,name)
np.savez_compressed(HERE/'data.npz',dlw_x=dlw['x'],dlw_y=dlw['second'],
                    dlw_u=dlw['fields'][0],dlw_v=dlw['fields'][1],
                    dlw_eu=dlw['errors'][0],dlw_ev=dlw['errors'][1],
                    hs_x=xx,hs_t=hsdata['second'],hs_u=hsdata['fields'][0],
                    hs_rho=hsdata['fields'][1],hs_eu=hsdata['errors'][0],hs_erho=hsdata['errors'][1])
for p in PATHS:assert hashes[p.name]==hashlib.sha256(p.read_bytes()).hexdigest()
report=dict(notebooks_unchanged=True,hashes=hashes,dlw_tau_direct_difference=float(tau_difference),
            exact_peak_counts=peak_counts,dlw_completed=bool(r['completed']),
            dlw_time=float(r['reached']),hs_final_time=float(times[-1]),hs_samples=len(times),
            coordinates={'DLW':'x,y; height is u,v or absolute error','2HS':'x,t; height is u,rho or absolute error'},
            scope='Candidate figures only; long-time soliton check uses analytic exact fields, not long-time numerical evolution.')
(HERE/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
