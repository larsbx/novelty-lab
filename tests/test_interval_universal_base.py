"""Exact finite-order base-lemma controls for the universal interval theorem.

These are independent bounded regressions, not a proof of an unbounded theorem.
Every interval is closed; repeated intervals/vertices retain distinct labels.
"""
GUARDS_CONTRACT = "point–interval lopsided bound, endpoint doubling and interval-induction arithmetic"

from itertools import combinations, product
from math import prod
import unittest


INTERVALS = tuple((a, b) for a in range(3) for b in range(a, 3))
POSITIONS = tuple(range(3))


def contains(interval, value):
    return interval[0] <= value <= interval[1]


def intersects(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def contains_kst(edges, m, n, s, t):
    if m < s or n < t:
        return False
    return any(
        all((i, j) in edges for i in aa for j in bb)
        for aa in combinations(range(m), s)
        for bb in combinations(range(n), t)
    )


def sigma(sizes):
    return sum(prod(n for j, n in enumerate(sizes) if j != i)
               for i in range(len(sizes)))


class TestIntervalUniversalBase(unittest.TestCase):

    def test_point_interval_lopsided_with_ties(self):
        """All point configurations (incl. ties), interval labels, s/t up to 3."""
        count = 0
        for m in range(1, 4):
            for n in range(1, 3):
                for point_labels in product(POSITIONS, repeat=m):
                    for intervals in product(INTERVALS, repeat=n):
                        edges = {
                            (i, j)
                            for i, x in enumerate(point_labels)
                            for j, I in enumerate(intervals)
                            if contains(I, x)
                        }
                        for s in range(1, 4):
                            for t in range(1, 4):
                                if not contains_kst(edges, m, n, s, t):
                                    self.assertLessEqual(
                                        len(edges), m * (t-1) + 3*n*(s-1),
                                        (point_labels, intervals, s, t))
                        count += 1
        self.assertGreater(count, 1000)

    def test_interval_endpoint_double_count(self):
        """Every intersecting labelled pair has two tagged endpoint witnesses."""
        for aa in product(INTERVALS, repeat=2):
            for bb in product(INTERVALS, repeat=2):
                edges = {(i, j) for i, A in enumerate(aa)
                         for j, B in enumerate(bb) if intersects(A, B)}
                ga = sum(contains(B, endpoint)
                         for A in aa for endpoint in A for B in bb)
                gb = sum(contains(A, endpoint)
                         for B in bb for endpoint in B for A in aa)
                self.assertGreaterEqual(ga + gb, 2 * len(edges))

    def test_interval_interval_kst_bound(self):
        """Endpoint-lifted base lemma for all 2x2 labelled interval choices."""
        for aa in product(INTERVALS, repeat=2):
            for bb in product(INTERVALS, repeat=2):
                edges = {(i, j) for i, A in enumerate(aa)
                         for j, B in enumerate(bb) if intersects(A, B)}
                for s in (1, 2, 3):
                    for t in (1, 2, 3):
                        if not contains_kst(edges, 2, 2, s, t):
                            self.assertLessEqual(len(edges),
                                                 4*(2*(t-1)+2*(s-1)))

    def test_induction_threshold_monotonicity(self):
        """The exact r-1 threshold dominates every restricted part-size tuple."""
        for r in (3, 4, 5):
            for t in (2, 3):
                for sizes in product(range(1, 4), repeat=r):
                    prefix = sizes[:-1]
                    threshold = 4**(r-2)*(t-1)*sigma(prefix)
                    self.assertGreaterEqual(threshold, 1)
                    for restricted in product(*(range(1, n+1) for n in prefix)):
                        self.assertGreaterEqual(
                            threshold, 4**(r-2)*(t-1)*sigma(restricted))
                    left = 4*((t-1)*prod(prefix) + sizes[-1]*(threshold-1))
                    right = 4**(r-1)*(t-1)*sigma(sizes)
                    self.assertLessEqual(left, right)

    def test_unbalanced_matching_lower_construction(self):
        """K-free construction realizes at least Sigma_r/r, not a global novelty claim."""
        for sizes in ((1, 2), (1, 7, 3), (2, 3, 5), (1, 4, 9, 2)):
            for t in (2, 3, 5):
                k = sizes.index(min(sizes))
                q = min(sizes[k], t-1)
                families = [[(0, 0)] * n for n in sizes]
                families[k] = [(0, 0)]*q + [(1, 1)]*(sizes[k]-q)
                edges = {
                    idx for idx in product(*(range(n) for n in sizes))
                    if max(families[i][j][0] for i, j in enumerate(idx))
                    <= min(families[i][j][1] for i, j in enumerate(idx))
                }
                self.assertEqual(len(edges), q*prod(n for i, n in enumerate(sizes) if i != k))
                self.assertGreaterEqual(len(edges)*len(sizes), sigma(sizes))
                self.assertTrue(q < t)


if __name__ == "__main__":
    unittest.main()
