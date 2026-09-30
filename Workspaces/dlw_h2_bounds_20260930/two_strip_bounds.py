"""Transfer C's global bounds to the current strip via exact witnesses.

The global upper bounds cover any subset. Each rational lower-bound witness
is realizable inside the specified physical domain at EVERY t in [0,.01].
Hence the same narrow enclosures bound the strip maximum at each such t.
"""
from pathlib import Path
import json
import sympy as s
from single_bounds import exp_positive_bounds

HERE=Path(__file__).resolve().parent
old=json.loads((HERE/'two_bounds.json').read_text(encoding='utf-8'))
# theta_2-theta_1=4t-5y/12. The intersection of the feasible odds-ratio
# windows over all t in [0,.01] is [exp(-117/200), exp(5/8)].
exp585lo,_=exp_positive_bounds(s.Rational(117,200))
exp625lo,_=exp_positive_bounds(s.Rational(5,8))
exp1lo,_=exp_positive_bounds(s.Rational(1))
out={'domain':'x in [-10,10], y in [-3/2,3/2], each fixed time in [0,1/100]',
     'method':'Global exact rational upper bounds and exactly admissible interior rational witnesses for lower bounds.',
     'bounds':{}}
for key,row in old['bounds'].items():
    r,t=map(s.Rational,row['witness'])
    odds1,odds2=r/(1-r),t/(1-t)
    ratio=odds2/odds1
    assert 1/exp585lo<ratio<exp625lo
    assert 1/exp1lo<odds1<exp1lo
    # y=(12/5)(4time-log(ratio)) is inside [-1.5,1.5].
    # x=log(odds1)+11time+y/12 is inside [-1.125,1.235],
    # itself a subset of [-10,10]. Both checks use rational exp enclosures.
    row['strip_witness_ratio']=str(ratio)
    row['physical_witness_x_enclosure']=['-9/8','247/200']
    row['strip_witness_valid_for_every_time']=True
    out['bounds'][key]=row
    print(key,row['bound'],'physical strip lower witness certified',flush=True)
(HERE/'two_strip_bounds.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

