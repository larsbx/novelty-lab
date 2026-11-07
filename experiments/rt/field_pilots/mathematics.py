"""Bounded F5 Gram-defect contrasts; independent consumer oracle, not new kernel.

The generic identity has an upstream proof; these fixed configurations test
interpretations (in particular vanishing defect != planar rank).
"""
from experiments.rt.independent_reference import SplitQuadratic8, triple_spread_defect

F = SplitQuadratic8(5)
P = F.p
ZERO = (0,) * 8


def axis(i):
    if type(i) is not int or i not in range(8):
        raise ValueError("invalid coordinate")
    return tuple(int(j == i) for j in range(8))


def unit(i):
    return F.add(axis(i), F.scalar(pow(2, -1, P), axis(i + 4)))


def triple(x, y, z):
    """Only the three declared F5 vectors; no general-purpose Gram kernel."""
    vectors = (F.vector(x), F.vector(y), F.vector(z))
    norms = tuple(F.norm(v) for v in vectors)
    if 0 in norms:
        raise ValueError("null direction; spread undefined")
    a, b, c = norms
    inv2 = pow(2, -1, P)
    u = F.polar(x, y) * inv2 % P
    v = F.polar(y, z) * inv2 % P
    w = F.polar(z, x) * inv2 % P
    d = (a*b*c + 2*u*v*w - a*v*v - b*w*w - c*u*u) % P
    s = (F.spread(x, y), F.spread(y, z), F.spread(z, x))
    defect = triple_spread_defect(*s, P)
    gram_predicted = d*(4*u*v*w-d)*pow((a*b*c)**2, -1, P) % P
    return {"norms": norms, "spreads": s, "gram3": d, "defect": defect,
            "gram_predicted": gram_predicted, "agreement": defect == gram_predicted}


def run():
    x, y, z = (unit(i) for i in range(3))
    planar = triple(x, y, F.add(x, y))
    orthogonal = triple(x, y, z)
    nonplanar_zero = triple(x, F.add(x, axis(1)),
                            F.add(F.scalar(-1, x), F.scalar(2, axis(5))))
    if not (planar["defect"] == 0 and planar["gram3"] == 0
            and orthogonal["defect"] == 4
            and nonplanar_zero["gram3"] == 1
            and nonplanar_zero["defect"] == 0
            and all(r["agreement"] for r in (planar, orthogonal, nonplanar_zero))):
        raise AssertionError("Gram interpretation negative control failed")
    try:
        triple(axis(0), y, z)
    except ValueError:
        null_rejected = True
    else:
        raise AssertionError("null direction accepted")
    return {"discipline": "pure-mathematics", "status": "bounded-conformance",
            "field": "F5", "fixtures": 3, "planar": planar,
            "orthogonal_nonplanar": orthogonal, "nonplanar_zero_defect": nonplanar_zero,
            "null_guard_rejected": null_rejected,
            "scope": "three fixed triples; polynomial theorem imported, not newly proved"}
