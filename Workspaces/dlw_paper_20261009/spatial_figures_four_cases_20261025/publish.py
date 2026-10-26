"""Four-case presentation, preserving the other manuscript sections."""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json,hashlib,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SOURCE=(HERE/'before_dlw-paper.html').read_text(encoding='utf-8')
BASE=BeautifulSoup(SOURCE,'html.parser')
CASES=['A','C','Gaussian','Sinusoidal']
NAMES={'A':'One-soliton','C':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
PREFIX='Workspaces/dlw_paper_20261009/spatial_figures_four_cases_20261025/figures/'
FORMULAS=[]
def m(tex):
    token='FOURCASEMATH'+str(len(FORMULAS))+'END';FORMULAS.append(tex);return token
def frag(s):return BeautifulSoup(s,'html.parser')
def plain(e):
    d=BeautifulSoup(str(e),'html.parser')
    for k in d.select('.katex'):
        k.replace_with(k.select_one('annotation').get_text())
    return d.get_text(' ',strip=True)
def span(s,identity):
    f=re.search(r'<section\b[^>]*\bid="'+re.escape(identity)+r'"[^>]*>',s);assert f,identity
    depth=1
    for t in re.finditer(r'</?section\b[^>]*>',s[f.end():]):
        depth+=-1 if t.group().startswith('</') else 1
        if depth==0:return f.start(),f.end()+t.end()
    raise ValueError(identity)
def replace(s,identity,value):
    a,b=span(s,identity);return s[:a]+value+s[b:]
def filter_table(table):
    for tr in list(table.select('tbody tr')):
        name=tr.th.get_text(strip=True)
        if name not in CASES:tr.decompose()
        else:tr.th.string=NAMES[name]
    return str(table.parent)
def figure(case,stage,number):
    stem=('exact_' if stage=='exact' else 'initial_' if stage=='rate' else 'spatial_')+case
    name=NAMES[case]+' case'
    if stage=='exact':
        cap=name+'. Exact initial physical fields. Left: sections at '+m('y=0')+'; right: physical-field heatmaps, with the central section marked by a white dashed line. The upper and lower rows show '+m('u')+' and '+m('v')+', respectively.'
    else:
        field='initial time derivatives at '+m('t=0') if stage=='rate' else 'physical fields at '+m('T=0.01')
        cap=name+'. Comparison of the '+field+'. Panels (a,c): reference curves and numerical symbols at '+m('y=0')+'. Panels (b,d): absolute errors along the same section. The two lower rows show first- and second-component errors; columns correspond to Endpoint-SD, Centered-SD and FD. Each row shares a logarithmic color scale; light gray denotes values below the scale. Panel maxima cover the full table region.'
    if case=='C':cap+=' The section panels focus on '+m(r'x\in[-8,8]')+'; the heatmaps retain the full '+m('[-30,30]')+' window.'
    if case in ['Gaussian','Sinusoidal']:
        cap+=' The displayed '+m('x')+' window is '+m('[-18,18]' if case=='Gaussian' else '[-12,12]')+'; the error tables use the full periodic interval '+m('[-96,96)')+'.'
        cap+=' The exact central second field satisfies '+m('v(x,0,t)=4')+(' and '+m('v_t(x,0,0)=0') if stage=='rate' else '')+'.'
    return '<figure id="figure-'+str(number)+'"><img src="'+PREFIX+stem+'.png" alt="'+name+' '+stage+' field and error comparisons" loading="lazy"><figcaption><strong>Figure '+str(number)+'.</strong> '+cap+' <a class="export" href="'+PREFIX+stem+'.pdf">PDF</a></figcaption></figure>'

s51=frag(str(BASE.find(id='section-5.1'))).section
for f in list(s51.find_all('figure')):f.decompose()
for p in list(s51.find_all('p',recursive=False)):
    if plain(p).startswith(('Case A','Case B','Case C','Case D','The Gaussian test starts','The sinusoidal test replaces')):p.decompose()
s51.find('p').replace_with(frag('<p>All tests use '+m('a=2')+' and '+m(r'\lambda=-2')+'. The one- and two-soliton references are obtained from the continuous Gram determinant solutions in Section 2.1, with '+m(r'\rho_i=1')+' and zero phase shifts. Table 1 lists their spectral parameters and regions.</p>'))
table=s51.find(id='table-parameters')
for tr in list(table.select('tbody tr')):
    name=tr.th.get_text(strip=True)
    if name not in ['A','C']:tr.decompose()
    else:tr.th.string=NAMES[name]
# The descriptive case labels already specify the soliton count.
table.thead.tr.find_all('th')[1].decompose()
for tr in table.select('tbody tr'):tr.find_all('td')[0].decompose()
profiles={
'A':'The one-soliton case contains a single oblique wave with negative pulses in both physical fields. The heatmaps show its spatial orientation, while the central sections resolve the pulse shape.',
'C':'The two-soliton case combines two positive ridges in u with different orientations. They meet in a region of higher amplitude, while the corresponding v field contains two negative troughs. The heatmaps locate both wave branches and their interaction; the enlarged central sections show the resulting profiles along x.',
'Gaussian':'The Gaussian test starts from a positive localized u profile with a sinusoidal envelope in y. The second field varies about v=4, with opposite departures from this background in the lower and upper halves of the region. Its central section remains at four.',
'Sinusoidal':'The sinusoidal test replaces the Gaussian factor by cos(πx/12). The first field alternates in sign along x, while the deviation of the second field from its background reverses its transverse sign across y=0. The plots display one spatial period.'}
regions=next(p for p in s51.find_all('p',recursive=False) if plain(p).startswith('The regions contain'))
text=''.join('<p>'+profiles[c]+'</p>'+figure(c,'exact',i+1) for i,c in enumerate(['A','C']))
for node in reversed(list(frag(text).contents)):regions.insert_after(node)
ref=next(p for p in s51.find_all('p',recursive=False) if plain(p).startswith('For these two initial-value'))
text=''.join('<p>'+profiles[c]+'</p>'+figure(c,'exact',i+3) for i,c in enumerate(['Gaussian','Sinusoidal']))
for node in reversed(list(frag(text).contents)):ref.insert_after(node)

old=BASE.find(id='section-5.2')
initial=filter_table(frag(str(old.find(id='table-initial').parent)).find('table'))
final=filter_table(frag(str(old.find(id='table-final').parent)).find('table'))
ps=old.find_all('p',recursive=False)
select=lambda start:str(next(p for p in ps if plain(p).startswith(start)))
qpara=next(p for p in ps if plain(p).startswith('The difference in the first component'))
qeq=str(qpara.find_next_sibling('div'))
s52='<section id="section-5.2" class="numerical-section"><h3>5.2 Comparison of spatial formulations</h3>'
s52+=select('We fix')+initial
s52+='<p>Endpoint-SD gives the smallest '+m('u_t')+' error in all four tests. Centered-SD reduces the '+m('v_t')+' error relative to Endpoint-SD by factors ranging from approximately 60 to 125. It gives the smallest second-component defect in the one-soliton, Gaussian and sinusoidal cases, while FD gives the smallest value in the two-soliton case. The first and second components therefore favor different spatial approximations.</p>'
s52+=str(qpara)+qeq+select('The auxiliary quantity')
s52+='<p>The figures below place all three spatial formulations together for each test. The left profile panels compare the reference at '+m('y=0')+' with numerical values shown as distinct symbols. Where this section lies between native field sites, its numerical values are recovered by local polynomial interpolation through the nearest 12 '+m('y')+' nodes. The right panels display the absolute errors along that same section as continuous curves through all sampled '+m('x')+' points. The lower panels locate the errors in the '+m('x,y')+' plane, using one logarithmic color scale for each component across the three methods. The color scales resolve both the spatial pattern and the differences in error magnitude.</p>'
s52+='<div id="initial-rate-figures"><h4>Initial time derivatives</h4>'
rate_text={
'A':'The one-soliton comparison separates the two components clearly. Endpoint-SD gives the smallest initial u_t defect, whereas Centered-SD gives the smallest v_t defect. The error maps show how each discrepancy is distributed across the oblique wave.',
'C':'For the two-soliton case, the central section passes through the interacting wave profiles. The u_t error is smallest for Endpoint-SD; the v_t errors of Centered-SD and FD are much smaller than that of Endpoint-SD, with FD giving the smallest maximum.',
'Gaussian':'The Gaussian derivatives are localized in x and vary across y. The exact v_t vanishes on the central symmetry line, so the two-dimensional maps provide the spatial comparison of this component. Centered-SD gives the smallest v_t defect over the region.',
'Sinusoidal':'The sinusoidal derivatives repeat periodically along x. The central v_t reference is again zero, while its off-axis variation produces the error bands in the maps. The ranking matches the Gaussian case: Endpoint-SD gives the smallest u_t defect and Centered-SD the smallest v_t defect.'}
for i,c in enumerate(CASES):s52+='<h5>'+NAMES[c]+' case</h5><p>'+rate_text[c]+'</p>'+figure(c,'rate',5+i)
s52+='</div><h4>Physical fields after time advancement</h4>'+select('We next advance')+final
final_text={
'A':f'In the one-soliton case, the three methods reproduce the central pulse profiles, while the error panels separate their different accuracies. Centered-SD reduces the final {m("u")} and {m("v")} errors relative to Endpoint-SD by factors of approximately 2.8 and 72. Its first-field error is smaller even though Endpoint-SD had the smaller initial {m("u_t")} defect. The first equation couples the evolution of {m("u")} to the curvature of {m("v")} through {m("-v_{xx}")}, so the second-field error also enters the subsequent first-field evolution. FD gives the smallest final {m("u")} error, while Centered-SD gives the smallest {m("v")} error.',
'C':f'For the two-soliton case, the final {m("u")} errors are closely grouped near {m(r"1.15\times10^{-4}")}. The {m("v")} errors are more widely separated: {m(r"5.442\times10^{-4}")} for Endpoint-SD, {m(r"1.049\times10^{-5}")} for Centered-SD and {m(r"8.998\times10^{-6}")} for FD. Centered-SD reduces the second-field error by a factor of approximately 52 relative to Endpoint-SD. The enlarged sections resolve the central profiles, and the heatmaps show the errors across both wave branches.',
'Gaussian':f'The Gaussian profile remains close to the continuous reference after the short evolution. Endpoint-SD gives the smallest {m("u")} error, while Centered-SD gives the smallest {m("v")} error. The centered second-field error is {m(r"6.967\times10^{-9}")}, approximately 3.2 times smaller than FD and 87 times smaller than Endpoint-SD. The central {m("v")} profile stays at four; the lower heatmaps show the errors away from this symmetry line.',
'Sinusoidal':f'The sinusoidal case gives the same ordering as the Gaussian case. The sections compare the first field over one period, and the heatmaps show the repeated spatial pattern of the errors. Centered-SD gives a {m("v")} error of {m(r"4.706\times10^{-9}")}, approximately 3.5 times smaller than FD and 60 times smaller than Endpoint-SD. Its {m("u")} error lies between the Endpoint-SD and FD values.'}
for i,c in enumerate(CASES):s52+='<h5>'+NAMES[c]+' case</h5><p>'+final_text[c]+'</p>'+figure(c,'final',9+i)
s52+='<p>For the Gaussian and sinusoidal tests, '+m(r'E_u(T)/(T E_{u_t})')+' and '+m(r'E_v(T)/(T E_{v_t})')+' differ from one by at most '+m(r'0.43\%')+' across all three formulations. The initial derivative defects therefore explain their short-time error levels quantitatively. The soliton comparisons also show how the initial errors develop through the coupled equations: the Endpoint-SD advantage in the initial '+m('u_t')+' defect does not persist in the one-soliton '+m('u')+' field, while the centered reconstruction substantially improves '+m('v')+' in both soliton tests.</p></section>'
intro='<section id="section-5"><h2>5. Numerical experiments</h2><p>We use four wave problems to examine how the spatial formulation affects the accuracy of the physical fields. A one-soliton solution provides a single localized wave, and a two-soliton solution introduces the interaction of two wave profiles. Gaussian and sinusoidal initial data extend the comparison to localized and periodic smooth fields. Section 5.1 introduces these test problems, their continuous references and the error measures. In Section 5.2, we first evaluate the numerical time derivatives at the initial state, then advance the same fields with RK4 to examine how the spatial errors develop in the coupled evolution of '+m('u')+' and '+m('v')+'.</p>\n'

def render(html):
    js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(t=>k.renderToString(t,{throwOnError:true,strict:'error'}))));"
    out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(FORMULAS),text=True,encoding='utf-8',capture_output=True,check=True)
    for i,v in enumerate(json.loads(out.stdout)):html=html.replace('FOURCASEMATH'+str(i)+'END',v)
    return html

