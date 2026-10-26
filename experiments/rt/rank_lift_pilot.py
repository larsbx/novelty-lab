"""Bounded F5 RT coherence pilot; non-authoritative consumer experiment.

P3 is a two-dimensional hexagon, not a 3-cell. A frozen additive
three-influence update instead has a cubical 3-cell. Spread gates label
admissible FORMAL rewrites, not semantic equivalence of training schedules.
Uses the independent RT oracle, not a second mathematical kernel.
"""

import json
from itertools import combinations

from experiments.rt.independent_reference import SplitQuadratic8

F = SplitQuadratic8(5)
LABELS = (0, 1, 2)
HEXAGON = ((0, 1, 2), (1, 0, 2), (1, 2, 0),
           (2, 1, 0), (2, 0, 1), (0, 2, 1))


def _accumulate(terms):
    """Add signed incidence coefficients; only this pilot's tiny cell chains."""
    out = {}
    for coefficient, key in terms:
        out[key] = out.get(key, 0) + coefficient
    return {key: coefficient for key, coefficient in out.items() if coefficient}


def endpoint_boundary(edge):
    source, target = edge
    return ((-1, source), (1, target))


def hexagon_boundary():
    """P3 face boundary, with edges oriented along the six permutations."""
    return tuple((1, (HEXAGON[i], HEXAGON[(i + 1) % 6])) for i in range(6))


def cubical_edge(point, axis):
    if point[axis] != 0:
        raise ValueError("cubical edge needs a zero coordinate")
    target = list(point)
    target[axis] = 1
    return point, tuple(target)


def cubical_face(missing, fixed):
    """Oriented square: the remaining two axes, in increasing order."""
    a, b = (axis for axis in LABELS if axis != missing)
    start = tuple(fixed if axis == missing else 0 for axis in LABELS)
    va = cubical_edge(start, a)[1]
    vb = cubical_edge(start, b)[1]
    return ((1, cubical_edge(start, a)),
            (1, cubical_edge(va, b)),
            (-1, cubical_edge(vb, a)),
            (-1, cubical_edge(start, b)))


def cube_boundary():
    """Boundary of the oriented 3-cube with product-coordinate orientation."""
    return tuple(((-1) ** missing * (1 if fixed else -1), (missing, fixed))
                 for missing in LABELS for fixed in (0, 1))


def boundary_squared_is_zero():
    hex_boundary = _accumulate((coeff * ec, point)
                               for coeff, edge in hexagon_boundary()
                               for ec, point in endpoint_boundary(edge))
    cube_face_boundaries = {
        face: cubical_face(*face) for _, face in cube_boundary()
    }
    cube_boundary_twice = _accumulate((coeff * ec, edge)
                                      for coeff, face in cube_boundary()
                                      for ec, edge in cube_face_boundaries[face])
    return hex_boundary == {} and cube_boundary_twice == {}


def directions():
    """Three pairwise orthogonal non-null norm-one directions in split F5^8."""
    result = []
    for axis in LABELS:
        x = [0] * 8
        x[axis] = 1
        x[axis + 4] = pow(2, -1, F.p)
        result.append(tuple(x))
    return tuple(result)


def permitted(dirs, gate):
    """All three cross-influence RT spreads must satisfy the declared gate."""
    values = tuple(F.spread(dirs[i], dirs[j]) for i, j in combinations(LABELS, 2))
    return None not in values and all(value in gate for value in values), values


def rank2_spread(U, W):
    """Guarded rank-two Grassmann spread; exact 2x2 Gram determinants only."""
    if len(U) != 2 or len(W) != 2:
        raise ValueError("rank-two basis required")

    def g(a, b):
        return F.polar(a, b) * pow(2, -1, F.p) % F.p

    def det2(A, B):
        return (g(A[0], B[0]) * g(A[1], B[1]) -
                g(A[0], B[1]) * g(A[1], B[0])) % F.p

    den = det2(U, U) * det2(W, W) % F.p
    if not den:
        return None
    overlap = det2(U, W) ** 2 * pow(den, -1, F.p) % F.p
    return (1 - overlap) % F.p


def pilot():
    dirs = directions()
    accepted, spreads = permitted(dirs, {1})
    rejected, _ = permitted(dirs, {0})
    if not boundary_squared_is_zero() or not accepted or rejected:
        raise AssertionError("coherence/guard negative control failed")
    plane1 = (dirs[0], dirs[1])
    plane2 = (F.add(dirs[0], dirs[2]), F.add(dirs[1], dirs[2]))
    # Distinct nondegenerate 2-planes; basis change leaves the ratio fixed.
    value = rank2_spread(plane1, plane2)
    changed = (F.add(plane1[0], plane1[1]), plane1[1])
    if value is None or value != rank2_spread(changed, tuple(reversed(plane2))):
        raise AssertionError("Grassmann basis-change check failed")
    return {
        "status": "bounded-experiment", "field": "F5", "labels": 3,
        "spreads": spreads, "gate_accepts": accepted, "negative_gate_rejects": not rejected,
        "permutohedron": {"dimension": 2, "vertices": 6, "edges": 6, "faces_2": 1,
                          "H1_without_face": 1, "H1_with_face": 0},
        "additive_cube": {"dimension": 3, "vertices": 8, "edges": 12,
                          "faces_2": 6, "cells_3": 1,
                          "boundary_twice_zero": True},
        "rank2_spread": value,
        "qualification": "formal coherence / additive frozen-contribution model only",
    }


if __name__ == "__main__":
    print(json.dumps(pilot(), sort_keys=True))
