"""Put native, within-method perturbation responses into Numerical Experiments."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PAPER=ROOT/'dlw-paper.html'
REPORT=ROOT/'report/dlw_native_perturbation_responses_20261026.html'
CASES=['A','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
LABELS=dict(A='One-soliton',D='Two-soliton',Gaussian='Gaussian',Sinusoidal='Sinusoidal')
ZH=dict(A='一孤子',D='双孤子',Gaussian='高斯',Sinusoidal='正弦')
data={c:json.loads((HERE/'native'/f'{c}.json').read_text(encoding='utf-8')) for c in CASES}
audit=json.loads((HERE/'audit/native_output_validation.json').read_text(encoding='utf-8'))
assert audit['independent_native_audit_passed'] and audit['trajectories']==24
for c,d in data.items():
    assert d['status']=='complete' and d['reached']==.01
    assert d['interpolation_used'] is False and d['method_pair_comparisons'] is False
for name in ['response_u_input','response_v_input','response_overview']:
    assert (HERE/'figures'/f'{name}.png').exists() and (HERE/'figures'/f'{name}.pdf').exists()

maths=[]
def m(tex,display=False):
    maths.append(dict(tex=tex,display=display));return f'NATIVEMATH{len(maths)-1}END'
def text(s):
    bits=s.split('$');assert len(bits)%2==1
    return ''.join(m(t) if i%2 else t for i,t in enumerate(bits))
def p(s):return '<p>'+text(s)+'</p>\n'
def eq(s):return '<div class="equation">'+m(s,True)+'</div>\n'
def value(case,method,inp,out):
    r=next(r for r in data[case]['terminal'] if r['method']==method and r['input']==inp)
    return r['terminal_response_normalized'][0 if out=='u' else 1]
def num(x):return f'{x:.5f}'
def vals(case,method,inp):return [num(value(case,method,inp,q)) for q in ['u','v']]

def discussion(method,lang):
    au,av=vals('A',method,'u');du,dv=vals('D',method,'u')
    avu,avv=vals('A',method,'v');dvu,dvv=vals('D',method,'v')
    gu,gv=vals('Gaussian',method,'u');su,sv=vals('Sinusoidal',method,'u')
    gvu,gvv=vals('Gaussian',method,'v');svu,svv=vals('Sinusoidal',method,'v')
    if lang=='zh':
        return p(method+r' 的 $u_0$ 扰动在演化中保留了接近初始幅值的 $u$ 响应，同时逐渐产生 $v$ 响应。在 $T=0.01$，一孤子和双孤子的诱导 $v$ 响应分别为 $'+av+r'\varepsilon$、$'+dv+r'\varepsilon$；高斯和正弦算例分别为 $'+gv+r'\varepsilon$、$'+sv+r'\varepsilon$。')+p(r'只扰动 $v_0$ 时，$u$ 响应从零开始累积，一孤子和双孤子终态分别达到 $'+avu+r'\varepsilon$、$'+dvu+r'\varepsilon$，对应的 $v$ 响应为 $'+avv+r'\varepsilon$、$'+dvv+r'\varepsilon$。高斯、正弦的诱导 $u$ 响应分别为 $'+gvu+r'\varepsilon$、$'+svu+r'\varepsilon$。这些曲线分别记录了初始受扰分量的持续变化，以及耦合在另一物理场中产生的响应。')
    if method=='Endpoint-SD':
        return p(r'For Endpoint-SD, the $u_0$ perturbation remains visible in $u$ while a $v$ response develops from zero. The normalized $v$ responses at $T=0.01$ are $'+av+'$ and $'+dv+r'$ for the one- and two-soliton cases, and approximately $0.019$ for the Gaussian and sinusoidal cases. With $v_0$ perturbed, the induced $u$ responses reach $'+avu+'$ and $'+dvu+r'$ in the two soliton tests. The initially perturbed $v$ component retains normalized magnitudes $'+avv+'$ and $'+dvv+'$, respectively.')
    if method=='Centered-SD':
        return p(r'Centered-SD follows the transfer in both directions. An initial $u$ perturbation produces terminal $v$ responses of $'+av+'$ and $'+dv+r'$ in the soliton cases. For $v_0$ input, the $u$ response accumulates to $'+avu+'$ in the one-soliton case and $'+dvu+r'$ in the two-soliton case. On the Gaussian and sinusoidal backgrounds, the induced responses are approximately $0.019$ for $u\to v$ and $0.049$ for $v\to u$, while the initially perturbed field stays close to its initial magnitude.')
    return p(r'For FD, an initial disturbance also evolves into a response in both physical fields. The one- and two-soliton $u_0$ tests finish with normalized pairs $('+au+','+av+')$ and $('+du+','+dv+r')$. With $v_0$ input, the pairs are $('+avu+','+avv+')$ and $('+dvu+','+dvv+r')$. The Gaussian and sinusoidal trajectories retain a response near the initial amplitude in the perturbed field and develop a smaller response in the other field. Their native-node maxima vary as the evolving peaks move across the grid.')

def fig(inp,number,lang,report=False):
    filename=f'response_{inp}_input'
    base=HERE.relative_to(ROOT).as_posix()+'/figures/'
    if report:base='../'+base
    title=('Response to an initial '+inp+' perturbation' if lang=='en' else '仅扰动 '+inp+' 初值的物理场响应')
    if lang=='en':
        cap=f'Figure {number}. '+r'Response to an independent perturbation of $'+inp+r'_0$. Rows show the one-soliton, two-soliton, Gaussian, and sinusoidal backgrounds; columns show $\|\delta u_h(t)\|_\infty/\varepsilon$ and $\|\delta v_h(t)\|_\infty/\varepsilon$. Blue solid, orange dashed, and green dash-dot curves denote Endpoint-SD, Centered-SD, and FD. Each curve subtracts that method\textquotesingle s own unperturbed trajectory and uses its native physical-field sites.'.replace(r'method\textquotesingle s',"method's")
    else:
        cap=f'图 {number}．仅扰动 $'+inp+r'_0$。四行依次为一孤子、双孤子、高斯和正弦；左右列分别为 $u$、$v$ 的响应。蓝色实线、橙色虚线、绿色点划线分别表示 Endpoint-SD、Centered-SD、FD。每条曲线均由该方法自身的受扰解减去未扰动解，在原生物理场格点上取最大值，再除以规定幅值 $\varepsilon$。'
    return '<figure id="figure-native-'+inp+'"><img src="'+base+filename+'.png" alt="'+title+'"><figcaption>'+text(cap)+' <a class="export" href="'+base+filename+'.pdf">PDF</a></figcaption></figure>\n'

new='<section id="section-5.5" class="numerical-section">\n<h3>5.5 Evolution of independent physical-field perturbations</h3>\n'
new+=p(r'We now follow how an independent change in one initial physical field propagates through the coupled evolution. For each of the four backgrounds, Endpoint-SD, Centered-SD, and FD are initialized from the same continuous physical fields. Two separate experiments add $\varepsilon\Phi$ to $u_0$ or to $v_0$, with')
new+=eq(r'\Phi(x,y)=\sin^2\!\left(\frac{\pi(y-y_L)}{y_R-y_L}\right)\cos(\kappa x),\qquad \varepsilon=10^{-6},\qquad \kappa=\frac{\pi}{2}.')
new+=p(r'The perturbation is sampled at each field\textquotesingle s native sites.'.replace(r'field\textquotesingle s',"field's")+r' The transverse node intervals are $[-9.95,9.95]$ for the one-soliton case, $[-39.95,39.95]$ for the two-soliton case, and $[-2,2]$ for the Gaussian and sinusoidal cases. The envelope and its first derivative vanish at the transverse endpoints. All trajectories use $h=\Delta x=0.1$, RK4, $\Delta t=10^{-4}$, and $T=0.01$, with the prescribed lower $u$ trace and the boundary closures of Section 4.2.')
new+=p(r'For each spatial formulation, let $(u_h^\varepsilon,v_h^\varepsilon)$ and $(u_h^0,v_h^0)$ be its perturbed and unperturbed numerical trajectories. We record $\delta u_h=u_h^\varepsilon-u_h^0$ and $\delta v_h=v_h^\varepsilon-v_h^0$, and plot their native-node maximum magnitudes divided by $\varepsilon$ in the observation regions of Section 5.1. The initial ordinates are the maxima of the imposed perturbation sampled at those same sites. The nonlinear difference equations are advanced together with the corresponding background at every RK4 stage.')
new+=p(r'Figure 29 follows an initial perturbation of $u$, including the response subsequently generated in $v$. Figure 30 follows an initial perturbation of $v$ and its transfer into $u$. The two columns in each figure separate the continuing response of the initially perturbed field from the response generated by the coupling.')
new+=fig('u',29,'en')+fig('v',30,'en')
for method in METHODS:new+=discussion(method,'en')
new+=p(r'The response histories describe how a disturbance initially confined to one field develops into a coupled physical-field perturbation. In particular, the first field equation recovers the $u$ evolution through transverse integration, allowing the effect of a $v$ perturbation to accumulate over the transverse interval. This helps interpret the substantial induced $u$ response on the wider two-soliton domain during the computed interval.')
new+='</section>\n'

report='<header><p class="eyebrow">DLW · Independent initial perturbations · RK4</p><h1>三种空间离散的独立初始扰动响应</h1></header>'
report+=p(r'四个背景分别在 Endpoint-SD、Centered-SD 和 FD 下演化，每种方法独立记录自身受扰轨道与未扰动轨道的差。只扰动 $u_0$ 或只扰动 $v_0$，共24条受扰轨道；取 $h=\Delta x=0.1$、$\Delta t=10^{-4}$、$T=0.01$、$\varepsilon=10^{-6}$、$\kappa=\pi/2$。所有响应都在本方法的原生物理场格点上统计。')
report+=eq(r'\delta u_h=u_h^\varepsilon-u_h^0,\qquad\delta v_h=v_h^\varepsilon-v_h^0,\qquad \Phi(x,y)=\sin^2\!\left(\frac{\pi(y-y_L)}{y_R-y_L}\right)\cos(\kappa x).')
report+=p(r'一孤子使用 $|x|\le5,|y|<5$，双孤子使用 $|x|\le30,|y|<30$ 的观测区域；高斯与正弦使用完整周期 $x$ 区间及 $|y|\le1.8$。纵轴除以规定的扰动幅值 $\varepsilon$，初始曲线高度由该扰动在原生格点上的采样最大值决定。')
report+=fig('u',1,'zh',True)+fig('v',2,'zh',True)
for i,method in enumerate(METHODS):
    report+='<section><h2>'+method+'</h2>'+discussion(method,'zh')
    report+='<div class="table-wrap"><table><caption>'+text(f'表 {i+1}．{method} 在 $T=0.01$ 的物理场响应。')+'</caption><thead><tr><th>背景</th><th>初始受扰场</th><th>'+m(r'\|\delta u_h(T)\|_\infty/\varepsilon')+'</th><th>'+m(r'\|\delta v_h(T)\|_\infty/\varepsilon')+'</th></tr></thead><tbody>'
    for c in CASES:
        for inp in ['u','v']:
            report+='<tr><th>'+ZH[c]+'</th><td>'+m(inp+'_0')+'</td>'+''.join(f'<td>{value(c,method,inp,o):.6f}</td>' for o in ['u','v'])+'</tr>'
    report+='</tbody></table></div></section>'
report+=p(r'$u$ 方程中的横向积分使 $v$ 扰动的作用沿横向累积，有助于解释双孤子区域中逐渐形成的 $u$ 响应。图中的两列分别描述初始受扰分量的持续变化和另一物理场的诱导响应，呈现各个数值演化中的耦合过程。')
base='../'+HERE.relative_to(ROOT).as_posix()
report+='<details><summary>四算例总览图</summary><img class="overview" src="'+base+'/figures/response_overview.png" alt="Native perturbation responses, four-case overview"><p><a href="'+base+'/figures/response_overview.pdf">总览矢量 PDF</a></p></details>'
report+='<p><a href="../dlw-paper.html#section-5.5">主论文 Section 5.5</a> · <a href="'+base+'/native/terminal_rows.csv">终态响应数据</a></p>'
style='''body{max-width:1080px;margin:44px auto;padding:0 24px;font:17px/1.8 Georgia,"Times New Roman","Microsoft YaHei",serif;color:#222;background:#fff}h1{font-size:29px;line-height:1.4}h2{font-size:23px;margin-top:38px}a{color:#245c7b}.eyebrow{font-size:14px;color:#666}.equation{overflow-x:auto;margin:22px 0}.table-wrap{overflow-x:auto;margin:24px 0}table{width:100%;border-collapse:collapse;border-top:2px solid #222;border-bottom:2px solid #222;font:15px/1.6 Georgia,"Times New Roman","Microsoft YaHei",serif;font-variant-numeric:tabular-nums}caption{text-align:left;padding-bottom:10px}thead{border-bottom:1px solid #222}th,td{padding:9px 12px;white-space:nowrap}th{font-weight:normal;text-align:left}td{text-align:right}figure{margin:32px 0}figure img,.overview{width:100%;height:auto}figcaption{font-size:14px;line-height:1.7}.export{margin-left:8px;font:12px Arial}.katex{font-size:1.02em}details{margin:32px 0;border-top:1px solid #ccc;padding-top:16px}summary{cursor:pointer}@media print{body{margin:0;max-width:none;padding:0;font-size:11pt}figure,tr{break-inside:avoid}table{font-size:9pt}h2{break-after:avoid}.table-wrap{overflow:visible}.export{display:none}}'''
report='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 独立物理场扰动响应</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body>'+report+'</body></html>'

js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));"
out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf-8',capture_output=True,check=True)
rendered=json.loads(out.stdout)
def render(s):return re.sub(r'NATIVEMATH(\d+)END',lambda q:rendered[int(q[1])],s)
new,report=render(new),render(report)

before=PAPER.read_bytes();src=before.decode('utf-8')
start6=src.index('<section id="section-6"');start7=src.index('<section id="section-7">',start6)
old6=src[start6:start7]
assert '6. Response to initial perturbations' in old6
prefix=src[:start6];end5=prefix.rfind('</section>')
assert not prefix[end5+len('</section>'):].strip()
prefix=prefix[:end5]+new+'\n'+prefix[end5:]
old_roadmap='Finally, Section 5.4 examines how redistributing the shared '
assert prefix.count(old_roadmap)==1
prefix=prefix.replace(old_roadmap,'Section 5.4 examines how redistributing the shared ',1)
end_roadmap='affects the computed soliton fields.</p>'
assert prefix.count(end_roadmap)==1
prefix=prefix.replace(end_roadmap,'affects the computed soliton fields. Section 5.5 follows independent initial perturbations under each spatial formulation to examine their evolution in the two coupled physical fields.</p>',1)
oldnav='<a href="#section-6">6. Response to initial perturbations</a><a class="subsection" href="#section-6.1">6.1 Linearized evolution under the numerical closure</a><a class="subsection" href="#section-6.2">6.2 Independent physical-field perturbations</a><a href="#section-7">7. Conclusions</a>'
newnav='<a class="subsection" href="#section-5.5">5.5 Evolution of independent physical-field perturbations</a><a href="#section-6">6. Conclusions</a>'
assert prefix.count(oldnav)==1;prefix=prefix.replace(oldnav,newnav)
suffix=src[start7:]
assert suffix.count('<h2>7. Conclusions</h2>')==1
suffix=suffix.replace('<section id="section-7">','<section id="section-6">',1).replace('<h2>7. Conclusions</h2>','<h2>6. Conclusions</h2>',1)
assert suffix.count('<caption>Table 10. Control runs for Section 5.')==1
suffix=suffix.replace('<caption>Table 10. Control runs for Section 5.','<caption>Table 6. Control runs for Section 5.')
updated=prefix+suffix

# All changes outside the old response section are enumerated and reversible.
restored_prefix=prefix.replace(new+'\n','',1).replace(newnav,oldnav,1)
restored_prefix=restored_prefix.replace('Section 5.4 examines how redistributing the shared ',old_roadmap,1)
restored_prefix=restored_prefix.replace('affects the computed soliton fields. Section 5.5 follows independent initial perturbations under each spatial formulation to examine their evolution in the two coupled physical fields.</p>',end_roadmap,1)
assert restored_prefix==src[:start6]
restored_suffix=suffix.replace('<section id="section-6">','<section id="section-7">',1).replace('<h2>6. Conclusions</h2>','<h2>7. Conclusions</h2>',1).replace('<caption>Table 6. Control runs for Section 5.','<caption>Table 10. Control runs for Section 5.',1)
assert restored_suffix==src[start7:]
assert re.findall(r'<figure\b.*?</figure>',src[:start6],re.S)==re.findall(r'<figure\b.*?</figure>',updated[:updated.index('<section id="section-5.5"')],re.S)
for html,figures,tables in [(updated,30,6),(report,2,3)]:
    soup=BeautifulSoup(html,'html.parser');assert not soup.select('.katex-error')
    assert len(soup.select('figure'))==figures and len(soup.select('table'))==tables
    ids=[q['id'] for q in soup.find_all(id=True)];assert len(ids)==len(set(ids))
    if tables==6:
        assert soup.find(id='section-5.5').find_parent('section',id='section-5')
        assert soup.find(id='section-6').h2.get_text()=='6. Conclusions'
        assert not soup.find(id='section-6.1') and not soup.find(id='section-6.2')
backup=HERE/('before_publication_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir()
(backup/'dlw-paper.html').write_bytes(before);(backup/'section6_retained.html').write_text(old6,encoding='utf-8')
if REPORT.exists():(backup/REPORT.name).write_bytes(REPORT.read_bytes())
assert PAPER.read_bytes()==before,'Concurrent paper edit; reread before retrying.'
PAPER.write_bytes(updated.encode('utf-8'));REPORT.write_text(report,encoding='utf-8')
(HERE/'section55.html').write_text(new,encoding='utf-8')

linked_reports=[]
for name in ['dlw_independent_stability_20261026.html','dlw_reference_certification_20261026.html','dlw_perturbation_sweep_20261026.html','dlw_reference_goal_20261026.html']:
    file=ROOT/'report'/name
    if not file.exists():continue
    content=file.read_bytes();s=content.decode('utf-8')
    def link(match):
        return '<a href="../dlw-paper.html#section-5.5">主论文：扰动响应（§5.5）</a>'
    revised,n=re.subn(r'<a href="\.\./dlw-paper\.html#section-6(?:\.[123])?">.*?</a>',link,s)
    if n:
        (backup/name).write_bytes(content)
        assert file.read_bytes()==content
        file.write_bytes(revised.encode('utf-8'));linked_reports.append(name)
status=dict(date='2026-10-26',main_section='5.5',trajectories=24,native_sites=True,interpolation=False,intermethod_difference=False,
    main_figures=30,main_tables=6,reader_tables=3,katex_errors=0,original_28_figures_preserved=True,
    protected_content_exact_except=['Section 5 roadmap','navigation','conclusion number7→6','control table number10→6'],
    old_section_6_retained=str(backup/'section6_retained.html'),report=str(REPORT),updated_report_links=linked_reports,
    before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest())
(HERE/'publication_validation.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(status,ensure_ascii=False,indent=2))
