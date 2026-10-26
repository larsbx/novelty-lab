"""Six-influence certificate-demanded permutohedral coherence, bounded F5 experiment.

P6 is a five-dimensional permutohedron. This non-authoritative consumer driver
checks signed integer incidence and separately gates *actual local effects* of
six deterministic F5 updates. Its finite comparator is not rt-route-stream/v1:
that external schema explicitly stops at five updates.
"""
from collections import defaultdict
from itertools import product, permutations
from math import factorial, comb
import json

from experiments.rt.rank_lift_pilot import F, rank2_spread
from experiments.rt.p5_full_coherence import FullP5, rank_f5

N = 6
LABELS = tuple(range(N))
ORIGIN = (0,) * 8
NULL_E0 = (1,) + (0,) * 7


def validate_face(face):
    if type(face) is not tuple or not 1 <= len(face) <= N:
        raise ValueError("expected an ordered P6 partition")
    if any(type(block) is not tuple or not block or
           block != tuple(sorted(block)) or
           any(type(value) is not int for value in block) for block in face):
        raise ValueError("noncanonical partition block")
    if tuple(sorted(value for block in face for value in block)) != LABELS:
        raise ValueError("not a partition of six labels")
    return face


def dimension(face):
    return N - len(face)


def facets(face):
    """Single-block ordered splits; does not enumerate all P6 cells."""
    children = []
    for at, block in enumerate(face):
        if len(block) < 2:
            continue
        for assignments in product((0, 1), repeat=len(block)):
            if set(assignments) != {0, 1}:
                continue
            a = tuple(v for v, side in zip(block, assignments) if side == 0)
            b = tuple(v for v, side in zip(block, assignments) if side == 1)
            children.append(face[:at] + (a, b) + face[at + 1:])
    return tuple(sorted(children))


def doubled_center(face):
    center, lo = [0] * N, 1
    for block in face:
        hi = lo + len(block) - 1
        for i in block:
            center[i] = lo + hi
        lo = hi + 1
    return tuple(center)


def tangent_basis(face):
    return tuple((v, block[0]) for block in face for v in block[1:])


def exact_sign_determinant(matrix):
    """Fixed n<=5 tiny integer determinants, no rational/float arithmetic."""
    size = len(matrix)
    det = 0
    for permutation in permutations(range(size)):
        sign = -1 if sum(permutation[i] > permutation[j]
                         for i in range(size) for j in range(i + 1, size)) % 2 else 1
        term = sign
        for i in range(size):
            term *= matrix[i][permutation[i]]
        det += term
    if det == 0:
        raise AssertionError("degenerate permutohedral orientation basis")
    return 1 if det > 0 else -1


def incidence(parent, child):
    """Outward-first signed incidence for an immediate P6 facet."""
    if child not in facets(parent):
        raise ValueError("not a P6 facet")
    x, y = doubled_center(parent), doubled_center(child)
    columns = (tuple(y[i] - x[i] for i in LABELS),) + tuple(
        tuple(int(i == j) - int(i == root) for i in LABELS)
        for j, root in tangent_basis(child))
    return exact_sign_determinant([
        [col[row] for col in columns] for row, _ in tangent_basis(parent)
    ])


def expected_fvector():
    """Independent Stirling-number count k! S(6,k), ordered partitions."""
    stirling = [[0] * 7 for _ in range(7)]
    stirling[0][0] = 1
    for n in range(1, 7):
        for k in range(1, n + 1):
            stirling[n][k] = k * stirling[n - 1][k] + stirling[n - 1][k - 1]
    return tuple(factorial(N - d) * stirling[N][N - d] for d in range(N))


def cube_fvector():
    """Six independent frozen subset additions, a dimension-six cube."""
    return tuple(comb(N, d) * 2 ** (N - d) for d in range(N + 1))


