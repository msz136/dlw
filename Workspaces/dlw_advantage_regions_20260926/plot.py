"""Scientific figures: mode-level theorem and independently predicted error sources."""
from scan import HERE,OUT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'font.size':10})
fig,ax=plt.subplots(figsize=(7.5,3.8))
q=np.linspace(.01,3.99,2000)
ratio=np.abs(1-q/3)/np.abs(q*q/4-q/3)
ax.plot(q,np.minimum(ratio,5),color='#3b5e76',lw=2)
ax.axhline(1,color='gray',ls='--',lw=1);ax.axvspan(2,4,color='#7cb09c',alpha=.2)
ax.set(xlabel=r'$-\xi\eta$ (oscillatory sector: $0<-\xi\eta<4$)',ylabel='SD / FD leading eigenfrequency error',ylim=(0,4),xlim=(0,4))
ax.text(2.15,3.4,'SD advantage: 2 < -xi*eta < 4',fontsize=10)
ax.set_title('A proved Fourier-mode criterion; not a nonlinear field-error bound')
fig.tight_layout();fig.savefig(HERE/'dispersion_advantage.png',dpi=180);fig.savefig(HERE/'dispersion_advantage.pdf');plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(11.5,4),sharey=True)
for ax,method,title in zip(axs,('fd','original'),('P6: ordinary FD','P6: original integrable semidiscretization')):
    data=np.load(OUT/f'propagation_P6_main_{method}.npz')
    i,j=np.unravel_index(np.argmax(abs(data['u_actual'])),data['u_actual'].shape)
    xx=-10+np.arange(data['u_actual'].shape[1])*20/data['u_actual'].shape[1]
    use=abs(xx)<2
    for key,label,color,ls in [('u_actual','actual total','#1e2529','-'),('u_predicted','linear prediction','#718c3b',':'),('u_x','x error response','#456d89','--'),('u_y','y/closure error response','#b87646','-.')]:
        ax.plot(xx[use],data[key][i,use]*1e4,label=label,color=color,ls=ls,lw=1.7)
    ax.set(title=title,xlabel='x');ax.axhline(0,color='gray',lw=.5);ax.grid(alpha=.15)
axs[0].set_ylabel(r'$u$ error ($\times10^{-4}$)');axs[1].legend(fontsize=8)
fig.suptitle('Different signed y responses change how the total error adds up',fontsize=12)
fig.tight_layout();fig.savefig(HERE/'p6_error_sources.png',dpi=180);fig.savefig(HERE/'p6_error_sources.pdf');plt.close(fig)
print('Two scientific figures generated')
