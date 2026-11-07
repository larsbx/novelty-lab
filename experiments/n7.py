"""Independent, exact differential oracle for the declared N7 fixtures."""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

from experiments.n2.defect_census import rank

FIXTURE = Path(__file__).resolve().parents[1] / "tests/fixtures/n7_projective_arithmetic_v1.json"
ZERO = (0, 0)
ONE = (1, 0)
STANDARD_FRAME = ((0, 1), (1, 1), (1, 0))


def check(actual, expected, context):
    if actual != expected:
        raise AssertionError(f"{context}: got {actual!r}, expected {expected!r}")


def scale(p, s, x):
    return tuple(s * a % p for a in x)


def add(p, x, y):
    return tuple((a + b) % p for a, b in zip(x, y, strict=True))


def canonical(p, x):
    lead = next((a for a in x if a), 0)
    return scale(p, pow(lead, -1, p), x) if lead else x


def orbits(p, n):
    groups = {}
    for v in product(range(p), repeat=n):
        groups.setdefault(canonical(p, v), set()).add(v)
    for orbit in groups.values():
        for v in orbit:
            check(orbit, {scale(p, s, v) for s in range(1, p)}, ("orbit", v))
    return dict(sorted(groups.items()))


def binary_counts(p, groups, x, y):
    return Counter(add(p, a, b) for a, b in product(groups[x], groups[y]))


def incidence(p, groups, x, y):
    zero = (0,) * len(x)
    if x == zero or y == zero:
        return {y if x == zero else x}
    if x == y:
        return {zero, x} if p > 2 else {zero}
    return {z for z in groups if z not in (zero, x, y) and rank([x, y, z], p) == 2}


def compose(table, left, right):
    return [
        sum(a * b * table[i][j][z] for i, a in enumerate(left) for j, b in enumerate(right)
            if a and b)
        for z in range(len(table))
    ]


def extension_product(x, y):
    a, b = x
    c, d = y
    return ((a * c + 3 * b * d) % 7, (a * d + b * c) % 7)


def extension_checks(groups, fixed):
    # Independent multiplication by exponents of 1+u. Its power list is built
    # by the linear recurrence for multiplication by 1+u, not binary products.
    check(3 in {s * s % 7 for s in range(7)}, False, "u² − 3 has no root")
    powers = [ONE]
    for _ in range(1, 48):
        a, b = powers[-1]
        powers.append(((a + 3 * b) % 7, (a + b) % 7))
    a, b = powers[-1]
    check(((a + 3 * b) % 7, (a + b) % 7), ONE, "power cycle")
    check(set(powers), set().union(*groups.values()) - {ZERO}, "nonzero field elements")
    for (i, x), (j, y) in product(enumerate(powers), repeat=2):
        check(extension_product(x, y), powers[(i + j) % 48], ("extension product", x, y))

    classes = list(groups)
    index = {x: i for i, x in enumerate(classes)}
    table = [[index[canonical(7, extension_product(x, y))] for y in classes] for x in classes]
    for i, j in product(range(len(classes)), repeat=2):
        target = classes[table[i][j]]
        check({extension_product(x, y) for x, y in product(groups[classes[i]], groups[classes[j]])},
              groups[target], ("product orbit", i, j))
    for a in powers:
        # Each vector multiplier, including all six reps of each nonzero class.
        action = [index[canonical(7, extension_product(a, x))] for x in classes]
        check(set(action), set(range(len(classes))), ("class permutation", a))
        for x, y, z in product(range(len(classes)), repeat=3):
            check(fixed[action[x]][action[y]][action[z]], fixed[x][y][z],
                  ("nonzero coefficient transport", a, x, y, z))
    check(table[0], [0] * 9, "zero product row")
    check([row[0] for row in table], [0] * 9, "zero product column")
    return table


