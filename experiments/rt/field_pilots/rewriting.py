"""Bounded P4 formal/operational coherence classification.

Reuses the established P4 face poset and state-dependent certificate verifier.
"""
from experiments.rt.state_dependent_coherence_pilot import audit
from experiments.rt.p4_coherence_pilot import P4, F, four_orthogonal_directions


def prefix_stability_counterexample():
    """Two state-dependent swaps agree at one prefix but not another.

    Same non-null transported rays at both prefixes are not a context-free
    independence relation. All arithmetic is F5 and uses the existing oracle.
    """
    d0, d1 = four_orthogonal_directions()[:2]
    origin = (0,) * 8
    shifted = F.scalar(2, d1)

    def a(state):
        return F.add(state, F.scalar(2 + state[1] * state[1], d0))

    def b(state):
        return F.add(state, d1)

    def details(state):
        after_ab = b(a(state))
        after_ba = a(b(state))
        before_dir = F.sub(a(state), state)
        after_dir = F.sub(a(b(state)), b(state))
        spread = F.spread(before_dir, after_dir)
        return {"equal": after_ab == after_ba,
                "residual": F.sub(after_ab, after_ba), "spread": spread,
                "directions_nonnul": F.norm(before_dir) != 0 and F.norm(after_dir) != 0}

    at_origin, at_shifted = details(origin), details(shifted)
    if (at_origin["equal"] or not at_shifted["equal"]
            or at_origin["spread"] != 0 or at_shifted["spread"] != 0
            or not at_origin["directions_nonnul"]
            or not at_shifted["directions_nonnul"]):
        raise AssertionError("prefix-conditioned independence witness failed")
    return {"base": at_origin, "shifted": at_shifted,
            "scope": "two declared F5 prefixes; no general independence theorem"}


def run():
    p = P4()
    if not p.d1d2_zero() or not p.d2d3_zero():
        raise AssertionError("invalid formal incidence")
    frozen = audit("translations", {0})
    coupled = audit("scalar_coupled", {0})
    null_defect = audit("null_defect", {0, 3})
    prefix_dependent = prefix_stability_counterexample()
    if not (frozen["certified_edges"] == 36
            and coupled["geometric_edges"] == 36
            and coupled["certified_edges"] == 30
            and null_defect["null_nonzero_effect_residuals"] == 6
            and frozen["top_3_cell"] and not coupled["top_3_cell"]):
        raise AssertionError("semantic versus formal control failed")
    return {"discipline": "theoretical-computer-science", "status": "bounded-experiment",
            "field": "F5", "route_vertices": len(p.cells[0]),
            "formal_edges": len(p.cells[1]), "formal_faces": len(p.cells[2]),
            "frozen": frozen, "state_dependent": coupled, "null_defect": null_defect,
            "prefix_dependent": prefix_dependent,
            "claim_scope": "P4 full 36 swap contexts only; no general confluence theorem"}
