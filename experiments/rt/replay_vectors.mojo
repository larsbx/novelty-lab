"""Replay the consumer's immutable 48-vector corpus through vendored Mojo.

Only fixture decoding and assertions live here; every mathematical operation
calls the estate implementation. Expected values come from the independent
upstream Python corpus, also checked by tests/test_mojo_rt_estate.py.
"""
from std.testing import assert_equal, assert_true, assert_false
from std.sys import argv
from finite_exact.fp import Fp, FpField
from projective_limits.hyperbolic_rt import norm8, polar8, spread8, triple_spread_defect
from projective_limits.hyperbolic_rt_batch import spreads_batched


def parse_vec[p: Int64](text: String) raises -> List[Fp[p]]:
    var out = List[Fp[p]]()
    for cell in text.split(","):
        out.append(Fp[p](Int64(Int(cell))))
    assert_equal(len(out), 8)
    return out^


def check_result[p: Int64](actual: Fp[p], expected: String) raises:
    if expected == "rejected":
        assert_false(actual.accepted())
    else:
        assert_true(actual.accepted())
        assert_equal(actual.v, Int64(Int(expected)))


def replay[p: Int64](rows: List[List[String]]) raises:
    var counts = List[Int](length=4, fill=0)
    var xs = List[List[Fp[p]]]()
    var ys = List[List[Fp[p]]]()
    var expected_spreads = List[String]()
    for row in rows:
        if Int(row[1]) != Int(p):
            continue
        var kind = row[0]
        if kind == "norm":
            assert_equal(len(row), 4)
            check_result[p](norm8[FpField[p]](parse_vec[p](row[2])), row[3])
            counts[0] += 1
        elif kind == "polar":
            assert_equal(len(row), 5)
            check_result[p](polar8[FpField[p]](parse_vec[p](row[2]), parse_vec[p](row[3])), row[4])
            counts[1] += 1
        elif kind == "spread":
            assert_equal(len(row), 5)
            var x = parse_vec[p](row[2])
            var y = parse_vec[p](row[3])
            check_result[p](spread8[FpField[p]](x, y), row[4])
            xs.append(x^)
            ys.append(y^)
            expected_spreads.append(row[4])
            counts[2] += 1
        elif kind == "triple":
            assert_equal(len(row), 7)
            assert_true(row[2] == "planar" or row[2] == "nonplanar")
            var actual = triple_spread_defect[FpField[p]](
                Fp[p](Int64(Int(row[3]))), Fp[p](Int64(Int(row[4]))), Fp[p](Int64(Int(row[5])))
            )
            check_result[p](actual, row[6])
            assert_equal(actual.is_zero(), row[2] == "planar")
            counts[3] += 1
        else:
            raise Error("unexpected RT vector kind: " + kind)
    assert_equal(counts[0], 4)
    assert_equal(counts[1], 4)
    assert_equal(counts[2], 6)
    assert_equal(counts[3], 2)
    # Check batch output directly against independently generated expectations,
    # including null lanes, rather than only comparing it to scalar output.
    var batch = spreads_batched[FpField[p]](xs, ys)
    assert_equal(len(batch), len(expected_spreads))
    for i in range(len(batch)):
        check_result[p](batch[i], expected_spreads[i])


def main() raises:
    var path = String("../../tests/fixtures/hyperbolic_rt_v1.txt")
    if len(argv()) > 1:
        path = String(argv()[1])
    var rows = List[List[String]]()
    for raw in open(path, "r").read().split("\n"):
        var line = String(raw)
        if line.byte_length() == 0 or line.startswith("#"):
            continue
        var row = List[String]()
        for cell in line.split("\t"):
            row.append(String(cell))
        assert_true(len(row) >= 4)
        var p = Int(row[1])
        if p != 3 and p != 5 and p != 7:
            raise Error("unexpected prime in RT fixture")
        rows.append(row^)
    assert_equal(len(rows), 48)
    replay[3](rows)
    replay[5](rows)
    replay[7](rows)
    print("[PASS] 48 consumer RT vectors + 18 batched spread expectations (vendored Mojo)")