def line_arithmetic():
    groups = orbits(7, 2)
    classes = list(groups)
    check((len(classes), sum(map(len, groups.values()))), (9, 49), "F7 domain")
    fixed, raw = [], []
    for x in classes:
        fixed_row, raw_row = [], []
        for y in classes:
            counts = binary_counts(7, groups, x, y)
            support = incidence(7, groups, x, y)
            for z, orbit in groups.items():
                expected = (6 if z == ZERO else 5) if x == y != ZERO else 1
                for out in orbit:
                    # The second count intersects a translated orbit with the first.
                    translated = {tuple((c - b) % 7 for c, b in zip(out, v, strict=True))
                                  for v in groups[y]}
                    check(counts[out], len(groups[x] & translated), ("translated orbit", x, y, out))
                    check(counts[out], expected if z in support else 0, ("coefficient", x, y, out))
            fixed_row.append([counts[z] for z in classes])
            raw_row.append([sum(counts[v] for v in groups[z]) for z in classes])
            check(raw_row[-1], [counts[z] * len(groups[z]) for z in classes], ("raw vs fixed", x, y))
        fixed.append(fixed_row)
        raw.append(raw_row)

    unit = [[int(i == j) for j in range(9)] for i in range(9)]
    check(fixed[0], unit, "additive identity")
    for x, y in product(range(9), repeat=2):
        check(fixed[x][y], fixed[y][x], ("commutativity", x, y))
    def support_row(row):
        return [int(c > 0) for c in row]

    for x, y, z in product(range(9), repeat=3):
        triples = Counter(tuple(sum(coords) % 7 for coords in zip(a, b, c, strict=True))
                          for a, b, c in product(groups[classes[x]], groups[classes[y]], groups[classes[z]]))
        left = compose(fixed, fixed[x][y], unit[z])
        right = compose(fixed, unit[x], fixed[y][z])
        expected = [triples[v] for v in classes]
        check(left, expected, ("left association", x, y, z))
        check(right, expected, ("right association", x, y, z))
        # With nonnegative coefficients, support of composition is set composition.
        check(support_row(compose(fixed, support_row(fixed[x][y]), unit[z])), support_row(expected),
              ("left support association", x, y, z))
        check(support_row(compose(fixed, unit[x], support_row(fixed[y][z]))), support_row(expected),
              ("right support association", x, y, z))

    for x, y in product(range(9), repeat=2):
        check(sum(fixed[x][y]), 1 if x == 0 or y == 0 else 11 if x == y else 6,
              ("zero-multiplier pushforward mass", x, y))
    i, j, k = map(classes.index, ((1, 0), (0, 1), (1, 1)))
    left = compose(raw, raw[i][i], unit[j])
    right = compose(raw, unit[i], raw[i][j])
    check((fixed[i][j][k], raw[i][j][k], raw[0][i][i]), (1, 6, 6), "raw normalization controls")
    check((left[j], right[j]), (36, 216), "raw associativity witness")
    check((compose(fixed, fixed[i][i], unit[j])[j], compose(fixed, unit[i], fixed[i][j])[j]),
          (6, 6), "fixed associativity at the raw witness")
    check((sum(fixed[i][i]), fixed[0][0][0]), (11, 1), "zero multiplier witness")
    binary = orbits(2, 2)
    check(binary_counts(2, binary, ONE, ONE), Counter({ZERO: 1}), "F2 boundary")

    return {"classes": classes, "fixed": fixed, "raw": raw,
            "product": extension_checks(groups, fixed),
            "controls": {
                "raw_associativity": {"inputs": [i, i, j], "output": j, "left": left[j], "right": right[j]},
                "raw_identity": {"input": i, "fixed": fixed[0][i][i], "raw": raw[0][i][i]},
                "fixed_vs_raw": {"inputs": [i, j], "output": k, "fixed": fixed[i][j][k], "raw": raw[i][j][k]},
                "zero_multiplier": {"input": i, "pushforward": sum(fixed[i][i]), "rhs": fixed[0][0][0]},
                "f2_self_sum": {"input": ONE, "output": ZERO, "coefficient": 1},
            }}


def det(x, y):
    return (x[0] * y[1] - x[1] * y[0]) % 7


def frame_basis(zero, one, infinity):
    return scale(7, det(one, zero), infinity), scale(7, det(infinity, one), zero)


def linear_image(columns, x):
    return add(7, scale(7, x[0], columns[0]), scale(7, x[1], columns[1]))


def framed_outputs(columns, x, y):
    u, v = columns
    a, b = det(x, v), det(u, x)
    c, d = det(y, v), det(u, y)
    outputs = ((a * d + b * c) % 7, b * d % 7), (a * c % 7, b * d % 7)
    return tuple(None if w == ZERO else canonical(7, linear_image(columns, w)) for w in outputs)


def chart_outputs(x, y):
    a, b = x
    c, d = y
    infinity = (1, 0)
    if b and d:
        s, t = a * pow(b, -1, 7) % 7, c * pow(d, -1, 7) % 7
        return canonical(7, ((s + t) % 7, 1)), canonical(7, (s * t % 7, 1))
    return (infinity if b or d else None,
            infinity if a and c else None)


