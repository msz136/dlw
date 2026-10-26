"""Outward-rounded constants for the v=4 shifted mixed-time problem."""
from pathlib import Path
import json
from flint import arb,ctx
ctx.prec=256
HERE=Path(__file__).resolve().parent

def main():
    rho=arb('.1'); eps=arb('1e-6'); k=arb.pi()/2
    kap=arb.pi()/4
    cases={}
    for name,A in [('sine',arb('.03')),('gaussian',arb('.05'))]:
        if name=='sine':fn=(rho*arb.pi()/12).exp()
        else:
            # rho*r <= r^2+rho^2/4; Gaussian sum bounded by 1+integral.
            w=arb.pi()/96; C=arb.pi().sqrt()/32
            fn=C*(rho*rho/4).exp()*(1+arb.pi().sqrt()/(arb(8).sqrt()*w))
        B0=4*A*kap*fn
        perturb_v=eps*(rho*k).exp()
        perturb_u=eps*kap*(rho*k).exp()
        cases[name]={'base_B0_norm_upper':str(B0),
            'independent_u_B0_norm_upper':str(B0+perturb_u),
            'independent_v_B0_norm_upper':str(B0+perturb_v),
            'allowed_terminal_A_norm_if_d_0_3':str(arb('.3')-B0-perturb_v)}
        assert B0+perturb_v<arb('.2')
    rows=[]
    for st in ['.01','.02']:
        T=arb(st);h=(T/2).sqrt();R=arb('.4');d=arb('.3')
        image=d+2*h*R*R;lip=4*h*R
        assert image<R and lip<1
        rows.append({'T':st,'image_norm_upper':str(image),'contraction_upper':str(lip)})
    out={'shifted_full_equations':'A_t=-A_xx-(u*A)_x; B_t=B_xx-(u*B)_x',
       'rho':'.1','z_interval':[0,4],'x_period':192,'ball_radius':'.4','mixed_datum_bound':'.3',
       'independent_perturbation_amplitude':'1e-6','carrier':'cos(pi*x/2)','y_envelope':'sin(pi*z/4)^2',
       'mixed_constants':rows,'initial_data_bounds':cases,
       'initial_matching_proved':False,'certified':False,'eta_u':None,'eta_v':None}
    (HERE/'independent_constants.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
