"""Contract tests: exact local swap effects vs geometric RT eligibility on P4.

These assertions replay finite F5 certificates. They do not prove general
training equivalence, global confluence, or novel algebraic topology.
"""

from dataclasses import replace
import unittest

from experiments.rt.p4_coherence_pilot import P4, DirectionModel, F
from experiments.rt.state_dependent_coherence_pilot import (
    ORIGIN, audit, certificates, compute_swap, forge_negative_control,
    run, suffix_masking_negative_control, verify_swap,
)

GUARDS_CONTRACT = "State-dependent P4 adjacent-swap effect equality with guarded RT directions and top-face closure"


class StateDependentCoherenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poly = P4()
        cls.ray = DirectionModel("ray", (0,))

    def test_frozen_translations_admit_full_p4(self):
        result = audit("translations", {0})
        self.assertEqual(result["potential_edges"], 36)
        self.assertEqual(result["geometric_edges"], 36)
        self.assertEqual(result["effect_equal_edges"], 36)
        self.assertEqual(result["certified_edges"], 36)
        self.assertEqual(result["admitted_faces"], 14)
        self.assertTrue(result["top_3_cell"])
        self.assertEqual(result["certified_route_components"], 1)
        self.assertEqual(result["distinct_full_endpoints"], 1)

    def test_state_dependent_geometric_false_positive(self):
        result = audit("scalar_coupled", {0})
        self.assertEqual(result["geometric_edges"], 36)
        self.assertEqual(result["effect_equal_edges"], 30)
        self.assertEqual(result["blocked_effect_edges"], 6)
        self.assertEqual(result["certified_edges"], 30)
        self.assertLess(result["admitted_faces"], 14)
        self.assertFalse(result["top_3_cell"])
        self.assertEqual(result["certified_route_components"], 2)
        self.assertEqual(result["distinct_full_endpoints"], 2)

    def test_null_nonzero_residual_never_counts_as_equality(self):
        result = audit("null_defect", {0, 3})
        self.assertEqual(result["geometric_edges"], 36)
        self.assertEqual(result["effect_equal_edges"], 30)
        self.assertEqual(result["null_nonzero_effect_residuals"], 6)
        self.assertFalse(result["top_3_cell"])
        mismatch = next(c for c in certificates(
            self.poly, "null_defect", {0, 3}, self.ray).values()
                        if c.residual != ORIGIN)
        self.assertEqual(F.norm(mismatch.residual), 0)
        self.assertFalse(mismatch.effect_equal)

    def test_certificate_exact_replay_and_tamper_rejection(self):
        certs = certificates(self.poly, "scalar_coupled", {0}, self.ray)
        self.assertEqual(len(certs), 36)
        self.assertTrue(all(verify_swap(c, "scalar_coupled", {0}, self.ray)
                            for c in certs.values()))
        mismatch = next(c for c in certs.values() if not c.effect_equal)
        forged = replace(mismatch, residual=ORIGIN, effect_equal=True, certified=True)
        self.assertFalse(verify_swap(forged, "scalar_coupled", {0}, self.ray))
        self.assertFalse(verify_swap(mismatch, "translations", {0}, self.ray))
        self.assertTrue(forge_negative_control())

    def test_suffix_masking_does_not_certify_local_swap(self):
        self.assertTrue(suffix_masking_negative_control())

    def test_tensor_direction_rank_is_independent(self):
        vector = audit("translations", {0}, self.ray)
        plane = audit("translations", {0}, DirectionModel("grassmann", (0, 1)))
        self.assertEqual(vector["certified_edges"], plane["certified_edges"])
        self.assertTrue(vector["top_3_cell"] and plane["top_3_cell"])
        self.assertEqual(plane["direction_rank"], 2)
        self.assertEqual(plane["coherence_labels"], 4)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            audit("unsupported", {0})
        with self.assertRaises(ValueError):
            compute_swap((0,1,2,3),(2,1,0,3),"translations",{0},self.ray)

    def test_driver_bounded_summary(self):
        report = run()
        self.assertEqual(report["status"], "bounded-experiment")
        self.assertEqual(report["state_dependent"]["blocked_effect_edges"], 6)
        self.assertTrue(report["forged_certificate_rejected"])


if __name__ == "__main__":
    unittest.main()