class DemandP6:
    """Actual on-demand P6 signed-face cache, not eager face selection."""

    def __init__(self):
        self.boundaries = {}
        self.incidence_calls = 0

    def request(self, faces, max_cells=None):
        if type(faces) not in (tuple, list):
            raise ValueError("faces must be an ordered sequence")
        if max_cells is not None and (type(max_cells) is not int or max_cells < 0):
            raise ValueError("invalid materialization budget")
        requested = tuple(validate_face(face) for face in faces)
        staged, calls = {}, 0

        def visit(face):
            nonlocal calls
            if face in staged or face in self.boundaries:
                return
            if max_cells is not None and len(self.boundaries) + len(staged) >= max_cells:
                raise ValueError("P6 cell budget exhausted")
            staged[face] = {}
            boundary = {}
            for child in facets(face):
                visit(child)
                boundary[child] = incidence(face, child)
                calls += 1
            staged[face] = boundary

        for face in requested:
            visit(face)
        self.boundaries.update(staged)
        self.incidence_calls += calls
        return {"cells_by_dimension": self.counts(),
                "new_cells": len(staged), "new_incidence_calls": calls}

    def counts(self):
        return tuple(sum(dimension(f) == d for f in self.boundaries)
                     for d in range(N))

    def chain_defects(self):
        """Return all nonzero integer coefficients of d_(k-1) d_k."""
        defects = {}
        for face, boundary in self.boundaries.items():
            if dimension(face) < 2:
                continue
            coefficients = defaultdict(int)
            for child, outer in boundary.items():
                if child not in self.boundaries:
                    raise AssertionError("incomplete face boundary")
                for lower, inner in self.boundaries[child].items():
                    coefficients[lower] += outer * inner
            residual = {lower: c for lower, c in coefficients.items() if c}
            if residual:
                defects[face] = residual
        return defects

    def compare_p5_facet(self):
        """Check all signed incidences against already certified P5 reference.

        The canonical P5 facet is on 0..4, with label 5 as a final singleton;
        its orientation agrees with the P5 reference under this embedding.
        """
        parent = ((0, 1, 2, 3, 4), (5,))
        if parent not in self.boundaries:
            raise ValueError("first materialize the canonical P5 facet")
        reference = FullP5()
        number = 0
        for d in range(5):
            for face in reference.cells[d]:
                embedded = face + ((5,),)
                expected = ({} if d == 0 else
                            {child + ((5,),): sign
                             for child, sign in reference.boundary[face].items()})
                if self.boundaries.get(embedded) != expected:
                    raise AssertionError("P6/P5 orientation or face disagreement")
                number += 1
        return number

    def admitted_profile(self, allowed_edges):
        """Effect-gated subcomplex and exact F5 cellular ranks, no float."""
        allowed = set(allowed_edges)
        yes, counts = {}, [0] * N
        for face in sorted(self.boundaries, key=lambda f: (dimension(f), f)):
            d = dimension(face)
            if d == 0:
                good = True
            elif d == 1:
                endpoints = sorted(tuple(block[0] for block in vertex)
                                   for vertex in self.boundaries[face])
                good = tuple(endpoints) in allowed
            else:
                good = all(yes[child] for child in self.boundaries[face])
            yes[face] = good
            counts[d] += good
        selected = {d: tuple(f for f in self.boundaries
                              if dimension(f) == d and yes[f])
                    for d in range(N)}
        ranks = {d: rank_f5(self.boundaries[f] for f in selected[d])
                 for d in range(1, N)}
        betti = tuple(counts[d] - ranks.get(d, 0) - ranks.get(d + 1, 0)
                      for d in range(N))
        return {"admitted_cells": tuple(counts),
                "boundary_ranks_F5": tuple(ranks[d] for d in range(1, N)),
                "betti_F5": betti}


def directions():
    """Six non-null directions in split F5^8; NOT six orthogonal rays."""
    result = []
    half = pow(2, -1, 5)
    for axis in range(4):
        v = [0] * 8
        v[axis], v[axis + 4] = 1, half
        result.append(tuple(v))
    negative = [0] * 8
    negative[0], negative[4] = 1, (-half) % 5
    result.append(tuple(negative))
    result.append(F.add(result[2], result[3]))
    if not all(F.norm(v) for v in result):
        raise AssertionError("declared direction is null")
    return tuple(result)


DIRECTIONS = directions()
MODES = ("translations", "scalar_coupled", "null_defect")


def update(x, label, mode):
    if mode not in MODES or label not in LABELS:
        raise ValueError("unsupported update")
    if label != 0 or mode == "translations":
        return F.add(x, DIRECTIONS[label])
    if mode == "scalar_coupled":
        return F.add(x, F.scalar(1 + x[1], DIRECTIONS[0]))
    return F.add(F.add(x, DIRECTIONS[0]), F.scalar(x[1], NULL_E0))


def spread_for(a, b, label, rank):
    if rank == 1:
        return F.spread(a, b)
    if rank == 2:
        probe = DIRECTIONS[(label + 1) % N]
        return rank2_spread((a, probe), (b, probe))
    raise ValueError("direction rank must be 1 or 2")


