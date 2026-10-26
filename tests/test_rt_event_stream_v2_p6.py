"""External six-influence pinned F5 receipts and higher-face replay conformance.

GUARDS_CONTRACT protects exact bounded trace/certificate semantics only.
No signature, float-training soundness, or general rank-R result is inferred.
"""

import copy
import json
import unittest

from experiments.rt import event_stream_v1 as v1
from experiments.rt.event_stream_v2_p6 import (
    MAX_RECEIPT_BYTES, VERSION, create_receipt, sample_spec,
    validate_spec, verify_receipt,
)
from experiments.rt.p6_lift_pilot import DemandP6, LABELS, N

GUARDS_CONTRACT = "Versioned independent six-influence F5 receipt replay and P6 face admission"


class SixEventReceiptTest(unittest.TestCase):
    TOP = (LABELS,)
    SQUARE = ((0, 1), (2, 3), (4,), (5,))

    def test_v1_is_not_silently_extended(self):
        with self.assertRaises(ValueError):
            v1.sample_spec(6)
        with self.assertRaises(ValueError):
            v1.make_envelope(sample_spec())

    def test_frozen_full_1800_swaps_verified(self):
        spec = sample_spec()
        result = verify_receipt(create_receipt(spec), v1.digest(spec))
        self.assertEqual(result["scope"], "complete")
        self.assertEqual((result["potential_swaps"], result["audited_swaps"],
                          result["admitted_swaps"]), (1800, 1800, 1800))
        self.assertEqual(result["blocked_effects"], 0)

    def test_coupled_and_null_semantics_disagree_with_geometry(self):
        for mode in ("scalar_coupled", "null_defect"):
            with self.subTest(mode=mode):
                spec = sample_spec(mode)
                result = verify_receipt(create_receipt(spec), v1.digest(spec))
                self.assertEqual(result["geometric_passes"], 1800)
                self.assertEqual(result["admitted_swaps"], 1680)
                self.assertEqual(result["blocked_effects"], 120)
                self.assertEqual(result["nonzero_null_residuals"],
                                 120 if mode == "null_defect" else 0)

    def test_rank2_complete_receipt_authorizes_full_p6_top(self):
        spec = sample_spec(direction_rank=2)
        result = verify_receipt(create_receipt(spec), v1.digest(spec),
                                requested_faces=(self.TOP,))
        self.assertEqual(result["direction_rank"], 2)
        self.assertEqual(result["face_witness"]["materialized"],
                         (720, 1800, 1560, 540, 62, 1))
        self.assertTrue(result["face_witness"]["top_admitted"])
        self.assertEqual(result["face_witness"]["betti_F5"],
                         (1, 0, 0, 0, 0, 0))

    def test_four_edge_partial_receipt_certifies_square_not_top(self):
        spec = sample_spec()
        local = DemandP6()
        local.request((self.SQUARE,))
        edges = []
        for face, boundary in local.boundaries.items():
            if len(face) == N - 1:
                endpoints = sorted(tuple(block[0] for block in vertex)
                                   for vertex in boundary)
                edges.append(tuple(endpoints))
        self.assertEqual(len(edges), 4)
        requested = [[list(a), list(b)] for a, b in sorted(edges)]
        report = verify_receipt(create_receipt(spec, requested), v1.digest(spec),
                                requested_faces=(self.SQUARE,), max_cells=9)
        self.assertEqual(report["scope"], "requested-only")
        self.assertEqual(report["audited_swaps"], 4)
        self.assertEqual(report["face_witness"]["materialized"],
                         (4, 4, 1, 0, 0, 0))
        self.assertTrue(report["face_witness"]["requested_admitted"])
        self.assertFalse(report["face_witness"]["top_admitted"])
        with self.assertRaisesRegex(ValueError, "budget"):
            verify_receipt(create_receipt(spec, requested), v1.digest(spec),
                           requested_faces=(self.SQUARE,), max_cells=8)

    def test_forged_record_with_refreshed_checksum_still_fails(self):
        spec = sample_spec("scalar_coupled")
        payload = json.loads(create_receipt(spec))
        record = next(r for r in payload["records"] if not r["effect_equal"])
        record["effect_equal"] = True
        record["admitted"] = True
        record["residual"] = [0] * 8
        payload["records_sha256"] = v1.digest(payload["records"])
        with self.assertRaisesRegex(ValueError, "certificate replay"):
            verify_receipt(v1.encode(payload), v1.digest(spec))

    def test_independent_pin_blocks_modified_program_even_when_rehashed(self):
        original = sample_spec()
        pin = v1.digest(original)
        altered = copy.deepcopy(original)
        altered["updates"][0]["gain"] = 1
        payload = create_receipt(altered)
        with self.assertRaisesRegex(ValueError, "program pin"):
            verify_receipt(payload, pin)

    def test_canonical_format_and_invalid_parameters_fail_closed(self):
        spec = sample_spec()
        receipt = create_receipt(spec, [])
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            verify_receipt(b" " + receipt, v1.digest(spec))
        with self.assertRaises(ValueError):
            verify_receipt(receipt + b"\n", v1.digest(spec))
        with self.assertRaises(ValueError):
            verify_receipt(receipt, "0" * 64)
        with self.assertRaises(ValueError):
            verify_receipt(b"x" * (MAX_RECEIPT_BYTES + 1), v1.digest(spec))
        changed = copy.deepcopy(spec)
        changed["updates"][0]["offset"] = [0] * 8
        with self.assertRaises(ValueError):
            validate_spec(changed)
        changed = copy.deepcopy(spec)
        changed["direction_rank"] = 3
        with self.assertRaises(ValueError):
            validate_spec(changed)
        changed = copy.deepcopy(spec)
        changed["updates"].pop()
        with self.assertRaises(ValueError):
            validate_spec(changed)
        edges = v1.all_edges(6)
        dupe = [[list(a), list(b)] for a, b in [edges[0], edges[0]]]
        with self.assertRaises(ValueError):
            create_receipt(spec, dupe)
        self.assertEqual(VERSION, "rt-route-stream/v2-p6")


if __name__ == "__main__":
    unittest.main()
