"""Error decomposition at a common time reached by every configuration."""
from dynamics_study import run, write


if __name__=='__main__':
    rows=[run(case=case,h=h,T=.005,fit=False)
          for case in ('A','B') for h in (.25,.125,.0625)]
    assert all(r['complete'] for r in rows)
    write('dynamics_short_controls',rows)
