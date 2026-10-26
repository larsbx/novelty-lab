"""Certificate-demanded exact P5 face boundary closure (bounded consumer pilot).

Only instantiate requested faces and their signed lower boundaries. This code
reuses the *existing* P5 incidence oracle; it is not a second math kernel.
A budget failure leaves the preexisting cache unchanged. Geometry gates do
not substitute for effect equality or independently pinned receipt replay.
"""

import json

from experiments.rt.event_stream_v1 import (
    digest, make_envelope, sample_spec, verify_envelope,
)
from experiments.rt.p5_full_coherence import (
    LABELS, N, FullP5, dimension, facets, incidence,
)


def _canonical_face(face):
    """Reject invalid partition labels, empty blocks, or ambiguous ordering."""
    if (type(face) is not tuple or not 1 <= len(face) <= N or
            any(type(b) is not tuple or not b or b != tuple(sorted(b))
                or any(type(x) is not int for x in b) for b in face)):
        raise ValueError("face must be an ordered partition with sorted blocks")
    if tuple(sorted(x for b in face for x in b)) != LABELS:
        raise ValueError("face is not a partition of 0..4")
    return face


def _edge_of(face, boundary):
    """A 1-cell has two permutation vertices, independent of their orientation."""
    if dimension(face) != 1 or len(boundary) != 2:
        raise ValueError("not an edge")
    vertices = [tuple(block[0] for block in point)
                for point in boundary]
    return tuple(sorted(vertices))


def _counts(cells):
    return tuple(sum(dimension(face) == i for face in cells) for i in range(N))


class CertificateDemandedP5:
    """On-demand boundary-closed consumer view; no full face enumeration."""

    def __init__(self):
        # Face maps to its signed immediate boundary; a vertex has {}.
        self.boundaries = {}
        self.incidence_calls = 0

    def require(self, requested, max_cells=None):
        """Atomically materialize the requested face boundary closures.

        max_cells bounds total unique cached cells **after** the request.
        It is checked before commit; failure does not change cache/counters.
        """
        if type(requested) not in (tuple, list):
            raise ValueError("requested faces must be a sequence")
        if max_cells is not None and (type(max_cells) is not int or
                                     max_cells < 0):
            raise ValueError("invalid cell budget")
        targets = tuple(_canonical_face(face) for face in requested)
        staged = {}
        calls = 0

        def visit(face):
            nonlocal calls
            if face in self.boundaries or face in staged:
                return
            if max_cells is not None and len(self.boundaries) + len(staged) >= max_cells:
                raise ValueError("P5 materialization budget exhausted")
            # Provisional insertion breaks no cycles; only staged values are mutated.
            staged[face] = {}
            lower = facets(face) if dimension(face) else ()
            signed = {}
            for child in lower:
                visit(child)
                signed[child] = incidence(face, child)
                calls += 1
            staged[face] = signed

        for face in targets:
            visit(face)
        self.boundaries.update(staged)
        self.incidence_calls += calls
        return {"counts": _counts(self.boundaries),
                "new_cells": len(staged), "new_incidence_calls": calls,
                "cached_cells": len(self.boundaries)}

    def differential_defects(self):
        """All instantiated d² compositions; none may have an unowned facet."""
        defects = {}
        for face, boundary in self.boundaries.items():
            if dimension(face) < 2:
                continue
            residue = {}
            for sub, outer in boundary.items():
                if sub not in self.boundaries:
                    raise AssertionError("incomplete cell boundary")
                for lower, inner in self.boundaries[sub].items():
                    residue[lower] = residue.get(lower, 0) + outer * inner
            nz = {key: value for key, value in residue.items() if value}
            if nz:
                defects[face] = nz
        return defects

    def validate_against(self, reference):
        """An independent eager P5 oracle must give every signed incidence."""
        if not isinstance(reference, FullP5):
            raise ValueError("expected the established full-P5 reference")
        for face, boundary in self.boundaries.items():
            expected = {} if dimension(face) == 0 else reference.boundary[face]
            if boundary != expected:
                raise AssertionError("lazy/eager oriented incidence disagreement")
        return len(self.boundaries)

    def admit(self, receipt_bytes, expected_spec_sha256, requested, max_cells=None):
        """Replay untrusted receipt first; then construct requested faces.

        Only authenticated-to-the-independent-pin *effect-equal AND
        geometry-admissible* adjacent swaps can seed higher-dimensional cells.
        A partial receipt never silently becomes a global completeness claim.
        """
        checked = verify_envelope(receipt_bytes, expected_spec_sha256)
        if checked["coherence_labels"] != N:
            raise ValueError("P5 cell witness requires five influences")
        receipt = json.loads(receipt_bytes)
        admitted_edges = {
            tuple(sorted((tuple(record["source"]), tuple(record["target"]))))
            for record in receipt["records"] if record["admitted"]
        }
        materialized = self.require(requested, max_cells=max_cells)
        permission = {}
        for face in sorted(self.boundaries, key=lambda f: (dimension(f), f)):
            d = dimension(face)
            if d == 0:
                permission[face] = True
            elif d == 1:
                permission[face] = _edge_of(face, self.boundaries[face]) in admitted_edges
            else:
                permission[face] = all(permission[child]
                                       for child in self.boundaries[face])
        requested_targets = tuple(_canonical_face(face) for face in requested)
        top = (LABELS,)
        return {
            **materialized,
            "admitted_counts": tuple(
                sum(permission[f] for f in self.boundaries if dimension(f) == d)
                for d in range(N)),
            "requested_admitted": all(permission[target]
                                     for target in requested_targets),
            "P5_top_materialized": top in self.boundaries,
            "P5_top_admitted": top in self.boundaries and permission[top],
            "receipt_scope": checked["scope"],
            "replayed_edges": checked["audited_edges"],
            "semantic_effect_failures": checked["blocked_effect_edges"],
        }


