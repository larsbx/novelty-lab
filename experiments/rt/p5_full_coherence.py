"""Full P5 permutation CW incidence and certified-face comparisons (bounded experiment).

P5 is dimension 4 (five labels). Exact signed integer incidences from ordered
partition facets, outward-first doubled-barycenter orientation; no floats.
Uses the earlier pinned-replay F5 route receipt verifier. Not a general
permutation polytope kernel or a training equivalence result.
"""

import itertools
import json
from collections import Counter, defaultdict
from math import comb

from experiments.rt.event_stream_v1 import (
    digest, make_envelope, sample_spec, verify_envelope,
)

N = 5
LABELS = tuple(range(N))


def ordered_partitions():
    """All faces: surjections from five labels onto ordered nonempty blocks."""
    for blocks in range(1, N + 1):
        for assignment in itertools.product(range(blocks), repeat=N):
            if len(set(assignment)) != blocks:
                continue
            yield tuple(tuple(i for i in LABELS if assignment[i] == k)
                        for k in range(blocks))


def dimension(face):
    return N - len(face)


def tangent_basis(face):
    """Tuples (j,root) stand for e_j - e_root, one per nonroot block label."""
    return tuple((j, block[0]) for block in face for j in block[1:])


def doubled_center(face):
    """Twice the mean of the contiguous coordinate values in each block."""
    result = [0] * N
    low = 1
    for block in face:
        high = low + len(block) - 1
        for i in block:
            result[i] = low + high
        low = high + 1
    return tuple(result)


def facets(face):
    """All codimension-one ordered refinements of one nontrivial block."""
    result = []
    for at, block in enumerate(face):
        if len(block) < 2:
            continue
        for sides in itertools.product((0, 1), repeat=len(block)):
            if 0 not in sides or 1 not in sides:
                continue
            a = tuple(block[i] for i, side in enumerate(sides) if side == 0)
            b = tuple(block[i] for i, side in enumerate(sides) if side == 1)
            result.append(face[:at] + (a, b) + face[at + 1:])
    return tuple(sorted(result))


def sign_determinant(matrix):
    """Small bounded integer determinant, no division and no field ordering."""
    n = len(matrix)
    total = 0
    for perm in itertools.permutations(range(n)):
        parity = sum(perm[i] > perm[j] for i in range(n)
                     for j in range(i + 1, n))
        term = -1 if parity % 2 else 1
        for i in range(n):
            term *= matrix[i][perm[i]]
        total += term
    if total == 0:
        raise AssertionError("singular face-orientation determinant")
    return 1 if total > 0 else -1


def incidence(face, facet):
    """Signed outward-normal-first boundary incidence of a geometric face."""
    if dimension(face) != dimension(facet) + 1 or facet not in facets(face):
        raise ValueError("not a codimension-one facet")
    a, b = doubled_center(face), doubled_center(facet)
    outward = tuple(b[i] - a[i] for i in LABELS)
    columns = (outward,) + tuple(
        tuple(int(i == j) - int(i == root) for i in LABELS)
        for j, root in tangent_basis(facet))
    # Components at nonroot indices are coordinates in the parent's tangent basis.
    indices = (j for j, _ in tangent_basis(face))
    return sign_determinant([[column[row] for column in columns] for row in indices])


def signed_sum(terms):
    result = defaultdict(int)
    for coeff, face in terms:
        result[face] += coeff
    return {key: val for key, val in result.items() if val}


def _permutation(vertex):
    if any(len(block) != 1 for block in vertex):
        raise ValueError("not a permutation vertex")
    return tuple(block[0] for block in vertex)


def _edge_key(vertices):
    return tuple(sorted(_permutation(vertex) for vertex in vertices))


class FullP5:
    """Reference P5 cellular chain over Z, dimensions 0 through 4."""

    def __init__(self):
        all_faces = tuple(ordered_partitions())
        self.cells = {d: tuple(face for face in all_faces if dimension(face) == d)
                      for d in range(N)}
        self.boundary = {
            face: {facet: incidence(face, facet) for facet in facets(face)}
            for d in range(1, N) for face in self.cells[d]
        }
        self.edge_of = {face: _edge_key(self.boundary[face])
                        for face in self.cells[1]}
        if len(set(self.edge_of.values())) != 240:
            raise AssertionError("P5 edge incidence is not injective")

    def differential_squared(self):
        """Return explicit nonzero residue if d_{k-1}d_k fails, else {}."""
        defects = {}
        for d in range(2, N):
            for cell in self.cells[d]:
                residue = signed_sum(
                    (outer * inner, subface)
                    for facet, outer in self.boundary[cell].items()
                    for subface, inner in self.boundary[facet].items())
                if residue:
                    defects[cell] = residue
        return defects

    def face_fvector(self):
        return tuple(len(self.cells[d]) for d in range(N))

    def face_types(self):
        return {
            "squares": sum(len(self.boundary[f]) == 4 for f in self.cells[2]),
            "hexagons": sum(len(self.boundary[f]) == 6 for f in self.cells[2]),
            "P4_facets": sum(len(self.boundary[f]) == 14 for f in self.cells[3]),
            "hexagonal_prisms": sum(len(self.boundary[f]) == 8 for f in self.cells[3]),
        }

    def requested_closure(self, requested):
        """Materialize the cellular boundary closure of named face witnesses."""
        if any(dimension(face) not in self.cells or
               face not in self.cells[dimension(face)] for face in requested):
            raise ValueError("unknown requested P5 face")
        closure = set(requested)
        frontier = list(closure)
        while frontier:
            face = frontier.pop()
            for facet in self.boundary.get(face, ()):
                if facet not in closure:
                    closure.add(facet)
                    frontier.append(facet)
        return tuple(sum(dimension(face) == d for face in closure) for d in range(N))

    def admitted(self, permitted_edges):
        """All higher cells whose complete oriented facet closure is permitted."""
        accepted = {}
        for face, edge in self.edge_of.items():
            accepted[face] = edge in permitted_edges
        for d in range(2, N):
            for face in self.cells[d]:
                accepted[face] = all(accepted[facet] for facet in self.boundary[face])
        return {
            "admitted_cell_counts": tuple(
                len(self.cells[0]) if d == 0 else
                sum(accepted[face] for face in self.cells[d])
                for d in range(N)),
            "top_admitted": accepted[self.cells[4][0]],
        }


