"""Bounded P4 formal/operational coherence classification.

Reuses the established P4 face poset and state-dependent certificate verifier.
"""
from experiments.rt.state_dependent_coherence_pilot import audit
from experiments.rt.p4_coherence_pilot import P4


def run():
    p = P4()
    if not p.d1d2_zero() or not p.d2d3_zero():
        raise AssertionError("invalid formal incidence")
    frozen = audit("translations", {0})
    coupled = audit("scalar_coupled", {0})
    null_defect = audit("null_defect", {0, 3})
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
            "claim_scope": "P4 full 36 swap contexts only; no general confluence theorem"}
