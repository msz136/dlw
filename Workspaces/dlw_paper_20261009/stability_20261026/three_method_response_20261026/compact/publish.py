from pathlib import Path
from datetime import datetime
import re,json,csv,subprocess
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
PAPER=ROOT/'dlw-paper.html'
raw=PAPER.read_bytes(); old=raw.decode('utf-8')
backup=HERE/('backup_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir()
(backup/'dlw-paper.html').write_bytes(raw)
match=re.search(r'<section id="section-5.5"[\s\S]*?</section>',old);assert match
prior=match[0]; paras=re.findall(r'<p>[\s\S]*?</p>',prior)
maths=[]
def m(tex):
    maths.append({'tex':tex,'display':False});return f'COMPACTMATH{len(maths)-1}END'
def tx(s):
    bits=s.split('$');assert len(bits)%2==1
    return ''.join(m(t) if i%2 else t for i,t in enumerate(bits))
def p(s):return '<p>'+tx(s)+'</p>\n'
def fig(case,num,report=False):
    name={'A':'One-soliton','D':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}[case]
    prefix='../' if report else ''
    path=prefix+(HERE/'figures'/f'response_{case}').relative_to(ROOT).as_posix()
    caption=tx(f'Figure {num}. {name} perturbation responses. The upper and lower rows perturb $u_0$ and $v_0$, respectively; the columns show the normalized $u$ and $v$ responses. Blue: Endpoint-SD; orange: Centered-SD; green: FD. Each curve uses its own unperturbed trajectory and native field sites. Equal-length dashes are staggered to keep all three colors visible where curves overlap.')
    ident={'A':'figure-native-u','D':'figure-native-v'}.get(case,'supplement-'+case)
    return f'<figure id="{ident}" style="max-width:720px;margin:22px auto"><img src="{path}.png" alt="{name}: native perturbation response histories" style="width:100%;height:auto"><figcaption>{caption} <a class="export" href="{path}.pdf">PDF</a></figcaption></figure>\n'

new='<section id="section-5.5" class="numerical-section">\n<h3>5.5 Evolution of independent physical-field perturbations</h3>\n'
new+=p('The preceding experiments start from prescribed reference wave fields and examine how accurately their evolution is reproduced. A related question concerns the response of the numerical evolution when the initial physical fields are slightly changed. Such changes may arise when initial data are sampled or prescribed, and their influence develops through the coupling between the two fields. A disturbance introduced into $u$ can generate a response in $v$, while a disturbance in $v$ can also affect the subsequent evolution of $u$. Understanding this response helps describe how the computed waves depend on their initial physical data.')
new+=p('We examine this dependence on the same four backgrounds by perturbing $u_0$ and $v_0$ separately. For each spatial formulation, the perturbed evolution is measured relative to its own unperturbed trajectory. This separates the continuing response in the initially disturbed field from the response generated in the other component, allowing us to follow both processes over time. The two experiments add $\\varepsilon\\Phi$ to $u_0$ or $v_0$, respectively, with')
new+=re.search(r'<div class="equation">[\s\S]*?</div>',prior)[0]+'\n'
new+=next(x for x in paras if 'The perturbation is sampled' in x)+'\n'
new+=next(x for x in paras if 'For each spatial formulation, let' in x)+'\n'
new+=p('For the one-soliton background, Figure 13 follows both perturbation directions. With $u_0$ perturbed, the response in $u$ remains near its initial amplitude and grows slightly, while the initially unperturbed $v$ field develops a response from zero. For Endpoint-SD, Centered-SD, and FD, the terminal induced $v$ responses are $0.09182$, $0.09186$, and $0.09185$ times $\\varepsilon$, respectively. With $v_0$ perturbed, each formulation produces a growing $u$ response reaching approximately $0.225\\varepsilon$, alongside a small increase in the initially imposed $v$ disturbance. The two inputs thus expose both the persistence of the original disturbance and the response generated through coupling.')
new+=fig('A',13)
new+=p('The two-soliton background produces a substantial induced $u$ response when the initial perturbation is applied to $v_0$ (Figure 14). By $T=0.01$, this response reaches approximately $0.974\\varepsilon$ within each formulation, while the $v$ response remains close to its initial magnitude. For the reverse input, an initial $u_0$ perturbation produces terminal $v$ responses of $0.10280\\varepsilon$, $0.10278\\varepsilon$, and $0.10277\\varepsilon$ for Endpoint-SD, Centered-SD, and FD, respectively. These histories show how a disturbance initially confined to one component develops into a response in both physical fields on the interacting-wave background.')
new+=fig('D',14)
new+=p('On the Gaussian and sinusoidal backgrounds, the initially perturbed component stays close to its initial magnitude over the computed interval, while a smaller response develops in the other field. Table 6 records the terminal responses separately for each formulation. An initial $u_0$ disturbance induces a $v$ response of approximately $0.019\\varepsilon$, and a $v_0$ disturbance induces a $u$ response of approximately $0.049\\varepsilon$. The full time histories are included in the supplementary response plots.')
rows=list(csv.DictReader((HERE.parent/'native/terminal_rows.csv').open(encoding='utf-8-sig')))
new+='<div class="table-wrap"><table id="table-native-terminal"><caption>'+tx('Table 6. Terminal normalized responses on the Gaussian and sinusoidal backgrounds at $T=0.01$. Each pair gives $(\\|\\delta u_h\\|_\\infty/\\varepsilon,\\|\\delta v_h\\|_\\infty/\\varepsilon)$ for the indicated initial perturbation.')+'</caption><thead><tr><th>Method</th><th>Background</th><th>'+m('u_0')+' perturbed</th><th>'+m('v_0')+' perturbed</th></tr></thead><tbody>'
for method in ['Endpoint-SD','Centered-SD','FD']:
    for case in ['Gaussian','Sinusoidal']:
        vals=[]
        for inp in ['u','v']:
            r=next(r for r in rows if r['case']==case and r['method']==method and r['input']==inp)
            vals.append('('+', '.join(f'{float(r[k]):.5f}' for k in ['terminal_u_over_epsilon','terminal_v_over_epsilon'])+')')
        new+=f'<tr><td>{method}</td><td>{case}</td><td>{vals[0]}</td><td>{vals[1]}</td></tr>'
new+='</tbody></table></div>\n'
new+=paras[-1]+'\n</section>'
supp='<html lang="en"><head><meta charset="utf-8"><title>DLW perturbation response histories</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>body{max-width:850px;margin:40px auto;padding:0 24px;font:17px/1.65 Georgia,serif;color:#222}figcaption{font-size:14px}figure{break-inside:avoid}h2{font-size:22px}</style></head><body><h1>Independent physical-field perturbations</h1>'
supp+=p('For each formulation, the plotted response is the perturbed trajectory minus its own unperturbed trajectory, measured at native physical-field sites and normalized by $\\varepsilon=10^{-6}$. Blue, orange and green denote Endpoint-SD, Centered-SD and FD. Line segments alternate at overlaps; all trajectory coordinates are unchanged.')
for n,c in enumerate(['A','D','Gaussian','Sinusoidal'],1):supp+=fig(c,n,True)
supp+='</body></html>'
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true}))));"
rr=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),capture_output=True,text=True,encoding='utf-8',check=True)
rendered=json.loads(rr.stdout)
def render(s):return re.sub(r'COMPACTMATH(\d+)END',lambda q:rendered[int(q[1])],s)
new,supp=render(new),render(supp)
tail=old[match.end():].replace('Table 6','Table 7')
updated=old[:match.start()]+new+tail
s=BeautifulSoup(updated,'html.parser');assert len(s.find_all('figure'))==14 and len(s.find_all('table'))==7
assert not s.select('.katex-error')
for image in s.find_all('img'):assert (ROOT/image['src']).exists()
assert old[:match.start()]==updated[:match.start()]
report=ROOT/'report/dlw_compact_perturbation_responses_20261026.html'
report.write_text(supp,encoding='utf-8');PAPER.write_bytes(updated.encode('utf-8'))
(HERE/'section55.html').write_text(new,encoding='utf-8')
(HERE/'publication_validation.json').write_text(json.dumps({'figures':14,'tables':7,'pre_section55_unchanged':True,'native_data_unchanged':True,'katex_errors':0,'table_rows':6,'backup':str(backup)},indent=2))
print('Published compact Section 5.5 and supplementary response figures.')
