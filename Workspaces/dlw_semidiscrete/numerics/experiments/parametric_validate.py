"""Final data/source/page accounting; scientific gate failures remain failures."""
from parametric_study import ROOT,OUT,inf
from parametric_assess import read
from parametric import Model,Parameters
from pathlib import Path
import numpy as np,json,hashlib,sys,platform,re,subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import scipy,mpmath,matplotlib
from scipy.interpolate import RectBivariateSpline

def main():
    checks={}
    for name,n in [('scan',180),('finite_h',30),('time_domain_controls',18),('defects',360),('bounds',9),('open_bounds',18),
                   ('perturbations',18),('reference_controls',18),('assessment',18),('open',11),('open_controls',11),
                   ('open_parameter_sweep',7),('parameter_gates',20),('cost',10)]:
        data=read('parametric_'+name);assert len(data)==n,(name,len(data));checks[name]=n
    for row in read('parametric_scan'):
        c=row['config'];m=Model(Parameters(**c['pars']),c['h'],c['nx'],model=c['model'],closure=c['closure'],yhalf=c['yhalf'],continuous=True)
        a=np.load(OUT/row['fields']);assert np.isfinite(a['state']).all()
        u,v=m.error_fields(a['state']-a['exact']);last=row['history'][-1]
        assert abs(inf(u)-last['u'])<1e-11 and abs(inf(v)-last['v'])<1e-11
        assert last['u']<=last['u_bound']+1e-12 and last['v']<=last['v_bound']+1e-12
        assert row['complete'] and abs(row['final_t']-.02)<1e-12
    checks['full_scan_fields_rechecked']=180
    files=set();stopped=0;runs=0
    for name in ('parametric_perturbations','parametric_reference_controls','parametric_open','parametric_open_controls','parametric_open_parameter_sweep'):
        for g in read(name):
            rr=g.get('variants',[])+g.get('references',[])+([g['run']] if 'run' in g else [])
            for r in rr:
                runs+=1;stopped+=not r['complete'];files.add(r['file'])
                a=np.load(OUT/r['file']);assert len(a['times'])==len(r['history'])
                assert np.isfinite(a['fields']).all()
                if r['complete']:assert abs(a['times'][-1]-.01)<1e-12
                for i,his in enumerate(r['history']):
                    assert abs(inf(a['fields'][i,0])-his['u_response'])<1e-12
                    assert abs(inf(a['fields'][i,1])-his['v_response'])<1e-12
    checks['perturbation_run_records']=runs;checks['stopped_run_records']=stopped;checks['unique_perturbation_files']=len(files)
    sweep=read('parametric_open_parameter_sweep')
    assert {g['parameter_id'] for g in sweep}=={f'P{i}' for i in range(3,10)}
    assert all(g['mode']=='low' and g['eps']==.001 and len(g['variants'])==4 and len(g['references'])==5 for g in sweep)
    for g in sweep:
        ref=np.load(OUT/g['references'][3]['file']);idx=np.flatnonzero(abs(ref['times']-.01)<1e-12)
        assert len(idx)==1
        for run in g['variants']:
            coarse=np.load(OUT/run['file']);j=np.flatnonzero(abs(coarse['times']-.01)<1e-12)
            assert len(j)==1
            for field,k in (('u',0),('v',1)):
                z=RectBivariateSpline(ref['y'],ref['x'],ref['fields'][idx[0],k],s=0)(coarse['y'],coarse['x'])
                calculated=inf(coarse['fields'][j[0],k]-z)/max(inf(z),1e-30)
                reported=run['comparison'][-1][field]['relative_response_error']
                assert abs(calculated-reported)<1e-10,(g['parameter_id'],field)
    checks['expanded_parameter_comparisons_rechecked']=7*4*2
    gates=read('parametric_parameter_gates')
    assert {g['parameter_id'] for g in gates}=={f'P{i}' for i in range(1,11)}
    assert all(g['passed']==all(v is not None and v<.05 for v in g['reference_check_sums'].values()) for g in gates)
    checks['parameter_reference_gates_passed']=sum(g['passed'] for g in gates)
    assert all(len(r['seconds'])==3 and min(r['seconds'])>0 for r in read('parametric_cost'))
    log=(OUT/'parametric_regressions_log.txt').read_text(encoding='utf-8')
    assert 'RESULT: all regression checks PASSED' in log and '[FAIL]' not in log
    checks['original_regressions']=log.count('[PASS]')
    work=ROOT.parents[2];html=work/'numerical_analysis.html'
    soup=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser');ids=[x['id'] for x in soup.select('[id]')]
    assert len(ids)==len(set(ids));missing=[]
    for tag in soup.find_all(['a','img']):
        val=tag.get('href' if tag.name=='a' else 'src','');url=urlsplit(val)
        if not val or url.scheme or val.startswith('//'):continue
        if url.path:
            p=work/unquote(url.path)
            if not p.exists() and p.name!='parametric_validation_manifest.json':missing.append(val)
        elif url.fragment and url.fragment not in ids:missing.append(val)
    assert not missing,missing
    checks['page_images']=len(soup.find_all('img'));checks['links_and_anchors']=True
    for tag in soup(['script','style','code','pre']):tag.decompose()
    expr=[]
    for mat in re.finditer(r'\$\$(.*?)\$\$|(?<!\\)\$([^$\n]+?)\$|\\\[(.*?)\\\]|\\\((.*?)\\\)',soup.get_text(),re.S):
        expr.append({'tex':next(x for x in mat.groups() if x is not None),'display':mat.group(1) is not None or mat.group(3) is not None})
    node=Path('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
    katex=work/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    js="const k=require(process.argv[1]);let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>{let a=JSON.parse(s);for(const v of a)k.renderToString(v.tex,{displayMode:v.display,throwOnError:true,strict:'ignore'});console.log(a.length)});"
    r=subprocess.run([str(node),'-e',js,str(katex)],input=json.dumps(expr),text=True,capture_output=True);assert r.returncode==0,r.stderr
    checks['katex_expressions']=int(r.stdout)
    paths=list((ROOT/'lib').glob('parametric*.py'))+list((ROOT/'experiments').glob('parametric*.py'))
    paths+=list(ROOT.glob('PARAMETRIC*.md'))+[ROOT/'REPORT.md',ROOT/'README.md',ROOT/'PRE_PARAMETRIC_REPORT_20260923.md',ROOT/'lib/solver.py',ROOT/'lib/gramtau.py',ROOT/'lib/dynamics.py',html,work/'AGENTS.md']
    paths+=list(OUT.glob('parametric*'))+[OUT/f for f in files]+list((ROOT/'figures').glob('fig1[1234]_*.png'))
    paths+=[work/'Workspaces/gsg_project/dlw_report/sync_numerical_results.py',work/'Workspaces/gsg_project/dlw_report/_src/numerical_analysis.src.html']
    manifest=OUT/'parametric_validation_manifest.json'
    hashes={str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file() and p!=manifest}
    payload={'checks':checks,'sha256':hashes,'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__,'matplotlib':matplotlib.__version__},
             'scope':'Conditional finite-dimensional theory and short-time experiments; new extrapolation changes the boundary problem. No general PDE stability or long-distance propagation claim.',
             'historical_comparisons':'Initial perturbation comparison fields superseded by parametric_assessment.json after exact spline re-evaluation; original fields retained.'}
    manifest.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(checks),flush=True)

if __name__=='__main__':main()
