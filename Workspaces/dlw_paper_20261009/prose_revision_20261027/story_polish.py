from pathlib import Path
from bs4 import BeautifulSoup
import re,json,subprocess
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;P=R/'dlw-paper.html'
raw=P.read_bytes();s=raw.decode('utf-8');assert not (H/'before_story_polish.html').exists()
(H/'before_story_polish.html').write_bytes(raw)
cache={}
def render(t):
 def sub(a):
  tex=a[1]
  if tex not in cache:
   js="const k=require('./Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');process.stdout.write(k.renderToString(JSON.parse(process.argv[1]),{throwOnError:true}));"
   cache[tex]=subprocess.check_output(['node','-e',js,json.dumps(tex)],cwd=R).decode()
  return cache[tex]
 return re.sub(r'\$(.*?)\$',sub,t)
edits=[]
def paragraph(needle,text):
 global s
 hits=[m for m in re.finditer(r'<p\b[^>]*>.*?</p>',s,re.S) if needle in m[0]];assert len(hits)==1,needle
 m=hits[0];s=s[:m.start()]+('<p>'+render(text)+'</p>' if text else '')+s[m.end():];edits.append((needle,text))
paragraph('In the last two subsections,',r'Endpoint-SD follows naturally from the Miwa expansion, and its one-sided pairings identify the first-order correction in (16). Centered-SD is obtained by placing these same pairings symmetrically about the continuous reference, giving second-order bilinear consistency. The two constructions therefore let us examine how the placement of a common bilinear lattice affects its approximation of the continuous system. Their physical-field reconstructions carry this comparison into the nonlinear equations.')
paragraph('The four tests show how the initial spatial errors',r'The four tests distinguish the accuracy of the initial time derivatives from that of the fields after evolution. Endpoint-SD retains its initial advantage in the first component on the Gaussian and sinusoidal backgrounds, while Centered-SD gives smaller terminal errors in both fields in the soliton tests. The initial approximation of one component must therefore be considered together with the evolution of the coupled fields.')
paragraph('The spatial error analysis helps interpret this behavior.',r'The consistency analysis identifies the truncation terms introduced by each lattice arrangement. During evolution, the coupling provides a route for these errors to affect the other component; in particular, the $v_{xx}$ term links the approximation of $v$ to the computed $u$ field. The change in error ordering in the soliton tests is consistent with this coupling. Initial derivative errors and evolved field errors thus provide complementary measures of the spatial approximation.')
paragraph('In this subsection, we examine how time integration affects',r'The preceding comparison follows spatial approximation errors through the coupled evolution using RK4. We now keep Centered-SD fixed and vary the time integrator to examine how temporal approximation changes this behavior. Forward Euler, classical RK4, and Crank–Nicolson use the same exact initial fields, spatial operators and boundary data on the uniform grid with $h=\Delta x=0.1$, and advance to $T=0.01$ with $\Delta t=10^{-4}$. We compare both the terminal errors and their time histories to see how the additional temporal error affects each physical component.')
paragraph('This opposite displacement is a straightforward consequence',r'The opposite shifts in the two field errors suggest that the temporal contribution partly cancels the spatial error in $u$ and reinforces it in $v$. To examine this interpretation, we halve the Euler time step to $\Delta t=5\times10^{-5}$. The terminal error pair moves from $(1.664\times10^{-4},\,8.026\times10^{-5})$ to $(1.671\times10^{-4},\,7.880\times10^{-5})$ in the one-soliton test, and from $(1.420\times10^{-4},\,1.090\times10^{-4})$ to $(1.560\times10^{-4},\,1.048\times10^{-4})$ in the two-soliton test. In both cases, the errors move toward the RK4 values. This step-size response supports the cancellation and reinforcement interpretation and helps explain the smaller terminal $u$ errors obtained with Euler at the tested step size.')
paragraph('The terminal errors and their time histories show that the choice','')
paragraph('These results help explain how time integration modifies',r'The similar shapes of the error histories suggest that the spatial approximation and wave evolution largely determine the pattern of accumulation, while the time integrator changes its magnitude in each component. Read together with the spatial comparison, these results show why the initial derivative accuracy, the terminal field error and the response to a smaller time step describe different aspects of the same computation.')
conclusion=[
r'We have developed two related integrable semi-discretizations of the $(2+1)$-dimensional DLW system. Endpoint-SD follows from a Miwa expansion of the Hirota–Miwa equation, and Centered-SD is obtained from it through a half-step parameter shift and a staggered placement of the $\tau$ functions. Both admit explicit Gram determinant solutions, common positivity conditions for regular field reconstruction, and Darboux–Lax representations compatible with their nonlinear equations. Their shared construction makes it possible to study the effect of lattice placement while retaining these integrable structures.',
r'The continuum analysis makes this effect explicit. Endpoint-SD is second-order consistent in the first physical-field equation and first-order consistent in the second, whereas Centered-SD is second-order consistent in both. The leading Endpoint-SD residual correction identifies the contribution of its endpoint arrangement. For Centered-SD, matching the Gram solutions to the continuous family also establishes second-order approximation of both exact physical fields under the stated regularity and positivity assumptions. Lattice placement and field reconstruction thus determine concrete approximation properties within the common integrable framework.',
r'The numerical experiments follow these properties from the initial time derivatives to the evolved fields. Endpoint-SD gives the smallest initial $u_t$ error in all four tests and retains the smallest terminal $u$ error on the Gaussian and sinusoidal backgrounds. In the soliton tests, Centered-SD gives smaller terminal errors in both fields than Endpoint-SD, illustrating the importance of assessing the two components through their coupled evolution. Time integration adds another contribution to this process: the Euler step-size controls support partial cancellation of spatial and temporal errors in $u$ and reinforcement in $v$. The resulting accuracy therefore depends on how the spatial and temporal approximations combine in each field.',
r'The conservation law provides a practical way to allocate resolution. Its density concentrates shared longitudinal nodes along the soliton wave bands and improves both field errors at a fixed node count. Over the computed interval, the gain comes mainly from the initial density-adapted placement, showing the usefulness of this quantity for mesh design. The independent perturbation experiments complement the accuracy comparisons by following the persistence of a disturbance in its initial component and the response it generates in the other.',
r'The DLW construction therefore connects a choice made at the bilinear lattice level to the approximation and computation of the physical waves. Exact solutions support the continuum comparison, while the conservation density guides the placement of numerical resolution. These are concrete ways in which the retained integrable structure contributes to the analysis and numerical treatment of the continuous system.'
]
match=re.search(r'(<section\b[^>]*id="section-6"[^>]*>)(.*?)(</section>)',s,re.S);assert match
body=match[2];ps=list(re.finditer(r'<p\b[^>]*>.*?</p>',body,re.S));assert len(ps)==5
for a,new in reversed(list(zip(ps,conclusion))):body=body[:a.start()]+'<p>'+render(new)+'</p>'+body[a.end():]
s=s[:match.start()]+match[1]+body+match[3]+s[match.end():]
old=BeautifulSoup(raw.decode('utf-8'),'html.parser');new=BeautifulSoup(s,'html.parser')
for tag in ['figure','table']:assert [str(x) for x in old.find_all(tag)]==[str(x) for x in new.find_all(tag)]
changed=['section-2.3','section-5.2','section-5.3','section-6']
for sid in changed:old.find(id=sid).decompose();new.find(id=sid).decompose()
assert str(old)==str(new)
P.write_bytes(s.encode('utf-8'))
(H/'story_polish.json').write_text(json.dumps({'sections':changed,'figures_and_tables_unchanged':True,'edits':edits,'conclusion':conclusion},ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md').open('a',encoding='utf-8') as f:f.write('\n2026-10-27 同轮叙述收紧：2.3集中共同格点构造的比较意义，5.2–5.3衔接初始/演化/时间误差，Euler解释改由步长实验支撑，Conclusion去重；仅四节文字改变，图表与数值不变。证据：prose_revision_20261027/story_polish.json。\n')
p=R/'PROGRESS_LOG.md';t=p.read_text(encoding='utf-8');t=t.replace('下一步继续审稿，其他图布局暂不调整。','已小幅收紧2.3、5.2–5.3和Conclusion，突出共同结构/耦合误差/守恒布点，图表不变。下一步继续审稿，其他图布局暂不调整。');p.write_text(t,encoding='utf-8')
print('Updated four sections; figures, tables and all other sections unchanged.')
