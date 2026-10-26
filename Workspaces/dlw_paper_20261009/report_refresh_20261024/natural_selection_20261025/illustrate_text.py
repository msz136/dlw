"""Insert the six-case figure narrative into the proposed numerical text."""
from pathlib import Path
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
FIGS=HERE/'figures'
PREFIX='../Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_selection_20261025/figures/'
CASES=['A','B','C','D','Gaussian','Sinusoidal']
PROFILES={
'A':'Case A contains a single oblique wave with negative pulses in both physical fields. The heatmaps show the wave band across the region, while the central sections resolve its pulse shape. This gives a simple localized profile on which to compare the two physical components.',
'B':'Case B has a positive ridge in u and a negative trough in v. Its amplitude, width and orientation also differ from Case A, so the two one-soliton tests examine distinct spatial scales within the same exact solution family.',
'C':'Case C combines two positive u ridges with different orientations. They meet in a region of higher amplitude, and the corresponding v field contains two negative troughs whose shapes change near the interaction. The heatmaps identify both wave branches and their meeting region; the central sections pass through this spatial structure.',
'D':'Case D combines the parameter pairs used in A and B. A stronger negative u trough appears together with a smaller positive ridge, while both v wave bands remain negative. The approximation must therefore resolve two features of different polarity and strength within the same first field.',
'Gaussian':'The Gaussian test starts from a positive localized u profile with a sinusoidal envelope in y. The second field varies about v=4, lying below this value in the lower half of the region and above it in the upper half. Both variations inherit the same localized Gaussian dependence on x.',
'Sinusoidal':'The sinusoidal test replaces the Gaussian factor by cos(πx/12). The u field alternates in sign along x, while the oscillatory deviation of v from its background reverses its transverse sign across y=0. The displayed window contains two periods and provides a periodic counterpart to the localized Gaussian profile.'}
FINAL_TEXT={
'A':'In Case A, the central profiles compare the pulse shapes directly, and the section-error panels resolve differences that are small on the scale of the fields. FD gives the smallest global u error, while Centered-SD gives the smallest v error. Relative to Endpoint-SD, the centered formulation improves both components at the final time.',
'B':'The three methods show similar error levels in Case B. The section panels display their agreement with the reference along y=0, while the heatmaps locate the deviations across the full region. The common color scales make the close magnitudes of the three error fields visible.',
'C':'Case C has closely grouped global u errors, all near 1.15 × 10⁻⁴. The v errors remain more separated: Endpoint-SD gives 5.442 × 10⁻⁴, Centered-SD gives 1.049 × 10⁻⁵ and FD gives 8.998 × 10⁻⁶. The two-dimensional maps show how these errors are distributed around the interacting wave profiles.',
'D':'For the mixed-polarity waves in Case D, the central sections resolve the negative and positive parts of u within the same panel. Centered-SD reduces both final errors relative to Endpoint-SD. Its v error is also smaller than FD, while FD retains the smallest u error.',
'Gaussian':'The Gaussian profiles remain close to the continuous reference after the short evolution. The u section compares the localized pulse, while the v section shows preservation of the central background value. The v heatmaps resolve the errors away from this symmetry line, where the three spatial formulations are more clearly separated.',
'Sinusoidal':'The sinusoidal sections compare the oscillatory first field over two periods. The exact v section remains at its background value, and its spatial error is resolved in the off-axis heatmaps. Centered-SD gives the smallest global v error, retaining the advantage already seen in the initial derivative comparison.'}
RATE_TEXT={
'A':'For the one-soliton profile A, Endpoint-SD gives the smallest u_t defect and Centered-SD the smallest v_t defect. The paired plots compare the analytic derivatives along the central section and locate the corresponding discrepancies in the plane.',
'B':'Case B combines the smallest initial u_t defect from Endpoint-SD with the smallest v_t defect from FD. The common field scales show the larger Endpoint-SD discrepancy in the second derivative component.',
'C':'In Case C, the derivative profiles pass through the interaction of the two waves. Endpoint-SD gives the smallest u_t defect, while FD gives the smallest v_t defect; Centered-SD substantially reduces the second-component discrepancy relative to Endpoint-SD.',
'D':'The mixed-polarity Case D separates the advantages of the two semi-discrete formulations at the initial state. Endpoint-SD gives the smallest u_t defect, while Centered-SD gives the smallest v_t defect. The maps show these errors over both wave branches.',
'Gaussian':'The Gaussian derivative comparison follows the same ranking as the final-field comparison. Endpoint-SD gives the smallest first-component defect and Centered-SD the smallest second-component defect. The central v_t reference is zero by symmetry, while its error varies away from y=0.',
'Sinusoidal':'The sinusoidal derivatives have a repeated spatial structure. The central first-component comparison resolves the oscillatory time derivative; the v_t reference is zero on y=0. The full error maps display the transverse variation responsible for the second-component norms.'}
def chunk(html):
    soup=BeautifulSoup(html,'html.parser')
    return list(soup.contents)
