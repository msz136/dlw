"""Plot controlled long-distance transport separately from DLW accuracy gates."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'out/moving_mesh'


def main():
    transport=json.loads((BASE/'route1_transport.json').read_text())
    gates=json.loads((BASE/'route1_dlw_gate.json').read_text())
    idx={(r['parameter_id'],r['nx'],r['mode']):r for r in transport['runs']}
    colors={'P1':'#2563eb','P2':'#ea580c','P7':'#16a34a','P10':'#9333ea'}
    fig,axes=plt.subplots(1,2,figsize=(10.5,4),constrained_layout=True)
    max_pass=max(r['last_passed']['D'] for r in gates['runs'] if r['last_passed'])
    axes[0].axvspan(0,max_pass,color='#cbd5e1',alpha=.4,
                    label='observed DLW 1% window')
    for pid,color in colors.items():
        moving=idx[pid,128,'moving']['observations']
        frozen=idx[pid,128,'static_adaptive']['observations']
        for field,style in (('u','-'),('v','--')):
            axes[0].plot([r['D'] for r in moving],
                         [a[f'{field}_common_error']/b[f'{field}_common_error']
                          for a,b in zip(moving,frozen)],
                         style,marker='o',color=color,label=f'{pid} {field}')
    axes[0].axhline(1,color='black',lw=.8)
    axes[0].axhline(.8,color='gray',lw=.8,ls=':')
    axes[0].set(xlabel='travel / initial width',
                ylabel='moving / frozen field error',
                title='Transport field solve, 128 x nodes',ylim=(0,1.6))
    axes[0].legend(ncol=2,fontsize=7)
    for pid,color in colors.items():
        for field,marker in (('u','o'),('v','x')):
            values=[]
            for nx in (64,128,256):
                a=idx[pid,nx,'moving']['observations'][-1]
                b=idx[pid,nx,'static_adaptive']['observations'][-1]
                values.append(a[f'{field}_common_error']/b[f'{field}_common_error'])
            axes[1].plot((64,128,256),values,marker=marker,color=color,
                         label=f'{pid} {field}')
    axes[1].axhline(1,color='black',lw=.8)
    axes[1].axhline(.8,color='gray',lw=.8,ls=':')
    axes[1].set(xlabel='number of x nodes',
                ylabel='moving / frozen field error',
                title='After two widths: resolution check',
                xticks=(64,128,256),ylim=(0,1.25))
    axes[1].legend(ncol=2,fontsize=7)
    dest=ROOT/'figures/fig20_route1_transport.png'
    fig.savefig(dest,dpi=170)
    print(dest)


if __name__=='__main__':main()