sec51=render(str(s51));sec52=render(s52);intro=render(intro)
paper=replace(SOURCE,'section-5.1',sec51);paper=replace(paper,'section-5.2',sec52)
a,_=span(paper,'section-5');b,_=span(paper,'section-5.1');paper=paper[:a]+intro+paper[b:]
# Keep the editor's current scope accurate, leaving later experiment sections intact.
g=frag(str(BASE.find(id='appendix-G'))).section
for p in g.find_all('p'):
    if '六算例' in p.get_text():p.string='2026-10-25：空间比较现选四算例：原A、C改称One-soliton、Two-soliton，加Gaussian、Sinusoidal。5.1–5.2含三表、48个误差值、12组图；初始导数与终态场各按四案成组，三格式热图全部正文展示。3.3–3.4及4.1–4.2沿用此前自然Centered同步。'
g.append(frag('<p>本轮空间图文源：Workspaces/dlw_paper_20261009/spatial_figures_four_cases_20261025/。误差曲线连接全部原始截面采样点，热图共用分量对数色标；不新增时间推进计算。下一步仍为5.3当前表示的Euler/CN比较。</p>').p)
paper=replace(paper,'appendix-G',str(g))
target=ROOT/'dlw-paper.html';prev=HERE/'publication.json'
allowed={hashlib.sha256((HERE/'before_dlw-paper.html').read_bytes()).hexdigest()}
if prev.exists():allowed.add(json.loads(prev.read_text(encoding='utf-8'))['paper_sha256'])
assert hashlib.sha256(target.read_bytes()).hexdigest() in allowed,'Concurrent manuscript edit'
target.write_text(paper,encoding='utf-8')

# Synchronize the standalone numerical draft with the same selected sections.
draft=(HERE/'before_numerical_draft.html').read_text(encoding='utf-8')
for sid,content in [('section-5.1',sec51),('section-5.2',sec52)]:
    content=content.replace('src="'+PREFIX,'src="../'+PREFIX).replace('href="'+PREFIX,'href="../'+PREFIX)
    draft=replace(draft,sid,content)
a,_=span(draft,'section-5');b,_=span(draft,'section-5.1');draft=draft[:a]+intro+draft[b:]
draft=draft.replace('Test problems and exact profiles','Test problems and exact profiles')
(ROOT/'report/dlw_numerical_text_20261025.html').write_text(draft,encoding='utf-8')
(HERE/'section-5.1.html').write_text(sec51,encoding='utf-8');(HERE/'section-5.2.html').write_text(sec52,encoding='utf-8')
record=dict(paper_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),cases=CASES,display_names=NAMES,figures=12,exact_profiles=4,initial_comparisons=4,terminal_comparisons=4,all_heatmaps_in_body=True,error_curves='all sampled section errors connected, no markers or smoothing',time_and_mesh_sections_unchanged=True)
prev.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
