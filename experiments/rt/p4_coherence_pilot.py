"""Non-authoritative exact P4 incidence and tensor-direction adapter pilot.

CW dimension, number of influences, tensor direction rank, and certificate
materialization budget are independent. This is finite combinatorics, not
proof of equivalence of state-dependent model updates.
"""

import itertools
import json
from collections import defaultdict, deque
from dataclasses import dataclass

from experiments.rt.rank_lift_pilot import F, rank2_spread

LABELS = (0, 1, 2, 3)


def ordered_partitions(labels=LABELS):
    """Generate faces as ordered nonempty blocks, without duplicate faces."""
    labels = tuple(labels)
    for slots in range(1, len(labels) + 1):
        for assignment in itertools.product(range(slots), repeat=len(labels)):
            if set(assignment) != set(range(slots)):
                continue
            yield tuple(tuple(labels[i] for i in range(len(labels))
                              if assignment[i] == slot) for slot in range(slots))


def vertices_of(face):
    """Permutations refining an ordered set partition."""
    choices = [itertools.permutations(block) for block in face]
    return frozenset(tuple(itertools.chain.from_iterable(parts))
                     for parts in itertools.product(*choices))


def _edge(a, b):
    return tuple(sorted((a, b)))


def _boundary_path(vertices, adjacency):
    """Orient polygon at its least vertex by its least neighboring vertex."""
    start = min(vertices)
    first = min(adjacency[start])
    route = [start, first]
    while True:
        options = adjacency[route[-1]] - {route[-2]}
        if len(options) != 1:
            raise AssertionError("face boundary is not a simple polygon")
        nxt = next(iter(options))
        if nxt == start:
            break
        if nxt in route:
            raise AssertionError("premature boundary repetition")
        route.append(nxt)
    if len(route) != len(vertices):
        raise AssertionError("face boundary disconnected")
    return tuple(route)


def add_terms(terms):
    result = defaultdict(int)
    for coefficient, key in terms:
        result[key] += coefficient
    return {key: n for key, n in result.items() if n}


class P4:
    """Face-incidence CW model of the 3D permutohedron P4."""

    def __init__(self):
        parts = tuple(ordered_partitions())
        self.cells = {dimension: tuple(p for p in parts if 4 - len(p) == dimension)
                      for dimension in range(4)}
        self.vertex_sets = {p: vertices_of(p) for p in parts}
        self.vertex_by_face = {p: next(iter(self.vertex_sets[p])) for p in self.cells[0]}
        self.edges = {self._vertices(p): _edge(*self._vertices(p))
                      for p in self.cells[1]}
        self.edge_list = tuple(sorted(set(self.edges.values())))
        if len(self.edges) != 36 or len(self.edge_list) != 36:
            raise AssertionError("P4 must have 36 distinct edges")
        self.face_boundaries = {face: self._face_boundary(face)
                                for face in self.cells[2]}
        self.top_boundary = self._oriented_top_boundary()

    def _vertices(self, face):
        return tuple(sorted(self.vertex_sets[face]))

    def _face_boundary(self, face):
        vs = self.vertex_sets[face]
        inner_edges = tuple(edge for edge in self.edge_list
                            if edge[0] in vs and edge[1] in vs)
        adjacency = {v: set() for v in vs}
        for a, b in inner_edges:
            adjacency[a].add(b)
            adjacency[b].add(a)
        if any(len(neighbors) != 2 for neighbors in adjacency.values()):
            raise AssertionError("P4 polygon adjacency not degree two")
        cycle = _boundary_path(vs, adjacency)
        directed = tuple((cycle[i], cycle[(i + 1) % len(cycle)])
                         for i in range(len(cycle)))
        return {_edge(a, b): (1 if (a, b) == _edge(a, b) else -1)
                for a, b in directed}

    def _oriented_top_boundary(self):
        around = defaultdict(list)
        for face, bdry in self.face_boundaries.items():
            for edge, coefficient in bdry.items():
                around[edge].append((face, coefficient))
        if len(around) != 36 or any(len(incidences) != 2 for incidences in around.values()):
            raise AssertionError("P4 not a closed polyhedral surface")
        adjacent = defaultdict(list)
        for incidences in around.values():
            (face_a, sign_a), (face_b, sign_b) = incidences
            adjacent[face_a].append((face_b, -sign_a * sign_b))
            adjacent[face_b].append((face_a, -sign_b * sign_a))
        first = min(self.cells[2])
        oriented = {first: 1}
        queue = deque([first])
        while queue:
            face = queue.popleft()
            for other, transition in adjacent[face]:
                expected = oriented[face] * transition
                if other in oriented and oriented[other] != expected:
                    raise AssertionError("nonorientable/inconsistent P4 shell")
                if other not in oriented:
                    oriented[other] = expected
                    queue.append(other)
        if len(oriented) != 14:
            raise AssertionError("P4 boundary is disconnected")
        if add_terms((weight * coeff, edge) for face, weight in oriented.items()
                     for edge, coeff in self.face_boundaries[face].items()):
            raise AssertionError("d2 d3 != 0")
        return oriented

    def d1d2_zero(self):
        for boundary in self.face_boundaries.values():
            if add_terms((coeff * endpoint_sign, vertex)
                         for edge, coeff in boundary.items()
                         for endpoint_sign, vertex in ((-1, edge[0]), (1, edge[1]))):
                return False
        return True

    def d2d3_zero(self):
        return not add_terms((weight * coeff, edge)
                             for face, weight in self.top_boundary.items()
                             for edge, coeff in self.face_boundaries[face].items())

    def materialize(self, requested_faces=(), include_top=False):
        """Certificate-demanded faces and their boundary closure only."""
        face_set = set(requested_faces)
        if include_top:
            face_set.update(self.cells[2])
        if not face_set.issubset(self.face_boundaries):
            raise ValueError("unknown face requested")
        edges = set().union(*(set(self.face_boundaries[face]) for face in face_set)) if face_set else set()
        vertices = set().union(*(set(edge) for edge in edges)) if edges else set()
        return {"vertices": len(vertices), "edges": len(edges), "faces": len(face_set),
                "top": int(include_top)}


