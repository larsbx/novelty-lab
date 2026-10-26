"""Contract tests for bounded incremental P6 route receipts and final-seal discipline.

These are exact F5 toy-update checks. SHA-256 chaining does not authenticate
a sender or establish floating-point optimizer semantics.
"""

import copy
import unittest

from experiments.rt import event_stream_v1 as v1
from experiments.rt import event_stream_v2_p6 as v2
from experiments.rt.chunked_replay_p6 import (
    MAX_CHUNK_RECORDS, MAX_FRAME_BYTES, MAX_FRAMES, MAX_STREAM_BYTES,
    _frame, emit_frames, experiment, verify_frames,
)
from experiments.rt.p6_lift_pilot import DemandP6, LABELS, N

GUARDS_CONTRACT = "Canonical bounded P6 chunk transport, linked replay, exact effect admission, EOF completeness"


def rechained(frames):
    """Recompute an attacker's entire chain after tampering with a record."""
    values = [v1.json.loads(frame) for frame in frames]
    prior = v1.digest(values[0])
    for position in range(1, len(values) - 1):
        current = values[position]
        current["previous_sha256"] = prior
        body = {key: val for key, val in current.items() if key != "sha256"}
        current["sha256"] = v1.digest(body)
        prior = current["sha256"]
    tail = values[-1]
    tail["previous_sha256"] = prior
    body = {key: val for key, val in tail.items() if key != "sha256"}
    tail["sha256"] = v1.digest(body)
    return [v1.encode(frame) for frame in values]


