"""Exact F5 state-dependent update audits on the established P4 route skeleton.

Non-authoritative, finite consumer experiment. Geometry-gated swaps are not
effect equalities. We certify equality at each actual prefix state, before
any subsequent suffix; all coordinates of the residual must vanish.
"""

import itertools
import json
from collections import defaultdict, deque
from dataclasses import dataclass, replace

from experiments.rt.p4_coherence_pilot import (
    F, P4, DirectionModel, four_orthogonal_directions,
)

DIRECTIONS = four_orthogonal_directions()
ORIGIN = (0,) * 8
NULL_E0 = (1,) + (0,) * 7
MODES = frozenset({"translations", "scalar_coupled", "null_defect"})


def subtract(a, b):
    return F.sub(a, b)


def apply_update(state, influence, mode):
    """A frozen translation or one of two exact state-dependent variations."""
    if mode not in MODES or influence not in range(4):
        raise ValueError("unsupported mode or influence")
    state = F.vector(state)
    if influence != 0 or mode == "translations":
        return F.add(state, DIRECTIONS[influence])
    if mode == "scalar_coupled":
        return F.add(state, F.scalar(1 + state[1], DIRECTIONS[0]))
    return F.add(F.add(state, DIRECTIONS[0]), F.scalar(state[1], NULL_E0))


def run_word(word, mode, initial=ORIGIN):
    state = F.vector(initial)
    for label in word:
        state = apply_update(state, label, mode)
    return state


def _swap_index(src, dst):
    if len(src) != 4 or len(dst) != 4 or sorted(src) != list(range(4)):
        raise ValueError("invalid permutation")
    for position in range(3):
        swapped = src[:position] + (src[position + 1], src[position]) + src[position + 2:]
        if swapped == dst:
            return position
    raise ValueError("not a single adjacent transposition")


def frame(vector, label):
    """Declared consumer frame; rank-2 adds an independent probe direction."""
    return (vector, DIRECTIONS[(label + 1) % 4])


@dataclass(frozen=True)
class SwapCertificate:
    source: tuple
    target: tuple
    position: int
    prefix: tuple
    first_a: tuple
    first_b: tuple
    after_ab: tuple
    after_ba: tuple
    before_a_direction: tuple
    after_b_a_direction: tuple
    before_b_direction: tuple
    after_a_b_direction: tuple
    spreads: tuple
    residual: tuple
    geometric_pass: bool
    effect_equal: bool
    certified: bool


def compute_swap(source, target, mode, gate, direction):
    """Compute both local orders at the actual common prefix state."""
    position = _swap_index(source, target)
    a, b = source[position:position + 2]
    prefix = run_word(source[:position], mode)
    first_a = apply_update(prefix, a, mode)
    first_b = apply_update(prefix, b, mode)
    after_ab = apply_update(first_a, b, mode)
    after_ba = apply_update(first_b, a, mode)

    before_a = subtract(first_a, prefix)
    after_b_a = subtract(after_ba, first_b)
    before_b = subtract(first_b, prefix)
    after_a_b = subtract(after_ab, first_a)
    spreads = (direction.spread(frame(before_a, a), frame(after_b_a, a)),
               direction.spread(frame(before_b, b), frame(after_a_b, b)))
    residual = subtract(after_ab, after_ba)
    geom = all(s is not None and s in gate for s in spreads)
    effect = residual == ORIGIN
    return SwapCertificate(
        source, target, position, prefix, first_a, first_b, after_ab, after_ba,
        before_a, after_b_a, before_b, after_a_b, spreads,
        residual, geom, effect, geom and effect,
    )


def verify_swap(cert, mode, gate, direction):
    """Replay in exact field arithmetic; reject altered values or wrong guards."""
    try:
        return cert == compute_swap(cert.source, cert.target, mode, gate, direction)
    except (TypeError, ValueError, IndexError):
        return False


def certificates(poly, mode, gate, direction):
    """All 36 locally anchored P4 adjacent-transposition certificates."""
    return {edge: compute_swap(edge[0], edge[1], mode, gate, direction)
            for edge in poly.edge_list}