@dataclass(frozen=True)
class DirectionModel:
    """Consumer-only typed selection interface; rank does not set cell depth."""

    kind: str
    indices: tuple

    def __post_init__(self):
        if (self.kind, len(self.indices)) not in (("ray", 1), ("grassmann", 2)):
            raise ValueError("supported pilot direction kinds: ray/1, grassmann/2")
        if len(set(self.indices)) != len(self.indices):
            raise ValueError("duplicate direction index")

    def select(self, bundle):
        if any(type(index) is not int or index < 0 or index >= len(bundle)
               for index in self.indices):
            raise ValueError("direction index outside observed tensor bundle")
        return tuple(F.vector(bundle[i]) for i in self.indices)

    def spread(self, left, right):
        a, b = self.select(left), self.select(right)
        if self.kind == "ray":
            return F.spread(a[0], b[0])
        return rank2_spread(a, b)


def four_orthogonal_directions():
    result = []
    for axis in LABELS:
        v = [0] * 8
        v[axis], v[axis + 4] = 1, pow(2, -1, F.p)
        result.append(tuple(v))
    return tuple(result)


def admit_coherence(directions, gate):
    """Formal geometric eligibility only, not semantic rewrite authority."""
    values = tuple(F.spread(directions[i], directions[j])
                   for i, j in itertools.combinations(LABELS, 2))
    return all(v is not None and v in gate for v in values), values


def noncommuting_counterexample():
    """Same geometric gate, different state-dependent update order."""
    v = four_orthogonal_directions()[0]
    at_zero = F.scalar(0, v)
    add = lambda x: F.add(x, v)
    scale = lambda x: F.scalar(2, x)
    return scale(add(at_zero)) != add(scale(at_zero))


def run():
    poly = P4()
    if not poly.d1d2_zero() or not poly.d2d3_zero():
        raise AssertionError("P4 differential check failed")
    d = four_orthogonal_directions()
    ok, spreads = admit_coherence(d, {1})
    bad, _ = admit_coherence(d, {0})
    if not ok or bad or not noncommuting_counterexample():
        raise AssertionError("invalid gating or semantic negative control")
    model = DirectionModel("grassmann", (0, 1))
    rank_two = model.spread(d, (d[0], d[2], d[1], d[3]))
    if rank_two is None:
        raise AssertionError("unexpected null rank-two plane")
    square = next(face for face in poly.cells[2] if len(poly.vertex_sets[face]) == 4)
    report = {
        "status": "bounded-experiment", "field": "F5", "coherence_labels": 4,
        "p4_cells": {str(k): len(v) for k, v in poly.cells.items()},
        "faces": {"hexagons": sum(len(poly.vertex_sets[f]) == 6 for f in poly.cells[2]),
                  "squares": sum(len(poly.vertex_sets[f]) == 4 for f in poly.cells[2])},
        "boundary_squared_zero": True,
        "sparse_square": poly.materialize((square,)),
        "sparse_top": poly.materialize(include_top=True),
        "geometric_spreads": spreads, "gate_passes": ok,
        "negative_gate_rejects": not bad,
        "semantic_counterexample": noncommuting_counterexample(),
        "direction_models": {"ray_rank": 1, "grassmann_rank": 2,
                             "sample_grassmann_spread": rank_two},
        "scope": "exact incidence and gated direction interface, not training equivalence",
    }
    assert report["p4_cells"] == {"0": 24, "1": 36, "2": 14, "3": 1}
    assert report["faces"] == {"hexagons": 8, "squares": 6}
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
