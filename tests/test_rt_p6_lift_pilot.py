"""Finite six-influence RT route lift: exact P6 incidence, effect and homology.

Guards a bounded, consumer-specific combinatorial and F5 conformance experiment.
No neural-network training or general rank-R theorem is inferred from checks.
"""

import unittest

from experiments.rt.p5_full_coherence import FullP5
from experiments.rt.p6_lift_pilot import (
    LABELS, DemandP6, expected_fvector, cube_fvector, audit_updates,
    experiment, directions, incidence,
)
from experiments.rt.rank_lift_pilot import F
from experiments.rt.event_stream_v1 import sample_spec

GUARDS_CONTRACT = "Demand-driven P6 signed cellular incidence, exact F5 effect equality and subcomplex homology"


class P6LiftTest(unittest.TestCase):
    TOP = (LABELS,)
    SQUARE = ((0, 1), (2, 3), (4,), (5,))
    HEXAGON = ((0, 1, 2), (3,), (4,), (5,))
    P5_FACET = ((0, 1, 2, 3, 4), (5,))

    def test_stirling_face_count_and_cube_difference(self):
        self.assertEqual(expected_fvector(), (720, 1800, 1560, 540, 62, 1))
        self.assertEqual(sum(expected_fvector()), 4683)
        self.assertEqual(cube_fvector(), (64, 192, 240, 160, 60, 12, 1))
        self.assertEqual(sum((-1) ** k * count
                             for k, count in enumerate(expected_fvector())), 1)

    def test_just_one_square_or_hexagon_is_demanded(self):
        for requested, expected in (
                (self.SQUARE, (4, 4, 1, 0, 0, 0)),
                (self.HEXAGON, (6, 6, 1, 0, 0, 0))):
            with self.subTest(requested=requested):
                p = DemandP6()
                report = p.request((requested,))
                self.assertEqual(report["cells_by_dimension"], expected)
                self.assertEqual(report["new_cells"], sum(expected))
                self.assertFalse(p.chain_defects())
                again = p.request((requested,))
                self.assertEqual(again["new_cells"], 0)
                self.assertEqual(again["new_incidence_calls"], 0)

    def test_failed_budget_atomic_and_malformed_faces(self):
        p = DemandP6()
        p.request((self.SQUARE,), max_cells=9)
        old = (dict(p.boundaries), p.incidence_calls)
        with self.assertRaises(ValueError):
            p.request((self.HEXAGON,), max_cells=9)
        self.assertEqual((p.boundaries, p.incidence_calls), old)
        for value in (True, -1):
            with self.assertRaises(ValueError):
                p.request((self.HEXAGON,), max_cells=value)
        for bad in (((0, 1, 2, 3, 4, 5), (0,)),
                    ((1, 0), (2,), (3,), (4,), (5,)),
                    ((0,), (1,), (2,), (3,), (5,))):
            with self.assertRaises(ValueError):
                p.request((bad,))
        self.assertEqual((p.boundaries, p.incidence_calls), old)

    def test_full_p5_facet_matches_existing_reference(self):
        p = DemandP6()
        report = p.request((self.P5_FACET,))
        self.assertEqual(report["cells_by_dimension"],
                         (120, 240, 150, 30, 1, 0))
        self.assertEqual(p.compare_p5_facet(), 541)
        self.assertFalse(p.chain_defects())

    def test_full_top_and_every_integer_boundary_squared(self):
        p = DemandP6()
        r = p.request((self.TOP,))
        self.assertEqual(r["cells_by_dimension"], expected_fvector())
        self.assertEqual(r["new_cells"], 4683)
        self.assertFalse(p.chain_defects())
        self.assertEqual(len(p.boundaries[self.TOP]), 62)
        self.assertEqual(p.request((self.TOP,))["new_cells"], 0)

    def test_mutated_incidence_breaks_chain(self):
        p = DemandP6()
        p.request((self.TOP,))
        child = next(iter(p.boundaries[self.TOP]))
        original = p.boundaries[self.TOP][child]
        p.boundaries[self.TOP][child] = -original
        self.assertIn(self.TOP, p.chain_defects())

    def test_full_geometric_pass_can_fail_whole_vector_effect(self):
        for mode, expected in (("translations", 1800),
                               ("scalar_coupled", 1680),
                               ("null_defect", 1680)):
            with self.subTest(mode=mode):
                report, accepted = audit_updates(mode)
                self.assertEqual(report["potential_swaps"], 1800)
                self.assertEqual(report["geometric_passes"], 1800)
                self.assertEqual(report["effect_equal"], expected)
                self.assertEqual(len(accepted), expected)
                self.assertEqual(report["nonzero_null_residuals"],
                                 120 if mode == "null_defect" else 0)
                self.assertEqual(report["effect_rejected"], 1800 - expected)

    def test_admitted_complex_ranks_and_betti(self):
        p = DemandP6()
        p.request((self.TOP,))
        for mode, counts, ranks, betti in (
            ("translations", (720, 1800, 1560, 540, 62, 1),
             (719, 1081, 479, 61, 1), (1, 0, 0, 0, 0, 0)),
            ("scalar_coupled", (720, 1680, 1320, 390, 32, 0),
             (718, 962, 358, 32, 0), (2, 0, 0, 0, 0, 0)),
            ("null_defect", (720, 1680, 1320, 390, 32, 0),
             (718, 962, 358, 32, 0), (2, 0, 0, 0, 0, 0))):
            with self.subTest(mode=mode):
                _, edges = audit_updates(mode)
                result = p.admitted_profile(edges)
                self.assertEqual(result["admitted_cells"], counts)
                self.assertEqual(result["boundary_ranks_F5"], ranks)
                self.assertEqual(result["betti_F5"], betti)

    def test_grassmann_rank_independent_of_permutation_rank(self):
        rank1, _ = audit_updates("translations", 1)
        rank2, _ = audit_updates("translations", 2)
        self.assertEqual(rank1["certified_swaps"], 1800)
        self.assertEqual(rank2["certified_swaps"], 1800)
        self.assertEqual(rank2["direction_rank"], 2)
        self.assertEqual(len(directions()), 6)
        self.assertTrue(all(F.norm(v) != 0 for v in directions()))

    def test_existing_wire_protocol_does_not_accept_six_updates(self):
        with self.assertRaises(ValueError):
            sample_spec(6)

    def test_complete_experiment_summary(self):
        report = experiment()
        self.assertEqual(report["full_P6_fvector"],
                         (720, 1800, 1560, 540, 62, 1))
        self.assertEqual(report["P5_facet_signed_cross_checks"], 541)
        self.assertEqual(report["modes"]["scalar_coupled"]["admitted_cells"],
                         (720, 1680, 1320, 390, 32, 0))
        self.assertTrue(report["budget_failure_atomic"])


if __name__ == "__main__":
    unittest.main()
