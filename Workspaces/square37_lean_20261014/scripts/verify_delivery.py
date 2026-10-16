"""Validate current-source hashes, saved proof receipts and report links."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
status = json.loads((ROOT/'STATUS.json').read_text(encoding='utf-8'))
receipt = ROOT/status['final_receipt']
run = json.loads(receipt.read_text(encoding='utf-8'))
checks = [{'kind':'unified_lean_build', 'pass':run['status']=='PASSED'}]
for row in run['files']:
    p = Path(row['file'])
    checks.append({'kind':'current_source_matches_kernel_run', 'path':str(p.relative_to(ROOT)),
                   'pass':row['passed'] and row['exit_code']==0 and
                   hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']})
log = (receipt.parent/'build.log').read_text(encoding='utf-8')
axioms = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', log)
allowed = {'propext','Classical.choice','Quot.sound'}
checks.append({'kind':'printed_axioms', 'count':len(axioms),
               'pass':bool(axioms) and all(set(x.strip() for x in a.split(',') if x.strip())<=allowed for a in axioms)})
for name in ('n37_exact_verification.json','n37_provenance_audit.json'):
    data=json.loads((ROOT/'analysis'/name).read_text(encoding='utf-8'))
    checks.append({'kind':'saved_exact_check','path':name,'pass':data['all_pass']})
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key in ('href','src'): self.links.append(value)
report=ROOT.parents[1]/'report/square37_cantrell_lean_20261014.html'
parser=Links(); parser.feed(report.read_text(encoding='utf-8'))
for link in parser.links:
    if not urlparse(link).scheme and not link.startswith('#'):
        target=(report.parent/unquote(link.split('#')[0])).resolve()
        checks.append({'kind':'report_local_link','link':link,'pass':target.is_file()})
result={'all_pass':all(c['pass'] for c in checks), 'checks':checks,
        'scope':'Delivery integrity and receipt audit. Does not establish unrestricted optimality.'}
(ROOT/'analysis/delivery_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_pass':result['all_pass'],'checks':len(checks),'printed_axiom_lists':len(axioms)}))
if not result['all_pass']: raise SystemExit(1)
