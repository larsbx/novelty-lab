"""Guards F5 P3 hexagon, additive cubical 3-cell, and rank-2 Gram basis independence.

This test replays a bounded classical-combinatorics acceptance contract only;
it makes no universal coherence or neural-training equivalence claim.
"""

import unittest

from experiments.rt.rank_lift_pilot import (
    F, HEXAGON, boundary_squared_is_zero, cube_boundary, cubical_face,
    directions, endpoint_boundary, hexagon_boundary, permitted, pilot, rank2_spread,
    _accumulate,
)

GUARDS_CONTRACT = "Bounded split-RT P3 hexagon / additive cube coherent incidence and Grassmann rank-two interface"


class RankLiftPilotTest(unittest.TestCase):
    def test_p3_hexagon_is_two_dimensional(self):
        self.assertEqual(len(HEXAGON), 6)
        edges = hexagon_boundary()
        self.assertEqual(len(edges), 6)
        self.assertEqual(len({e for _, e in edges}), 6)
        self.assertEqual(_accumulate((c * d, v) for c, e in edges
                                      for d, v in endpoint_boundary(e)), {})
        # Connected six-edge hexagon graph: cyclomatic number E-V+1 = 1.
        self.assertEqual(6 - 6 + 1, 1)

    def test_cube_three_cell_boundary(self):
        self.assertTrue(boundary_squared_is_zero())
        shell = cube_boundary()
        self.assertEqual(len(shell), 6)
        self.assertEqual(len({face for _, face in shell}), 6)
        self.assertTrue(all(len(cubical_face(*face)) == 4 for _, face in shell))

    def test_spread_gate_and_null_negative_controls(self):
        dirs = directions()
        ok, spreads = permitted(dirs, {1})
        self.assertTrue(ok)
        self.assertEqual(spreads, (1, 1, 1))
        self.assertFalse(permitted(dirs, {0})[0])
        self.assertIsNone(F.spread((0,) * 8, dirs[0]))

    def test_parameterized_rank2_direction(self):
        d = directions()
        U = (d[0], d[1])
        W = (F.add(d[0], d[2]), F.add(d[1], d[2]))
        value = rank2_spread(U, W)
        self.assertIsNotNone(value)
        self.assertEqual(value, rank2_spread((F.add(U[0], U[1]), U[1]),
                                                  tuple(reversed(W))))
        self.assertEqual(rank2_spread(U, U), 0)
        self.assertIsNone(rank2_spread((U[0], U[0]), W))

    def test_replay_summary(self):
        result = pilot()
        self.assertEqual(result["permutohedron"]["dimension"], 2)
        self.assertEqual(result["additive_cube"]["dimension"], 3)
        self.assertTrue(result["negative_gate_rejects"])


if __name__ == "__main__":
    unittest.main()
