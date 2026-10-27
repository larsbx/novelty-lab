"""Native consumer of immutable upstream RT route primitives.

Only fixture decoding, bounded context traversal and assertions live here.
All field/vector/Gram/effect/admission mathematics calls the vendored estate.
The temporary TSV is a differential test input, NOT a receipt protocol.
"""
from std.sys import argv
from std.testing import assert_equal, assert_true
from finite_exact.fp import Fp, FpField
from projective_limits.hyperbolic_rt import equal8, sub8, norm8, spread8, valid8
from projective_limits.rt_route import (
    affine_step8, swap_residual8, swap_equal8, certified_swap8, gram2_spread8
)


def fields(line: String, kind: String, count: Int) raises -> List[String]:
    var out = List[String]()
    for cell in line.split("\t"):
        out.append(String(cell))
    assert_equal(len(out), count)
    assert_equal(out[0], kind)
    return out^


def field_values(text: String) raises -> List[Fp[5]]:
    var out = List[Fp[5]]()
    for cell in text.split(","):
        var value = Int(cell)
        assert_true(value >= 0 and value < 5)
        out.append(Fp[5](Int64(value)))
    return out^


def vector(text: String) raises -> List[Fp[5]]:
    var out = field_values(text)
    assert_equal(len(out), 8)
    return out^


def word(text: String) raises -> List[Int]:
    var out = List[Int]()
    var seen = List[Bool](length=6, fill=False)
    for cell in text.split(","):
        var label = Int(cell)
        assert_true(label >= 0 and label < 6)
        assert_true(not seen[label])
        seen[label] = True
        out.append(label)
    assert_equal(len(out), 6)
    return out^


def word_key(route: List[Int]) -> Int:
    var key = 0
    for label in route:
        key = 6 * key + label
    return key


def boolean(text: String) raises -> Bool:
    assert_true(text == "0" or text == "1")
    return text == "1"


def expect_field(value: Fp[5], expected: String) raises:
    if expected == "rejected":
        assert_true(not value.accepted())
    else:
        var number = Int(expected)
        assert_true(number >= 0 and number < 5)
        assert_true(value.accepted())
        assert_equal(value.v, Int64(number))


def member(value: Fp[5], gate: List[Fp[5]]) -> Bool:
    if not value.accepted():
        return False
    for item in gate:
        if value == item:
            return True
    return False


def apply(
    state: List[Fp[5]], label: Int, offsets: List[List[Fp[5]]],
    gains: List[Fp[5]], coords: List[Int], shears: List[List[Fp[5]]]
) -> List[Fp[5]]:
    return affine_step8[FpField[5]](
        state, offsets[label], gains[label], coords[label], shears[label]
    )


def prefix(
    initial: List[Fp[5]], route: List[Int], length: Int,
    offsets: List[List[Fp[5]]], gains: List[Fp[5]],
    coords: List[Int], shears: List[List[Fp[5]]]
) raises -> List[Fp[5]]:
    var state = initial.copy()
    for i in range(length):
        state = apply(state, route[i], offsets, gains, coords, shears)
        assert_true(valid8[FpField[5]](state))
    return state^


