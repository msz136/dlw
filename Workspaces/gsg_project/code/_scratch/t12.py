import sympy as sp
from engine import DLW, e_add, e_scale
tests=[([3,5],[2,4],7),([4,1],[14,8],18),([6,9],[1,3],4),([2,8],[5,7],11),
       ([4,1],[14,8],sp.Rational(37,2)),([8,sp.Rational(4,7)],[2,3],1)]
for Nval in (2,):
    for ps,qs,a in tests:
        m=DLW(2,kind="none")
        m.set_point({m.p[0]:sp.nsimplify(ps[0]),m.p[1]:sp.nsimplify(ps[1]),
                     m.q[0]:sp.nsimplify(qs[0]),m.q[1]:sp.nsimplify(qs[1]),m.a:sp.nsimplify(a)})
        f,g=m.tau(1),m.tau(0)
        r7=m.B(f,g)
        r6=e_add(m.DyB(f,g),e_scale(m.Dx(f,g),-4))
        ok7 = len(r7)==0
        ok6 = len(r6)==0
        print(f"p={ps} q={qs} a={a}: engine eq7={ok7} eq6={ok6}"
              + ("" if ok7 else f"  r7={ {k:sp.nsimplify(v) for k,v in r7.items()} }"))
