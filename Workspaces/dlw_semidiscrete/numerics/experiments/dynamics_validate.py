"""Validate recorded outcomes, plot/report links, math rendering and provenance."""
from pathlib import Path
import hashlib,json,re,subprocess
from urllib.parse import urlsplit,unquote
import numpy as np
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[2]
OUT=ROOT/'out'


def main():
    checks={};records=[]
    for name,n in [('propagation',20),('comparison',28),('short_controls',6)]:
        payload=json.loads((OUT/f'dynamics_{name}.json').read_text())
        rows=payload['data'];assert len(rows)==n
        for rel,digest in payload['source_sha256'].items():
            assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,rel
        for r in rows:
            c=r['config'];h=r['history']
            assert h[0]['t']==0 and r['rhs_calls']==4*r['steps']
            assert r['complete']==(r['stopped'] is None and abs(r['final_t']-c['T'])<1e-12)
            assert r['final_t']>=h[-1]['t']
            if not r['complete']:assert r['stopped']
            arr=np.load(OUT/r['field_array'])
            assert abs(float(arr['t'])-h[-1]['t'])<1e-12
            for z in ('u','v'):
                assert np.isfinite(arr[z]).all()
                measured=float(np.max(abs(arr[z]-arr['exact_'+z])))
                assert abs(measured-h[-1][z]['inf'])<1e-10*max(1,measured)
                assert h[0][z]['inf']<1e-12
                assert r['decomposition'][z]['identity_residual']<1e-10
            passed=0.;failed=None
            for e in h:
                if failed is None:
                    if all(e[z]['relative_inf']<=.01 for z in ('u','v')):passed=e['t']
                    else:failed=e['t']
            assert abs(passed-r['valid_through'])<1e-12 and failed==r['first_failed_observation']
        checks[name]={'configs':n,'completed_target':sum(r['complete'] for r in rows),
                      'accuracy_gate_at_target_passed':sum(r['complete'] and r['first_failed_observation'] is None for r in rows)}
        records+=rows
    sens=json.loads((OUT/'dynamics_sensitivity.json').read_text())['data'];assert len(sens)==16
    for r in sens:
        arr=np.load(OUT/r['array'])['response']
        assert np.isfinite(arr).all() and len(arr)==len(r['times'])
        assert np.allclose(np.linalg.norm(arr,axis=1),r['gain'],rtol=1e-12)
        assert r['complete'] or r['failures']
    checks['paired_responses']=16
    cost=json.loads((OUT/'dynamics_cost.json').read_text())['data'];assert len(cost)==16
    assert all(len(r['seconds'])==3 and min(r['seconds'])>0 and r['rhs_calls']==80 for r in cost)
    checks['cost_repeats']=48
    log=(OUT/'dynamics_regressions_log.txt').read_text(encoding='utf-8')
    assert 'RESULT: all regression checks PASSED' in log and '[FAIL]' not in log
    checks['regression_pass_count']=log.count('[PASS]')
    html=WORK/'numerical_analysis.html';soup=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser')
    ids=[t['id'] for t in soup.select('[id]')];assert len(ids)==len(set(ids))
    missing=[]
    for tag in soup.find_all(['a','img']):
        value=tag.get('href' if tag.name=='a' else 'src','');url=urlsplit(value)
        if not value or url.scheme or value.startswith('//'):continue
        if url.path:
            p=WORK/unquote(url.path)
            if not p.exists() and p.name!='dynamics_validation_manifest.json':missing.append(value)
        elif url.fragment and url.fragment not in ids:missing.append(value)
    assert not missing,missing
    assert '@@KATEX' not in str(soup)
    checks['page_images']=len(soup.find_all('img'));checks['page_links_and_anchors']=True
    for tag in soup(['script','style','code','pre']):tag.decompose()
    body=soup.get_text()
    expressions=[]
    pattern=r'\$\$(.*?)\$\$|(?<!\\)\$([^$\n]+?)\$|\\\[(.*?)\\\]|\\\((.*?)\\\)'
    for match in re.finditer(pattern,body,re.S):
        expressions.append({'tex':next(x for x in match.groups() if x is not None),
                            'display':match.group(1) is not None or match.group(3) is not None})
    katex=WORK/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    js="const k=require(process.argv[1]);let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>{let a=JSON.parse(s);for(const v of a)k.renderToString(v.tex,{displayMode:v.display,throwOnError:true,strict:'ignore'});console.log(a.length)});"
    result=subprocess.run(['node','-e',js,str(katex)],input=json.dumps(expressions),text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    checks['katex_expressions_compiled']=int(result.stdout)
    # Include every new source, report, log, response and figure; no old manifest overwritten.
    paths=list((ROOT/'experiments').glob('dynamics_*.py'))+[ROOT/'run_all.py',ROOT/'lib/dynamics.py',ROOT/'lib/solver.py',ROOT/'lib/gramtau.py',ROOT/'REPORT.md',ROOT/'DYNAMICS_REPORT.md',ROOT/'BASELINE_REPORT_20260922.md',ROOT/'README.md',html]
    paths+=list(OUT.glob('dynamics_*.json'))+list(OUT.glob('dynamics_*log.txt'))+list(OUT.glob('dynamics_field_*.npz'))+list(OUT.glob('response_*.npz'))
    paths += [ROOT/'figures'/f'fig{n}_dynamics_{suffix}.png' for n,suffix in
              [(5,'profiles'),(6,'errors'),(7,'refinement'),(8,'comparison'),(9,'sensitivity'),(10,'error_maps')]]
    paths += [WORK/'AGENTS.md',WORK/'Workspaces/gsg_project/dlw_report/sync_numerical_results.py',WORK/'Workspaces/gsg_project/dlw_report/_src/numerical_analysis.src.html']
    manifest=OUT/'dynamics_validation_manifest.json'
    hashes={str(p.relative_to(WORK)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p!=manifest}
    data={'date':'2026-09-23','checks':checks,'source_and_artifact_sha256':hashes,
          'scope':'Observed numerical experiments; failed accuracy gates retained. No Lean or production solver changes.',
          'visual_inspection':'Profile and response PNGs inspected; HTML links/anchors and KaTeX compiled. No new full-browser layout audit.'}
    manifest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(checks,ensure_ascii=False));print('manifest files:',len(hashes))


if __name__=='__main__':main()
