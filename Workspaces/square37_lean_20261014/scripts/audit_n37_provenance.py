"""Audit recorded input/output hashes after the three independent n=37 checks."""
from pathlib import Path
import hashlib,json

BASE=Path(__file__).resolve().parents[1]
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest=BASE/'references/n37/source_manifest.json'
    source=json.loads(manifest.read_text());checks=[]
    commit=json.loads((BASE/'references/n37/repository_commit.json').read_text())
    assert commit['sha']==source['repository_commit']
    checks.append({'kind':'git_commit_metadata','pass':True,'commit':commit['sha'],'tree':commit['commit']['tree']['sha']})
    for row in source['files']:
        path=BASE/'references/n37'/row['file']
        assert SHA(path)==row['sha256'] and path.stat().st_size==row['size']
        checks.append({'kind':'source','path':str(path.relative_to(BASE)),'pass':True,'sha256':SHA(path)})
    reports=[('analysis/n37_exact_verification.json','scripts/verify_n37_certificate.py'),('analysis/n37_fixed_branch_dual.json','scripts/n37_support_analysis.py'),('analysis/n37_symbolic_support.json','scripts/n37_symbolic_support.py'),('analysis/n37_bernstein_support.json','scripts/n37_bernstein_support.py')]
    for rp,sp in reports:
        report=json.loads((BASE/rp).read_text());assert report['script_sha256']==SHA(BASE/sp)
        if 'certificate_sha256' in report:assert report['certificate_sha256']==SHA(BASE/'certificates/n37_rational_sat.json')
        if 'source_manifest_sha256' in report:assert report['source_manifest_sha256']==SHA(manifest)
        checks.append({'kind':'report_and_code','path':rp,'pass':True,'sha256':SHA(BASE/rp),'script':sp,'script_sha256':SHA(BASE/sp)})
    result={'all_pass':True,'scope':'Provenance integrity only; mathematical results are in the referenced exact and symbolic reports.','checks':checks,'certificate_sha256':SHA(BASE/'certificates/n37_rational_sat.json'),'derivation_sha256':SHA(BASE/'analysis/conditional_support_derivation.md')}
    (BASE/'analysis/n37_provenance_audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print('provenance checks',len(checks),'all pass')

if __name__=='__main__':main()
