#!/usr/bin/env python3
"""Exhaustive test of the defect rank law (Conjecture 3.8 of paper/associator-defects) over F_ell.

For x, y in C = A_3 of cayley-dickson/v1 with parameters (-1, -1, -1) over F_ell,
let phi(z) = [x, y, z] and Q = span{1, x, y, xy}. When N(xy) != 0,
Fix(Delta(x, y)) = L_xy(ker phi), so rank(Delta - I) = rank(phi). The rank law
is therefore the statement

    rank(phi) = 2 * max(0, dim Q - 2)        for all x, y in C.

Reduction (exact, no sampling): phi and Q are unchanged by x -> lambda x + alpha,
y -> mu y + beta (lambda, mu != 0), because the associator is trilinear and
vanishes on scalars. The pair is also symmetric. So it suffices to take x and y
in distinct points of the projective space of trace-zero elements; scalar x or y,
or y in span{1, x}, gives phi = 0 and dim Q <= 2 (Proposition 3.9). The census
below covers every unordered pair of distinct pure projective points, hence every
pair in C x C.

Usage: rank_law.py [--check]     writes or checks data/n2/rank-law-v1.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import defect_census as C  # noqa: E402

OUT = HERE.parents[1] / "data" / "n2" / "rank-law-v1.json"
ELLS = (3,)


def projective_pure(ell: int) -> list[C.Vec]:
    """One representative per projective point of the trace-zero subspace: first nonzero coordinate 1."""
    reps = []
    for tail in product(range(ell), repeat=C.DIM - 1):
        lead = next((t for t in tail if t), 0)
        if lead == 1:
            reps.append((0,) + tail)
    return reps


def matsub(a: C.Mat, b: C.Mat, ell: int) -> list[list[int]]:
    return [[(a[i][j] - b[i][j]) % ell for j in range(C.DIM)] for i in range(C.DIM)]


def census(ell: int) -> dict:
    points = projective_pure(ell)
    left = {p: C.left(p, ell) for p in points}
    table = Counter()
    for i, x in enumerate(points):
        lx = left[x]
        for y in points[i + 1:]:
            xy = C.mul(x, y, ell)
            phi = matsub(C.matmul(lx, left[y], ell), C.left(xy, ell), ell)
            table[(C.rank((C.BASIS[0], x, y, xy), ell), C.rank(phi, ell))] += 1
    rows = [{"dim_Q": d, "rank_phi": r, "pairs": n} for (d, r), n in sorted(table.items())]
    violations = sum(n for (d, r), n in table.items() if r != 2 * max(0, d - 2))
    return {"ell": ell, "projective_points": len(points), "unordered_pairs": sum(table.values()),
            "strata": rows, "violations": violations}


def render() -> str:
    return json.dumps({"schema": "novelty-lab/n2-rank-law/v1", "model": "cayley-dickson/v1 (-1,-1,-1) mod ell",
                       "statement": "rank([x,y,-]) == 2*max(0, dim span{1,x,y,xy} - 2)",
                       "coverage": "every unordered pair of distinct projective pure points (all pairs up to the exact reduction)",
                       "rows": [census(ell) for ell in ELLS]}, indent=1, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if argv[1:] == ["--check"]:
        current = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print("OK: rank-law census is current" if current else f"stale: {OUT}")
        return 0 if current else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