def framed_arithmetic():
    groups = orbits(7, 2)
    del groups[ZERO]
    points = list(groups)
    frames = {}
    # Enumerate projectivities independently of the determinant frame decoder.
    for u, v in product(points, (w for w in product(range(7), repeat=2) if w != ZERO)):
        if det(u, v):
            columns = u, v
            image = {x: canonical(7, linear_image(columns, x)) for x in points}
            key = tuple(image[x] for x in STANDARD_FRAME)
            if key in frames:
                raise AssertionError(f"duplicate projectivity for {key}")
            frames[key] = image
    check(set(frames), set(permutations(points, 3)), "all ordered frames")
    table = [[chart_outputs(x, y) for y in points] for x in points]
    for marks, image in frames.items():
        columns = frame_basis(*marks)
        for reps in product(*(groups[mark] for mark in marks)):
            check(canonical(7, sum(frame_basis(*reps), ())), canonical(7, sum(columns, ())),
                  ("frame-mark rescaling", marks, reps))
        for i, x in enumerate(points):
            for j, y in enumerate(points):
                expected = tuple(None if z is None else image[z] for z in table[i][j])
                for a, b in product(groups[image[x]], groups[image[y]]):
                    check(framed_outputs(columns, a, b), expected, ("framed covariance", marks, a, b))
    i, j = map(points.index, ((0, 1), (1, 0)))
    check(table[j][j], (None, (1, 0)), "infinity with itself")
    check(table[i][j], ((1, 0), None), "affine zero with infinity")
    return {"points": points, "standard_frame": STANDARD_FRAME, "standard_outputs": table,
            "frames": len(frames)}


def cross(x, y):
    a, b, c = x
    d, e, f = y
    return ((b * f - c * e) % 3, (c * d - a * f) % 3, (a * e - b * d) % 3)


def plane_geometry():
    groups = orbits(3, 3)
    zero = (0, 0, 0)
    points = [x for x in groups if x != zero]
    check((len(points), sum(map(len, groups.values()))), (13, 27), "F3 domain")
    lines = {n: {x for x in points if sum(a * b for a, b in zip(n, x, strict=True)) % 3 == 0}
             for n in points}
    for n, line in lines.items():
        check(len(line), 4, ("line size", n))
        self_sum = {canonical(3, v) for v in binary_counts(3, groups, n, n)}
        check(self_sum, {zero, n}, ("repeated point support", n))
        check({z for z in points if rank([n, n, z], 3) == 1}, {n}, ("diagonal span", n))
    joins, meets = [], []
    for x, y in combinations(points, 2):
        n = canonical(3, cross(x, y))
        support = {canonical(3, v) for v in binary_counts(3, groups, x, y)}
        check(support, incidence(3, groups, x, y), ("F3 rank support", x, y))
        check(support | {x, y}, lines[n], ("join", x, y))
        for a, b in product(groups[x], groups[y]):
            check(canonical(3, cross(a, b)), n, ("join/meet rescaling", a, b))
        check(lines[x] & lines[y], {n}, ("meet by incidence", x, y))
        check({z for z in points if rank([x, y, z], 3) == 2}, lines[n], ("join by rank", x, y))
        i, j, k = map(points.index, (x, y, n))
        joins.append([i, j, k])
        meets.append([i, j, points.index(next(iter(lines[x] & lines[y])))])
    return {"points_and_dual_normals": points,
            "lines": [sorted(points.index(x) for x in line) for line in lines.values()],
            "joins": joins, "meets": meets}


def build_fixture():
    # JSON-native lists give a single representation for committed and Lean data.
    return json.loads(json.dumps({"schema": "n7-projective-arithmetic/v1",
                                  "f7": line_arithmetic(), "framed_f7": framed_arithmetic(),
                                  "f3": plane_geometry()}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--emit", action="store_true", help="write recomputed fixture to stdout")
    mode.add_argument("--lean-export", type=Path, help="compare a separate Lean computation")
    args = parser.parse_args()
    if args.emit:
        fixture = build_fixture()
        print(json.dumps(fixture, separators=(",", ":"), sort_keys=True))
    elif args.check:
        check(build_fixture(), json.loads(FIXTURE.read_text()), "committed N7 fixture")
        print("N7 exhaustive fixture replay passed")
    else:
        fixture = json.loads(FIXTURE.read_text())
        lean = json.loads(args.lean_export.read_text())
        for section in ("f7", "framed_f7", "f3"):
            check(lean.get(section), {key: value for key, value in fixture[section].items()
                                      if key in LEAN_KEYS[section]}, f"Lean {section} differential")
        print("N7 Lean/Python differential passed")


LEAN_KEYS = {"f7": {"classes", "fixed", "raw", "product"},
             "framed_f7": {"points", "standard_outputs"},
             "f3": {"points_and_dual_normals", "lines", "joins", "meets"}}


if __name__ == "__main__":
    main()