def rank_f5(columns):
    """Independently labelled *bounded* F5 cellular rank oracle, not shared math."""
    pivots = {}
    for column in columns:
        work = {k: v % 5 for k, v in column.items() if v % 5}
        while work:
            leading = min(work)
            if leading not in pivots:
                inv = pow(work[leading], -1, 5)
                pivots[leading] = {k: val * inv % 5 for k, val in work.items()}
                break
            scale = work[leading]
            for k, v in pivots[leading].items():
                remainder = (work.get(k, 0) - scale * v) % 5
                if remainder:
                    work[k] = remainder
                else:
                    work.pop(k, None)
    return len(pivots)


def homology_profile(p):
    ranks = {d: rank_f5(p.boundary[face] for face in p.cells[d])
             for d in range(1, N)}
    betti_filled = tuple(
        len(p.cells[d]) - ranks.get(d, 0) - ranks.get(d + 1, 0)
        for d in range(N))
    betti_boundary = tuple(
        len(p.cells[d]) - ranks.get(d, 0) -
        (0 if d == 3 else ranks.get(d + 1, 0))
        for d in range(4))
    return {"boundary_ranks_F5": tuple(ranks[d] for d in range(1, N)),
            "filled_betti_F5": betti_filled, "boundary_betti_F5": betti_boundary}


def audit_receipt(p, payload, independently_trusted_spec_sha):
    """Accept no P5 face from raw JSON before exact externally pinned replay."""
    verified = verify_envelope(payload, independently_trusted_spec_sha)
    if verified["coherence_labels"] != 5:
        raise ValueError("P5 admission needs five influence labels")
    envelope = json.loads(payload)
    certified_edges = {
        tuple(sorted((tuple(r["source"]), tuple(r["target"]))))
        for r in envelope["records"] if r["admitted"]
    }
    if not certified_edges.issubset(set(p.edge_of.values())):
        raise AssertionError("unrecognized P5 rewrite edge")
    promoted = p.admitted(certified_edges)
    return {
        "direction_rank": verified["direction_rank"],
        "potential_swaps": verified["potential_edges"],
        "audited_swaps": verified["audited_edges"],
        "geometric_passes": verified["geometric_edges"],
        "semantic_failures": verified["blocked_effect_edges"],
        **promoted,
        "scope": verified["scope"],
    }


def cube_fvector(influences=5):
    """Independent frozen-additive subset cube, dimension = influences."""
    return tuple(comb(influences, d) * (2 ** (influences - d))
                 for d in range(influences + 1))


def run():
    p = FullP5()
    if p.differential_squared():
        raise AssertionError("nonzero cellular boundary composition")
    types = p.face_types()
    h = homology_profile(p)
    expected_fvector = (120, 240, 150, 30, 1)
    if (p.face_fvector() != expected_fvector or
            types != {"squares": 90, "hexagons": 60,
                      "P4_facets": 10, "hexagonal_prisms": 20} or
            h["boundary_ranks_F5"] != (119, 121, 29, 1) or
            h["filled_betti_F5"] != (1, 0, 0, 0, 0) or
            h["boundary_betti_F5"] != (1, 0, 0, 1)):
        raise AssertionError("P5 exact face/homology negative control failed")

    modes = {}
    for label in ("translations", "coupled", "null_defect"):
        spec = sample_spec(5, label, 1)
        modes[label] = audit_receipt(p, make_envelope(spec), digest(spec))
    rank_two = sample_spec(5, "translations", 2)
    modes["grassmann_rank2"] = audit_receipt(
        p, make_envelope(rank_two), digest(rank_two))
    sparse_spec = sample_spec(5)
    sparse = [[list(a), list(b)] for a, b in sorted(p.edge_of.values())[:2]]
    modes["requested_only"] = audit_receipt(
        p, make_envelope(sparse_spec, sparse), digest(sparse_spec))
    if (modes["translations"]["admitted_cell_counts"] != expected_fvector or
            modes["coupled"]["admitted_cell_counts"] != (120, 216, 114, 16, 0) or
            modes["null_defect"]["admitted_cell_counts"] != (120, 216, 114, 16, 0) or
            not modes["grassmann_rank2"]["top_admitted"] or
            modes["requested_only"]["top_admitted"]):
        raise AssertionError("P5 semantic/coherence comparison failed")

    return {
        "status": "bounded-experiment", "field": "F5",
        "P3_cells": (6, 6, 1), "P4_cells": (24, 36, 14, 1),
        "P5_cells": p.face_fvector(), "P5_face_types": types,
        "P5_chain": {"boundary_squared_zero": True, **h},
        "additive_five_cube_cells": cube_fvector(5),
        "verified_receipts": modes,
        "scope": "full P5 cellular incidence; finite F5 state-dependent certificates",
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
