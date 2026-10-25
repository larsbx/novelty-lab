"""Consumer execution of byte-identical vendored estate Mojo kernels.

This validates that novelty-lab can *execute* the pinned Mojo/ MAX source,
not merely compare the Python oracle. The run is not a claim-proof oracle:
the finite-math-kernels package and its tests own the mathematical contract.
"""
from std.testing import assert_true, assert_false, assert_equal
from finite_exact.fp import Fp, FpField
from projective_limits.hyperbolic_rt import (
    norm8, polar8, spread8, norm_shell_transport8, equal8, add8,
)
from projective_limits.hyperbolic_rt_batch import spreads_batched
from projective_limits.hyperbolic_rt_max import norm_one_count_max
from projective_limits.gram_geometry import (gram2_determinant8, gram3_determinant8, rank_le_two8, planar_triple_spread_defect8)


def nonnull_axis(i: Int) -> List[Fp[3]]:
    var out = List[Fp[3]]()
    for j in range(8):
        out.append(Fp[3](Int64(1 if j == i else (2 if j == i + 4 else 0))))
    return out^


def null_axis(i: Int) -> List[Fp[3]]:
    var out = List[Fp[3]]()
    for j in range(8):
        out.append(Fp[3](Int64(1 if j == i else 0)))
    return out^


def main() raises:
    var x = nonnull_axis(0)
    var y = nonnull_axis(1)
    assert_true(norm8[FpField[3]](x) == Fp[3](1))
    assert_true(polar8[FpField[3]](x, y) == Fp[3](0))
    assert_true(spread8[FpField[3]](x, y) == Fp[3](1))
    assert_true(equal8[FpField[3]](norm_shell_transport8[FpField[3]](x, y), y))

    var xs = List[List[Fp[3]]]()
    var ys = List[List[Fp[3]]]()
    xs.append(x.copy())
    ys.append(y.copy())
    xs.append(null_axis(0))
    ys.append(y.copy())
    var results = spreads_batched[FpField[3]](xs, ys)
    assert_equal(len(results), 2)
    assert_true(results[0] == Fp[3](1))
    assert_false(results[1].accepted())
    assert_equal(norm_one_count_max[3](2), 2160)
    # Planar incidence is an exterior-rank test, not a Gram-null test.
    var z = nonnull_axis(2)
    var xy = add8[FpField[3]](x, y)
    assert_true(rank_le_two8[FpField[3]](x, y, xy) == Fp[3](1))
    assert_true(planar_triple_spread_defect8[FpField[3]](x, y, xy).is_zero())
    assert_true(gram3_determinant8[FpField[3]](x, y, z) == Fp[3](1))
    var radical = add8[FpField[3]](xy, null_axis(2))
    assert_true(gram3_determinant8[FpField[3]](x, y, radical).is_zero())
    assert_true(rank_le_two8[FpField[3]](x, y, radical) == Fp[3](0))
    assert_false(planar_triple_spread_defect8[FpField[3]](x, y, radical).accepted())
    var tangent = add8[FpField[3]](x, null_axis(2))
    assert_true(gram2_determinant8[FpField[3]](x, tangent).is_zero())
    print("[PASS] vendored Mojo RT, exterior Gram guard, batch spread and MAX census")
