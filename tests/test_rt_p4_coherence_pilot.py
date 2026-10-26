"""P4 (24,36,14,1) chain boundaries, sparse closure, and guarded F5 tensor directions.

Verifies a bounded exact polyhedral-conformance experiment, not a universal
training-update equivalence or novel theorem.
"""

import unittest

from experiments.rt.p4_coherence_pilot import (
    P4, DirectionModel, F, admit_coherence, four_orthogonal_directions,
    noncommuting_counterexample, run, add_terms,
)

GUARDS_CONTRACT = "P4 permutation coherence lift, exact F5 rank-one/rank-two direction interface and semantic negative controls"


class P4CoherencePilotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poly = P4()
        cls.dirs = four_orthogonal_directions()

    def test_full_face_incidence_and_chain_squared(self):
        self.assertEqual({k: len(v) for k,v in self.poly.cells.items()},
                         {0: 24, 1: 36, 2: 14, 3: 1})
        self.assertEqual(sum(len(self.poly.vertex_sets[f]) == 6 for f in self.poly.cells[2]), 8)
        self.assertEqual(sum(len(self.poly.vertex_sets[f]) == 4 for f in self.poly.cells[2]), 6)
        self.assertTrue(self.poly.d1d2_zero())
        self.assertTrue(self.poly.d2d3_zero())
        self.assertEqual(len(self.poly.top_boundary), 14)
        self.assertEqual(24 - 36 + 14, 2)  # Euler characteristic of P4 boundary

    def test_corrupt_orientation_fails(self):
        corrupt = dict(self.poly.top_boundary)
        key = next(iter(corrupt))
        corrupt[key] = -corrupt[key]
        unbalanced = add_terms((weight * coefficient, edge)
                               for face, weight in corrupt.items()
                               for edge, coefficient in self.poly.face_boundaries[face].items())
        self.assertTrue(unbalanced)

    def test_sparse_materialization_only_instantiates_boundary_closure(self):
        face = next(f for f in self.poly.cells[2] if len(self.poly.vertex_sets[f]) == 4)
        self.assertEqual(self.poly.materialize((face,)),
                         {"vertices": 4, "edges": 4, "faces": 1, "top": 0})
        self.assertEqual(self.poly.materialize(include_top=True),
                         {"vertices": 24, "edges": 36, "faces": 14, "top": 1})
        self.assertEqual(self.poly.materialize(),
                         {"vertices": 0, "edges": 0, "faces": 0, "top": 0})
        with self.assertRaises(ValueError):
            self.poly.materialize(((0, 1, 2, 3),))

    def test_geometric_gate_is_not_semantic_equivalence(self):
        ok, spreads = admit_coherence(self.dirs, {1})
        self.assertTrue(ok)
        self.assertEqual(spreads, (1,) * 6)
        self.assertFalse(admit_coherence(self.dirs, {0})[0])
        self.assertIsNone(F.spread((0,) * 8, self.dirs[0]))
        self.assertTrue(noncommuting_counterexample())

    def test_tensor_direction_rank_independent_of_coherence_labels(self):
        vector = DirectionModel("ray", (0,))
        self.assertEqual(vector.spread(self.dirs, self.dirs), 0)
        rank2 = DirectionModel("grassmann", (0, 1))
        pair = (self.dirs[0], self.dirs[2], self.dirs[1], self.dirs[3])
        self.assertEqual(rank2.spread(self.dirs, pair), 1)
        self.assertEqual(rank2.spread(self.dirs, self.dirs), 0)
        self.assertIsNone(rank2.spread((self.dirs[0], self.dirs[0]), self.dirs))
        with self.assertRaises(ValueError):
            DirectionModel("grassmann", (0, 0))
        with self.assertRaises(ValueError):
            DirectionModel("grassmann", (0,))
        with self.assertRaises(ValueError):
            DirectionModel("ray", (7,)).select(self.dirs)

    def test_report_is_bounded(self):
        r = run()
        self.assertEqual(r["p4_cells"], {"0": 24, "1": 36, "2": 14, "3": 1})
        self.assertTrue(r["semantic_counterexample"])
        self.assertEqual(r["status"], "bounded-experiment")


if __name__ == "__main__":
    unittest.main()
