"""Exact finite-order regression oracle for interval/box intersection contracts.

Each assertion is a finite labelled combinatorial check, not an accepted
asymptotic theorem. All intervals are closed with integer endpoints.
"""
GUARDS_CONTRACT = "labelled hypergraph intersection, endpoint ties, Helly-2, tagged induction interfaces"

from itertools import combinations, combinations_with_replacement, product
from math import prod
import unittest


def intersect(intervals):
    return max(x[0] for x in intervals) <= min(x[1] for x in intervals)


def boxes_meet(boxes):
    return all(intersect(axis) for axis in zip(*boxes))


def hyperedges(families):
    """Original edges are tuples of part-local labels, not geometric objects."""
    return {
        idx for idx in product(*(range(len(part)) for part in families))
        if intersect([families[i][j] for i, j in enumerate(idx)])
    }


def lambda_raw(families):
    result = []
    for k, part in enumerate(families):
        count = 0
        for anchor, _ in part:
            count += prod(
                sum(lo <= anchor <= hi for lo, hi in other)
                for j, other in enumerate(families) if j != k
            )
        result.append(count)
    return tuple(result)


def lambda_charged(families):
    """Max-left-endpoint witness, with smallest attaining index winning ties."""
    result = []
    for k, part in enumerate(families):
        count = 0
        for anchor, _ in part:
            count += prod(
                sum((lo < anchor <= hi if j < k else lo <= anchor <= hi)
                    for lo, hi in other)
                for j, other in enumerate(families) if j != k
            )
        result.append(count)
    return tuple(result)


def tagged_intersections(families):
    """Tags distinguish identical geometric intersections from different tuples."""
    return {
        idx: (max(families[i][j][0] for i, j in enumerate(idx)),
              min(families[i][j][1] for i, j in enumerate(idx)))
        for idx in product(*(range(len(part)) for part in families))
        if intersect([families[i][j] for i, j in enumerate(idx)])
    }


def auxiliary_edges(families):
    tagged = tagged_intersections(families[:-1])
    return {
        (idx, j)
        for idx, clipped in tagged.items()
        for j, last in enumerate(families[-1])
        if intersect((clipped, last))
    }


def sigma(sizes):
    return sum(prod(v for j, v in enumerate(sizes) if i != j)
               for i in range(len(sizes)))


def has_complete(edge_set, sizes, t):
    if any(n < t for n in sizes):
        return False
    for selections in product(*(combinations(range(n), t) for n in sizes)):
        if all(tuple(idx) in edge_set for idx in product(*selections)):
            return True
    return False


