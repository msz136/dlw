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
    out={'linearization_background':'u=0, v=4; X=x-4t',
         'time':'.01','target_terminal_A_coefficient':'1e-10',
         'grid_scales':rows,'nonzero_base_analytic_smoothing':smooth,
         'sine_first_Born_sideband':born,
         'certified':False,'eta_u':None,'eta_v':None}
    (HERE/'matching_conditioning.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
