"""Bounded field-pilot conformance: independent exact negative controls.

The seven fixtures are separate finite experiments, not a general mathematical
proof, authenticated execution trace, or real model-training comparison.
"""
import unittest

from experiments.rt.field_pilots import (
    mathematics, rewriting, topology, systems, stochastic, machine_learning, bridges,
)
from experiments.rt.field_pilots.__main__ import run as run_all

GUARDS_CONTRACT = (
    "Seven field-scoped RT pilot fixtures: guarded Gram, P4 operational swaps, "
    "cylinder classes, trusted replay, rational schedules, optimizer order, and "
    "nonfaithful finite-field projection"
)


class TestFieldSeparatedRTPilots(unittest.TestCase):
    def test_mathematics_defect_does_not_decide_planarity(self):
        out = mathematics.run()
        self.assertEqual(out["fixtures"], 3)
        self.assertEqual(out["orthogonal_nonplanar"]["defect"], 4)
        self.assertEqual(out["nonplanar_zero_defect"]["defect"], 0)
        self.assertNotEqual(out["nonplanar_zero_defect"]["gram3"], 0)
        with self.assertRaises(ValueError):
            mathematics.triple(mathematics.axis(0), mathematics.unit(1),
                               mathematics.unit(2))

    def test_theoretical_cs_geometry_does_not_authorize_swap(self):
        out = rewriting.run()
        self.assertEqual(out["formal_edges"], 36)
        self.assertEqual(out["frozen"]["certified_edges"], 36)
        self.assertEqual(out["state_dependent"]["certified_edges"], 30)
        self.assertEqual(out["state_dependent"]["blocked_effect_edges"], 6)
        self.assertFalse(out["state_dependent"]["top_3_cell"])
        self.assertFalse(out["prefix_dependent"]["base"]["equal"])
        self.assertTrue(out["prefix_dependent"]["shifted"]["equal"])
        self.assertEqual(out["prefix_dependent"]["base"]["spread"], 0)
        self.assertEqual(out["prefix_dependent"]["shifted"]["spread"], 0)

    def test_topology_witness_hit_is_not_class_elimination(self):
        out = topology.run()
        self.assertTrue(out["top_minus_bottom_boundary"])
        self.assertTrue(out["homologous_bottom_still_survives"])
        self.assertFalse(topology.is_boundary(topology.TOP))
        self.assertTrue(topology.is_boundary(
            tuple((a-b) % 5 for a,b in zip(topology.TOP, topology.BOTTOM))))
        with self.assertRaises(ValueError):
            topology.is_boundary((1,))

    def test_systems_reject_forged_receipt_even_if_hash_recalculated(self):
        out = systems.run()
        self.assertTrue(out["genuine_replayed"])
        self.assertTrue(out["forged_rejected"])
        self.assertTrue(out["incomplete_trace_rejected"])
        self.assertTrue(out["forged_can_recompute_untrusted_digest"])
        self.assertTrue(out["independently_pinned_digest_mismatch"])

    def test_probability_locally_equal_versus_unequal_paths(self):
        out = stochastic.run()
        self.assertTrue(out["balanced"])
        self.assertTrue(out["biased"])
        self.assertEqual(out["biased_path_weights"], ("3/8", "1/8"))
        self.assertEqual(out["other_probability_mass"], "1/2")
        with self.assertRaises(ValueError):
            stochastic.weights(stochastic.Q(1,2), stochastic.Q(2), stochastic.Q(1,2))

    def test_machine_learning_full_optimizer_state_matters(self):
        out = machine_learning.run()
        self.assertEqual((out["sgd_loss_ab"], out["sgd_loss_ba"]), ("2", "5/2"))
        self.assertTrue(out["momentum_same_weight"])
        self.assertTrue(out["momentum_distinct_full_state"])
        self.assertTrue(out["third_step_divergence"])

    def test_bridge_f5_equality_does_not_lift(self):
        out = bridges.run()
        self.assertEqual(out["nonzero_integer_defect"], 5)
        self.assertTrue(out["field_effect_equal"])
        self.assertFalse(out["integer_effect_equal"])

    def test_aggregate_is_deterministic_and_separate(self):
        a, b = run_all(), run_all()
        self.assertEqual(a, b)
        self.assertEqual(a["pilot_count"], 7)
        self.assertEqual(len({v["discipline"] for v in a["experiments"]}), 7)
        self.assertTrue(all("scope" in v or "claim_scope" in v
                            for v in a["experiments"]))


if __name__ == "__main__":
    unittest.main()
