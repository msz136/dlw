"""Publish A/D, terminal-field emphasis and additive 3D candidates."""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json,csv,hashlib,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
assert not (HERE/'surface_only_20261025/publication.json').exists(), 'The paper now includes added transparent surfaces. Edit the current section-5.2.html and manuscript in place; this archived publisher would revert them.'
SOURCE=(HERE/'before_dlw-paper.html').read_text(encoding='utf-8');BASE=BeautifulSoup(SOURCE,'html.parser')
CASES=['A','D','Gaussian','Sinusoidal'];NAMES={'A':'One-soliton','D':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
PREFIX='Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/figures/'
REPORT=HERE.parent/'report_refresh_20261024';MATH=[]
def m(tex):
    key='ADUVMATH'+str(len(MATH))+'END';MATH.append(tex);return key
def frag(s):return BeautifulSoup(s,'html.parser')
def span(s,identity):
    a=re.search(r'<section\b[^>]*\bid="'+re.escape(identity)+r'"[^>]*>',s);assert a,identity
    depth=1
    for t in re.finditer(r'</?section\b[^>]*>',s[a.end():]):
        depth+=-1 if t.group().startswith('</') else 1
        if depth==0:return a.start(),a.end()+t.end()
    raise ValueError(identity)
def replace(s,identity,content):
    a,b=span(s,identity);return s[:a]+content+s[b:]
def plain(e):
    d=frag(str(e))
    for k in d.select('.katex'):k.replace_with(k.select_one('annotation').get_text())
    return d.get_text(' ',strip=True)
def number(v,win):
    a,b=f'{v:.3e}'.split('e');s=a+' × 10<sup>'+str(int(b))+'</sup>'
    return '<strong>'+s+'</strong>' if win else s
def table(kind):
    initial=kind=='initial';tid='table-'+kind
    old=BASE.find(id=tid);out=frag(str(old.parent));target=out.find('table');target.tbody.clear()
    file='table1_initial_derivative_errors.csv' if initial else 'table2_final_field_errors.csv'
    keys=['error_ut','error_vt'] if initial else ['error_u','error_v'];mk='method' if initial else 'space'
    rows=list(csv.DictReader((REPORT/file).open(encoding='utf-8-sig',newline='')))
    for c in CASES:
        pairs=[[float(next(r for r in rows if r['case']==c and r[mk]==mth)[key]) for key in keys] for mth in ['Endpoint-SD','Centered-SD','FD']]
        best=[min(p[j] for p in pairs) for j in [0,1]]
        tr='<tr><th>'+NAMES[c]+'</th>'
        for vals in pairs:
            for j,v in enumerate(vals):tr+='<td data-value="'+format(v,'.17g')+'">'+number(v,f'{v:.3e}'==f'{best[j]:.3e}')+'</td>'
        target.tbody.append(frag(tr+'</tr>').tr)
    return str(out)
def figure(c,kind,num):
    name=NAMES[c]+' case'
    if kind=='heatmap':
        stem='spatial_'+c
        cap=name+' at '+m('T=0.01')+'. Panels (a,c) compare the continuous '+m('y=0')+' profiles with numerical symbols; panels (b,d) show the absolute errors along that section. The lower rows show the '+m('u')+' and '+m('v')+' error maps, with columns for Endpoint-SD, Centered-SD and FD. Each row uses one logarithmic color scale; light gray marks values below the scale. Panel maxima refer to the full table region.'
    else:
        stem='errors_3d_'+kind+'_'+c
        if kind=='separate':cap=name+'. Separate three-dimensional views of the '+m('T=0.01')+' physical-field errors. Rows show '+m(r'|u_h-u^*|')+' and '+m(r'|v_h-v^*|')+'; columns show Endpoint-SD, Centered-SD and FD. Each row shares the same linear height and color scale.'
        else:cap=name+'. The three spatial formulations on common three-dimensional axes at '+m('T=0.01')+'. The left and right panels show '+m(r'|u_h-u^*|')+' and '+m(r'|v_h-v^*|')+'. Blue, orange and green identify Endpoint-SD, Centered-SD and FD. Transparent surfaces and colored wireframes retain the same physical coordinates and linear height scale.'
    if c=='D' and kind=='heatmap':cap+=' The sections focus on '+m(r'x\in[-8,8]')+', while the maps retain '+m('[-30,30]')+'.'
    if c in ['Gaussian','Sinusoidal']:
        cap+=' The display window is '+m('[-18,18]' if c=='Gaussian' else '[-12,12]')+'; the table uses the full periodic interval '+m('[-96,96)')+'.'
        if kind=='heatmap':cap+=' The exact central second field is '+m('v(x,0,t)=4')+'.'
    return '<figure id="figure-'+str(num)+'" data-case="'+c+'" data-view="'+kind+'"><img loading="lazy" src="'+PREFIX+stem+'.png" alt="'+name+' terminal physical-field '+kind+' comparison"><figcaption><strong>Figure '+str(num)+'.</strong> '+cap+' <a class="export" href="'+PREFIX+stem+'.pdf">PDF</a></figcaption></figure>'

def exact_3d_figure(c,num):
    stem='exact_3d_'+c
    cap=NAMES[c]+' case. Three-dimensional views of the exact initial physical fields '+m(r'u^*(x,y,0)')+' and '+m(r'v^*(x,y,0)')+'. Surface height and color represent the field value in each panel.'
    if c=='D':cap+=' The full '+m('[-30,30]')+' window shows the two oblique wave bands.'
    if c in ['Gaussian','Sinusoidal']:cap+=' The second field is shown with its background value '+m('v=4')+'.'
    return '<figure id="figure-'+str(num)+'" data-case="'+c+'" data-view="exact-3d"><img loading="lazy" src="'+PREFIX+stem+'.png" alt="'+NAMES[c]+' exact initial physical fields in three dimensions"><figcaption><strong>Figure '+str(num)+'.</strong> '+cap+' <a class="export" href="'+PREFIX+stem+'.pdf">PDF</a></figcaption></figure>'

s51=frag(str(BASE.find(id='section-5.1'))).section
two=s51.find(id='table-parameters').select('tbody tr')[1]
two.find_all('td')[0].string='(1, 2), (4, −3)'
for p in s51.find_all('p',recursive=False):
    if plain(p).startswith('The two-soliton case combines'):
        p.string='The two-soliton case combines the spectral pair of the one-soliton test with the pair (4, −3). Its first field contains a dominant negative trough and a smaller positive ridge, while both wave bands in the second field are negative. This extends the single-wave comparison to interacting profiles of different strengths and polarities.'
for i,f in enumerate(s51.find_all('figure')):
    c=CASES[i]
    f['id']='figure-'+str(2*i+1)
    f.figcaption.strong.string='Figure '+str(2*i+1)+'.'
    for el in f.select('[src], [href]'):
        for attr in ['src','href']:
            if attr not in el.attrs:continue
            leaf=Path(el[attr]).name
            if leaf.startswith('exact_C'):leaf=leaf.replace('exact_C','exact_D')
            el[attr]=PREFIX+leaf
    f.insert_after(frag(exact_3d_figure(c,2*i+2)).figure)
# State the terminal field errors first. Initial derivatives remain a short table diagnostic.
first=next(p for p in s51.find_all('p',recursive=False) if plain(p).startswith('Each method starts'))
to_remove=[];n=first
while n is not None:
    to_remove.append(n);n=n.next_sibling
for n in to_remove:n.extract()
s51.append(frag('<p>Each method starts from the same continuous physical fields. At '+m('T=0.01')+', we measure the maximum absolute field errors at the native sites in the specified region:</p>').p)
old_eq=next(e for e in BASE.find(id='section-5.1').find_all('div',recursive=False) if 'E_u(T)' in plain(e))
s51.append(frag(str(old_eq)).div)
s51.append(frag('<p>Here '+m(r'\mathcal G_u')+' and '+m(r'\mathcal G_v')+' contain the native locations of the two physical fields. As an initial diagnostic, '+m(r'E_{u_t}')+' and '+m(r'E_{v_t}')+' denote the analogous maximum differences between the spatially computed and continuous time derivatives at '+m('t=0')+'. Bold entries identify the smallest error for each case and field.</p>').p)

s52='<section id="section-5.2" class="numerical-section"><h3>5.2 Comparison of spatial formulations</h3>'
s52+='<p>We compare the physical fields produced by Endpoint-SD, Centered-SD and FD at '+m('T=0.01')+'. All three formulations use '+m(r'h=\Delta x=0.1')+' and RK4 with '+m(r'\Delta t=10^{-4}')+', starting from the same continuous initial fields. Their initial derivative errors are summarized in Table 2 as a diagnostic of the spatial approximation discussed in Section 3.4.</p>'+table('initial')
s52+='<p>Endpoint-SD gives the smallest initial '+m('u_t')+' defect in all four cases, while Centered-SD gives the smallest '+m('v_t')+' defect. Table 3 follows these same initial states to '+m('T=0.01')+' and measures the resulting errors in the physical fields.</p>'+table('final')
s52+='<p>The terminal errors distinguish the two physical components. Centered-SD gives the smallest '+m('v')+' error in all four tests, while the smallest '+m('u')+' error depends on the initial wave.</p>'
s52+='<p>The profile panels compare the continuous solution at '+m('y=0')+' with numerical values shown as colored symbols. Where the native lattice does not contain this section, we use the verified local polynomial reconstruction through the nearest 12 '+m('y')+' nodes. Continuous error curves connect all sampled '+m('x')+' values. The heatmaps locate the errors in the plane. The separate and overlaid three-dimensional views show the same absolute error fields as surface heights, using a common linear height scale for each component.</p>'
analysis={
'A':'The one-soliton test provides a single localized profile in each field. All three methods reproduce these central pulse shapes. Centered-SD reduces the terminal u error relative to Endpoint-SD by a factor of 2.8 and the v error by a factor of 72. This first-field improvement develops during the coupled evolution, even though Endpoint-SD has the smaller initial u_t defect. The first equation contains the curvature of v, so the approximation of the second field also enters the evolution of the first.',
'D':'The two-soliton test retains the stronger wave of the preceding case and adds a second profile of different polarity in u. Centered-SD again improves both physical fields relative to Endpoint-SD: the u error is reduced from 4.942 × 10⁻⁴ to 1.792 × 10⁻⁴, and the v error from 7.076 × 10⁻³ to 1.009 × 10⁻⁴. The corresponding factors, 2.8 and 70, are close to those of the one-soliton test. The heatmaps and surfaces show how these errors extend across the two interacting wave bands.',
'Gaussian':'The Gaussian profile remains close to its continuous reference after the short evolution. Endpoint-SD gives the smallest u error, whereas Centered-SD gives the smallest v error, 6.967 × 10⁻⁹. The latter is approximately 3.2 times smaller than FD and 87 times smaller than Endpoint-SD. The exact second field equals four along y=0; its errors away from this symmetry line are visible in the two-dimensional maps and the surface views.',
'Sinusoidal':'The sinusoidal test gives the same ordering as the Gaussian test. Centered-SD produces a v error of 4.706 × 10⁻⁹, approximately 3.5 times smaller than FD and 60 times smaller than Endpoint-SD, while its u error lies between the other two methods. One spatial period is shown, making the repeated structure of the wave and its error visible in each representation.'}
for i,c in enumerate(CASES):
    s52+='<h4>'+NAMES[c]+' case</h4><p>'+analysis[c]+'</p>'
    for j,kind in enumerate(['heatmap','separate','overlay']):s52+=figure(c,kind,9+3*i+j)
s52+='<p>The two soliton tests show the same componentwise comparison despite their different wave structures: Centered-SD improves both fields relative to Endpoint-SD and gives the smallest error in the second field. The Gaussian and sinusoidal tests retain this second-field advantage at smaller absolute error levels. The resulting physical-field comparisons connect the choice of spatial formulation with the accuracy of the computed waves.</p></section>'
intro='<section id="section-5"><h2>5. Numerical experiments</h2><p>We use a one-soliton wave, a two-soliton interaction, Gaussian initial data and sinusoidal initial data to examine the physical fields computed by the three spatial formulations. Section 5.1 introduces these test problems, their continuous references and the error measures. Section 5.2 compares the fields at '+m('T=0.01')+' under common RK4 time advancement, using the initial derivative errors as a short diagnostic of the spatial approximation.</p>\n'
def render(s):
    js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(t=>k.renderToString(t,{throwOnError:true,strict:'error'}))));"
    r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(MATH),text=True,encoding='utf-8',capture_output=True,check=True)
    for i,v in enumerate(json.loads(r.stdout)):s=s.replace('ADUVMATH'+str(i)+'END',v)
    return s