def replay_case(rows: List[String], start: Int, case_index: Int) raises:
    var header = fields(rows[start], "case", 4)
    var rank = Int(header[2])
    var expected_mode = String("translations")
    if case_index == 1:
        expected_mode = "scalar_coupled"
    elif case_index == 2:
        expected_mode = "null_defect"
    assert_equal(header[1], expected_mode)
    assert_equal(rank, 2 if case_index == 3 else 1)
    var gate = field_values(header[3])
    assert_equal(header[3], "0,3" if case_index == 2 else "0")
    var initial_row = fields(rows[start + 1], "initial", 2)
    var initial = vector(initial_row[1])
    var offsets = List[List[Fp[5]]]()
    var gains = List[Fp[5]]()
    var coords = List[Int]()
    var shears = List[List[Fp[5]]]()
    for i in range(6):
        var row = fields(rows[start + 2 + i], "update", 6)
        assert_equal(Int(row[1]), i)
        offsets.append(vector(row[2]))
        var gain = Int(row[3])
        var coord = Int(row[4])
        assert_true(gain >= 0 and gain < 5 and coord >= 0 and coord < 8)
        gains.append(Fp[5](Int64(gain)))
        coords.append(coord)
        shears.append(vector(row[5]))
    var seen_routes = List[Bool](length=46656, fill=False)  # 6^6 keys
    for i in range(720):
        var row = fields(rows[start + 8 + i], "route", 3)
        var route = word(row[1])
        var key = word_key(route)
        assert_true(not seen_routes[key])
        seen_routes[key] = True
        var state = prefix(initial, route, 6, offsets, gains, coords, shears)
        assert_true(equal8[FpField[5]](state, vector(row[2])))
    var seen_swaps = List[Bool](length=233280, fill=False)  # 5*6^6
    var geometric = 0
    var effects = 0
    var admitted_count = 0
    var nonzero_null = 0
    for i in range(1800):
        var row = fields(rows[start + 728 + i], "swap", 10)
        var route = word(row[1])
        var position = Int(row[2])
        assert_true(position >= 0 and position < 5)
        var a = route[position]
        var b = route[position + 1]
        assert_true(a < b)  # exactly one orientation per undirected edge
        var key = 5 * word_key(route) + position
        assert_true(not seen_swaps[key])
        seen_swaps[key] = True
        # Replay the ACTUAL common prefix, never a frozen or supplied state.
        var state = prefix(initial, route, position, offsets, gains, coords, shears)
        assert_true(equal8[FpField[5]](state, vector(row[3])))
        var residual = swap_residual8[FpField[5]](
            state, offsets[a], gains[a], coords[a], shears[a],
            offsets[b], gains[b], coords[b], shears[b]
        )
        assert_true(valid8[FpField[5]](residual))
        assert_true(equal8[FpField[5]](residual, vector(row[4])))
        var same = swap_equal8[FpField[5]](
            state, offsets[a], gains[a], coords[a], shears[a],
            offsets[b], gains[b], coords[b], shears[b]
        )
        var after_a = apply(state, a, offsets, gains, coords, shears)
        var after_b = apply(state, b, offsets, gains, coords, shears)
        var ab = apply(after_a, b, offsets, gains, coords, shears)
        var ba = apply(after_b, a, offsets, gains, coords, shears)
        assert_equal(same, equal8[FpField[5]](ab, ba))
        var da = sub8[FpField[5]](after_a, state)
        var da_after = sub8[FpField[5]](ba, after_b)
        var db = sub8[FpField[5]](after_b, state)
        var db_after = sub8[FpField[5]](ab, after_a)
        var aprobe = offsets[(a + 1) % 6].copy()
        var bprobe = offsets[(b + 1) % 6].copy()
        var sa = spread8[FpField[5]](da, da_after)
        var sb = spread8[FpField[5]](db, db_after)
        if rank == 2:
            sa = gram2_spread8[FpField[5]](da, aprobe, da_after, aprobe)
            sb = gram2_spread8[FpField[5]](db, bprobe, db_after, bprobe)
        expect_field(sa, row[5])
        expect_field(sb, row[6])
        var geometry = member(sa, gate) and member(sb, gate)
        var admitted = certified_swap8[FpField[5]](
            state, offsets[a], gains[a], coords[a], shears[a],
            offsets[b], gains[b], coords[b], shears[b],
            gate, rank, aprobe, bprobe
        )
        assert_equal(geometry, boolean(row[7]))
        assert_equal(same, boolean(row[8]))
        assert_equal(admitted, boolean(row[9]))
        assert_equal(admitted, geometry and same)
        if geometry:
            geometric += 1
        if same:
            effects += 1
        if admitted:
            admitted_count += 1
        if not same:
            var n = norm8[FpField[5]](residual)
            assert_true(n.accepted())
            if n.is_zero():
                nonzero_null += 1
    assert_equal(rows[start + 2528], "end")
    assert_equal(geometric, 1800)
    assert_equal(effects, 1680 if case_index == 1 or case_index == 2 else 1800)
    assert_equal(admitted_count, effects)
    assert_equal(nonzero_null, 120 if case_index == 2 else 0)
    print("[PASS]", header[1], "rank", rank, ": 720 routes / 1800 swaps; geometry", geometric,
          "effect/admitted", admitted_count, "nonzero null", nonzero_null)


def main() raises:
    assert_equal(len(argv()), 2)
    var raw = open(String(argv()[1]), "r").read()
    var rows = List[String]()
    for line in raw.split("\n"):
        if line.byte_length() != 0:
            rows.append(String(line))
    assert_equal(len(rows), 1 + 4 * 2529)
    assert_equal(rows[0], "rt-route-differential/v1")
    for case_index in range(4):
        replay_case(rows, 1 + case_index * 2529, case_index)
