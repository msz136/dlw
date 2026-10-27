from pathlib import Path
import sys,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'hs_numerics_plan'))
from hs_exact import Soliton
from hs_solver import MovingSystem,solve
OUT=ROOT/'data';FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
colors=['#2878B5','#E47C25','#27946B']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'lines.linewidth':1.6,'savefig.dpi':300})
def save(fig,name):
 fig.savefig(FIG/(name+'.png'),bbox_inches='tight');fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