def figure(stem,label,caption):
    assert (FIGS/(stem+'.png')).exists(),stem
    assert (FIGS/(stem+'.pdf')).exists(),stem
    return f'<figure id="figure-{label}"><img src="{PREFIX}{stem}.png" alt="{caption}" loading="lazy"><figcaption><strong>Figure {label}.</strong> {caption} <a class="export" href="{PREFIX}{stem}.pdf">PDF</a></figcaption></figure>'
def exact_figure(case):
    label=CASES.index(case)+1
    caption=f'Exact initial physical fields for {case}. Upper row: u; lower row: v. Central sections at y=0 are on the left, and x–y heatmaps are on the right. The dashed line marks y=0.'
    if case in ('Gaussian','Sinusoidal'):
        caption+=' The central v section equals 4; the displayed x window is [−24,24].'
    return '<p>'+PROFILES[case]+'</p>'+figure(f'exact_{case}_initial',label,caption)
def final_pair(case,label):
    caption=f'{case}: physical-field sections at y=0 and T=0.01. Left: continuous reference (black solid curves) and numerical values (symbols). Right: absolute errors along the same section. Numerical values use their native sites when available, otherwise a local 12-point polynomial reconstruction in y; selected x nodes carry symbols.'
    if case in ('Gaussian','Sinusoidal'):
        caption+=' The central second-field panel displays v−4 and uses the global field-error scale; the exact value is zero.'
    s=figure(f'final_{case}_sections',label,caption)
    s+='<p>The corresponding heatmaps compare all three methods over the region. Each row uses one common linear color scale, so its colors represent the same absolute error in every method.</p>'
    caption=f'{case}: absolute physical-field errors at T=0.01. Columns: Endpoint-SD, Centered-SD, FD. Rows: u and v. Errors are evaluated at the native field positions. RK4 uses Δt=10⁻⁴ with h=Δx=0.1.'
    if case in ('Gaussian','Sinusoidal'):caption+=' The plots show x∈[−24,24]; tabulated maxima use the full periodic interval.'
    return s+figure(f'final_{case}_errors',label+1,caption)
def illustrate(body):
    soup=BeautifulSoup(body,'html.parser')
    sect=soup.find(id='section-5.1')
    anchor=next(p for p in sect.find_all('p',recursive=False) if p.get_text().startswith('The regions contain'))
    for node in reversed(chunk(''.join(exact_figure(c) for c in CASES[:4]))):anchor.insert_after(node)
    anchor=next(p for p in sect.find_all('p',recursive=False) if p.get_text().startswith('For these two initial-value'))
    for node in reversed(chunk(''.join(exact_figure(c) for c in CASES[4:]))):anchor.insert_after(node)
    sect=soup.find(id='section-5.2')
    # Keep the numerical discussion together, then follow each case through its figures.
    after=next(p for p in sect.find_all('p',recursive=False) if p.get_text().startswith('The centered field definition'))
    s='<h4>Physical-field sections and spatial error distributions</h4><p>The following figures pair a fixed central section with the complete spatial error map for each case. The exact fields are evaluated at y=0. The numerical section reconstruction is used consistently across all methods, while the heatmaps retain their native field locations.</p>'
    for j,c in enumerate(CASES):s+='<h5>'+c+'</h5><p>'+FINAL_TEXT[c]+'</p>'+final_pair(c,7+2*j)
    for node in reversed(chunk(s)):after.insert_after(node)
    s='<details id="initial-rate-figures"><summary>Initial time-derivative figures for all six cases</summary><p>These figures accompany Table 2. Each case includes the analytic and numerical y=0 sections of u_t and v_t, followed by their absolute-error heatmaps. The method order and color convention are the same as in the terminal-field figures.</p>'
    for j,c in enumerate(CASES):
        s+='<h4>'+c+'</h4><p>'+RATE_TEXT[c]+'</p>'
        cap=f'{c}: initial time-derivative sections. Black curves show the analytic continuous derivatives, and symbols show the three spatial formulations at y=0. Right panels show absolute section errors. The same 12-point reconstruction is used where y=0 lies between native sites.'
        if c in ('Gaussian','Sinusoidal'):cap+=' The exact v_t section is zero by symmetry.'
        s+=figure(f'initial_{c}_rates','S'+str(2*j+1),cap)
        s+='<p>The maps locate the initial derivative discrepancy over the region and show its relative size for the three formulations.</p>'
        cap=f'{c}: absolute initial u_t and v_t errors, evaluated at native positions. Each field shares a linear color scale across Endpoint-SD, Centered-SD and FD. The grid spacings are h=Δx=0.1.'
        s+=figure(f'initial_{c}_errors','S'+str(2*j+2),cap)
    s+='</details>'
    for node in chunk(s):sect.append(node)
    # Add a direct link next to the initial table rather than duplicating its figures.
    table=sect.find(id='table-initial').parent
    table.insert_after(BeautifulSoup('<p class="figure-link"><a href="#initial-rate-figures" onclick="document.getElementById(\'initial-rate-figures\').open=true">Initial derivative sections and error maps for all six cases</a></p>','html.parser'))
    return str(soup)
