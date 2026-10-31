"""Independent finite-run, endpoint and tagged-carrier audit.

Enumerations retain multiplicities. Sorting each family quotients only label
permutations, which preserve every counted predicate; equal entries remain
separate indices. These finite controls do not prove a universal theorem.
"""
GUARDS_CONTRACT = "independent interval-bound audit: sliding windows, tagged carrier, endpoint occurrences"

from itertools import combinations, combinations_with_replacement, product
from math import prod
import unittest


def intervals(order):
    return tuple((a, b) for a in range(order) for b in range(a, order))


def meet(items):
    return max(a for a, _ in items) <= min(b for _, b in items)


def sigma(ns):
    return sum(prod(ns[:i] + ns[i+1:]) for i in range(len(ns)))


def biclique(rows, n, s, t):
    """Rows are bitmasks of labelled neighbors; labels never deduplicated."""
    for selected in combinations(rows, s):
        common = (1 << n)-1
        for row in selected:
            common &= row
        if common.bit_count() >= t:
            return True
    return False


def hyperedges(families):
    return {idx for idx in product(*(range(len(f)) for f in families))
            if meet([f[j] for f, j in zip(families, idx)])}


def complete(es, ns, t):
    return any(all(idx in es for idx in product(*chosen))
               for chosen in product(*(combinations(range(n), t) for n in ns)))


def audit_points(order=3, max_m=5, max_n=3):
    count = eligible = 0
    for m in range(max_m+1):
        for points in combinations_with_replacement(range(order), m):
            for n in range(max_n+1):
                for bs in combinations_with_replacement(intervals(order), n):
                    rows = [sum((1 << j) for j, (a, b) in enumerate(bs) if a <= x <= b)
                            for x in points]
                    e = sum(row.bit_count() for row in rows)
                    for s in range(1, max_m+2):
                        for t in range(1, max_n+2):
                            if biclique(rows, n, s, t):
                                continue
                            eligible += 1
                            assert e <= m*(t-1) + n*(s-1), (points, bs, s, t)
                            # Directly reconstruct the window charging, using
                            # sorted point LABELS, including tied positions.
                            late = 0
                            for a, b in bs:
                                run = [i for i, x in enumerate(points) if a <= x <= b]
                                assert not run or run == list(range(run[0], run[-1]+1))
                                late += max(0, len(run)-s+1)
                            windows = sum(sum(all(a <= points[k] <= b for k in range(i, i+s))
                                              for a, b in bs)
                                          for i in range(max(0, m-s+1)))
                            assert late == windows
                            assert windows <= max(0, m-s+1)*(t-1)
                    count += 1
    return count, eligible


def audit_pairs(order=3, max_size=3):
    count = eligible = 0
    for m in range(max_size+1):
        for aa in combinations_with_replacement(intervals(order), m):
            for n in range(max_size+1):
                for bb in combinations_with_replacement(intervals(order), n):
                    rows = [sum(1 << j for j, B in enumerate(bb) if meet((A, B))) for A in aa]
                    e = sum(row.bit_count() for row in rows)
                    ga = sum(c <= x <= d for A in aa for x in A for c, d in bb)
                    gb = sum(a <= x <= b for B in bb for x in B for a, b in aa)
                    assert ga+gb >= 2*e
                    for s in range(1, max_size+2):
                        for t in range(1, max_size+2):
                            if not biclique(rows, n, s, t):
                                eligible += 1
                                assert e <= 2*(m*(t-1)+n*(s-1)), (aa, bb, s, t)
                                # Test the actual endpoint lift too.
                                lifted = [sum(1 << j for j, (c, d) in enumerate(bb) if c <= x <= d)
                                          for A in aa for x in A]
                                assert not biclique(lifted, n, 2*s-1, t)
                    count += 1
    return count, eligible


def audit_hypergraphs(order=2, shapes=((2, 2, 2), (1, 3, 8), (2, 2, 2, 2))):
    count = eligible = 0
    for ns in shapes:
        choices = [tuple(combinations_with_replacement(intervals(order), n)) for n in ns]
        for families in product(*choices):
            es = hyperedges(families)
            tags = {idx: (max(families[i][j][0] for i, j in enumerate(idx)),
                          min(families[i][j][1] for i, j in enumerate(idx)))
                    for idx in hyperedges(families[:-1])}
            auxiliary = {(*idx, j) for idx, clipped in tags.items()
                         for j, last in enumerate(families[-1]) if meet((clipped, last))}
            assert auxiliary == es
            for t in (2, 3):
                if not complete(es, ns, t):
                    eligible += 1
                    assert len(es) <= 2**(len(ns)-1)*(t-1)*sigma(ns)
                    assert len(es) <= 4**(len(ns)-1)*(t-1)*sigma(ns)
                # Nonvacuous test of the key geometric lifting obligation:
                # for EACH pair of last-part labels take ALL prefix tuples
                # meeting both, restrict to their actual original labels,
                # and check any prefix clique extends to that last pair.
            for last in combinations(range(ns[-1]), 2):
                chosen = [idx for idx, clipped in tags.items()
                          if all(meet((clipped, families[-1][j])) for j in last)]
                restricted = [sorted({idx[i] for idx in chosen}) for i in range(len(ns)-1)]
                for clique in product(*(combinations(labels, 2) for labels in restricted)):
                    if all(idx in tags for idx in product(*clique)):
                        assert all((*idx, j) in es for idx in product(*clique) for j in last)
            count += 1
    return count, eligible