class TestOrderedIntersection(unittest.TestCase):
    """Independent enumeration checks the finite contracts in the survey."""

    def test_raw_witness_fails_with_ties(self):
        """Count one labelled edge versus three raw and one charged witnesses.

        Three identical intervals give raw counts (1, 1, 1) and charged counts
        (1, 0, 0), pinning the tie counterexample and smallest-index repair.
        This single fixture does not establish a universal witness identity.
        """
        families = [[(1, 2)]] * 3
        self.assertEqual(len(hyperedges(families)), 1)
        self.assertEqual(lambda_raw(families), (1, 1, 1))
        self.assertEqual(lambda_charged(families), (1, 0, 0))

    def test_witness_distinct_anchor(self):
        """Compare raw and charged counts with (0, 1, 0) for one triple.

        The unique maximum left endpoint is in part 1; this fixture guards
        agreement of the two witness rules when that anchor has no tie.
        """
        families = [[(0, 5)], [(2, 4)], [(1, 3)]]
        self.assertEqual(lambda_raw(families), (0, 1, 0))
        self.assertEqual(lambda_charged(families), (0, 1, 0))

    def test_charged_identity_exhaustive(self):
        """Compare summed charged witnesses with enumerated labelled edges.

        Exhaust all closed intervals on {1, 2}, allowing repeated labels,
        for sizes (1, 1), (2, 2), (1, 2, 1) and (2, 2, 2). Equality guards
        the tie-broken counting identity on precisely these finite domains.
        """
        # Exhaustive, including repeated labelled intervals from a 2-point order.
        choices = [(1, 1), (1, 2), (2, 2)]
        for sizes in ((1, 1), (2, 2), (1, 2, 1), (2, 2, 2)):
            for flat in product(choices, repeat=sum(sizes)):
                families, cursor = [], 0
                for n in sizes:
                    families.append(flat[cursor:cursor + n])
                    cursor += n
                self.assertEqual(sum(lambda_charged(families)),
                                 len(hyperedges(families)), (sizes, flat))

    def test_tagged_auxiliary_bijection_exhaustive(self):
        """Compare flattened auxiliary edges with original labelled triples.

        Exhaust size-(2, 2, 2) families on {1, 2}; equality of edge sets
        guards the tagged-intersection bijection on this finite domain.
        A repeated-interval fixture also checks that two tags survive even
        when their geometric intersections coincide.
        """
        choices = [(1, 1), (1, 2), (2, 2)]
        for flat in product(choices, repeat=6):
            families = [flat[:2], flat[2:4], flat[4:]]
            self.assertEqual(
                {(*tag, final) for tag, final in auxiliary_edges(families)},
                hyperedges(families))
        self.assertEqual(len(tagged_intersections([[(1, 2), (1, 2)], [(1, 2)]])), 2)

    def test_tensor_cannot_preserve_small_forbidden_clique(self):
        """Compute four original edges, no K(2,2,2), and an auxiliary K(2,2).

        This explicit interval fixture guards a counterexample to transferring
        the same forbidden-clique threshold through naive tensor grouping;
        it does not reject tagged grouping with a separately justified bound.
        """
        # A K2,2 after grouping the first two parts does not force K2,2,2.
        families = [[(1, 1), (2, 2)], [(1, 2), (4, 4)],
                    [(1, 2), (1, 3)]]
        edges = hyperedges(families)
        self.assertEqual(len(edges), 4)
        self.assertFalse(has_complete(edges, (2, 2, 2), 2))
        aux = auxiliary_edges([families[1], families[2], families[0]])
        self.assertTrue(all((tag, i) in aux
                            for tag in ((0, 0), (0, 1)) for i in (0, 1)))

    def test_box_helly_two_exact(self):
        """Compare pairwise box intersection with common triple intersection.

        Exhaust the 8,436 unordered triples with repetition from all 36 boxes
        over the order {1, 2, 3} squared. Boolean equality guards Helly-2 for
        these triples only; it is not a proof for arbitrary box families.
        """
        intervals = [(a, b) for a in range(1, 4) for b in range(a, 4)]
        boxes = tuple(product(intervals, repeat=2))
        self.assertEqual(len(boxes), 36)
        n = 0
        for triple in combinations_with_replacement(boxes, 3):
            pairwise = all(boxes_meet((a, b))
                           for a, b in combinations(triple, 2))
            self.assertEqual(pairwise, boxes_meet(triple))
            n += 1
        self.assertEqual(n, 8436)

    def test_small_interval_bound_only(self):
        """Compare K(2,...,2)-free edge counts with 4**(r-1)*2*Sigma(sizes).

        Exhaust labelled interval families on {1, 2} with sizes (2, 2),
        (2, 2, 2) and (3, 3), and require strict inequality only when no
        forbidden clique exists. This is a bounded inequality sanity check,
        not an exact counting identity or proof of an asymptotic bound.
        """
        # A finite sanity check, not a tight asymptotic bound.
        choices = [(1, 1), (1, 2), (2, 2)]
        for sizes in ((2, 2), (2, 2, 2), (3, 3)):
            for flat in product(choices, repeat=sum(sizes)):
                families, cursor = [], 0
                for n in sizes:
                    families.append(flat[cursor:cursor + n])
                    cursor += n
                es = hyperedges(families)
                if not has_complete(es, sizes, 2):
                    self.assertLess(len(es), 4 ** (len(sizes) - 1) * 2 * sigma(sizes))


if __name__ == "__main__":
    unittest.main()
