"""Exact F5 cylinder: hitting one cycle does not destroy its homology class.

Three oriented side squares give top-bottom as a 2-boundary.
The fixture is deliberately finite; this is not a general homology library.
"""
from itertools import product

P = 5
EDGES = tuple("t%d" % i for i in range(3)) + tuple("b%d" % i for i in range(3)) + tuple("v%d" % i for i in range(3))


def chain(terms):
    out = [0] * 9
    for name, coefficient in terms:
        out[EDGES.index(name)] = (out[EDGES.index(name)] + coefficient) % P
    return tuple(out)


FACES = tuple(chain(((f"t{i}", 1), (f"b{i}", -1),
                     (f"v{(i+1)%3}", 1), (f"v{i}", -1))) for i in range(3))
TOP = chain(((f"t{i}", 1) for i in range(3)))
BOTTOM = chain(((f"b{i}", 1) for i in range(3)))


def lincomb(coeffs):
    if len(coeffs) != 3:
        raise ValueError("expected three square coefficients")
    return tuple(sum(c * FACES[i][e] for i, c in enumerate(coeffs)) % P for e in range(9))


def is_boundary(target):
    if len(target) != 9:
        raise ValueError("invalid chain")
    return any(lincomb(coeffs) == target for coeffs in product(range(P), repeat=3))


def boundary1(edge):
    """Tail/head in the fixed oriented cylinder graph."""
    k, i = edge[0], int(edge[1])
    if k == "t":
        return (("t", i), ("t", (i+1)%3))
    if k == "b":
        return (("b", i), ("b", (i+1)%3))
    if k == "v":
        return (("t", i), ("b", i))
    raise ValueError("unknown edge")


def is_cycle(c):
    endpoints = {}
    for e, coeff in zip(EDGES, c):
        tail, head = boundary1(e)
        endpoints[tail] = (endpoints.get(tail, 0) - coeff) % P
        endpoints[head] = (endpoints.get(head, 0) + coeff) % P
    return all(v == 0 for v in endpoints.values())


def run():
    delta = tuple((a-b)%P for a,b in zip(TOP,BOTTOM))
    if not (all(is_cycle(f) for f in FACES)
            and is_cycle(TOP) and is_cycle(BOTTOM)
            and lincomb((1,1,1)) == delta and is_boundary(delta)
            and not is_boundary(TOP) and not is_boundary(BOTTOM)):
        raise AssertionError("cylinder homology fixture invalid")
    # Pinning a top edge deletes the TOP representative and incident faces.
    # The BOTTOM representative survives and was nontrivial already in K.
    remaining_after_pin = tuple(e for e in EDGES if e != "t0")
    bottom_remains = all(EDGES[i] in remaining_after_pin for i,c in enumerate(BOTTOM) if c)
    if not bottom_remains:
        raise AssertionError("bottom witness unexpectedly removed")
    return {"discipline": "algebraic-topology", "status": "bounded-experiment",
            "field": "F5", "vertices": 6, "edges": len(EDGES),
            "square_faces": len(FACES), "top_is_cycle": True, "bottom_is_cycle": True,
            "top_minus_bottom_boundary": True,
            "top_nonboundary": True, "bottom_nonboundary": True,
            "top_witness_hit": True, "homologous_bottom_still_survives": bottom_remains,
            "scope": "fixed three-face cylinder; not a generic minimal leader solver"}