def audit_updates(mode, direction_rank=1):
    """All 1800 actual shared-prefix adjacent swaps, exactly recomputed."""
    if mode not in MODES or direction_rank not in (1, 2):
        raise ValueError("invalid mode or direction rank")
    gate = {0, 3} if mode == "null_defect" else {0}
    allowed = set()
    geometric = effect_equal = nonzero_null_residuals = 0
    for route in permutations(LABELS):
        for position in range(N - 1):
            exchanged = (route[:position] +
                         (route[position + 1], route[position]) +
                         route[position + 2:])
            if route > exchanged:
                continue
            state = ORIGIN
            for label in route[:position]:
                state = update(state, label, mode)
            a, b = route[position:position + 2]
            after_a, after_b = update(state, a, mode), update(state, b, mode)
            ab = update(after_a, b, mode)
            ba = update(after_b, a, mode)
            da, db = F.sub(after_a, state), F.sub(after_b, state)
            da_after = F.sub(ba, after_b)
            db_after = F.sub(ab, after_a)
            s1 = spread_for(da, da_after, a, direction_rank)
            s2 = spread_for(db, db_after, b, direction_rank)
            passes = s1 is not None and s2 is not None and s1 in gate and s2 in gate
            equal = ab == ba  # whole vector, never merely Q(ab-ba)==0
            geometric += passes
            effect_equal += equal
            if not equal and F.norm(F.sub(ab, ba)) == 0:
                nonzero_null_residuals += 1
            if passes and equal:
                allowed.add((route, exchanged))
    return {"mode": mode, "direction_rank": direction_rank,
            "potential_swaps": factorial(N) * (N - 1) // 2,
            "geometric_passes": geometric, "effect_equal": effect_equal,
            "certified_swaps": len(allowed),
            "effect_rejected": geometric - len(allowed),
            "nonzero_null_residuals": nonzero_null_residuals}, allowed


def experiment():
    p = DemandP6()
    square = ((0, 1), (2, 3), (4,), (5,))
    hexagon = ((0, 1, 2), (3,), (4,), (5,))
    p5_facet = ((0, 1, 2, 3, 4), (5,))
    first = p.request((square,), max_cells=9)
    if first["cells_by_dimension"] != (4, 4, 1, 0, 0, 0):
        raise AssertionError("square closure expanded unexpectedly")
    memo = (len(p.boundaries), p.incidence_calls)
    try:
        p.request((hexagon,), max_cells=9)
    except ValueError:
        pass
    else:
        raise AssertionError("insufficient budget did not fail")
    if memo != (len(p.boundaries), p.incidence_calls):
        raise AssertionError("budget failure mutated cache")
    p.request((p5_facet,))
    p5_agreement = p.compare_p5_facet()
    if p5_agreement != 541 or p.chain_defects():
        raise AssertionError("P5 facet cross-check failed")
    top = (LABELS,)
    p.request((top,))
    expected = expected_fvector()
    if p.counts() != expected or p.chain_defects():
        raise AssertionError("P6 complete incidence is invalid")
    comparisons = {}
    for mode in MODES:
        details, allowed = audit_updates(mode)
        details.update(p.admitted_profile(allowed))
        comparisons[mode] = details
    rank2, allowed2 = audit_updates("translations", direction_rank=2)
    rank2.update(p.admitted_profile(allowed2))
    comparisons["grassmann_rank2"] = rank2
    full = (720, 1800, 1560, 540, 62, 1)
    partial = (720, 1680, 1320, 390, 32, 0)
    if (comparisons["translations"]["admitted_cells"] != full or
        comparisons["grassmann_rank2"]["admitted_cells"] != full or
        comparisons["scalar_coupled"]["admitted_cells"] != partial or
        comparisons["null_defect"]["admitted_cells"] != partial or
        comparisons["null_defect"]["nonzero_null_residuals"] != 120 or
        comparisons["translations"]["boundary_ranks_F5"] !=
            (719, 1081, 479, 61, 1) or
        comparisons["translations"]["betti_F5"] !=
            (1, 0, 0, 0, 0, 0) or
        comparisons["scalar_coupled"]["boundary_ranks_F5"] !=
            (718, 962, 358, 32, 0) or
        comparisons["scalar_coupled"]["betti_F5"] !=
            (2, 0, 0, 0, 0, 0)):
        raise AssertionError("P6 effect-gated comparison differs")
    return {"status": "bounded-experiment", "field": "F5",
            "coherence_labels": N, "top_cell_dimension": N - 1,
            "full_P6_fvector": expected, "full_cells": sum(expected),
            "P5_facet_signed_cross_checks": p5_agreement,
            "first_requested_square": first,
            "budget_failure_atomic": True, "integer_d_squared_zero": True,
            "additive_six_cube_fvector": cube_fvector(),
            "modes": comparisons,
            "scope": "finite P6 combinatorics and internal six-update F5 audit only"}


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True))