def audit_large_pairs():
    """Some complete graphs in this domain exceed even the original bound."""
    count = eligible = nonvacuous = 0
    for m, n in ((9, 9), (2, 25), (25, 2)):
        for aa in combinations_with_replacement(intervals(2), m):
            for bb in combinations_with_replacement(intervals(2), n):
                rows = [sum(1 << j for j, B in enumerate(bb) if meet((A, B))) for A in aa]
                e = sum(row.bit_count() for row in rows)
                for s in (2, 3):
                    for t in (2, 3):
                        if not biclique(rows, n, s, t):
                            eligible += 1
                            assert e <= 2*(m*(t-1)+n*(s-1))
                            if m*n > 4*(m*(t-1)+n*(s-1)):
                                nonvacuous += 1
                count += 1
    assert nonvacuous > 0
    return count, eligible, nonvacuous


class TestIndependentIntervalAudit(unittest.TestCase):
    def test_points(self):
        """Exhaust sorted labelled multisets on 3 positions, m<=5,n<=3,s<=6,t<=4."""
        self.assertEqual(audit_points()[0], 4704)

    def test_pairs(self):
        """Exhaust size<=3 families on 3 positions, s,t<=4, with endpoint lift."""
        self.assertEqual(audit_pairs()[0], 7056)

    def test_hypergraphs(self):
        """Exhaust 2-position multisets, shapes (2,2,2),(1,3,8),(2,2,2,2)."""
        self.assertEqual(audit_hypergraphs()[0], 2862)

    def test_larger_pairs(self):
        """Exhaust 2-position multisets for (9,9),(2,25),(25,2), s,t=2,3."""
        self.assertEqual(audit_large_pairs()[0], 7237)

    def test_rejected_strengthenings(self):
        """Concrete counterexamples reject missing terms and untagged counting."""
        # One interval covering two labels: K(3,2)-free but e=2>m*(t-1)=0 for t=1.
        rows = [1, 1]
        self.assertFalse(biclique(rows, 1, 3, 1))
        self.assertGreater(2, 2*(1-1))
        # K(2,2)-free intervals can have endpoint K(2s-2,t).
        aa, bb = [(0, 0), (1, 1)], [(0, 0)]*2
        rows = [sum(1 << j for j, B in enumerate(bb) if meet((A, B))) for A in aa]
        lift = [sum(1 << j for j, (c, d) in enumerate(bb) if c <= x <= d)
                for A in aa for x in A]
        self.assertFalse(biclique(rows, 2, 2, 2))
        self.assertTrue(biclique(lift, 2, 2, 2))
        # Repeated singleton labels: deduplicating coordinates on both
        # endpoint sides gives only 3 incidences, below twice the 2 edges.
        aa, bb = [(0, 0)]*2, [(0, 0)]
        e = len(hyperedges((aa, bb)))
        dedup_a = sum(c <= x <= d for x in {x for A in aa for x in A} for c, d in bb)
        dedup_b = sum(a <= x <= b for x in {x for B in bb for x in B} for a, b in aa)
        self.assertEqual(dedup_a + dedup_b, 3)
        self.assertLess(dedup_a + dedup_b, 2*e)
        # Equal intervals produce FOUR occurrences per pair, not exactly two.
        A = B = (0, 1)
        tagged = sum(B[0] <= x <= B[1] for x in A) + sum(A[0] <= x <= A[1] for x in B)
        self.assertEqual(tagged, 4)
        # Geometric intersection dedup loses 3 of 4 distinct prefix tuples.
        families = [[(0, 0)]*2, [(0, 0)]*2, [(0, 0)]]
        self.assertEqual(len(hyperedges(families)), 4)
        # Carrying K(2,2)-freeness unchanged through grouping fails.
        fs = [[(0, 0)], [(0, 0)]*2, [(0, 0)]*2]
        self.assertFalse(complete(hyperedges(fs), (1, 2, 2), 2))
        self.assertTrue(biclique([3, 3], 2, 2, 2))

    def test_unequal_arithmetic(self):
        """Exact recurrence and monotonicity for large highly unequal sizes."""
        for ns in ((1, 10**6, 2), (10**9, 1, 3, 7), (2, 2, 100003, 1, 19)):
            p, z = prod(ns[:-1]), ns[-1]
            self.assertEqual(sigma(ns), p+z*sigma(ns[:-1]))
            for c in (2, 4):
                for t in (2, 3, 17):
                    B = c**(len(ns)-2)*(t-1)*sigma(ns[:-1])
                    self.assertLess(B, B+1)
                    self.assertLessEqual(c*(p*(t-1)+z*B), c**(len(ns)-1)*(t-1)*sigma(ns))


if __name__ == '__main__':
    unittest.main()
