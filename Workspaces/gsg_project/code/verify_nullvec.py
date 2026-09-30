"""Verify the reported null vectors at FRESH random points (a null space found from
finitely many samples can be spurious)."""
import sympy as sp
from engine import DLW, random_point, e_add, e_scale

def combo(m, vec, stagger=False):
    f, g = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    s1 = m.a + m.h / 2 if stagger else m.a
    s2 = m.a - m.h / 2 if stagger else m.a
    terms = [m.B(f1, g, s=s1), m.B(f, g1, s=s2), m.B(f, g, s=m.a),
             m.Dx(f, g), m.Dx(f1, g), m.Dx(f, g1), m.Dx(f1, g1),
             m.bilin(f1, g1, ax=2)]
    return e_add(*[e_scale(t, c) for t, c in zip(terms, vec) if c != 0])

VECS = {
 'sym/uniform  [1,1,0,0,0,0,0,0]':
    ({1: 1, 2: 1}, False),
 'sym/uniform  [0,0,1,0,0,0,0,0]':
    ({3: 1}, False),
 'sym/uniform  [v3]':
    ({1: sp.Rational(-579460132783, 90291334452),
      4: sp.Rational(-1560733974977, 15048555742),
      5: sp.Rational(3897983818313, 45145667226), 6: 1}, False),
 'exp/uniform  [v3]':
    ({1: sp.Rational(-102805560936519, 94067556205636),
      4: sp.Rational(-5373454768936769, 423304002925362),
      5: sp.Rational(589516067706551, 47033778102818), 6: 1}, False),
}

# fix sym/uniform v3 with the exact rationals from the run (they were for the 8-column
# ordering: a1..a8 -> order in the script).
print("=" * 92)
print("Test each null-candidate at 12 FRESH random points")
print("=" * 92)
for name, (vec, stagger) in VECS.items():
    v = [vec.get(i, 0) for i in range(1, 9)]
    kind = name.split('/')[0]
    bad = 0
    for tt in range(12):
        m = DLW(1, h=sp.Rational(1, 3), kind=kind)
        m.set_point(random_point(m, seed=9000 + 13 * tt))
        r = combo(m, v, stagger)
        if len(r) != 0:
            bad += 1
    print(f"   {name:34s}  nonzero at {bad}/12 fresh points  -> "
          f"{'IDENTITY' if bad == 0 else 'spurious (not an identity)'}")