def _components(poly, admitted):
    """Connectivity in the certified-rewrite subgraph, not all route edges."""
    neighbors = defaultdict(set)
    for a, b in admitted:
        neighbors[a].add(b)
        neighbors[b].add(a)
    remaining = set(itertools.permutations(range(4)))
    comps = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        queue = deque([seed])
        members = {seed}
        while queue:
            for nxt in neighbors[queue.popleft()]:
                if nxt in remaining:
                    remaining.remove(nxt)
                    members.add(nxt)
                    queue.append(nxt)
        comps.append(tuple(sorted(members)))
    return tuple(comps)


def audit(mode, gate, direction=None):
    """Audit geometric vs semantic swap authority, face closure and top cell."""
    if mode not in MODES:
        raise ValueError("unsupported mode")
    direction = direction or DirectionModel("ray", (0,))
    poly = P4()
    certs = certificates(poly, mode, frozenset(gate), direction)
    if any(not verify_swap(c, mode, frozenset(gate), direction) for c in certs.values()):
        raise AssertionError("swap replay mismatch")
    admitted = frozenset(edge for edge, c in certs.items() if c.certified)
    admitted_faces = frozenset(face for face, boundary in poly.face_boundaries.items()
                               if set(boundary).issubset(admitted))
    top = (len(admitted_faces) == len(poly.cells[2]) and poly.d2d3_zero())
    comps = _components(poly, admitted)

    # Local equality is sufficient for identical full-route endpoints with
    # a common deterministic suffix. Check this on the bounded specimen.
    endpoints = {p: run_word(p, mode) for p in itertools.permutations(range(4))}
    if any(endpoints[a] != endpoints[b] for a, b in admitted):
        raise AssertionError("an admitted swap changed a whole-route effect")
    if any(len({endpoints[p] for p in component}) != 1 for component in comps):
        raise AssertionError("certified component endpoints disagree")

    return {
        "field": "F5", "status": "bounded-experiment", "mode": mode,
        "direction_kind": direction.kind, "direction_rank": len(direction.indices),
        "coherence_labels": 4, "potential_edges": len(poly.edge_list),
        "geometric_edges": sum(c.geometric_pass for c in certs.values()),
        "effect_equal_edges": sum(c.effect_equal for c in certs.values()),
        "certified_edges": len(admitted),
        "blocked_effect_edges": sum(c.geometric_pass and not c.effect_equal
                                    for c in certs.values()),
        "null_nonzero_effect_residuals": sum(
            c.residual != ORIGIN and F.norm(c.residual) == 0 for c in certs.values()),
        "admitted_faces": len(admitted_faces),
        "top_3_cell": top,
        "certified_route_components": len(comps),
        "distinct_full_endpoints": len(set(endpoints.values())),
    }


def suffix_masking_negative_control():
    """A lossy suffix can conceal a failed *local* swap."""
    a, b = (0, 1, 2, 3), (1, 0, 2, 3)
    # For the first two micro-steps, the raw effects already differ.
    local_a = run_word(a[:2], "scalar_coupled")
    local_b = run_word(b[:2], "scalar_coupled")
    erase = lambda _: ORIGIN
    return local_a != local_b and erase(local_a) == erase(local_b)


def forge_negative_control():
    poly = P4()
    certs = certificates(poly, "scalar_coupled", {0}, DirectionModel("ray", (0,)))
    failed = next(c for c in certs.values() if not c.effect_equal)
    forged = replace(failed, residual=ORIGIN, effect_equal=True, certified=True)
    return not verify_swap(forged, "scalar_coupled", {0}, DirectionModel("ray", (0,)))


def run():
    additive = audit("translations", {0})
    coupled = audit("scalar_coupled", {0})
    null_residual = audit("null_defect", {0, 3})
    rank_two = audit("translations", {0}, DirectionModel("grassmann", (0, 1)))
    if not (additive["top_3_cell"] and rank_two["top_3_cell"]
            and not coupled["top_3_cell"] and not null_residual["top_3_cell"]
            and suffix_masking_negative_control() and forge_negative_control()):
        raise AssertionError("semantic/geometric distinction failed")
    return {
        "status": "bounded-experiment", "field": "F5",
        "additive": additive, "state_dependent": coupled,
        "null_residual": null_residual, "grassmann_rank_two": rank_two,
        "forged_certificate_rejected": True,
        "suffix_masking_rejected": True,
        "claim_scope": "bounded equality checks on four finite update maps only",
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
