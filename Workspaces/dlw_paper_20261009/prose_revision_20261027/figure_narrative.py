from pathlib import Path
from bs4 import BeautifulSoup
import re,json,subprocess
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;p=R/'dlw-paper.html'
raw=p.read_bytes();s=raw.decode('utf-8');assert not (H/'before_figure_narrative.html').exists()
(H/'before_figure_narrative.html').write_bytes(raw)
def m(t):
 js="const k=require('./Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');process.stdout.write(k.renderToString(JSON.parse(process.argv[1]),{throwOnError:true}));"
 return subprocess.check_output(['node','-e',js,json.dumps(t)],cwd=R).decode()
u,v,y=m('u'),m('v'),m('y=0')
old='In the one-soliton test (Figure 5), all three formulations capture the shape and position of the central pulse. '
new='Figure 5(a,c) shows the one-soliton profiles along '+y+'. Both fields form a localized depression, with a single trough and a return toward the background on either side. The numerical symbols from all three formulations follow the continuous reference closely, resolving both the trough and its flanks. Panels (b,d) make their differences visible through the absolute errors along the same section. These errors have several local peaks around the wave, with a particularly clear separation between Endpoint-SD and the other two methods in '+v+'.</p>\n<p>'
assert old in s;s=s.replace(old,new,1)
old='The two-soliton test (Figure 6) shows the exact same behavior across the two intersecting wave bands. '
new='The two-soliton section in Figure 6(a,c) has a more asymmetric shape. Along '+y+', the '+u+' profile has a small positive shoulder to the left of a pronounced negative trough, while '+v+' has a broader depression leading into a deeper minimum. The numerical values reproduce these features closely. The section errors in panels (b,d) resolve the differences beneath this visual agreement, including local oscillations and larger errors near the central trough.</p>\n<p>'
assert old in s;s=s.replace(old,new,1)
texts={
5:'The heatmaps in Figure 5(e–j) extend this section comparison to the two-dimensional region. The dashed horizontal line marks '+y+', linking the upper panels to the maps below. Bands of larger error follow the inclined wave structure, with narrow low-error strips separating local maxima. The common color scale within each field makes the smaller '+v+' errors of Centered-SD and FD visible alongside the broader, brighter Endpoint-SD error band.',
6:'The heatmaps in Figure 6(e–j) show how this error pattern extends across the two-dimensional wave configuration. Several bands and their intersections are visible over the wider plotting region, whereas the upper panels focus on the central section. In '+v+', the dominant oblique band is substantially brighter for Endpoint-SD; the Centered-SD and FD maps retain a narrower band of larger error. These maps locate the errors reported in Table 3 and show their variation away from '+y+'.',
7:'Figure 7(a) shows the Gaussian section as a smooth positive hump, with all three sets of numerical symbols following the reference curve. Panel (b) resolves the much smaller differences between them as several error lobes across the hump. The second field is constant along '+y+' in panel (c), and the enlarged vertical scale in panel (d) displays section errors of order '+m('10^{-12}')+'. The heatmaps below show the transverse variation that this central section does not sample: the '+v+' error grows away from the symmetry line and forms corresponding patterns in the upper and lower halves of the strip.',
8:'Figure 8(a) presents the sinusoidal section, with a positive crest near the center and negative values toward the ends of the displayed interval. The numerical symbols follow this alternating profile, while panel (b) separates their section errors. As in the Gaussian test, '+v+' is constant on '+y+' and its section error remains of order '+m('10^{-12}')+'. In the heatmaps, the errors vary along both spatial directions, forming repeated bands and lobes. Reading the sections together with these maps shows how close agreement on the central line accompanies a nonuniform error distribution across the strip.'
}
for i,t in texts.items():
 pattern=r'(<figure\b[^>]*\bid="figure-'+str(i)+r'"[^>]*>.*?</figure>)'
 s,n=re.subn(pattern,lambda a:a.group()+'\n<p>'+t+'</p>',s,count=1,flags=re.S);assert n==1
before=BeautifulSoup(raw.decode('utf-8'),'html.parser');after=BeautifulSoup(s,'html.parser')
for tag in ['figure','table']:assert [str(x) for x in before.find_all(tag)]==[str(x) for x in after.find_all(tag)]
def without_section(doc):
 doc.find(id='section-5.2').decompose();return str(doc)
assert without_section(before)==without_section(after)
p.write_bytes(s.encode('utf-8'))
(H/'figure_narrative_validation.json').write_text(json.dumps({'only_section_5_2_changed':True,'figures_and_tables_unchanged':True,'added_reading_paragraphs':4,'expanded_soliton_section_descriptions':2},indent=2),encoding='utf-8')
with (R/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md').open('a',encoding='utf-8') as f:
 f.write('\n2026-10-27 同轮补充：Section 5.2增加四算例的截线波形、截面误差及热图衔接叙述；逐图检查形状，只改该节文字，图表及数值不变。证据：Workspaces/dlw_paper_20261009/prose_revision_20261027/figure_narrative_validation.json。\n')
q=R/'PROGRESS_LOG.md';a=q.read_text(encoding='utf-8');a=a.replace('下一步按用户选择继续审稿，其他图布局暂不调整。','Section 5.2已补充四算例截线波形、截面误差和热图的读图叙述，仅本节文字改变。下一步按用户选择继续审稿，其他图布局暂不调整。');q.write_text(a,encoding='utf-8')
print('Updated Section 5.2; all figures, tables and other sections unchanged.')
