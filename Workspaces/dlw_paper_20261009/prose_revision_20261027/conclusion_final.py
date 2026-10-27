from pathlib import Path
from bs4 import BeautifulSoup
import re,json,subprocess
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;P=R/'dlw-paper.html'
raw=P.read_bytes();s=raw.decode('utf-8')
assert not (H/'before_conclusion_final.html').exists()
(H/'before_conclusion_final.html').write_bytes(raw)
paragraphs=[
r'In this work, building on the bilinear formulation and exact solutions of the continuous DLW system, we have developed two related integrable semi-discretizations. A Miwa expansion of the Hirota–Miwa equation gives Endpoint-SD, from which we obtain Centered-SD through a half-step parameter shift and a staggered placement of the $\tau$ functions. For both formulations, we construct explicit Gram determinant solutions, establish common positivity conditions for regular field reconstruction, and derive Darboux–Lax representations compatible with the nonlinear equations. These shared structures allow us to examine how lattice placement affects the approximation of the physical waves.',
r'We then examine the continuum limits of the equations and exact wave fields to make this dependence explicit. Endpoint-SD is second-order consistent in the first physical-field equation and first-order consistent in the second, whereas Centered-SD is second-order consistent in both. For Endpoint-SD, we identify the leading residual correction associated with its endpoint arrangement. For Centered-SD, matching the Gram solutions to the continuous family establishes second-order approximation of both exact physical fields under the stated regularity and positivity assumptions. The comparison thus traces the effect of lattice placement through the reconstructed equations and, for Centered-SD, through the wave profiles themselves.',
r'Through numerical experiments, we follow these approximation properties from the initial time derivatives to the evolved physical fields. Endpoint-SD gives the smallest initial $u_t$ error in all four tests and retains the smallest terminal $u$ error on the Gaussian and sinusoidal backgrounds. In the soliton tests, Centered-SD gives smaller terminal errors in both fields than Endpoint-SD, illustrating the importance of assessing the two components through their coupled evolution. Keeping the spatial formulation fixed, we further examine how time integration modifies these errors. The Euler step-size controls support partial cancellation of spatial and temporal errors in $u$ and reinforcement in $v$, showing how their combined effect depends on the physical-field component.',
r'We also use the semi-discrete conservation law to guide the allocation of spatial resolution. Its density concentrates shared longitudinal nodes along the soliton wave bands and improves both field errors at a fixed node count. Over the computed interval, the gain comes mainly from the initial density-adapted placement, demonstrating the usefulness of this quantity for mesh design. To complement these accuracy comparisons, we perturb the initial fields independently and follow both the persistence of the imposed disturbance and the response generated in the other component.',
r'The DLW construction therefore connects a choice made at the bilinear lattice level to the approximation and computation of the physical waves. Exact solutions support the continuum comparison, while the conservation density guides the allocation of spatial resolution. In this way, the integrable structure provides a foundation for understanding and improving the approximation of continuous waves through the design of their discrete representations.'
]
cache={}
def math(m):
 t=m[1]
 if t not in cache:
  js="const k=require('./Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');process.stdout.write(k.renderToString(JSON.parse(process.argv[1]),{throwOnError:true}));"
  cache[t]=subprocess.check_output(['node','-e',js,json.dumps(t)],cwd=R).decode()
 return cache[t]
m=re.search(r'(<section\b[^>]*id="section-6"[^>]*>)(.*?)(</section>)',s,re.S);assert m
body=m[2];ps=list(re.finditer(r'<p\b[^>]*>.*?</p>',body,re.S));assert len(ps)==5
for a,t in reversed(list(zip(ps,paragraphs))):body=body[:a.start()]+'<p>'+re.sub(r'\$(.*?)\$',math,t)+'</p>'+body[a.end():]
new=s[:m.start()]+m[1]+body+m[3]+s[m.end():]
a=BeautifulSoup(s,'html.parser');b=BeautifulSoup(new,'html.parser')
assert len(b.find_all('figure'))==14 and len(b.find_all('table'))==8
a.find(id='section-6').decompose();b.find(id='section-6').decompose();assert str(a)==str(b)
P.write_bytes(new.encode('utf-8'))
(H/'conclusion_final_validation.json').write_text(json.dumps({'only_conclusion_changed':True,'paragraphs':5,'figures':14,'tables':8,'inline_math_valid':True},indent=2),encoding='utf-8')
with (R/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md').open('a',encoding='utf-8') as f:f.write('\n2026-10-27 同轮结论定稿：按用户确认版更新Conclusion五段，加入主动主体和过渡，末句改为离散表示设计支撑连续波近似的理解与改善。仅结论改变，14图8表不变，公式渲染检查通过。证据：prose_revision_20261027/conclusion_final_validation.json。\n')
p=R/'PROGRESS_LOG.md';t=p.read_text(encoding='utf-8');t=t.replace('下一步继续审稿，其他图布局暂不调整。','Conclusion已同步用户确认的五段主动表述和最终收尾句，仅本节改变。下一步继续审稿，其他图布局暂不调整。');p.write_text(t,encoding='utf-8')
print('Conclusion updated; other sections, 14 figures and 8 tables unchanged.')
