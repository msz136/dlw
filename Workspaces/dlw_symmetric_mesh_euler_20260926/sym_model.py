"""Exact symmetric combination; the frozen branch solver remains unchanged."""
from pathlib import Path
from types import SimpleNamespace
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'dlw_branch_mesh_euler_20260926'
sys.path.insert(0,str(BASE))
from model import BranchProblem,Parameters,evaluate


class SymmetricProblem(BranchProblem):
    def __init__(self,pars,route='sd',branch='symmetric',**kwargs):
        super().__init__(pars,route=route,branch=branch,**kwargs)

    def _view(self,branch):
        return SimpleNamespace(m=self.m,X=self.X,weights=self.weights,branch=branch)

    def density_flux(self,t,z):
        if self.branch!='symmetric':return super().density_flux(t,z)
        rm,qm=BranchProblem.density_flux(self._view('minus'),t,z)
        rp,qp=BranchProblem.density_flux(self._view('plus'),t,z)
        return (rm+rp)/2,(qm+qp)/2

    def density_time_derivative(self,t,z,physical_rhs):
        if self.branch!='symmetric':return super().density_time_derivative(t,z,physical_rhs)
        minus=BranchProblem.density_time_derivative(self._view('minus'),t,z,physical_rhs)
        plus=BranchProblem.density_time_derivative(self._view('plus'),t,z,physical_rhs)
        return (minus+plus)/2

    def initial_potential_density(self,x):
        if self.branch!='symmetric':return super().initial_potential_density(x)
        im,rm=BranchProblem.initial_potential_density(self._view('minus'),x)
        ip,rp=BranchProblem.initial_potential_density(self._view('plus'),x)
        return (im+ip)/2,(rm+rp)/2

    def direct_density(self,t,z):
        """Independent physical-field form, including the finite-h correction."""
        m=self.m;u,v=m.fields(z,t)
        w=v-m.dy(u,m.state_ghosts(u,t))
        r=1-v[1:-1]/4-(w[2:]-2*w[1:-1]+w[:-2])/32
        return np.einsum('j,jx->x',self.weights,r)