class ChunkedP6Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = v2.sample_spec("translations")
        cls.coupled = v2.sample_spec("scalar_coupled")
        cls.full_frames = list(emit_frames(cls.frozen, chunk_size=24))
        cls.coupled_frames = list(emit_frames(cls.coupled, chunk_size=24))
        cls.square = ((0, 1), (2, 3), (4,), (5,))
        c = DemandP6()
        c.request((cls.square,))
        edges = []
        for face, bdry in c.boundaries.items():
            if len(face) == N - 1:
                pair = sorted(tuple(block[0] for block in v) for v in bdry)
                edges.append(tuple(pair))
        cls.square_requests = [[list(a), list(b)] for a, b in sorted(edges)]

    def test_full_stream_seals_all_swaps(self):
        report = verify_frames(iter(self.full_frames), v1.digest(self.frozen))
        self.assertTrue(report["end_of_stream_verified"])
        self.assertEqual(report["audited_swaps"], 1800)
        self.assertEqual(report["admitted_swaps"], 1800)
        self.assertEqual(report["geometric_passes"], 1800)
        self.assertEqual(report["chunks"], 75)
        self.assertEqual(report["scope"], "complete")
        self.assertEqual(len(self.full_frames), 77)

    def test_exact_state_dependent_negative_control(self):
        report = verify_frames(iter(self.coupled_frames), v1.digest(self.coupled))
        self.assertEqual(report["geometric_passes"], 1800)
        self.assertEqual(report["effect_equal"], 1680)
        self.assertEqual(report["blocked_effects"], 120)
        self.assertEqual(report["admitted_swaps"], 1680)

    def test_no_seal_no_acceptance_extra_or_reordered_chunks(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            verify_frames(iter(self.full_frames[:-1]), v1.digest(self.frozen))
        with self.assertRaisesRegex(ValueError, "extra data"):
            verify_frames(iter(self.full_frames + [self.full_frames[-1]]),
                          v1.digest(self.frozen))
        bad = self.full_frames[:]
        bad[1], bad[2] = bad[2], bad[1]
        with self.assertRaisesRegex(ValueError, "sequence"):
            verify_frames(iter(bad), v1.digest(self.frozen))
        bad = self.full_frames[:]
        bad.pop(1)
        with self.assertRaises(ValueError):
            verify_frames(iter(bad), v1.digest(self.frozen))

    def test_forged_effect_with_fully_rehashed_hash_chain_still_fails(self):
        corrupted = [v1.json.loads(frame) for frame in self.coupled_frames]
        victim = next(r for item in corrupted[1:-1] for r in item["records"]
                      if not r["effect_equal"])
        victim["residual"] = [0] * 8
        victim["effect_equal"] = True
        victim["admitted"] = True
        changed = rechained([v1.encode(record) for record in corrupted])
        with self.assertRaisesRegex(ValueError, "exact record replay"):
            verify_frames(iter(changed), v1.digest(self.coupled))

    def test_modified_program_or_noncanonical_header_rejected(self):
        modified = copy.deepcopy(self.frozen)
        modified["updates"][0]["gain"] = 1
        attacker = emit_frames(modified, chunk_size=24)
        with self.assertRaisesRegex(ValueError, "specification pin"):
            verify_frames(attacker, v1.digest(self.frozen))
        frames = self.full_frames[:]
        frames[0] = b" " + frames[0]
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            verify_frames(iter(frames), v1.digest(self.frozen))
        frames = self.full_frames[:]
        frames[0] = frames[0].replace(b'"kind":"header"',
                                      b'"kind":"header","kind":"header"')
        with self.assertRaises(ValueError):
            verify_frames(iter(frames), v1.digest(self.frozen))

    def test_sparse_square_and_top_authority_are_different(self):
        frames = list(emit_frames(self.frozen, requests=self.square_requests,
                                  chunk_size=2))
        report = verify_frames(iter(frames), v1.digest(self.frozen),
                               requested_faces=(self.square,), max_cells=9)
        self.assertEqual(report["audited_swaps"], 4)
        self.assertEqual(report["scope"], "requested-only")
        self.assertEqual(report["chunks"], 2)
        self.assertEqual(report["face_witness"]["materialized"],
                         (4, 4, 1, 0, 0, 0))
        self.assertTrue(report["face_witness"]["requested_admitted"])
        self.assertFalse(report["face_witness"]["top_admitted"])
        with self.assertRaisesRegex(ValueError, "budget"):
            verify_frames(iter(frames), v1.digest(self.frozen),
                          requested_faces=(self.square,), max_cells=8)

    def test_empty_partial_stream_has_header_and_seal_only(self):
        frames = list(emit_frames(self.frozen, requests=[], chunk_size=1))
        self.assertEqual(len(frames), 2)
        report = verify_frames(iter(frames), v1.digest(self.frozen))
        self.assertEqual(report["audited_swaps"], 0)
        self.assertEqual(report["chunks"], 0)
        self.assertEqual(report["scope"], "requested-only")
        self.assertEqual(report["admitted_swaps"], 0)

    def test_one_record_chunks_and_invalid_chunk_sizes(self):
        requests = self.square_requests[:2]
        frames = list(emit_frames(self.frozen, requests=requests, chunk_size=1))
        self.assertEqual(len(frames), 4)
        self.assertEqual(verify_frames(iter(frames), v1.digest(self.frozen))[
            "audited_swaps"], 2)
        for bad in (True, 0, -1, MAX_CHUNK_RECORDS + 1):
            with self.subTest(chunk=bad), self.assertRaises(ValueError):
                list(emit_frames(self.frozen, requests=[], chunk_size=bad))

    def test_strict_frame_byte_limit_and_false_seal(self):
        with self.assertRaisesRegex(ValueError, "oversized"):
            verify_frames(iter([b"x" * (MAX_FRAME_BYTES + 1)]),
                          v1.digest(self.frozen))
        wrong = self.full_frames[:]
        footer = v1.json.loads(wrong[-1])
        footer["summary"]["admitted_swaps"] = 1799
        body = {key: val for key, val in footer.items() if key != "sha256"}
        footer["sha256"] = v1.digest(body)
        wrong[-1] = v1.encode(footer)
        with self.assertRaisesRegex(ValueError, "false audit summary"):
            verify_frames(iter(wrong), v1.digest(self.frozen))

    def test_explicit_finite_boundaries(self):
        self.assertEqual(MAX_FRAMES, 1802)
        self.assertGreater(MAX_STREAM_BYTES, MAX_FRAME_BYTES)
        self.assertEqual(experiment()["full"]["admitted_swaps"], 1800)


if __name__ == "__main__":
    unittest.main()