sec51=render(str(s51));sec52=render(s52);intro=render(intro)
paper=replace(SOURCE,'section-5.1',sec51);paper=replace(paper,'section-5.2',sec52)
a,_=span(paper,'section-5');b,_=span(paper,'section-5.1');paper=paper[:a]+intro+paper[b:]
guide=frag(str(BASE.find(id='appendix-G'))).section
status=guide.find('p',class_='status');status.string='2026-10-25：空间比较采用A/D孤子及Gaussian/Sinusoidal。5.1为每案加入精确初始u/v的3D分布图；5.2聚焦T=0.01物理场，三格式3D比较只展示绝对误差。初始u_t/v_t只留诊断表。现有热图与截面、独立3D和三格式同轴3D候选全部保留。'
for p in guide.find_all('p',recursive=False):
    if '四案空间图文源' in p.get_text():p.extract()
guide.append(frag('<p>当前图文源：Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/。两孤子使用原D参数(1,2)、(4,−3)。物理场介绍展示t=0的精确u/v，空间格式比较展示T=0.01的场误差；现有2D图保持。下一步可选图，时间算法与动网格本轮未改。</p>').p)
paper=replace(paper,'appendix-G',str(guide))
target=ROOT/'dlw-paper.html';recordfile=HERE/'publication.json'
allowed={hashlib.sha256((HERE/'before_dlw-paper.html').read_bytes()).hexdigest()}
if recordfile.exists():allowed.add(json.loads(recordfile.read_text(encoding='utf-8'))['paper_sha256'])
assert hashlib.sha256(target.read_bytes()).hexdigest() in allowed,'Concurrent paper edit'
target.write_text(paper,encoding='utf-8')
draft=(HERE/'before_numerical_draft.html').read_text(encoding='utf-8')
for identity,content in [('section-5.1',sec51),('section-5.2',sec52)]:
    content=content.replace('src="'+PREFIX,'src="../'+PREFIX).replace('href="'+PREFIX,'href="../'+PREFIX)
    draft=replace(draft,identity,content)
