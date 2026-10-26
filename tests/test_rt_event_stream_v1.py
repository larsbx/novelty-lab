"""Strict F5 P4/P5 receipt replay, forged record, sparse closure controls.

Checks finite effects only, not program provenance or general training claims.
"""
import copy
import json
import unittest

from experiments.rt.event_stream_v1 import (
    ZERO, all_edges, digest, encode, make_envelope, pilot, sample_spec,
    validate, verify_envelope,
)
from experiments.rt.p4_coherence_pilot import P4

GUARDS_CONTRACT = "Bounded F5 canonical P4/P5 route receipt replay, effect equality and sparse closure"


class EventStreamTest(unittest.TestCase):
    def test_complete_r5_translations(self):
        spec = sample_spec(5, "translations")
        report = verify_envelope(make_envelope(spec), digest(spec))
        self.assertEqual((report["potential_edges"], report["audited_edges"],
                          report["admitted_edges"]), (240, 240, 240))
        self.assertEqual(report["blocked_effect_edges"], 0)
        self.assertIsNone(report["P4_top_cell"])

    def test_coupled_passes_geometry_not_effect(self):
        spec = sample_spec(5, "coupled")
        report = verify_envelope(make_envelope(spec), digest(spec))
        self.assertEqual((report["geometric_edges"], report["admitted_edges"],
                          report["blocked_effect_edges"]), (240, 216, 24))

    def test_null_nonzero_residual_not_zero_effect(self):
        spec = sample_spec(5, "null_defect")
        report = verify_envelope(make_envelope(spec), digest(spec))
        self.assertEqual(report["nonzero_null_residuals"], 24)
        self.assertEqual(report["blocked_effect_edges"], 24)

    def test_four_label_grassmann_complete_top_cell(self):
        spec = sample_spec(4, "translations", 2)
        report = verify_envelope(make_envelope(spec), digest(spec))
        self.assertEqual((report["admitted_edges"], report["P4_admitted_faces"]), (36, 14))
        self.assertTrue(report["P4_top_cell"])

    def test_sparse_request_never_promotes_global_coverage(self):
        spec = sample_spec(5)
        chosen = [[list(a), list(b)] for a, b in all_edges(5)[:2]]
        report = verify_envelope(make_envelope(spec, chosen), digest(spec))
        self.assertEqual(report["scope"], "requested-only")
        self.assertEqual(report["audited_edges"], 2)
        self.assertEqual(report["potential_edges"], 240)
        poly = P4()
        square = next(f for f in poly.cells[2] if len(poly.vertex_sets[f]) == 4)
        requested = [[list(a), list(b)] for a, b in sorted(poly.face_boundaries[square])]
        sp4 = sample_spec(4)
        face_report = verify_envelope(make_envelope(sp4, requested), digest(sp4))
        self.assertEqual(face_report["P4_admitted_faces"], 1)
        self.assertFalse(face_report["P4_top_cell"])

    def test_forged_record_even_with_refreshed_digest_fails(self):
        spec = sample_spec(5, "coupled")
        env = json.loads(make_envelope(spec))
        bad = next(r for r in env["records"] if not r["effect_equal"])
        bad["residual"] = list(ZERO)
        bad["effect_equal"] = True
        bad["admitted"] = True
        env["records_sha256"] = digest(env["records"])
        with self.assertRaisesRegex(ValueError, "certificate replay"):
            verify_envelope(encode(env), digest(spec))

    def test_rehashing_unauthorized_program_does_not_bypass_pinning(self):
        spec = sample_spec(5)
        pin = digest(spec)
        altered = copy.deepcopy(spec)
        altered["updates"][0]["gain"] = 1
        with self.assertRaisesRegex(ValueError, "untrusted program"):
            verify_envelope(make_envelope(altered), pin)

    def test_noncanonical_and_invalid_requests_fail_closed(self):
        spec = sample_spec(5)
        payload = make_envelope(spec)
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            verify_envelope(b' ' + payload, digest(spec))
        edges = all_edges(5)
        repeated = [[list(x), list(y)] for x, y in (edges[0], edges[0])]
        with self.assertRaises(ValueError):
            make_envelope(spec, repeated)
        reversed_request = [[list(y), list(x)] for x, y in [edges[0]]]
        with self.assertRaises(ValueError):
            make_envelope(spec, reversed_request)
        with self.assertRaises(ValueError):
            verify_envelope(payload, "0" * 64)
        with self.assertRaises(ValueError):
            verify_envelope(payload + b'\n', digest(spec))

    def test_invalid_fields_and_null_offsets_fail_closed(self):
        spec = sample_spec(3)
        for value in [0, 2, True, "5"]:
            candidate = copy.deepcopy(spec)
            candidate["field"] = value
            with self.assertRaises(ValueError):
                validate(candidate)
        candidate = copy.deepcopy(spec)
        candidate["updates"][0]["offset"] = list(ZERO)
        with self.assertRaises(ValueError):
            validate(candidate)
        candidate = copy.deepcopy(spec)
        candidate["direction_rank"] = 3
        with self.assertRaises(ValueError):
            validate(candidate)

    def test_bounded_reproducible_driver(self):
        report = pilot()
        self.assertEqual(report["status"], "bounded-experiment")
        self.assertEqual(report["runs"]["coupled_R5"]["blocked_effect_edges"], 24)
        self.assertEqual(report["runs"]["sparse_R5"]["audited_edges"], 2)


if __name__ == "__main__":
    unittest.main()
