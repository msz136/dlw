"""Validated linear matching scales and a nonlinear-base smoothing bound.

The numerical values below do NOT certify a continuous IVP reference.
"""
from pathlib import Path
import json
from flint import arb, ctx
ctx.prec=256
HERE=Path(__file__).resolve().parent

def main():
    T=arb('.01'); eta=arb('1e-10')
    rows=[]
    for dxs in ['.1','.05','.025']:
        dx=arb(dxs); k=arb.pi()/dx
        growth=(T*k*k).exp()
        fdgrowth=(4*T/(dx*dx)).exp()
        rows.append({'dx':dxs,'continuum_resolved_cutoff_pi_over_dx':str(k),
          'continuum_linear_inverse_amplification':str(growth),
          'initial_A_matching_scale_for_terminal_1e_10':str(eta/growth),
          'centered_second_difference_inverse_amplification':str(fdgrowth),
          'centered_second_difference_matching_scale':str(eta/fdgrowth)})
    # This is a theorem conditional on the explicitly stated analytic base bound.
    # It applies to any nonzero mixed solution in that ball, not just zero.
    rho=arb('.1'); sigma=arb('.1'); R=arb('.4')
    h_sigma=T.sqrt()*(sigma*sigma/(2*T)).exp()
    lipschitz=4*R*h_sigma
    boundary=(sigma*sigma/(4*T)).exp()
    C=boundary/(1-lipschitz)
    assert lipschitz<1
    smooth={'rho':str(rho),'sigma':str(sigma),'T':str(T),
      'required_base_norm_at_rho_plus_sigma':str(R),
      'differentiated_heat_bound':str(h_sigma),
      'linear_contraction_bound':str(lipschitz),
      'DF_H_norm_rho_to_rho_plus_sigma_upper':str(C),
      'actual_benchmark_base_enclosure_completed':False,
      'inverse_bound_exists_in_same_Wiener_space':False,
      'same_radius_high_input_corollary':{
        'required_base_radius':'.1','required_base_norm_upper':'.4',
        'input_normalization':'||g_N||_.1=1, single x frequency xi_N',
        'output_bound':'||DF_H g_N||_.1 <= C*exp(-.1*abs(xi_N))',
        'constant_C_upper':str(C),
        'requires_transverse_compactness':False}}
    # Exact derivative at zero of the matching linearization with respect to
    # the sine benchmark amplitude. At z=2, f=phi=1, f'=0. This is the first
    # Born coefficient, not the full derivative at amplitude .03.
    q=arb.pi()/12
    born=[]
    for ks in ['carrier','.1','.05','.025']:
        k=arb.pi()/2 if ks=='carrier' else arb.pi()/arb(ks)
        p=k+q; delta=p*p-k*k
        jminus=(1-(-(delta-q*q)*T).exp())/(delta-q*q)
        jplus=(1-(-(delta+q*q)*T).exp())/(delta+q*q)
        derivative=p/2*(-T*k*k).exp()*(-jminus+2*jplus)
        preconditioned=p/2*((T*delta).exp())*(-jminus+2*jplus)
        born.append({'input':ks,'k':str(k),
           'sideband_k_plus_q_abs_d_amplitude_DF':str(abs(derivative)),
           'inverse_heat_preconditioned_sideband_abs_d_amplitude_DF':str(abs(preconditioned)),
           'first_order_contribution_at_sine_amplitude_0_03':str(arb('.03')*abs(preconditioned))})
    # A constructive first correction for independently prescribed initial
    # alpha=delta A0 and beta=delta B0. It includes beta, not only terminal g.
    corrections=[]
    k=arb.pi()/2; kap=arb.pi()/4; eps=arb('1e-6')
    def J(d):
        return (1-(-T*d).exp())/d
    for kind,z in [('independent_v',arb(2)),('independent_u',arb(1))]:
        f=(kap*z).sin(); fp=kap*(kap*z).cos()
        phi=f*f; iphi=z/2-(2*kap*z).sin()/(4*kap)
        if kind=='independent_v': alpha=beta=phi; ia=ib=iphi
        else: alpha=kap*(2*kap*z).sin(); beta=-alpha; ia=phi; ib=-phi
        for sign in [1,-1]:
            q=sign*arb.pi()/12;p=k+q
            bracket=-(f*alpha+fp*ia)*J(2*k*q)+2*f*alpha*J(2*q*p)+fp*ib*J(2*k*p)
            value=p/2*(T*p*p).exp()*bracket
            corrections.append({'kind':kind,'z':str(z),'q_sign':sign,
                'absolute_terminal_first_correction_for_eps_1e_6_lambda_0_03':str(abs(eps*arb('.03')*value))})
    # Gaussian q-tail for this first correction only, in terminal X_.1 norm.
    # Sum over both q signs and the real cosine carrier. The |q|+k bound is
    # valid for all four signed sidebands.
    wg=arb.pi()/96; Cg=arb.pi().sqrt()/32; N=128
    q1=(N+1)*wg;a=9-T;b=2*T*k+rho;c=T*k*k+rho*k
    first=(q1+k)*(-a*q1*q1+b*q1+c).exp()
    ratio=(q1+wg+k)/(q1+k)*(-a*wg*(2*q1+wg)+b*wg).exp()
    assert ratio<1
    gaussian_tail={}
    for kind,shape in [('independent_v',3+4*kap),('independent_u',5*kap)]:
        tail=eps*arb('.05')*2*T*Cg*shape*first/(1-ratio)
        gaussian_tail[kind]=str(tail)
    out={'linearization_background':'u=0, v=4; X=x-4t',
         'time':'.01','target_terminal_A_coefficient':'1e-10',
         'grid_scales':rows,'nonzero_base_analytic_smoothing':smooth,
         'sine_first_Born_sideband':born,
         'first_initial_matching_terminal_correction':corrections,
         'gaussian_first_correction_tail_X_0_1_after_n_128':gaussian_tail,
         'certified':False,'eta_u':None,'eta_v':None}
    (HERE/'matching_conditioning.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
