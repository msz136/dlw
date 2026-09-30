"""Make the route-one geometry/field distinction visible from saved JSON."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'out'/'moving_mesh'


def main():
    geometry=json.loads((BASE/'route1_geometry.json').read_text(encoding='utf-8'))
    coupled=json.loads((BASE/'route1_coupled.json').read_text(encoding='utf-8'))
    fig,axes=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
    for case in geometry['cases']:
        rows=case['rows']
        for field,style in (('u','-'),('v','--')):
            y=[r['metrics']['moving_gram_oracle'][field]/
               r['metrics']['frozen_gram'][field] for r in rows]
            axes[0].plot([r['D'] for r in rows],y,style,marker='o',
                         label=f"{case['parameter_id']} {field}")
    axes[0].axhline(1,color='black',lw=.8)
    axes[0].set(xlabel='pulse displacement / initial width',
                ylabel='moving / frozen interpolation error',
                title='Exact-field sampling geometry')
    axes[0].legend(ncol=2,fontsize=7)
    grouped={(r['parameter_id'],r['model'],r['T'],r['mode']):r
             for r in coupled['runs'] if r['status']=='complete'}
    colors={'P1':'#2563eb','P2':'#ea580c','P7':'#16a34a','P10':'#9333ea'}
    for pid in colors:
        for model,marker in (('structure','o'),('fd','x')):
            xs=[];ys=[]
            for T in (.02,.04):
                a=grouped[(pid,model,T,'moving')]['observations'][-1]
                b=grouped[(pid,model,T,'static_adaptive')]['observations'][-1]
                xs.append(T);ys.append(a['v_common_error']/b['v_common_error'])
            axes[1].plot(xs,ys,marker=marker,color=colors[pid],
                         label=f'{pid} {model}')
    axes[1].axhline(1,color='black',lw=.8)
    axes[1].set(xlabel='time',ylabel='moving / frozen common-x v error',
                title='Coupled field solve: short reachable window',
                xlim=(.015,.045))
    axes[1].legend(ncol=2,fontsize=7)
    dest=ROOT/'figures'/'fig19_route1_mesh.png'
    fig.savefig(dest,dpi=170)
    print(dest)


if __name__=='__main__':main()