a,_=span(draft,'section-5');b,_=span(draft,'section-5.1');draft=draft[:a]+intro+draft[b:]
(ROOT/'report/dlw_numerical_text_20261025.html').write_text(draft,encoding='utf-8')
for name,content in [('section-5.1.html',sec51),('section-5.2.html',sec52)]: (HERE/name).write_text(content,encoding='utf-8')

# A standalone comparison page makes choosing among the three renderings easier.
gallery='<h1>DLW: physical fields and error figures</h1><p>Each case begins with the exact initial physical fields in three dimensions. The following sections, heatmaps and surfaces compare Endpoint-SD, Centered-SD and FD at T=0.01. The separate and overlaid three-dimensional comparisons show absolute physical-field errors.</p><nav>'+' · '.join('<a href="#case-'+c+'">'+NAMES[c]+'</a>' for c in CASES)+'</nav>'
for i,c in enumerate(CASES):
    gallery+='<section id="case-'+c+'"><h2>'+NAMES[c]+' case</h2>'
    f=frag(sec51).find('figure',attrs={'data-case':c,'data-view':'exact-3d'});f['id']='choice-exact-3d-'+c
    for e in f.select('[src], [href]'):
        for key in ['src','href']:
            if e.get(key,'').startswith('Workspaces/'):e[key]='../'+e[key]
    gallery+='<h3>Exact initial physical fields</h3>'+str(f)
    for j,(kind,title) in enumerate([('heatmap','1. Sections and heatmaps'),('separate','2. Separate 3D surfaces'),('overlay','3. Three methods on common 3D axes')]):
        # Reuse already-rendered captions from the published manuscript.
        f=frag(sec52).find(id='figure-'+str(9+3*i+j));f['id']='choice-'+kind+'-'+c
        for e in f.select('[src], [href]'):
            for key in ['src','href']:
                if e.get(key,'').startswith('Workspaces/'):e[key]='../'+e[key]
        gallery+='<h3>'+title+'</h3>'+str(f)
    gallery+='</section>'
style='body{max-width:1120px;margin:40px auto;padding:0 24px;font:17px/1.75 Georgia,serif;color:#222}figure{margin:24px 0 44px}img{display:block;width:100%;height:auto}figcaption{font-size:14px}h2{border-top:1px solid #ddd;padding-top:28px}a{color:#245c7b}.export{margin-left:8px;font-size:13px}'
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW physical fields and error figures</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body>'+gallery+'</body></html>'
(ROOT/'report/dlw_uv_figure_choices_20261025.html').write_text(html,encoding='utf-8')
record=dict(paper_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),cases=CASES,terminal_time=.01,derivative_figures=0,initial_derivative_table_retained=True,exact_initial_field_figures=4,exact_initial_3d_groups=4,terminal_heatmap_groups=4,separate_3d_groups=4,overlay_3d_groups=4,three_d_quantities={'case_introduction':'exact physical fields at t=0','method_comparison':'absolute physical-field error at T=0.01'},time_methods_and_mesh_unchanged=True)
recordfile.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