def specimen():
    """Small deterministic sample comparing actual lazy closure vs full P5."""
    reference = FullP5()
    lazy = CertificateDemandedP5()
    square = next(f for f in reference.cells[2]
                  if len(reference.boundary[f]) == 4)
    prism = next(f for f in reference.cells[3]
                 if len(reference.boundary[f]) == 8)
    first = lazy.require((square,), max_cells=12)
    if first["counts"] != (4, 4, 1, 0, 0):
        raise AssertionError("square materialized unrelated faces")
    lazy.validate_against(reference)
    before = (len(lazy.boundaries), lazy.incidence_calls)
    try:
        lazy.require((prism,), max_cells=12)
    except ValueError:
        pass
    else:
        raise AssertionError("tight budget admitted a prism")
    if before != (len(lazy.boundaries), lazy.incidence_calls):
        raise AssertionError("failed request mutated cache")
    prism_result = lazy.require((prism,))
    lazy.validate_against(reference)
    if lazy.differential_defects():
        raise AssertionError("differential squared on sparse closure")
    top = (LABELS,)
    additive = sample_spec(5, "translations", 1)
    accepted = lazy.admit(make_envelope(additive), digest(additive), (top,))
    if accepted["counts"] != (120, 240, 150, 30, 1) or not accepted["P5_top_admitted"]:
        raise AssertionError("complete frozen additive certificate rejected")
    lazy.validate_against(reference)
    coupled = sample_spec(5, "coupled", 1)
    blocked = CertificateDemandedP5().admit(
        make_envelope(coupled), digest(coupled), (top,))
    if blocked["P5_top_admitted"] or blocked["semantic_effect_failures"] != 24:
        raise AssertionError("effect-negative P5 top incorrectly admitted")
    return {
        "status": "bounded-experiment", "field": "F5", "coherence_labels": 5,
        "first_square": first, "prism_after_square": prism_result,
        "budget_failure_atomic": True,
        "lazy_exact_matches_eager": True,
        "top_frozen": {k: accepted[k] for k in
                       ("counts", "P5_top_admitted", "replayed_edges")},
        "top_state_dependent": {k: blocked[k] for k in
                                ("P5_top_admitted", "semantic_effect_failures")},
        "reference_cells": sum(len(c) for c in reference.cells.values()),
        "scope": "finite on-demand P5 boundary closure, not an asymptotic speed theorem",
    }


if __name__ == "__main__":
    print(json.dumps(specimen(), sort_keys=True))
