"""Section 3.4 exact DLW surfaces. No time stepping.
Style: existing STIX/jet comparison plots; paired u/v surfaces, view (28,-62).
Edit CASES to change the provisional display windows.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
CASES = {
 "single_1_2": ([1.], [2.], (-5.,5.), (-5.,5.), r"One soliton: $p=1,\ q=2$"),
 "single_4_m3": ([4.], [-3.], (-10.,10.), (-10.,10.), r"One soliton: $p=4,\ q=-3$"),
 "two_soliton": ([6.,4.], [-5.,-3.], (-30.,30.), (-30.,30.),
 r"Two solitons: $(p_1,q_1)=(6,-5),\ (p_2,q_2)=(4,-3)$"),
 "two_soliton_mixed": ([1.,4.], [2.,-3.], (-30.,30.), (-30.,30.), r"Two solitons: $(p_1,q_1)=(1,2),\ (p_2,q_2)=(4,-3)$"),
}

def exact(p,q,x,y,t=0.):
    """Analytic log derivatives of positive exponential tau sums."""
    p,q=np.asarray(p),np.asarray(q)
    k=p+q
    ell=1/(p-2)+1/(q+2)
    c=-(p-2)/(q+2)
    theta=k[:,None,None]*x+ell[:,None,None]*y+(q*q-p*p)[:,None,None]*t
    terms=[np.zeros_like(x)]+[theta[i]-np.log(k[i]) for i in range(len(p))]
    ks,ls,cs=[0.,*k],[0.,*ell],[0.,*np.log(c)]
    if len(p)==2:
        interaction=(p[0]-p[1])*(q[0]-q[1])/((p[0]+q[1])*(p[1]+q[0]))
        terms += [terms[1]+terms[2]+np.log(interaction)]
        ks += [sum(k)]
        ls += [sum(ell)]
        cs += [sum(np.log(c))]
    terms=np.stack(terms)
    ks,ls=np.array(ks)[:,None,None],np.array(ls)[:,None,None]
    def derivatives(a):
        w=np.exp(a-a.max(axis=0))
        w/=w.sum(axis=0)
        dx=(w*ks).sum(axis=0)
        return dx,(w*ks*ls).sum(axis=0)-dx*(w*ls).sum(axis=0)
    fx,fxy=derivatives(terms+np.array(cs)[:,None,None])
    gx,gxy=derivatives(terms)
    return 2*(fx-gx),2*(fxy+gxy)

def main():
    plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","font.size":12})
    records=[]
    for name,(p,q,xlim,ylim,title) in CASES.items():
        x,y=np.meshgrid(np.linspace(*xlim,201),np.linspace(*ylim,201))
        fields=exact(p,q,x,y)
        fig=plt.figure(figsize=(10.8,4.8),layout="constrained")
        for i,(field,z) in enumerate(zip(("u","v"),fields)):
            assert np.isfinite(z).all()
            ax=fig.add_subplot(1,2,i+1,projection="3d")
            ax.plot_surface(x,y,z,cmap="jet",rcount=201,ccount=201,
                linewidth=0,antialiased=False,shade=False,rasterized=True)
            ax.set(xlabel="$x$",ylabel="$y$",zlabel="$"+field+"_*$",xlim=xlim,ylim=ylim)
            ax.set_title("("+chr(97+i)+") $"+field+"_*(x,y,0)$",pad=8)
            ax.view_init(28,-62)
            ax.set_box_aspect((1.15,1,.8))
            for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
                axis.set_major_locator(MaxNLocator(4))
            ax.xaxis.set_major_locator(MaxNLocator(4, integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(4, integer=True))
            ax.tick_params(labelsize=10,pad=1)
        fig.suptitle(title+r", $t=0$",fontsize=15)
        stem="exact_"+name
        fig.savefig(OUT/(stem+".png"),dpi=300)
        fig.savefig(OUT/(stem+".pdf"),dpi=200)
        (OUT/(stem+".py")).write_text("from pathlib import Path\nimport runpy\nrunpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_exact_solutions.py'),run_name='__main__')\n",encoding="utf-8")
        plt.close(fig)
        records.append(dict(case=name,t=0,xlim=xlim,ylim=ylim,
            extrema=[[float(z.min()),float(z.max())] for z in fields]))
    x,y=np.meshgrid(np.linspace(-2,2,17),np.linspace(-1,1,13))
    for p,q in ((1.,2.),(4.,-3.)):
        k,ell,c=p+q,1/(p-2)+1/(q+2),-(p-2)/(q+2)
        e=np.exp(k*x+ell*y)/k
        ref=(2*k*(c-1)*e/((1+c*e)*(1+e)),2*k*ell*(c*e/(1+c*e)**2+e/(1+e)**2))
        assert np.allclose(exact([p],[q],x,y),ref,atol=1e-13,rtol=1e-12)
    (OUT/"exact_solutions_validation.json").write_text(json.dumps(dict(plots=records,explicit_single_soliton_check=True),indent=2),encoding="utf-8")
    print(json.dumps(records))
if __name__=="__main__":
    main()
