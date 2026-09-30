"""Recheck locked decisions, identities, controls and source/data hashes."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/injection_amplification'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def check_source(data):
    for rel,want in data.get('source_sha256',data.get('sources_sha256',{})).items():
        assert sha(ROOT/rel)==want,rel


def main():
    lock=json.loads((OUT/'locked_rule.json').read_text(encoding='utf-8'))
    mech=json.loads((OUT/'mechanism.json').read_text(encoding='utf-8'))
    held=json.loads((OUT/'holdout.json').read_text(encoding='utf-8'))
    p5=json.loads((OUT/'p5_controls.json').read_text(encoding='utf-8'))
    multi=json.loads((OUT/'multisoliton.json').read_text(encoding='utf-8'))
    cost=json.loads((OUT/'rule_cost.json').read_text(encoding='utf-8'))
    time_lock=json.loads((OUT/'locked_time_rule.json').read_text(encoding='utf-8'))
    time_held=json.loads((OUT/'time_holdout.json').read_text(encoding='utf-8'))
    count=0
    for data in (lock,mech,held,p5,multi,cost,time_lock,time_held):check_source(data);count+=1
    assert held['locked_rule_sha256']==sha(OUT/'locked_rule.json');count+=1
    assert cost['locked_rule_sha256']==sha(OUT/'locked_rule.json');count+=1
    assert time_lock['base_rule_sha256']==sha(OUT/'locked_rule.json');count+=1
    assert time_held['locked_time_rule_sha256']==sha(OUT/'locked_time_rule.json');count+=1
    assert len(cost['rows'])==4;count+=1
    for row in cost['rows']:
        assert row['feature_median_seconds']>0
        assert row['selector_plus_selected_to_baseline_advance_ratio']>=1
        count+=1
    assert len(mech['runs'])==18;count+=1
    for row in mech['runs']:
        assert row['complete'];count+=1
        if 'linear' in row:
            assert row['split_closure_residual']<1e-11;count+=1
            assert max(row['linear_prediction_relative'])<1e-3;count+=1
    assert len(held['results'])==4;count+=1
    for row in held['results']:
        assert len(row['runs'])==6;count+=1
        chosen=next(r for r in row['runs'] if r['h']==row['chosen']['h'] and r['nx']==row['chosen']['nx'])
        assert chosen['observed_pass'];count+=1
        for r in row['runs']:
            assert r['complete'] and r['decomposition_residual']<1e-13;count+=1
            assert not any(r['predicted_upper_violations']);count+=1
    assert len(time_held['results'])==2;count+=1
    time_underestimates=0
    for row in time_held['results']:
        assert len(row['runs'])==6;count+=1
        selected=next(r for r in row['runs'] if r['h']==row['chosen']['h'] and r['nx']==row['chosen']['nx'])
        assert selected['observed_pass'];count+=1
        for r in row['runs']:
            assert r['complete'] and r['decomposition_residual']<1e-13;count+=1
            time_underestimates+=int(any(r['predicted_upper_violations']))
    assert time_underestimates==5;count+=1
    p5rows={(r['nx'],r['dt']):r for r in p5['runs']}
    assert len(p5rows)==4;count+=1
    for r in p5['runs']:
        assert r['tangent_fd_residual']<2e-8;count+=1
    fine=p5rows[(512,.00025)]['records'][-1]['actual']
    half=p5rows[(512,.000125)]['records'][-1]['actual']
    coarse=p5rows[(256,.00025)]['records'][-1]['actual']
    assert max(abs(a-b)/a for a,b in zip(fine,half))<.001;count+=1
    assert min(a/b for a,b in zip(fine,coarse))>1000;count+=1
    assert len(multi['results'])==6;count+=1
    by={r['label']:r for r in multi['results']}
    for stage,control in (('N2_separated_before','matched_N1_before'),
                          ('N2_separated_after','matched_N1_after')):
        for x,y in zip(by[stage]['u_v_error'],by[control]['u_v_error']):
            assert abs(x-y)/y<.01;count+=1
    for r in multi['results']:
        assert r['complete'];count+=1
        assert max(a/max(b,1e-30) for a,b in zip(r['nonlinear_remainder'],r['u_v_error']))<.001;count+=1
    files=['mechanism.json','locked_rule.json','holdout.json','p5_controls.json','multisoliton.json','rule_cost.json','locked_time_rule.json','time_holdout.json']
    manifest={'checks_passed':count,'data_sha256':{name:sha(OUT/name) for name in files}}
    (OUT/'validation.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('PASS',count,'checks')


if __name__=='__main__':main()
