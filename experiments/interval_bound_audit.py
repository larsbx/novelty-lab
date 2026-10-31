#!/usr/bin/env python3
"""Deterministic bounded audit receipt; not a universal theorem certificate.

No ledger record depends on this experiment. The output gives exact domains
and counts; no random sampling or unreported truncation is used.
"""
import json
from itertools import combinations_with_replacement
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tests'))
from test_interval_bound_audit import (  # noqa: E402
    audit_points, audit_pairs, audit_hypergraphs, audit_large_pairs, intervals, biclique,
)


def counterexamples():
    found = {}
    for m in range(1, 4):
        for n in range(1, 4):
            for ps in combinations_with_replacement(range(3), m):
                for bs in combinations_with_replacement(intervals(3), n):
                    rows = [sum(1 << j for j, (a, b) in enumerate(bs) if a <= x <= b)
                            for x in ps]
                    e = sum(x.bit_count() for x in rows)
                    if not biclique(rows, n, 2, 2) and e > m:
                        found.setdefault('omit_n_s_minus_one', dict(points=ps, intervals=bs,
                                                                  s=2, t=2, edges=e, false_bound=m))
    # Search a too-small endpoint lift: K(s,t)-free does NOT imply that
    # endpoints are K(2s-2,t)-free. Singleton labels retain both occurrences.
    for aa in combinations_with_replacement(intervals(2), 2):
        for bb in combinations_with_replacement(intervals(2), 2):
            rows = [sum(1 << j for j, (c, d) in enumerate(bb)
                        if max(A[0], c) <= min(A[1], d)) for A in aa]
            lift = [sum(1 << j for j, (c, d) in enumerate(bb) if c <= x <= d)
                    for A in aa for x in A]
            if not biclique(rows, 2, 2, 2) and biclique(lift, 2, 2, 2):
                found.setdefault('endpoint_threshold_2s_minus_2', dict(A=aa, B=bb, s=2, t=2))
    assert set(found) == {'omit_n_s_minus_one', 'endpoint_threshold_2s_minus_2'}
    return found


def main():
    receipt = {'scope': 'finite enumerations up to within-family label permutations; repetitions retained',
               'points': {'order_size': 3, 'm': [0, 5], 'n': [0, 3], 's': [1, 6], 't': [1, 4]},
               'pairs': {'order_size': 3, 'm_n': [0, 3], 's_t': [1, 4]},
               'hypergraphs': {'order_size': 2, 'shapes': [[2, 2, 2], [1, 3, 8], [2, 2, 2, 2]], 't': [2, 3]}}
    for name, run in [('points', audit_points), ('pairs', audit_pairs), ('hypergraphs', audit_hypergraphs)]:
        cases, free_checks = run()
        receipt[name].update(configurations=cases, forbidden_free_parameter_checks=free_checks)
    cases, checks, nonvacuous = audit_large_pairs()
    receipt['large_pairs'] = dict(order_size=2, shapes=[[9,9],[2,25],[25,2]],
                                  s_t=[2,3], configurations=cases,
                                  forbidden_free_parameter_checks=checks,
                                  checks_with_complete_graph_exceeding_original_bound=nonvacuous)
    receipt['counterexamples'] = counterexamples()
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
