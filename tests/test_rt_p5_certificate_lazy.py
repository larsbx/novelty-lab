"""Genuine certificate-demanded P5 closure, exact incidence and atomic budget.

Test asserts agreement with separately constructed eager reference and
independently pinned receipt replay. No mathematical novelty or LLM claims.
"""

import unittest

from experiments.rt.event_stream_v1 import (
    all_edges, digest, make_envelope, sample_spec,
)
from experiments.rt.p5_full_coherence import FullP5
from experiments.rt.p5_certificate_lazy import (
    CertificateDemandedP5, specimen,
)

GUARDS_CONTRACT = "P5 on-demand complete signed boundaries, fail-closed materialization and effect-certified admission"


class P5CertificateLazyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eager = FullP5()
        cls.square = next(f for f in cls.eager.cells[2]
                          if len(cls.eager.boundary[f]) == 4)
        cls.hexagon = next(f for f in cls.eager.cells[2]
                           if len(cls.eager.boundary[f]) == 6)
        cls.facet = next(f for f in cls.eager.cells[3]
                         if len(cls.eager.boundary[f]) == 14)
        cls.prism = next(f for f in cls.eager.cells[3]
                         if len(cls.eager.boundary[f]) == 8)
        cls.top = ((0, 1, 2, 3, 4),)

    def test_square_and_hexagon_only_touch_boundary_closure(self):
        for cell, expected in ((self.square, (4,4,1,0,0)),
                               (self.hexagon, (6,6,1,0,0)),
                               (self.facet, (24,36,14,1,0)),
                               (self.prism, (12,18,8,1,0))):
            with self.subTest(face=cell):
                lazy = CertificateDemandedP5()
                result = lazy.require((cell,))
                self.assertEqual(result["counts"], expected)
                self.assertEqual(result["new_cells"], sum(expected))
                self.assertEqual(lazy.validate_against(self.eager), sum(expected))
                self.assertEqual(lazy.differential_defects(), {})
                self.assertLess(sum(expected), 541)

    def test_repeated_request_uses_cache_and_does_not_recompute(self):
        lazy = CertificateDemandedP5()
        once = lazy.require((self.hexagon,))
        original_calls = lazy.incidence_calls
        again = lazy.require((self.hexagon,))
        self.assertEqual(once["counts"], again["counts"])
        self.assertEqual(again["new_cells"], 0)
        self.assertEqual(again["new_incidence_calls"], 0)
        self.assertEqual(lazy.incidence_calls, original_calls)

    def test_exhausted_budget_is_atomic(self):
        lazy = CertificateDemandedP5()
        lazy.require((self.square,), max_cells=9)
        old = (dict(lazy.boundaries), lazy.incidence_calls)
        with self.assertRaisesRegex(ValueError, "budget"):
            lazy.require((self.prism,), max_cells=12)
        self.assertEqual((lazy.boundaries, lazy.incidence_calls), old)
        with self.assertRaises(ValueError):
            lazy.require((self.hexagon,), max_cells=True)

    def test_unknown_or_malformed_faces_fail_closed(self):
        lazy = CertificateDemandedP5()
        for face in (((0,1,2,3,4), (0,)),
                     ((1,0), (2,), (3,), (4,)),
                     ((0,), (1,), (2,), (4,))):
            with self.subTest(face=face), self.assertRaises(ValueError):
                lazy.require((face,))
        self.assertEqual(lazy.boundaries, {})

    def test_full_top_equal_to_eager_reference(self):
        lazy = CertificateDemandedP5()
        result = lazy.require((self.top,))
        self.assertEqual(result["counts"], (120,240,150,30,1))
        self.assertEqual(result["new_cells"], 541)
        self.assertEqual(lazy.differential_defects(), {})
        self.assertEqual(lazy.validate_against(self.eager), 541)

    def test_independent_pin_and_effect_control_for_top(self):
        for mode, expected in (("translations", True),
                               ("coupled", False),
                               ("null_defect", False)):
            spec = sample_spec(5, mode)
            lazy = CertificateDemandedP5()
            result = lazy.admit(make_envelope(spec), digest(spec), (self.top,))
            self.assertEqual(result["P5_top_admitted"], expected)
            self.assertEqual(result["replayed_edges"], 240)
            self.assertEqual(result["semantic_effect_failures"],
                             0 if expected else 24)
        spec = sample_spec(5)
        with self.assertRaisesRegex(ValueError, "untrusted program"):
            CertificateDemandedP5().admit(make_envelope(spec), "0"*64, (self.top,))

    def test_single_face_receipt_admits_only_local_closure(self):
        from experiments.rt.p5_certificate_lazy import _edge_of
        spec = sample_spec(5, "translations")
        probe = CertificateDemandedP5()
        probe.require((self.square,))
        pairs = sorted(_edge_of(face, boundary)
                       for face, boundary in probe.boundaries.items()
                       if len(face) == 4)
        self.assertEqual(len(pairs), 4)
        requests = [[list(a), list(b)] for a, b in pairs]
        lazy = CertificateDemandedP5()
        result = lazy.admit(make_envelope(spec, requests),
                            digest(spec), (self.square,))
        self.assertTrue(result["requested_admitted"])
        self.assertEqual(result["admitted_counts"], (4, 4, 1, 0, 0))
        self.assertEqual(result["replayed_edges"], 4)
        self.assertFalse(result["P5_top_admitted"])

    def test_partial_evidence_cannot_promote_entire_top(self):
        spec = sample_spec(5, "translations")
        edges = [[list(a), list(b)] for a, b in all_edges(5)[:2]]
        partial = CertificateDemandedP5().admit(
            make_envelope(spec, edges), digest(spec), (self.top,))
        self.assertEqual(partial["receipt_scope"], "requested-only")
        self.assertEqual(partial["replayed_edges"], 2)
        self.assertFalse(partial["P5_top_admitted"])

    def test_sample_finite_replay(self):
        report = specimen()
        self.assertEqual(report["first_square"]["new_cells"], 9)
        self.assertTrue(report["budget_failure_atomic"])
        self.assertTrue(report["top_frozen"]["P5_top_admitted"])
        self.assertFalse(report["top_state_dependent"]["P5_top_admitted"])


if __name__ == "__main__":
    unittest.main()
