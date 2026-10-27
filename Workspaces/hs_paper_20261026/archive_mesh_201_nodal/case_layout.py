"""Build case-by-case figure/table blocks from unchanged terminal tables."""
from bs4 import BeautifulSoup
from pathlib import Path
import json
def apply(rep,fig,sci,mesh):
 def split(key,case,label):
  soup=BeautifulSoup(rep[key],'html.parser')
  for tr in list(soup.select('tbody tr')):
   if tr.find('td').get_text()!=case:tr.decompose()
  if key=='TABLE_SPATIAL':
   soup.select('thead th')[2].string='Spacing'
   for tr in list(soup.select('tbody tr')):
    if tr.find_all('td')[1].get_text()=='Moving FD':tr.decompose()
   raw=json.loads((Path(__file__).parent/'data/results.json').read_text())['spatial']
   for tr in soup.select('tbody tr'):
    cells=tr.find_all('td');symbol=r'\Delta x' if cells[1].get_text()=='Fixed FD' else 'a'
    step=float(cells[2].get_text());method=cells[1].get_text()
    subset=[d for d in raw if d['case']==case and d['spacing']==step and d['method']!='Moving FD']
    item=next(d for d in subset if d['method']==method)
    for col,q in [(3,'u'),(5,'rho')]:
     if item[q]==min(d[q] for d in subset):
      bold=soup.new_tag('b')
      for child in list(cells[col].contents):bold.append(child.extract())
      cells[col].append(bold)
    if method=='Fixed FD':cells[1].string='FD'
    cells[2].string=r'\('+symbol+'='+cells[2].get_text()+r'\)'
  if key=='TABLE_MESH_EVOLUTION':
   selected=[d for d in mesh if d['case']==case]
   for tr,d in zip(soup.select('tbody tr'),selected):
    cells=tr.find_all('td')
    for col,q in enumerate(['u','rho','common_u','common_rho'],2):
     if d[q]==min(v[q] for v in selected):
      bold=soup.new_tag('b')
      for child in list(cells[col].contents):bold.append(child.extract())
      cells[col].append(bold)
  numbers={'2a':'1','2b':'2','3a':'3','3b':'4','4a':'5','4b':'6','5a':'7','5b':'8'}
  cap=soup.caption;txt=cap.get_text();cap.string='Table '+numbers.get(label,label)+'. '+txt.split('. ',1)[1]
  if key=='TABLE_MESH_EVOLUTION':cap.append(' Bold values indicate the smaller error in each column for this case.')
  if key=='TABLE_SPATIAL':cap.append(' Bold values indicate the smaller field error at each nominal spacing.')
  return str(soup)
 spatial_table=rep['TABLE_SPATIAL'];time_table=rep['TABLE_TIME'];mesh_table=rep['TABLE_MESH_EVOLUTION'];response_table=rep['TABLE_RESPONSE']
 profiles=[];spatial=[];temporal=[];meshes=[];responses=[]
 for i,case in enumerate(['One soliton','Two solitons']):
  letter='ab'[i];title=['One-soliton case','Two-soliton case'][i]
  profiles.append('<h4>'+title+'</h4><p>'+['The velocity consists of one smooth localized peak, accompanied by a density depression. These two features locate the region where the field curvature and natural cell width change most strongly.','The two-soliton profile contains two resolved peaks with different heights and a corresponding pair of density depressions. This gives the mesh two distinct regions to resolve within the same physical interval.'][i]+'</p>'+fig(i+1,[f'profile_mid_{i}'],title+': continuous exact velocity and density at T=0.125.'))
  spatial.append('<h4>'+title+'</h4><p>'+['We first examine the single localized wave. The terminal table measures the refinement rates, while the midpoint curves show where the differences develop in physical space.','The second case places two wave structures in the computational interval. We use the same refinement and midpoint sampling to examine how their different amplitudes affect the two field errors.'][i]+'</p>'+split('TABLE_SPATIAL',case,'2'+letter)+'<p>'+['Figure 3 compares the numerical velocity and density with the exact profiles at the midpoint. The lower panels display the corresponding absolute errors, locating the differences that are summarized by the terminal table.','Figure 4 makes the same midpoint comparison for the two-soliton case. Its field panels show how the two wave structures are resolved, and its error panels show where the numerical profiles depart from the reference.'][i]+'</p>'+fig(i+3,[f'spatial_mid_{i}'],title+': fields and spatial errors at T=0.125, with nominal spacing 0.02 and RK4 step 0.0005. Black curves are continuous point values; colored symbols are computed samples. Moving-cell density errors use exact cell averages.')+'<p>'+['The direct FD samples closely follow the exact wave at this resolution. Integrable SD develops a broader velocity discrepancy on the downstream side and larger density errors than the direct formulations. Its density discrepancy is nevertheless much smaller in absolute magnitude than its velocity discrepancy. Table 2 confirms that the direct formulations retain smaller errors in their respective field metrics across the tested resolutions.','Integrable SD again has the larger field errors, with its velocity discrepancy extending downstream of the localized waves. The density errors vary more locally around the two depressions. The direct FD formulations resolve both structures more closely in the displayed comparison, and Table 3 records smaller terminal errors throughout the tested resolutions. Thus the additional wave structure changes the magnitude and distribution of the errors while preserving the overall pattern seen in the one-soliton case.'][i]+'</p>')
  temporal.append('<h4>'+title+'</h4><p>'+['For the single wave, all three time integrators start on the same exact lattice trajectory. Their differences therefore measure how accurately they advance that trajectory.','The two-wave profile tests the same time algorithms on a more structured lattice trajectory. Both components are measured against the matching exact finite-lattice solution.'][i]+'</p>'+split('TABLE_TIME',case,'3'+letter)+fig(i+5,[f'time_{i}'],title+': maximum temporal errors on the integrable lattice; a=0.02 and ΔT=0.0025.')+'<p>The curves summarize the largest error over the lattice at each time. Euler accumulates the largest error, Crank–Nicolson reduces it substantially, and RK4 follows the exact trajectory most closely at the displayed step. The refinement table identifies the corresponding temporal orders.</p>'+'<details><summary>Spatial distribution of the temporal error — '+title.lower()+'</summary><p>In these maps, the horizontal coordinate is the exact lattice position and the vertical coordinate is time. Each horizontal row is one spatial error profile. Color gives the absolute error at matching lattice labels, interpolated onto the displayed exact-position axis. Each panel uses its own color scale. The maps locate the temporal error within the wave; the curves above give its maximum magnitude.</p>'+fig('S'+str(i+1),[f'temporal_maps_{i}'],title+': space–time distribution of temporal integration errors for Euler, RK4 and Crank–Nicolson. References are the exact finite-lattice fields, not the continuous fields.')+'</details>')
  d0,d1=mesh[2*i:2*i+2]
  meshes.append('<h4>'+title+'</h4><p>'+['The one-soliton density depression widens the natural cells near the velocity peak. Curvature-adapted labels place additional resolution around the parts of the profile that bend most strongly.','The two-soliton profile requires resolution around two separate structures. The initial monitor responds to both, producing a more varied distribution of cell widths during the evolution.'][i]+'</p>'+split('TABLE_MESH_EVOLUTION',case,'4'+letter)+fig(i+7,[f'moving_mesh_{i}'],title+': moving FD with uniform and curvature-adapted initial labels, 201 nodes, T=0.25. Left: cell widths. Center and right: native velocity and density errors.')+f'<p>The adapted labels reduce the native velocity and density errors by factors of {d0["u"]/d1["u"]:.2f} and {d0["rho"]/d1["rho"]:.2f}. After reconstruction onto common physical points, the factors are {d0["common_u"]/d1["common_u"]:.2f} and {d0["common_rho"]/d1["common_rho"]:.2f}. The error curves show where this gain occurs, while the width panel connects it with the changed node allocation. Both meshes retain positive cells; halving the time step changes the terminal states by less than {sci(max(d0["dt_half_state_change"],d1["dt_half_state_change"]))}.</p>')
  responses.append('<h4>'+title+'</h4><p>We apply the velocity-only perturbation to this background and follow each spatial method against its own unperturbed trajectory. The density starts unchanged, so its response records the subsequent transfer through the coupled equations.</p>'+fig(i+9,[f'response_{i}'],title+': normalized velocity and density responses to a velocity perturbation of amplitude 10⁻⁶, at matching native indices.')+split('TABLE_RESPONSE',case,'5'+letter)+'<p>The moving-label velocity response grows over the interval and generates a density response. The fixed-position calculation also develops a density response while its velocity response remains below its initial maximum at the terminal time. The table reports these histories’ terminal values and their sensitivity to amplitude and time-step halving within each formulation.</p>')
 clean_temporal=BeautifulSoup(''.join(temporal),'html.parser')
 for block in clean_temporal.find_all('details'):block.decompose()
 spatial_html=''.join(spatial).replace('spatial_mid_','spatial_sd_fd_').replace('direct formulations','FD formulation').replace('direct FD formulations','FD formulation').replace('direct FD samples','FD samples').replace('The direct FD formulations resolve','The FD formulation resolves').replace('Table 2 confirms','Table 1 confirms').replace('Table 3 records','Table 2 records').replace('FD formulation retain','FD formulation retains').replace('FD formulation resolve','FD formulation resolves')
 comparison=json.loads((Path(__file__).parent/'data/conserved_mesh.json').read_text())
 meshes=[]
 for i,case in enumerate(['One soliton','Two solitons']):
  entries=[d for d in comparison if d['case']==case]
  tab=f'<div class="table-wrap"><table><caption>Table {i+5}. FD mesh comparison under RK4 at T=0.25, with 201 nodes and time step 0.0005. Errors are measured at each method’s computational nodes in [-2.5,2.5]. Bold values are the smallest in each error column.</caption><thead><tr><th class="label">Method</th><th class="number">E<sub>u</sub></th><th class="number">E<sub>ρ</sub></th></tr></thead><tbody>'
  for d in entries:
   tab+='<tr><td class="label">'+d['method']+'</td>'
   for q in ['u','rho']:
    value=sci(d[q]);value='<b>'+value+'</b>' if d[q]==min(v[q] for v in entries) else value
    tab+='<td class="number">'+value+'</td>'
   tab+='</tr>'
  tab+='</tbody></table></div>'
  fixed,adaptive=entries
  reductions=[100*(1-adaptive[q]/fixed[q]) for q in ['u','rho']]
  introduction=['The single wave provides a direct test of the allocation predicted by the conserved density. Figure 7 relates the terminal cell widths to the spatial distribution of the two field errors.','For the two-soliton profile, the same density allocates nodes around both wave structures. Figure 8 shows how this redistribution changes the errors across the common physical interval.'][i]
  observation=['The moving grid has smaller cells around the localized wave and wider cells in the background. The density error decreases, while the fixed grid gives the smaller velocity error.','The nonuniform widths resolve the two wave structures with the same total node count. Both maximum errors decrease, with a larger relative reduction in density than in velocity.'][i]
  meshes.append('<h4>'+['One-soliton case','Two-soliton case'][i]+'</h4><p>'+introduction+'</p>'+tab+fig(i+7,[f'conserved_mesh_{i}'],case+': fixed and conserved-density moving FD at T=0.25. Left: physical cell widths. Center and right: absolute errors at the actual computational nodes in [-2.5,2.5]; lines connect consecutive samples.')+f'<p>{observation} Relative to fixed FD, the velocity error {"decreases" if reductions[0]>=0 else "increases"} by {abs(reductions[0]):.1f}%, and the density error {"decreases" if reductions[1]>=0 else "increases"} by {abs(reductions[1]):.1f}%. The minimum moving-cell width during evolution is {adaptive["min_h"]:.4f}, and the computed density and mesh monitor remain positive. Halving the RK4 step changes the terminal nodal states by less than {sci(max(d["dt_halving_change"] for d in entries))}.</p>')

 rep.update(FIG_PROFILES=''.join(profiles),FIG_SPATIAL=spatial_html,FIG_TIME=str(clean_temporal),FIG_MESH_EVOLUTION=''.join(meshes),FIG_RESPONSE=''.join(responses))
